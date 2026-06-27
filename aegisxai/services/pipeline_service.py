import numpy as np
from datetime import datetime, timedelta


def generate_pipeline_data(seed=42):
    rng = np.random.default_rng(seed)

    pipelines = [
        {"name": "Customer Data Ingestion", "status": "Running", "rows_processed": 245000, "last_run": "2 min ago", "duration": "3.2 min", "source": "CRM API", "destination": "Data Lake", "freshness_min": 3},
        {"name": "Payment Transaction Sync", "status": "Running", "rows_processed": 182000, "last_run": "5 min ago", "duration": "4.8 min", "source": "Payment Gateway", "destination": "Analytics DB", "freshness_min": 6},
        {"name": "User Behavior ETL", "status": "Running", "rows_processed": 310000, "last_run": "1 min ago", "duration": "6.1 min", "source": "Event Stream", "destination": "Warehouse", "freshness_min": 2},
        {"name": "Support Ticket Pipeline", "status": "Running", "rows_processed": 89000, "last_run": "4 min ago", "duration": "2.5 min", "source": "Zendesk API", "destination": "Support DB", "freshness_min": 5},
        {"name": "Marketing Attribution Sync", "status": "Failed", "rows_processed": 45000, "last_run": "22 min ago", "duration": "8.7 min", "source": "HubSpot API", "destination": "Marketing DB", "freshness_min": 30},
        {"name": "Regulatory Reporting Batch", "status": "Paused", "rows_processed": 12000, "last_run": "3 hours ago", "duration": "1.5 min", "source": "Compliance DB", "destination": "Reporting Bucket", "freshness_min": 180},
    ]

    total_rows_processed_today = 850000

    pipeline_runs = []
    base_time = datetime(2024, 6, 1, 0, 0, 0)
    pipeline_names = [p["name"] for p in pipelines]
    statuses = ["Success", "Failed", "Running"]
    for i in range(30):
        ts = base_time + timedelta(hours=rng.integers(0, 24), minutes=rng.integers(0, 59))
        pipeline_runs.append({
            "pipeline": str(rng.choice(pipeline_names)),
            "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
            "status": str(rng.choice(statuses, p=[0.82, 0.10, 0.08])),
            "rows": int(rng.integers(1000, 80000)),
            "duration": round(rng.uniform(0.5, 12.0), 1),
        })

    tables = ["customers", "transactions", "support_tickets", "user_events", "marketing_attribution", "regulatory_reports"]
    data_freshness = []
    for t in tables:
        staleness = round(rng.uniform(0, 12), 1)
        if staleness < 1:
            status = "Fresh"
        elif staleness < 5:
            status = "Stale"
        else:
            status = "Overdue"
        data_freshness.append({
            "table": t,
            "last_updated": (datetime(2024, 6, 1, 6, 0) - timedelta(hours=staleness)).strftime("%Y-%m-%d %H:%M:%S"),
            "staleness_hours": staleness,
            "status": status,
        })

    schema_changes = []
    change_types = ["Column Added", "Column Dropped", "Data Type Changed", "Index Added", "Constraint Modified"]
    status_choices = ["Applied", "Pending Review", "Rolled Back"]
    for i in range(5):
        schema_changes.append({
            "table": str(rng.choice(tables)),
            "column": f"col_{rng.integers(1, 20)}",
            "change_type": str(rng.choice(change_types)),
            "date": datetime(2024, 6, rng.integers(1, 28)).strftime("%Y-%m-%d"),
            "status": str(rng.choice(status_choices)),
        })

    return {
        "pipelines": pipelines,
        "total_rows_processed_today": total_rows_processed_today,
        "avg_pipeline_duration": "4.2 min",
        "failed_pipelines_today": 2,
        "pipeline_runs": pipeline_runs,
        "data_freshness": data_freshness,
        "schema_changes": schema_changes,
    }


def get_data_quality_score():
    return {
        "overall": 87,
        "completeness": 92,
        "validity": 85,
        "timeliness": 78,
        "uniqueness": 88,
    }
