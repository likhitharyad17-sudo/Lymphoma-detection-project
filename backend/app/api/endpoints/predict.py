import os
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database.session import get_db
from backend.app.database.models import FeedbackRecord, PredictionRecord, User
from backend.app.schemas.prediction import (
    PredictionResponse, BatchPredictionResponse, ValidationResponse,
    FeedbackCreate, FeedbackResponse
)
from backend.app.api.endpoints.auth import get_optional_current_user
from backend.app.services.inference_service import inference_service
from backend.app.services.image_validator import ImageValidator

router = APIRouter()

@router.post("/validate", response_model=ValidationResponse)
async def validate_uploaded_image(file: UploadFile = File(...)):
    contents = await file.read()
    is_valid, msg = ImageValidator.validate_image(contents)
    return ValidationResponse(is_valid=is_valid, message=msg)

@router.post("/", response_model=PredictionResponse)
async def predict_single_image(
    file: UploadFile = File(...),
    threshold: Optional[float] = Form(None),
    is_private: Optional[bool] = Form(False),
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    try:
        contents = await file.read()
        response = inference_service.predict_image(
            file_bytes=contents,
            filename=file.filename,
            db=db,
            current_user=current_user,
            custom_threshold=threshold,
            is_private=is_private or False
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference processing failed: {str(e)}")

@router.post("/batch", response_model=BatchPredictionResponse)
async def predict_batch_images(
    files: List[UploadFile] = File(...),
    threshold: Optional[float] = Form(None),
    is_private: Optional[bool] = Form(False),
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    results = []
    detected = 0
    rejected = 0
    invalid = 0

    for file in files:
        contents = await file.read()
        res = inference_service.predict_image(
            file_bytes=contents,
            filename=file.filename,
            db=db,
            current_user=current_user,
            custom_threshold=threshold,
            is_private=is_private or False
        )
        results.append(res)
        if res.outcome == "LYMPHOMA_DETECTED":
            detected += 1
        elif res.outcome == "NO_LYMPHOMA_DETECTED":
            rejected += 1
        else:
            invalid += 1

    return BatchPredictionResponse(
        total_processed=len(results),
        lymphoma_detected_count=detected,
        rejected_count=rejected,
        invalid_count=invalid,
        results=results
    )

@router.post("/feedback", response_model=FeedbackResponse)
def submit_pathologist_feedback(data: FeedbackCreate, db: Session = Depends(get_db)):
    fb = FeedbackRecord(
        prediction_id=data.prediction_id,
        review_status=data.review_status,
        notes=data.notes,
        reviewed_by=data.reviewed_by
    )
    db.add(fb)
    db.commit()
    db.refresh(fb)
    return fb
