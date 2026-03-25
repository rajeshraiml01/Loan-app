from pydantic import BaseModel, Field


class LoanApplication(BaseModel):
    person_age: float = Field(..., ge=18, le=100)
    person_gender: str
    person_education: str
    person_income: float = Field(..., ge=0)
    person_emp_exp: float = Field(..., ge=0)
    person_home_ownership: str
    loan_amnt: float = Field(..., gt=0)
    loan_intent: str
    loan_int_rate: float = Field(..., gt=0)
    loan_percent_income: float = Field(..., ge=0, le=1.5)
    cb_person_cred_hist_length: float = Field(..., ge=0)
    credit_score: float = Field(..., ge=300, le=850)
    previous_loan_defaults_on_file: str


class PredictionResponse(BaseModel):
    loan_status: int
    probability: float
    threshold: float
    decision: str
