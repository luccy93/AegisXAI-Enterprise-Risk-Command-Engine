"""Shared fixtures for AegisXAI tests."""
import sys
import pytest
import pandas as pd
import numpy as np

sys.path.insert(0, ".")


@pytest.fixture(scope="session")
def sample_customer():
    return {
        "customerID": "TEST-0001",
        "gender": "Male",
        "SeniorCitizen": 0,
        "Partner": "No",
        "Dependents": "No",
        "tenure": 12,
        "PhoneService": "Yes",
        "MultipleLines": "No",
        "InternetService": "Fiber optic",
        "OnlineSecurity": "No",
        "OnlineBackup": "Yes",
        "DeviceProtection": "No",
        "TechSupport": "No",
        "StreamingTV": "Yes",
        "StreamingMovies": "Yes",
        "Contract": "Month-to-month",
        "PaperlessBilling": "Yes",
        "PaymentMethod": "Electronic check",
        "MonthlyCharges": 89.90,
        "TotalCharges": 1078.80,
    }


@pytest.fixture(scope="session")
def sample_df():
    np.random.seed(42)
    n = 200
    df = pd.DataFrame({
        "customerID": [f"TEST-{i:04d}" for i in range(n)],
        "gender": np.random.choice(["Male", "Female"], n),
        "SeniorCitizen": np.random.choice([0, 1], n, p=[0.8, 0.2]),
        "Partner": np.random.choice(["Yes", "No"], n),
        "Dependents": np.random.choice(["Yes", "No"], n, p=[0.3, 0.7]),
        "tenure": np.random.randint(1, 73, n),
        "PhoneService": np.random.choice(["Yes", "No"], n, p=[0.9, 0.1]),
        "MultipleLines": np.random.choice(["Yes", "No", "No phone service"], n, p=[0.42, 0.48, 0.1]),
        "InternetService": np.random.choice(["Fiber optic", "DSL", "No"], n, p=[0.44, 0.34, 0.22]),
        "OnlineSecurity": "No",
        "OnlineBackup": "No",
        "DeviceProtection": "No",
        "TechSupport": "No",
        "StreamingTV": "No",
        "StreamingMovies": "No",
        "Contract": np.random.choice(["Month-to-month", "One year", "Two year"], n, p=[0.55, 0.21, 0.24]),
        "PaperlessBilling": np.random.choice(["Yes", "No"], n),
        "PaymentMethod": np.random.choice(["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"], n),
        "MonthlyCharges": np.round(np.random.uniform(18, 119, n), 2),
        "TotalCharges": np.round(np.random.uniform(18, 8000, n), 2),
        "Churn": np.random.choice(["Yes", "No"], n, p=[0.27, 0.73]),
    })
    # Fix no-internet services
    mask = df["InternetService"] == "No"
    for c in ["OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies"]:
        df.loc[mask, c] = "No internet service"
    return df
