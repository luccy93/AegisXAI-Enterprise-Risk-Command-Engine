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
from aegisxai.dashboards.cx_pages import *
from aegisxai.dashboards.enterprise_pages import *
from aegisxai.dashboards.ai_pages import AI_PAGE_FUNCTIONS
from aegisxai.dashboards.ops_pages import OPS_PAGE_FUNCTIONS
from aegisxai.dashboards.biz_pages import BIZ_PAGE_FUNCTIONS
from aegisxai.dashboards.corp_pages import CORP_PAGE_FUNCTIONS
from aegisxai.dashboards.premium_dashboards import PREMIUM_PAGE_FUNCTIONS
from aegisxai.dashboards.ux_pages import UX_PAGE_FUNCTIONS
from aegisxai.services.premium_ux import *

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
        @keyframes holographicRotate {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
        @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
        @keyframes float {{ 0% {{ transform: translateY(0px); }} 50% {{ transform: translateY(-6px); }} 100% {{ transform: translateY(0px); }} }}
        .holographic {{ position:relative; overflow:hidden; animation: float 3s ease-in-out infinite; }}
        .holographic::before {{ content:''; position:absolute; top:-50%;left:-50%;width:200%;height:200%;
            background:conic-gradient(from 0deg, transparent, rgba(255,255,255,0.03), transparent, rgba(255,255,255,0.03), transparent);
            animation: holographicRotate 6s linear infinite; }}
        /* Welcome Screen */
        .welcome-container {{ display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:90vh;text-align:center; }}
        .welcome-title {{ font-size:48px;font-weight:800;background:{C["gradient"]};-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px; }}
        .welcome-subtitle {{ font-size:16px;color:{C["text2"]};margin-bottom:32px; }}
        .boot-line {{ font-size:14px;font-family:monospace;margin:4px 0; }}
        .boot-done {{ color:{C["success"]}; }} .boot-pending {{ color:{C["text2"]}; }} .boot-active {{ color:{C["accent"]}; }}
        .particle-canvas {{ position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none; }}
        /* Status Bar */
        .status-bar {{ position:fixed;bottom:0;left:0;right:0;z-index:9998;background:rgba(15,23,42,0.95);backdrop-filter:blur(12px);
            border-top:1px solid {C["border"]};padding:4px 20px;display:flex;justify-content:space-between;align-items:center;font-size:11px; }}
        .status-item {{ display:flex;align-items:center;gap:6px;color:{C["text2"]}; }}
        .status-dot {{ width:6px;height:6px;border-radius:50%;display:inline-block; }}
        /* Notification Panel */
        .notif-panel {{ position:fixed;top:52px;right:0;width:360px;bottom:32px;z-index:9997;background:rgba(15,23,42,0.97);backdrop-filter:blur(20px);
            border-left:1px solid {C["border"]};padding:16px;overflow-y:auto;transform:translateX(100%);transition:transform 0.3s; }}
        .notif-panel.open {{ transform:translateX(0); }}
        .notif-category {{ font-size:11px;color:{C["text2"]};text-transform:uppercase;letter-spacing:1px;margin:12px 0 6px; }}
        .notif-item {{ padding:8px 10px;margin:2px 0;border-radius:8px;font-size:12px;cursor:pointer; }}
        .notif-item:hover {{ background:{C["surface2"]}; }}
        /* Quick Actions Dock */
        .quick-dock {{ position:fixed;bottom:40px;right:20px;z-index:9999;display:flex;flex-direction:column;gap:6px; }}
        .quick-btn {{ width:44px;height:44px;border-radius:50%;border:1px solid {C["border"]};background:rgba(15,23,42,0.9);backdrop-filter:blur(12px);
            color:{C["text"]};display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:18px;transition:all 0.2s;box-shadow:0 4px 12px rgba(0,0,0,0.3); }}
        .quick-btn:hover {{ border-color:{C["accent"]};transform:scale(1.1);box-shadow:0 0 20px rgba(37,99,235,0.3); }}
        /* Command Palette */
        .cmd-overlay {{ position:fixed;top:0;left:0;right:0;bottom:0;z-index:10000;background:rgba(0,0,0,0.6);display:flex;align-items:flex-start;justify-content:center;padding-top:80px; }}
        .cmd-modal {{ width:560px;background:{C["surface"]};border:1px solid {C["border"]};border-radius:16px;overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,0.5); }}
        .cmd-input {{ width:100%;padding:16px 20px;background:{C["surface2"]};border:none;color:{C["text"]};font-size:16px;outline:none; }}
        .cmd-input:focus {{ outline:none; }}
        .cmd-results {{ max-height:300px;overflow-y:auto; }}
        .cmd-item {{ padding:10px 20px;display:flex;justify-content:space-between;cursor:pointer;font-size:14px; }}
        .cmd-item:hover {{ background:{C["surface2"]}; }}
        .cmd-shortcut {{ font-size:11px;color:{C["text2"]};background:{C["bg"]};padding:2px 8px;border-radius:4px; }}
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
        "shortcut_help": False, "mobile_layout": False,
        "show_welcome": True, "notif_open": False, "cmd_palette": False,
        "report_builder_cards": [], "slack_webhooks": []
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
    ("Customer Experience", "cx"),
    ("Sentiment & NPS", "sentiment"),
    ("Service Quality", "svcquality"),
    ("VOC Analytics", "voc"),
    ("Loyalty & Engagement", "loyalty"),
    ("CLV Dashboard", "clv"),
    ("Anomaly Detection", "anomaly"),
    ("Integration Hub", "integration"),
    ("Pipeline Monitor", "pipeline"),
    ("Compliance", "compliance"),
    ("Executive Reports", "exec_reports"),
    ("Alert Webhooks", "alert_webhooks"),
    ("Model Explainability", "model_explain"),
    ("--- AI & Intelligence ---", None),
    ("AI Executive Copilot", "ai_copilot"),
    ("Business Forecasting", "biz_forecast"),
    ("Retention Agent", "retention_agent"),
    ("Recommendation Engine", "rec_engine"),
    ("--- Operations ---", None),
    ("Global Operations Center", "global_ops"),
    ("Enterprise Digital Twin", "ent_digital_twin"),
    ("Network Graph", "network_graph"),
    ("Streaming Analytics", "streaming"),
    ("--- Business ---", None),
    ("Revenue Intelligence", "rev_intel"),
    ("Hyper-Personalization", "hyper_pers"),
    ("Team Performance", "team_perf"),
    ("Gamification", "gamification"),
    ("--- Enterprise ---", None),
    ("Governance Center", "governance"),
    ("Knowledge Management", "knowledge"),
    ("Advanced Search", "search"),
    ("Experimentation Lab", "experiment"),
    ("Innovation Lab", "innovation"),
    ("Voice Analytics", "voice"),
    ("ESG Dashboard", "esg"),
    ("Mobile Companion", "mobile"),
    ("--- Premium Suite ---", None),
    ("Executive Command", "exec_cmd"),
    ("AI Command Center", "ai_cmd"),
    ("Global Risk Intel", "global_risk"),
    ("Revenue Intel Premium", "rev_prem"),
    ("CX Intel Premium", "cx_prem"),
    ("Segmentation Premium", "seg_prem"),
    ("Journey Premium", "journey_prem"),
    ("Voice of Customer", "voc_prem"),
    ("XAI Diagnostic v2", "xai_v2"),
    ("AI Copilot Premium", "copilot_prem"),
    ("Scenario Lab v2", "scenario_v2"),
    ("Live Ops Center", "live_ops"),
    ("Alert Management", "alert_mgmt"),
    ("Incident Management", "incident_mgmt"),
    ("Model Intel Center", "model_intel"),
    ("Drift Detection", "drift_detect"),
    ("Customer 360", "c360_prem"),
    ("Team Perf Premium", "team_prem"),
    ("Retention Campaigns", "retention_camp"),
    ("Security & Governance", "sec_gov"),
    ("Reporting Center", "report_center"),
    ("Premium Widgets", "premium_widgets"),
    ("--- UX Experience ---", None),
    ("Voice Commands", "voice_cmds"),
    ("Collaboration", "collab"),
    ("Calendar", "calendar"),
    ("Onboarding Tour", "onboarding"),
    ("Achievements", "achievements"),
    ("Digital Twin Workspace", "dtwin_ws"),
    ("Executive Brief", "exec_brief"),
    ("KPI Drill-Down", "kpi_drill"),
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
            if key is None:
                st.markdown(f"""<div style="font-size:10px;color:{C['text2']};text-transform:uppercase;letter-spacing:1px;margin:12px 0 4px;opacity:0.5;">{label.replace('---','').strip()}</div>""", unsafe_allow_html=True)
                continue
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
                "/z":"Ticketing Workflow","/x":"Scheduled Reports",
                "/cx":"Customer Experience","/sn":"Sentiment & NPS","/sq":"Service Quality",
                "/vo":"VOC Analytics",                "/lo":"Loyalty & Engagement",
                "/clv":"CLV Dashboard","/an":"Anomaly Detection","/ih":"Integration Hub",
                "/pm":"Pipeline Monitor",                "/cg":"Compliance",
                 "/er":"Executive Reports","/aw":"Alert Webhooks","/me":"Model Explainability",
                 "/ec":"Executive Command","/ac":"AI Command Center","/gr":"Global Risk Intel",
                 "/rp":"Revenue Intel Premium","/xp":"CX Intel Premium","/sp":"Segmentation Premium",
                 "/jp":"Journey Premium","/vc":"Voice of Customer","/xd":"XAI Diagnostic v2",
                 "/cp":"AI Copilot Premium","/sv":"Scenario Lab v2","/lv":"Live Ops Center",
                 "/am":"Alert Management","/im":"Incident Management","/mi":"Model Intel Center",
                 "/dd":"Drift Detection","/36":"Customer 360","/tp":"Team Perf Premium",
                 "/rc":"Retention Campaigns","/sg":"Security & Governance","/rpt":"Reporting Center",
                 "/pw":"Premium Widgets"
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
                <tr><td width="100">/cx</td><td>Customer Experience</td></tr>
                <tr><td>/sn</td><td>Sentiment & NPS</td></tr>
                <tr><td>/sq</td><td>Service Quality</td></tr>
                <tr><td>/vo</td><td>VOC Analytics</td></tr>
                <tr><td>/lo</td><td>Loyalty & Engagement</td></tr>
                <tr><td>/clv</td><td>CLV Dashboard</td></tr>
                <tr><td>/an</td><td>Anomaly Detection</td></tr>
                <tr><td>/ih</td><td>Integration Hub</td></tr>
                <tr><td>/pm</td><td>Pipeline Monitor</td></tr>
                <tr><td>/cg</td><td>Compliance</td></tr>
                <tr><td>/er</td><td>Executive Reports</td></tr>
                <tr><td>/aw</td><td>Alert Webhooks</td></tr>
                <tr><td>/me</td><td>Model Explainability</td></tr>
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
    "Scheduled Reports": page_scheduled_reports,
    "Customer Experience": page_cx_intelligence,
    "Sentiment & NPS": page_sentiment_nps,
    "Service Quality": page_service_quality,
    "VOC Analytics": page_voc_analytics,
    "Loyalty & Engagement": page_loyalty_engagement,
    "CLV Dashboard": page_clv_dashboard,
    "Anomaly Detection": page_anomaly_detection,
    "Integration Hub": page_integration_hub,
    "Pipeline Monitor": page_pipeline_monitor,
    "Compliance": page_compliance_dashboard,
    "Executive Reports": page_executive_report_builder,
    "Alert Webhooks": page_alert_webhooks,
    "Model Explainability": page_model_explainability_report,
    **AI_PAGE_FUNCTIONS, **OPS_PAGE_FUNCTIONS, **BIZ_PAGE_FUNCTIONS, **CORP_PAGE_FUNCTIONS,
    **PREMIUM_PAGE_FUNCTIONS, **UX_PAGE_FUNCTIONS
}


def show_welcome_screen():
    C = THEMES[st.session_state.theme]
    st.markdown(f"""<div class="welcome-container">
        <div class="welcome-title">&#9889; AEGIS-XAI v4.0</div>
        <div class="welcome-subtitle">Enterprise Churn Intelligence &bull; Operational Risk Command Engine</div>
    </div>""", unsafe_allow_html=True)
    boot_items = get_boot_sequence()
    cols = st.columns(3)
    for i, item in enumerate(boot_items):
        with cols[i % 3]:
            cls = "boot-done" if item["status"] == "done" else ("boot-active" if item["status"] == "active" else "boot-pending")
            icon = "&#10003;" if item["status"] == "done" else ("&#9889;" if item["status"] == "active" else "&#9632;")
            st.markdown(f'<div class="boot-line {cls}">{icon} {item["label"]}</div>', unsafe_allow_html=True)
    if st.button("Launch Platform", key="welcome_launch", type="primary", use_container_width=True):
        st.session_state.show_welcome = False
        st.rerun()


def show_status_bar():
    C = THEMES[st.session_state.theme]
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    user = st.session_state.get("username","User")
    role = st.session_state.get("role","viewer")
    model_health = st.session_state.get("model_health", get_model_health_status())
    status = get_system_status()
    st.markdown(f"""<div class="status-bar">
        <div class="status-item"><span class="status-dot" style="background:{C['success']}"></span> LIVE | {now}</div>
        <div class="status-item"><span class="status-dot" style="background:{C['success']}"></span> {user} [{role}]</div>
        <div class="status-item"><span class="status-dot" style="background:{C['success'] if model_health['accuracy']>0.8 else C['warning']}"></span> Model: {model_health['accuracy']:.1%} acc | Drift: {model_health['drift']:.1%}</div>
        <div class="status-item">{status['cpu']}% CPU | {status['memory']}% MEM | {status['sessions']} sessions</div>
    </div>""", unsafe_allow_html=True)


def show_notification_panel():
    C = THEMES[st.session_state.theme]
    open_class = " open" if st.session_state.get("notif_open", False) else ""
    notif_dict = get_notifications()
    alerts_df = get_alerts()
    st.markdown(f'<div class="notif-panel{open_class}" id="notif-panel">', unsafe_allow_html=True)
    st.markdown("### &#128276; Notifications")
    for category, items in notif_dict.items():
        st.markdown(f'<div class="notif-category">{category}</div>', unsafe_allow_html=True)
        for n in items:
            st.markdown(f'<div class="notif-item" style="border-left:3px solid {C[n["color"]]};">{n["icon"]} <strong>{n["title"]}</strong><br><span style="font-size:11px;color:{C["text2"]}">{n["time"]}</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="notif-category">Active Alerts</div>', unsafe_allow_html=True)
    for _, a in alerts_df.iterrows():
        sev_col = "error" if a["severity"] == "Critical" else ("warning" if a["severity"] == "High" else "success")
        st.markdown(f'<div class="notif-item" style="border-left:3px solid {C[sev_col]};">&#9888; <strong>{a["title"]}</strong><br><span style="font-size:11px;color:{C["text2"]}">{a["created"]}</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("&#10005; Close Panel", key="close_notif", help="Close notifications"):
        st.session_state.notif_open = False
        st.rerun()


def show_quick_actions_dock():
    st.markdown("""<div class="quick-dock">
        <button class="quick-btn" title="Quick Insights" onclick="alert('Quick Insights')">&#128200;</button>
        <button class="quick-btn" title="New Alert" onclick="alert('New Alert')">&#128276;</button>
        <button class="quick-btn" title="Scenario" onclick="alert('New Scenario')">&#128202;</button>
        <button class="quick-btn" title="Report" onclick="alert('Generate Report')">&#128196;</button>
        <button class="quick-btn" title="AI Assist" onclick="alert('AI Assistant')">&#129302;</button>
    </div>""", unsafe_allow_html=True)


def show_command_palette():
    if st.session_state.get("cmd_palette", False):
        C = THEMES[st.session_state.theme]
        st.markdown(f"""<div class="cmd-overlay" id="cmd-overlay">
            <div class="cmd-modal">
                <input class="cmd-input" id="cmd-input" placeholder="Type a command or page name... &#8984;K" autofocus/>
                <div class="cmd-results" id="cmd-results">
                    <div class="cmd-item"><span>&#127760; Change Theme</span><span class="cmd-shortcut">T</span></div>
                    <div class="cmd-item"><span>&#128269; Search Customers</span><span class="cmd-shortcut">S</span></div>
                    <div class="cmd-item"><span>&#128200; New Report</span><span class="cmd-shortcut">R</span></div>
                    <div class="cmd-item"><span>&#128276; View Alerts</span><span class="cmd-shortcut">A</span></div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)
        st.markdown("""<script>
            const overlay = document.getElementById('cmd-overlay');
            if(overlay) overlay.addEventListener('click', function(e) { if(e.target===this) document.getElementById('cmd-overlay').style.display='none'; });
        </script>""", unsafe_allow_html=True)


def show_sidebar_mini_widgets():
    C = THEMES[st.session_state.theme]
    with st.sidebar:
        st.markdown("---")
        col1, col2 = st.columns(2)
        alerts_df = get_alerts()
        active = (alerts_df["status"] == "New").sum() if not alerts_df.empty else 0
        col1.metric("Active Alerts", int(active), delta=0)
        col2.metric("Response Time", "1.2s", delta="-0.3s")
        col3, col4 = st.columns(2)
        col3.metric("Today's Predictions", "847", delta="+12")
        col4.metric("Churn Rate", "26.5%", delta="-1.2%")
        st.markdown("---")
        activities = get_activity_feed()
        st.markdown("### &#128340; Recent Activity")
        for act in activities[:5]:
            st.markdown(f'<div style="font-size:12px;padding:4px 0;border-bottom:1px solid {C["border"]};">{act["icon"]} {act["text"]}<br><span style="font-size:10px;color:{C["text2"]}">{act["time"]}</span></div>', unsafe_allow_html=True)


def show_enterprise_header():
    C = THEMES[st.session_state.theme]
    user = st.session_state.get("username","User")
    role = st.session_state.get("role","viewer")
    col1, col2, col3 = st.columns([1,3,1])
    with col1:
        st.markdown(f'<span style="font-size:22px;">&#9889;</span>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div style="text-align:center;"><span style="font-size:14px;color:{C["text2"]};">AEGIS-XAI &bull; {role.title()} Command Center</span></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div style="text-align:right;font-size:12px;color:{C["text2"]};">{user} | <span style="color:{C["accent"]};">{datetime.now().strftime("%H:%M")}</span></div>', unsafe_allow_html=True)
    st.markdown(f'<hr style="margin:4px 0;border-color:{C["border"]};">', unsafe_allow_html=True)


def main():
    st.set_page_config(page_title="AEGIS-XAI v4.0", page_icon="\u26a1", layout="wide", initial_sidebar_state="collapsed")
    init_session_state()
    C = THEMES[st.session_state.theme]
    st.markdown(get_css(C), unsafe_allow_html=True)
    if not st.session_state.authenticated:
        show_login()
        return
    if st.session_state.get("show_welcome", True):
        show_welcome_screen()
        return
    show_enterprise_header()
    show_sidebar()
    page_func = PAGE_FUNCTIONS.get(st.session_state.page)
    if page_func:
        page_func()
    else:
        page_dashboard()
    show_status_bar()
    show_notification_panel()
    show_quick_actions_dock()
    show_command_palette()
    show_sidebar_mini_widgets()


if __name__ == "__main__":
    main()
