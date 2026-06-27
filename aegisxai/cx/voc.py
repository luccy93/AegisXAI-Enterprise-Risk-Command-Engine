import numpy as np


def generate_voc_data(seed=42):
    rng = np.random.default_rng(seed)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    categories = ["Network", "Billing", "Support", "Application", "Pricing"]
    monthly_complaints = []
    for m in months:
        for cat in categories:
            base = {"Network": 35, "Billing": 25, "Support": 20, "Application": 15, "Pricing": 5}[cat]
            count = max(0, int(base + rng.normal(0, 5)))
            monthly_complaints.append({"month": m, "category": cat, "count": count})

    top_complaints = [
        {"issue": "Frequent network outages during peak hours", "count": 245, "trend": "up"},
        {"issue": "Incorrect billing charges on monthly invoice", "count": 198, "trend": "stable"},
        {"issue": "Long wait times for customer support", "count": 156, "trend": "down"},
        {"issue": "Mobile app crashes on latest update", "count": 112, "trend": "up"},
        {"issue": "Unexpected price increase on renewal", "count": 87, "trend": "stable"},
    ]

    top_praises = [
        {"feature": "Fast internet speeds", "count": 312},
        {"feature": "Helpful customer support agents", "count": 278},
        {"feature": "Easy online bill pay", "count": 195},
        {"feature": "Reliable network coverage", "count": 167},
        {"feature": "User-friendly mobile app", "count": 143},
    ]

    emerging_concerns = [
        "Increasing dissatisfaction with 5G tower placement in residential areas",
        "Growing demand for customized family plan options",
        "Rising complaints about international roaming charges",
        "Customers requesting better self-service portal functionality",
        "Early signs of churn among long-tenure customers due to pricing",
    ]

    return {
        "top_complaints": top_complaints,
        "top_praises": top_praises,
        "complaint_categories": {"Network": 35, "Billing": 25, "Support": 20, "Application": 15, "Pricing": 5},
        "monthly_complaints": monthly_complaints,
        "emerging_concerns": emerging_concerns,
    }


def classify_complaint(text):
    text_lower = text.lower()
    network_keywords = ["network", "coverage", "signal", "dropped call", "slow internet", "speed", "connection", "outage"]
    billing_keywords = ["bill", "billing", "charge", "price", "pricing", "cost", "fee", "expensive", "overcharge", "invoice"]
    support_keywords = ["support", "agent", "customer service", "help desk", "wait time", "response", "representative"]
    app_keywords = ["app", "application", "login", "portal", "interface", "mobile", "website", "ui", "crash", "bug"]

    weights = {"Network": 0, "Billing": 0, "Support": 0, "Application": 0, "Pricing": 0, "Other": 0}

    for kw in network_keywords:
        if kw in text_lower:
            weights["Network"] += 1
    for kw in billing_keywords:
        if kw in text_lower:
            weights["Billing"] += 1
    for kw in support_keywords:
        if kw in text_lower:
            weights["Support"] += 1
    for kw in app_keywords:
        if kw in text_lower:
            weights["Application"] += 1

    if "price" in text_lower or "pricing" in text_lower or "expensive" in text_lower or "cost" in text_lower:
        weights["Pricing"] += 1

    best = max(weights, key=weights.get)
    return best if weights[best] > 0 else "Other"


def generate_complaint_data(seed=42):
    rng = np.random.default_rng(seed)

    complaint_templates = [
        "The network signal keeps dropping every evening",
        "I was overcharged on my last bill and need a refund",
        "Customer support takes forever to respond to my tickets",
        "The mobile app crashes every time I try to check my usage",
        "Your pricing is too high compared to competitors",
        "Poor network coverage in my area, especially indoors",
        "I got charged twice for the same month",
        "Waiting for 30 minutes to speak to an agent is unacceptable",
        "The app keeps logging me out randomly",
        "My bill increased without any notification",
        "Slow internet speeds during work hours affecting productivity",
        "The customer service representative was rude and unhelpful",
        "Hidden fees appeared on my latest statement",
        "App notifications are not working properly",
        "Service outages are becoming too frequent",
        "Annual price hike is unreasonable for loyal customers",
        "The self-service portal is confusing to navigate",
        "Installation appointment was delayed without notice",
        "International roaming charges are way too expensive",
        "Technical support could not fix my issue after three visits",
    ]

    complaints = []
    for i, template in enumerate(complaint_templates):
        category = classify_complaint(template)
        complaints.append({
            "complaint_id": f"CMP-{2000 + i}",
            "text": template,
            "category": category,
            "priority": rng.choice(["Low", "Medium", "High", "Critical"], p=[0.15, 0.40, 0.35, 0.10]),
            "status": rng.choice(["Open", "In Progress", "Resolved", "Closed"], p=[0.20, 0.30, 0.35, 0.15]),
            "date": f"2025-{rng.integers(1, 13):02d}-{rng.integers(1, 29):02d}",
        })

    return complaints
