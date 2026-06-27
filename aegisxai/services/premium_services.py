"""
Premium Enterprise Dashboard Services
Data generation for all 22 premium dashboards and widgets
"""
import numpy as np
import pandas as pd
import networkx as nx
from datetime import datetime, timedelta
from collections import Counter

def get_executive_kpis():
    return {
        "total_customers": 7043,
        "active_customers": 5174,
        "high_risk": 847,
        "churn_rate": 26.5,
        "revenue_at_risk": 456000,
        "clv_avg": 1850,
        "retention_rate": 73.5,
        "csat": 4.2,
        "nps": 46,
        "happiness_index": 74,
        "monthly_revenue": 1652000,
        "upsell_potential": 890000,
        "cross_sell_potential": 420000,
    }

def get_kpi_sparklines(days=90):
    today = datetime.now()
    dates = [today - timedelta(days=i) for i in range(days)]
    kpi_trends = {}
    for kpi in ["churn_rate", "revenue", "csat", "nps", "retention", "happiness"]:
        np.random.seed(hash(kpi) % (2**31))
        base = {"churn_rate": 26.5, "revenue": 456000, "csat": 4.2, "nps": 46, "retention": 73.5, "happiness": 74}[kpi]
        noise = np.random.normal(0, base * 0.02, days)
        trend = np.cumsum(np.random.normal(0, 0.1, days)) * (base * 0.01)
        values = np.maximum(base + noise + trend, base * 0.5)
        kpi_trends[kpi] = pd.DataFrame({"date": dates, "value": values})
    return kpi_trends

def get_ai_status():
    return {
        "status": "ONLINE", "model_version": "XGBoost_v3.2.1",
        "inference_latency_ms": 14, "predictions_per_minute": 14200,
        "model_confidence": 98.6, "drift_status": "Stable",
        "uptime_hours": 876, "total_predictions": 12450000,
        "queue_depth": 342, "queue_status": "Normal",
        "last_trained": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
        "gpu_util": 67, "memory_util": 72, "cpu_util": 45,
    }

def get_regional_risk():
    regions = {
        "North America": {"lat": 40.7, "lon": -100, "customers": 2500, "churn": 22.4, "csat": 4.3, "revenue": 1850000, "risk": "Low", "code": "USA"},
        "Europe": {"lat": 50.0, "lon": 10.0, "customers": 1800, "churn": 24.1, "csat": 4.1, "revenue": 1320000, "risk": "Medium", "code": "EU"},
        "APAC": {"lat": 25.0, "lon": 115.0, "customers": 1200, "churn": 31.5, "csat": 3.8, "revenue": 890000, "risk": "High", "code": "APAC"},
        "LATAM": {"lat": -15.0, "lon": -60.0, "customers": 800, "churn": 28.3, "csat": 3.9, "revenue": 520000, "risk": "High", "code": "LATAM"},
        "MEA": {"lat": 25.0, "lon": 45.0, "customers": 743, "churn": 19.8, "csat": 4.4, "revenue": 480000, "risk": "Low", "code": "MEA"},
    }
    return pd.DataFrame(regions).T.reset_index().rename(columns={"index": "region"})

def get_segment_data():
    segments = ["Champions", "Loyal Customers", "Potential Loyalists", "At Risk", "Dormant", "Lost Customers"]
    counts = [852, 1431, 965, 1142, 432, 653]
    colors = ["#10B981", "#34D399", "#06B6D4", "#F59E0B", "#8B5CF6", "#EF4444"]
    churn = [3.2, 7.8, 18.5, 42.3, 65.1, 94.7]
    clv = [4200, 2800, 1850, 980, 420, 0]
    return pd.DataFrame({"segment": segments, "count": counts, "color": colors, "churn_rate": churn, "avg_clv": clv})

def get_journey_funnel():
    stages = ["Acquisition", "Onboarding", "Engagement", "Support", "Renewal", "Retention"]
    counts = [7043, 6230, 4890, 3540, 2810, 1869]
    dropoff = [0, 813, 1340, 1350, 730, 941]
    return pd.DataFrame({"stage": stages, "count": counts, "dropoff": dropoff})

def get_voice_of_customer():
    complaints = {
        "Billing Issues": np.random.randint(200, 500),
        "Network Reliability": np.random.randint(150, 400),
        "Customer Service": np.random.randint(180, 350),
        "Pricing": np.random.randint(250, 450),
        "Contract Terms": np.random.randint(100, 300),
        "Speed/Performance": np.random.randint(120, 380),
        "Technical Support": np.random.randint(160, 320),
        "Bundling Options": np.random.randint(80, 200),
    }
    praises = {
        "Easy Setup": np.random.randint(200, 500),
        "User Interface": np.random.randint(150, 350),
        "Customer Support": np.random.randint(180, 400),
        "Reliability": np.random.randint(120, 300),
        "Value for Money": np.random.randint(100, 250),
        "Self-Service Portal": np.random.randint(80, 200),
    }
    topics = {
        "Support Experience": 0.28, "Billing & Payments": 0.22,
        "Technical Issues": 0.18, "Account Management": 0.15,
        "Product Features": 0.12, "Other": 0.05,
    }
    return {"complaints": complaints, "praises": praises, "topics": topics}

def get_word_cloud_data():
    words = ["billing", "support", "internet", "price", "contract", "speed", "service",
             "cancel", "slow", "expensive", "help", "downgrade", "refund", "complaint",
             "disconnect", "frustrated", "hidden fees", "long wait", "unreliable",
             "great", "easy", "fast", "reliable", "helpful", "satisfied", "recommend",
             "excellent", "smooth", "responsive", "clear", "fair", "simple"]
    return [(w, np.random.randint(20, 500)) for w in words]

def get_incident_data():
    incidents = []
    for i in range(20):
        incidents.append({
            "id": f"INC-{5000+i}", "title": np.random.choice(["Network Outage", "Billing Error", "Login Failure",
                "Payment Decline", "System Latency", "Security Alert", "Data Sync Failure", "API Timeout"]),
            "severity": np.random.choice(["Critical", "High", "Medium", "Low"], p=[0.15, 0.25, 0.35, 0.25]),
            "status": np.random.choice(["Open", "In Progress", "Resolved", "Closed", "Escalated"], p=[0.2, 0.25, 0.3, 0.15, 0.1]),
            "owner": f"Agent-{np.random.randint(1, 30)}",
            "created": (datetime.now() - timedelta(hours=np.random.randint(1, 168))).strftime("%Y-%m-%d %H:%M"),
            "sla_remaining": np.random.randint(-2, 48),
        })
    return pd.DataFrame(incidents)

def get_alerts():
    alerts = []
    for severity, count in [("Critical", 3), ("High", 7), ("Medium", 12), ("Low", 18)]:
        for i in range(count):
            alerts.append({
                "id": f"ALT-{9000+i}", "severity": severity, "title": np.random.choice(
                    ["Churn risk spike detected", "Revenue drop in APAC", "Model drift warning",
                     "SLA breach imminent", "Customer satisfaction decline", "System health degraded",
                     "Support ticket surge", "Payment failure cluster"]),
                "assigned": np.random.choice(["Unassigned", f"Agent-{np.random.randint(1,20)}"]),
                "status": np.random.choice(["New", "Acknowledged", "Investigating", "Resolved"], p=[0.3, 0.25, 0.25, 0.2]),
                "created": (datetime.now() - timedelta(minutes=np.random.randint(5, 1440))).strftime("%Y-%m-%d %H:%M"),
                "sla": np.random.choice(["Within SLA", "At Risk", "Breached"], p=[0.6, 0.25, 0.15]),
            })
    return pd.DataFrame(alerts)

def get_live_events(n=30):
    events = []
    types = ["Network Failure", "App Crash", "Payment Issue", "Login Failure", "Sentiment Spike", "Data Sync"]
    for i in range(n):
        events.append({
            "id": f"EVT-{8000+i}", "type": np.random.choice(types),
            "severity": np.random.choice(["Critical", "High", "Medium", "Info"]),
            "message": f"{np.random.choice(types)} detected in {np.random.choice(['APAC', 'NA', 'EU', 'LATAM'])}",
            "timestamp": (datetime.now() - timedelta(seconds=np.random.randint(0, 300))).strftime("%H:%M:%S"),
            "status": np.random.choice(["Active", "Investigating", "Resolved"], p=[0.5, 0.3, 0.2]),
        })
    return pd.DataFrame(events)

def get_model_metrics():
    return {
        "accuracy": 0.796, "precision": 0.782, "recall": 0.641, "f1": 0.704,
        "roc_auc": 0.847, "pr_auc": 0.712, "log_loss": 0.482,
        "confusion_matrix": np.array([[982, 108], [154, 278]]),
        "fpr": np.linspace(0, 1, 20), "tpr": np.cumsum(np.random.uniform(0.02, 0.08, 20)).clip(0, 1),
        "precision_curve": np.linspace(0.8, 0.5, 20), "recall_curve": np.linspace(0.2, 0.9, 20),
    }

def get_drift_data():
    features = ["Contract", "Tenure", "MonthlyCharges", "InternetService", "TechSupport",
                "OnlineSecurity", "PaymentMethod", "TotalCharges", "Gender", "SeniorCitizen"]
    drift_scores = np.random.uniform(0, 0.3, len(features))
    statuses = ["Stable" if d < 0.1 else "Warning" if d < 0.2 else "Critical" for d in drift_scores]
    return pd.DataFrame({"feature": features, "drift_score": drift_scores, "status": statuses})

def get_customer_360(customer_id="C1001"):
    return {
        "id": customer_id, "name": f"Customer {customer_id}", "gender": np.random.choice(["Male", "Female"]),
        "age": np.random.randint(25, 75), "tenure_months": np.random.randint(1, 72),
        "contract": np.random.choice(["Month-to-month", "One year", "Two year"]),
        "monthly_charges": round(np.random.uniform(30, 120), 2),
        "total_charges": round(np.random.uniform(500, 8000), 2),
        "internet_service": np.random.choice(["Fiber optic", "DSL", "No"]),
        "tech_support": np.random.choice(["Yes", "No"]),
        "payment_method": np.random.choice(["Electronic check", "Mailed check", "Bank transfer", "Credit card"]),
        "churn_risk": round(np.random.uniform(0, 1), 2),
        "csat": round(np.random.uniform(1, 5), 1),
        "nps": np.random.randint(-50, 100),
        "sentiment": np.random.choice(["Positive", "Neutral", "Negative"]),
        "loyalty_tier": np.random.choice(["Bronze", "Silver", "Gold", "Platinum"]),
        "engagement_score": round(np.random.uniform(20, 100), 0),
        "lifetime_value": round(np.random.uniform(500, 5000), 0),
        "service_count": np.random.randint(1, 7),
        "tickets_30d": np.random.randint(0, 10),
    }

def get_team_perf_premium():
    teams = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta"]
    data = []
    for t in teams:
        agents = np.random.randint(5, 20)
        data.append({
            "team": t, "agents": agents,
            "resolution_time": round(np.random.uniform(8, 45), 1),
            "quality": round(np.random.uniform(72, 98), 1),
            "rating": round(np.random.uniform(3.5, 5.0), 1),
            "resolved": np.random.randint(100, 500),
            "satisfaction": round(np.random.uniform(75, 98), 1),
            "tickets_per_agent": round(np.random.uniform(10, 40), 0),
            "escalation_rate": round(np.random.uniform(2, 15), 1),
        })
    return pd.DataFrame(data)

def get_campaigns():
    campaigns = [
        {"name": "Loyalty Rewards", "type": "Loyalty", "reach": 2500, "conversions": 425, "roi": 2.4, "retention_improvement": 8.2},
        {"name": "Summer Discount", "type": "Discount", "reach": 3500, "conversions": 612, "roi": 3.1, "retention_improvement": 6.7},
        {"name": "VIP Support Plus", "type": "VIP Support", "reach": 800, "conversions": 342, "roi": 4.8, "retention_improvement": 12.5},
        {"name": "Fiber Upgrade", "type": "Upgrade", "reach": 1200, "conversions": 287, "roi": 5.2, "retention_improvement": 15.3},
    ]
    return pd.DataFrame(campaigns)

def get_security_data():
    return {
        "login_attempts_24h": np.random.randint(500, 5000),
        "failed_logins": np.random.randint(10, 200),
        "mfa_enabled": 96.5,
        "active_users": np.random.randint(50, 200),
        "audit_entries": np.random.randint(1000, 10000),
        "model_fairness": 0.88,
        "gdpr_compliance": 94.2,
        "soc2_status": "Compliant",
        "iso27001_status": "Certified",
        "data_breaches_30d": 0,
        "consent_rate": 87.3,
        "privacy_requests": np.random.randint(5, 50),
    }

def get_shap_waterfall(customer_idx=0):
    features = ["Contract_M2M", "Tenure", "MonthlyCharges", "InternetService_Fiber",
                "TechSupport_No", "OnlineSecurity_No", "PaymentMethod_Electronic",
                "TotalCharges", "ServiceCount", "PaperlessBilling"]
    base_value = 0.265
    shap_values = np.random.uniform(-0.15, 0.15, len(features))
    shap_values[np.argmax(np.abs(shap_values))] = 0.18
    shap_values[np.argmin(np.abs(shap_values))] = -0.12
    final_value = base_value + sum(shap_values)
    fv = [float(base_value)]
    for s in shap_values:
        fv.append(fv[-1] + float(s))
    return {"features": features, "shap_values": [float(s) for s in shap_values],
            "base_value": float(base_value), "final_value": float(final_value),
            "cumulative": fv}

def get_sankey_data():
    sources = ["Acquisition", "Acquisition", "Onboarding", "Onboarding", "Engagement",
               "Engagement", "Support", "Support", "Renewal", "Renewal"]
    targets = ["Onboarding", "Drop-Off", "Engagement", "Drop-Off", "Support",
               "Drop-Off", "Renewal", "Drop-Off", "Retention", "Churn"]
    values = [6230, 813, 4890, 1340, 3540, 1350, 2810, 730, 1869, 941]
    return {"source": sources, "target": targets, "value": values}

def get_scenario_simulation():
    levers = {
        "Support Tickets": {"current": 8, "min": 0, "max": 20, "unit": "tickets"},
        "Discount Level": {"current": 10, "min": 0, "max": 40, "unit": "%"},
        "Sentiment Score": {"current": 74, "min": 0, "max": 100, "unit": ""},
        "App Crashes": {"current": 5, "min": 0, "max": 20, "unit": "/day"},
        "Tech Support Adoption": {"current": 45, "min": 0, "max": 100, "unit": "%"},
        "CSAT Target": {"current": 4.2, "min": 1, "max": 5, "unit": ""},
    }
    return levers

def calculate_scenario_impact(levers, values):
    base_churn = 26.5
    impact = 0
    details = {}
    if "Support Tickets" in levers:
        diff = levers["Support Tickets"]["current"] - values.get("Support Tickets", levers["Support Tickets"]["current"])
        t_impact = diff * 0.8
        impact += t_impact
        details["Support Tickets"] = f"{'Reducing' if diff > 0 else 'Increasing'} tickets by {abs(diff)} → {t_impact:+.1f}% churn impact"
    if "Discount Level" in levers:
        diff = values.get("Discount Level", levers["Discount Level"]["current"]) - levers["Discount Level"]["current"]
        d_impact = diff * 0.15
        impact += d_impact
        details["Discount Level"] = f"{'Increasing' if diff > 0 else 'Reducing'} discount by {abs(diff)}% → {d_impact:+.1f}% churn impact"
    if "Sentiment Score" in levers:
        diff = values.get("Sentiment Score", levers["Sentiment Score"]["current"]) - levers["Sentiment Score"]["current"]
        s_impact = -diff * 0.12
        impact += s_impact
        details["Sentiment"] = f"{'Improving' if diff > 0 else 'Worsening'} sentiment by {abs(diff)}pts → {s_impact:+.1f}% churn impact"
    if "App Crashes" in levers:
        diff = levers["App Crashes"]["current"] - values.get("App Crashes", levers["App Crashes"]["current"])
        c_impact = diff * 0.5
        impact += c_impact
        details["App Crashes"] = f"{'Reducing' if diff > 0 else 'Increasing'} crashes by {abs(diff)} → {c_impact:+.1f}% churn impact"
    new_churn = max(5, min(60, base_churn + impact))
    return {
        "base_churn": base_churn, "new_churn": round(new_churn, 1),
        "churn_change": round(new_churn - base_churn, 1),
        "revenue_impact": round((new_churn - base_churn) / 100 * 456000 * 12, 0),
        "customers_saved": round((base_churn - new_churn) / 100 * 7043, 0),
        "details": details,
    }
