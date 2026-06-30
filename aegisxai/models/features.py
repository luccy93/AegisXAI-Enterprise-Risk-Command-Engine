import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from ..config.settings import Settings


def load_data(csv_path=None):
    if csv_path is None:
        csv_path = Settings.CSV_PATH
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        from aegisxai.utils.bootstrap import ensure_dataset
        csv_path = ensure_dataset(csv_path)
        df = pd.read_csv(csv_path)
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df.dropna(inplace=True)
    return df


def engineer_features(df):
    df = df.copy()
    df["gender"] = df["gender"].map({"Female": 1, "Male": 0})
    df["Partner"] = df["Partner"].map({"Yes": 1, "No": 0})
    df["Dependents"] = df["Dependents"].map({"Yes": 1, "No": 0})
    df["PhoneService"] = df["PhoneService"].map({"Yes": 1, "No": 0})
    df["PaperlessBilling"] = df["PaperlessBilling"].map({"Yes": 1, "No": 0})
    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

    df["tenure_group"] = pd.cut(
        df["tenure"],
        bins=[0, 12, 24, 48, 60, 72],
        labels=["0-1yr", "1-2yr", "2-4yr", "4-5yr", "5-6yr"],
    )
    df["avg_monthly"] = df["TotalCharges"] / (df["tenure"] + 1)

    service_cols = [
        "PhoneService",
        "MultipleLines",
        "InternetService",
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies",
    ]
    df["service_count"] = 0
    for col in service_cols:
        if col in df.columns:
            df["service_count"] += (df[col] != "No").astype(int)

    df["has_online_security"] = (df["OnlineSecurity"] == "Yes").astype(int)
    df["has_tech_support"] = (df["TechSupport"] == "Yes").astype(int)
    df["is_month_to_month"] = (df["Contract"] == "Month-to-month").astype(int)
    df["is_electronic_check"] = (df["PaymentMethod"] == "Electronic check").astype(int)

    return df


def prepare_ml_data(df):
    df = engineer_features(df)
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    if "customerID" in cat_cols:
        cat_cols.remove("customerID")
    df = pd.get_dummies(df, columns=cat_cols, drop_first=True)

    feature_cols = [c for c in df.columns if c != "Churn" and c != "customerID"]
    X = df[feature_cols]
    y = df["Churn"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    return X_train, X_test, y_train, y_test, scaler, feature_cols


def get_churn_rate(df):
    if "Churn" not in df.columns:
        return 0.0
    return round(df["Churn"].value_counts(normalize=True).get("Yes", 0) * 100, 2)
