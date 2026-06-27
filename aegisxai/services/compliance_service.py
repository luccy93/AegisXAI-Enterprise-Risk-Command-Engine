import numpy as np
from datetime import datetime, timedelta


def generate_compliance_data(seed=42):
    rng = np.random.default_rng(seed)

    activities = [
        {"activity": "Customer Analytics Processing", "status": "Active", "data_categories": ["Personal", "Behavioral"], "retention_days": 365},
        {"activity": "Payment Transaction Logging", "status": "Active", "data_categories": ["Financial"], "retention_days": 730},
        {"activity": "Support Ticket Management", "status": "Active", "data_categories": ["Personal", "Behavioral"], "retention_days": 180},
        {"activity": "Marketing Profile Building", "status": "Active", "data_categories": ["Personal", "Behavioral"], "retention_days": 90},
        {"activity": "Fraud Detection Analysis", "status": "Active", "data_categories": ["Financial", "Behavioral"], "retention_days": 365},
        {"activity": "Product Recommendation Engine", "status": "Active", "data_categories": ["Behavioral", "Technical"], "retention_days": 180},
        {"activity": "Data Backup and Recovery", "status": "Active", "data_categories": ["Personal", "Financial", "Behavioral", "Technical"], "retention_days": 1095},
        {"activity": "Employee Access Auditing", "status": "Active", "data_categories": ["Personal", "Technical"], "retention_days": 365},
    ]

    consent_by_purpose = {
        "Marketing": 78,
        "Analytics": 92,
        "Support": 96,
        "Profiling": 65,
    }

    access_logs = []
    users = ["alice@aegisxai.com", "bob@aegisxai.com", "carol@aegisxai.com", "dave@aegisxai.com"]
    actions = ["READ", "WRITE", "DELETE", "EXPORT"]
    resources = ["customer_db", "payment_table", "analytics_warehouse", "support_tickets"]
    ips = ["10.0.1.42", "10.0.1.55", "10.0.2.10", "192.168.1.100"]
    for i in range(12):
        ts = datetime(2024, 6, rng.integers(1, 28), rng.integers(8, 18), rng.integers(0, 59))
        access_logs.append({
            "user": str(rng.choice(users)),
            "action": str(rng.choice(actions)),
            "resource": str(rng.choice(resources)),
            "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
            "ip": str(rng.choice(ips)),
        })

    privacy_requests = []
    types_list = ["Access Request", "Deletion Request", "Correction Request", "Portability Request", "Objection"]
    statuses = ["Completed", "In Progress", "Pending", "Approved"]
    for i in range(5):
        privacy_requests.append({
            "request_id": f"PR-{rng.integers(1000, 9999)}",
            "type": str(rng.choice(types_list)),
            "status": str(rng.choice(statuses)),
            "date": datetime(2024, 6, rng.integers(1, 28)).strftime("%Y-%m-%d"),
        })

    return {
        "gdpr_compliance_pct": 94,
        "data_retention_ok": True,
        "consent_rate": 87,
        "active_processing_activities": activities,
        "data_categories": {"Personal": 45, "Financial": 20, "Behavioral": 25, "Technical": 10},
        "consent_by_purpose": consent_by_purpose,
        "access_logs_recent": access_logs,
        "data_retention_summary": {"Compliant": 92, "Expiring Soon": 5, "Overdue": 3},
        "privacy_requests": privacy_requests,
    }


def get_data_map():
    return [
        {
            "source": "Customer Registration",
            "categories": ["Personal", "Technical"],
            "purpose": "Account Management",
            "retention": "365 days",
            "security": "AES-256 encrypted",
        },
        {
            "source": "Payment Processing",
            "categories": ["Financial"],
            "purpose": "Billing & Invoicing",
            "retention": "730 days",
            "security": "PCI-DSS compliant",
        },
        {
            "source": "Usage Analytics",
            "categories": ["Behavioral", "Technical"],
            "purpose": "Product Improvement",
            "retention": "180 days",
            "security": "Anonymized & encrypted",
        },
        {
            "source": "Support Tickets",
            "categories": ["Personal", "Behavioral"],
            "purpose": "Customer Support",
            "retention": "180 days",
            "security": "AES-256 encrypted",
        },
        {
            "source": "Marketing Platform",
            "categories": ["Personal", "Behavioral"],
            "purpose": "Marketing & Outreach",
            "retention": "90 days",
            "security": "Consent-controlled",
        },
        {
            "source": "Third-party Integrations",
            "categories": ["Personal", "Behavioral", "Financial"],
            "purpose": "Service Delivery",
            "retention": "365 days",
            "security": "DPA in place",
        },
        {
            "source": "Data Backup",
            "categories": ["Personal", "Financial", "Behavioral", "Technical"],
            "purpose": "Disaster Recovery",
            "retention": "1095 days",
            "security": "Encrypted at rest",
        },
    ]
