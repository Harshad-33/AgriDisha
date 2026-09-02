"""
Fertilizer Recommendation Service.
Evaluates crop-specific nutrient requirements against current soil N-P-K levels.
"""
import os
import json
import logging
from typing import Dict, Any, List

logger = logging.getLogger("ml_service.fertilizer")

KNOWLEDGE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "fertilizer_knowledge.json")


class FertilizerService:
    def __init__(self, knowledge_path: str = KNOWLEDGE_PATH):
        self.knowledge_path = knowledge_path
        self.knowledge = self._load_knowledge()

    def _load_knowledge(self) -> Dict[str, Any]:
        """Load fertilizer knowledge base JSON."""
        if os.path.exists(self.knowledge_path):
            try:
                with open(self.knowledge_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error reading fertilizer knowledge: {e}")
        return {"crop_requirements": {}, "rules": {}}

    def recommend(self, crop_name: str, n: float, p: float, k: float) -> Dict[str, Any]:
        """
        Generate comprehensive fertilizer recommendation for given crop and soil nutrients.
        """
        crop_key = crop_name.lower().strip()
        crop_reqs = self.knowledge.get("crop_requirements", {})
        rules = self.knowledge.get("rules", {})

        # Default standard crop requirement if specific not found
        req = crop_reqs.get(crop_key, {"n": 80, "p": 40, "k": 40, "name": crop_name.capitalize()})
        target_n, target_p, target_k = req["n"], req["p"], req["k"]
        display_name = req.get("name", crop_name.capitalize())

        diff_n = n - target_n
        diff_p = p - target_p
        diff_k = k - target_k

        # Threshold for deficit/excess
        threshold = 15.0

        n_status = "Optimal" if abs(diff_n) <= threshold else ("High" if diff_n > threshold else "Low")
        p_status = "Optimal" if abs(diff_p) <= threshold else ("High" if diff_p > threshold else "Low")
        k_status = "Optimal" if abs(diff_k) <= threshold else ("High" if diff_k > threshold else "Low")

        nutrient_evaluations = []
        actionable_recommendations = []
        chemical_suggestions = []
        organic_suggestions = []

        # Nitrogen evaluation
        if n_status == "Low":
            rule = rules.get("NLow", {})
            nutrient_evaluations.append(f"Nitrogen is deficient (Current: {n}, Ideal: {target_n})")
            if rule:
                chemical_suggestions.append(rule.get("chemical_fertilizer"))
                organic_suggestions.append(rule.get("organic_alternative"))
                actionable_recommendations.append(rule.get("action_advice"))
        elif n_status == "High":
            rule = rules.get("NHigh", {})
            nutrient_evaluations.append(f"Nitrogen is in excess (Current: {n}, Ideal: {target_n})")
            if rule:
                chemical_suggestions.append(rule.get("chemical_fertilizer"))
                organic_suggestions.append(rule.get("organic_alternative"))
                actionable_recommendations.append(rule.get("action_advice"))
        else:
            nutrient_evaluations.append(f"Nitrogen is well balanced (Current: {n}, Ideal: {target_n})")

        # Phosphorus evaluation
        if p_status == "Low":
            rule = rules.get("PLow", {})
            nutrient_evaluations.append(f"Phosphorus is deficient (Current: {p}, Ideal: {target_p})")
            if rule:
                chemical_suggestions.append(rule.get("chemical_fertilizer"))
                organic_suggestions.append(rule.get("organic_alternative"))
                actionable_recommendations.append(rule.get("action_advice"))
        elif p_status == "High":
            rule = rules.get("PHigh", {})
            nutrient_evaluations.append(f"Phosphorus is in excess (Current: {p}, Ideal: {target_p})")
            if rule:
                chemical_suggestions.append(rule.get("chemical_fertilizer"))
                organic_suggestions.append(rule.get("organic_alternative"))
                actionable_recommendations.append(rule.get("action_advice"))
        else:
            nutrient_evaluations.append(f"Phosphorus is well balanced (Current: {p}, Ideal: {target_p})")

        # Potassium evaluation
        if k_status == "Low":
            rule = rules.get("KLow", {})
            nutrient_evaluations.append(f"Potassium is deficient (Current: {k}, Ideal: {target_k})")
            if rule:
                chemical_suggestions.append(rule.get("chemical_fertilizer"))
                organic_suggestions.append(rule.get("organic_alternative"))
                actionable_recommendations.append(rule.get("action_advice"))
        elif k_status == "High":
            rule = rules.get("KHigh", {})
            nutrient_evaluations.append(f"Potassium is in excess (Current: {k}, Ideal: {target_k})")
            if rule:
                chemical_suggestions.append(rule.get("chemical_fertilizer"))
                organic_suggestions.append(rule.get("organic_alternative"))
                actionable_recommendations.append(rule.get("action_advice"))
        else:
            nutrient_evaluations.append(f"Potassium is well balanced (Current: {k}, Ideal: {target_k})")

        if n_status == "Optimal" and p_status == "Optimal" and k_status == "Optimal":
            rule = rules.get("Balanced", {})
            chemical_suggestions.append(rule.get("chemical_fertilizer", "NPK 19:19:19 Maintenance dose"))
            organic_suggestions.append(rule.get("organic_alternative", "Aged Vermicompost"))
            actionable_recommendations.append(rule.get("action_advice", "Maintain current soil management practices."))

        summary_status = f"N: {n_status}, P: {p_status}, K: {k_status}"

        # Clean list of unique non-empty suggestions
        chemical_suggestions = [c for c in chemical_suggestions if c]
        organic_suggestions = [o for o in organic_suggestions if o]
        actionable_recommendations = [a for a in actionable_recommendations if a]

        return {
            "crop": display_name,
            "soil_status": summary_status,
            "nutrient_levels": {
                "nitrogen": {"current": n, "ideal": target_n, "status": n_status},
                "phosphorus": {"current": p, "ideal": target_p, "status": p_status},
                "potassium": {"current": k, "ideal": target_k, "status": k_status}
            },
            "evaluations": nutrient_evaluations,
            "chemical_fertilizers": chemical_suggestions,
            "organic_alternatives": organic_suggestions,
            "recommendations": actionable_recommendations,
            "primary_recommendation": actionable_recommendations[0] if actionable_recommendations else "Soil nutrients are in optimal proportion."
        }
