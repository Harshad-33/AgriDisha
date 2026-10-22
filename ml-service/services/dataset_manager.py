"""
Agricultural Dataset Manager for AgriDisha.
Handles dynamic registration, schema mapping, validation, multi-priority dataset selection,
and district-wise querying across multi-region CSV datasets.

Datasets Supported:
1. Western Maharashtra Agricultural Dataset (Priority 1 - Empirical Verified Trials for 5 districts)
2. Maharashtra State Agricultural Dataset - Expanded Consistent (Priority 2 - Regional Reference for 31 districts)
"""
import os
import json
import logging
import csv
from typing import Dict, Any, List, Optional, Tuple

logger = logging.getLogger("ml_service.dataset_manager")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
REGISTRY_PATH = os.path.join(DATA_DIR, "dataset_registry.json")

DISTRICT_ALIASES = {
    "chhatrapati sambhajinagar": "aurangabad",
    "sambhajinagar": "aurangabad",
    "chhatrapati sambhaji nagar": "aurangabad",
    "dharashiv": "osmanabad",
    "ahilyanagar": "ahmednagar",
    "mumbai": "mumbai city",
}


def normalize_district_name(district: Optional[str]) -> str:
    """Normalize district name and resolve historical/new administrative aliases."""
    if not district:
        return ""
    clean = district.lower().strip()
    # Strip parenthesized text if any, e.g. "Chhatrapati Sambhajinagar (Aurangabad)" -> both parts checked
    for alias, canonical in DISTRICT_ALIASES.items():
        if alias in clean:
            return canonical
    return clean


class DatasetManager:
    _instance: Optional["DatasetManager"] = None

    def __init__(self, registry_path: str = REGISTRY_PATH):
        self.registry_path = registry_path
        self.datasets: List[Dict[str, Any]] = []
        self.dataset_data: Dict[str, List[Dict[str, Any]]] = {}
        self.district_index: Dict[str, str] = {}  # district_lower -> dataset_id
        self.load_registry()

    @classmethod
    def get_instance(cls) -> "DatasetManager":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def load_registry(self) -> None:
        """Load and validate all registered regional datasets respecting priority."""
        self.datasets = []
        self.dataset_data = {}
        self.district_index = {}

        if not os.path.exists(self.registry_path):
            logger.warning("Dataset registry file not found at %s", self.registry_path)
            return

        try:
            with open(self.registry_path, "r", encoding="utf-8") as f:
                registry_json = json.load(f)
                datasets = registry_json.get("datasets", [])
        except Exception as e:
            logger.error("Failed to parse dataset registry JSON: %s", e)
            return

        # Sort by priority ascending (1 = highest priority, e.g. Western Maharashtra empirical)
        sorted_datasets = sorted(datasets, key=lambda d: d.get("priority", 99))

        for ds in sorted_datasets:
            ds_id = ds.get("id")
            rel_file = ds.get("file")
            priority = ds.get("priority", 99)
            if not ds_id or not rel_file:
                continue

            csv_path = os.path.join(DATA_DIR, rel_file)
            if not os.path.exists(csv_path):
                logger.warning("Dataset file %s does not exist for dataset %s", csv_path, ds_id)
                continue

            mapping = ds.get("column_mapping", {})
            rows = self._load_and_validate_csv(csv_path, mapping)
            if rows is None:
                logger.warning("Dataset %s failed schema validation, skipping.", ds_id)
                continue

            # Check actual districts in CSV
            dist_col = mapping.get("district", "District")
            actual_districts = set()
            for r in rows:
                val = r.get(dist_col)
                if val:
                    actual_districts.add(val.strip().title())

            specified_covered = [d.strip().title() for d in ds.get("covered_districts", [])]
            effective_districts = specified_covered if specified_covered else sorted(list(actual_districts))

            ds["actual_districts"] = effective_districts
            ds["total_rows"] = len(rows)
            ds["csv_path"] = csv_path
            self.datasets.append(ds)
            self.dataset_data[ds_id] = rows

            # Index districts without overwriting higher priority datasets
            for d in effective_districts:
                norm_d = normalize_district_name(d)
                if norm_d not in self.district_index:
                    self.district_index[norm_d] = ds_id
                # Also index raw lower
                raw_lower = d.lower()
                if raw_lower not in self.district_index:
                    self.district_index[raw_lower] = ds_id

            logger.info("Successfully loaded regional dataset [%s] (priority %d): %d rows covering %d districts",
                        ds_id, priority, len(rows), len(effective_districts))

    def _load_and_validate_csv(self, file_path: str, mapping: Dict[str, str]) -> Optional[List[Dict[str, Any]]]:
        """Validate header schema and parse CSV rows."""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.DictReader(f)
                headers = set(reader.fieldnames or [])

                # Verify mapped columns exist in CSV
                for role, col_name in mapping.items():
                    if col_name not in headers:
                        logger.error("Schema validation failed: Column '%s' mapped to '%s' not in CSV headers %s",
                                     col_name, role, headers)
                        return None

                rows = list(reader)
                return rows
        except Exception as e:
            logger.error("Failed to read CSV %s: %s", file_path, e)
            return None

    def get_dataset_for_district(self, state: Optional[str], district: Optional[str], service: str = "crop") -> Optional[Dict[str, Any]]:
        """
        Identify whether a verified or reference dataset covers the requested district.
        Returns dataset configuration dict if found and covered, else None.
        """
        if not district or not district.strip():
            return None

        clean_dist = normalize_district_name(district)
        raw_dist = district.strip().lower()

        matched_id = self.district_index.get(clean_dist) or self.district_index.get(raw_dist)

        if not matched_id:
            # Substring scan across indexed districts
            for d_name, ds_id in self.district_index.items():
                if d_name in clean_dist or clean_dist in d_name or d_name in raw_dist or raw_dist in d_name:
                    matched_id = ds_id
                    break

        if not matched_id:
            return None

        for ds in self.datasets:
            if ds["id"] == matched_id:
                if service in ds.get("supported_services", []):
                    return ds
        return None

    def find_crop_matches(
        self,
        district: str,
        n: float,
        p: float,
        k: float,
        ph: float,
        rainfall: float,
        temperature: float
    ) -> Dict[str, Any]:
        """
        Query regional dataset for crop recommendations based on empirical soil/climate trials or agronomic reference targets.
        """
        ds = self.get_dataset_for_district(None, district, service="crop")
        if not ds:
            return {"matched": False}

        ds_id = ds["id"]
        rows = self.dataset_data.get(ds_id, [])
        mapping = ds["column_mapping"]

        dist_col = mapping["district"]
        n_col = mapping["nitrogen"]
        p_col = mapping["phosphorus"]
        k_col = mapping["potassium"]
        ph_col = mapping["ph"]
        crop_col = mapping["crop"]

        clean_dist = normalize_district_name(district)
        raw_dist = district.strip().lower()

        # Filter rows for this district
        dist_rows = []
        for r in rows:
            r_dist = r.get(dist_col, "").strip().lower()
            norm_r = normalize_district_name(r_dist)
            if norm_r == clean_dist or clean_dist in norm_r or norm_r in clean_dist or raw_dist in r_dist or r_dist in raw_dist:
                dist_rows.append(r)

        if not dist_rows:
            return {"matched": False}

        scored_rows = []
        has_climate = ("rainfall" in mapping and "temperature" in mapping)

        if has_climate:
            # Priority 1: Full Empirical Distance with Rainfall & Temperature
            rain_col = mapping["rainfall"]
            temp_col = mapping["temperature"]
            for r in dist_rows:
                try:
                    rn = float(r[n_col])
                    rp = float(r[p_col])
                    rk = float(r[k_col])
                    rph = float(r[ph_col])
                    rrain = float(r[rain_col])
                    rtemp = float(r[temp_col])
                    crop_name = r[crop_col].strip()

                    dn = (n - rn) / 100.0
                    dp = (p - rp) / 50.0
                    dk = (k - rk) / 50.0
                    dph = (ph - rph) / 2.0
                    drain = (rainfall - rrain) / 500.0
                    dtemp = (temperature - rtemp) / 10.0

                    dist = (dn ** 2) * 1.5 + (dp ** 2) + (dk ** 2) + (dph ** 2) * 1.2 + (drain ** 2) * 1.8 + (dtemp ** 2)
                    scored_rows.append((dist, crop_name, None, None))
                except Exception:
                    continue
        else:
            # Priority 2: Regional Reference Distance with NPK, pH, and Micronutrient extraction
            has_zn = "zinc" in mapping
            has_s = "sulphur" in mapping
            zn_col = mapping.get("zinc")
            s_col = mapping.get("sulphur")

            for r in dist_rows:
                try:
                    rn = float(r[n_col])
                    rp = float(r[p_col])
                    rk = float(r[k_col])
                    rph = float(r[ph_col])
                    crop_name = r[crop_col].strip()
                    rzn = float(r[zn_col]) if has_zn and r.get(zn_col) else None
                    rs = float(r[s_col]) if has_s and r.get(s_col) else None

                    dn = (n - rn) / 100.0
                    dp = (p - rp) / 50.0
                    dk = (k - rk) / 50.0
                    dph = (ph - rph) / 2.0

                    dist = (dn ** 2) * 1.5 + (dp ** 2) + (dk ** 2) + (dph ** 2) * 1.5
                    scored_rows.append((dist, crop_name, rzn, rs))
                except Exception:
                    continue

        if not scored_rows:
            return {"matched": False}

        scored_rows.sort(key=lambda x: x[0])

        # Top K nearest neighbor vote (k=25)
        k_neighbors = scored_rows[:25]
        crop_weights: Dict[str, float] = {}
        zinc_vals = []
        sulphur_vals = []

        for dist, crop_name, rzn, rs in k_neighbors:
            weight = 1.0 / (1.0 + dist)
            crop_weights[crop_name] = crop_weights.get(crop_name, 0.0) + weight
            if rzn is not None:
                zinc_vals.append(rzn)
            if rs is not None:
                sulphur_vals.append(rs)

        total_weight = sum(crop_weights.values())
        sorted_crops = sorted(crop_weights.items(), key=lambda x: x[1], reverse=True)

        crop_probs = {c: round(w / total_weight, 4) for c, w in sorted_crops}
        best_crop = sorted_crops[0][0]

        # Soil types observed in this district
        soil_col = mapping.get("soil_color") or mapping.get("soil_type")
        soils = list(set(r.get(soil_col, "").strip() for r in dist_rows if soil_col and r.get(soil_col)))

        canonical_district = dist_rows[0].get(dist_col, district).strip().title()
        is_primary = (ds.get("level") == "verified_primary")

        avg_zn = round(sum(zinc_vals) / len(zinc_vals), 2) if zinc_vals else None
        avg_s = round(sum(sulphur_vals) / len(sulphur_vals), 2) if sulphur_vals else None

        if is_primary:
            regional_notes = (
                f"Verified with {len(dist_rows)} empirical field records from {canonical_district} district ({ds['name']}). "
                f"Prevalent soils: {', '.join(soils[:3])}."
            )
        else:
            zn_str = f", Target Zn: ~{avg_zn} kg/ha" if avg_zn else ""
            s_str = f", S: ~{avg_s} kg/ha" if avg_s else ""
            regional_notes = (
                f"Referenced with {len(dist_rows)} agronomic records from {canonical_district} district ({ds['name']}). "
                f"Prevalent soils: {', '.join(soils[:3])}{zn_str}{s_str}."
            )

        return {
            "matched": True,
            "dataset_id": ds["id"],
            "dataset_level": ds.get("level", "regional_reference"),
            "dataset_name": ds["name"],
            "dataset_source": ds.get("source", ""),
            "district": canonical_district,
            "sample_count": len(dist_rows),
            "top_crop": best_crop,
            "crop_probabilities": crop_probs,
            "soil_types": soils,
            "zinc_target": avg_zn,
            "sulphur_target": avg_s,
            "regional_notes": regional_notes
        }

    def find_fertilizer_matches(
        self,
        district: str,
        crop_name: str,
        soil_color: Optional[str] = None,
        n: Optional[float] = None,
        p: Optional[float] = None,
        k: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Query verified or reference district dataset for tested commercial fertilizers,
        recommended micronutrients (Zinc, Sulphur), and extension links.
        """
        ds = self.get_dataset_for_district(None, district, service="fertilizer")
        if not ds:
            return {"matched": False}

        ds_id = ds["id"]
        rows = self.dataset_data.get(ds_id, [])
        mapping = ds["column_mapping"]

        dist_col = mapping["district"]
        crop_col = mapping["crop"]
        fert_col = mapping["fertilizer"]
        link_col = mapping.get("link")
        soil_col = mapping.get("soil_color") or mapping.get("soil_type")
        zn_col = mapping.get("zinc")
        s_col = mapping.get("sulphur")

        clean_dist = normalize_district_name(district)
        raw_dist = district.strip().lower()
        clean_crop = crop_name.strip().lower()

        # Normalize crop aliases
        crop_aliases = {
            "pigeon peas": "tur",
            "pigeonpeas": "tur",
            "pigeon pea": "tur",
            "arhar": "tur",
            "chickpea": "gram",
            "harbara": "gram",
            "sorghum": "jowar",
            "black gram": "urad",
            "blackgram": "urad",
            "mung bean": "moong",
            "mungbean": "moong",
            "kidney beans": "masoor",
            "lentil": "masoor"
        }
        resolved_crop = crop_aliases.get(clean_crop, clean_crop)

        # Filter rows by district
        district_filtered = []
        for r in rows:
            r_dist = r.get(dist_col, "").strip().lower()
            norm_r = normalize_district_name(r_dist)
            if norm_r == clean_dist or clean_dist in norm_r or norm_r in clean_dist or raw_dist in r_dist or r_dist in raw_dist:
                district_filtered.append(r)

        if not district_filtered:
            return {"matched": False}

        # Filter rows by crop
        matched_rows = []
        for r in district_filtered:
            c_val = r.get(crop_col, "").strip().lower()
            c_alias = crop_aliases.get(c_val, c_val)
            if (c_val == clean_crop or c_alias == resolved_crop or
                resolved_crop in c_val or c_val in resolved_crop or
                clean_crop in c_val or c_val in clean_crop):
                matched_rows.append(r)

        if not matched_rows:
            matched_rows = district_filtered

        # If soil color provided, prioritize matching soil type
        if soil_color and soil_color.strip() and soil_col:
            sc_clean = soil_color.strip().lower()
            exact_soil_rows = [r for r in matched_rows if sc_clean in r.get(soil_col, "").strip().lower() or r.get(soil_col, "").strip().lower() in sc_clean]
            if exact_soil_rows:
                matched_rows = exact_soil_rows

        fert_counts: Dict[str, int] = {}
        links: Dict[str, str] = {}
        soils_seen = set()
        zinc_list = []
        sulphur_list = []

        for r in matched_rows:
            f_val = r.get(fert_col, "").strip()
            if f_val:
                fert_counts[f_val] = fert_counts.get(f_val, 0) + 1
            if link_col and r.get(link_col):
                links[f_val] = r.get(link_col).strip()
            if soil_col and r.get(soil_col):
                soils_seen.add(r.get(soil_col).strip())
            if zn_col and r.get(zn_col):
                try:
                    zinc_list.append(float(r[zn_col]))
                except ValueError:
                    pass
            if s_col and r.get(s_col):
                try:
                    sulphur_list.append(float(r[s_col]))
                except ValueError:
                    pass

        sorted_ferts = sorted(fert_counts.items(), key=lambda x: x[1], reverse=True)
        verified_fert_names = [f[0] for f in sorted_ferts]
        primary_fert = verified_fert_names[0] if verified_fert_names else "Urea / Balanced NPK"
        best_link = links.get(primary_fert) or (list(links.values())[0] if links else None)

        canonical_district = district_filtered[0].get(dist_col, district).strip().title()
        is_primary = (ds.get("level") == "verified_primary")

        avg_zn = round(sum(zinc_list) / len(zinc_list), 1) if zinc_list else None
        avg_s = round(sum(sulphur_list) / len(sulphur_list), 1) if sulphur_list else None

        if is_primary:
            regional_notes = (
                f"Based on {len(matched_rows)} verified trials in {canonical_district} for {crop_name.title()}. "
                f"Most widely used: {primary_fert}."
            )
        else:
            micronutrient_txt = ""
            if avg_zn and avg_s:
                micronutrient_txt = f" Recommended micronutrient baseline: Zn ~{avg_zn} kg/ha, S ~{avg_s} kg/ha."
            regional_notes = (
                f"Agronomic Reference: {len(matched_rows)} records for {crop_name.title()} in {canonical_district}. "
                f"Prevalent fertilizer: {primary_fert}.{micronutrient_txt}"
            )

        return {
            "matched": True,
            "dataset_id": ds["id"],
            "dataset_level": ds.get("level", "regional_reference"),
            "dataset_name": ds["name"],
            "dataset_source": ds.get("source", ""),
            "district": canonical_district,
            "sample_count": len(matched_rows),
            "primary_fertilizer": primary_fert,
            "verified_fertilizers": verified_fert_names[:4],
            "reference_link": best_link,
            "soil_color": list(soils_seen)[0] if soils_seen else "Medium Black",
            "zinc_target": avg_zn,
            "sulphur_target": avg_s,
            "regional_notes": regional_notes
        }

    def get_district_disease_advisory(self, state: Optional[str], district: Optional[str], crop: str, disease: str) -> Dict[str, Any]:
        """
        Generate location-aware pathological and agricultural extension advisory.
        Mappable across Maharashtra agro-climatic zones and State Agricultural Universities (SAUs).
        """
        if not district or not district.strip():
            return {
                "is_district_verified": False,
                "dataset_used": "General Plant Pathology Benchmark",
                "advisory": "Standard agricultural university management protocol."
            }

        clean_dist = normalize_district_name(district)
        canonical = district.strip().title()

        # Priority 1: Western Maharashtra
        western_mh = ["solapur", "kolhapur", "satara", "sangli", "pune"]
        if any(w in clean_dist for w in western_mh):
            return {
                "is_district_verified": True,
                "dataset_level": "verified_primary",
                "dataset_used": "Western Maharashtra Agro-Climatic Advisory (MPKV Rahuri / KVK)",
                "district": canonical,
                "advisory": (
                    f"Verified Agro-Climatic Advisory for {canonical} District (Western Maharashtra Zone): "
                    f"Under local semi-arid/irrigated black soil conditions, monitor {crop} foliage closely. "
                    f"Consult the local Krishi Vigyan Kendra (KVK) or MPKV Rahuri extension officer if symptoms exceed 10% canopy coverage."
                )
            }

        # Vidarbha Zone (PDKV Akola)
        vidarbha_districts = ["nagpur", "akola", "amravati", "buldhana", "washim", "wardha", "yavatmal", "chandrapur", "gadchiroli", "bhandara", "gondia"]
        if any(v in clean_dist for v in vidarbha_districts):
            return {
                "is_district_verified": True,
                "dataset_level": "regional_reference",
                "dataset_used": "Vidarbha Agro-Climatic Pathology Advisory (Dr. PDKV Akola / KVK)",
                "district": canonical,
                "advisory": (
                    f"Regional Agro-Climatic Advisory for {canonical} District (Vidarbha Zone - Dr. PDKV Akola jurisdiction): "
                    f"Scout {crop} fields regularly during monsoon/post-monsoon humidity peaks. "
                    f"Follow Dr. Panjabrao Deshmukh Krishi Vidyapeeth disease management bulletins and consult the district KVK."
                )
            }

        # Marathwada Zone (VNMKV Parbhani)
        marathwada_districts = ["aurangabad", "chhatrapati sambhajinagar", "sambhajinagar", "jalna", "beed", "parbhani", "hingoli", "nanded", "latur", "osmanabad", "dharashiv"]
        if any(m in clean_dist for m in marathwada_districts):
            return {
                "is_district_verified": True,
                "dataset_level": "regional_reference",
                "dataset_used": "Marathwada Agro-Climatic Advisory (VNMKV Parbhani / KVK)",
                "district": canonical,
                "advisory": (
                    f"Regional Agro-Climatic Advisory for {canonical} District (Marathwada Zone - VNMKV Parbhani jurisdiction): "
                    f"Under rainfed vertisol soil conditions, watch for {crop} vascular wilt and foliar spot complexes. "
                    f"Consult Vasantrao Naik Marathwada Krishi Vidyapeeth extension scientists."
                )
            }

        # Konkan Coastal Zone (BSKKV Dapoli)
        konkan_districts = ["ratnagiri", "sindhudurg", "raigad", "thane", "palghar", "mumbai city", "mumbai suburban", "mumbai"]
        if any(k in clean_dist for k in konkan_districts):
            return {
                "is_district_verified": True,
                "dataset_level": "regional_reference",
                "dataset_used": "Konkan Agro-Climatic Advisory (Dr. BSKKV Dapoli / KVK)",
                "district": canonical,
                "advisory": (
                    f"Regional Agro-Climatic Advisory for {canonical} District (Konkan Coastal Zone - Dr. BSKKV Dapoli jurisdiction): "
                    f"Due to heavy maritime precipitation and high humidity, prioritize preventative fungicidal sprays on {crop}. "
                    f"Consult Dr. Balasaheb Sawant Konkan Krishi Vidyapeeth extension stations."
                )
            }

        # North Maharashtra / Khandesh Zone (MPKV Rahuri)
        khandesh_districts = ["nashik", "jalgaon", "dhule", "nandurbar", "ahmednagar", "ahilyanagar"]
        if any(kh in clean_dist for kh in khandesh_districts):
            return {
                "is_district_verified": True,
                "dataset_level": "regional_reference",
                "dataset_used": "North Maharashtra Agro-Climatic Advisory (MPKV Rahuri / KVK)",
                "district": canonical,
                "advisory": (
                    f"Regional Agro-Climatic Advisory for {canonical} District (North Maharashtra / Khandesh Zone): "
                    f"Monitor {crop} crops for foliar blights and powdery mildew in irrigated blocks. "
                    f"Refer to MPKV Rahuri / Regional Agricultural Research Station advisories."
                )
            }

        # General Fallback
        return {
            "is_district_verified": False,
            "dataset_level": "fallback",
            "dataset_used": "General Plant Pathology Benchmark",
            "district": canonical,
            "advisory": f"Advisory for {canonical}: Follow standard state university integrated pest and disease management guidelines."
        }


dataset_manager = DatasetManager.get_instance()
