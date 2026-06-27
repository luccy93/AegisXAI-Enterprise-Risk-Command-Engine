#!/usr/bin/env python3
"""
AEGIS-XAI Enterprise Churn Prediction Platform
Version 4.0.0 | Modular Architecture
"""

import streamlit as st
import time
from datetime import datetime

from aegisxai.config.settings import Settings as settings
from aegisxai.utils.logging import setup_logging
from aegisxai.utils.helpers import audit_log
from aegisxai.models.features import load_data
from aegisxai.models.registry import init_registry
from aegisxai.dashboards.pages import *
from aegisxai.dashboards.components import display_data_quality_report, export_full_report

logger = setup_logging(settings.LOG_LEVEL)

THEMES = {
    "Quantum Aurora": {
        "bg": "#020617", "surface": "#0F172A", "surface2": "#1E293B",
        "accent": "#2563EB", "neon": "#06B6D4", "success": "#10B981",
        "danger": "#EF4444", "warning": "#F59E0B", "text": "#F8FAFC",
        "text2": "#94A3B8", "border": "#1E293B",
        "glow": "0 0 20px rgba(37, 99, 235, 0.15)",
        "gradient": "linear-gradient(135deg, #2563EB, #06B6D4)"
    },
    "Cyber Command": {
        "bg": "#0A0A0A", "surface": "#1A1A1A", "surface2": "#2A2A2A",
        "accent": "#00FF41", "neon": "#00FF41", "success": "#00FF41",
        "danger": "#FF0040", "warning": "#FFD700", "text": "#00FF41",
        "text2": "#008F28", "border": "#2A2A2A",
        "glow": "0 0 15px rgba(0, 255, 65, 0.2)",
        "gradient": "linear-gradient(135deg, #00FF41, #008F28)"
    },
    "Neo Corporate": {
        "bg": "#FFFFFF", "surface": "#F8F9FA", "surface2": "#E9ECEF",
        "accent": "#4361EE", "neon": "#4361EE", "success": "#2EC4B6",
        "danger": "#E63946", "warning": "#F4A261", "text": "#212529",
        "text2": "#6C757D", "border": "#DEE2E6",
        "glow": "0 0 20px rgba(67, 97, 238, 0.1)",
        "gradient": "linear-gradient(135deg, #4361EE, #3A0CA3)"
    },
    "Dark Glass": {
        "bg": "#0D1117", "surface": "#161B22", "surface2": "#21262D",
        "accent": "#58A6FF", "neon": "#58A6FF", "success": "#3FB950",
        "danger": "#F85149", "warning": "#D29922", "text": "#C9D1D9",
        "text2": "#8B949E", "border": "#30363D",
        "glow": "0 0 20px rgba(88, 166, 255, 0.1)",
        "gradient": "linear-gradient(135deg, #58A6FF, #1F6FEB)"
    },
    "Holographic Blue": {
        "bg": "#0A0E27", "surface": "#12163A", "surface2": "#1A1F4E",
        "accent": "#00D4FF", "neon": "#00D4FF", "success": "#00E5A0",
        "danger": "#FF3366", "warning": "#FFB800", "text": "#E8EAF6",
        "text2": "#9FA8DA", "border": "#1A1F4E",
        "glow": "0 0 25px rgba(0, 212, 255, 0.15)",
        "gradient": "linear-gradient(135deg, #00D4FF, #7C4DFF)"
    }
}


def get_css(C):
    return f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        * {{ font-family: 'Inter', sans-serif; box-sizing: border-box; }}
        .stApp {{ background: {C["bg"]} !important; }}
        h1, h2, h3, h4, h5, h6, p, span, div, label {{ color: {C["text"]} !important; }}
        .stButton>button {{
            background: {C["gradient"]} !important; color: white !important;
            border: none !important; border-radius: 8px !important;
            padding: 8px 20px !important; font-weight: 500 !important;
            box-shadow: {C["glow"]} !important;
            transition: all 0.3s !important;
        }}
        .stButton>button:hover {{ transform: translateY(-2px); box-shadow: 0 0 30px rgba(37,99,235,0.3) !important; }}
        .stSelectbox>div>div {{ background: {C["surface"]} !important; color: {C["text"]} !important; border: 1px solid {C["border"]} !important; }}
        .stSlider>div>div {{ color: {C["accent"]} !important; }}
        .stDataFrame {{ background: {C["surface"]} !important; border-radius: 12px !important; }}
        div[data-testid="stMetricValue"] {{ color: {C["neon"]} !important; font-size: 28px !important; font-weight: 700 !important; }}
        div[data-testid="stMetricDelta"] {{ color: {C["text2"]} !important; }}
        .glow-card {{
            background: {C["surface"]}; border: 1px solid {C["border"]};
            border-radius: 16px; padding: 24px;
            box-shadow: {C["glow"]}; backdrop-filter: blur(10px);
        }}
        .glow-card:hover {{ border-color: {C["accent"]}; }}
        .glass {{
            background: rgba(255,255,255,0.03); backdrop-filter: blur(20px);
            border: 1px solid rgba(255,255,255,0.06); border-radius: 16px;
            padding: 20px;
        }}
        .pulse-dot {{
            width: 8px; height: 8px; background: {C["success"]};
            border-radius: 50%; display: inline-block;
            animation: pulse 2s infinite;
        }}
        @keyframes pulse {{ 0% {{ opacity: 1; transform: scale(1); }} 50% {{ opacity: 0.5; transform: scale(1.3); }} 100% {{ opacity: 1; transform: scale(1); }} }}
        .header-bar {{
            position: fixed; top: 0; left: 0; right: 0; z-index: 1000;
            background: rgba(15,23,42,0.92); backdrop-filter: blur(20px);
            border-bottom: 1px solid {C["border"]}; padding: 8px 24px;
            display: flex; align-items: center; justify-content: space-between;
        }}
        .badge {{
            padding: 2px 10px; border-radius: 20px; font-size: 11px; font-weight: 600;
            background: {C["accent"]}; color: white;
        }}
        .kpi-card {{
            background: {C["surface"]}; border: 1px solid {C["border"]};
            border-radius: 12px; padding: 16px; text-align: center;
        }}
        .kpi-value {{ font-size: 32px; font-weight: 800; color: {C["neon"]}; }}
        .kpi-label {{ font-size: 13px; color: {C["text2"]}; margin-top: 4px; }}
        .sidebar-section {{ padding: 8px 0; }}
        .nav-item {{
            padding: 10px 16px; margin: 2px 0; border-radius: 8px;
            cursor: pointer; transition: all 0.2s;
            color: {C["text"]}; font-size: 14px;
        }}
        .nav-item:hover {{ background: {C["surface2"]}; color: {C["accent"]}; }}
        .nav-item.active {{ background: {C["accent"]}; color: white !important; }}
        ::-webkit-scrollbar {{ width: 6px; }}
        ::-webkit-scrollbar-track {{ background: {C["bg"]}; }}
        ::-webkit-scrollbar-thumb {{ background: {C["surface2"]}; border-radius: 3px; }}
        ::-webkit-scrollbar-thumb:hover {{ background: {C["accent"]}; }}
        hr {{ border-color: {C["border"]} !important; }}
        .st-dx {{ background: {C["surface"]} !important; color: {C["text"]} !important; }}
        .st-e5 {{ background: {C["surface"]} !important; }}
        .shortcut-hint {{ position:fixed;bottom:16px;right:16px;z-index:9999;background:{C["surface"]};border:1px solid {C["border"]};border-radius:12px;padding:12px 16px;font-size:12px;color:{C["text2"]};box-shadow:{C["glow"]}; }}
        .ticket-card {{ background:{C["surface"]};border:1px solid {C["border"]};border-radius:12px;padding:16px;margin:8px 0; }}
        .ticket-card:hover {{ border-color:{C["accent"]}; }}
        .stage-column {{ background:{C["surface2"]};border-radius:12px;padding:12px;min-height:200px; }}
    </style>
    <script>
    document.addEventListener('keydown', function(e) {{
        if (e.ctrlKey || e.metaKey) {{
            var key = e.key.toLowerCase();
            var map = {{'d':'Dashboard','e':'Executive Intelligence','r':'Risk Queue','g':'Diagnostic Chamber',
                       's':'Scenario Simulation','m':'Model Monitoring','a':'Alert Center',
                       'c':'AI Copilot','o':'Root Cause Analysis','p':'Customer Segmentation',
                       'k':'Global Risk Map','f':'Forecasting','t':'Digital Twin','h':'Cohort Analysis',
                       'j':'Customer Journey','v':'Model Registry','b':'A/B Comparison',
                       'w':'Drift Monitor','i':'Incident Timeline','u':'Customer 360','l':'Audit Logs',
                       'n':'Live Monitor','y':'Reports','q':'Customer Similarity',
                       'z':'Ticketing Workflow','x':'Scheduled Reports'}};
            if (key === '/') {{ e.preventDefault(); document.getElementById('shortcut_cmd')?.focus(); }}
        }}
    }});
    </script>
    """


def init_session_state():
    defaults = {
        "authenticated": False, "page": "Dashboard", "user_role": "Viewer",
        "username": "", "theme": "Quantum Aurora", "login_time": None,
        "notification_count": 3, "session_timer_start": time.time(),
        "mfa_verified": False, "mfa_code": "", "alerts": [],
        "cases": [], "campaigns": [], "events": [],
        "audit_logs": [], "risk_filters": {}, "model_registry": [],
        "show_sidebar": True, "tickets": [], "scheduled_reports": [],
        "similarity_results": None, "last_customer": None,
        "shortcut_help": False
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
    if not st.session_state.model_registry:
        st.session_state.model_registry = [
            {"version": "v4.0.0", "date": "2025-06-15", "algorithm": "XGBoost+Optuna", "roc_auc": 0.847, "status": "Active"},
            {"version": "v3.2.1", "date": "2025-03-10", "algorithm": "XGBoost", "roc_auc": 0.831, "status": "Staging"},
            {"version": "v3.1.0", "date": "2025-01-22", "algorithm": "RandomForest", "roc_auc": 0.812, "status": "Archived"},
            {"version": "v3.0.0", "date": "2024-11-05", "algorithm": "LogisticRegression", "roc_auc": 0.789, "status": "Archived"},
            {"version": "v2.1.0", "date": "2024-08-18", "algorithm": "XGBoost", "roc_auc": 0.805, "status": "Deprecated"}
        ]


def show_login():
    C = THEMES[st.session_state.theme]
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""<div style="text-align:center;padding:40px 0;">
            <h1 style="font-size:52px;font-weight:800;background:{C["gradient"]};-webkit-background-clip:text;-webkit-text-fill-color:transparent;">AEGIS-XAI</h1>
            <p style="color:{C["text2"]};font-size:16px;">Enterprise Churn Prediction Platform v4.0</p>
        </div>""", unsafe_allow_html=True)
        with st.form("login_form"):
            st.text_input("Username", key="login_user")
            st.text_input("Password", type="password", key="login_pass")
            col_a, col_b = st.columns(2)
            with col_a:
                st.selectbox("Role", ["Admin","Analyst","Manager","Viewer"], key="login_role")
            with col_b:
                st.selectbox("Theme", list(THEMES.keys()), key="login_theme")
            if st.form_submit_button("Sign In", use_container_width=True):
                st.session_state.authenticated = True
                st.session_state.username = st.session_state.login_user or "admin"
                st.session_state.user_role = st.session_state.login_role
                st.session_state.theme = st.session_state.login_theme
                st.session_state.mfa_verified = True
                st.session_state.login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state.session_timer_start = time.time()
                audit_log("LOGIN", f"User {st.session_state.username} logged in as {st.session_state.user_role}", st.session_state.username)
                st.rerun()
        st.markdown(f"""<div style="text-align:center;margin-top:16px;">
            <p style="color:{C["text2"]};font-size:12px;">MFA: Code <b style="color:{C["accent"]};">123456</b> would be required in production</p>
        </div>""", unsafe_allow_html=True)


NAV_ITEMS = [
    ("Dashboard", "dashboard"),
    ("Executive Intelligence", "insights"),
    ("Risk Queue", "risk"),
    ("Diagnostic Chamber", "diagnostic"),
    ("Scenario Simulation", "scenario"),
    ("Model Monitoring", "monitor"),
    ("Alert Center", "alerts"),
    ("AI Copilot", "copilot"),
    ("Root Cause Analysis", "rootcause"),
    ("Customer Segmentation", "segmentation"),
    ("Global Risk Map", "riskmap"),
    ("Forecasting", "forecast"),
    ("Digital Twin", "digitaltwin"),
    ("Cohort Analysis", "cohort"),
    ("Customer Journey", "journey"),
    ("Model Registry", "registry"),
    ("A/B Comparison", "abtest"),
    ("Drift Monitor", "drift"),
    ("Case Management", "cases"),
    ("Campaign Manager", "campaigns"),
    ("Incident Timeline", "incidents"),
    ("Customer 360", "c360"),
    ("Audit Logs", "audit"),
    ("Live Monitor", "live"),
    ("Reports", "reports"),
    ("Customer Similarity", "similarity"),
    ("Ticketing Workflow", "tickets"),
    ("Scheduled Reports", "schedreports"),
    ("Settings", "settings")
]


def show_header():
    C = THEMES[st.session_state.theme]
    elapsed = int(time.time() - st.session_state.session_timer_start)
    m, s = divmod(elapsed, 60)
    h, m = divmod(m, 60)
    timer_str = f"{h:02d}:{m:02d}:{s:02d}"
    role_badge = {"Admin":"#EF4444","Analyst":"#3B82F6","Manager":"#F59E0B","Viewer":"#6B7280"}
    role_color = role_badge.get(st.session_state.user_role, "#6B7280")
    st.markdown(f"""
    <div style="position:fixed;top:0;left:0;right:0;z-index:9999;background:rgba(15,23,42,0.95);backdrop-filter:blur(20px);border-bottom:1px solid {C["border"]};padding:6px 20px;">
        <div style="display:flex;align-items:center;justify-content:space-between;max-width:100%;">
            <div style="display:flex;align-items:center;gap:12px;">
                <span style="font-size:20px;font-weight:800;background:{C["gradient"]};-webkit-background-clip:text;-webkit-text-fill-color:transparent;">AEGIS</span>
                <span class="pulse-dot"></span>
                <span style="font-size:11px;color:{C["success"]};font-weight:500;">AI CORE ACTIVE</span>
            </div>
            <div style="display:flex;align-items:center;gap:20px;">
                <span style="font-size:12px;color:{C["text2"]};">{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</span>
                <span style="font-size:12px;color:{C["text2"]};">? {timer_str}</span>
                <span style="position:relative;font-size:18px;">??
                    <span style="position:absolute;top:-6px;right:-8px;background:{C["danger"]};color:white;font-size:10px;padding:1px 5px;border-radius:10px;font-weight:700;">{st.session_state.notification_count}</span>
                </span>
                <span style="font-size:13px;color:{C["text"]};">{st.session_state.username}</span>
                <span style="background:{role_color};color:white;padding:2px 10px;border-radius:20px;font-size:11px;font-weight:600;">{st.session_state.user_role}</span>
            </div>
        </div>
    </div>
    <div style="height:52px;"></div>
    """, unsafe_allow_html=True)


def show_sidebar():
    C = THEMES[st.session_state.theme]
    with st.sidebar:
        st.markdown(f"""<div style="padding:8px 0 16px;">
            <h3 style="font-size:13px;color:{C["text2"]};text-transform:uppercase;letter-spacing:1px;">Navigation</h3>
        </div>""", unsafe_allow_html=True)
        for label, key in NAV_ITEMS:
            if st.button(label, key=f"nav_{key}", use_container_width=True,
                         type="secondary" if st.session_state.page != label else "primary"):
                st.session_state.page = label
                audit_log("NAVIGATION", f"Navigated to {label}", st.session_state.username)
                st.rerun()
        st.markdown(f"""<hr style="border-color:{C["border"]};margin:16px 0;">""", unsafe_allow_html=True)
        cmd = st.text_input("?? Cmd+/? ", placeholder="Type /d, /r, /a...", key="shortcut_cmd", label_visibility="collapsed")
        if cmd:
            shortcut_map = {
                "/d":"Dashboard","/e":"Executive Intelligence","/r":"Risk Queue","/g":"Diagnostic Chamber",
                "/s":"Scenario Simulation","/m":"Model Monitoring","/a":"Alert Center","/c":"AI Copilot",
                "/o":"Root Cause Analysis","/p":"Customer Segmentation","/k":"Global Risk Map","/f":"Forecasting",
                "/t":"Digital Twin","/h":"Cohort Analysis","/j":"Customer Journey","/v":"Model Registry",
                "/b":"A/B Comparison","/w":"Drift Monitor","/i":"Incident Timeline","/u":"Customer 360",
                "/l":"Audit Logs","/n":"Live Monitor","/y":"Reports","/q":"Customer Similarity",
                "/z":"Ticketing Workflow","/x":"Scheduled Reports"
            }
            if cmd in shortcut_map:
                st.session_state.page = shortcut_map[cmd]
                st.session_state.shortcut_cmd = ""
                audit_log("SHORTCUT", f"Navigated to {shortcut_map[cmd]} via keyboard shortcut", st.session_state.username)
                st.rerun()
        if st.button("?? Shortcuts", key="shortcut_help_btn", use_container_width=True):
            st.session_state.shortcut_help = not st.session_state.shortcut_help
        if st.session_state.shortcut_help:
            shortcut_help_html = f"""<div class="glass" style="padding:12px;margin:8px 0;font-size:11px;">
                <div style="font-weight:600;color:{C["text"]};margin-bottom:8px;">Keyboard Shortcuts</div>
                <table style="width:100%;color:{C["text2"]};">
                <tr><td>Ctrl+D</td><td>Dashboard</td></tr>
                <tr><td>Ctrl+E</td><td>Executive Intel</td></tr>
                <tr><td>Ctrl+R</td><td>Risk Queue</td></tr>
                <tr><td>Ctrl+G</td><td>Diagnostic</td></tr>
                <tr><td>Ctrl+S</td><td>Scenario Sim</td></tr>
                <tr><td>Ctrl+M</td><td>Model Monitor</td></tr>
                <tr><td>Ctrl+A</td><td>Alert Center</td></tr>
                <tr><td>Ctrl+C</td><td>AI Copilot</td></tr>
                <tr><td>Ctrl+O</td><td>Root Cause</td></tr>
                <tr><td>Ctrl+P</td><td>Segmentation</td></tr>
                <tr><td>Ctrl+K</td><td>Risk Map</td></tr>
                <tr><td>Ctrl+F</td><td>Forecasting</td></tr>
                <tr><td>Ctrl+/</td><td>Command Palette</td></tr>
                </table>
            </div>"""
            st.markdown(shortcut_help_html, unsafe_allow_html=True)
        st.markdown(f"""<div style="padding:8px 0;">
            <p style="font-size:11px;color:{C["text2"]};">
                AEGIS-XAI v4.0.0<br>
                &copy; 2025 Aegis Intelligence<br>
                Session: {st.session_state.username} | {st.session_state.user_role}
            </p>
        </div>""", unsafe_allow_html=True)


PAGE_FUNCTIONS = {
    "Dashboard": page_dashboard,
    "Executive Intelligence": page_executive_intelligence,
    "Risk Queue": page_risk_queue,
    "Diagnostic Chamber": page_diagnostic,
    "Scenario Simulation": page_scenario,
    "Model Monitoring": page_model_monitoring,
    "Alert Center": page_alert_center,
    "Reports": page_reports,
    "Settings": page_settings,
    "AI Copilot": page_ai_copilot,
    "Root Cause Analysis": page_root_cause,
    "Customer Segmentation": page_customer_segmentation,
    "Global Risk Map": page_global_risk_map,
    "Forecasting": page_forecasting,
    "Digital Twin": page_digital_twin,
    "Cohort Analysis": page_cohort_analysis,
    "Customer Journey": page_customer_journey,
    "Model Registry": page_model_registry,
    "A/B Comparison": page_ab_comparison,
    "Drift Monitor": page_drift_monitor,
    "Case Management": page_case_management,
    "Campaign Manager": page_campaign_manager,
    "Incident Timeline": page_incident_timeline,
    "Customer 360": page_customer_360,
    "Audit Logs": page_audit_logs,
    "Live Monitor": page_live_monitor,
    "Customer Similarity": page_customer_similarity,
    "Ticketing Workflow": page_ticketing_workflow,
    "Scheduled Reports": page_scheduled_reports
}


def main():
    st.set_page_config(page_title="AEGIS-XAI v4.0", page_icon="\u26a1", layout="wide", initial_sidebar_state="collapsed")
    init_session_state()
    C = THEMES[st.session_state.theme]
    st.markdown(get_css(C), unsafe_allow_html=True)
    if not st.session_state.authenticated:
        show_login()
        return
    show_header()
    show_sidebar()
    page_func = PAGE_FUNCTIONS.get(st.session_state.page)
    if page_func:
        page_func()
    else:
        page_dashboard()


if __name__ == "__main__":
    main()
