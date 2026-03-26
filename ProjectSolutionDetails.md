# Loan Approval Prediction Application

## 1. Problem Statement

**Context:**  
Financial institutions need to decide quickly and consistently whether to approve or reject a loan application. Traditional rule-based systems are slow to adapt and often fail to capture non-linear patterns in applicant data.

**Business Goal:**  
Build a machine learning model that predicts whether a loan applicant is likely to **default** on a loan, and expose that model as a real-time web service that any loan officer (or consumer-facing portal) can query.

**Secondary Requirement:**  
Ensure the model does not exhibit unfair bias against protected demographic groups (gender, education level). Quantify and report approval rates per group so stakeholders can make informed policy decisions.

## 2. Proposed Solution

### High-Level Approach

```
Raw CSV data
     │
     ▼
Exploratory Data Analysis (Jupyter Notebook)
     │
     ▼
Scikit-learn Preprocessing Pipeline
  ├── Numeric: Median Imputation → StandardScaler
  └── Categorical: Mode Imputation → OneHotEncoder
     │
     ▼
XGBoost Classifier (n_estimators=200, max_depth=6, learning_rate=0.1)
     │
     ▼
Youden's J Optimal Threshold Selection
     │
     ▼
Persisted model bundle  →  FastAPI /predict endpoint  →  Streamlit Web UI
```

## 3. Dataset Overview

**File:** `data/loan_data.csv`

| # | Feature | Type | Description |
|---|---------|------|-------------|
| 1 | `person_age` | Numeric | Applicant age (18–100) |
| 2 | `person_gender` | Categorical | `male` / `female` |
| 3 | `person_education` | Categorical | `High School`, `Associate`, `Bachelor`, `Master`, `Doctorate` |
| 4 | `person_income` | Numeric | Annual income (USD) |
| 5 | `person_emp_exp` | Numeric | Employment experience (years) |
| 6 | `person_home_ownership` | Categorical | `RENT`, `OWN`, `MORTGAGE`, `OTHER` |
| 7 | `loan_amnt` | Numeric | Requested loan amount |
| 8 | `loan_intent` | Categorical | `PERSONAL`, `EDUCATION`, `MEDICAL`, `VENTURE`, `HOMEIMPROVEMENT`, `DEBTCONSOLIDATION` |
| 9 | `loan_int_rate` | Numeric | Annual interest rate (%) |
| 10 | `loan_percent_income` | Numeric | Loan-to-income ratio |
| 11 | `cb_person_cred_hist_length` | Numeric | Credit history length (years) |
| 12 | `credit_score` | Numeric | Credit bureau score (300–850) |
| 13 | `previous_loan_defaults_on_file` | Categorical | `Yes` / `No` |
| — | **`loan_status`** | **Target** | `1` = default (rejected), `0` = no default (approved) |

**Target semantics (critical):**
- `loan_status = 1` → applicant is predicted to **default → REJECTED**
- `loan_status = 0` → applicant is predicted to be **safe → APPROVED**