import numpy as np
from datetime import datetime, timedelta


def generate_anomaly_data(df=None, seed=42):
    rng = np.random.default_rng(seed)

    total_anomalies = 47
    anomaly_rate = 1.8

    severity_distribution = {"Critical": 8, "High": 15, "Medium": 24}

    by_type = {
        "Usage Drop": 18,
        "Support Spike": 12,
        "Payment Failure": 9,
        "Sentiment Crash": 5,
        "Login Anomaly": 3,
    }

    daily_trend = []
    base_date = datetime(2024, 6, 1)
    severities = ["Critical", "High", "Medium"]
    for d in range(30):
        date_str = (base_date + timedelta(days=d)).strftime("%Y-%m-%d")
        count = int(rng.integers(0, 5))
        sev = str(rng.choice(severities, size=1)[0])
        daily_trend.append({"date": date_str, "anomalies": count, "severity": sev})

    types_pool = ["Usage Drop", "Support Spike", "Payment Failure", "Sentiment Crash", "Login Anomaly"]
    severities_pool = ["Critical", "High", "Medium"]
    statuses = ["Investigating", "Resolved", "Escalated", "Dismissed"]
    recent_anomalies = []
    for i in range(15):
        cid = f"CUST_{rng.integers(10000, 99999)}"
        atype = str(rng.choice(types_pool))
        sev = str(rng.choice(severities_pool))
        score = round(rng.uniform(0.6, 0.99), 3)
        descs = {
            "Usage Drop": "Sudden drop in daily usage metrics",
            "Support Spike": "Unusual increase in support ticket volume",
            "Payment Failure": "Multiple consecutive payment failures detected",
            "Sentiment Crash": "Negative sentiment spike in customer feedback",
            "Login Anomaly": "Abnormal login pattern detected from new location",
        }
        ts = datetime(2024, 6, rng.integers(1, 30), rng.integers(0, 23), rng.integers(0, 59))
        recent_anomalies.append({
            "customer_id": cid,
            "type": atype,
            "severity": sev,
            "score": score,
            "description": descs.get(atype, "Anomalous behavior detected"),
            "detected_at": ts.strftime("%Y-%m-%d %H:%M:%S"),
            "status": str(rng.choice(statuses)),
        })

    return {
        "total_anomalies": total_anomalies,
        "anomaly_rate": anomaly_rate,
        "severity_distribution": severity_distribution,
        "by_type": by_type,
        "daily_trend": daily_trend,
        "recent_anomalies": recent_anomalies,
    }


def detect_anomalies(customer_data):
    score = 0.0
    reasons = []

    monthly = customer_data.get("monthly_charges", 0)
    tenure = customer_data.get("tenure", 0)
    support_tickets = customer_data.get("support_tickets", 0)
    payment_failures = customer_data.get("payment_failures", 0)
    sentiment = customer_data.get("sentiment_score", 0.5)
    login_attempts = customer_data.get("login_attempts", 1)

    threshold_monthly = customer_data.get("avg_monthly_charges", monthly) * 1.5
    if monthly > threshold_monthly and threshold_monthly > 0:
        score += 0.25
        reasons.append("Usage Drop")

    if support_tickets > 5:
        score += 0.20
        reasons.append("Support Spike")

    if payment_failures > 2:
        score += 0.30
        reasons.append("Payment Failure")

    if sentiment < 0.3:
        score += 0.20
        reasons.append("Sentiment Crash")

    if login_attempts > 10:
        score += 0.15
        reasons.append("Login Anomaly")

    score = min(score, 1.0)

    is_anomaly = score >= 0.4

    if score >= 0.7:
        severity = "Critical"
    elif score >= 0.5:
        severity = "High"
    elif score >= 0.4:
        severity = "Medium"
    else:
        severity = "None"

    anomaly_type = reasons[0] if reasons else "None"

    return {
        "is_anomaly": is_anomaly,
        "anomaly_score": round(score, 3),
        "anomaly_type": anomaly_type,
        "severity": severity,
    }


def get_anomaly_alerts():
    rng = np.random.default_rng(42)
    types = ["Usage Drop", "Support Spike", "Payment Failure", "Sentiment Crash", "Login Anomaly"]
    severities = ["Critical", "High", "Medium"]
    alerts = []
    for i in range(8):
        cid = f"CUST_{rng.integers(10000, 99999)}"
        atype = str(rng.choice(types))
        sev = str(rng.choice(severities))
        ts = datetime(2024, 6, rng.integers(1, 30), rng.integers(0, 23), rng.integers(0, 59))
        alerts.append({
            "alert_id": f"ALT-{rng.integers(1000, 9999)}",
            "customer_id": cid,
            "type": atype,
            "severity": sev,
            "message": f"{atype} detected for customer {cid}",
            "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "Open",
        })
    return alerts
