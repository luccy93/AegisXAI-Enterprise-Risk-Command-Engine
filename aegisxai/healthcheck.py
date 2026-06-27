"""Healthcheck endpoint for Docker container orchestration."""
import sys
import json

try:
    from aegisxai.models.features import load_data
    df = load_data()
    if df.empty:
        print("UNHEALTHY: dataset empty")
        sys.exit(1)
    print(json.dumps({
        "status": "healthy",
        "rows": len(df),
        "columns": list(df.columns),
    }))
    sys.exit(0)
except Exception as e:
    print(f"UNHEALTHY: {e}")
    sys.exit(1)
