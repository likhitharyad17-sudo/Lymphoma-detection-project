import os

project_root = r"D:\Lymphoma Detection Project"
files = {}

# 1. Config
files["backend/app/core/__init__.py"] = """"""
files["backend/app/core/config.py"] = """import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Attention Augmented Residual Deep Learning Framework for Lymphoma Detection"
    PROJECT_VERSION: str = "2.0.0"
    API_V1_STR: str = "/api"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "lymphoma-detection-secret-key-production-2026-academic")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days
    ALGORITHM: str = "HS256"

    # Lymphoma Rejection / Confidence Threshold
    LYMPHOMA_CONFIDENCE_THRESHOLD: float = float(os.getenv("LYMPHOMA_CONFIDENCE_THRESHOLD", "0.80"))

    # File Paths
    BASE_DIR: str = r"D:\Lymphoma Detection Project"
    MODEL_PATH: str = os.path.join(BASE_DIR, "models", "best_model.pth")
    UPLOADS_DIR: str = os.path.join(BASE_DIR, "backend", "uploads")
    RESULTS_DIR: str = os.path.join(BASE_DIR, "results")
    
    # SQLite Database
    DATABASE_URL: str = f"sqlite:///{os.path.join(BASE_DIR, 'lymphoma_predictions.db')}"

    # Target Classes
    CLASSES: list = ["CLL", "FL", "MCL"]
    CLASS_FULL_NAMES: dict = {
        "CLL": "Chronic Lymphocytic Leukemia / Small Lymphocytic Lymphoma",
        "FL": "Follicular Lymphoma",
        "MCL": "Mantle Cell Lymphoma"
    }

    class Config:
        case_sensitive = True

settings = Settings()
"""

# 2. Database Models & Session
files["backend/app/database/__init__.py"] = """"""
files["backend/app/database/session.py"] = """from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""

files["backend/app/database/models.py"] = """import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
from .session import Base

class PredictionRecord(Base):
    __tablename__ = "prediction_records"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(String(64), unique=True, index=True)
    file_name = Column(String(255))
    file_path = Column(String(512))
    
    # Outcome: 'LYMPHOMA_DETECTED', 'NO_LYMPHOMA_DETECTED', 'UNABLE_TO_ANALYZE'
    outcome = Column(String(64), index=True)
    
    # Classification (if detected)
    predicted_subtype = Column(String(32), nullable=True)
    confidence = Column(Float, nullable=True)
    
    # Probabilities
    prob_cll = Column(Float, nullable=True)
    prob_fl = Column(Float, nullable=True)
    prob_mcl = Column(Float, nullable=True)
    
    # Threshold & Rejection Metadata
    threshold_used = Column(Float, default=0.80)
    rejection_reason = Column(Text, nullable=True)
    
    # Artifact Paths
    heatmap_path = Column(String(512), nullable=True)
    report_path = Column(String(512), nullable=True)
    
    patient_id = Column(String(64), default="ANONYMOUS")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, index=True)
    email = Column(String(128), unique=True, index=True)
    hashed_password = Column(String(255))
    full_name = Column(String(128), default="Pathology Investigator")
    role = Column(String(32), default="researcher") # researcher, pathologist, admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
"""

# 3. Schemas
files["backend/app/schemas/__init__.py"] = """"""
files["backend/app/schemas/prediction.py"] = """from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

class ProbabilityBreakdown(BaseModel):
    CLL: float
    FL: float
    MCL: float

class PredictionResponse(BaseModel):
    case_id: str
    file_name: str
    outcome: str # 'LYMPHOMA_DETECTED' | 'NO_LYMPHOMA_DETECTED' | 'UNABLE_TO_ANALYZE'
    outcome_display: str
    predicted_subtype: Optional[str] = None
    predicted_subtype_full: Optional[str] = None
    confidence: Optional[float] = None
    confidence_percentage: Optional[str] = None
    probabilities: Optional[ProbabilityBreakdown] = None
    threshold_used: float
    rejection_reason: Optional[str] = None
    heatmap_url: Optional[str] = None
    original_url: Optional[str] = None
    report_url: Optional[str] = None
    morphology_summary: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class BatchPredictionResponse(BaseModel):
    total_processed: int
    lymphoma_detected_count: int
    rejected_count: int
    invalid_count: int
    results: List[PredictionResponse]

class ThresholdConfigUpdate(BaseModel):
    threshold: float
"""

files["backend/app/schemas/auth.py"] = """from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = "Pathologist"
    role: Optional[str] = "researcher"

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_info: dict
"""

# 4. Image Validator Service
files["backend/app/services/__init__.py"] = """"""
files["backend/app/services/image_validator.py"] = """import cv2
import numpy as np
from PIL import Image

class ImageValidator:
    \"\"\"
    Validates uploaded images to reject non-histopathological, blank, corrupted, or unsupported images.
    \"\"\"
    @staticmethod
    def validate_image(image_bytes: bytes):
        if not image_bytes or len(image_bytes) < 100:
            return False, "Uploaded file is empty or corrupted."

        # Attempt to decode as PIL Image
        try:
            pil_img = Image.open(io.BytesIO(image_bytes))
            pil_img.verify() # Verify file integrity
            
            # Reopen for content analysis (verify closes stream)
            pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        except Exception as e:
            return False, f"Unsupported or unreadable image format ({e}). Please upload a valid TIFF, PNG, or JPEG file."

        w, h = pil_img.size
        if w < 64 or h < 64:
            return False, f"Image resolution too small ({w}x{h}). Minimum required resolution is 64x64."

        # Convert to numpy for statistical analysis
        np_img = np.array(pil_img)
        
        # Check standard deviation (detect uniform/blank images)
        std_dev = np.std(np_img)
        if std_dev < 8.0:
            return False, "Image contains almost zero contrast (uniform or blank field). Please upload a valid histological slide."

        # Check mean intensity (detect completely pitch black or pure white slides)
        mean_val = np.mean(np_img)
        if mean_val < 5.0:
            return False, "Image is pitch black with no cellular structure."
        if mean_val > 250.0:
            return False, "Image is blank white with no cellular tissue."

        return True, "Valid histopathological image."
"""

for rel_path, content in files.items():
    full_path = os.path.join(project_root, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {rel_path}")

print("FastAPI core, db, schemas, and validator created successfully.")
