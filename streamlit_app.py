import streamlit as st
import pandas as pd
import joblib
import os
import sys
from datetime import datetime

# Fix path to import generate_report.py from parent folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from generate_report import generate_pdf_report

st.set_page_config(page_title="Loan Default Risk App", layout="centered")

st.title("🏦 Loan Default Risk Prediction App")
st.markdown("Enter applicant information to predict the default risk.")

# Load model
model_path = "model/loan_default_model.pkl"
if os.path.exists(model_path)
    model = joblib.load(model_path)
else:
    st.error("Model file not found. Please train the model and save it to 'model/loan_default_model.pkl'")
    st.stop()

# Input fields
age = st.slider("Age", 18, 75, 30)
income = st.number_input("Annual Income (in ₹)", min_value=10000, step=1000)
loan_amount = st.number_input("Loan Amount (in ₹)", min_value=1000, step=500)
credit_score = st.slider("Credit Score", 300, 900, 650)
loan_term = st.number_input("Loan Term (in months)", min_value=6, max_value=360, step=6)

if st.button("🔍 Predict Default Risk"):
    input_data = pd.DataFrame([{
        'Age': age,
        'AnnualIncome': income,
        'LoanAmount': loan_amount,
        'CreditScore': credit_score,
        'LoanTerm': loan_term
    }])

    prediction = model.predict(input_data)[0]
    risk = "🔴 High Risk of Default" if prediction == 1 else "🟢 Low Risk of Default"
    
    st.subheader("Prediction Result:")
    st.info(risk)

    # PDF Report Button
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reports/loan_risk_report_{timestamp}.pdf"
    generate_pdf_report(input_data, prediction, filename)

    with open(filename, "rb") as f:
        st.download_button("📄 Download PDF Report", f, file_name=os.path.basename(filename), mime="application/pdf")
