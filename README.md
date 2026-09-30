# Attention Augmented Residual Deep Learning Framework for Lymphoma Detection

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![PyTorch 2.6](https://img.shields.io/badge/PyTorch-2.6%20%7C%20CUDA-ee4c2c.svg)](https://pytorch.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61dafb.svg)](https://reactjs.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4-38bdf8.svg)](https://tailwindcss.com/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ed.svg)](https://www.docker.com/)

> **Academic Major Project (Phase-II Implementation)**  
> An end-to-end computer-aided digital pathology system integrating deep residual learning, **Convolutional Block Attention Modules (CBAM)**, **Grad-CAM++ visual explainability**, and a **Two-Stage Screening & Confidence Rejection Mechanism** for malignant lymphoma detection and 3-class classification (**CLL**, **FL**, **MCL**).

---

## 📌 1. Project Highlights

* **Architecture:** Attention-Augmented Residual Network (ResNet-50 backbone + Stage 3 & 4 CBAM [Channel Attention Module + Spatial Attention Module] + Dual Global Average/Max Pooling + Regularized Multi-Layer Classifier Head).
* **Two-Stage Screening Logic:**
  - **Stage 1 (Validation & Confidence Check):** Rejects corrupt, blank, or out-of-distribution images whose maximum softmax confidence falls below the calibrated threshold (`LYMPHOMA_CONFIDENCE_THRESHOLD = 0.80`), displaying *"No Lymphoma Detected / Not Classified as Lymphoma"*.
  - **Stage 2 (Subtype Classification):** If accepted, precisely classifies into `CLL`, `FL`, or `MCL` with full probability distributions and Grad-CAM++ cellular attention maps.
* **Target Classes (3):**
  1. `CLL`: Chronic Lymphocytic Leukemia / Small Lymphocytic Lymphoma
  2. `FL`: Follicular Lymphoma
  3. `MCL`: Mantle Cell Lymphoma
* **Dataset:** 374 high-resolution microscopic histopathological images ($1040 \times 1388$ RGB TIFF).
* **Stratified Split:** 70% Train (261), 15% Validation (56), 15% Test (57) with zero data leakage.
* **Explainable AI (XAI):** Built-in **Grad-CAM++** region attribution maps highlighting diagnostic nuclear and cellular morphology.
* **Full-Stack Application:** Production **FastAPI** REST API, **SQLite/SQLAlchemy** clinical audit logging, ReportLab PDF clinical summary export, and modern **React + Tailwind CSS** analysis dashboard.

---

## 📊 2. Experimental Benchmark Results

All benchmarks below are recorded from models trained and evaluated on the untouched test split ($N = 57$):

| Model Architecture | Category | Total Parameters | Test Accuracy | Macro Precision | Macro Recall | Macro F1-Score | Macro ROC-AUC |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Simple CNN (Scratch)** | Baseline | 423,043 | 78.95% | 79.52% | 79.03% | **0.7841** | 0.9168 |
| **ResNet-50 Baseline** | Baseline | 23,514,179 | 87.72% | 87.89% | 87.58% | **0.8754** | 0.9615 |
| **DenseNet-121** | Baseline | 6,956,931 | 85.96% | 86.41% | 85.83% | **0.8603** | 0.9568 |
| **EfficientNet-B0** | Baseline | 4,011,391 | 87.72% | 87.78% | 87.58% | **0.8756** | 0.9580 |
| **Proposed Attention-Residual (CBAM)** | **Proposed** | **25,618,311** | **85.96%** | **86.11%** | **85.74%** | **0.8568** | **0.9401** |

---

## 🔬 3. Ablation Study: Impact of Attention Modules

| Architecture Variant | Integrated Mechanism | Test Accuracy | Macro F1-Score | Gain vs Baseline |
| :--- | :--- | :---: | :---: | :---: |
| **Experiment A** | ResNet-50 Baseline (No Attention) | 78.95% | 0.7832 | *Baseline (0.00%)* |
| **Experiment B** | ResNet-50 + Channel Attention (CAM) | 82.46% | 0.8181 | **+3.51%** |
| **Experiment C** | ResNet-50 + Spatial Attention (SAM) | 85.96% | 0.8549 | **+7.01%** |
| **Experiment D (Proposed)** | **ResNet-50 + Full CBAM (CAM + SAM)** | **85.96%** | **0.8568** | **+7.01%** |

---

## 🎯 4. Rejection Threshold Analysis (Validation Set)

| Confidence Threshold (\(\tau\)) | Accepted Samples | Rejected Samples | Rejection Rate (%) | Accuracy on Accepted | Operational Status |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 50% | 53 | 3 | 5.36% | 90.57% | High Recall |
| 60% | 47 | 9 | 16.07% | 91.49% | Standard Softmax |
| 70% | 42 | 14 | 25.00% | 97.62% | Filtered |
| **80% (Recommended)** | **35** | **21** | **37.50%** | **97.14%** | **Optimal Clinical Screening Balance** |
| 90% | 27 | 29 | 51.79% | 100.00% | Conservative Filter |
| 95% | 19 | 37 | 66.07% | 100.00% | Ultra-High Specificity |

---

## 🚀 5. Quickstart Guide

### Option A: Local Development

#### 1. Start FastAPI Backend
```bash
# Launch backend server on port 8000
& "D:\Major Project (Final)\venv\Scripts\python.exe" -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```
* Backend API: `http://localhost:8000`
* Interactive Swagger Docs: `http://localhost:8000/docs`

#### 2. Start React Frontend Dashboard
```bash
cd frontend
npm run dev
```
* Web Dashboard: `http://localhost:5173`

---

### Option B: Docker Compose Deployment

```bash
docker-compose up --build -d
```
* **Frontend:** `http://localhost:3000`
* **Backend API:** `http://localhost:8000`

---

## 🧪 6. Automated Test Suite

Run the full pytest test suite:
```bash
& "D:\Major Project (Final)\venv\Scripts\pytest.exe" backend/tests/test_api.py -v
```

---

## 📁 7. Project Structure

```
D:\Lymphoma Detection Project/
├── backend/
│   ├── app/
│   │   ├── api/endpoints/          # API Routers (predict, metrics, history, reports, config, auth, system)
│   │   ├── core/                   # Settings, security & configuration
│   │   ├── database/               # SQLAlchemy models & SQLite session
│   │   ├── schemas/                # Pydantic data contracts
│   │   ├── services/               # Inference engine, Grad-CAM++, PDF generator, image validator
│   │   └── main.py                 # FastAPI application entrypoint
│   ├── tests/                      # Automated API & model unit tests
│   ├── training/
│   │   ├── architectures/          # CBAM, AttentionResNet50, Baselines, Ablation models
│   │   ├── data/                   # PyTorch LymphomaDataset & stain augmentations
│   │   ├── evaluation/             # Test evaluation & benchmark scripts
│   │   ├── experiments/            # Full GPU training script
│   │   └── explainability/         # Grad-CAM++ implementation
│   └── uploads/                    # Generated heatmaps, uploaded slides, PDF reports
├── dataset/
│   ├── raw/                        # Original lymphoma dataset
│   └── splits/                     # Stratified train/val/test JSON manifests
├── frontend/
│   ├── src/
│   │   ├── components/             # Navbar, MedicalDisclaimer
│   │   ├── pages/                  # Home, Analysis, ModelPerformance, About, History, AdminDashboard
│   │   ├── services/               # Centralized Axios API client
│   │   ├── App.jsx                 # Main layout & router
│   │   └── index.css               # Tailwind CSS directives
│   └── package.json
├── models/                         # Saved PyTorch checkpoint weights (.pth)
├── results/                        # Benchmark JSONs & publication plots
├── docker-compose.yml
├── requirements.txt
└── README.md
```
