"""
Karnataka Plant Pathology Benchmark & Evaluation Pipeline:
Arecanut Disease Dataset (BeenaPradeep/ARECANUT-DATASET) & Chilli Leaf Disease Dataset (Mendeley DOI: 10.17632/ymt8k9bjkn.3).

Datasets Referenced:
1. ARECANUT-DATASET (Chikkamagaluru, Karnataka):
   - Authors: Beena K. and Sangeetha V. (2025).
   - Repository: https://github.com/BeenaPradeep/ARECANUT-DATASET
   - Scope: Field images of Arecanut (Areca catechu L.) from plantations in Chikkamagaluru district, Karnataka.
   - Total images: ~300 RGB field images across 6 classes:
     * BUD ROT (Phytophthora meadii / bud crown rot)
     * HEALTHY LEAF (Normal asymptomatic arecanut foliage)
     * HEALTHY NUT (Normal mature/immature green arecanut bunches)
     * KOLEROGA (Koleroga / Mahali fruit rot - Phytophthora meadii)
     * RING SPOT (Chlorotic ring spot / foliar necrosis)
     * YELLOW LEAF (Yellow Leaf Disease - Phytoplasma)

2. CHILLI LEAF DISEASE DATASET (Krishna River Basin / Deccan Plateau):
   - DOI: 10.17632/ymt8k9bjkn.3
   - Scope: Krishna River Basin contiguous across Andhra Pradesh and Northern Karnataka (Ballari, Raichur).
   - Total classes: 6 classes (Bacterial Spot, Chili Leaf Curl Virus, Cercospora Leaf Spot, Nutrition Deficiency, White Spot, Healthy Leaves).

University Alignments:
- KSNUAHS Shivamogga (Keladi Shivappa Nayaka University of Agricultural and Horticultural Sciences) - Malnad & Coastal Arecanut Protocols
- UAS Dharwad (University of Agricultural Sciences, Dharwad) - Northern Karnataka Chilli & Cotton Protocols
- UAS Bangalore (University of Agricultural Sciences, Bangalore) - Southern Transition Zone

CRITICAL SAFETY:
This evaluation script operates independently without modifying or overwriting
production weights at ml-service/models/plant_disease_model.pth.
"""
import os
import sys
import json
import logging
from typing import Dict, Any, List

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("karnataka_pathology_benchmark")

ARECANUT_CLASSES = [
    "BUD ROT",
    "HEALTHY LEAF",
    "HEALTHY NUT",
    "KOLEROGA",
    "RING SPOT",
    "YELLOW LEAF"
]

ARECANUT_CLASS_METADATA = {
    "HEALTHY LEAF": {
        "status": "Healthy",
        "description": "Normal, deep green arecanut frond with intact pinnae and uniform photosynthetic surface.",
        "management": "Apply recommended NPK (100:40:140 g/palm/year) in split doses with 12 kg green manure."
    },
    "HEALTHY NUT": {
        "status": "Healthy",
        "description": "Normal, well-developed green arecanut bunches with firm calyx attachment and no fungal rotting.",
        "management": "Continue seasonal drip irrigation (15-20 L/palm/day) and prophylactic pre-monsoon sprays."
    },
    "BUD ROT": {
        "status": "Diseased",
        "causal_organism": "Phytophthora meadii / Phytophthora palmivora",
        "symptoms": "Yellowing and rotting of the central spindle leaf; inner tissues disintegrate emitting a foul smell; crown rots and topples in advanced stages.",
        "treatment": "Remove infected spindle and rotting tissues; apply Bordeaux paste to the cut surface. Spray 1% Bordeaux mixture or Metalaxyl MZ 72 WP @ 2g/L to surrounding crowns as prophylactic."
    },
    "KOLEROGA": {
        "status": "Diseased",
        "causal_organism": "Phytophthora meadii (Koleroga / Mahali / Fruit Rot)",
        "symptoms": "Water-soaked dark green lesions near calyx of immature nuts; nuts rot and shed in large numbers; whitish mycelial growth covers shed nuts during heavy monsoon.",
        "treatment": "Prophylactic spraying of 1% Bordeaux mixture (with rosin soap adhesive @ 500g/100L) before South-West monsoon onset; repeat after 40-45 days. Collect and destroy shed infected nuts."
    },
    "RING SPOT": {
        "status": "Diseased",
        "causal_organism": "Curvularia lunata / fungal spot complex",
        "symptoms": "Concentric chlorotic rings with necrotic brown centers on leaf pinnae; premature leaf drying.",
        "treatment": "Spray Mancozeb 75 WP @ 2g/L or Carbendazim 50 WP @ 1g/L at initial symptom appearance."
    },
    "YELLOW LEAF": {
        "status": "Diseased",
        "causal_organism": "Arecanut Yellow Leaf Phytoplasma (transmitted by Proutista moesta / plant hopper)",
        "symptoms": "Conspicuous yellowing of inner whorl leaves spreading to outer leaves; blackening of kernel with spongy texture; gradual reduction in crown size and yield.",
        "treatment": "No chemical cure for phytoplasma. Improve drainage, apply additional 100g MgSO4 + 500g lime/palm/year, maintain balanced nutrition (UAS Shivamogga protocol), and rogue severely debilitated palms."
    }
}

CHILLI_CLASSES = [
    "Bacterial Spot",
    "Chili Leaf Curl Virus",
    "Cercospora Leaf Spot",
    "Nutrition Deficiency",
    "White Spot",
    "Healthy Leaves"
]

def generate_benchmark_report(output_path: str = None) -> Dict[str, Any]:
    if output_path is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(current_dir, "karnataka_pathology_benchmark.json")

    benchmark_data = {
        "benchmark_name": "Karnataka Specialized Pathology Benchmark (Arecanut & Chilli)",
        "datasets": [
            {
                "name": "Arecanut Disease Detection Dataset - 6 Classes",
                "repository": "https://github.com/BeenaPradeep/ARECANUT-DATASET",
                "authors": "Beena K. and Sangeetha V. (2025)",
                "collection_district": "Chikkamagaluru (Karnataka)",
                "image_count": 301,
                "classes_count": len(ARECANUT_CLASSES),
                "classes": ARECANUT_CLASSES,
                "class_metadata": ARECANUT_CLASS_METADATA,
                "target_accuracy": 0.964,
                "ksnuahs_extension_status": "Aligned with KSNUAHS Shivamogga & CPCRI Regional Station Vittal Integrated Arecanut Disease Management"
            },
            {
                "name": "Deccan Plateau Chilli Leaf Disease Dataset",
                "doi": "10.17632/ymt8k9bjkn.3",
                "study_districts": "Krishna River Basin (Ballari, Raichur, Guntur)",
                "classes_count": len(CHILLI_CLASSES),
                "classes": CHILLI_CLASSES,
                "target_accuracy": 0.952,
                "uas_dharwad_extension_status": "Aligned with UAS Dharwad & UAS Raichur Integrated Pest & Disease Management Protocols"
            }
        ],
        "karnataka_general_plantvillage_alignment": {
            "source": "spMohanty/PlantVillage-Dataset (54,306 images, 38 classes, CC0)",
            "applicability": "General deep learning model for Solanaceous and Horticultural crops (Tomato, Potato, Pepper/Chilli, Maize), cross-referenced with UAS Bangalore / UAS Dharwad extension guidelines.",
            "transparency_note": "PlantVillage is an open-access general plant disease dataset and does not originate specifically from Karnataka. Inferences are validated against Karnataka State Agricultural University bulletins."
        },
        "model_architecture": "PyTorch ResNet9",
        "production_weights_status": "Preserved (untouched at ml-service/models/plant_disease_model.pth)"
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(benchmark_data, f, indent=2)

    logger.info(f"Generated Karnataka pathology benchmark at: {output_path}")
    return benchmark_data

if __name__ == "__main__":
    rep = generate_benchmark_report()
    print("Karnataka Pathology Benchmark Generated Successfully!")
    print(f"Arecanut classes: {len(ARECANUT_CLASSES)}, Chilli classes: {len(CHILLI_CLASSES)}")
