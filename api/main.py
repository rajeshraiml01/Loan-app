import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from loan_app.config import MODEL_PATH as DEFAULT_MODEL_PATH
from loan_app.inference import LoanPredictor
from loan_app.schemas import LoanApplication, PredictionResponse

app = FastAPI(title="Loan Approval Prediction API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

predictor = None
MODEL_PATH = os.getenv("MODEL_PATH", str(DEFAULT_MODEL_PATH))


@app.on_event("startup")
def load_model() -> None:
    global predictor
    try:
        predictor = LoanPredictor(model_path=MODEL_PATH)
    except Exception as exc:
        predictor = None
        print(f"Model load error: {exc}")


@app.get("/")
def root() -> dict:
    return {"message": "Loan Approval API is running"}


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "model_loaded": predictor is not None,
        "model_path": MODEL_PATH,
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(application: LoanApplication) -> PredictionResponse:
    if predictor is None:
        raise HTTPException(status_code=503, detail="Model is not loaded. Train model first.")

    result = predictor.predict_one(application)
    return PredictionResponse(**result)
