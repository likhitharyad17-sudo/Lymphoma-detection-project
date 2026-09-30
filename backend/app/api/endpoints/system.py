import os
import torch
from fastapi import APIRouter
from backend.app.core.config import settings

router = APIRouter()

@router.get("/health")
def system_health():
    cuda_avail = torch.cuda.is_available()
    gpu_name = torch.cuda.get_device_name(0) if cuda_avail else "N/A"
    gpu_mem = torch.cuda.get_device_properties(0).total_memory / (1024**3) if cuda_avail else 0.0

    ram_gb = 16.0
    try:
        import psutil
        ram_gb = round(psutil.virtual_memory().total / (1024**3), 2)
    except Exception:
        pass

    return {
        "status": "online",
        "project": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "classes": settings.CLASSES,
        "hardware": {
            "cuda_available": cuda_avail,
            "gpu_name": gpu_name,
            "gpu_memory_gb": round(gpu_mem, 2),
            "cpu_cores": os.cpu_count() or 8,
            "ram_gb": ram_gb
        },
        "threshold": settings.LYMPHOMA_CONFIDENCE_THRESHOLD
    }
