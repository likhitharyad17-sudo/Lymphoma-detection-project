import os

project_root = r"D:\Lymphoma Detection Project"
files = {}

# 1. Prediction Router
files["backend/app/api/endpoints/predict.py"] = """import os
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database.session import get_db
from backend.app.schemas.prediction import PredictionResponse, BatchPredictionResponse
from backend.app.services.inference_service import inference_service

router = APIRouter()

@router.post("/", response_model=PredictionResponse)
async def predict_single_image(
    file: UploadFile = File(...),
    threshold: Optional[float] = Form(None),
    db: Session = Depends(get_db)
):
    try:
        contents = await file.read()
        response = inference_service.predict_image(
            file_bytes=contents,
            filename=file.filename,
            db=db,
            custom_threshold=threshold
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference processing failed: {str(e)}")

@router.post("/batch", response_model=BatchPredictionResponse)
async def predict_batch_images(
    files: List[UploadFile] = File(...),
    threshold: Optional[float] = Form(None),
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
            custom_threshold=threshold
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
"""

# 2. Metrics Router
files["backend/app/api/endpoints/metrics.py"] = """import os
import json
from fastapi import APIRouter, HTTPException
from backend.app.core.config import settings

router = APIRouter()

@router.get("/benchmarks")
def get_benchmarks():
    path = os.path.join(settings.RESULTS_DIR, "benchmark_metrics.json")
    if not os.path.exists(path):
        return {"status": "pending", "message": "Evaluation pending — model has not yet been trained."}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

@router.get("/ablation")
def get_ablation():
    path = os.path.join(settings.RESULTS_DIR, "ablation_metrics.json")
    if not os.path.exists(path):
        return {"status": "pending", "message": "Ablation study evaluation pending."}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

@router.get("/thresholds")
def get_threshold_analysis():
    path = os.path.join(settings.RESULTS_DIR, "threshold_analysis.json")
    if not os.path.exists(path):
        return {
            "recommended_threshold": settings.LYMPHOMA_CONFIDENCE_THRESHOLD,
            "metric_sweeps": [],
            "rationale": "Validation sweep pending."
        }
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

@router.get("/classes")
def get_class_metadata():
    path = os.path.join(settings.BASE_DIR, "dataset", "splits", "classes.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "classes": settings.CLASSES,
        "class_full_names": settings.CLASS_FULL_NAMES,
        "total_samples": 374
    }

@router.get("/histories")
def get_training_histories():
    path = os.path.join(settings.RESULTS_DIR, "training_histories.json")
    if not os.path.exists(path):
        return {"status": "pending", "message": "Training in progress."}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
"""

# 3. History Router
files["backend/app/api/endpoints/history.py"] = """from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.app.database.session import get_db
from backend.app.database.models import PredictionRecord

router = APIRouter()

@router.get("/")
def get_prediction_history(
    outcome: Optional[str] = None,
    subtype: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(PredictionRecord)
    if outcome:
        query = query.filter(PredictionRecord.outcome == outcome)
    if subtype:
        query = query.filter(PredictionRecord.predicted_subtype == subtype)
    
    total = query.count()
    records = query.order_by(desc(PredictionRecord.created_at)).offset(offset).limit(limit).all()
    
    return {
        "total": total,
        "offset": offset,
        "limit": limit,
        "records": records
    }

@router.get("/{case_id}")
def get_single_record(case_id: str, db: Session = Depends(get_db)):
    rec = db.query(PredictionRecord).filter(PredictionRecord.case_id == case_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Case record not found.")
    return rec

@router.delete("/{case_id}")
def delete_record(case_id: str, db: Session = Depends(get_db)):
    rec = db.query(PredictionRecord).filter(PredictionRecord.case_id == case_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Case record not found.")
    db.delete(rec)
    db.commit()
    return {"message": f"Record {case_id} deleted successfully."}

@router.post("/clear-all")
def clear_all_records(db: Session = Depends(get_db)):
    db.query(PredictionRecord).delete()
    db.commit()
    return {"message": "All prediction history records cleared."}
"""

# 4. Reports Router
files["backend/app/api/endpoints/reports.py"] = """import os
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
"""

# 5. Config Router
files["backend/app/api/endpoints/config.py"] = """from fastapi import APIRouter
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
"""

# 6. Auth Router
files["backend/app/api/endpoints/auth.py"] = """import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt
from passlib.context import CryptContext

from backend.app.database.session import get_db
from backend.app.database.models import User
from backend.app.schemas.auth import UserCreate, UserLogin, Token
from backend.app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

@router.post("/register", response_model=Token)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter((User.username == user_in.username) | (User.email == user_in.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username or email already registered.")
    
    hashed = pwd_context.hash(user_in.password)
    new_user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed,
        full_name=user_in.full_name,
        role=user_in.role or "researcher"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": new_user.username, "role": new_user.role})
    return Token(
        access_token=token,
        token_type="bearer",
        user_info={
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "full_name": new_user.full_name,
            "role": new_user.role
        }
    )

@router.post("/login", response_model=Token)
def login(login_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == login_in.username).first()
    if not user or not pwd_context.verify(login_in.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password.")

    token = create_access_token({"sub": user.username, "role": user.role})
    return Token(
        access_token=token,
        token_type="bearer",
        user_info={
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role
        }
    )
"""

# 7. System Health Router
files["backend/app/api/endpoints/system.py"] = """import torch
import psutil
from fastapi import APIRouter
from backend.app.core.config import settings

router = APIRouter()

@router.get("/health")
def system_health():
    cuda_avail = torch.cuda.is_available()
    gpu_name = torch.cuda.get_device_name(0) if cuda_avail else "N/A"
    gpu_mem = torch.cuda.get_device_properties(0).total_memory / (1024**3) if cuda_avail else 0.0

    return {
        "status": "online",
        "project": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "classes": settings.CLASSES,
        "hardware": {
            "cuda_available": cuda_avail,
            "gpu_name": gpu_name,
            "gpu_memory_gb": round(gpu_mem, 2),
            "cpu_cores": psutil.cpu_count(),
            "ram_gb": round(psutil.virtual_memory().total / (1024**3), 2)
        },
        "threshold": settings.LYMPHOMA_CONFIDENCE_THRESHOLD
    }
"""

# 8. Main API App
files["backend/app/main.py"] = """import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.app.core.config import settings
from backend.app.database.session import engine, Base
from backend.app.api.endpoints import predict, metrics, history, reports, config, auth, system

# Initialize SQLite database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="End-to-end digital pathology screening and 3-class classification for Malignant Lymphoma (CLL, FL, MCL)."
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure upload folders exist
os.makedirs(os.path.join(settings.UPLOADS_DIR, "images"), exist_ok=True)
os.makedirs(os.path.join(settings.UPLOADS_DIR, "heatmaps"), exist_ok=True)
os.makedirs(os.path.join(settings.UPLOADS_DIR, "reports"), exist_ok=True)

# Mount static uploads
app.mount("/uploads", StaticFiles(directory=settings.UPLOADS_DIR), name="uploads")

# Include API Routers
app.include_router(predict.router, prefix="/api/predict", tags=["Screening & Inference"])
app.include_router(metrics.router, prefix="/api/metrics", tags=["Benchmarks & Evaluation"])
app.include_router(history.router, prefix="/api/history", tags=["Case Audit History"])
app.include_router(reports.router, prefix="/api/reports", tags=["Clinical PDF Reports"])
app.include_router(config.router, prefix="/api/config", tags=["System Configuration"])
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(system.router, prefix="/api/system", tags=["System Health"])

@app.get("/")
def root():
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "status": "healthy",
        "docs_url": "/docs",
        "classes": settings.CLASSES
    }
"""

# 9. Unit Tests
files["backend/tests/test_api.py"] = """import pytest
import io
from PIL import Image
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.core.config import settings

client = TestClient(app)

def create_synthetic_image(color=(128, 64, 180), size=(224, 224)):
    img = Image.new("RGB", size, color=color)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    return buf

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "CLL" in data["classes"]
    assert "FL" in data["classes"]
    assert "MCL" in data["classes"]

def test_system_health():
    response = client.get("/api/system/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "hardware" in data

def test_config_threshold():
    response = client.get("/api/config/threshold")
    assert response.status_code == 200
    data = response.json()
    assert "current_threshold" in data

def test_image_validation_rejection():
    # Submit empty/corrupted file
    response = client.post(
        "/api/predict/",
        files={"file": ("corrupt.txt", b"not an image", "text/plain")}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["outcome"] == "UNABLE_TO_ANALYZE"
    assert "validation failed" in data["rejection_reason"].lower()
"""

for rel_path, content in files.items():
    full_path = os.path.join(project_root, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {rel_path}")

print("All FastAPI API routes, main.py, and test_api.py created successfully.")
