import numpy as np
from datetime import datetime, timedelta


def generate_clv_data(df=None, seed=42):
    rng = np.random.default_rng(seed)

    clv_values = rng.uniform(200, 5000, 1000).tolist()
    avg_clv = round(sum(clv_values) / len(clv_values), 2)

    segments = {
        "High Value": 22,
        "Medium Value": 45,
        "Low Value": 33,
    }

    monthly_clv = []
    base = avg_clv
    for m in range(1, 13):
        month_name = datetime(2024, m, 1).strftime("%b")
        variation = rng.uniform(-150, 150)
        monthly_clv.append({"month": month_name, "avg_clv": round(base + variation, 2)})

    top_customers = []
    contract_types = ["Month-to-month", "One year", "Two year"]
    for i in range(1, 11):
        cid = f"CUST_{rng.integers(10000, 99999)}"
        clv = round(rng.uniform(2000, 5000), 2)
        tenure = int(rng.integers(1, 72))
        contract = rng.choice(contract_types)
        risk = rng.choice(["High", "Medium", "Low"], p=[0.2, 0.5, 0.3])
        top_customers.append({
            "customer_id": cid,
            "clv": clv,
            "tenure": tenure,
            "contract": contract,
            "risk": risk,
        })

    clv_by_contract = {
        "Month-to-month": 950,
        "One year": 2100,
        "Two year": 3800,
    }

    clv_by_region = {
        "NA": 2200,
        "EMEA": 1800,
        "APAC": 1500,
        "LATAM": 1200,
    }

    at_risk_high_value = []
    for i in range(8):
        cid = f"CUST_{rng.integers(10000, 99999)}"
        clv = round(rng.uniform(2500, 4800), 2)
        prob = round(rng.uniform(0.35, 0.85), 2)
        actions = ["Send retention offer", "Schedule check-in call", "Apply loyalty discount",
                    "Upgrade support tier", "Personalized outreach campaign"]
        at_risk_high_value.append({
            "customer_id": cid,
            "clv": clv,
            "churn_probability": prob,
            "recommended_action": rng.choice(actions),
        })

    return {
        "clv_distribution": [round(v, 2) for v in clv_values],
        "avg_clv": avg_clv,
        "high_value_threshold": 2500,
        "segments": segments,
        "monthly_clv": monthly_clv,
        "top_customers": top_customers,
        "clv_by_contract": clv_by_contract,
        "clv_by_region": clv_by_region,
        "at_risk_high_value": at_risk_high_value,
    }


def predict_clv_for_customer(tenure, contract, monthly_charges, total_charges):
    multipliers = {"Month-to-month": 1.0, "One year": 1.8, "Two year": 2.5}
    base = 200
    tenure_bonus = min(tenure * 5, 500)
    contract_mult = multipliers.get(contract, 1.0)
    predicted = round(base + tenure_bonus + contract_mult * monthly_charges * 12, 2)
    ci_lower = round(predicted * 0.88, 2)
    ci_upper = round(predicted * 1.12, 2)

    if predicted >= 2500:
        segment = "High Value"
    elif predicted >= 1200:
        segment = "Medium Value"
    else:
        segment = "Low Value"

    return {
        "predicted_clv": predicted,
        "confidence_interval": [ci_lower, ci_upper],
        "segment": segment,
        "factors": [
            {"name": "Base Value", "value": base, "weight": "Fixed"},
            {"name": "Tenure Bonus", "value": tenure_bonus, "weight": f"{tenure} months"},
            {"name": "Contract Multiplier", "value": contract_mult, "weight": contract},
            {"name": "Annualized Charges", "value": round(contract_mult * monthly_charges * 12, 2), "weight": "Recurring"},
        ],
    }
