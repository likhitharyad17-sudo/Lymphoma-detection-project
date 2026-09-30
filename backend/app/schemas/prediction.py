from pydantic import BaseModel, ConfigDict
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
    user_id: Optional[int] = None
    user_email: Optional[str] = None
    user_name: Optional[str] = None
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
    model_version: Optional[str] = "model_v2_15000"
    is_hidden_by_admin: bool = False
    is_private: bool = False
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class BatchPredictionResponse(BaseModel):
    total_processed: int
    lymphoma_detected_count: int
    rejected_count: int
    invalid_count: int
    results: List[PredictionResponse]

class VisibilityUpdateRequest(BaseModel):
    is_hidden_by_admin: bool

class PrivacyUpdateRequest(BaseModel):
    is_private: bool

class ThresholdConfigUpdate(BaseModel):
    threshold: float
