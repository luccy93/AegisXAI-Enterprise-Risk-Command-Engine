import pytest
import pandas as pd
import numpy as np
from aegisxai.models.features import engineer_features, get_churn_rate

def test_engineer_features_creates_new_columns():
    df = pd.DataFrame({
        "customerID": ["C1"], "gender": ["Male"], "SeniorCitizen": [0], "Partner": ["No"],
        "Dependents": ["No"], "tenure": [12], "PhoneService": ["Yes"], "MultipleLines": ["No"],
        "InternetService": ["DSL"], "OnlineSecurity": ["No"], "OnlineBackup": ["No"],
        "DeviceProtection": ["No"], "TechSupport": ["No"], "StreamingTV": ["No"],
        "StreamingMovies": ["No"], "Contract": ["Month-to-month"], "PaperlessBilling": ["Yes"],
        "PaymentMethod": ["Electronic check"], "MonthlyCharges": [50.0], "TotalCharges": [600.0],
        "Churn": ["No"]
    })
    result = engineer_features(df)
    assert "tenure_group" in result.columns
    assert "service_count" in result.columns
    assert "is_month_to_month" in result.columns

def test_get_churn_rate():
    df = pd.DataFrame({"Churn": ["Yes", "No", "Yes", "No", "No"]})
    rate = get_churn_rate(df)
    assert rate == 40.0

def test_engineer_features_no_missing():
    df = pd.DataFrame({
        "customerID": ["C1"], "gender": ["Male"], "SeniorCitizen": [0], "Partner": ["No"],
        "Dependents": ["No"], "tenure": [12], "PhoneService": ["Yes"], "MultipleLines": ["No"],
        "InternetService": ["DSL"], "OnlineSecurity": ["No"], "OnlineBackup": ["No"],
        "DeviceProtection": ["No"], "TechSupport": ["No"], "StreamingTV": ["No"],
        "StreamingMovies": ["No"], "Contract": ["Month-to-month"], "PaperlessBilling": ["Yes"],
        "PaymentMethod": ["Electronic check"], "MonthlyCharges": [50.0], "TotalCharges": [600.0],
        "Churn": ["No"]
    })
    result = engineer_features(df)
    assert result.isnull().sum().sum() == 0
