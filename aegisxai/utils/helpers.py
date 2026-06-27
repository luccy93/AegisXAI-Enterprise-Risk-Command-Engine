import base64
import random
import pandas as pd


def format_currency(val):
    return f"${val:,.2f}"


def make_download_link(df, filename, label):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{label}</a>'
    return href


def audit_log(action, details="", user="system"):
    try:
        import streamlit as st

        if "audit_logs" not in st.session_state:
            st.session_state.audit_logs = []
        st.session_state.audit_logs.append(
            {"action": action, "details": details, "user": user}
        )
    except ImportError:
        pass


def generate_event():
    event_types = [
        "Model Drift Detected",
        "High Churn Risk Alert",
        "Data Pipeline Failure",
        "Retraining Completed",
        "A/B Test Started",
        "Compliance Audit Triggered",
        "Threshold Breach",
    ]
    severities = ["low", "medium", "high", "critical"]
    return {
        "event": random.choice(event_types),
        "severity": random.choice(severities),
        "timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def get_system_health_status():
    data = {
        "Component": [
            "Model Server",
            "Database",
            "API Gateway",
            "Data Pipeline",
            "Monitoring",
            "Alert System",
        ],
        "Status": [
            random.choice(["Healthy", "Healthy", "Healthy", "Degraded"]),
            random.choice(["Healthy", "Healthy", "Healthy", "Degraded"]),
            random.choice(["Healthy", "Healthy", "Healthy", "Unhealthy"]),
            random.choice(["Healthy", "Healthy", "Degraded", "Unhealthy"]),
            random.choice(["Healthy", "Healthy", "Healthy", "Degraded"]),
            random.choice(["Healthy", "Healthy", "Degraded", "Unhealthy"]),
        ],
        "Uptime": [
            "99.9%",
            "99.8%",
            "99.7%",
            "98.5%",
            "99.9%",
            "99.6%",
        ],
        "Response Time": [
            "45ms",
            "12ms",
            "23ms",
            "150ms",
            "8ms",
            "5ms",
        ],
    }
    return pd.DataFrame(data)


def get_compliance_status():
    return {
        "GDPR": {"status": "Compliant", "last_audit": "2024-12-01", "score": 96},
        "CCPA": {"status": "Compliant", "last_audit": "2024-11-15", "score": 94},
        "HIPAA": {
            "status": "Partially Compliant",
            "last_audit": "2024-10-20",
            "score": 87,
        },
        "SOC2": {"status": "Compliant", "last_audit": "2024-12-10", "score": 98},
    }


def render_system_status():
    try:
        import streamlit as st

        health_df = get_system_health_status()
        status_map = {
            "Healthy": ":green_circle:",
            "Degraded": ":orange_circle:",
            "Unhealthy": ":red_circle:",
        }
        health_df["Indicator"] = health_df["Status"].map(status_map)
        st.dataframe(
            health_df[["Indicator", "Component", "Status", "Uptime", "Response Time"]],
            hide_index=True,
            use_container_width=True,
        )
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Overall Health", "97.2%", delta="+0.3%")
        with col2:
            st.metric("Active Alerts", "3", delta="-1")
    except ImportError:
        pass
