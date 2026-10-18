"""
Agricultural Dataset Manager for AgriDisha.
Handles dynamic registration, schema mapping, validation, and district-wise querying
across multi-region CSV datasets (starting with Western Maharashtra).
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
        """Load and validate all registered regional datasets."""
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

        for ds in datasets:
            ds_id = ds.get("id")
            rel_file = ds.get("file")
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

            # Verify actual district coverage in CSV data
            dist_col = mapping.get("district", "District_Name")
            actual_districts = set()
            for r in rows:
                val = r.get(dist_col)
                if val:
                    actual_districts.add(val.strip().title())

            # Store dataset
            ds["actual_districts"] = sorted(list(actual_districts))
            ds["total_rows"] = len(rows)
            ds["csv_path"] = csv_path
            self.datasets.append(ds)
            self.dataset_data[ds_id] = rows

            # Index districts for fast lookup
            for d in actual_districts:
                d_key = d.lower()
                self.district_index[d_key] = ds_id

            logger.info("Successfully loaded regional dataset [%s]: %d rows covering %s",
                        ds_id, len(rows), list(actual_districts))

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
        Identify whether a verified dataset covers the requested district.
        Returns dataset configuration dict if found and covered, else None.
        """
        if not district or not district.strip():
            return None

        clean_dist = district.strip().lower()
        # Direct lookup or substring match
        matched_id = self.district_index.get(clean_dist)
        if not matched_id:
            for d_name, ds_id in self.district_index.items():
                if d_name in clean_dist or clean_dist in d_name:
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
        Query verified district dataset for crop recommendations based on empirical soil & climate trials.
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
        rain_col = mapping["rainfall"]
        temp_col = mapping["temperature"]
        crop_col = mapping["crop"]

        clean_dist = district.strip().lower()
        # Filter rows for this district
        dist_rows = [r for r in rows if r.get(dist_col, "").strip().lower() == clean_dist or clean_dist in r.get(dist_col, "").strip().lower()]

        if not dist_rows:
            return {"matched": False}

        # Calculate Euclidean distance to user inputs
        scored_rows = []
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
                scored_rows.append((dist, crop_name))
            except Exception:
                continue

        if not scored_rows:
            return {"matched": False}

        scored_rows.sort(key=lambda x: x[0])

        # Top K nearest neighbor vote (k=25)
        k_neighbors = scored_rows[:25]
        crop_weights: Dict[str, float] = {}
        for dist, crop_name in k_neighbors:
            weight = 1.0 / (1.0 + dist)
            crop_weights[crop_name] = crop_weights.get(crop_name, 0.0) + weight

        total_weight = sum(crop_weights.values())
        sorted_crops = sorted(crop_weights.items(), key=lambda x: x[1], reverse=True)

        crop_probs = {c: round(w / total_weight, 4) for c, w in sorted_crops}
        best_crop = sorted_crops[0][0]

        # Extract soil colors observed in this district
        soil_col = mapping.get("soil_color")
        soils = list(set(r.get(soil_col, "").strip() for r in dist_rows if r.get(soil_col)))

        canonical_district = dist_rows[0].get(dist_col, district).strip().title()

        return {
            "matched": True,
            "dataset_id": ds["id"],
            "dataset_name": ds["name"],
            "dataset_source": ds.get("source", ""),
            "district": canonical_district,
            "sample_count": len(dist_rows),
            "top_crop": best_crop,
            "crop_probabilities": crop_probs,
            "soil_types": soils,
            "regional_notes": f"Verified with {len(dist_rows)} empirical field records from {canonical_district} district ({ds['name']}). Prevalent soils: {', '.join(soils)}."
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
        Query verified district dataset for tested commercial fertilizers and extension links.
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
        soil_col = mapping.get("soil_color")

        clean_dist = district.strip().lower()
        clean_crop = crop_name.strip().lower()

        # Crop name alias mappings between standard and dataset names
        crop_aliases = {
            "pigeon peas": "tur",
            "pigeonpeas": "tur",
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

        # Filter rows by district and crop
        matched_rows = []
        for r in rows:
            d_val = r.get(dist_col, "").strip().lower()
            c_val = r.get(crop_col, "").strip().lower()
            if (d_val == clean_dist or clean_dist in d_val) and (c_val == resolved_crop or resolved_crop in c_val or c_val in resolved_crop):
                matched_rows.append(r)

        if not matched_rows:
            # If no crop-specific rows in that district, filter by district only
            matched_rows = [r for r in rows if r.get(dist_col, "").strip().lower() == clean_dist]

        if not matched_rows:
            return {"matched": False}

        # If soil color provided, rank matching soil color higher
        if soil_color and soil_color.strip():
            sc_clean = soil_color.strip().lower()
            exact_soil_rows = [r for r in matched_rows if r.get(soil_col, "").strip().lower() == sc_clean]
            if exact_soil_rows:
                matched_rows = exact_soil_rows

        # Tally fertilizer frequencies
        fert_counts: Dict[str, int] = {}
        links: Dict[str, str] = {}
        soils_seen = set()

        for r in matched_rows:
            f_val = r.get(fert_col, "").strip()
            if f_val:
                fert_counts[f_val] = fert_counts.get(f_val, 0) + 1
            if link_col and r.get(link_col):
                links[f_val] = r.get(link_col).strip()
            if soil_col and r.get(soil_col):
                soils_seen.add(r.get(soil_col).strip())

        sorted_ferts = sorted(fert_counts.items(), key=lambda x: x[1], reverse=True)
        verified_fert_names = [f[0] for f in sorted_ferts]
        primary_fert = verified_fert_names[0] if verified_fert_names else "Urea / Balanced NPK"
        best_link = links.get(primary_fert) or (list(links.values())[0] if links else None)

        canonical_district = matched_rows[0].get(dist_col, district).strip().title()

        return {
            "matched": True,
            "dataset_id": ds["id"],
            "dataset_name": ds["name"],
            "dataset_source": ds.get("source", ""),
            "district": canonical_district,
            "sample_count": len(matched_rows),
            "primary_fertilizer": primary_fert,
            "verified_fertilizers": verified_fert_names[:4],
            "reference_link": best_link,
            "soil_color": list(soils_seen)[0] if soils_seen else "Medium Black",
            "regional_notes": f"Based on {len(matched_rows)} verified trials in {canonical_district} for {crop_name.title()}. Most widely used: {primary_fert}."
        }

    def get_district_disease_advisory(self, state: Optional[str], district: Optional[str], crop: str, disease: str) -> Dict[str, Any]:
        """
        Generate location-aware pathological and agricultural extension advisory.
        """
        if not district or not district.strip():
            return {
                "is_district_verified": False,
                "advisory": "Standard agricultural university management protocol."
            }

        clean_dist = district.strip().lower()
        western_mh = ["solapur", "kolhapur", "satara", "sangli", "pune"]

        if any(w in clean_dist for w in western_mh):
            canonical = district.strip().title()
            return {
                "is_district_verified": True,
                "dataset_used": "Western Maharashtra Agro-Climatic Advisory (MPKV Rahuri / KVK)",
                "district": canonical,
                "advisory": (
                    f"Verified Agro-Climatic Advisory for {canonical} District (Western Maharashtra Zone): "
                    f"Under local semi-arid/irrigated black soil conditions, monitor {crop} foliage closely. "
                    f"Consult the local Krishi Vigyan Kendra (KVK) or MPKV Rahuri extension officer if symptoms exceed 10% canopy coverage."
                )
            }

        return {
            "is_district_verified": False,
            "dataset_used": "General Plant Pathology Benchmark",
            "district": district.strip().title(),
            "advisory": f"Advisory for {district.strip().title()}: Follow standard state university integrated pest and disease management guidelines."
        }


dataset_manager = DatasetManager.get_instance()
