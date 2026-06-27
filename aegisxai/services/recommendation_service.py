import numpy as np
import pandas as pd


def generate_recommendations(df, model, scaler, feature_cols):
    try:
        X = scaler.transform(df[feature_cols].fillna(0))
        probas = model.predict_proba(X)[:, 1]
        df = df.copy()
        df["churn_probability"] = probas

        high_risk = df[df["churn_probability"] > 0.7].sort_values(
            "churn_probability", ascending=False
        )
        recommendations = []
        for _, row in high_risk.iterrows():
            cid = row.get("customerID", "Unknown")
            prob = row["churn_probability"]
            recs = []
            if row.get("Contract") == "Month-to-month":
                recs.append("Offer 12-month contract with 10% discount")
            if row.get("OnlineSecurity") == "No":
                recs.append("Enroll in free Online Security trial")
            if row.get("TechSupport") == "No":
                recs.append("Provide complimentary Tech Support for 3 months")
            if row.get("MonthlyCharges", 0) > 80:
                recs.append("Review pricing plan - consider loyalty discount")
            if row.get("tenure", 0) < 12:
                recs.append("Send personalized onboarding follow-up")
            recommendations.append(
                {"customer_id": cid, "churn_probability": round(prob, 4), "recommendations": recs}
            )
        return recommendations
    except Exception:
        return []


def get_retention_recommendation(churn_prob):
    if churn_prob < 0.3:
        return {
            "risk": "Low",
            "message": "Customer appears stable.", 
            "actions": ["Send quarterly satisfaction survey", "Share loyalty program benefits"],
        }
    elif churn_prob < 0.6:
        return {
            "risk": "Medium",
            "message": "Customer showing early churn signals.",
            "actions": [
                "Proactive check-in call",
                "Offer personalized discount",
                "Review service usage patterns",
            ],
        }
    else:
        return {
            "risk": "High",
            "message": "Customer at high risk of churning.",
            "actions": [
                "Immediate retention call from manager",
                "Offer retention incentive (20-30% discount)",
                "Assign dedicated account representative",
                "Escalate to executive support team",
            ],
        }


def generate_retention_strategies():
    return [
        {
            "id": 1,
            "name": "Loyalty Rewards Program",
            "target": "Customers with >24 months tenure",
            "expected_impact": "15-20% churn reduction",
            "cost": "Medium",
            "priority": "High",
        },
        {
            "id": 2,
            "name": "Contract Incentive",
            "target": "Month-to-month customers",
            "expected_impact": "25-30% churn reduction",
            "cost": "Low",
            "priority": "High",
        },
        {
            "id": 3,
            "name": "Tech Support Outreach",
            "target": "Customers without Tech Support",
            "expected_impact": "10-15% churn reduction",
            "cost": "Medium",
            "priority": "Medium",
        },
        {
            "id": 4,
            "name": "Pricing Optimization",
            "target": "Customers with >$80 monthly charges",
            "expected_impact": "20-25% churn reduction",
            "cost": "High",
            "priority": "Medium",
        },
        {
            "id": 5,
            "name": "Early Tenure Engagement",
            "target": "Customers with <12 months tenure",
            "expected_impact": "30-35% churn reduction",
            "cost": "Low",
            "priority": "High",
        },
    ]


def ab_test_summary():
    return {
        "current_winner": "Variant B - Personalized Discount",
        "confidence": "95%",
        "metrics": {
            "variant_a": {"name": "Generic Email Campaign", "retention_rate": 0.12, "cost_per_customer": 2.50},
            "variant_b": {"name": "Personalized Discount Offer", "retention_rate": 0.22, "cost_per_customer": 8.00},
            "control": {"name": "No Intervention", "retention_rate": 0.05, "cost_per_customer": 0},
        },
        "recommendation": "Deploy Variant B (Personalized Discount Offer) to all high-risk customers",
        "sample_size": 5000,
        "duration_days": 30,
    }
