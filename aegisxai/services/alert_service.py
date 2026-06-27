import uuid
from datetime import datetime


def init_alerts():
    try:
        import streamlit as st
    except ImportError:
        return

    if "alerts" not in st.session_state:
        st.session_state.alerts = [
            {
                "id": str(uuid.uuid4()),
                "severity": "high",
                "type": "Churn Risk",
                "description": "Customer #7590-VHVEG showing 87% churn probability",
                "customer_id": "7590-VHVEG",
                "status": "open",
                "created_at": datetime.now().isoformat(),
                "resolved_at": None,
                "escalated": False,
            },
            {
                "id": str(uuid.uuid4()),
                "severity": "medium",
                "type": "Model Drift",
                "description": "Feature distribution shift detected in tenure_group",
                "customer_id": None,
                "status": "open",
                "created_at": datetime.now().isoformat(),
                "resolved_at": None,
                "escalated": False,
            },
            {
                "id": str(uuid.uuid4()),
                "severity": "low",
                "type": "Data Quality",
                "description": "3 missing values detected in TotalCharges column",
                "customer_id": None,
                "status": "resolved",
                "created_at": datetime.now().isoformat(),
                "resolved_at": datetime.now().isoformat(),
                "escalated": False,
            },
        ]


def create_alert(severity, alert_type, description, customer_id=None):
    try:
        import streamlit as st
    except ImportError:
        return

    if "alerts" not in st.session_state:
        init_alerts()
    st.session_state.alerts.insert(
        0,
        {
            "id": str(uuid.uuid4()),
            "severity": severity,
            "type": alert_type,
            "description": description,
            "customer_id": customer_id,
            "status": "open",
            "created_at": datetime.now().isoformat(),
            "resolved_at": None,
            "escalated": False,
        },
    )


def resolve_alert(alert_id):
    try:
        import streamlit as st
    except ImportError:
        return

    if "alerts" not in st.session_state:
        return
    for alert in st.session_state.alerts:
        if alert["id"] == alert_id:
            alert["status"] = "resolved"
            alert["resolved_at"] = datetime.now().isoformat()
            break


def escalate_alert(alert_id):
    try:
        import streamlit as st
    except ImportError:
        return

    if "alerts" not in st.session_state:
        return
    severity_order = {"low": "medium", "medium": "high", "high": "critical"}
    for alert in st.session_state.alerts:
        if alert["id"] == alert_id:
            current = alert["severity"]
            alert["severity"] = severity_order.get(current, current)
            alert["escalated"] = True
            break
