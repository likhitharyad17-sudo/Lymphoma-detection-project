import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String(128), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(32), default="USER", nullable=False) # "USER" or "ADMIN"
    status = Column(String(32), default="ACTIVE", nullable=False) # "ACTIVE", "DISABLED", "INACTIVE"
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    predictions = relationship("PredictionRecord", back_populates="user", cascade="all, delete-orphan")


class PredictionRecord(Base):
    __tablename__ = "prediction_records"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    case_id = Column(String(64), unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user_email = Column(String(255), nullable=True)
    user_name = Column(String(128), nullable=True)
    
    file_name = Column(String(255))
    file_path = Column(String(512), nullable=True)
    
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
    
    # Privacy & Visibility Controls
    # is_hidden_by_admin: Admin decides if result should be hidden from general view without deleting
    is_hidden_by_admin = Column(Boolean, default=False, nullable=False)
    # is_private: User decides to keep their test private (only visible to themselves and Admin)
    is_private = Column(Boolean, default=False, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

    patient_id = Column(String(64), default="ANONYMOUS")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="predictions")
    feedbacks = relationship("FeedbackRecord", back_populates="prediction", cascade="all, delete-orphan")


class FeedbackRecord(Base):
    __tablename__ = "feedback_records"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    prediction_id = Column(Integer, ForeignKey("prediction_records.id"))
    review_status = Column(String(64)) # 'Verified Correct', 'Misclassified', 'Needs Further Testing'
    notes = Column(Text, nullable=True)
    reviewed_by = Column(String(128), default="Pathologist")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    prediction = relationship("PredictionRecord", back_populates="feedbacks")
