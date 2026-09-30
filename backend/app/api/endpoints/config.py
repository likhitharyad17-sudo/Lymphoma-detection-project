from fastapi import APIRouter
from backend.app.core.config import settings
from backend.app.schemas.prediction import ThresholdConfigUpdate

router = APIRouter()

@router.get("/threshold")
def get_threshold():
    return {
        "current_threshold": settings.LYMPHOMA_CONFIDENCE_THRESHOLD,
        "default_threshold": 0.80,
        "min_threshold": 0.50,
        "max_threshold": 0.99,
        "description": "Confidence threshold to distinguish Lymphoma Detected vs Rejected (No Lymphoma Detected)."
    }

@router.post("/threshold")
def update_threshold(payload: ThresholdConfigUpdate):
    if payload.threshold < 0.50 or payload.threshold > 0.99:
        return {"error": "Threshold must be between 0.50 and 0.99"}
    settings.LYMPHOMA_CONFIDENCE_THRESHOLD = float(payload.threshold)
    return {
        "message": f"Updated LYMPHOMA_CONFIDENCE_THRESHOLD to {settings.LYMPHOMA_CONFIDENCE_THRESHOLD:.2f}",
        "current_threshold": settings.LYMPHOMA_CONFIDENCE_THRESHOLD
    }
