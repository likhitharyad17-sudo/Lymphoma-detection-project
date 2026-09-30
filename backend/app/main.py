import os
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
