import numpy as np
import pandas as pd


def generate_engagement_data(df=None, seed=42):
    rng = np.random.default_rng(seed)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    monthly_active_users = []
    base_mau = 1200
    for i, m in enumerate(months):
        mau = max(500, int(base_mau + rng.normal(0, 60) + i * 15))
        monthly_active_users.append({"month": m, "maus": mau})

    retention_curve = []
    rates = [100.0, 85.0, 72.0, 63.0, 56.0, 50.0, 45.0, 41.0, 38.0, 35.0, 33.0, 31.0]
    for m, rate in zip(months, rates):
        noise = rng.normal(0, 1.5)
        retention_curve.append({"month": m, "retention_rate": round(min(100.0, max(0.0, rate + noise)), 1)})

    return {
        "engagement_distribution": {"Highly Engaged": 22, "Moderately Engaged": 35, "Disengaged": 28, "Inactive": 15},
        "avg_login_frequency": 3.2,
        "avg_session_duration": 14.5,
        "feature_adoption_rate": 67.0,
        "monthly_active_users": monthly_active_users,
        "retention_curve": retention_curve,
    }


def predict_loyalty(customer_id=None, seed=42):
    rng = np.random.default_rng(seed + (customer_id or 0))

    loyalty_distribution = {"Advocate": 15, "Loyal": 28, "Neutral": 32, "At Risk": 18, "Detractor": 7}

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    loyalty_trend = []
    for i, m in enumerate(months):
        val = int(60 + rng.normal(0, 5) + i * 0.5)
        loyalty_trend.append({"month": m, "loyalty_score": val})

    if customer_id is not None:
        tiers = ["Diamond", "Platinum", "Gold", "Silver", "Bronze"]
        weights = [0.02, 0.07, 0.18, 0.32, 0.41]
        tier = rng.choice(tiers, p=weights)
        score = int(rng.normal(65, 15))
        score = max(0, min(100, score))

        recommendations = []
        if score < 40:
            recommendations = ["Offer retention discount", "Schedule personal check-in call", "Resolve open support tickets"]
        elif score < 60:
            recommendations = ["Send loyalty program invite", "Provide usage tips and tricks", "Offer referral bonus"]
        elif score < 80:
            recommendations = ["Thank you communication", "Early access to new features", "Exclusive webinar invite"]
        else:
            recommendations = ["Advocate program enrollment", "Customer advisory board invite", "Case study opportunity"]

        return {
            "customer_id": customer_id,
            "tier": tier,
            "loyalty_score": score,
            "recommendations": recommendations,
            "loyalty_distribution": loyalty_distribution,
            "loyalty_trend": loyalty_trend,
        }

    return {
        "loyalty_distribution": loyalty_distribution,
        "loyalty_trend": loyalty_trend,
    }


def get_loyalty_tiers():
    return [
        {"tier": "Bronze", "min_points": 0, "customers": 450},
        {"tier": "Silver", "min_points": 500, "customers": 320},
        {"tier": "Gold", "min_points": 1500, "customers": 180},
        {"tier": "Platinum", "min_points": 3500, "customers": 70},
        {"tier": "Diamond", "min_points": 7000, "customers": 15},
    ]


def generate_loyalty_data(seed=42):
    rng = np.random.default_rng(seed)

    tiers = get_loyalty_tiers()
    total_customers = sum(t["customers"] for t in tiers)

    reward_points_distribution = {
        "0-500": int(total_customers * 0.40),
        "501-1500": int(total_customers * 0.28),
        "1501-3500": int(total_customers * 0.18),
        "3501-7000": int(total_customers * 0.10),
        "7000+": int(total_customers * 0.04),
    }

    redemption_history = []
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    base_redemptions = 45
    for i, m in enumerate(months):
        count = max(5, int(base_redemptions + rng.normal(0, 8) + i * 2))
        redemption_history.append({"month": m, "redemptions": count})

    return {
        "loyalty_tiers": tiers,
        "total_enrolled_customers": total_customers,
        "reward_points_distribution": reward_points_distribution,
        "redemption_history": redemption_history,
        "avg_points_earned_monthly": 320,
        "avg_reward_redemption_rate": 0.45,
    }
