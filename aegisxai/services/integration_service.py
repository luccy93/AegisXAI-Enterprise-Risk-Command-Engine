import numpy as np
from datetime import datetime, timedelta


def generate_integration_data(seed=42):
    rng = np.random.default_rng(seed)

    integrations = [
        {"name": "Salesforce", "status": "Connected", "last_sync": "2 min ago", "records_imported": 485000, "connection_type": "API", "health": "Healthy"},
        {"name": "HubSpot", "status": "Connected", "last_sync": "5 min ago", "records_imported": 312000, "connection_type": "API", "health": "Healthy"},
        {"name": "Zendesk", "status": "Connected", "last_sync": "1 min ago", "records_imported": 198000, "connection_type": "API", "health": "Healthy"},
        {"name": "Shopify", "status": "Connected", "last_sync": "12 min ago", "records_imported": 425000, "connection_type": "Webhook", "health": "Healthy"},
        {"name": "Segment", "status": "Connected", "last_sync": "3 min ago", "records_imported": 567000, "connection_type": "Webhook", "health": "Healthy"},
        {"name": "Snowflake", "status": "Connected", "last_sync": "8 min ago", "records_imported": 290000, "connection_type": "DB", "health": "Degraded"},
        {"name": "BigQuery", "status": "Disconnected", "last_sync": "45 min ago", "records_imported": 98000, "connection_type": "DB", "health": "Down"},
        {"name": "Slack", "status": "Connected", "last_sync": "1 min ago", "records_imported": 25000, "connection_type": "Webhook", "health": "Healthy"},
    ]

    total_records_synced = 2400000

    sync_history = []
    base_time = datetime(2024, 6, 1, 0, 0, 0)
    integration_names = [i["name"] for i in integrations]
    statuses = ["Success", "Failed", "Partial"]
    for i in range(20):
        ts = base_time + timedelta(hours=rng.integers(0, 48), minutes=rng.integers(0, 59))
        sync_history.append({
            "integration": str(rng.choice(integration_names)),
            "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
            "status": str(rng.choice(statuses, p=[0.85, 0.10, 0.05])),
            "records": int(rng.integers(500, 50000)),
            "duration_sec": int(rng.integers(10, 300)),
        })

    return {
        "integrations": integrations,
        "total_records_synced": total_records_synced,
        "sync_frequency": "15 min",
        "failed_syncs_24h": 3,
        "sync_history": sync_history,
    }


def run_sync(integration_name):
    rng = np.random.default_rng()
    should_fail = rng.random() < 0.05
    records = int(rng.integers(1000, 30000))
    duration = int(rng.integers(15, 180))

    if should_fail:
        return {
            "status": "Failed",
            "records_processed": 0,
            "duration": duration,
        }

    return {
        "status": "Success",
        "records_processed": records,
        "duration": duration,
    }


def get_integration_health(integration_name):
    rng = np.random.default_rng()

    latencies = {
        "Salesforce": 120,
        "HubSpot": 85,
        "Zendesk": 60,
        "Shopify": 200,
        "Segment": 45,
        "Snowflake": 350,
        "BigQuery": 500,
        "Slack": 30,
    }

    error_rates = {
        "Salesforce": 0.5,
        "HubSpot": 0.3,
        "Zendesk": 0.1,
        "Shopify": 1.2,
        "Segment": 0.2,
        "Snowflake": 3.8,
        "BigQuery": 12.5,
        "Slack": 0.05,
    }

    latency = latencies.get(integration_name, int(rng.integers(20, 500)))
    error_rate = error_rates.get(integration_name, round(rng.uniform(0.1, 10.0), 1))

    if latency > 400 or error_rate > 10:
        status = "Down"
    elif latency > 200 or error_rate > 3:
        status = "Degraded"
    else:
        status = "Healthy"

    return {
        "status": status,
        "latency_ms": latency,
        "error_rate": error_rate,
        "last_check": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
