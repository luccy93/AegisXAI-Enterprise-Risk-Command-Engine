import numpy as np
import pandas as pd


def generate_csat_data(df=None, seed=42):
    rng = np.random.default_rng(seed)
    if df is None:
        n = 1000
        df = pd.DataFrame({
            "customer_id": range(1, n + 1),
            "csat_score": rng.integers(1, 6, size=n).clip(1, 5),
            "department": rng.choice(["Support", "Billing", "Network", "Sales"], size=n),
            "region": rng.choice(["NA", "EMEA", "APAC", "LATAM"], size=n, p=[0.35, 0.25, 0.25, 0.15]),
            "satisfaction_date": pd.date_range(end="2025-11-30", periods=n, freq="D")
        })

    scores = df["csat_score"]
    overall = float(round(scores.mean(), 1))
    good = int(((scores >= 4) & (scores <= 5)).sum())
    excellent = int((scores == 5).sum())
    poor = int((scores <= 2).sum())

    dept_scores = df.groupby("department")["csat_score"].mean().round(1).to_dict()
    reg_scores = df.groupby("region")["csat_score"].mean().round(1).to_dict()

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    base = 4.2
    monthly_trend = []
    for i, m in enumerate(months):
        noise = rng.normal(0, 0.08)
        monthly_trend.append({"month": m, "score": round(min(5.0, max(1.0, base + noise)), 2)})

    return {
        "overall_score": overall,
        "excellent_pct": round(excellent / len(df) * 100, 1),
        "good_pct": round(good / len(df) * 100, 1),
        "poor_pct": round(poor / len(df) * 100, 1),
        "department_scores": dept_scores,
        "region_scores": reg_scores,
        "monthly_trend": monthly_trend,
        "distribution": [excellent, good, poor]
    }


def generate_nps_data(df=None, seed=42):
    rng = np.random.default_rng(seed)
    if df is None:
        n = 1000
        df = pd.DataFrame({
            "customer_id": range(1, n + 1),
            "nps_score": rng.integers(0, 11, size=n),
            "contract": rng.choice(["Month-to-month", "One year", "Two year"], size=n, p=[0.45, 0.35, 0.20]),
            "region": rng.choice(["NA", "EMEA", "APAC", "LATAM"], size=n, p=[0.30, 0.28, 0.24, 0.18])
        })

    promoters = (df["nps_score"] >= 9).sum()
    passives = ((df["nps_score"] >= 7) & (df["nps_score"] <= 8)).sum()
    detractors = (df["nps_score"] <= 6).sum()
    total = len(df)
    nps = int(round((promoters - detractors) / total * 100))

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly_trend = []
    base_nps = {"promoters": 62, "passives": 22, "detractors": 16}
    for m in months:
        p = max(0, base_nps["promoters"] + int(rng.normal(0, 3)))
        d = max(0, base_nps["detractors"] + int(rng.normal(0, 2)))
        pa = max(0, 100 - p - d)
        monthly_trend.append({"month": m, "promoters": p, "passives": pa, "detractors": d})

    segment_nps = {}
    for contract in df["contract"].unique():
        sub = df[df["contract"] == contract]
        p = (sub["nps_score"] >= 9).sum()
        d = (sub["nps_score"] <= 6).sum()
        segment_nps[contract] = int(round((p - d) / len(sub) * 100))

    region_nps = {}
    for region in df["region"].unique():
        sub = df[df["region"] == region]
        p = (sub["nps_score"] >= 9).sum()
        d = (sub["nps_score"] <= 6).sum()
        region_nps[region] = int(round((p - d) / len(sub) * 100))

    return {
        "promoters_pct": round(promoters / total * 100, 1),
        "passives_pct": round(passives / total * 100, 1),
        "detractors_pct": round(detractors / total * 100, 1),
        "overall_nps": nps,
        "monthly_trend": monthly_trend,
        "segment_nps": segment_nps,
        "region_nps": region_nps
    }


def calculate_happiness_index(df=None, seed=42):
    rng = np.random.default_rng(seed)
    if df is None:
        df = pd.DataFrame({
            "customer_id": range(1, 1001),
            "csat_score": rng.integers(1, 6, size=1000),
            "nps_score": rng.integers(0, 11, size=1000),
            "sentiment_score": rng.uniform(0, 100, size=1000),
            "usage_score": rng.uniform(0, 100, size=1000),
            "resolution_score": rng.uniform(0, 100, size=1000),
            "loyalty_score": rng.uniform(0, 100, size=1000),
            "engagement_score": rng.uniform(0, 100, size=1000)
        })

    components = {
        "csat_score": round(float(df["csat_score"].mean() * 20), 1),
        "nps_score": round(float((df["nps_score"].mean() / 10) * 100), 1),
        "sentiment_score": round(float(df["sentiment_score"].mean()), 1),
        "usage_score": round(float(df["usage_score"].mean()), 1),
        "resolution_score": round(float(df["resolution_score"].mean()), 1),
        "loyalty_score": round(float(df["loyalty_score"].mean()), 1),
        "engagement_score": round(float(df["engagement_score"].mean()), 1),
    }
    overall = int(round(sum(components.values()) / len(components)))
    overall = max(0, min(100, overall))

    if overall >= 85:
        category = "Excellent"
    elif overall >= 70:
        category = "Good"
    elif overall >= 50:
        category = "Neutral"
    elif overall >= 30:
        category = "At Risk"
    else:
        category = "Critical"

    dist = [23, 31, 22, 16, 8]
    return {
        "overall_happiness": overall,
        "score_category": category,
        "components": components,
        "distribution": dist
    }
