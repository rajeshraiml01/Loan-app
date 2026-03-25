from pathlib import Path

import joblib
import pandas as pd

from loan_app.config import MODEL_FEATURES, MODEL_PATH
from loan_app.schemas import LoanApplication


class LoanPredictor:
    def __init__(self, model_path: Path = MODEL_PATH) -> None:
        model_bundle = joblib.load(model_path)
        self.pipeline = model_bundle["model"]
        self.threshold = float(model_bundle["threshold"])

    @staticmethod
    def _normalize_payload(payload: dict) -> dict:
        normalized = payload.copy()
        normalized["person_gender"] = str(normalized["person_gender"]).strip().lower()
        normalized["person_home_ownership"] = str(normalized["person_home_ownership"]).strip().upper()
        normalized["loan_intent"] = str(normalized["loan_intent"]).strip().upper()
        normalized["previous_loan_defaults_on_file"] = str(
            normalized["previous_loan_defaults_on_file"]
        ).strip().title()
        normalized["person_education"] = str(normalized["person_education"]).strip().title()
        return normalized

    def predict_one(self, application: LoanApplication) -> dict:
        payload = self._normalize_payload(application.model_dump())
        x = pd.DataFrame([payload])[MODEL_FEATURES]
        default_probability = float(self.pipeline.predict_proba(x)[0][1])
        label = int(default_probability >= self.threshold)
        decision = "Rejected" if label == 1 else "Approved"
        return {
            "loan_status": label,
            "probability": default_probability,
            "threshold": self.threshold,
            "decision": decision,
        }
