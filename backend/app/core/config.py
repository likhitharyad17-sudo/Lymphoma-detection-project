import os
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

    # Model Versioning
    ACTIVE_MODEL_VERSION: str = "model_v2_15000"
    AVAILABLE_MODELS: dict = {
        "model_v2_15000": "Attention-Augmented ResNet-50 + CBAM (15,000-Image Dataset, 100.0% Test Acc)",
        "model_v1_374": "Attention-Augmented ResNet-50 + CBAM (374-Slide Dataset, 85.96% Test Acc)"
    }

    IMAGE_SIZE: int = 224
    NUM_CLASSES: int = 3

    # File Paths
    BASE_DIR: str = r"D:\Lymphoma Detection Project"
    MODEL_PATH: str = os.path.join(BASE_DIR, "models", "model_v2_15000", "best_model.pth")
    BEST_MODEL_PATH: str = os.path.join(BASE_DIR, "models", "model_v2_15000", "best_model.pth")
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
