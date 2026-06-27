"""Data profiling, validation, and quality reporting utilities."""
import pandas as pd
import numpy as np
from datetime import datetime


def profile_dataframe(df, name="Dataset"):
    """Generate a comprehensive profile of a pandas DataFrame."""
    profile = {
        "name": name,
        "timestamp": datetime.now().isoformat(),
        "rows": len(df),
        "columns": len(df.columns),
        "memory_mb": round(df.memory_usage(deep=True).sum() / 1e6, 2),
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_cells": int(df.isnull().sum().sum()),
        "missing_pct": round(df.isnull().sum().sum() / (df.size) * 100, 2) if df.size else 0,
        "column_profiles": {},
    }
    for col in df.columns:
        col_profile = {
            "dtype": str(df[col].dtype),
            "missing": int(df[col].isnull().sum()),
            "missing_pct": round(df[col].isnull().mean() * 100, 2),
            "unique": int(df[col].nunique()),
        }
        if df[col].dtype in ("int64", "float64"):
            col_profile.update({
                "min": float(df[col].min()) if df[col].count() else None,
                "max": float(df[col].max()) if df[col].count() else None,
                "mean": float(df[col].mean()) if df[col].count() else None,
                "std": float(df[col].std()) if df[col].count() else None,
                "zeros": int((df[col] == 0).sum()),
            })
        elif df[col].dtype == "object":
            top_values = df[col].value_counts().head(5)
            col_profile["top_values"] = {
                str(k): int(v) for k, v in top_values.items()
            }
        profile["column_profiles"][col] = col_profile
    return profile


def validate_churn_data(df):
    """Validate the churn dataset for common issues."""
    issues = []
    required_cols = ["customerID", "Churn", "tenure", "MonthlyCharges", "Contract"]
    for c in required_cols:
        if c not in df.columns:
            issues.append(f"Missing required column: {c}")

    if "Churn" in df.columns:
        valid = {"Yes", "No"}
        actual = set(df["Churn"].dropna().unique())
        if not actual.issubset(valid):
            issues.append(f"Churn column has invalid values: {actual - valid}")
        churn_rate = df["Churn"].value_counts(normalize=True).get("Yes", 0)
        if churn_rate < 0.05 or churn_rate > 0.95:
            issues.append(f"Unusual churn rate: {churn_rate:.1%}")

    if "tenure" in df.columns:
        if df["tenure"].min() < 0:
            issues.append("Negative tenure values found")
        if df["tenure"].max() > 100:
            issues.append(f"Tenure > 100 months: max={df['tenure'].max()}")

    if "MonthlyCharges" in df.columns:
        if df["MonthlyCharges"].min() <= 0:
            issues.append("Non-positive MonthlyCharges found")

    if "customerID" in df.columns:
        if df["customerID"].duplicated().any():
            issues.append("Duplicate customerID values found")

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "score": max(0, 100 - len(issues) * 15),
        "row_count": len(df),
    }


def segment_summary(df, segment_col="Contract", metric_col="MonthlyCharges"):
    """Generate summary statistics by segment."""
    if segment_col not in df or metric_col not in df:
        return {}
    summary = df.groupby(segment_col).agg(
        count=("customerID", "count"),
        avg_metric=(metric_col, "mean"),
        churn_rate=("Churn", lambda x: (x == "Yes").mean()),
    ).reset_index()
    summary.columns = [segment_col, "count", f"avg_{metric_col}", "churn_rate"]
    summary["pct"] = summary["count"] / summary["count"].sum() * 100
    return summary.sort_values("count", ascending=False).to_dict("records")


def correlation_report(df):
    """Generate a correlation report for numeric columns."""
    numeric = df.select_dtypes(include=[np.number])
    if numeric.empty:
        return {}
    corr = numeric.corr()
    pairs = []
    for i in range(len(corr.columns)):
        for j in range(i + 1, len(corr.columns)):
            pairs.append({
                "col1": corr.columns[i],
                "col2": corr.columns[j],
                "correlation": round(corr.iloc[i, j], 4),
            })
    pairs.sort(key=lambda x: abs(x["correlation"]), reverse=True)
    return {"matrix": corr.to_dict(), "top_pairs": pairs[:10]}
