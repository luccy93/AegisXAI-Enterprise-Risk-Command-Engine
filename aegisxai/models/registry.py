from ..config.settings import Settings


def init_registry():
    try:
        import streamlit as st
    except ImportError:
        return

    if "model_registry" not in st.session_state:
        st.session_state.model_registry = [
            {
                "version": "v1.0.0",
                "algorithm": "LogisticRegression",
                "accuracy": 0.7856,
                "active": False,
                "status": "deprecated",
            },
            {
                "version": "v2.0.0",
                "algorithm": "RandomForest",
                "accuracy": 0.8012,
                "active": False,
                "status": "deprecated",
            },
            {
                "version": "v3.0.0",
                "algorithm": "XGBoost",
                "accuracy": 0.8105,
                "active": False,
                "status": "archived",
            },
            {
                "version": Settings.MODEL_VERSION,
                "algorithm": "XGBoost+LightGBM Ensemble",
                "accuracy": 0.8253,
                "active": True,
                "status": "active",
            },
        ]


def register_model(version, algorithm, metrics):
    try:
        import streamlit as st
    except ImportError:
        return

    if "model_registry" not in st.session_state:
        init_registry()
    for m in st.session_state.model_registry:
        m["active"] = False
    st.session_state.model_registry.append(
        {
            "version": version,
            "algorithm": algorithm,
            "accuracy": metrics.get("accuracy", 0),
            "active": True,
            "status": "active",
        }
    )


def get_active_model():
    try:
        import streamlit as st
    except ImportError:
        return None

    if "model_registry" not in st.session_state:
        init_registry()
    for m in st.session_state.model_registry:
        if m["active"]:
            return m
    return None


def list_models():
    try:
        import streamlit as st
    except ImportError:
        return []

    if "model_registry" not in st.session_state:
        init_registry()
    return st.session_state.model_registry
