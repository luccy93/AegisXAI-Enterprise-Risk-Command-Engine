"""Bootstrap utilities for first-run dataset generation on Streamlit Cloud."""
import os
import numpy as np
import pandas as pd


def ensure_dataset(csv_path):
    """Generate a synthetic dataset if the CSV doesn't exist."""
    if os.path.exists(csv_path):
        return csv_path

    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    n = 50_000  # smaller for cloud cold-start speed; full 500K can be regenerated
    np.random.seed(42)

    df = pd.DataFrame({"customerID": [f"CUS-{100000 + i:06d}" for i in range(n)]})
    df["gender"] = np.random.choice(["Male", "Female"], n, p=[0.505, 0.495])
    df["SeniorCitizen"] = np.random.choice([0, 1], n, p=[0.838, 0.162])
    df["Partner"] = np.random.choice(["Yes", "No"], n, p=[0.483, 0.517])
    df["Dependents"] = np.random.choice(["Yes", "No"], n, p=[0.300, 0.700])
    df["tenure"] = np.clip(np.random.exponential(scale=32, size=n).astype(int), 0, 72)
    df["PhoneService"] = np.random.choice(["Yes", "No"], n, p=[0.903, 0.097])
    mask_no_phone = df["PhoneService"] == "No"
    df["MultipleLines"] = np.random.choice(["Yes", "No"], n, p=[0.47, 0.53])
    df.loc[mask_no_phone, "MultipleLines"] = "No phone service"
    df["InternetService"] = np.random.choice(["Fiber optic", "DSL", "No"], n, p=[0.440, 0.344, 0.216])
    mask_no_inet = df["InternetService"] == "No"
    for col, yes_p in [("OnlineSecurity", 0.37), ("OnlineBackup", 0.44), ("DeviceProtection", 0.44),
                        ("TechSupport", 0.37), ("StreamingTV", 0.49), ("StreamingMovies", 0.49)]:
        df[col] = np.random.choice(["Yes", "No"], n, p=[yes_p, 1 - yes_p])
        df.loc[mask_no_inet, col] = "No internet service"
    df["Contract"] = np.random.choice(["Month-to-month", "One year", "Two year"], n, p=[0.550, 0.209, 0.241])
    df["PaperlessBilling"] = np.random.choice(["Yes", "No"], n, p=[0.592, 0.408])
    df["PaymentMethod"] = np.random.choice(
        ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"],
        n, p=[0.336, 0.229, 0.219, 0.216])
    r = np.random.normal(65, 30, n)
    r += np.select([df["InternetService"] == "Fiber optic", df["InternetService"] == "DSL"], [20, 5], default=-10)
    r -= np.select([df["Contract"] == "Two year", df["Contract"] == "One year"], [5, 2], default=0)
    r += df["tenure"] * 0.3
    df["MonthlyCharges"] = np.round(np.clip(r, 18.25, 118.75), 2)
    df["TotalCharges"] = np.round(df["MonthlyCharges"] * df["tenure"].clip(lower=1), 2)
    p = np.full(n, 0.265)
    p += np.where(df["Contract"] == "Month-to-month", 0.20, np.where(df["Contract"] == "Two year", -0.15, 0))
    p += np.where(df["tenure"] < 12, 0.10, np.where(df["tenure"] > 48, -0.08, 0))
    p += np.where(df["InternetService"] == "Fiber optic", 0.05, 0)
    p += np.where(df["TechSupport"] == "No", 0.06, 0)
    p += np.where(df["OnlineSecurity"] == "No", 0.05, 0)
    p += np.where(df["PaymentMethod"] == "Electronic check", 0.08, 0)
    p = np.clip(p, 0.02, 0.95)
    df["Churn"] = np.where(np.random.random(n) < p, "Yes", "No")
    df.to_csv(csv_path, index=False)
    return csv_path
