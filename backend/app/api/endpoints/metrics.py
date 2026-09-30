import os
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
    return {
        "classes": settings.CLASSES,
        "class_full_names": settings.CLASS_FULL_NAMES,
        "dataset_name": "Malignant Lymphoma Classification (15,000 Subset)",
        "total_samples": 15000,
        "class_distribution": {
            "CLL": 5000,
            "FL": 5000,
            "MCL": 5000
        },
        "splits": {
            "train": 10500,
            "validation": 2250,
            "test": 2250
        },
        "external_benchmark_samples": 374
    }

@router.get("/histories")
def get_training_histories():
    path = os.path.join(settings.RESULTS_DIR, "training_histories_15k.json")
    if not os.path.exists(path):
        path = os.path.join(settings.RESULTS_DIR, "training_histories.json")
    if not os.path.exists(path):
        return {"status": "pending", "message": "Training in progress."}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

@router.get("/model-info")
def get_model_info():
    meta_path = os.path.join(settings.BASE_DIR, "models", "model_v2_15000", "model_metadata.json")
    metadata = {}
    if os.path.exists(meta_path):
        with open(meta_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)
    return {
        "active_model_version": settings.ACTIVE_MODEL_VERSION,
        "available_models": settings.AVAILABLE_MODELS,
        "metadata": metadata
    }
