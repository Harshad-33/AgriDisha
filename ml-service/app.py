"""
FastAPI Microservice for AgriDisha Machine Learning Models.
Exposes REST endpoints for crop prediction, fertilizer recommendation, and plant disease detection,
benchmarked against Maharashtra Agricultural Universities standards.
"""
import sys
import os

# Ensure local module path resolution works in all IDEs and execution environments
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

import logging
from contextlib import asynccontextmanager
from typing import Optional, List

from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from services.crop_service import CropService
from services.fertilizer_service import FertilizerService
from services.disease_service import DiseaseService

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("ml_service")

# Global Service Singletons
crop_service: Optional[CropService] = None
fertilizer_service: Optional[FertilizerService] = None
disease_service: Optional[DiseaseService] = None


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Pre-load models on application startup."""
    global crop_service, fertilizer_service, disease_service
    logger.info("Initializing Maharashtra ML models and services...")
    crop_service = CropService()
    fertilizer_service = FertilizerService()
    disease_service = DiseaseService()
    logger.info("ML Services successfully initialized.")
    yield
    logger.info("Shutting down ML services...")


app = FastAPI(
    title="AgriDisha Maharashtra ML Service",
    description="Dedicated FastAPI Machine Learning Inference Service for AgriDisha Smart Agriculture (Maharashtra & Pan-India)",
    version="2.1.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------------------------------------
# Request & Response Schemas
# -------------------------------------------------------------
class CropPredictRequest(BaseModel):
    nitrogen: float = Field(..., ge=0, le=300, description="Nitrogen ratio in soil (mg/kg)")
    phosphorous: float = Field(..., ge=0, le=300, description="Phosphorous ratio in soil (mg/kg)")
    potassium: float = Field(..., ge=0, le=300, description="Potassium ratio in soil (mg/kg)")
    temperature: float = Field(..., ge=-10, le=60, description="Temperature in Celsius")
    humidity: float = Field(..., ge=0, le=100, description="Relative humidity percentage")
    ph: float = Field(..., ge=0, le=14, description="Soil pH value")
    rainfall: float = Field(..., ge=0, le=5000, description="Rainfall in mm (annual or seasonal)")
    city: Optional[str] = Field(default=None, description="City or District name")


class CropAlternative(BaseModel):
    crop: str
    probability: float


class CropPredictResponse(BaseModel):
    crop: str
    confidence: float
    top_alternatives: List[CropAlternative] = Field(default_factory=list)
    model_used: str
    agro_climatic_zone: Optional[str] = None
    description: Optional[str] = None


class FertilizerRecommendRequest(BaseModel):
    crop_name: str = Field(..., min_length=2, description="Target crop name")
    nitrogen: float = Field(..., ge=0, description="Current soil Nitrogen value")
    phosphorous: float = Field(..., ge=0, description="Current soil Phosphorous value")
    potassium: float = Field(..., ge=0, description="Current soil Potassium value")


class NutrientDetail(BaseModel):
    current: float
    ideal: float
    status: str


class NutrientLevels(BaseModel):
    nitrogen: NutrientDetail
    phosphorus: NutrientDetail
    potassium: NutrientDetail


class FertilizerRecommendResponse(BaseModel):
    crop: str
    soil_status: str
    nutrient_levels: NutrientLevels
    evaluations: List[str] = Field(default_factory=list)
    chemical_fertilizers: List[str] = Field(default_factory=list)
    organic_alternatives: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    primary_recommendation: str


class DiseasePredictResponse(BaseModel):
    raw_class: str
    crop: str
    disease: str
    status: str
    confidence: float
    severity: str
    cause: str
    symptoms: str
    prevention: str
    treatment: str
    supplement: str


# -------------------------------------------------------------
# Endpoints
# -------------------------------------------------------------
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "UP",
        "service": "agridisha-ml-service",
        "crop_model_ready": crop_service is not None and crop_service.model_payload is not None,
        "disease_model_ready": disease_service is not None,
        "dataset": "Maharashtra Agricultural Benchmark (MPKV / PDKV / VNMKV / BSKKV)"
    }


@app.post("/api/ml/crop-predict", response_model=CropPredictResponse, tags=["Crop Recommendation"])
async def predict_crop(request: CropPredictRequest):
    """
    Predict best-suited crop based on N-P-K, temperature, humidity, pH, and rainfall.
    """
    svc = crop_service
    if svc is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Crop prediction service not initialized"
        )

    try:
        result = svc.predict(
            n=request.nitrogen,
            p=request.phosphorous,
            k=request.potassium,
            temp=request.temperature,
            humidity=request.humidity,
            ph=request.ph,
            rainfall=request.rainfall,
            city=request.city
        )
        return CropPredictResponse(**result)
    except Exception as e:
        logger.error("Prediction failed: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Crop prediction failed: {str(e)}"
        ) from e


@app.post("/api/ml/fertilizer-recommend", response_model=FertilizerRecommendResponse, tags=["Fertilizer Recommendation"])
async def recommend_fertilizer(request: FertilizerRecommendRequest):
    """
    Recommend fertilizer and nutrient management based on crop requirements and soil status.
    """
    svc = fertilizer_service
    if svc is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Fertilizer recommendation service not initialized"
        )

    try:
        result = svc.recommend(
            crop_name=request.crop_name,
            n=request.nitrogen,
            p=request.phosphorous,
            k=request.potassium
        )
        return FertilizerRecommendResponse(**result)
    except Exception as e:
        logger.error("Fertilizer recommendation failed: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fertilizer recommendation failed: {str(e)}"
        ) from e


@app.post("/api/ml/disease-predict", response_model=DiseasePredictResponse, tags=["Plant Disease Detection"])
async def predict_disease(image: UploadFile = File(...)):
    """
    Classify plant disease from uploaded leaf image and return treatment advice.
    """
    svc = disease_service
    if svc is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Disease prediction service not initialized"
        )

    valid_content_types = ["image/jpeg", "image/png", "image/webp", "image/jpg", "application/octet-stream"]
    if image.content_type not in valid_content_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image format. Supported formats: JPEG, PNG, WebP."
        )

    try:
        image_bytes = await image.read()
        if len(image_bytes) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty."
            )
        
        result = svc.predict(image_bytes)
        return DiseasePredictResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Plant disease inference failed: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Disease prediction failed: {str(e)}"
        ) from e


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
