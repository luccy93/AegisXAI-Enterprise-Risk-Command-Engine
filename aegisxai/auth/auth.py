import streamlit as st

USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "exec": {"password": "admin123", "role": "executive"},
    "sci": {"password": "sci123", "role": "scientist"},
    "agent": {"password": "agent123", "role": "agent"},
}

ROLES = {
    "admin": {
        "pages": [
            "Executive Dashboard",
            "Customer 360",
            "Predictive Analytics",
            "Retention Hub",
            "Model Management",
            "System Health",
            "User Management",
        ],
        "can_retrain": True,
        "can_export": True,
        "can_manage_users": True,
    },
    "executive": {
        "pages": ["Executive Dashboard", "Customer 360", "Retention Hub", "System Health"],
        "can_retrain": False,
        "can_export": True,
        "can_manage_users": False,
    },
    "scientist": {
        "pages": [
            "Predictive Analytics",
            "Model Management",
            "Customer 360",
            "Retention Hub",
        ],
        "can_retrain": True,
        "can_export": True,
        "can_manage_users": False,
    },
    "agent": {
        "pages": ["Customer 360", "Retention Hub"],
        "can_retrain": False,
        "can_export": False,
        "can_manage_users": False,
    },
}


def authenticate(username, password, role):
    if username in USERS:
        user = USERS[username]
        if user["password"] == password and user["role"] == role:
            return {"username": username, "role": role, "authenticated": True}
    return {"username": username, "role": role, "authenticated": False}


def get_role_permissions(role):
    return ROLES.get(role, {"pages": [], "can_retrain": False, "can_export": False, "can_manage_users": False})


def check_page_access(page, role):
    permissions = get_role_permissions(role)
    return page in permissions["pages"]
