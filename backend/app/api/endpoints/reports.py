import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from backend.app.database.session import get_db
from backend.app.database.models import PredictionRecord
from backend.app.core.config import settings
from backend.app.services.pdf_report_service import PDFReportService
from backend.app.services.inference_service import MORPHOLOGY_KNOWLEDGE

router = APIRouter()

@router.get("/{case_id}/pdf")
def generate_and_download_pdf(case_id: str, db: Session = Depends(get_db)):
    rec = db.query(PredictionRecord).filter(PredictionRecord.case_id == case_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Case record not found.")

    report_filename = f"{case_id}_Clinical_Report.pdf"
    output_path = os.path.join(settings.UPLOADS_DIR, "reports", report_filename)

    # Resolve image paths
    orig_path = rec.file_path
    heat_path = None
    if rec.heatmap_path:
        # e.g. /uploads/heatmaps/CASE-XXX_gradcam.jpg
        h_rel = rec.heatmap_path.replace("/uploads/", "")
        heat_path = os.path.join(settings.UPLOADS_DIR, h_rel)

    data = {
        "case_id": rec.case_id,
        "file_name": rec.file_name,
        "outcome": rec.outcome,
        "predicted_subtype": rec.predicted_subtype,
        "predicted_subtype_full": settings.CLASS_FULL_NAMES.get(rec.predicted_subtype),
        "confidence": rec.confidence,
        "confidence_percentage": f"{rec.confidence*100:.2f}%" if rec.confidence else "N/A",
        "threshold_used": rec.threshold_used,
        "rejection_reason": rec.rejection_reason,
        "probabilities": {
            "CLL": rec.prob_cll or 0.0,
            "FL": rec.prob_fl or 0.0,
            "MCL": rec.prob_mcl or 0.0
        },
        "morphology_summary": MORPHOLOGY_KNOWLEDGE.get(rec.predicted_subtype),
        "original_path": orig_path,
        "heatmap_path_full": heat_path,
        "created_at": str(rec.created_at)
    }

    try:
        PDFReportService.generate_clinical_report(data, output_path)
        return FileResponse(
            output_path,
            media_type="application/pdf",
            filename=f"Lymphoma_Report_{case_id}.pdf"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF report: {e}")
