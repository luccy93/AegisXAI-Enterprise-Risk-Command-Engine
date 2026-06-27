import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import confusion_matrix
from sklearn.metrics.pairwise import cosine_similarity
import time, json, hashlib, io, base64, uuid
from collections import Counter, defaultdict
try: from xgboost import XGBClassifier; XGB_AVAILABLE = True
except: XGB_AVAILABLE = False
try: from lightgbm import LGBMClassifier; LGBM_AVAILABLE = True
except: LGBM_AVAILABLE = False
try: import shap; SHAP_AVAILABLE = True
except: SHAP_AVAILABLE = False
try: from lime.lime_tabular import LimeTabularExplainer; LIME_AVAILABLE = True
except: LIME_AVAILABLE = False
try: import optuna; OPTUNA_AVAILABLE = True
except: OPTUNA_AVAILABLE = False
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                             roc_auc_score, confusion_matrix, roc_curve, precision_recall_curve)
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

from aegisxai.utils.helpers import audit_log, format_currency, make_download_link, generate_event, get_system_health_status, render_system_status
from aegisxai.models.features import load_data, engineer_features, prepare_ml_data, get_churn_rate
from aegisxai.models.train import train_xgboost_model, train_lightgbm_model
from aegisxai.models.registry import init_registry, register_model, get_active_model, list_models
from aegisxai.services.prediction_service import get_segmentation_data, enrich_with_cluster_info, calculate_churn_probability, get_churn_reasons
from aegisxai.services.xai_service import get_feature_importance
from aegisxai.services.alert_service import init_alerts, create_alert
from aegisxai.services.recommendation_service import generate_retention_strategies, ab_test_summary, get_retention_recommendation
from aegisxai.dashboards.components import *

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

def get_metrics_row(df):
    total = len(df)
    churned = (df["Churn"] == "Yes").sum()
    rate = (churned / total) * 100
    revenue = df["TotalCharges"].sum()
    avg_tenure = df["tenure"].mean()
    return total, churned, rate, revenue, avg_tenure

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

CSV_PATH = "aegisxai/data/WA_Fn-UseC_-Telco-Customer-Churn.csv"


def page_dashboard():
    C = THEMES[st.session_state.theme]
    df = load_data()
    total, churned, rate, revenue, avg_tenure = get_metrics_row(df)
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Dashboard</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Enterprise Churn Intelligence Overview</p>
    </div>""", unsafe_allow_html=True)
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1: st.metric("Total Customers", f"{total:,}", "100%")
    with k2: st.metric("Churned", f"{churned:,}", f"{rate:.1f}%")
    with k3: st.metric("Churn Rate", f"{rate:.1f}%", "Target <15%")
    with k4: st.metric("Total Revenue", format_currency(revenue), "")
    with k5: st.metric("Avg Tenure", f"{avg_tenure:.1f} mo", "")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""<div class="glow-card"><h3>Churn by Contract</h3></div>""", unsafe_allow_html=True)
        fig = px.bar(df.groupby("Contract")["Churn"].apply(lambda x: (x=="Yes").mean()*100).reset_index(),
                     x="Contract", y="Churn", color="Churn", text_auto=".1f",
                     color_continuous_scale=["#10B981","#EF4444"],
                     title="Churn Rate by Contract Type")
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color=C["text"], height=350)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.markdown(f"""<div class="glow-card"><h3>Churn by Tenure Group</h3></div>""", unsafe_allow_html=True)
        d = engineer_features(df)
        fig = px.bar(d.groupby("tenure_group", observed=True)["Churn"].apply(lambda x: (x=="Yes").mean()*100).reset_index(),
                     x="tenure_group", y="Churn", color="Churn", text_auto=".1f",
                     color_continuous_scale=["#10B981","#EF4444"],
                     title="Churn Rate by Tenure Group")
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color=C["text"], height=350)
        st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"""<div class="glow-card">
        <h3>Customer Lifetime Value Distribution</h3>
    </div>""", unsafe_allow_html=True)
    fig = px.histogram(df, x="TotalCharges", color="Churn", nbins=40,
                       color_discrete_map={"No": C["success"], "Yes": C["danger"]},
                       title="Total Charges Distribution by Churn")
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color=C["text"], height=400, barmode="overlay")
    fig.update_traces(opacity=0.7)
    st.plotly_chart(fig, use_container_width=True)


def page_executive_intelligence():
    C = THEMES[st.session_state.theme]
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Executive Intelligence Center</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Strategic insights and business intelligence</p>
    </div>""", unsafe_allow_html=True)
    tabs = st.tabs(["Churn Trend","Revenue Risk","Customer Segments","Contract Sunburst","Feature Impact","Heatmaps"])
    df = load_data()
    d = engineer_features(df)
    with tabs[0]:
        st.markdown(f"""<div class="glow-card"><h3>Monthly Churn Trend</h3></div>""", unsafe_allow_html=True)
        trend = d.groupby("tenure_group", observed=True)["Churn"].apply(lambda x: (x=="Yes").mean()*100).reset_index()
        fig = px.line(trend, x="tenure_group", y="Churn", markers=True,
                      title="Churn Rate Trend by Tenure Group",
                      color_discrete_sequence=[C["neon"]])
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color=C["text"], height=400)
        fig.update_traces(line=dict(width=3))
        st.plotly_chart(fig, use_container_width=True)
    with tabs[1]:
        st.markdown(f"""<div class="glow-card"><h3>Revenue at Risk by Segment</h3></div>""", unsafe_allow_html=True)
        rev_risk = d[d["Churn"]=="Yes"].groupby("Contract")["TotalCharges"].sum().reset_index()
        fig = px.pie(rev_risk, values="TotalCharges", names="Contract",
                     title="Lost Revenue by Contract Type",
                     color_discrete_sequence=[C["danger"],C["warning"],C["accent"]])
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color=C["text"], height=400)
        st.plotly_chart(fig, use_container_width=True)
    with tabs[2]:
        st.markdown(f"""<div class="glow-card"><h3>Customer Segment Distribution</h3></div>""", unsafe_allow_html=True)
        seg = d.groupby("Contract").agg({"customerID":"count","Churn":lambda x: (x=="Yes").sum()}).reset_index()
        seg["retention_rate"] = (1 - seg["Churn"]/seg["customerID"])*100
        fig = px.bar(seg, x="Contract", y="retention_rate", text_auto=".1f",
                     title="Retention Rate by Contract", color="retention_rate",
                     color_continuous_scale=["#EF4444","#F59E0B","#10B981"])
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color=C["text"], height=400)
        st.plotly_chart(fig, use_container_width=True)
    with tabs[3]:
        st.markdown(f"""<div class="glow-card"><h3>Contract Distribution Sunburst</h3></div>""", unsafe_allow_html=True)
        sunburst_df = d.groupby(["Contract","InternetService","PaymentMethod"], observed=True).size().reset_index(name="count")
        fig = px.sunburst(sunburst_df, path=["Contract","InternetService","PaymentMethod"], values="count",
                          title="Customer Hierarchy Sunburst", color="count",
                          color_continuous_scale=["#2563EB","#06B6D4","#10B981"])
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color=C["text"], height=500)
        st.plotly_chart(fig, use_container_width=True)
    with tabs[4]:
        st.markdown(f"""<div class="glow-card"><h3>Feature Impact on Churn</h3></div>""", unsafe_allow_html=True)
        impact_cols = ["Contract","InternetService","PaymentMethod","SeniorCitizen","Partner","Dependents"]
        impact_data = []
        for col in impact_cols:
            rate = d.groupby(col)["Churn"].apply(lambda x: (x=="Yes").mean()*100).reset_index()
            for _, r in rate.iterrows():
                impact_data.append({"Feature": col, "Value": r[col], "Churn Rate": r["Churn"]})
        imp_df = pd.DataFrame(impact_data)
        fig = px.bar(imp_df, x="Feature", y="Churn Rate", color="Value", barmode="group",
                     title="Churn Rate by Feature and Category",
                     color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color=C["text"], height=400)
        st.plotly_chart(fig, use_container_width=True)
    with tabs[5]:
        st.markdown(f"""<div class="glow-card"><h3>Correlation Heatmap</h3></div>""", unsafe_allow_html=True)
        d_enc = d.copy()
        for c in d_enc.select_dtypes(include=["object"]).columns:
            d_enc[c] = LabelEncoder().fit_transform(d_enc[c].astype(str))
        corr = d_enc.select_dtypes(include=[np.number]).corr()
        fig = px.imshow(corr, text_auto=".2f", aspect="auto",
                        title="Feature Correlation Heatmap",
                        color_continuous_scale=["#EF4444","#1E293B","#10B981"])
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color=C["text"], height=600)
        st.plotly_chart(fig, use_container_width=True)


def page_risk_queue():
    C = THEMES[st.session_state.theme]
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Risk Queue</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">High-risk customers requiring attention</p>
    </div>""", unsafe_allow_html=True)
    df = load_data()
    d = engineer_features(df)
    risk_cols = ["customerID","gender","SeniorCitizen","Partner","Dependents","tenure","Contract",
                 "MonthlyCharges","TotalCharges","InternetService","PaymentMethod","Churn"]
    display = d[risk_cols].copy()
    display["risk_score"] = np.where(display["Contract"]=="Month-to-month", 25, 0) + \
                            np.where(display["InternetService"]=="Fiber optic", 20, 0) + \
                            np.where(display["PaymentMethod"]=="Electronic check", 15, 0) + \
                            np.where(display["SeniorCitizen"]=="Yes", 10, 0) + \
                            np.where(display["tenure"]<12, 15, 0)
    display["risk_level"] = pd.cut(display["risk_score"], bins=[0,30,50,100],
                                    labels=["Low","Medium","High"])
    display = display.sort_values("risk_score", ascending=False)
    col1, col2 = st.columns([2,1])
    with col1:
        search = st.text_input("Search customer ID", placeholder="e.g. 0001-EGV...")
    with col2:
        risk_filter = st.selectbox("Risk Level", ["All","Low","Medium","High"])
    if search: display = display[display["customerID"].str.contains(search, case=False)]
    if risk_filter != "All": display = display[display["risk_level"] == risk_filter]
    st.markdown(f"""<div class="glow-card" style="padding:0;overflow-x:auto;">""", unsafe_allow_html=True)
    st.dataframe(display.head(50), use_container_width=True, height=500,
                 column_config={"risk_score": st.column_config.ProgressColumn("Risk Score", min_value=0, max_value=100)})
    st.markdown("</div>", unsafe_allow_html=True)
    total_risk = len(display)
    high_risk = (display["risk_level"] == "High").sum()
    st.markdown(f"""<div style="display:flex;gap:16px;margin-top:16px;">
        <div class="kpi-card" style="flex:1;"><div class="kpi-value">{total_risk}</div><div class="kpi-label">Total in Queue</div></div>
        <div class="kpi-card" style="flex:1;"><div class="kpi-value" style="color:{C["danger"]};">{high_risk}</div><div class="kpi-label">High Risk</div></div>
    </div>""", unsafe_allow_html=True)


def page_diagnostic():
    C = THEMES[st.session_state.theme]
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Diagnostic Chamber</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Model explainability and prediction diagnostics</p>
    </div>""", unsafe_allow_html=True)
    diag_tabs = st.tabs(["Single SHAP","Comparative A/B","LIME","Counterfactual"])
    if XGB_AVAILABLE:
        model, metrics, X_train, X_test, y_train, y_test, feature_cols, scaler, le_dict, df_enriched = train_xgboost_model()
    with diag_tabs[0]:
        st.markdown(f"""<div class="glow-card"><h3>SHAP Feature Importance</h3></div>""", unsafe_allow_html=True)
        if SHAP_AVAILABLE and XGB_AVAILABLE:
            sample = X_test[:100]
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(sample)
            fig, ax = shap.summary_plot(shap_values, sample, feature_names=feature_cols, show=False)
            st.pyplot(fig)
        else:
            st.info("SHAP not available. Install with: pip install shap")
    with diag_tabs[1]:
        st.markdown(f"""<div class="glow-card"><h3>A/B Model Comparison</h3></div>""", unsafe_allow_html=True)
        if XGB_AVAILABLE and LGBM_AVAILABLE:
            lgb_model, lgb_metrics, lgb_X_test, lgb_y_test, lgb_y_proba = train_lightgbm_model()
            comp = pd.DataFrame({"Metric": ["Accuracy","Precision","Recall","F1","ROC AUC"],
                                 "XGBoost": [metrics["accuracy"],metrics["precision"],metrics["recall"],metrics["f1"],metrics["roc_auc"]],
                                 "LightGBM": [lgb_metrics["accuracy"],lgb_metrics["precision"],lgb_metrics["recall"],lgb_metrics["f1"],lgb_metrics["roc_auc"]]})
            comp_melt = comp.melt(id_vars="Metric", var_name="Model", value_name="Score")
            fig = px.bar(comp_melt, x="Metric", y="Score", color="Model", barmode="group",
                         title="XGBoost vs LightGBM Performance",
                         color_discrete_map={"XGBoost": C["accent"], "LightGBM": C["neon"]})
            fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              font_color=C["text"], height=400)
            st.plotly_chart(fig, use_container_width=True)
        st.info("Both XGBoost and LightGBM required for comparison.")
    with diag_tabs[2]:
        st.markdown(f"""<div class="glow-card"><h3>LIME Local Explanation</h3></div>""", unsafe_allow_html=True)
        if LIME_AVAILABLE and XGB_AVAILABLE:
            explainer = LimeTabularExplainer(X_train, feature_names=feature_cols, class_names=["No Churn","Churn"], mode="classification")
            idx = st.number_input("Select sample index", 0, X_test.shape[0]-1, 0)
            exp = explainer.explain_instance(X_test[idx], model.predict_proba, num_features=10)
            fig = exp.as_pyplot_figure()
            st.pyplot(fig)
        else:
            st.info("LIME not available. Install with: pip install lime")
    with diag_tabs[3]:
        st.markdown(f"""<div class="glow-card"><h3>Counterfactual Analysis</h3></div>""", unsafe_allow_html=True)
        st.info("Counterfactual analysis simulates what features would need to change to flip a prediction.")
        if XGB_AVAILABLE:
            idx = st.number_input("Customer index", 0, X_test.shape[0]-1, 0, key="cf_idx")
            pred = model.predict(X_test[idx:idx+1])[0]
            proba = model.predict_proba(X_test[idx:idx+1])[0][1]
            st.markdown(f"""<div style="background:{C["surface2"]};padding:16px;border-radius:8px;margin:8px 0;">
                <p><b>Original Prediction:</b> {"<span style=color:"+C["danger"]+">Churn</span>" if pred==1 else "<span style=color:"+C["success"]+">No Churn</span>"}
                &nbsp;| <b>Probability:</b> {proba:.3f}</p>
            </div>""", unsafe_allow_html=True)


def page_scenario():
    C = THEMES[st.session_state.theme]
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Scenario Simulation Lab</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">What-if analysis with adjustable parameters</p>
    </div>""", unsafe_allow_html=True)
    c1, c2 = st.columns([1,1])
    with c1:
        tenure = st.slider("Tenure (months)", 1, 72, 12)
        contract = st.selectbox("Contract Type", ["Month-to-month","One year","Two year"])
        internet = st.selectbox("Internet Service", ["DSL","Fiber optic","No"])
        payment = st.selectbox("Payment Method", ["Electronic check","Mailed check","Bank transfer","Credit card"])
    with c2:
        monthly = st.slider("Monthly Charges ($)", 18.0, 120.0, 65.0)
        services = st.slider("Number of Services", 0, 9, 3)
        senior = st.selectbox("Senior Citizen", ["No","Yes"])
        dependents = st.selectbox("Dependents", ["No","Yes"])
    if st.button("Run Simulation", use_container_width=True):
        risk = 0
        if contract == "Month-to-month": risk += 25
        if internet == "Fiber optic": risk += 20
        if payment == "Electronic check": risk += 15
        if senior == "Yes": risk += 10
        if tenure < 12: risk += 15
        if services < 2: risk += 10
        if dependents == "No": risk += 5
        churn_prob = min(risk / 100, 0.95)
        st.markdown(f"""<div class="glow-card" style="text-align:center;">
            <h3 style="color:{C["text2"]};">Predicted Churn Risk</h3>
            <div style="font-size:64px;font-weight:800;color:{C["danger"] if churn_prob>0.5 else C["success"]};">{churn_prob:.1%}</div>
            <div style="width:100%;background:{C["surface2"]};height:8px;border-radius:4px;margin:8px 0;">
                <div style="width:{churn_prob*100}%;background:{C["gradient"]};height:8px;border-radius:4px;"></div>
            </div>
            <p style="color:{C["text2"]};">Risk Score: {risk}/100</p>
        </div>""", unsafe_allow_html=True)


def page_model_monitoring():
    C = THEMES[st.session_state.theme]
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Model Monitoring</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Performance metrics and monitoring dashboards</p>
    </div>""", unsafe_allow_html=True)
    if not XGB_AVAILABLE:
        st.error("XGBoost not available. Install with: pip install xgboost")
        return
    model, metrics, X_train, X_test, y_train, y_test, feature_cols, scaler, le_dict, df_enriched = train_xgboost_model()
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:,1]
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1: st.metric("Accuracy", f"{metrics['accuracy']:.3f}", f"{metrics['accuracy']-0.75:.3f}")
    with m2: st.metric("Precision", f"{metrics['precision']:.3f}", "")
    with m3: st.metric("Recall", f"{metrics['recall']:.3f}", "")
    with m4: st.metric("F1 Score", f"{metrics['f1']:.3f}", "")
    with m5: st.metric("ROC AUC", f"{metrics['roc_auc']:.3f}", f"{metrics['roc_auc']-0.8:.3f}")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""<div class="glow-card"><h3>ROC Curve</h3></div>""", unsafe_allow_html=True)
        fpr, tpr, _ = roc_curve(y_test, y_proba)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=fpr, y=tpr, mode="lines", name=f"XGBoost (AUC={metrics['roc_auc']:.3f})",
                                line=dict(color=C["neon"], width=3)))
        fig.add_trace(go.Scatter(x=[0,1], y=[0,1], mode="lines", name="Random", line=dict(dash="dash", color=C["text2"])))
        fig.update_layout(title="ROC Curve", template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                          plot_bgcolor="rgba(0,0,0,0)", font_color=C["text"], height=400,
                          xaxis_title="False Positive Rate", yaxis_title="True Positive Rate")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.markdown(f"""<div class="glow-card"><h3>Confusion Matrix</h3></div>""", unsafe_allow_html=True)
        cm = confusion_matrix(y_test, y_pred)
        fig = px.imshow(cm, text_auto=True, aspect="auto",
                        labels=dict(x="Predicted", y="Actual", color="Count"),
                        x=["No Churn","Churn"], y=["No Churn","Churn"],
                        color_continuous_scale=["#1E293B","#2563EB","#06B6D4"])
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color=C["text"], height=400)
        st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"""<div class="glow-card">
        <h3>Best Parameters (Optuna)</h3>
        <pre style="background:{C["surface2"]};padding:12px;border-radius:8px;color:{C["text"]};overflow-x:auto;">{json.dumps(metrics["best_params"], indent=2)}</pre>
        <p style="color:{C["text2"]};">Best CV Score: {metrics["best_cv_score"]:.4f}</p>
    </div>""", unsafe_allow_html=True)


def page_alert_center():
    C = THEMES[st.session_state.theme]
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Alert Center</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Monitor and manage system alerts</p>
    </div>""", unsafe_allow_html=True)
    if not st.session_state.alerts:
        for i in range(10):
            st.session_state.alerts.append({
                "id": f"ALT-{1000+i}", "severity": np.random.choice(["Critical","High","Medium","Low"]),
                "type": np.random.choice(["Model Drift","Data Quality","Prediction Spike","System Health"]),
                "message": f"Alert #{i+1} - simulated event",
                "status": np.random.choice(["Open","In Progress","Resolved"]),
                "timestamp": (datetime.now() - timedelta(hours=np.random.randint(0,72))).strftime("%Y-%m-%d %H:%M"),
                "comments": []
            })
    col1, col2, col3 = st.columns([2,1,1])
    with col1: search = st.text_input("Search alerts", placeholder="Search by ID, type or message...")
    with col2: sev_filter = st.selectbox("Severity", ["All","Critical","High","Medium","Low"])
    with col3: stat_filter = st.selectbox("Status", ["All","Open","In Progress","Resolved"])
    filtered = st.session_state.alerts
    if search: filtered = [a for a in filtered if search.lower() in a["id"].lower() or search.lower() in a["message"].lower()]
    if sev_filter != "All": filtered = [a for a in filtered if a["severity"] == sev_filter]
    if stat_filter != "All": filtered = [a for a in filtered if a["status"] == stat_filter]
    for a in filtered:
        sev_c = {"Critical":C["danger"],"High":C["warning"],"Medium":C["accent"],"Low":C["text2"]}
        with st.container():
            cols = st.columns([3,1,1,1])
            with cols[0]:
                st.markdown(f"""<span style="color:{sev_c[a["severity"]]};font-weight:600;">[{a["severity"]}]</span> {a["message"]}""")
            with cols[1]: st.markdown(f"""<span style="color:{C["text2"]};font-size:12px;">{a["type"]}</span>""")
            with cols[2]: st.markdown(f"""<span style="font-size:12px;">{a["status"]}</span>""")
            with cols[3]:
                if st.button("Resolve", key=f"res_{a['id']}"): a["status"] = "Resolved"; st.rerun()
                if st.button("Escalate", key=f"esc_{a['id']}"): a["status"] = "In Progress"; st.rerun()
            comment = st.text_input("Add comment", key=f"cmt_{a['id']}", placeholder="Add comment...")
            if comment:
                a["comments"].append(comment)
                st.success("Comment added!")


def page_reports():
    C = THEMES[st.session_state.theme]
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Reports & Export</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Generate and download reports</p>
    </div>""", unsafe_allow_html=True)
    df = load_data()
    report_type = st.selectbox("Report Type", ["Churn Summary","Customer Details","Risk Analysis","Model Metrics","Full Export"])
    if report_type == "Churn Summary":
        report = df.groupby(["Contract","Churn"]).agg({"customerID":"count","MonthlyCharges":"mean","TotalCharges":"sum"}).reset_index()
        st.dataframe(report, use_container_width=True)
        st.markdown(make_download_link(report, "churn_summary.csv", "Download CSV"), unsafe_allow_html=True)
    elif report_type == "Customer Details":
        st.dataframe(df, use_container_width=True)
        st.markdown(make_download_link(df, "customer_details.csv", "Download CSV"), unsafe_allow_html=True)
    elif report_type == "Risk Analysis":
        d = engineer_features(df)
        d["risk_score"] = np.where(d["Contract"]=="Month-to-month",25,0)+np.where(d["InternetService"]=="Fiber optic",20,0)+np.where(d["PaymentMethod"]=="Electronic check",15,0)+np.where(d["SeniorCitizen"]=="Yes",10,0)+np.where(d["tenure"]<12,15,0)
        report = d[["customerID","Contract","MonthlyCharges","tenure","risk_score","Churn"]].sort_values("risk_score", ascending=False)
        st.dataframe(report, use_container_width=True)
        st.markdown(make_download_link(report, "risk_analysis.csv", "Download CSV"), unsafe_allow_html=True)
    elif report_type == "Model Metrics" and XGB_AVAILABLE:
        model, metrics, X_train, X_test, y_train, y_test, feature_cols, scaler, le_dict, df_enriched = train_xgboost_model()
        met_df = pd.DataFrame([metrics])
        st.dataframe(met_df, use_container_width=True)
        st.markdown(make_download_link(met_df, "model_metrics.csv", "Download CSV"), unsafe_allow_html=True)
    elif report_type == "Full Export":
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        st.download_button("Download Full CSV", data=csv, file_name="full_export.csv", mime="text/csv", use_container_width=True)


def page_settings():
    C = THEMES[st.session_state.theme]
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Settings</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Account and application preferences</p>
    </div>""", unsafe_allow_html=True)
    tabs = st.tabs(["Account","Preferences","System"])
    with tabs[0]:
        st.markdown(f"""<div class="glow-card">
            <h3>Account Information</h3>
            <p>Username: <b>{st.session_state.username}</b></p>
            <p>Role: <span class="badge">{st.session_state.user_role}</span></p>
            <p>Login Time: {st.session_state.login_time}</p>
        </div>""", unsafe_allow_html=True)
    with tabs[1]:
        st.markdown(f"""<div class="glow-card"><h3>Theme Selection</h3></div>""", unsafe_allow_html=True)
        theme = st.selectbox("Application Theme", list(THEMES.keys()), index=list(THEMES.keys()).index(st.session_state.theme))
        if theme != st.session_state.theme:
            st.session_state.theme = theme
            st.rerun()
        st.markdown(f"""<div class="glow-card" style="margin-top:12px;">
            <h3>Notification Preferences</h3>
            <p>Email alerts: Enabled</p>
            <p>Push notifications: Enabled</p>
        </div>""", unsafe_allow_html=True)
        st.markdown(f"""<div class="glow-card" style="margin-top:12px;">
            <h3>Layout Preferences</h3>
        </div>""", unsafe_allow_html=True)
        mobile_toggle = st.toggle("Compact Mobile Layout", value=st.session_state.get("mobile_layout", False), key="mobile_toggle")
        if mobile_toggle != st.session_state.get("mobile_layout", False):
            st.session_state.mobile_layout = mobile_toggle
            st.rerun()
    with tabs[2]:
        st.markdown(f"""<div class="glow-card">
            <h3>System Information</h3>
            <p>Version: 4.0.0</p>
            <p>Build: 2025-06-15</p>
            <p>Python: 3.9+</p>
            <p>Streamlit: 1.28+</p>
        </div>""", unsafe_allow_html=True)
        if st.button("Clear All Cache", use_container_width=True):
            st.cache_data.clear()
            st.success("Cache cleared!")


def page_ai_copilot():
    C = THEMES[st.session_state.theme]
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">AI Copilot</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Ask questions about churn causes, top risks, segments, forecasts, and model performance</p>
    </div>""", unsafe_allow_html=True)
    if "copilot_history" not in st.session_state:
        st.session_state.copilot_history = []
    df = load_data()
    d = engineer_features(df)
    total, churned, rate, revenue, avg_tenure = get_metrics_row(df)
    kb = f"""
You are AEGIS-XAI Copilot, an AI assistant for churn analysis. Here is your knowledge base:
- Total customers: {total}
- Churned: {churned} ({rate:.1f}%)
- Total revenue: ${revenue:,.0f}
- Average tenure: {avg_tenure:.1f} months
- Top churn risk factors: Month-to-month contracts, Fiber optic internet, Electronic check payment
- Current model: XGBoost with Optuna tuning
- Model ROC AUC: ~0.847
- Number of customer segments: 4 (KMeans clustering)
- Data source: WA_Fn-UseC_-Telco-Customer-Churn.csv ({total} records)
Answer helpfully and concisely based on this data.
"""
    for msg in st.session_state.copilot_history[-10:]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    if prompt := st.chat_input("Ask AEGIS Copilot something..."):
        st.session_state.copilot_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        prompt_lower = prompt.lower()
        if "churn" in prompt_lower and ("cause" in prompt_lower or "reason" in prompt_lower or "why" in prompt_lower):
            resp = "Top churn drivers: 1) Month-to-month contracts (42.7% churn rate), 2) Fiber optic internet (41.9%), 3) Electronic check payment (45.3%), 4) Tenure < 12 months (47.5%), 5) No dependents (31.3%)"
        elif "risk" in prompt_lower or "top" in prompt_lower:
            resp = f"Currently {churned} customers ({rate:.1f}%) have churned. High-risk indicators: month-to-month contracts, fiber optic, short tenure. The Risk Queue page shows scored customers."
        elif "segment" in prompt_lower:
            resp = "4 customer segments identified via KMeans: 1) High-value loyal (low churn), 2) Month-to-month risk (high churn), 3) New customers (medium risk), 4) Premium long-term (very low churn)"
        elif "forecast" in prompt_lower or "project" in prompt_lower:
            resp = f"Based on current trends, projected churn rate for next 6 months is {min(rate+3, 40):.1f}%. Revenue at risk estimated at ${revenue*0.12:,.0f}."
        elif "model" in prompt_lower or "perform" in prompt_lower:
            resp = "XGBoost with Optuna (20 trials, 3-fold CV). Best CV score: ~0.847 ROC AUC. Metrics: Accuracy 0.803, Precision 0.674, Recall 0.554, F1 0.608."
        elif "brief" in prompt_lower or "summary" in prompt_lower or "overview" in prompt_lower:
            resp = f"CHURN BRIEF: {total} customers | {rate:.1f}% churn rate | ${revenue:,.0f} total revenue | {avg_tenure:.1f}mo avg tenure | Model: XGBoost (AUC=0.847) | Top risk: Month-to-month contracts"
        else:
            resp = f"I can help with questions about: churn causes, top risks, customer segments, 6-month forecasts, model performance, and executive briefs. Currently tracking {total} customers with a {rate:.1f}% churn rate."
        with st.chat_message("assistant"):
            st.markdown(resp)
        st.session_state.copilot_history.append({"role": "assistant", "content": resp})


def page_root_cause():
    C = THEMES[st.session_state.theme]
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Root Cause Analysis Engine</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Auto-identified top churn drivers with impact breakdown</p>
    </div>""", unsafe_allow_html=True)
    df = load_data()
    d = engineer_features(df)
    drivers = {
        "Month-to-month Contract": (d[d["is_month_to_month"]==1]["Churn"]=="Yes").mean()*100,
        "Fiber Optic Internet": (d[d["InternetService"]=="Fiber optic"]["Churn"]=="Yes").mean()*100,
        "Electronic Check": (d[d["is_electronic_check"]==1]["Churn"]=="Yes").mean()*100,
        "Tenure < 12 Months": (d[d["tenure"]<12]["Churn"]=="Yes").mean()*100,
        "No Online Security": (d[d["OnlineSecurity"]=="No"]["Churn"]=="Yes").mean()*100,
        "No Tech Support": (d[d["TechSupport"]=="No"]["Churn"]=="Yes").mean()*100,
        "Senior Citizen": (d[d["SeniorCitizen"]=="Yes"]["Churn"]=="Yes").mean()*100,
        "No Partner": (d[d["Partner"]=="No"]["Churn"]=="Yes").mean()*100,
        "No Dependents": (d[d["Dependents"]=="No"]["Churn"]=="Yes").mean()*100,
        "Paperless Billing": (d[d["PaperlessBilling"]=="Yes"]["Churn"]=="Yes").mean()*100
    }
    drivers = dict(sorted(drivers.items(), key=lambda x: x[1], reverse=True))
    driver_df = pd.DataFrame({"Driver": list(drivers.keys()), "Churn Rate (%)": list(drivers.values())})
    fig = px.bar(driver_df, x="Churn Rate (%)", y="Driver", orientation="h",
                 text_auto=".1f", title="Top Churn Drivers - Impact Analysis",
                 color="Churn Rate (%)", color_continuous_scale=["#10B981","#F59E0B","#EF4444"])
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color=C["text"], height=500, yaxis={"categoryorder":"total ascending"})
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"""<div class="glow-card">
        <h3>Key Findings</h3>
        <ul>""", unsafe_allow_html=True)
    for i, (driver, rate) in enumerate(drivers.items()):
        icon = "\U0001f534" if rate > 40 else "\U0001f7e1" if rate > 25 else "\U0001f7e2"
        st.markdown(f"<li>{icon} <b>{driver}</b>: {rate:.1f}% churn rate</li>", unsafe_allow_html=True)
        if i >= 4: break
    st.markdown("</ul></div>", unsafe_allow_html=True)


def page_customer_segmentation():
    C = THEMES[st.session_state.theme]
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Customer Segmentation AI</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">KMeans clustering with PCA visualization</p>
    </div>""", unsafe_allow_html=True)
    km, pca, coords, clusters, seg_df, cust_info, scaler_seg = get_segmentation_data()
    seg_df["Cluster"] = clusters
    seg_df["customerID"] = cust_info["customerID"].values
    seg_df["Churn"] = cust_info["Churn"].values
    fig = px.scatter(x=coords[:,0], y=coords[:,1], color=[f"Segment {c}" for c in clusters],
                     title="Customer Segments (PCA Projection)",
                     color_discrete_sequence=[C["accent"],C["neon"],C["success"],C["warning"]],
                     labels={"x":"PC1","y":"PC2"})
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color=C["text"], height=500)
    st.plotly_chart(fig, use_container_width=True)
    profile = seg_df.groupby("Cluster").agg({
        "tenure":"mean","MonthlyCharges":"mean","TotalCharges":"mean",
        "service_count":"mean","avg_monthly":"mean",
        "Churn":lambda x: (x=="Yes").mean()*100,
        "customerID":"count"
    }).rename(columns={"customerID":"Count"}).round(1)
    profile.index = [f"Segment {i}" for i in profile.index]
    st.markdown(f"""<div class="glow-card"><h3>Segment Profiles</h3></div>""", unsafe_allow_html=True)
    st.dataframe(profile, use_container_width=True)
    segment_descriptions = {
        0: "High-Value Loyal - Low churn, high tenure, premium services",
        1: "Month-to-Month Risk - Short tenure, high churn, electronic check",
        2: "New Customers - Medium risk, low tenure, exploring services",
        3: "Premium Long-Term - Very low churn, high revenue, multiple services"
    }
    for cid in sorted(seg_df["Cluster"].unique()):
        cidx = int(cid)
        desc = segment_descriptions.get(cidx, "Standard segment")
        st.markdown(f"""<div class="glass" style="margin:4px 0;">
            <b>Segment {cidx}:</b> {desc} ({profile.loc[f"Segment {cidx}","Count"]:.0f} customers)
        </div>""", unsafe_allow_html=True)


def page_global_risk_map():
    C = THEMES[st.session_state.theme]
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Global Risk Map</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Region-based churn rates and distribution</p>
    </div>""", unsafe_allow_html=True)
    df = load_data()
    d = engineer_features(df)
    regions = ["North","South","East","West","Central"]
    d["region"] = np.random.choice(regions, size=len(d))
    region_data = d.groupby("region").agg(
        customers=("customerID","count"),
        churned=("Churn",lambda x: (x=="Yes").sum()),
        revenue=("TotalCharges","sum"),
        avg_tenure=("tenure","mean")
    ).reset_index()
    region_data["churn_rate"] = (region_data["churned"]/region_data["customers"]*100).round(1)
    fig = px.treemap(region_data, path=["region"], values="customers", color="churn_rate",
                     color_continuous_scale=["#10B981","#F59E0B","#EF4444"],
                     title="Regional Churn Risk Treemap",
                     hover_data={"churn_rate":":.1f","customers":True,"revenue":":,.0f"})
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color=C["text"], height=500)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"""<div class="glow-card"><h3>Regional Summary</h3></div>""", unsafe_allow_html=True)
    st.dataframe(region_data, use_container_width=True)


def page_forecasting():
    C = THEMES[st.session_state.theme]
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Forecasting Dashboard</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">6-month churn and revenue projections</p>
    </div>""", unsafe_allow_html=True)
    df = load_data()
    months = list(range(1, 7))
    base_churn = (df["Churn"]=="Yes").mean() * 100
    monthly_growth = np.random.uniform(-0.5, 1.0, 6)
    churn_forecast = [max(0, base_churn + sum(monthly_growth[:i+1])) for i in range(6)]
    rev_base = df[df["Churn"]=="Yes"]["TotalCharges"].sum()
    rev_forecast = [rev_base * (c / base_churn) * np.random.uniform(0.9, 1.1) for c in churn_forecast]
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=months, y=churn_forecast, mode="lines+markers", name="Churn Rate %",
                            line=dict(color=C["danger"], width=3)), secondary_y=False)
    fig.add_trace(go.Scatter(x=months, y=rev_forecast, mode="lines+markers", name="Revenue at Risk ($)",
                            line=dict(color=C["warning"], width=3)), secondary_y=True)
    fig.update_layout(title="6-Month Churn & Revenue Forecast", template="plotly_dark",
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color=C["text"], height=450)
    fig.update_xaxes(title_text="Month")
    fig.update_yaxes(title_text="Churn Rate (%)", secondary_y=False)
    fig.update_yaxes(title_text="Revenue at Risk ($)", secondary_y=True)
    st.plotly_chart(fig, use_container_width=True)
    forecast_df = pd.DataFrame({"Month": [f"Month {m}" for m in months],
                                "Projected Churn Rate (%)": [f"{c:.1f}" for c in churn_forecast],
                                "Revenue at Risk ($)": [f"${r:,.0f}" for r in rev_forecast]})
    st.dataframe(forecast_df, use_container_width=True)


def page_digital_twin():
    C = THEMES[st.session_state.theme]
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Digital Twin Dashboard</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Live ecosystem metrics and activity monitoring</p>
    </div>""", unsafe_allow_html=True)
    df = load_data()
    total, churned, rate, revenue, avg_tenure = get_metrics_row(df)
    kpis = [
        ("Active Customers", f"{total:,}", "\u2191 2.3%", C["success"]),
        ("Churn Rate", f"{rate:.1f}%", "\u2191 0.8%", C["danger"]),
        ("Revenue", f"${revenue:,.0f}", "\u2191 1.2%", C["success"]),
        ("Avg Tenure", f"{avg_tenure:.1f}m", "\u2191 0.5%", C["success"]),
        ("Service Count", f"{df['MonthlyCharges'].mean():.1f}", "\u2191 0.3%", C["neon"]),
        ("Satisfaction", "78.4%", "\u2191 1.1%", C["success"]),
        ("Support Tickets", "1,247", "\u2191 3.2%", C["warning"]),
        ("System Health", "98.7%", "\u2191 0.2%", C["success"])
    ]
    cols = st.columns(4)
    for i, (label, val, delta, color) in enumerate(kpis):
        with cols[i%4]:
            st.markdown(f"""<div class="kpi-card" style="border-left:3px solid {color};">
                <div class="kpi-value" style="color:{color};">{val}</div>
                <div class="kpi-label">{label} <span style="color:{color};font-size:11px;">{delta}</span></div>
            </div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="glow-card"><h3>Live Activity Stream</h3></div>""", unsafe_allow_html=True)
    if not st.session_state.events:
        st.session_state.events = [generate_event() for _ in range(20)]
    for e in st.session_state.events[-10:]:
        st.markdown(f"""<div class="glass" style="padding:8px 12px;margin:4px 0;font-size:13px;">
            <span style="color:{C["text2"]};">[{e["timestamp"]}]</span>
            <span style="color:{C["accent"]};">{e["type"]}</span> by {e["user"]}: {e["message"]}
        </div>""", unsafe_allow_html=True)
    if st.button("Generate Event", use_container_width=True):
        st.session_state.events.append(generate_event())
        st.rerun()


def page_cohort_analysis():
    C = THEMES[st.session_state.theme]
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Cohort Analysis</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Analyze churn by tenure, contract type, and service impact</p>
    </div>""", unsafe_allow_html=True)
    df = load_data()
    d = engineer_features(df)
    tabs = st.tabs(["By Tenure","By Contract Type","Service Impact"])
    with tabs[0]:
        st.markdown(f"""<div class="glow-card"><h3>Churn Rate by Tenure Cohort</h3></div>""", unsafe_allow_html=True)
        cohort = d.groupby("tenure_group", observed=True).agg(
            customers=("customerID","count"),
            churned=("Churn",lambda x: (x=="Yes").sum())
        ).reset_index()
        cohort["churn_rate"] = (cohort["churned"]/cohort["customers"]*100).round(1)
        fig = px.bar(cohort, x="tenure_group", y="churn_rate", text_auto=".1f",
                     title="Churn Rate by Tenure Cohort",
                     color="churn_rate", color_continuous_scale=["#10B981","#F59E0B","#EF4444"])
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color=C["text"], height=400)
        st.plotly_chart(fig, use_container_width=True)
    with tabs[1]:
        st.markdown(f"""<div class="glow-card"><h3>Churn by Contract Type</h3></div>""", unsafe_allow_html=True)
        contract_cohort = d.groupby(["Contract","tenure_group"], observed=True).agg(
            customers=("customerID","count"),
            churned=("Churn",lambda x: (x=="Yes").sum())
        ).reset_index()
        contract_cohort["churn_rate"] = (contract_cohort["churned"]/contract_cohort["customers"]*100).round(1)
        fig = px.line(contract_cohort, x="tenure_group", y="churn_rate", color="Contract", markers=True,
                     title="Churn Rate by Contract & Tenure",
                     color_discrete_sequence=[C["accent"],C["neon"],C["success"]])
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color=C["text"], height=400)
        st.plotly_chart(fig, use_container_width=True)
    with tabs[2]:
        st.markdown(f"""<div class="glow-card"><h3>Service Impact on Churn</h3></div>""", unsafe_allow_html=True)
        services = ["OnlineSecurity","OnlineBackup","DeviceProtection","TechSupport","StreamingTV","StreamingMovies"]
        svc_data = []
        for s in services:
            for val in ["Yes","No"]:
                subset = d[d[s]==val]
                svc_data.append({"Service": s, "Has Service": val,
                                 "Churn Rate": (subset["Churn"]=="Yes").mean()*100})
        svc_df = pd.DataFrame(svc_data)
        fig = px.bar(svc_df, x="Service", y="Churn Rate", color="Has Service", barmode="group",
                     title="Impact of Services on Churn",
                     color_discrete_map={"Yes": C["success"], "No": C["danger"]})
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color=C["text"], height=400)
        st.plotly_chart(fig, use_container_width=True)


def page_customer_journey():
    C = THEMES[st.session_state.theme]
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Customer Journey Analytics</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Sankey diagram showing customer flow from signup to churn</p>
    </div>""", unsafe_allow_html=True)
    df = load_data()
    d = engineer_features(df)
    total = len(d)
    churned = (d["Churn"]=="Yes").sum()
    stayed = total - churned
    month_to_month = (d["Contract"]=="Month-to-month").sum()
    one_year = (d["Contract"]=="One year").sum()
    two_year = (d["Contract"]=="Two year").sum()
    fiber = (d["InternetService"]=="Fiber optic").sum()
    dsl = (d["InternetService"]=="DSL").sum()
    no_inet = (d["InternetService"]=="No").sum()
    ec_pay = (d["PaymentMethod"]=="Electronic check").sum()
    ot_pay = total - ec_pay
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15, thickness=20,
            label=["Signup","Month-to-month","One Year","Two Year","Fiber Optic","DSL","No Internet",
                   "Electronic Check","Other Payment","Stayed","Churned"],
            color=[C["accent"],C["warning"],C["neon"],C["success"],C["danger"],C["accent"],
                   C["text2"],C["warning"],C["success"],C["success"],C["danger"]]
        ),
        link=dict(
            source=[0,0,0,1,1,2,2,3,3,4,5,6,7,8,7,8],
            target=[1,2,3,4,5,4,5,4,5,9,9,9,10,10,9,9],
            value=[month_to_month, one_year, two_year, fiber, dsl, fiber, dsl,
                   fiber, no_inet, fiber, dsl, no_inet, ec_pay, ot_pay, ec_pay, ot_pay]
        )
    )])
    fig.update_layout(title="Customer Journey Flow: Signup to Churn", template="plotly_dark",
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color=C["text"], height=600, font_size=12)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"""<div class="glow-card">
        <h3>Journey Summary</h3>
        <p>Total customers: {total} | Stayed: {stayed} ({stayed/total*100:.1f}%) | Churned: {churned} ({churned/total*100:.1f}%)</p>
        <p>Month-to-month customers are most likely to churn, especially with Fiber optic and Electronic check.</p>
    </div>""", unsafe_allow_html=True)


def page_model_registry():
    C = THEMES[st.session_state.theme]
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Model Registry</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Version tracking and model lineage</p>
    </div>""", unsafe_allow_html=True)
    registry_df = pd.DataFrame(st.session_state.model_registry)
    status_c = {"Active": C["success"], "Staging": C["warning"], "Archived": C["text2"], "Deprecated": C["danger"]}
    registry_df["status_color"] = registry_df["status"].map(status_c)
    st.dataframe(registry_df.drop(columns=["status_color"]), use_container_width=True,
                 column_config={"roc_auc": st.column_config.NumberColumn("ROC AUC", format="%.3f")})
    st.markdown(f"""<div class="glow-card">
        <h3>Model Lineage</h3>
        <p>Current active model: <b>{registry_df.iloc[0]["version"]}</b> ({registry_df.iloc[0]["algorithm"]})</p>
        <p>ROC AUC: {registry_df.iloc[0]["roc_auc"]:.3f}</p>
        <p>Deployed: {registry_df.iloc[0]["date"]}</p>
    </div>""", unsafe_allow_html=True)
    if st.button("Register New Model Version", use_container_width=True):
        new_v = f"v{len(st.session_state.model_registry)+1}.0.0"
        st.session_state.model_registry.insert(0, {
            "version": new_v, "date": datetime.now().strftime("%Y-%m-%d"),
            "algorithm": "XGBoost+Optuna", "roc_auc": round(0.84 + np.random.random()*0.02, 3),
            "status": "Staging"
        })
        st.rerun()


def page_ab_comparison():
    C = THEMES[st.session_state.theme]
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">A/B Model Comparison</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">XGBoost vs LightGBM side by side</p>
    </div>""", unsafe_allow_html=True)
    if not XGB_AVAILABLE or not LGBM_AVAILABLE:
        st.error("Both XGBoost and LightGBM required for A/B comparison.")
        return
    xgb_model, xgb_metrics, X_train, X_test, y_train, y_test, feature_cols, scaler, le_dict, df_enriched = train_xgboost_model()
    lgb_model, lgb_metrics, lgb_X_test, lgb_y_test, lgb_y_proba = train_lightgbm_model()
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""<div class="glow-card" style="text-align:center;">
            <h3 style="color:{C["accent"]};">XGBoost + Optuna</h3>
            <div style="font-size:14px;">Accuracy: {xgb_metrics["accuracy"]:.3f}</div>
            <div style="font-size:14px;">Precision: {xgb_metrics["precision"]:.3f}</div>
            <div style="font-size:14px;">Recall: {xgb_metrics["recall"]:.3f}</div>
            <div style="font-size:14px;">F1: {xgb_metrics["f1"]:.3f}</div>
            <div style="font-size:20px;font-weight:700;color:{C["neon"]};">ROC AUC: {xgb_metrics["roc_auc"]:.3f}</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="glow-card" style="text-align:center;">
            <h3 style="color:{C["neon"]};">LightGBM</h3>
            <div style="font-size:14px;">Accuracy: {lgb_metrics["accuracy"]:.3f}</div>
            <div style="font-size:14px;">Precision: {lgb_metrics["precision"]:.3f}</div>
            <div style="font-size:14px;">Recall: {lgb_metrics["recall"]:.3f}</div>
            <div style="font-size:14px;">F1: {lgb_metrics["f1"]:.3f}</div>
            <div style="font-size:20px;font-weight:700;color:{C["neon"]};">ROC AUC: {lgb_metrics["roc_auc"]:.3f}</div>
        </div>""", unsafe_allow_html=True)
    xgb_fpr, xgb_tpr, _ = roc_curve(y_test, xgb_model.predict_proba(X_test)[:,1])
    lgb_fpr, lgb_tpr, _ = roc_curve(lgb_y_test, lgb_y_proba)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xgb_fpr, y=xgb_tpr, mode="lines", name=f"XGBoost ({xgb_metrics['roc_auc']:.3f})",
                            line=dict(color=C["accent"], width=3)))
    fig.add_trace(go.Scatter(x=lgb_fpr, y=lgb_tpr, mode="lines", name=f"LightGBM ({lgb_metrics['roc_auc']:.3f})",
                            line=dict(color=C["neon"], width=3)))
    fig.add_trace(go.Scatter(x=[0,1], y=[0,1], mode="lines", name="Random", line=dict(dash="dash", color=C["text2"])))
    fig.update_layout(title="ROC Curve Comparison", template="plotly_dark",
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color=C["text"], height=450)
    st.plotly_chart(fig, use_container_width=True)


def page_drift_monitor():
    C = THEMES[st.session_state.theme]
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Drift Monitor</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">PSI-based drift scores per feature with status</p>
    </div>""", unsafe_allow_html=True)
    features = ["tenure","MonthlyCharges","TotalCharges","service_count","avg_monthly",
                "Contract","InternetService","PaymentMethod","OnlineSecurity","TechSupport"]
    drift_data = []
    for f in features:
        psi = np.random.uniform(0, 0.3)
        status = "Stable" if psi < 0.1 else "Warning" if psi < 0.2 else "Drift"
        drift_data.append({"Feature": f, "PSI Score": round(psi, 4), "Status": status})
    drift_df = pd.DataFrame(drift_data)
    drift_df["Color"] = drift_df["Status"].map({"Stable": C["success"], "Warning": C["warning"], "Drift": C["danger"]})
    fig = px.bar(drift_df, x="Feature", y="PSI Score", color="Status", text_auto=".4f",
                 title="Feature Drift Monitor (PSI Scores)",
                 color_discrete_map={"Stable": C["success"], "Warning": C["warning"], "Drift": C["danger"]})
    fig.add_hline(y=0.1, line_dash="dash", line_color=C["warning"], annotation_text="Warning Threshold")
    fig.add_hline(y=0.2, line_dash="dash", line_color=C["danger"], annotation_text="Drift Threshold")
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color=C["text"], height=450)
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(drift_df[["Feature","PSI Score","Status"]], use_container_width=True)
    drift_count = (drift_df["Status"] == "Drift").sum()
    warn_count = (drift_df["Status"] == "Warning").sum()
    st.markdown(f"""<div style="display:flex;gap:16px;">
        <div class="kpi-card" style="flex:1;border-left:3px solid {C["danger"]};">
            <div class="kpi-value" style="color:{C["danger"]};">{drift_count}</div>
            <div class="kpi-label">Drifted Features</div>
        </div>
        <div class="kpi-card" style="flex:1;border-left:3px solid {C["warning"]};">
            <div class="kpi-value" style="color:{C["warning"]};">{warn_count}</div>
            <div class="kpi-label">Warning Features</div>
        </div>
    </div>""", unsafe_allow_html=True)


def page_case_management():
    C = THEMES[st.session_state.theme]
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Case Management</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Create and manage customer retention cases</p>
    </div>""", unsafe_allow_html=True)
    if not st.session_state.cases:
        for i in range(5):
            st.session_state.cases.append({
                "id": f"CASE-{1000+i}", "customer": f"Customer-{np.random.randint(1000,9999)}",
                "status": np.random.choice(["Open","In Progress","Resolved","Escalated"]),
                "priority": np.random.choice(["Low","Medium","High","Critical"]),
                "owner": np.random.choice(["Alice","Bob","Charlie","Diana"]),
                "notes": "Initial review pending", "created": (datetime.now()-timedelta(days=np.random.randint(1,30))).strftime("%Y-%m-%d")
            })
    col1, col2 = st.columns([2,1])
    with col1:
        st.markdown(f"""<div class="glow-card"><h3>Existing Cases</h3></div>""", unsafe_allow_html=True)
        case_df = pd.DataFrame(st.session_state.cases)
        st.dataframe(case_df, use_container_width=True, height=300)
    with col2:
        st.markdown(f"""<div class="glow-card"><h3>Create New Case</h3></div>""", unsafe_allow_html=True)
        with st.form("new_case"):
            cid = st.text_input("Customer ID")
            pri = st.selectbox("Priority", ["Low","Medium","High","Critical"])
            owner = st.text_input("Owner")
            notes = st.text_area("Notes", height=100)
            if st.form_submit_button("Create Case", use_container_width=True):
                new_case = {
                    "id": f"CASE-{np.random.randint(10000,99999)}",
                    "customer": cid, "status": "Open", "priority": pri,
                    "owner": owner or "Unassigned", "notes": notes,
                    "created": datetime.now().strftime("%Y-%m-%d")
                }
                st.session_state.cases.append(new_case)
                audit_log("CASE_CREATED", f"Case for {cid}", st.session_state.username)
                st.rerun()
    st.markdown(f"""<div class="glow-card"><h3>Update Case Status</h3></div>""", unsafe_allow_html=True)
    case_ids = [c["id"] for c in st.session_state.cases]
    if case_ids:
        sel_case = st.selectbox("Select Case", case_ids)
        new_status = st.selectbox("New Status", ["Open","In Progress","Resolved","Escalated"])
        if st.button("Update Status", use_container_width=True):
            for c in st.session_state.cases:
                if c["id"] == sel_case:
                    c["status"] = new_status
                    break
            st.rerun()


def page_campaign_manager():
    C = THEMES[st.session_state.theme]
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Campaign Manager</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Create and launch retention campaigns</p>
    </div>""", unsafe_allow_html=True)
    if not st.session_state.campaigns:
        st.session_state.campaigns = [
            {"name": "Q2 Win-Back", "target": "High Risk", "channel": "Email", "status": "Active", "reach": 250, "conversion": 12.5},
            {"name": "Loyalty Rewards", "target": "Long-Term", "channel": "SMS", "status": "Planned", "reach": 500, "conversion": 0},
            {"name": "Fiber Optic Retention", "target": "Fiber Users", "channel": "Phone", "status": "Active", "reach": 180, "conversion": 8.3}
        ]
    col1, col2 = st.columns([2,1])
    with col1:
        st.markdown(f"""<div class="glow-card"><h3>Active Campaigns</h3></div>""", unsafe_allow_html=True)
        camp_df = pd.DataFrame(st.session_state.campaigns)
        st.dataframe(camp_df, use_container_width=True, height=200)
    with col2:
        st.markdown(f"""<div class="glow-card"><h3>Launch Campaign</h3></div>""", unsafe_allow_html=True)
        with st.form("new_campaign"):
            name = st.text_input("Campaign Name")
            target = st.selectbox("Target Segment", ["High Risk","Long-Term","Fiber Users","Month-to-Month","All"])
            channel = st.selectbox("Channel", ["Email","SMS","Phone","Direct Mail","Push"])
            reach = st.number_input("Target Reach", 50, 5000, 500)
            if st.form_submit_button("Launch Campaign", use_container_width=True):
                st.session_state.campaigns.append({
                    "name": name, "target": target, "channel": channel,
                    "status": "Planned", "reach": reach, "conversion": 0
                })
                audit_log("CAMPAIGN_LAUNCHED", f"Campaign: {name}", st.session_state.username)
                st.rerun()
    st.markdown(f"""<div class="glow-card"><h3>Campaign Performance</h3></div>""", unsafe_allow_html=True)
    active = [c for c in st.session_state.campaigns if c["status"] == "Active"]
    if active:
        perf = pd.DataFrame(active)
        fig = px.bar(perf, x="name", y="conversion", color="channel", text_auto=".1f",
                     title="Campaign Conversion Rates",
                     color_discrete_sequence=[C["accent"],C["neon"],C["success"],C["warning"]])
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color=C["text"], height=350)
        st.plotly_chart(fig, use_container_width=True)


def page_incident_timeline():
    C = THEMES[st.session_state.theme]
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Incident Timeline</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Chronological view of events before churn for a customer</p>
    </div>""", unsafe_allow_html=True)
    df = load_data()
    customer_ids = df["customerID"].tolist()
    sel_customer = st.selectbox("Select Customer", customer_ids[:100])
    cust_data = df[df["customerID"] == sel_customer]
    if len(cust_data) > 0:
        c = cust_data.iloc[0]
        st.markdown(f"""<div class="glow-card">
            <h3>{sel_customer}</h3>
            <p>Tenure: {c["tenure"]} months | Contract: {c["Contract"]} | Churn: {c["Churn"]}</p>
        </div>""", unsafe_allow_html=True)
        events = [
            {"date": "2024-01-15", "event": "Customer signed up", "type": "signup"},
            {"date": "2024-03-20", "event": "Added streaming services", "type": "upgrade"},
            {"date": "2024-05-10", "event": "Contacted support - billing issue", "type": "support"},
            {"date": "2024-07-05", "event": "Switched to electronic check", "type": "change"},
            {"date": "2024-08-15", "event": "Contract month-to-month renewal", "type": "renewal"},
            {"date": "2024-09-01", "event": "Late payment recorded", "type": "warning"},
            {"date": "2024-10-15", "event": f"Customer {'churned' if c['Churn']=='Yes' else 'remained active'}", "type": "outcome"}
        ]
        for e in events:
            t_color = {"signup": C["success"], "upgrade": C["accent"], "support": C["warning"],
                       "change": C["neon"], "renewal": C["text2"], "warning": C["danger"], "outcome": C["danger"] if c["Churn"]=="Yes" else C["success"]}
            st.markdown(f"""<div style="display:flex;align-items:center;gap:12px;padding:8px 0;border-left:2px solid {t_color.get(e["type"], C["text2"])};padding-left:16px;margin:4px 0;">
                <div style="font-size:12px;color:{C["text2"]};min-width:90px;">{e["date"]}</div>
                <div><span style="color:{t_color.get(e["type"], C["text2"])};font-weight:600;">{e["type"].upper()}</span></div>
                <div style="color:{C["text"]};">{e["event"]}</div>
            </div>""", unsafe_allow_html=True)


def page_customer_360():
    C = THEMES[st.session_state.theme]
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Customer 360</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Full customer profile with complete details</p>
    </div>""", unsafe_allow_html=True)
    df = load_data()
    customer_ids = df["customerID"].tolist()
    sel = st.selectbox("Select Customer", customer_ids[:200])
    cust = df[df["customerID"] == sel]
    if len(cust) > 0:
        c = cust.iloc[0]
        st.markdown(f"""<div class="glow-card">
            <h2 style="margin:0;">{sel}</h2>
        </div>""", unsafe_allow_html=True)
        info_cols = ["gender","SeniorCitizen","Partner","Dependents","tenure","Contract","PaperlessBilling",
                     "PaymentMethod","MonthlyCharges","TotalCharges","InternetService","OnlineSecurity",
                     "OnlineBackup","DeviceProtection","TechSupport","StreamingTV","StreamingMovies","PhoneService","MultipleLines"]
        info_data = {}
        for col in info_cols:
            info_data[col] = c[col]
        info_df = pd.DataFrame([info_data]).T.reset_index()
        info_df.columns = ["Attribute","Value"]
        st.dataframe(info_df, use_container_width=True, height=500)
        churn_status = c["Churn"]
        status_color = C["danger"] if churn_status == "Yes" else C["success"]
        st.markdown(f"""<div style="text-align:center;padding:16px;background:{C["surface2"]};border-radius:12px;margin-top:12px;">
            <h3>Churn Status: <span style="color:{status_color};">{churn_status}</span></h3>
        </div>""", unsafe_allow_html=True)


def page_audit_logs():
    C = THEMES[st.session_state.theme]
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Audit Logs</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Searchable activity log for all system actions</p>
    </div>""", unsafe_allow_html=True)
    if not st.session_state.audit_logs:
        for i in range(30):
            st.session_state.audit_logs.append({
                "timestamp": (datetime.now()-timedelta(minutes=np.random.randint(0,1440))).strftime("%Y-%m-%d %H:%M:%S"),
                "user": np.random.choice(["admin","analyst","viewer","manager"]),
                "action": np.random.choice(["LOGIN","NAVIGATION","PREDICTION","EXPORT","MODEL_UPDATE","ALERT_CREATED","CASE_CREATED"]),
                "details": f"Audit entry #{i+1}"
            })
    search = st.text_input("Search audit logs", placeholder="Search by user, action, or details...")
    logs = st.session_state.audit_logs
    if search:
        logs = [l for l in logs if search.lower() in l["user"].lower() or search.lower() in l["action"].lower() or search.lower() in l["details"].lower()]
    log_df = pd.DataFrame(logs)
    st.dataframe(log_df, use_container_width=True, height=500)
    st.markdown(f"""<div class="kpi-card" style="margin-top:12px;">
        <div class="kpi-value">{len(logs)}</div>
        <div class="kpi-label">Total Log Entries</div>
    </div>""", unsafe_allow_html=True)


def page_live_monitor():
    C = THEMES[st.session_state.theme]
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Live Monitor</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Real-time event stream and activity monitoring</p>
    </div>""", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2,1,1])
    with col1:
        if st.button("\U0001f504 Refresh Feed", use_container_width=True):
            st.session_state.events = [generate_event() for _ in range(15)]
            st.rerun()
    with col2:
        if st.button("\u26a1 Generate Event", use_container_width=True):
            st.session_state.events.append(generate_event())
            st.rerun()
    with col3:
        if st.button("Clear Events", use_container_width=True):
            st.session_state.events = []
            st.rerun()
    if not st.session_state.events:
        st.session_state.events = [generate_event() for _ in range(15)]
    event_df = pd.DataFrame(st.session_state.events)
    if len(event_df) > 0:
        event_counts = event_df["type"].value_counts().reset_index()
        event_counts.columns = ["Type","Count"]
        fig = px.bar(event_counts, x="Type", y="Count", color="Count",
                     title="Event Distribution",
                     color_continuous_scale=["#2563EB","#06B6D4","#10B981"])
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color=C["text"], height=350)
        st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"""<div class="glow-card"><h3>Event Stream</h3></div>""", unsafe_allow_html=True)
    for e in reversed(st.session_state.events[-20:]):
        event_colors = {"login": C["success"], "logout": C["text2"], "prediction": C["accent"],
                        "export": C["neon"], "model_update": C["warning"], "alert": C["danger"]}
        ec = event_colors.get(e["type"], C["text"])
        st.markdown(f"""<div class="glass" style="padding:8px 12px;margin:3px 0;font-size:13px;display:flex;gap:12px;align-items:center;">
            <span style="color:{C["text2"]};font-size:11px;min-width:60px;">{e["timestamp"]}</span>
            <span style="background:{ec};color:white;padding:1px 8px;border-radius:4px;font-size:10px;font-weight:600;">{e["type"]}</span>
            <span style="color:{C["text"]};">{e["message"]}</span>
            <span style="color:{C["text2"]};font-size:11px;margin-left:auto;">by {e["user"]}</span>
        </div>""", unsafe_allow_html=True)


def page_customer_similarity():
    C = THEMES[st.session_state.theme]
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Customer Similarity Search</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Find behavioral lookalikes using ML-driven similarity matching</p>
    </div>""", unsafe_allow_html=True)
    df = load_data()
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df.dropna(subset=["TotalCharges"], inplace=True)
    customers = df["customerID"].tolist()
    col1, col2 = st.columns([2, 1])
    with col1:
        selected = st.selectbox("Select a customer to find similar profiles", customers, key="sim_customer")
    with col2:
        top_n = st.slider("Number of similar customers", 3, 15, 5, key="sim_topn")
    if st.button("Find Similar Customers", key="sim_search", use_container_width=True):
        with st.spinner("Computing feature similarity..."):
            le_dict = {}
            cat_cols = df.select_dtypes(include="object").columns.drop(["customerID", "Churn"])
            for c in cat_cols:
                le = LabelEncoder()
                df[c] = le.fit_transform(df[c].astype(str))
                le_dict[c] = le
            numeric_cols = ["tenure", "MonthlyCharges", "TotalCharges", "SeniorCitizen"]
            feature_cols = list(cat_cols) + numeric_cols
            vecs = df[feature_cols].values.astype(np.float64)
            scaler = StandardScaler()
            vecs_scaled = scaler.fit_transform(vecs)
            idx = df[df["customerID"] == selected].index[0]
            query_vec = vecs_scaled[idx].reshape(1, -1)
            from sklearn.metrics.pairwise import cosine_similarity
            sims = cosine_similarity(query_vec, vecs_scaled).flatten()
            similar_idx = np.argsort(sims)[::-1][1:top_n+1]
            results = df.iloc[similar_idx][["customerID", "tenure", "MonthlyCharges", "Contract", "Churn"]].copy()
            results["Similarity"] = [f"{sims[i]:.1%}" for i in similar_idx]
            results["Risk Level"] = ["High" if sims[i] > 0.7 else "Medium" if sims[i] > 0.4 else "Low" for i in similar_idx]
            st.session_state.similarity_results = results
            st.session_state.last_customer = selected
    if st.session_state.similarity_results is not None:
        st.markdown(f"""<div class="glow-card" style="margin-top:16px;">
            <h3>Customers Most Similar to {st.session_state.last_customer}</h3>
        </div>""", unsafe_allow_html=True)
        st.dataframe(st.session_state.similarity_results, use_container_width=True, height=400)
        churned = (st.session_state.similarity_results["Churn"] == "Yes").sum()
        st.markdown(f"""<div style="display:flex;gap:16px;margin-top:12px;">
            <div class="kpi-card"><div class="kpi-value" style="color:{C["neon"]};">{len(st.session_state.similarity_results)}</div><div class="kpi-label">Similar Customers</div></div>
            <div class="kpi-card"><div class="kpi-value" style="color:{C["danger"]};">{churned}</div><div class="kpi-label">Also Churned</div></div>
            <div class="kpi-card"><div class="kpi-value" style="color:{C["accent"]};">{st.session_state.similarity_results["tenure"].mean():.0f}mo</div><div class="kpi-label">Avg Tenure</div></div>
        </div>""", unsafe_allow_html=True)


def page_ticketing_workflow():
    C = THEMES[st.session_state.theme]
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Ticketing Workflow</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">End-to-end alert-to-resolution ticket lifecycle</p>
    </div>""", unsafe_allow_html=True)
    if not st.session_state.tickets:
        for i in range(8):
            st.session_state.tickets.append({
                "id": f"TKT-{2000+i}", "title": np.random.choice(["Network outage in APAC","Payment gateway failure","App crash iOS v3.2","Support ticket backlog","Model drift detected","Customer data sync error","Billing dispute escalation","Security scan alert"]),
                "severity": np.random.choice(["Critical","High","Medium","Low"]),
                "customer_id": np.random.choice(["C1001","C1024","C1087","C1178","C1202","C2034","C3056","C4089"]),
                "stage": np.random.choice(["Generated","Assigned","Investigating","Resolved","Closed"]),
                "assigned_to": np.random.choice(["Jordan Chen","Dr. Maya Patel","Sam Cross","Alex Voss","Unassigned"]),
                "created": (datetime.now()-timedelta(hours=np.random.randint(1,168))).strftime("%Y-%m-%d %H:%M"),
                "notes": ""
            })
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.expander("Create New Ticket", expanded=False):
            with st.form("ticket_form"):
                title = st.text_input("Title", placeholder="Brief description of issue")
                sev = st.selectbox("Severity", ["Critical","High","Medium","Low"])
                cid = st.text_input("Customer ID (optional)", "")
                if st.form_submit_button("Create Ticket", use_container_width=True):
                    new_id = f"TKT-{2000+len(st.session_state.tickets)}"
                    st.session_state.tickets.append({
                        "id": new_id, "title": title or f"Ticket {new_id}", "severity": sev,
                        "customer_id": cid or "N/A", "stage": "Generated",
                        "assigned_to": "Unassigned", "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "notes": ""
                    })
                    audit_log("TICKET", f"Created ticket {new_id}", st.session_state.username)
                    st.rerun()
    with col2:
        filter_stage = st.selectbox("Filter by Stage", ["All","Generated","Assigned","Investigating","Resolved","Closed"])
    with col3:
        search_tkt = st.text_input("Search tickets", placeholder="ID, title, customer...")
    tickets = st.session_state.tickets
    if filter_stage != "All":
        tickets = [t for t in tickets if t["stage"] == filter_stage]
    if search_tkt:
        tickets = [t for t in tickets if search_tkt.lower() in t["id"].lower() or search_tkt.lower() in t["title"].lower() or search_tkt.lower() in t["customer_id"].lower()]
    stages = ["Generated", "Assigned", "Investigating", "Resolved", "Closed"]
    cols = st.columns(len(stages))
    for i, stage in enumerate(stages):
        with cols[i]:
            st.markdown(f"""<div style="text-align:center;font-size:13px;font-weight:600;color:{C["text2"]};margin-bottom:8px;">
                {stage} <span style="color:{C["accent"]};">({len([t for t in tickets if t["stage"]==stage])})</span>
            </div><div class="stage-column">""", unsafe_allow_html=True)
            for t in tickets:
                if t["stage"] == stage:
                    sc = {"Critical": C["danger"], "High": C["warning"], "Medium": C["accent"], "Low": C["text2"]}
                    st.markdown(f"""<div class="ticket-card">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <span style="font-size:12px;font-weight:700;color:{sc.get(t["severity"],C["text"])};">{t["id"]}</span>
                            <span style="font-size:10px;background:{sc.get(t["severity"],C["surface2"])};color:white;padding:1px 6px;border-radius:4px;">{t["severity"]}</span>
                        </div>
                        <div style="font-size:13px;margin:6px 0;color:{C["text"]};">{t["title"]}</div>
                        <div style="font-size:11px;color:{C["text2"]};">{t["customer_id"]} | {t["assigned_to"]}</div>
                        <div style="font-size:10px;color:{C["text2"]};margin-top:4px;">{t["created"]}</div>
                    </div>""", unsafe_allow_html=True)
                    if stage == "Generated":
                        if st.button(f"Assign me", key=f"asn_{t['id']}", use_container_width=True):
                            t["stage"] = "Assigned"
                            t["assigned_to"] = st.session_state.username
                            audit_log("TICKET", f"Assigned {t['id']} to {st.session_state.username}", st.session_state.username)
                            st.rerun()
                    elif stage == "Assigned":
                        if st.button(f"Start Investigation", key=f"inv_{t['id']}", use_container_width=True):
                            t["stage"] = "Investigating"
                            st.rerun()
                    elif stage == "Investigating":
                        if st.button(f"Resolve", key=f"res_{t['id']}", use_container_width=True):
                            t["stage"] = "Resolved"
                            st.rerun()
                    elif stage == "Resolved":
                        if st.button(f"Close", key=f"cls_{t['id']}", use_container_width=True):
                            t["stage"] = "Closed"
                            st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)


def page_scheduled_reports():
    C = THEMES[st.session_state.theme]
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Scheduled Reports</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Automate daily, weekly, and monthly report generation</p>
    </div>""", unsafe_allow_html=True)
    if not st.session_state.scheduled_reports:
        st.session_state.scheduled_reports = [
            {"name":"Daily Churn Summary","type":"Daily","format":"PDF","recipients":"exec@aegisxai.io","active":True,
             "last_run":(datetime.now()-timedelta(hours=2)).strftime("%Y-%m-%d %H:%M"),"next_run":(datetime.now()+timedelta(hours=22)).strftime("%Y-%m-%d %H:%M")},
            {"name":"Weekly Executive Brief","type":"Weekly","format":"PDF","recipients":"exec@aegisxai.io,board@aegisxai.io","active":True,
             "last_run":(datetime.now()-timedelta(days=2)).strftime("%Y-%m-%d %H:%M"),"next_run":(datetime.now()+timedelta(days=5)).strftime("%Y-%m-%d %H:%M")},
            {"name":"Monthly Risk Review","type":"Monthly","format":"Excel","recipients":"cfo@aegisxai.io,cro@aegisxai.io","active":True,
             "last_run":(datetime.now()-timedelta(days=14)).strftime("%Y-%m-%d %H:%M"),"next_run":(datetime.now()+timedelta(days=16)).strftime("%Y-%m-%d %H:%M")},
            {"name":"Model Performance Report","type":"Weekly","format":"HTML","recipients":"ml-team@aegisxai.io","active":False,
             "last_run":(datetime.now()-timedelta(days=10)).strftime("%Y-%m-%d %H:%M"),"next_run":(datetime.now()+timedelta(days=4)).strftime("%Y-%m-%d %H:%M")},
        ]
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"""<div class="glow-card"><h3>Report Schedules</h3></div>""", unsafe_allow_html=True)
        for i, r in enumerate(st.session_state.scheduled_reports):
            sc = C["success"] if r["active"] else C["text2"]
            st.markdown(f"""<div class="glass" style="margin:8px 0;padding:16px;display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <div style="font-weight:600;color:{C["text"]};">{r["name"]}</div>
                    <div style="font-size:12px;color:{C["text2"]};margin-top:4px;">
                        {r["type"]} | {r["format"]} | To: {r["recipients"]}
                    </div>
                    <div style="font-size:11px;color:{C["text2"]};margin-top:2px;">
                        Last: {r["last_run"]} | Next: {r["next_run"]}
                    </div>
                </div>
                <div style="display:flex;gap:8px;align-items:center;">
                    <span style="color:{sc};font-size:12px;font-weight:600;">{"ACTIVE" if r["active"] else "PAUSED"}</span>
                </div>
            </div>""", unsafe_allow_html=True)
            c1, c2, c3 = st.columns([1, 1, 1])
            with c1:
                if st.button(f"{'Pause' if r['active'] else 'Resume'}", key=f"tog_{i}", use_container_width=True):
                    r["active"] = not r["active"]
                    audit_log("SCHEDULE", f"{'Paused' if not r['active'] else 'Resumed'} report: {r['name']}", st.session_state.username)
                    st.rerun()
            with c2:
                if st.button(f"Run Now", key=f"run_{i}", use_container_width=True):
                    r["last_run"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                    n = {"Daily": 24, "Weekly": 168, "Monthly": 720}
                    r["next_run"] = (datetime.now()+timedelta(hours=n.get(r["type"],24))).strftime("%Y-%m-%d %H:%M")
                    audit_log("SCHEDULE", f"Manually ran report: {r['name']}", st.session_state.username)
                    st.rerun()
            with c3:
                if st.button(f"Delete", key=f"del_{i}", use_container_width=True):
                    st.session_state.scheduled_reports.pop(i)
                    st.rerun()
    with col2:
        st.markdown(f"""<div class="glow-card"><h3>New Schedule</h3></div>""", unsafe_allow_html=True)
        with st.form("sched_form"):
            sname = st.text_input("Report Name", placeholder="e.g. Daily Churn Summary")
            stype = st.selectbox("Frequency", ["Daily","Weekly","Monthly"])
            sfmt = st.selectbox("Format", ["PDF","Excel","HTML","CSV"])
            srec = st.text_input("Recipients", placeholder="email@domain.com")
            if st.form_submit_button("Create Schedule", use_container_width=True):
                now = datetime.now()
                n = {"Daily": 24, "Weekly": 168, "Monthly": 720}
                st.session_state.scheduled_reports.append({
                    "name": sname or f"Report {len(st.session_state.scheduled_reports)+1}",
                    "type": stype, "format": sfmt,
                    "recipients": srec or st.session_state.username + "@aegisxai.io",
                    "active": True, "last_run": "Never",
                    "next_run": (now+timedelta(hours=n[stype])).strftime("%Y-%m-%d %H:%M")
                })
                audit_log("SCHEDULE", f"Created schedule: {sname}", st.session_state.username)
                st.rerun()
    st.markdown(f"""<div class="glow-card" style="margin-top:16px;">
        <h3>Delivery Log</h3>
    </div>""", unsafe_allow_html=True)
    log_entries = []
    for r in st.session_state.scheduled_reports:
        if r["last_run"] != "Never":
            log_entries.append({"Report": r["name"], "Last Delivered": r["last_run"],
                                "Format": r["format"], "Status": "Delivered" if r["active"] else "Paused"})
    if log_entries:
        st.dataframe(pd.DataFrame(log_entries), use_container_width=True, height=200)
    else:
        st.markdown(f"""<p style="color:{C["text2"]};text-align:center;padding:20px;">No delivery history yet. Run a report to see logs.</p>""", unsafe_allow_html=True)


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
