import numpy as np
import pandas as pd


def generate_cx_recommendations(df=None, seed=42):
    rng = np.random.default_rng(seed)
    if df is None:
        n = 1000
        df = pd.DataFrame({
            "customer_id": range(1, n + 1),
            "churn_risk": rng.choice(["Low", "Medium", "High"], size=n, p=[0.55, 0.30, 0.15]),
            "engagement_score": rng.uniform(0, 100, size=n),
            "tenure_months": rng.integers(1, 73, size=n),
            "ticket_count": rng.integers(0, 10, size=n),
        })

    high_risk = df[df["churn_risk"] == "High"]
    medium_risk = df[df["churn_risk"] == "Medium"]

    issues_pool = [
        "Frequent support tickets without resolution",
        "Low engagement in the past 30 days",
        "Multiple billing complaints",
        "Decreased product usage",
        "Negative sentiment on recent survey",
        "Long tenure with no loyalty tier upgrade",
        "Competitive offer detected in market",
        "Unresolved technical issue",
    ]
    offer_types = ["Discount on next renewal", "Free upgrade for 3 months", "Loyalty bonus points", "Personalized onboarding session", "Premium support tier access"]
    channels = ["Email", "SMS", "Phone"]
    best_times = ["9:00 AM", "12:00 PM", "3:00 PM", "5:00 PM"]

    candidates = pd.concat([high_risk.sample(n=min(5, len(high_risk)), random_state=seed),
                            medium_risk.sample(n=min(3, len(medium_risk)), random_state=seed + 1)], ignore_index=True)

    recommendations = []
    for i, row in candidates.iterrows():
        if len(recommendations) >= 8:
            break
        recommendations.append({
            "customer_id": int(row["customer_id"]),
            "issue": rng.choice(issues_pool),
            "channel": rng.choice(channels),
            "offer_type": rng.choice(offer_types),
            "best_time": rng.choice(best_times),
            "expected_impact": f"{int(rng.uniform(15, 45))}% retention probability increase",
        })

    return recommendations


def get_customer_360_satisfaction(df, customer_id, seed=42):
    rng = np.random.default_rng(seed + customer_id)

    if customer_id not in df["customer_id"].values:
        row = pd.DataFrame({"customer_id": [customer_id], "churn_risk": ["Medium"], "engagement_score": [50.0], "tenure_months": [12], "ticket_count": [2]})
        df = pd.concat([df, row], ignore_index=True)

    cust = df[df["customer_id"] == customer_id].iloc[0]
    csat = int(rng.integers(2, 6))
    nps = int(rng.integers(0, 11))
    sentiment = rng.choice(["Positive", "Neutral", "Negative"], p=[0.58, 0.27, 0.15])
    happiness = int(rng.integers(40, 96))
    engagement = round(float(cust["engagement_score"]), 1)
    loyalty_tier = rng.choice(["Diamond", "Platinum", "Gold", "Silver", "Bronze"], p=[0.02, 0.07, 0.18, 0.32, 0.41])
    churn_risk = str(cust["churn_risk"])
    open_tickets = int(cust["ticket_count"])

    recent_complaints = []
    if open_tickets > 0:
        topics = ["Billing issue", "Network connectivity", "Support wait time", "App functionality"]
        for _ in range(min(open_tickets, 3)):
            recent_complaints.append(rng.choice(topics))

    actions = []
    if churn_risk == "High":
        actions = ["Offer retention discount", "Schedule executive call", "Fast-track open tickets"]
    elif churn_risk == "Medium":
        actions = ["Send satisfaction survey", "Proactive check-in email", "Share usage tips"]
    elif sentiment == "Negative":
        actions = ["Root cause analysis of complaint", "Personal apology from manager", "Compensatory offer"]
    else:
        actions = ["Thank you note", "Referral program invite", "Loyalty reward"]

    return {
        "customer_id": customer_id,
        "csat": csat,
        "nps": nps,
        "sentiment": sentiment,
        "happiness_index": happiness,
        "engagement_score": engagement,
        "loyalty_tier": loyalty_tier,
        "open_tickets": open_tickets,
        "recent_complaints": recent_complaints,
        "churn_risk": churn_risk,
        "recommended_actions": actions,
    }


def generate_ai_insight(query_text):
    q = query_text.lower()

    if "satisfaction" in q and "decrease" in q:
        return (
            "Based on our analysis, the recent dip in customer satisfaction correlates with "
            "two primary drivers: (1) increased billing disputes following the pricing model update "
            "in Q3 (+18% complaint volume), and (2) intermittent network outages in the APAC region "
            "that impacted ~3,200 customers. Recommended actions include targeted communication to "
            "affected customers and accelerated deployment of network redundancy."
        )

    if "unhappy" in q or "dissatisfied" in q or "unhappy customers" in q:
        return (
            "Our analysis identifies three customer segments with elevated dissatisfaction: "
            "(1) Month-to-month contract customers (NPS +35 vs +48 average), "
            "(2) Customers in the APAC region (NPS +38, lowest region), and "
            "(3) High-tenure customers (>3 years) who experienced recent billing adjustments. "
            "These segments represent ~28% of the customer base but account for 52% of negative sentiment."
        )

    if "top complaint" in q or "common complaint" in q:
        return (
            "The top 5 customer complaints this period are: "
            "1. Network outages during peak hours (245 cases, trending up), "
            "2. Incorrect billing charges (198 cases, stable), "
            "3. Long support wait times (156 cases, improving), "
            "4. Mobile app crashes (112 cases, trending up), "
            "5. Unexpected price increases (87 cases). "
            "Network and billing issues together represent 56% of all complaints."
        )

    if "lowest satisfaction" in q and "region" in q:
        return (
            "APAC region has the lowest customer satisfaction at CSAT 3.9/5.0 and NPS +38. "
            "Key drivers: network reliability concerns in Southeast Asia markets, longer support "
            "resolution times (average 6.8 hours vs 4.8 global), and language support gaps. "
            "Recommended: localized network investments and multilingual support expansion."
        )

    return (
        "Overall customer experience metrics show stable performance with CSAT at 4.2/5.0, "
        "NPS at +46, and Happiness Index at 74/100. Key areas for improvement include network "
        "reliability in APAC and billing transparency. Positive momentum in support resolution "
        "times and feature adoption rates suggests current initiatives are gaining traction."
    )
