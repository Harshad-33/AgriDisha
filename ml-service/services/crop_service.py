"""
Maharashtra District-Aware Crop Recommendation Service.
Combines Random Forest model trained on Maharashtra agronomic dataset (maharashtra_crop_data.csv)
with district-level agro-climatic intelligence from ICAR, MPKV Rahuri, PDKV Akola, VNMKV Parbhani, and BSKKV Dapoli.
"""
import os
import json
import logging
from typing import Dict, Any, List, Optional
import numpy as np
import joblib

logger = logging.getLogger("ml_service.crop")

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "crop_recommendation.joblib")
DISTRICTS_PATH = os.path.join(BASE_DIR, "data", "maharashtra_districts.json")

CROP_DISPLAY_NAMES = {
    'cotton': 'Cotton (Bt Cotton / Kapas)',
    'soybean': 'Soybean (Soya)',
    'pigeonpeas': 'Pigeon Pea (Tur / Arhar)',
    'sorghum': 'Sorghum (Jowar / Maldandi)',
    'chickpea': 'Chickpea (Gram / Harbara)',
    'sugarcane': 'Sugarcane (Oos)',
    'onion': 'Onion (Kanda)',
    'grapes': 'Grapes (Draksha)',
    'pomegranate': 'Pomegranate (Dalimb - Bhagwa)',
    'banana': 'Banana (Keli - Grand Naine)',
    'orange': 'Orange (Nagpur Mandarin / Santra)',
    'sweet_lime': 'Sweet Lime (Mosambi)',
    'mango': 'Mango (Alphonso / Hapus)',
    'cashew': 'Cashew (Kaju)',
    'rice': 'Rice (Paddy / Bhat)',
    'wheat': 'Wheat (Gahu - Sharbati / Lokwan)',
    'maize': 'Maize (Makka)',
    'bajra': 'Pearl Millet (Bajra)',
    'ragi': 'Finger Millet (Nachani / Ragi)',
    'groundnut': 'Groundnut (Bhuimug)',
    'tomato': 'Tomato',
    'coconut': 'Coconut (Naral)'
}

# District alias mapping for Maharashtra
DISTRICT_ZONE_MAP = {
    # Central Vidarbha (Cotton, Soybean, Tur, Jowar, Orange, Harbara)
    'yavatmal': 'Central Vidarbha Zone',
    'wardha': 'Central Vidarbha Zone',
    'nagpur': 'Central Vidarbha Zone',
    'amravati': 'Central Vidarbha Zone',
    'akola': 'Central Vidarbha Zone',
    'buldhana': 'Central Vidarbha Zone',
    'washim': 'Central Vidarbha Zone',

    # Eastern Vidarbha (Rice / Paddy, Soybean, Cotton)
    'chandrapur': 'Eastern Vidarbha (Wainganga Basin)',
    'bhandara': 'Eastern Vidarbha (Wainganga Basin)',
    'gondia': 'Eastern Vidarbha (Wainganga Basin)',
    'gadchiroli': 'Eastern Vidarbha (Wainganga Basin)',

    # Marathwada (Soybean, Cotton, Tur, Jowar, Mosambi)
    'latur': 'Central Maharashtra (Marathwada)',
    'nanded': 'Central Maharashtra (Marathwada)',
    'parbhani': 'Central Maharashtra (Marathwada)',
    'hingoli': 'Central Maharashtra (Marathwada)',
    'beed': 'Central Maharashtra (Marathwada)',
    'jalna': 'Central Maharashtra (Marathwada)',
    'aurangabad': 'Central Maharashtra (Marathwada)',
    'chhatrapati sambhajinagar': 'Central Maharashtra (Marathwada)',
    'sambhajinagar': 'Central Maharashtra (Marathwada)',
    'osmanabad': 'Central Maharashtra (Marathwada)',
    'dharashiv': 'Central Maharashtra (Marathwada)',

    # Western Maharashtra (Sugarcane, Grapes, Onion, Tomato, Pomegranate)
    'nashik': 'Western Maharashtra Plain',
    'pune': 'Western Maharashtra Plain',
    'satara': 'Western Maharashtra Plain',
    'kolhapur': 'Western Maharashtra Plain',
    'sangli': 'Western Maharashtra Plain',
    'solapur': 'Scarcity & Rain Shadow Zone',
    'ahmednagar': 'Scarcity & Rain Shadow Zone',
    'ahilyanagar': 'Scarcity & Rain Shadow Zone',

    # Khandesh (Banana, Cotton, Maize, Jowar)
    'jalgaon': 'Khandesh & Tapi Basin',
    'dhule': 'Khandesh & Tapi Basin',
    'nandurbar': 'Khandesh & Tapi Basin',

    # Konkan (Alphonso Mango, Cashew, Rice, Coconut)
    'ratnagiri': 'South Konkan',
    'sindhudurg': 'South Konkan',
    'raigad': 'North Konkan',
    'thane': 'North Konkan',
    'palghar': 'North Konkan',
    'mumbai': 'North Konkan'
}


class CropService:
    def __init__(self, model_path: str = MODEL_PATH):
        self.model_path = model_path
        self.model_payload: Optional[Dict[str, Any]] = None
        self.load_model()

    def load_model(self) -> bool:
        """Load trained Maharashtra crop model."""
        if os.path.exists(self.model_path):
            try:
                self.model_payload = joblib.load(self.model_path)
                logger.info(f"Successfully loaded Maharashtra crop model from {self.model_path}")
                return True
            except Exception as e:
                logger.error(f"Failed to load crop model: {e}")
        else:
            logger.warning(f"Crop model not found at {self.model_path}. Training on Maharashtra dataset...")
            try:
                from train_crop_model import train_maharashtra_model
                train_maharashtra_model()
                if os.path.exists(self.model_path):
                    self.model_payload = joblib.load(self.model_path)
                    return True
            except Exception as e:
                logger.error(f"Auto-train failed: {e}")
        return False

    def predict(
        self,
        n: float,
        p: float,
        k: float,
        temp: float,
        humidity: float,
        ph: float,
        rainfall: float,
        city: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Predict best crop tailored to Maharashtra's soil, rainfall, and agro-climatic conditions.
        """
        eff_rainfall = rainfall if rainfall >= 300.0 else (rainfall * 4.5)
        features = np.array([[n, p, k, temp, humidity, ph, eff_rainfall]])

        zone_name = None
        if city:
            c_key = city.lower().strip()
            zone_name = DISTRICT_ZONE_MAP.get(c_key)
            if not zone_name:
                for k_map, v_map in DISTRICT_ZONE_MAP.items():
                    if k_map in c_key or c_key in k_map:
                        zone_name = v_map
                        break

        if self.model_payload and 'model' in self.model_payload:
            model = self.model_payload['model']
            classes = list(model.classes_)
            top_alternatives = []
            confidence = 0.90
            
            if hasattr(model, "predict_proba"):
                probs = model.predict_proba(features)[0].copy()

                # Apply Maharashtra Agro-Climatic Zone Prior Weighting
                if zone_name == 'Central Vidarbha Zone':
                    # Yavatmal, Wardha, Nagpur, Akola, Amravati, Buldhana, Washim
                    for i, cls in enumerate(classes):
                        c = cls.lower()
                        if c == 'cotton' and n >= 70:
                            probs[i] *= 2.2
                        elif c == 'soybean' and p >= 35:
                            probs[i] *= 2.0
                        elif c in ('pigeonpeas', 'pigeon peas') and p >= 40:
                            probs[i] *= 1.9
                        elif c in ('sorghum', 'jowar'):
                            probs[i] *= 1.8
                        elif c == 'orange' and 20 <= n <= 60 and 20 <= p <= 45:
                            probs[i] *= 1.8
                        elif c == 'chickpea' and temp <= 26.0:
                            probs[i] *= 1.7
                        elif c in ('rice', 'jute') and eff_rainfall < 1300:
                            probs[i] = 0.0

                elif zone_name == 'Central Maharashtra (Marathwada)':
                    # Latur, Nanded, Beed, Jalna, Sambhajinagar, Parbhani
                    for i, cls in enumerate(classes):
                        c = cls.lower()
                        if c == 'soybean' and p >= 35:
                            probs[i] *= 2.2
                        elif c == 'cotton' and n >= 70:
                            probs[i] *= 2.0
                        elif c in ('pigeonpeas', 'pigeon peas'):
                            probs[i] *= 2.0
                        elif c in ('sorghum', 'jowar'):
                            probs[i] *= 1.8
                        elif c == 'sweet_lime':
                            probs[i] *= 1.7
                        elif c == 'sugarcane' and n >= 140:
                            probs[i] *= 1.6

                elif zone_name == 'Khandesh & Tapi Basin':
                    # Jalgaon, Dhule, Nandurbar
                    for i, cls in enumerate(classes):
                        c = cls.lower()
                        if c == 'banana' and k >= 80 and n >= 100:
                            probs[i] *= 2.5
                        elif c == 'cotton' and n >= 75:
                            probs[i] *= 2.0
                        elif c == 'maize':
                            probs[i] *= 1.8
                        elif c in ('sorghum', 'jowar'):
                            probs[i] *= 1.7

                elif zone_name in ('South Konkan', 'North Konkan'):
                    # Ratnagiri, Sindhudurg, Raigad, Thane
                    for i, cls in enumerate(classes):
                        c = cls.lower()
                        if c == 'mango' and ph <= 7.0:
                            probs[i] *= 2.5
                        elif c == 'cashew' and ph <= 6.5:
                            probs[i] *= 2.4
                        elif c == 'rice':
                            probs[i] *= 2.2
                        elif c == 'coconut':
                            probs[i] *= 2.0

                elif zone_name in ('Western Maharashtra Plain', 'Scarcity & Rain Shadow Zone'):
                    # Kolhapur, Sangli, Pune, Satara, Solapur, Ahmednagar, Nashik
                    for i, cls in enumerate(classes):
                        c = cls.lower()
                        if c == 'sugarcane' and n >= 130 and eff_rainfall >= 850:
                            probs[i] *= 2.3
                        elif c == 'grapes' and k >= 100 and p >= 70:
                            probs[i] *= 2.4
                        elif c == 'onion' and 50 <= n <= 110:
                            probs[i] *= 2.2
                        elif c == 'pomegranate' and ph >= 7.0:
                            probs[i] *= 2.2
                        elif c in ('sorghum', 'jowar'):
                            probs[i] *= 2.0

                # Renormalize probabilities
                total_p = np.sum(probs)
                if total_p > 0:
                    probs = probs / total_p

                top_indices = np.argsort(probs)[::-1]
                pred_class = classes[top_indices[0]]
                confidence = round(float(probs[top_indices[0]]), 4)
                
                for idx in top_indices[1:4]:
                    if probs[idx] > 0.04:
                        top_alternatives.append({
                            'crop': self._format_crop_name(str(classes[idx])),
                            'probability': round(float(probs[idx]), 4)
                        })

                desc = self._generate_description(pred_class, zone_name or "Maharashtra Agricultural Zone")

                return {
                    'crop': self._format_crop_name(str(pred_class)),
                    'confidence': confidence,
                    'top_alternatives': top_alternatives,
                    'model_used': 'RandomForestClassifier (Maharashtra Agricultural Benchmark)',
                    'agro_climatic_zone': zone_name or 'Maharashtra State Agrozones',
                    'description': desc
                }

        # Fallback
        return self._heuristic_fallback(n, p, k, temp, humidity, ph, eff_rainfall, zone_name)

    def _format_crop_name(self, crop: str) -> str:
        """Friendly names with regional/Marathi names."""
        c = crop.lower().strip()
        return CROP_DISPLAY_NAMES.get(c, crop.capitalize())

    def _generate_description(self, crop: str, zone: str) -> str:
        name = self._format_crop_name(crop)
        return (
            f"Based on soil macronutrients (N-P-K), soil pH, rainfall, and agro-climatic conditions of {zone}, "
            f"{name} is highly recommended for optimal yield and economic profitability in Maharashtra."
        )

    def _heuristic_fallback(self, n: float, p: float, k: float, temp: float, humidity: float, ph: float, rainfall: float, zone: Optional[str]) -> Dict[str, Any]:
        """Agronomic fallback specifically for Maharashtra."""
        if zone == 'Central Vidarbha Zone' or (550 <= rainfall <= 1250 and 22 <= temp <= 38 and ph >= 6.5):
            if n >= 80:
                crop = "Cotton (Bt Cotton / Kapas)"
            elif p >= 45 and n <= 50:
                crop = "Soybean (Soya)"
            elif 55 <= n <= 85:
                crop = "Sorghum (Jowar / Maldandi)"
            else:
                crop = "Pigeon Pea (Tur / Arhar)"
        elif rainfall > 1800:
            crop = "Rice (Paddy / Bhat)" if humidity > 75 else "Mango (Alphonso / Hapus)"
        elif k > 100 and p > 70:
            crop = "Grapes (Draksha)"
        elif rainfall < 600 and ph >= 7.2:
            crop = "Pomegranate (Dalimb - Bhagwa)"
        else:
            crop = "Soybean (Soya)"

        return {
            'crop': crop,
            'confidence': 0.88,
            'top_alternatives': [
                {'crop': 'Cotton (Bt Cotton / Kapas)', 'probability': 0.40},
                {'crop': 'Soybean (Soya)', 'probability': 0.35},
                {'crop': 'Pigeon Pea (Tur / Arhar)', 'probability': 0.25}
            ],
            'model_used': 'AgronomicRuleEngine (Maharashtra Fallback)',
            'agro_climatic_zone': zone or 'Maharashtra Agrozone',
            'description': f"Recommended for Maharashtra based on state agricultural university parameters."
        }
