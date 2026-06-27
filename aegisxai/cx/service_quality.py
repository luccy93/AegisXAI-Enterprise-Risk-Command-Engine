import numpy as np


def generate_service_quality_data(seed=42):
    rng = np.random.default_rng(seed)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    monthly_trend = []
    for m in months:
        monthly_trend.append({
            "month": m,
            "avg_response_time_hours": round(float(rng.normal(2.5, 0.3)), 2),
            "avg_resolution_time_hours": round(float(rng.normal(4.8, 0.5)), 2),
            "fcr_rate": round(float(rng.normal(78, 3)), 1),
            "escalation_rate": round(float(rng.normal(12, 2)), 1),
            "sla_compliance": round(float(rng.normal(94, 2)), 1),
            "reopen_rate": round(float(rng.normal(6, 1.5)), 1),
        })

    department_quality = {
        "Support": round(float(rng.normal(3.2, 0.5)), 1),
        "Billing": round(float(rng.normal(5.1, 0.6)), 1),
        "Network": round(float(rng.normal(6.8, 0.8)), 1),
        "Sales": round(float(rng.normal(2.1, 0.3)), 1),
        "Technical": round(float(rng.normal(4.5, 0.5)), 1),
    }

    return {
        "avg_response_time_hours": 2.5,
        "avg_resolution_time_hours": 4.8,
        "fcr_rate": 78.0,
        "escalation_rate": 12.0,
        "sla_compliance": 94.0,
        "reopen_rate": 6.0,
        "monthly_trend": monthly_trend,
        "department_quality": department_quality,
    }


def generate_ticket_satisfaction(seed=42):
    rng = np.random.default_rng(seed)

    feedback_texts = [
        "The agent was very helpful and resolved my issue quickly.",
        "Took too long to get a response. Very frustrating experience.",
        "Professional and courteous service. Would recommend.",
        "The issue was resolved but required multiple follow-ups.",
        "Excellent support! The team went above and beyond.",
        "Still facing the same problem after the fix. Not satisfied.",
        "Good response time but the solution was temporary.",
        "The technician explained everything clearly. Great experience.",
        "Billing department was difficult to reach. Poor experience.",
        "Quick resolution. Very happy with the service provided.",
        "The agent didn't seem knowledgeable about the issue.",
        "Smooth process from start to finish. Highly impressed.",
        "Had to repeat my issue multiple times. Annoying.",
        "Very patient and thorough support. Thank you!",
        "Automated responses delayed the resolution process.",
    ]

    tickets = []
    for i in range(15):
        rating = int(rng.integers(1, 6))
        tickets.append({
            "ticket_id": f"TKT-{1000 + i}",
            "rating": rating,
            "agent_rating": max(1, min(5, rating + int(rng.integers(-1, 2)))),
            "feedback_text": feedback_texts[i],
            "resolved": rating >= 3 if rng.random() > 0.15 else False,
            "time_to_resolve_hours": round(float(max(0.5, rng.normal(4.5, 2.5))), 1),
        })

    return tickets
