from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from backend.app.database.session import get_db
from backend.app.database.models import PredictionRecord, User
from backend.app.schemas.prediction import PredictionResponse, VisibilityUpdateRequest, PrivacyUpdateRequest
from backend.app.api.endpoints.auth import get_optional_current_user, get_current_user

router = APIRouter()

@router.get("/")
def get_prediction_history(
    outcome: Optional[str] = None,
    filter_mode: Optional[str] = Query("all", description="all | my_tests | public"),
    limit: int = 100,
    offset: int = 0,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(PredictionRecord).filter(PredictionRecord.is_deleted == False)

    is_admin = current_user is not None and current_user.role == "ADMIN"
    user_id = current_user.id if current_user else None

    if is_admin:
        if filter_mode == "my_tests" and user_id:
            query = query.filter(PredictionRecord.user_id == user_id)
        elif filter_mode == "hidden":
            query = query.filter(PredictionRecord.is_hidden_by_admin == True)
    elif current_user:
        if filter_mode == "my_tests":
            query = query.filter(PredictionRecord.user_id == user_id)
        elif filter_mode == "public":
            query = query.filter(
                and_(
                    PredictionRecord.is_hidden_by_admin == False,
                    PredictionRecord.is_private == False
                )
            )
        else:
            query = query.filter(
                or_(
                    PredictionRecord.user_id == user_id,
                    and_(
                        PredictionRecord.is_hidden_by_admin == False,
                        PredictionRecord.is_private == False
                    )
                )
            )
    else:
        query = query.filter(
            and_(
                PredictionRecord.is_hidden_by_admin == False,
                PredictionRecord.is_private == False
            )
        )

    if outcome:
        query = query.filter(PredictionRecord.outcome == outcome)

    total = query.count()
    records = query.order_by(PredictionRecord.created_at.desc()).offset(offset).limit(limit).all()

    results = []
    for r in records:
        probs = None
        if r.prob_cll is not None:
            probs = {"CLL": r.prob_cll, "FL": r.prob_fl, "MCL": r.prob_mcl}
        
        heatmap_url = f"/uploads/heatmaps/{r.case_id}_gradcam.jpg" if r.heatmap_path else None
        original_url = f"/uploads/images/{r.case_id}_original.jpg"

        results.append({
            "id": r.id,
            "case_id": r.case_id,
            "user_id": r.user_id,
            "user_email": r.user_email,
            "user_name": r.user_name,
            "file_name": r.file_name,
            "outcome": r.outcome,
            "outcome_display": "Lymphoma Detected" if r.outcome == "LYMPHOMA_DETECTED" else "No Lymphoma Detected" if r.outcome == "NO_LYMPHOMA_DETECTED" else "Unable to Analyze",
            "predicted_subtype": r.predicted_subtype,
            "predicted_class": r.predicted_subtype,
            "confidence": r.confidence,
            "confidence_percentage": f"{r.confidence * 100:.2f}%" if r.confidence else None,
            "probabilities": probs,
            "top_probabilities": probs,
            "threshold_used": r.threshold_used,
            "rejection_reason": r.rejection_reason,
            "heatmap_url": heatmap_url,
            "original_url": original_url,
            "report_url": f"/api/reports/{r.case_id}/pdf",
            "morphology_summary": r.notes,
            "is_hidden_by_admin": r.is_hidden_by_admin,
            "is_private": r.is_private,
            "created_at": r.created_at
        })

    return {
        "total": total,
        "records": results,
        "is_admin": is_admin,
        "current_user_id": user_id
    }

@router.patch("/{case_id}/admin-visibility")
def update_admin_visibility(
    case_id: str,
    data: VisibilityUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can modify result display/hidden visibility."
        )

    record = db.query(PredictionRecord).filter(PredictionRecord.case_id == case_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Case record not found")

    record.is_hidden_by_admin = data.is_hidden_by_admin
    db.commit()
    db.refresh(record)

    action_text = "hidden from users" if data.is_hidden_by_admin else "made visible to users"
    return {"message": f"Case {case_id} has been {action_text}.", "is_hidden_by_admin": record.is_hidden_by_admin}

@router.patch("/{case_id}/user-privacy")
def update_user_privacy(
    case_id: str,
    data: PrivacyUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    record = db.query(PredictionRecord).filter(PredictionRecord.case_id == case_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Case record not found")

    if current_user.role != "ADMIN" and record.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only change privacy settings for your own tests."
        )

    record.is_private = data.is_private
    db.commit()
    db.refresh(record)

    action_text = "marked as Private (hidden from other users)" if data.is_private else "marked as Public"
    return {"message": f"Case {case_id} is now {action_text}.", "is_private": record.is_private}

@router.delete("/{case_id}")
def delete_prediction_case(
    case_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    record = db.query(PredictionRecord).filter(PredictionRecord.case_id == case_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Case record not found")

    if current_user.role != "ADMIN" and record.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied: You can only delete your own test records. Only an administrator can delete other users' records."
        )

    db.delete(record)
    db.commit()
    return {"message": f"Case {case_id} deleted successfully"}

@router.post("/clear-all")
def clear_all_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators are authorized to clear all historical records."
        )

    db.query(PredictionRecord).delete()
    db.commit()
    return {"message": "All case history records have been permanently cleared by administrator."}
