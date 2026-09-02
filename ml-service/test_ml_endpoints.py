"""
Test script for ML services.
"""
import io
from PIL import Image
from services.crop_service import CropService
from services.fertilizer_service import FertilizerService
from services.disease_service import DiseaseService

def test_services():
    print("=== Testing Crop Service ===")
    crop_svc = CropService()
    crop_res = crop_svc.predict(n=90, p=42, k=43, temp=28.5, humidity=78.0, ph=6.5, rainfall=200.0)
    print(f"Crop Result: {crop_res}")
    assert crop_res['crop'] is not None

    print("\n=== Testing Fertilizer Service ===")
    fert_svc = FertilizerService()
    fert_res = fert_svc.recommend(crop_name="Rice", n=25, p=40, k=40)
    print(f"Fertilizer Result: {fert_res['crop']} - Status: {fert_res['soil_status']}")
    print(f"Chemical suggestions: {fert_res['chemical_fertilizers']}")
    assert "Low" in fert_res['soil_status']

    print("\n=== Testing Disease Service ===")
    disease_svc = DiseaseService()
    # Create sample synthetic leaf image
    img = Image.new("RGB", (256, 256), color=(34, 139, 34))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    leaf_bytes = buf.getvalue()

    disease_res = disease_svc.predict(leaf_bytes)
    print(f"Disease Result: Crop={disease_res['crop']}, Disease={disease_res['disease']}, Status={disease_res['status']}, Confidence={disease_res['confidence']}")
    assert disease_res['crop'] is not None

    print("\n>>> ALL ML SERVICE TESTS PASSED SUCCESSFULLY! <<<")

if __name__ == "__main__":
    test_services()
