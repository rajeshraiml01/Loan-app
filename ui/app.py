"""
Streamlit UI for Loan Approval Prediction
Connect to the FastAPI backend to get loan approval predictions.
"""

import streamlit as st
import requests
import os

st.set_page_config(page_title="Loan Approval Predictor", page_icon="💰")
st.title(" Loan Approval Predictor")

API_URL = os.getenv("API_URL", "http://localhost:8000/predict")

with st.form("loan_application"):
    st.subheader("Applicant Information")
    col1, col2 = st.columns(2)
    
    with col1:
        person_age = st.slider(
            "Age", min_value=18, max_value=100, value=30,
            help="Age of the applicant (18-100 years)"
        )
        person_income = st.number_input(
            "Annual Income ($)", min_value=0.0, value=50000.0, step=1000.0,
            help="Annual household income in USD"
        )
        person_emp_exp = st.number_input(
            "Years of Employment Experience", min_value=0.0, value=5.0, step=0.5,
            help="Total years of employment experience"
        )
        credit_score = st.slider(
            "Credit Score", min_value=300, max_value=850, value=650,
            help="Credit score (300-850)"
        )
    
    with col2:
        person_gender = st.selectbox(
            "Gender", options=["male", "female"],
            help="Use the dataset categories expected by the model: male or female"
        )
        person_education = st.selectbox(
            "Education Level", 
            options=["High School", "Associate", "Bachelor", "Master", "Doctorate"],
            help="Highest education level completed"
        )
        person_home_ownership = st.selectbox(
            "Home Ownership Status",
            options=["RENT", "OWN", "MORTGAGE", "OTHER"],
            help="Use one of the model categories: RENT, OWN, MORTGAGE, or OTHER"
        )
        previous_loan_defaults_on_file = st.selectbox(
            "Previous Loan Defaults?",
            options=["No", "Yes"],
            help="Previous loan default history from the original dataset labels"
        )
    
    st.subheader("Loan Details")
    col3, col4 = st.columns(2)
    
    with col3:
        loan_amnt = st.number_input(
            "Loan Amount ($)", min_value=1.0, value=10000.0, step=500.0,
            help="Loan amount requested in USD"
        )
        loan_int_rate = st.slider(
            "Interest Rate (%)", min_value=0.0, max_value=35.0, value=10.0, step=0.1,
            help="Annual interest rate (0-35%)"
        )
        cb_person_cred_hist_length = st.number_input(
            "Credit History Length (years)", min_value=0.0, value=5.0, step=0.5,
            help="Length of credit history in years"
        )
    
    with col4:
        loan_intent = st.selectbox(
            "Loan Purpose",
            options=["PERSONAL", "EDUCATION", "MEDICAL", "VENTURE", 
                    "HOMEIMPROVEMENT", "DEBTCONSOLIDATION"],
            help="Use one of the uppercase categories the model was trained on"
        )
        loan_percent_income = st.slider(
            "Loan as % of Income", min_value=0.0, max_value=1.5, value=0.3, step=0.05,
            help="Loan amount as a percentage of annual income (0-150%)"
        )
    
    submitted = st.form_submit_button("🔍 Get Prediction", use_container_width=True)

if submitted:
    # Prepare the request payload
    form_data = {
        "person_age": float(person_age),
        "person_gender": person_gender,
        "person_education": person_education,
        "person_income": float(person_income),
        "person_emp_exp": float(person_emp_exp),
        "person_home_ownership": person_home_ownership,
        "loan_amnt": float(loan_amnt),
        "loan_intent": loan_intent,
        "loan_int_rate": float(loan_int_rate),
        "loan_percent_income": float(loan_percent_income),
        "cb_person_cred_hist_length": float(cb_person_cred_hist_length),
        "credit_score": float(credit_score),
        "previous_loan_defaults_on_file": previous_loan_defaults_on_file,
    }
    
    try:
        with st.spinner("Analyzing application..."):
            response = requests.post(API_URL, json=form_data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                st.success("✅ Prediction Complete!")
                
                col_result1, col_result2 = st.columns(2)
                with col_result1:
                    status = "🔴 **DENIED**" if result["loan_status"] == 1 else "🟢 **APPROVED**"
                    st.markdown(f"### {status}")
                    st.caption("`loan_status = 1` means rejected, `loan_status = 0` means approved.")
                
                with col_result2:
                    prob = result.get("probability", 0)
                    if result["loan_status"] == 1:
                        st.metric("Default Risk", f"{prob*100:.1f}%")
                    else:
                        st.metric("Approval Confidence", f"{(1 - prob)*100:.1f}%")
                
                st.info(f"**Decision Threshold:** {result.get('threshold', 'N/A'):.4f}")
                st.write(f"**Decision:** {result.get('decision', 'N/A')}")
                
            else:
                st.error(f"❌ API Error: {response.status_code}")
                st.code(response.text)
                
    except requests.exceptions.ConnectionError:
        st.error(f"❌ Cannot connect to API at {API_URL}\n\nEnsure the API is running: `uvicorn api.main:app`")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
