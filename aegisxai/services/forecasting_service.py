"""
Predictive Business Forecasting - Prophet, LSTM, XGBoost forecasting engine
Simulates forecast models with confidence intervals
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def forecast_churn(days=90, model="prophet"):
    today = datetime.now()
    dates = [today + timedelta(days=i) for i in range(days)]
    base = 26.5
    np.random.seed(42)
    if model == "prophet":
        trend = np.cumsum(np.random.normal(0.02, 0.03, days))
        seasonal = 2 * np.sin(2 * np.pi * np.arange(days) / 30)
        noise = np.random.normal(0, 0.5, days)
        values = base + trend + seasonal + noise
    elif model == "lstm":
        values = base + np.cumsum(np.random.normal(0.01, 0.05, days)) + np.random.normal(0, 0.3, days)
    else:
        values = base + np.cumsum(np.random.normal(0.01, 0.02, days)) + np.random.normal(0, 0.4, days)
    values = np.maximum(values, 10)
    lower = values - np.random.uniform(1, 3, days)
    upper = values + np.random.uniform(1, 3, days)
    return pd.DataFrame({
        "Date": dates, "Forecast": values, "Lower CI": lower, "Upper CI": upper,
        "Model": model.upper()
    })

def forecast_revenue(days=90):
    today = datetime.now()
    dates = [today + timedelta(days=i) for i in range(days)]
    base = 456000
    np.random.seed(42)
    trend = np.cumsum(np.random.normal(-500, 200, days))
    seasonal = 15000 * np.sin(2 * np.pi * np.arange(days) / 30)
    noise = np.random.normal(0, 3000, days)
    values = base + trend + seasonal + noise
    values = np.maximum(values, 300000)
    lower = values - np.random.uniform(10000, 30000, days)
    upper = values + np.random.uniform(10000, 30000, days)
    return pd.DataFrame({
        "Date": dates, "Forecast": values, "Lower CI": lower, "Upper CI": upper
    })

def forecast_satisfaction(days=90):
    today = datetime.now()
    dates = [today + timedelta(days=i) for i in range(days)]
    base = 4.2
    np.random.seed(42)
    values = base + np.cumsum(np.random.normal(-0.005, 0.02, days)) + 0.1 * np.sin(2 * np.pi * np.arange(days) / 30)
    values = np.clip(values, 2.5, 5.0)
    lower = values - np.random.uniform(0.1, 0.4, days)
    upper = values + np.random.uniform(0.1, 0.4, days)
    return pd.DataFrame({
        "Date": dates, "Forecast": values, "Lower CI": lower, "Upper CI": upper
    })

def forecast_nps(days=90):
    today = datetime.now()
    dates = [today + timedelta(days=i) for i in range(days)]
    base = 46
    np.random.seed(42)
    values = base + np.cumsum(np.random.normal(-0.2, 0.5, days)) + 3 * np.sin(2 * np.pi * np.arange(days) / 30)
    values = np.clip(values, -50, 100)
    lower = values - np.random.uniform(5, 12, days)
    upper = values + np.random.uniform(5, 12, days)
    return pd.DataFrame({
        "Date": dates, "Forecast": values, "Lower CI": lower, "Upper CI": upper
    })

def forecast_acquisition(days=90):
    today = datetime.now()
    dates = [today + timedelta(days=i) for i in range(days)]
    base = 85
    np.random.seed(42)
    values = base + np.cumsum(np.random.normal(0.1, 0.8, days)) + 10 * np.sin(2 * np.pi * np.arange(days) / 30)
    values = np.maximum(values, 20)
    lower = values - np.random.uniform(8, 15, days)
    upper = values + np.random.uniform(8, 15, days)
    return pd.DataFrame({
        "Date": dates, "Forecast": values, "Lower CI": lower, "Upper CI": upper
    })

FORECAST_FUNCTIONS = {
    "Churn Rate": forecast_churn,
    "Monthly Revenue": forecast_revenue,
    "Customer Satisfaction": forecast_satisfaction,
    "NPS Score": forecast_nps,
    "New Customers Needed": forecast_acquisition,
}
