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
    # Maharashtra administrative aliases
    "chhatrapati sambhajinagar": "aurangabad",
    "sambhajinagar": "aurangabad",
    "chhatrapati sambhaji nagar": "aurangabad",
    "dharashiv": "osmanabad",
    "ahilyanagar": "ahmednagar",
    "mumbai": "mumbai city",

    # Telangana administrative aliases
    "warangal urban": "hanumakonda",
    "warangal rural": "warangal",
    "kothagudem": "bhadradri kothagudem",
    "bhupalpally": "jayashankar bhupalpally",
    "gadwal": "jogulamba gadwal",
    "asifabad": "kumuram bheem asifabad",
    "malkajgiri": "medchal-malkajgiri",
    "sircilla": "rajanna sircilla",
    "bhongir": "yadadri bhuvanagiri",
    "bhuvanagiri": "yadadri bhuvanagiri",

    # Andhra Pradesh administrative aliases
    "kadapa": "ysr kadapa",
    "ysr": "ysr kadapa",
    "cuddapah": "ysr kadapa",
    "ysr district": "ysr kadapa",
    "anantapur": "ananthapuramu",
    "nellore": "spsr nellore",
    "sri potti sriramulu nellore": "spsr nellore",
    "konaseema": "dr. b.r. ambedkar konaseema",
    "dr. b.r. ambedkar": "dr. b.r. ambedkar konaseema",
    "dr b r ambedkar konaseema": "dr. b.r. ambedkar konaseema",
    "vijayawada": "ntr",
    "ntr district": "ntr",
    "parvathipuram": "parvathipuram manyam",
    "manyam": "parvathipuram manyam",
    "sathya sai": "sri sathya sai",
    "alluri": "alluri sitharama raju",
    "alluri sitarama raju": "alluri sitharama raju",
    "asr district": "alluri sitharama raju",

    # Gujarat administrative aliases
    "ahmedabad": "ahmadabad",
    "kutch": "kachchh",
    "mehsana": "mahesana",
    "the dangs": "dang",
    "dangs": "dang",
    "chhotaudepur": "chhota udepur",
    "chhota udaipur": "chhota udepur",
    "panchmahal": "panch mahals",
    "panchmahals": "panch mahals",
    "dahod": "dohad",
    "banaskantha": "banas kantha",
    "sabarkantha": "sabar kantha",
    "dwarka": "devbhumi dwarka",
    "devbhoomi dwarka": "devbhumi dwarka",
    "somnath": "gir somnath",

    # Haryana administrative aliases
    "gurgaon": "gurugram",
    "mewat": "nuh",
    "sonepat": "sonipat",
    "hissar": "hisar",
    "charki dadri": "charkhi dadri",
    "charkidadri": "charkhi dadri",
    "narnaul": "mahendragarh",
    "mohindergarh": "mahendragarh",

    # Karnataka administrative aliases
    "belgaum": "belagavi",
    "bangalore rural": "bengaluru rural",
    "bangalore urban": "bengaluru urban",
    "bangalore": "bengaluru urban",
    "bengaluru": "bengaluru urban",
    "bellary": "ballari",
    "bijapur": "vijayapura",
    "gulbarga": "kalaburagi",
    "mysore": "mysuru",
    "shimoga": "shivamogga",
    "chikmagalur": "chikkamagaluru",
    "chikmagalore": "chikkamagaluru",
    "chikkamagalur": "chikkamagaluru",
    "chikballapur": "chikkaballapura",
    "chikkaballapur": "chikkaballapura",
    "dakshin kannad": "dakshina kannada",
    "south canara": "dakshina kannada",
    "uttar kannad": "uttara kannada",
    "north canara": "uttara kannada",
    "tumkur": "tumakuru",
    "chamarajanagar": "chamarajanagara",
    "coorg": "kodagu",
    "davangere": "davanagere",
    "ramanagar": "ramanagara",
    "hospet": "vijayanagara",
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
        Supports state-aware filtering (e.g. Telangana vs Maharashtra) while respecting dataset priority.
        """
        if not district or not district.strip():
            return None

        clean_dist = normalize_district_name(district)
        raw_dist = district.strip().lower()
        clean_state = state.strip().lower() if state and state.strip() else None

        # Pass 1: If state is explicitly provided, look for match in datasets belonging to that state
        if clean_state:
            for ds in self.datasets:
                if ds.get("state", "").lower() == clean_state and service in ds.get("supported_services", []):
                    covered = [normalize_district_name(d) for d in ds.get("actual_districts", [])]
                    raw_covered = [d.lower() for d in ds.get("actual_districts", [])]
                    if (clean_dist in covered or raw_dist in raw_covered or
                        any(clean_dist == c or clean_dist in c or c in clean_dist for c in covered) or
                        any(raw_dist == rc or raw_dist in rc or rc in raw_dist for rc in raw_covered)):
                        return ds

        # Pass 2: Fall back across all datasets ordered by priority
        for ds in self.datasets:
            if service in ds.get("supported_services", []):
                # If state was specified, do not accidentally match a different state in Pass 2
                if clean_state and ds.get("state", "").lower() != clean_state:
                    continue
                covered = [normalize_district_name(d) for d in ds.get("actual_districts", [])]
                raw_covered = [d.lower() for d in ds.get("actual_districts", [])]
                if (clean_dist in covered or raw_dist in raw_covered or
                    any(clean_dist == c or clean_dist in c or c in clean_dist for c in covered) or
                    any(raw_dist == rc or raw_dist in rc or rc in raw_dist for rc in raw_covered)):
                    return ds

        # Pass 3: Global district_index fallback if state was not specified
        if not clean_state:
            matched_id = self.district_index.get(clean_dist) or self.district_index.get(raw_dist)
            if not matched_id:
                for d_name, ds_id in self.district_index.items():
                    if d_name in clean_dist or clean_dist in d_name or d_name in raw_dist or raw_dist in d_name:
                        matched_id = ds_id
                        break
            if matched_id:
                for ds in self.datasets:
                    if ds["id"] == matched_id and service in ds.get("supported_services", []):
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
        temperature: float,
        state: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Query regional dataset for crop recommendations based on empirical soil/climate trials or agronomic reference targets.
        Supports state-aware multi-dataset priority (Maharashtra vs Telangana).
        """
        ds = self.get_dataset_for_district(state, district, service="crop")
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
            "state": ds.get("state", "Maharashtra"),
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
        k: Optional[float] = None,
        state: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Query verified or reference district dataset for tested commercial fertilizers,
        recommended micronutrients (Zinc, Sulphur), and extension links.
        Supports state-aware multi-dataset priority (Maharashtra vs Telangana).
        """
        ds = self.get_dataset_for_district(state, district, service="fertilizer")
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

        ds_state = ds.get("state", "Maharashtra")
        if is_primary:
            regional_notes = (
                f"Based on {len(matched_rows)} verified trials in {canonical_district} ({ds_state}) for {crop_name.title()}. "
                f"Most widely used: {primary_fert}."
            )
        else:
            micronutrient_txt = ""
            if avg_zn and avg_s:
                micronutrient_txt = f" Recommended micronutrient baseline: Zn ~{avg_zn} kg/ha, S ~{avg_s} kg/ha."
            if ds_state == "Telangana":
                regional_notes = (
                    f"Telangana Soil Health Reference: {len(matched_rows)} records for {crop_name.title()} in {canonical_district} "
                    f"(Soil Health Card & PJTSAU benchmark). Prevalent fertilizer: {primary_fert}.{micronutrient_txt}"
                )
            elif ds_state == "Andhra Pradesh":
                regional_notes = (
                    f"Andhra Pradesh Soil Health Reference: {len(matched_rows)} records for {crop_name.title()} in {canonical_district} "
                    f"(Soil Health Card & ANGRAU/Dr. YSRHU benchmark). Prevalent fertilizer: {primary_fert}.{micronutrient_txt}"
                )
            elif ds_state == "Gujarat":
                regional_notes = (
                    f"Gujarat Soil Health Reference: {len(matched_rows)} records for {crop_name.title()} in {canonical_district} "
                    f"(Soil Health Card & AAU/JAU/NAU/SDAU benchmark). Prevalent fertilizer: {primary_fert}.{micronutrient_txt}"
                )
            elif ds_state == "Haryana":
                regional_notes = (
                    f"Haryana Soil Health Reference: {len(matched_rows)} records for {crop_name.title()} in {canonical_district} "
                    f"(Soil Health Card & CCS HAU Hisar benchmark). Prevalent fertilizer: {primary_fert}.{micronutrient_txt}"
                )
            elif ds_state == "Karnataka":
                regional_notes = (
                    f"Karnataka Soil Health Reference: {len(matched_rows)} records for {crop_name.title()} in {canonical_district} "
                    f"(Soil Health Card & UAS Bangalore/Dharwad/Shivamogga benchmark). Prevalent fertilizer: {primary_fert}.{micronutrient_txt}"
                )
            else:
                regional_notes = (
                    f"Agronomic Reference: {len(matched_rows)} records for {crop_name.title()} in {canonical_district} ({ds_state}). "
                    f"Prevalent fertilizer: {primary_fert}.{micronutrient_txt}"
                )

        return {
            "matched": True,
            "dataset_id": ds["id"],
            "dataset_level": ds.get("level", "regional_reference"),
            "dataset_name": ds["name"],
            "dataset_source": ds.get("source", ""),
            "district": canonical_district,
            "state": ds_state,
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
        Mappable across Maharashtra and Telangana agro-climatic zones and State Agricultural Universities (SAUs / PJTSAU).
        Includes specialized Rice Pathology protocols referenced from Mendeley Rice Disease Dataset (10.17632/zfwkkdj6dk.1).
        """
        if not district or not district.strip():
            return {
                "is_district_verified": False,
                "dataset_used": "General Plant Pathology Benchmark",
                "advisory": "Standard agricultural university management protocol."
            }

        clean_dist = normalize_district_name(district)
        canonical = district.strip().title()
        clean_state = state.strip().lower() if state and state.strip() else ""
        c_lower = crop.lower().strip()

        # -------------------------------------------------------------
        # TELANGANA STATE AGRO-CLIMATIC ZONES (PJTSAU Jurisdiction)
        # -------------------------------------------------------------
        telangana_north = [
            "adilabad", "nirmal", "kumuram bheem asifabad", "asifabad", "mancherial",
            "nizamabad", "kamareddy", "jagtial", "peddapalli", "karimnagar", "rajanna sircilla", "sircilla"
        ]
        telangana_central = [
            "warangal", "hanumakonda", "warangal urban", "warangal rural", "jangaon",
            "jayashankar bhupalpally", "bhupalpally", "mahabubabad", "mulugu",
            "khammam", "bhadradri kothagudem", "kothagudem"
        ]
        telangana_south = [
            "nalgonda", "suryapet", "yadadri bhuvanagiri", "bhongir", "mahabubnagar",
            "nagarkurnool", "wanaparthy", "jogulamba gadwal", "gadwal", "narayanpet",
            "medak", "sangareddy", "siddipet", "vikarabad", "ranga reddy",
            "medchal-malkajgiri", "malkajgiri", "hyderabad"
        ]

        is_tg_north = any(d in clean_dist for d in telangana_north)
        is_tg_central = any(d in clean_dist for d in telangana_central)
        is_tg_south = any(d in clean_dist for d in telangana_south)
        is_telangana = (clean_state == "telangana") or is_tg_north or is_tg_central or is_tg_south

        if is_telangana:
            # Check for Mendeley Rice Leaf Disease specialization
            is_rice = ("rice" in c_lower or "paddy" in c_lower or "bhat" in c_lower)
            rice_protocol = ""
            if is_rice:
                rice_protocol = (
                    " [Mendeley Rice Pathology Protocol: For Bacterial Leaf Blight, apply Streptocycline @ 1g/10L + Copper Oxychloride @ 30g/10L. "
                    "For Fungal Blast/Brown Spot, spray Tricyclazole 75 WP @ 0.6g/L or Mancozeb @ 2.5g/L. "
                    "For Viral Tungro, control green leafhopper vectors with Dinotefuran 20 SG @ 0.4g/L]."
                )

            if is_tg_north:
                return {
                    "is_district_verified": True,
                    "dataset_level": "regional_reference",
                    "dataset_used": "Northern Telangana Agro-Climatic Advisory (PJTSAU RARS Jagtial / KVK)",
                    "district": canonical,
                    "advisory": (
                        f"Regional Agro-Climatic Advisory for {canonical} District (Northern Telangana Zone - PJTSAU RARS Jagtial jurisdiction): "
                        f"Under local black cotton vertisols and Godavari basin irrigation, inspect {crop} for foliar lesions and root rots during monsoon humidity peaks. "
                        f"Follow PJTSAU package of practices and consult the local Krishi Vigyan Kendra (KVK).{rice_protocol}"
                    )
                }
            elif is_tg_central:
                return {
                    "is_district_verified": True,
                    "dataset_level": "regional_reference",
                    "dataset_used": "Central Telangana Agro-Climatic Advisory (PJTSAU RARS Warangal / Wyra KVK)",
                    "district": canonical,
                    "advisory": (
                        f"Regional Agro-Climatic Advisory for {canonical} District (Central Telangana Zone - PJTSAU RARS Warangal jurisdiction): "
                        f"Watch for foliar blights, fruit rot complexes, and sucking pests on {crop} during warm humid intervals. "
                        f"Implement integrated pest and disease management (IPDM) bulletins from PJTSAU Warangal.{rice_protocol}"
                    )
                }
            else:
                return {
                    "is_district_verified": True,
                    "dataset_level": "regional_reference",
                    "dataset_used": "Southern Telangana Agro-Climatic Advisory (PJTSAU RARS Palem / Rajendranagar)",
                    "district": canonical,
                    "advisory": (
                        f"Regional Agro-Climatic Advisory for {canonical} District (Southern Telangana Zone - PJTSAU Palem / Rajendranagar jurisdiction): "
                        f"Under red chalka soils and semi-arid conditions, monitor {crop} for moisture-stress disease complexes, wilts, and leaf spots. "
                        f"Consult your district Agricultural Officer or PJTSAU extension scientists.{rice_protocol}"
                    )
                }

        # -------------------------------------------------------------
        # ANDHRA PRADESH STATE AGRO-CLIMATIC ZONES (ANGRAU / Dr. YSRHU)
        # -------------------------------------------------------------
        ap_north_coastal = [
            "srikakulam", "vizianagaram", "parvathipuram manyam", "parvathipuram", "manyam",
            "visakhapatnam", "anakapalli", "alluri sitharama raju", "alluri", "asr district"
        ]
        ap_godavari_delta = [
            "east godavari", "kakinada", "dr. b.r. ambedkar konaseema", "konaseema",
            "west godavari", "eluru"
        ]
        ap_krishna_chili = [
            "krishna", "ntr", "vijayawada", "guntur", "bapatla", "palnadu", "prakasam"
        ]
        ap_southern = [
            "spsr nellore", "nellore", "tirupati", "chittoor", "annamayya", "ysr kadapa", "kadapa", "cuddapah"
        ]
        ap_rayalaseema = [
            "kurnool", "nandyal", "ananthapuramu", "anantapur", "sri sathya sai", "sathya sai"
        ]

        is_ap_north = any(d in clean_dist for d in ap_north_coastal)
        is_ap_godavari = any(d in clean_dist for d in ap_godavari_delta)
        is_ap_krishna = any(d in clean_dist for d in ap_krishna_chili)
        is_ap_southern = any(d in clean_dist for d in ap_southern)
        is_ap_rayalaseema = any(d in clean_dist for d in ap_rayalaseema)
        is_andhra = (clean_state in ("andhra pradesh", "ap", "andhra")) or is_ap_north or is_ap_godavari or is_ap_krishna or is_ap_southern or is_ap_rayalaseema

        if is_andhra:
            is_chili = ("chili" in c_lower or "chilli" in c_lower or "mirchi" in c_lower or "pepper" in c_lower)
            chili_protocol = ""
            if is_chili:
                chili_protocol = (
                    " [Mendeley Krishna Basin Chili Pathology Protocol: For Bacterial Spot (Xanthomonas), spray Copper Oxychloride @ 30g + Streptocycline @ 1g/10L. "
                    "For Chili Leaf Curl Virus, control whitefly/thrips vectors with Diafenthiuron 50 WP @ 1.25g/L or Fipronil 5 SC @ 2ml/L and rogue symptomatic plants. "
                    "For Cercospora Leaf Spot, apply Mancozeb 75 WP @ 2.5g/L or Tebuconazole @ 1ml/L. "
                    "For Nutrition Deficiency (interveinal chlorosis), apply multi-micronutrient foliar spray (Formula 4/Zn+Fe+B) @ 2.5g/L. "
                    "For White Spot, ensure proper field drainage and apply Chlorothalonil 75 WP @ 2g/L]."
                )

            if is_ap_krishna:
                return {
                    "is_district_verified": True,
                    "dataset_level": "regional_reference",
                    "dataset_used": "Krishna Basin & Chili Belt Agro-Climatic Advisory (ANGRAU RARS Lam, Guntur)",
                    "district": canonical,
                    "advisory": (
                        f"Regional Agro-Climatic Advisory for {canonical} District (Krishna Delta & Chili Belt Zone - ANGRAU RARS Lam jurisdiction): "
                        f"Under deep black vertisols and Krishna basin irrigation, regularly scout {crop} for sucking pest complexes, virus transmission, and foliar blights. "
                        f"Implement ANGRAU Lam IPM bulletins and consult the district Krishi Vigyan Kendra.{chili_protocol}"
                    )
                }
            elif is_ap_godavari:
                return {
                    "is_district_verified": True,
                    "dataset_level": "regional_reference",
                    "dataset_used": "Godavari Delta Agro-Climatic Advisory (ANGRAU RARS Maruteru / Dr. YSRHU)",
                    "district": canonical,
                    "advisory": (
                        f"Regional Agro-Climatic Advisory for {canonical} District (Godavari Delta Zone - ANGRAU RARS Maruteru & Dr. YSRHU jurisdiction): "
                        f"Under alluvial canal irrigated tracts, monitor {crop} for sheath rot, bacterial lesions, and drainage-related root stress. "
                        f"Follow Dr. YSR Horticultural University & ANGRAU integrated advisories.{chili_protocol}"
                    )
                }
            elif is_ap_north:
                return {
                    "is_district_verified": True,
                    "dataset_level": "regional_reference",
                    "dataset_used": "North Coastal AP Agro-Climatic Advisory (ANGRAU RARS Anakapalle / KVK)",
                    "district": canonical,
                    "advisory": (
                        f"Regional Agro-Climatic Advisory for {canonical} District (North Coastal Zone - ANGRAU RARS Anakapalle jurisdiction): "
                        f"Under high precipitation and red/lateritic soils, inspect {crop} for fungal spots and root rots during monsoon spells. "
                        f"Consult Anakapalle research station or local KVK for preventative spray schedules.{chili_protocol}"
                    )
                }
            elif is_ap_southern:
                return {
                    "is_district_verified": True,
                    "dataset_level": "regional_reference",
                    "dataset_used": "Southern AP Agro-Climatic Advisory (ANGRAU RARS Tirupati / KVK)",
                    "district": canonical,
                    "advisory": (
                        f"Regional Agro-Climatic Advisory for {canonical} District (Southern Zone - ANGRAU RARS Tirupati jurisdiction): "
                        f"In red sandy loams and semi-arid conditions, monitor {crop} for moisture stress, vascular wilt, and leaf spot complexes. "
                        f"Implement ANGRAU Tirupati package of practices.{chili_protocol}"
                    )
                }
            else:
                return {
                    "is_district_verified": True,
                    "dataset_level": "regional_reference",
                    "dataset_used": "Scarce Rainfall Rayalaseema Advisory (ANGRAU RARS Nandyal / KVK)",
                    "district": canonical,
                    "advisory": (
                        f"Regional Agro-Climatic Advisory for {canonical} District (Scarce Rainfall Zone of Rayalaseema - ANGRAU RARS Nandyal jurisdiction): "
                        f"Under drought-prone and rainfed conditions, monitor {crop} for moisture stress, dry root rot, and foliar disease complexes. "
                        f"Consult Nandyal RARS and district KVK scientists.{chili_protocol}"
                    )
                }

        # -------------------------------------------------------------
        # HARYANA STATE AGRO-CLIMATIC ZONES (CCS HAU Hisar)
        # -------------------------------------------------------------
        hr_eastern = [
            "ambala", "panchkula", "yamunanagar", "kurukshetra", "karnal",
            "kaithal", "panipat", "sonipat", "sonepat"
        ]
        hr_western = [
            "hisar", "hissar", "sirsa", "fatehabad", "bhiwani",
            "charkhi dadri", "charki dadri", "rohtak", "jhajjar", "jind"
        ]
        hr_southern = [
            "gurugram", "gurgaon", "faridabad", "rewari", "mahendragarh",
            "narnaul", "palwal", "nuh", "mewat"
        ]

        is_hr_eastern = any(d in clean_dist for d in hr_eastern)
        is_hr_western = any(d in clean_dist for d in hr_western)
        is_hr_southern = any(d in clean_dist for d in hr_southern)
        is_haryana = (clean_state in ("haryana", "hr")) or is_hr_eastern or is_hr_western or is_hr_southern

        if is_haryana:
            # Check for Wheat/Rice/Cotton/Mustard/Solanaceous specialization aligned with CCS HAU Hisar & PlantVillage
            is_wheat_rice = any(w in c_lower for w in ["wheat", "rice", "paddy", "bhat"])
            is_cotton_mustard = any(cm in c_lower for cm in ["cotton", "kapas", "mustard", "raya", "sarson"])
            is_solanaceous = any(sc in c_lower for sc in ["potato", "tomato", "pepper", "chili", "corn", "maize"])

            hau_note = ""
            if is_wheat_rice:
                hau_note = (
                    " [CCS HAU Hisar Cereal Pathology Protocol: For Yellow Rust (Stripe Rust) in Wheat, spray Propiconazole 25 EC (Tilt) @ 1ml/L or Tebuconazole @ 1ml/L water immediately upon symptom onset. "
                    "For Bacterial Leaf Blight in Paddy, apply Streptocycline @ 1g/10L + Copper Oxychloride @ 30g/10L. For Blast, spray Tricyclazole 75 WP @ 0.6g/L]."
                )
            elif is_cotton_mustard:
                hau_note = (
                    " [CCS HAU Hisar Cash Crop Protocol: For Cotton Leaf Curl Virus (CLCuV), strictly manage Whitefly vector using Diafenthiuron 50 WP @ 1.25g/L or Pyriproxyfen 10 EC @ 2ml/L; rogue infected plants. "
                    "For White Rust and Alternaria blight in Mustard, spray Mancozeb 75 WP @ 2g/L or Ridomil MZ @ 2g/L at 50-60 DAS]."
                )
            elif is_solanaceous:
                hau_note = (
                    " [PlantVillage & CCS HAU Vegetable IPM Protocol: For Late Blight in Potato/Tomato, spray Metalaxyl + Mancozeb (Ridomil MZ) @ 2.5g/L or Cymoxanil + Mancozeb @ 2g/L. "
                    "For Tomato Yellow Leaf Curl Virus, control whitefly vectors and install yellow sticky traps]."
                )

            if is_hr_eastern:
                return {
                    "is_district_verified": True,
                    "dataset_level": "regional_reference",
                    "dataset_used": "Eastern Haryana Agro-Climatic Advisory (CCS HAU RRS Karnal / Kaul)",
                    "district": canonical,
                    "advisory": (
                        f"Regional Agro-Climatic Advisory for {canonical} District (Eastern Agrozone - Yamuna Basin - CCS HAU Karnal jurisdiction): "
                        f"Under intensive canal and tubewell irrigated alluvial soils, monitor {crop} fields regularly during humid spells. "
                        f"Implement Chaudhary Charan Singh Haryana Agricultural University (CCS HAU) integrated disease management advisories.{hau_note}"
                    )
                }
            elif is_hr_western:
                return {
                    "is_district_verified": True,
                    "dataset_level": "regional_reference",
                    "dataset_used": "Western Haryana Semi-Arid Advisory (CCS HAU Main Campus Hisar / Sirsa)",
                    "district": canonical,
                    "advisory": (
                        f"Regional Agro-Climatic Advisory for {canonical} District (Western Semi-Arid Cotton-Wheat Belt - CCS HAU Hisar jurisdiction): "
                        f"Under sandy loam to calcareous soils with dry semi-arid conditions, scout {crop} for sucking pest transmission, root rot complexes, and foliar blights. "
                        f"Consult CCS HAU Hisar Directorate of Extension Education and district KVK.{hau_note}"
                    )
                }
            else:
                return {
                    "is_district_verified": True,
                    "dataset_level": "regional_reference",
                    "dataset_used": "Southern Haryana Arid & NCR Advisory (CCS HAU RRS Bawal / KVK)",
                    "district": canonical,
                    "advisory": (
                        f"Regional Agro-Climatic Advisory for {canonical} District (Southern Arid & NCR Zone - CCS HAU RRS Bawal jurisdiction): "
                        f"Under light textured and Aravalli fringe soils, inspect {crop} for moisture-stress disease complexes, collar rot, and rust. "
                        f"Follow CCS HAU Regional Research Station Bawal recommendations.{hau_note}"
                    )
                }

        # -------------------------------------------------------------
        # GUJARAT STATE AGRO-CLIMATIC ZONES (AAU / JAU / NAU / SDAU)
        # -------------------------------------------------------------
        gj_middle = [
            "anand", "kheda", "vadodara", "panch mahals", "panchmahal", "panchmahals",
            "dohad", "dahod", "mahisagar", "chhota udepur", "chhotaudepur"
        ]
        gj_saurashtra = [
            "junagadh", "rajkot", "jamnagar", "porbandar", "amreli", "bhavnagar",
            "surendranagar", "gir somnath", "somnath", "botad", "devbhumi dwarka", "dwarka",
            "morbi", "ahmadabad", "ahmedabad"
        ]
        gj_north = [
            "banas kantha", "banaskantha", "sabar kantha", "sabarkantha", "patan",
            "mahesana", "mehsana", "gandhinagar", "aravalli", "kachchh", "kutch"
        ]
        gj_south = [
            "navsari", "surat", "bharuch", "valsad", "dang", "the dangs", "dangs", "narmada", "tapi"
        ]

        is_gj_middle = any(d in clean_dist for d in gj_middle)
        is_gj_saurashtra = any(d in clean_dist for d in gj_saurashtra)
        is_gj_north = any(d in clean_dist for d in gj_north)
        is_gj_south = any(d in clean_dist for d in gj_south)
        is_gujarat = (clean_state in ("gujarat", "gj")) or is_gj_middle or is_gj_saurashtra or is_gj_north or is_gj_south

        if is_gujarat:
            solanaceous_or_citrus = any(sc in c_lower for sc in ["tomato", "potato", "pepper", "chili", "orange", "citrus", "corn", "maize"])
            pv_note = ""
            if solanaceous_or_citrus:
                pv_note = (
                    " [PlantVillage & SAU IPM Benchmark: For Early/Late Blight in Solanaceous crops, apply Mancozeb 75 WP @ 2.5g/L or Metalaxyl-Mancozeb @ 2g/L. "
                    "For Bacterial Spot, apply Copper Oxychloride @ 30g + Streptocycline @ 1g/10L. "
                    "For Citrus Greening/HLB, manage psyllid vectors with Imidacloprid 17.8 SL @ 0.5ml/L]."
                )

            if is_gj_middle:
                return {
                    "is_district_verified": True,
                    "dataset_level": "regional_reference",
                    "dataset_used": "Middle Gujarat Agro-Climatic Advisory (AAU Anand / KVK)",
                    "district": canonical,
                    "advisory": (
                        f"Regional Agro-Climatic Advisory for {canonical} District (Middle Gujarat Agrozone - AAU Anand jurisdiction): "
                        f"Under alluvial loam (Goradu) and black vertisol soils with Charotar irrigation, monitor {crop} for fungal blights, viral complexes, and root rots during monsoon humidity. "
                        f"Implement Anand Agricultural University integrated crop protection advisories.{pv_note}"
                    )
                }
            elif is_gj_saurashtra:
                return {
                    "is_district_verified": True,
                    "dataset_level": "regional_reference",
                    "dataset_used": "Saurashtra & Coastal Agro-Climatic Advisory (JAU Junagadh / KVK)",
                    "district": canonical,
                    "advisory": (
                        f"Regional Agro-Climatic Advisory for {canonical} District (Saurashtra & Coastal Agrozone - JAU Junagadh jurisdiction): "
                        f"Under medium black calcareous vertisols and coastal semi-arid climate, scout {crop} for collar rot, tikka leaf spot, and sucking pest complexes. "
                        f"Follow Junagadh Agricultural University integrated pest management bulletins.{pv_note}"
                    )
                }
            elif is_gj_north:
                return {
                    "is_district_verified": True,
                    "dataset_level": "regional_reference",
                    "dataset_used": "North Gujarat & Arid Advisory (SDAU Sardarkrushinagar / KVK)",
                    "district": canonical,
                    "advisory": (
                        f"Regional Agro-Climatic Advisory for {canonical} District (North Gujarat & Semi-Arid Agrozone - SDAU jurisdiction): "
                        f"Under sandy loam to light alluvial soils, inspect {crop} for moisture-stress disease complexes, powdery mildew, and blight. "
                        f"Consult Sardarkrushinagar Dantiwada Agricultural University extension scientists.{pv_note}"
                    )
                }
            else:
                return {
                    "is_district_verified": True,
                    "dataset_level": "regional_reference",
                    "dataset_used": "South Gujarat Heavy Rainfall Advisory (NAU Navsari / KVK)",
                    "district": canonical,
                    "advisory": (
                        f"Regional Agro-Climatic Advisory for {canonical} District (South Gujarat Heavy Rainfall Zone - NAU Navsari jurisdiction): "
                        f"Under deep heavy black clay soils and high precipitation, prioritize drainage and preventative fungicide applications on {crop} against anthracnose and rot complexes. "
                        f"Consult Navsari Agricultural University research stations.{pv_note}"
                    )
                }

        # -------------------------------------------------------------
        # KARNATAKA STATE AGRO-CLIMATIC ZONES (UAS Bangalore, Dharwad & Shivamogga)
        # -------------------------------------------------------------
        ka_coastal_malnad = [
            "dakshina kannada", "dakshin kannad", "south canara", "udupi", "uttara kannada",
            "uttar kannad", "north canara", "chikkamagaluru", "chikmagalur", "kodagu",
            "coorg", "shivamogga", "shimoga", "hassan"
        ]
        ka_southern = [
            "bengaluru urban", "bangalore urban", "bangalore", "bengaluru rural", "bangalore rural",
            "ramanagara", "ramanagar", "mandya", "mysuru", "mysore", "chamarajanagara",
            "chamarajanagar", "tumakuru", "tumkur", "kolar", "chikkaballapura", "chikballapur",
            "chitradurga", "davanagere", "davangere"
        ]
        ka_northern = [
            "belagavi", "belgaum", "dharwad", "gadag", "haveri", "bagalkote", "bagalkot",
            "vijayapura", "bijapur", "ballari", "bellary", "vijayanagara", "koppal", "raichur",
            "kalaburagi", "gulbarga", "yadgir", "bidar"
        ]

        is_ka_coastal = any(d in clean_dist for d in ka_coastal_malnad)
        is_ka_southern = any(d in clean_dist for d in ka_southern)
        is_ka_northern = any(d in clean_dist for d in ka_northern)
        is_karnataka = (clean_state in ("karnataka", "ka")) or is_ka_coastal or is_ka_southern or is_ka_northern

        if is_karnataka:
            is_arecanut_plantation = any(p in c_lower for p in ["arecanut", "betel", "coconut", "coffee", "pepper", "rubber"])
            is_chilli_vegetable = any(ch in c_lower for ch in ["chilli", "chili", "pepper", "tomato", "potato", "brinjal", "eggplant"])
            is_cereal_pulse = any(cp in c_lower for cp in ["ragi", "rice", "paddy", "jowar", "sorghum", "tur", "redgram", "cotton", "maize"])

            ka_note = ""
            if is_arecanut_plantation:
                ka_note = (
                    " [Chikkamagaluru & Malnad Arecanut Benchmark (KSNUAHS Shivamogga): For Koleroga / Fruit Rot (Phytophthora meadii), spray 1% Bordeaux mixture with resin adhesive twice (pre-monsoon & 40 days later). "
                    "For Bud Rot, excise decayed tissue and smear 10% Bordeaux paste. For Yellow Leaf Disease, apply balanced NPK + 500g MgSO4 per palm and manage vector populations]."
                )
            elif is_chilli_vegetable:
                ka_note = (
                    " [Krishna Basin & Deccan Plateau Chilli Benchmark (UAS Dharwad): For Bacterial Leaf Spot (Xanthomonas), spray Streptocycline @ 1g/10L + Copper Oxychloride @ 30g/10L. "
                    "For Chilli Leaf Curl Virus (CLCuV), control whitefly/thrips vectors with Diafenthiuron 50 WP @ 1.25g/L; rogue infected plants. "
                    "For Anthracnose fruit rot, apply Azoxystrobin 23 SC @ 1ml/L or Difenoconazole @ 0.5ml/L]."
                )
            elif is_cereal_pulse:
                ka_note = (
                    " [UAS Bangalore & UAS Dharwad Crop Health Protocol: For Blast in Ragi/Paddy, apply Tricyclazole 75 WP @ 0.6g/L or Mancozeb @ 2g/L. "
                    "For Wilt / Stem Rot in Pulses, apply Trichoderma viride seed treatment @ 10g/kg and soil drenching with Carbendazim @ 1g/L]."
                )

            if is_ka_coastal:
                return {
                    "is_district_verified": True,
                    "dataset_level": "regional_reference",
                    "dataset_used": "Coastal & Malnad Agro-Climatic Advisory (KSNUAHS Shivamogga / CPCRI)",
                    "district": canonical,
                    "advisory": (
                        f"Regional Agro-Climatic Advisory for {canonical} District (Coastal & Malnad Heavy Rainfall Zone - KSNUAHS Shivamogga jurisdiction): "
                        f"Under high precipitation and humid tropical plantation conditions, protect {crop} against Phytophthora rot complexes, anthracnose, and fungal foliar blights during monsoon downpours. "
                        f"Implement KSNUAHS Shivamogga package of practices.{ka_note}"
                    )
                }
            elif is_ka_southern:
                return {
                    "is_district_verified": True,
                    "dataset_level": "regional_reference",
                    "dataset_used": "Southern Dry & Transition Agro-Climatic Advisory (UAS Bangalore / GKVK)",
                    "district": canonical,
                    "advisory": (
                        f"Regional Agro-Climatic Advisory for {canonical} District (Southern Dry & Transition Zone - UAS Bangalore GKVK jurisdiction): "
                        f"Under red sandy loam soils and Cauvery basin conditions, monitor {crop} for moisture-stress foliar leaf spots, blast, and viral complexes transmitted by sucking pests. "
                        f"Follow UAS Bangalore integrated pest and disease management bulletins.{ka_note}"
                    )
                }
            else:
                return {
                    "is_district_verified": True,
                    "dataset_level": "regional_reference",
                    "dataset_used": "Northern Dry & Transition Agro-Climatic Advisory (UAS Dharwad / UAS Raichur)",
                    "district": canonical,
                    "advisory": (
                        f"Regional Agro-Climatic Advisory for {canonical} District (Northern Dry & Transition Zone - UAS Dharwad & UAS Raichur jurisdiction): "
                        f"Under deep black vertisols and Krishna-Tungabhadra basin semi-arid climate, scout {crop} for wilt, rust, powdery mildew, and foliar blight complexes. "
                        f"Consult UAS Dharwad / Raichur extension stations and district KVK.{ka_note}"
                    )
                }

        # -------------------------------------------------------------
        # MAHARASHTRA STATE AGRO-CLIMATIC ZONES
        # -------------------------------------------------------------
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
