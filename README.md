# AI/ML Case Study: Loan Approval Prediction

## Instructions

This case study is designed to evaluate your ability to implement a working prototype based on a given set of requirements.
We will evaluate your submission based on:

* are the desired features implemented?
* did you provide a runnable prototype?
* can you reason about bringing this into production?
* how did you gain confidence in your implementation?

Please ensure that the code in the submission is fully functional on a local machine, and include instructions for building and running it.
Although it should still pass muster in code review, it is fine for the code to not be completely production ready in the submission.

As a guide for design decisions, treat this exercise as the initial prototype of an MVP that will need to be productionalized and
scaled out in the future, and be prepared for follow-up discussion on how that would look.


## Quick Start

### Prerequisites
- Python 3.13+
- Docker & Docker Compose (for containerized deployment)
- `uv` package manager (recommended) or `pip`

### 1. Environment Setup

```bash
# Create virtual environment
uv init
uv venv
source .venv/bin/activate  
# Install dependencies
uv pip install -e .
```

### 2. Train the Model

```bash
# From project root
python -m main
```
This will:
- Load `data/loan_data.csv`
- Train an XGBoost classifier
- Save to `models/best_model.joblib`
- Save metrics to `artifacts/metrics.json`

### 3a. Local Development (No Docker)

```bash
# Terminal 1: API Server
python -m uvicorn api.main:app --reload

# Terminal 2: Streamlit UI
streamlit run ui/app.py
```

- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- UI: http://localhost:8501

### 3b. Production with Docker

```bash
# Build and start all services
docker-compose up --build

# Or rebuild without cache
docker-compose up --build --no-cache

# Stop services
docker-compose down
```

**Services:**
- **API**: http://localhost:8000 (FastAPI)
- **API Docs**: http://localhost:8000/docs (Swagger)
- **UI**: http://localhost:8501 (Streamlit)

### 4. Using the Application

1. **Train the model** (if not already done):
   ```bash
   python -m loan_app.train
   ```

2. **Start the API & UI** (Docker or local):
   ```bash
   docker-compose up  # Docker
   # OR
   python -m uvicorn api.main:app & streamlit run ui/app.py  # Local
   ```

3. **Open the UI** in browser: `http://localhost:8501`
   - Fill in loan applicant details
   - Click "Get Prediction"
   - View approval decision and confidence

## Architecture

- **`src/loan_app/`** — Core ML modules
  - `config.py` — Feature definitions, paths, hyperparameters
  - `data.py` — Data loading & splitting
  - `modeling.py` — Preprocessing pipeline and XGBoost model spec
  - `evaluation.py` — Metrics and plots
  - `train.py` — Main training loop; saves best model to `models/`
  - `inference.py` — Prediction wrapper
  - `schemas.py` — Pydantic models for API
- **`api/main.py`** — FastAPI server that loads model from `models/`
- **`ui/app.py`** — Streamlit web UI with full loan application form
- **`models/`** — Trained model storage (created after training)
- **`artifacts/`** — Metrics, analysis, ROC plots
- **`data/loan_data.csv`** — Load data for training
- **`infra/`** — K8s and AKS configuration code
  - `/iac` — Terraform code to deploy AKS
  - `/k8s` - Kubernetes deployment and service files
- **`notebooks/loan_analysis_modular.ipynb`** — Clean EDA + training notebook

## Docker Deployment Details

### Volume Mounts
- **API**: Mounts `/workspace/src`, `/workspace/models`, `/workspace/data`, `/workspace/artifacts`
- **UI**: Mounts `/app` (read-only)

### Environment Variables
- **API**: `MODEL_PATH=/workspace/models/best_model.joblib`
- **UI**: `API_URL=http://api:8000/predict`

### Health Check
API includes a health check endpoint (`/health`) that Docker monitors to confirm the API is ready.

## Project Structure
```
Loan-app
├── api
│   ├── Dockerfile
│   └── main.py
├── artifacts
│   ├── confusion_matrix.png
│   ├── metrics.json
│   └── roc_curve.png
├── data
│   └── loan_data.csv
├── diagrams
├── docker-compose.yaml
├── infra
│   ├── iac
│   │   ├── acr.tf
│   │   ├── aks.tf
│   │   ├── main.tf
│   │   ├── monitoring.tf
│   │   ├── outputs.tf
│   │   ├── providers.tf
│   │   ├── terraform.tfvars.example
│   │   ├── variables.tf
│   │   └── versions.tf
│   └── k8s
│       ├── api-deployment.yaml
│       ├── api-service.yaml
│       ├── namespace.yaml
│       ├── secrets.example.yaml
│       ├── ui-deployment.yaml
│       └── ui-service.yaml
├── main.py
├── models
│   └── best_model.joblib
├── notebooks
├── pyproject.toml
├── README.md
├── requirements.txt
├── src
│   ├── loan_app
│   │   ├── config.py
│   │   ├── data.py
│   │   ├── evaluation.py
│   │   ├── inference.py
│   │   ├── modeling.py
│   │   ├── schemas.py
│   │   └── train.py
│   └── loan_app.egg-info
│       ├── dependency_links.txt
│       ├── PKG-INFO
│       ├── requires.txt
│       ├── SOURCES.txt
│       └── top_level.txt
├── ui
│   ├── app.py
│   └── Dockerfile
├── utils
```