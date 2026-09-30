import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import pytest
import io
import json
from PIL import Image
import numpy as np
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.core.config import settings

client = TestClient(app)

def create_synthetic_histology_image(size=(224, 224)):
    # Create realistic noisy H&E-like RGB image (purple/pink cellular noise)
    arr = np.random.randint(80, 220, (size[1], size[0], 3), dtype=np.uint8)
    arr[:, :, 0] = np.clip(arr[:, :, 0] + 30, 0, 255) # Red/Pink
    arr[:, :, 2] = np.clip(arr[:, :, 2] + 40, 0, 255) # Blue/Purple
    img = Image.fromarray(arr)
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

def test_image_validation_rejection_empty():
    response = client.post(
        "/api/predict/",
        files={"file": ("corrupt.txt", b"not an image", "text/plain")}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["outcome"] == "UNABLE_TO_ANALYZE"
    assert len(data["rejection_reason"]) > 0

def test_image_validation_rejection_blank_white():
    # Pure white image with 0 standard deviation
    img = Image.new("RGB", (224, 224), (255, 255, 255))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    response = client.post(
        "/api/predict/",
        files={"file": ("white.jpg", buf.read(), "image/jpeg")}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["outcome"] == "UNABLE_TO_ANALYZE"

def test_benchmark_endpoints():
    res_bench = client.get("/api/metrics/benchmarks")
    assert res_bench.status_code == 200
    bench_data = res_bench.json()
    assert "internal_test_metrics" in bench_data or "attention_resnet50_cbam" in bench_data

    res_abl = client.get("/api/metrics/ablation")
    assert res_abl.status_code == 200
    abl_data = res_abl.json()
    assert "ablation_resnet50_no_attention" in abl_data or "status" in abl_data

    res_thresh = client.get("/api/metrics/thresholds")
    assert res_thresh.status_code == 200
    thresh_data = res_thresh.json()
    assert "recommended_threshold" in thresh_data

def test_histology_prediction_flow():
    buf = create_synthetic_histology_image()
    response = client.post(
        "/api/predict/",
        files={"file": ("sample_histology.jpg", buf.read(), "image/jpeg")}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["outcome"] in ["LYMPHOMA_DETECTED", "NO_LYMPHOMA_DETECTED"]
    assert "probabilities" in data
    assert "CLL" in data["probabilities"]
    assert "FL" in data["probabilities"]
    assert "MCL" in data["probabilities"]
