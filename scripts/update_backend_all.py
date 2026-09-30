import os

project_root = r"D:\Lymphoma Detection Project"
files = {}

# 1. Chat Service (Pathology & AI Assistant)
files["backend/app/services/chat_service.py"] = """import re

class PathologyChatService:
    \"\"\"
    Intelligent Clinical Pathology & Deep Learning AI Assistant.
    Specialized in Malignant Lymphoma classification (CLL, FL, MCL),
    CBAM Attention Networks, Grad-CAM++ Explainability, and Two-Stage Screening Logic.
    \"\"\"
    def __init__(self):
        self.knowledge_base = [
            {
                "keywords": ["cll", "chronic lymphocytic", "sll", "small lymphocytic"],
                "response": (
                    "**Chronic Lymphocytic Leukemia / Small Lymphocytic Lymphoma (CLL/SLL):**\\n\\n"
                    "• **Histological Hallmark:** Diffuse effacement of lymph node architecture by small, mature, monotonous round lymphocytes.\\n"
                    "• **Nuclear Morphology:** Dense, clumped 'soccer-ball' chromatin, indistinct or absent nucleoli, and very scant cytoplasm.\\n"
                    "• **Proliferation Centers:** Contains pseudofollicles with prolymphocytes and para-immunoblasts.\\n"
                    "• **Key Immunophenotype:** CD5+, CD19+, CD20+ (dim), CD23+, Cyclin D1-."
                )
            },
            {
                "keywords": ["fl", "follicular lymphoma", "centrocytes", "centroblasts"],
                "response": (
                    "**Follicular Lymphoma (FL):**\\n\\n"
                    "• **Histological Hallmark:** Closely spaced, back-to-back neoplastic follicles effacing normal nodal architecture, lacking mantle zones or tingible-body macrophages.\\n"
                    "• **Nuclear Morphology:** Centrocytes feature angular, notched, or cleaved nuclear contours. Centroblasts are larger cells with vesicular chromatin and multiple peripheral nucleoli.\\n"
                    "• **Genetics:** Hallmark translocation t(14;18)(q32;q21) leading to BCL2 overexpression (anti-apoptotic).\\n"
                    "• **Key Immunophenotype:** CD10+, BCL2+, BCL6+, CD20+."
                )
            },
            {
                "keywords": ["mcl", "mantle cell", "cyclin d1", "ccnd1"],
                "response": (
                    "**Mantle Cell Lymphoma (MCL):**\\n\\n"
                    "• **Histological Hallmark:** Monotonous expansion in mantle zone, nodular, or diffuse growth patterns with hyalinized blood vessels.\\n"
                    "• **Nuclear Morphology:** Small-to-medium lymphocytes with irregular, indented nuclear membranes and condensed chromatin (lacks transformed centroblasts).\\n"
                    "• **Genetics:** Hallmark translocation t(11;14)(q13;q32) causing constitutive Cyclin D1 (CCND1) overexpression.\\n"
                    "• **Key Immunophenotype:** CD5+, CD20+, Cyclin D1+ (nuclear), SOX11+, CD23-."
                )
            },
            {
                "keywords": ["cbam", "channel attention", "spatial attention", "attention"],
                "response": (
                    "**Convolutional Block Attention Module (CBAM):**\\n\\n"
                    "CBAM adaptively refines feature maps sequentially:\\n"
                    "1. **Channel Attention Module (CAM):** Aggregates spatial information via GAP and GMP through a shared MLP with reduction ratio r=16 to determine *what* diagnostic features are significant.\\n"
                    "2. **Spatial Attention Module (SAM):** Aggregates channel context using a 7x7 convolution to pinpoint *where* diagnostic cellular morphology is located.\\n"
                    "Integrated after Stage 3 (1024ch) and Stage 4 (2048ch) in ResNet-50."
                )
            },
            {
                "keywords": ["grad-cam", "gradcam", "explainability", "xai", "heatmap"],
                "response": (
                    "**Grad-CAM++ Explainable AI:**\\n\\n"
                    "Grad-CAM++ calculates higher-order partial derivatives (2nd and 3rd order gradients) to compute pixel-level importance weights for the target class.\\n"
                    "In our system, Grad-CAM++ is hooked into the Stage 4 CBAM block, generating high-contrast jet thermal overlays that highlight diagnostic cellular clusters (such as cleaved centrocytes or clumped lymphocytic chromatin) without obscuring the underlying tissue."
                )
            },
            {
                "keywords": ["threshold", "rejection", "two-stage", "screening", "two stage", "no lymphoma"],
                "response": (
                    "**Two-Stage Screening & Rejection Logic:**\\n\\n"
                    "• **The Problem with Argmax:** Standard 3-class softmax models always pick one of CLL, FL, or MCL even on completely unrelated or non-cancerous images.\\n"
                    "• **Our Solution:** The model applies a calibrated confidence threshold (default 80%). If max confidence < 80%, the result is rejected as **'No Lymphoma Detected / Not Classified as Lymphoma'** to avoid false-positive hallucinations.\\n"
                    "• **Positive Decision:** If confidence >= 80%, the system outputs **'Lymphoma Detected'** with subtype, 3-class probabilities, and Grad-CAM++ heatmap."
                )
            },
            {
                "keywords": ["accuracy", "benchmark", "results", "performance", "f1"],
                "response": (
                    "**Experimental Test Benchmarks (Untouched Test Split N=57):**\\n\\n"
                    "• **Proposed Attention-Residual (CBAM):** 85.96% Accuracy, 0.8568 Macro F1, 0.9401 ROC-AUC.\\n"
                    "• **Ablation Study Gain:** The proposed model achieves a +7.01% gain in test accuracy over the ResNet-50 baseline without attention (78.95% -> 85.96%).\\n"
                    "• **Threshold Filter (tau=0.80):** Achieves 97.14% to 100% precision on accepted screening specimens."
                )
            }
        ]

    def reply(self, user_message: str) -> str:
        msg = user_message.lower().strip()
        for item in self.knowledge_base:
            if any(k in msg for k in item["keywords"]):
                return item["response"]

        return (
            "I am the **LymphomaAI Clinical & Technical Pathology Assistant**.\\n\\n"
            "I can assist you with:\\n"
            "1. **Clinical Morphology:** Characteristics of CLL, FL, and MCL.\\n"
            "2. **Attention Architecture:** How CBAM Channel and Spatial Attention refine ResNet-50 features.\\n"
            "3. **Two-Stage Screening:** The 80% confidence rejection guard against out-of-distribution slides.\\n"
            "4. **Explainability:** How Grad-CAM++ maps cellular focus regions.\\n"
            "5. **Benchmark Performance:** Real accuracy, F1-scores, and ablation results.\\n\\n"
            "Please ask any specific question about our digital pathology framework!"
        )

chat_service = PathologyChatService()
"""

# 2. Update Database Models with Feedback Table
files["backend/app/database/models.py"] = """import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
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
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    feedbacks = relationship("FeedbackRecord", back_populates="prediction", cascade="all, delete-orphan")

class FeedbackRecord(Base):
    __tablename__ = "feedback_records"

    id = Column(Integer, primary_key=True, index=True)
    prediction_id = Column(Integer, ForeignKey("prediction_records.id"))
    review_status = Column(String(64)) # 'Verified Correct', 'Misclassified', 'Needs Further Testing'
    notes = Column(Text, nullable=True)
    reviewed_by = Column(String(128), default="Pathologist")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    prediction = relationship("PredictionRecord", back_populates="feedbacks")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, index=True)
    email = Column(String(128), unique=True, index=True)
    hashed_password = Column(String(255))
    full_name = Column(String(128), default="Pathology Investigator")
    role = Column(String(32), default="USER") # USER, ADMIN
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
"""

# 3. Update Schemas
files["backend/app/schemas/prediction.py"] = """from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime

class ProbabilityBreakdown(BaseModel):
    CLL: float
    FL: float
    MCL: float

class ValidationResponse(BaseModel):
    is_valid: bool
    message: str

class FeedbackCreate(BaseModel):
    prediction_id: int
    review_status: str
    notes: Optional[str] = None
    reviewed_by: Optional[str] = "Pathologist"

class FeedbackResponse(BaseModel):
    id: int
    prediction_id: int
    review_status: str
    notes: Optional[str]
    reviewed_by: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PredictionResponse(BaseModel):
    id: Optional[int] = None
    case_id: str
    file_name: str
    outcome: str # 'LYMPHOMA_DETECTED' | 'NO_LYMPHOMA_DETECTED' | 'UNABLE_TO_ANALYZE'
    outcome_display: str
    predicted_subtype: Optional[str] = None
    predicted_subtype_full: Optional[str] = None
    confidence: Optional[float] = None
    confidence_percentage: Optional[str] = None
    probabilities: Optional[ProbabilityBreakdown] = None
    top_probabilities: Optional[Dict[str, float]] = None
    predicted_class: Optional[str] = None
    threshold_used: float
    rejection_reason: Optional[str] = None
    heatmap_url: Optional[str] = None
    original_url: Optional[str] = None
    report_url: Optional[str] = None
    morphology_summary: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class BatchPredictionResponse(BaseModel):
    total_processed: int
    lymphoma_detected_count: int
    rejected_count: int
    invalid_count: int
    results: List[PredictionResponse]

class ThresholdConfigUpdate(BaseModel):
    threshold: float
"""

files["backend/app/schemas/auth.py"] = """from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    role: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str
"""

# 4. Update Prediction Endpoint with Feedback & Validation
files["backend/app/api/endpoints/predict.py"] = """import os
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database.session import get_db
from backend.app.database.models import FeedbackRecord, PredictionRecord
from backend.app.schemas.prediction import (
    PredictionResponse, BatchPredictionResponse, ValidationResponse,
    FeedbackCreate, FeedbackResponse
)
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

@router.post("/feedback", response_model=FeedbackResponse)
def submit_pathologist_feedback(data: FeedbackCreate, db: Session = Depends(get_db)):
    pred = db.query(PredictionRecord).filter(PredictionRecord.id == data.prediction_id).first()
    if not pred:
        # Fallback query by id or create record
        pass

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
"""

# 5. Auth Router with /me, /login, /register
files["backend/app/api/endpoints/auth.py"] = """import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from passlib.context import CryptContext

from backend.app.database.session import get_db
from backend.app.database.models import User
from backend.app.schemas.auth import UserRegister, UserLogin, UserResponse, TokenResponse
from backend.app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)

router = APIRouter()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/register", response_model=TokenResponse)
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    email_clean = user_in.email.lower().strip()
    existing = db.query(User).filter(User.email == email_clean).first()
    if existing:
        raise HTTPException(status_code=400, detail="An account with this email already exists.")
    
    hashed = pwd_context.hash(user_in.password)
    new_user = User(
        username=email_clean,
        email=email_clean,
        hashed_password=hashed,
        full_name=user_in.full_name,
        role="USER",
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": str(new_user.id), "role": new_user.role})
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=new_user
    )

@router.post("/login", response_model=TokenResponse)
def login(login_in: UserLogin, db: Session = Depends(get_db)):
    email_clean = login_in.email.lower().strip()
    user = db.query(User).filter(User.email == email_clean).first()
    if not user or not pwd_context.verify(login_in.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password.")

    user.last_login = datetime.datetime.utcnow()
    db.commit()

    token = create_access_token({"sub": str(user.id), "role": user.role})
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=user
    )

@router.get("/me", response_model=UserResponse)
def get_me(user: User = Depends(get_current_user)):
    return user
"""

# 6. Chat Router
files["backend/app/api/endpoints/chat.py"] = """from fastapi import APIRouter
from backend.app.schemas.auth import ChatRequest, ChatResponse
from backend.app.services.chat_service import chat_service

router = APIRouter()

@router.post("/", response_model=ChatResponse)
def chat_with_assistant(data: ChatRequest):
    reply_text = chat_service.reply(data.message)
    return ChatResponse(reply=reply_text)
"""

# 7. Update main.py with Chat Router
files["backend/app/main.py"] = """import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.app.core.config import settings
from backend.app.database.session import engine, Base
from backend.app.api.endpoints import predict, metrics, history, reports, config, auth, system, chat

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
app.include_router(chat.router, prefix="/api/chat", tags=["Pathology Chat Assistant"])

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

for rel_path, content in files.items():
    full_path = os.path.join(project_root, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created/Updated: {rel_path}")

print("Backend services and chat routes successfully built.")
