import pytest
import pandas as pd
import numpy as np
from aegisxai.services.prediction_service import calculate_churn_probability, get_churn_reasons

def test_calculate_churn_probability_range():
    customer = {"tenure": 1, "Contract": "Month-to-month", "MonthlyCharges": 80, "TechSupport": "No"}
    prob = calculate_churn_probability(customer)
    assert 0 <= prob <= 1

def test_get_churn_reasons_returns_list():
    customer = {"tenure": 1, "Contract": "Month-to-month", "MonthlyCharges": 80,
                "TechSupport": "No", "OnlineSecurity": "No", "InternetService": "Fiber optic"}
    reasons = get_churn_reasons(customer)
    assert isinstance(reasons, list)
    assert len(reasons) > 0

def test_low_risk_customer():
    customer = {"tenure": 72, "Contract": "Two year", "MonthlyCharges": 30,
                "TechSupport": "Yes", "OnlineSecurity": "Yes", "InternetService": "DSL"}
    prob = calculate_churn_probability(customer)
    assert prob < 0.5
