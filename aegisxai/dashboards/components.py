import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time, io, base64
from collections import Counter
from sklearn.metrics import confusion_matrix, precision_recall_curve

try: from xgboost import XGBClassifier; XGB_AVAILABLE = True
except: XGB_AVAILABLE = False
try: import shap; SHAP_AVAILABLE = True
except: SHAP_AVAILABLE = False
try: from lime.lime_tabular import LimeTabularExplainer; LIME_AVAILABLE = True
except: LIME_AVAILABLE = False

from aegisxai.utils.helpers import audit_log, format_currency, make_download_link, generate_event, get_system_health_status, render_system_status
from aegisxai.models.features import load_data, engineer_features, prepare_ml_data, get_churn_rate
from aegisxai.models.train import train_xgboost_model, train_lightgbm_model
from aegisxai.services.prediction_service import get_segmentation_data, enrich_with_cluster_info, calculate_churn_probability, get_churn_reasons
from aegisxai.services.recommendation_service import generate_retention_strategies, ab_test_summary, get_retention_recommendation


def maybe_compact():
    if st.session_state.get("mobile_layout", False):
        st.markdown("<style>.main .block-container{padding:1rem 0.5rem!important;max-width:100%!important;}</style>", unsafe_allow_html=True)

def get_metrics_row(df):
    total = len(df)
    churned = (df["Churn"] == "Yes").sum()
    rate = (churned / total) * 100
    revenue = df["TotalCharges"].sum()
    avg_tenure = df["tenure"].mean()
    return total, churned, rate, revenue, avg_tenure


def dashboard_hero_metrics(C):
    df = load_data()
    total, churned, rate, revenue, avg_tenure = get_metrics_row(df)
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(f"""<div class="glow-card" style="text-align:center;padding:20px 12px;">
            <div style="font-size:11px;color:{C["text2"]};text-transform:uppercase;letter-spacing:1px;">Active Customers</div>
            <div style="font-size:36px;font-weight:800;color:{C["neon"]};">{total-churned:,}</div>
            <div style="font-size:12px;color:{C["success"]};">? {(1-rate/100)*100:.1f}% retention</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="glow-card" style="text-align:center;padding:20px 12px;">
            <div style="font-size:11px;color:{C["text2"]};text-transform:uppercase;letter-spacing:1px;">Churn Rate</div>
            <div style="font-size:36px;font-weight:800;color:{C["danger"]};">{rate:.1f}%</div>
            <div style="font-size:12px;color:{C["text2"]};">{churned:,} customers lost</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="glow-card" style="text-align:center;padding:20px 12px;">
            <div style="font-size:11px;color:{C["text2"]};text-transform:uppercase;letter-spacing:1px;">Total Revenue</div>
            <div style="font-size:36px;font-weight:800;color:{C["success"]};">{revenue:,.0f}</div>
            <div style="font-size:12px;color:{C["text2"]};">Lifetime value</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="glow-card" style="text-align:center;padding:20px 12px;">
            <div style="font-size:11px;color:{C["text2"]};text-transform:uppercase;letter-spacing:1px;">Avg Monthly Charge</div>
            <div style="font-size:36px;font-weight:800;color:{C["accent"]};">${df["MonthlyCharges"].mean():.1f}</div>
            <div style="font-size:12px;color:{C["text2"]};">Per customer</div>
        </div>""", unsafe_allow_html=True)
    with c5:
        st.markdown(f"""<div class="glow-card" style="text-align:center;padding:20px 12px;">
            <div style="font-size:11px;color:{C["text2"]};text-transform:uppercase;letter-spacing:1px;">Avg Tenure</div>
            <div style="font-size:36px;font-weight:800;color:{C["neon"]};">{avg_tenure:.1f}</div>
            <div style="font-size:12px;color:{C["text2"]};">Months</div>
        </div>""", unsafe_allow_html=True)


def dashboard_charts_row1(C, df):
    d = engineer_features(df)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""<div class="glow-card"><h3 style="font-size:16px;margin:0 0 12px;">Monthly Charges Distribution</h3></div>""", unsafe_allow_html=True)
        fig = px.histogram(df, x="MonthlyCharges", color="Churn", nbins=30,
                           color_discrete_map={"No": C["success"], "Yes": C["danger"]},
                           title="", marginal="box")
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color=C["text"], height=350, showlegend=True, barmode="overlay")
        fig.update_traces(opacity=0.65)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.markdown(f"""<div class="glow-card"><h3 style="font-size:16px;margin:0 0 12px;">Tenure vs Monthly Charges</h3></div>""", unsafe_allow_html=True)
        fig = px.scatter(d, x="tenure", y="MonthlyCharges", color="Churn", opacity=0.5,
                         color_discrete_map={"No": C["accent"], "Yes": C["danger"]},
                         title="", trendline="lowess")
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color=C["text"], height=350)
        st.plotly_chart(fig, use_container_width=True)


def dashboard_charts_row2(C, df):
    services = ["OnlineSecurity","OnlineBackup","DeviceProtection","TechSupport","StreamingTV","StreamingMovies"]
    svc_churn = []
    for s in services:
        for v in ["Yes","No"]:
            subset = df[df[s]==v]
            svc_churn.append({"Service": s, "Has Service": v,
                              "Count": len(subset),
                              "Churn Rate": (subset["Churn"]=="Yes").mean()*100})
    sc_df = pd.DataFrame(svc_churn)
    fig = px.bar(sc_df, x="Service", y="Churn Rate", color="Has Service", barmode="group",
                 title="Service Impact on Churn Rates",
                 color_discrete_map={"Yes": C["success"], "No": C["danger"]})
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color=C["text"], height=400)
    st.plotly_chart(fig, use_container_width=True)


def dashboard_recent_activity(C):
    st.markdown(f"""<div class="glow-card"><h3 style="font-size:16px;">Recent Activity</h3></div>""", unsafe_allow_html=True)
    if not st.session_state.events:
        st.session_state.events = [generate_event() for _ in range(8)]
    for e in st.session_state.events[-5:]:
        st.markdown(f"""<div class="glass" style="padding:6px 12px;margin:3px 0;font-size:12px;">
            <span style="color:{C["text2"]};">[{e["timestamp"]}]</span>
            <span style="color:{C["accent"]};">{e["type"]}</span> - {e["message"]}
        </div>""", unsafe_allow_html=True)


def risk_queue_stats(C, df):
    d = engineer_features(df)
    d["risk_score"] = np.where(d["Contract"]=="Month-to-month",25,0) + \
                      np.where(d["InternetService"]=="Fiber optic",20,0) + \
                      np.where(d["PaymentMethod"]=="Electronic check",15,0) + \
                      np.where(d["SeniorCitizen"]=="Yes",10,0) + \
                      np.where(d["tenure"]<12,15,0)
    d["risk_level"] = pd.cut(d["risk_score"], bins=[0,30,50,100], labels=["Low","Medium","High"])
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-value" style="color:{C["success"]};">{(d["risk_level"]=="Low").sum()}</div><div class="kpi-label">Low Risk</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-value" style="color:{C["warning"]};">{(d["risk_level"]=="Medium").sum()}</div><div class="kpi-label">Medium Risk</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-value" style="color:{C["danger"]};">{(d["risk_level"]=="High").sum()}</div><div class="kpi-label">High Risk</div></div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-value" style="color:{C["neon"]};">{d["risk_score"].mean():.1f}</div><div class="kpi-label">Avg Risk Score</div></div>""", unsafe_allow_html=True)


def risk_queue_chart(C, df):
    d = engineer_features(df)
    d["risk_score"] = np.where(d["Contract"]=="Month-to-month",25,0) + \
                      np.where(d["InternetService"]=="Fiber optic",20,0) + \
                      np.where(d["PaymentMethod"]=="Electronic check",15,0) + \
                      np.where(d["SeniorCitizen"]=="Yes",10,0) + \
                      np.where(d["tenure"]<12,15,0)
    d["risk_level"] = pd.cut(d["risk_score"], bins=[0,30,50,100], labels=["Low","Medium","High"])
    risk_by_contract = d.groupby(["Contract","risk_level"], observed=True).size().reset_index(name="count")
    fig = px.bar(risk_by_contract, x="Contract", y="count", color="risk_level",
                 title="Risk Distribution by Contract Type", barmode="stack",
                 color_discrete_map={"Low": C["success"], "Medium": C["warning"], "High": C["danger"]})
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color=C["text"], height=350)
    st.plotly_chart(fig, use_container_width=True)


def model_monitoring_detailed_metrics(C, model, X_test, y_test):
    if not XGB_AVAILABLE: return
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:,1]
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
    npv = tn / (tn + fn) if (tn + fn) > 0 else 0
    mcc_den = ((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn))**0.5
    mcc = (tp*tn - fp*fn) / mcc_den if mcc_den > 0 else 0
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Specificity", f"{specificity:.3f}")
    with c2: st.metric("NPV", f"{npv:.3f}")
    with c3: st.metric("MCC", f"{mcc:.3f}")
    with c4: st.metric("Best CV Score", "N/A")
    precision_vals, recall_vals, _ = precision_recall_curve(y_test, y_proba)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=recall_vals, y=precision_vals, mode="lines",
                             name="PR Curve", fill="tozeroy",
                             line=dict(color=C["neon"], width=3)))
    fig.update_layout(title="Precision-Recall Curve", template="plotly_dark",
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color=C["text"], height=400,
                      xaxis_title="Recall", yaxis_title="Precision")
    st.plotly_chart(fig, use_container_width=True)


def model_monitoring_feature_importance(C, model, feature_cols):
    if not XGB_AVAILABLE: return
    imp = pd.DataFrame({"Feature": feature_cols, "Importance": model.feature_importances_})
    imp = imp.sort_values("Importance", ascending=True)
    fig = px.bar(imp.tail(15), x="Importance", y="Feature", orientation="h",
                 title="Top 15 Feature Importances",
                 color="Importance", color_continuous_scale=["#2563EB","#06B6D4","#10B981"])
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color=C["text"], height=500)
    st.plotly_chart(fig, use_container_width=True)


def diagnostic_shap_detailed(C, model, X_test, feature_cols):
    st.markdown(f"""<div class="glow-card"><h3>SHAP Waterfall Explanation</h3></div>""", unsafe_allow_html=True)
    if SHAP_AVAILABLE and XGB_AVAILABLE:
        explainer = shap.TreeExplainer(model)
        idx = st.number_input("Select sample for waterfall", 0, X_test.shape[0]-1, 0, key="waterfall_idx")
        shap_values = explainer.shap_values(X_test[idx:idx+1])
        expected = explainer.expected_value
        if isinstance(expected, np.ndarray): expected = expected[0]
        st.info(f"Expected value (base): {expected:.4f} | Prediction: {model.predict_proba(X_test[idx:idx+1])[0][1]:.4f}")
        st.markdown(f"""<p style="color:{C["text2"]};font-size:13px;">SHAP waterfall shows how each feature pushes the prediction from the base value.</p>""", unsafe_allow_html=True)
    else:
        st.info("Install SHAP for detailed waterfall explanations.")


def diagnostic_lime_detailed(C, model, X_test, feature_cols):
    st.markdown(f"""<div class="glow-card"><h3>LIME Feature Contribution</h3></div>""", unsafe_allow_html=True)
    if LIME_AVAILABLE and XGB_AVAILABLE:
        explainer = LimeTabularExplainer(X_test, feature_names=feature_cols, class_names=["No Churn","Churn"], mode="classification")
        idx = st.number_input("Sample index for LIME", 0, X_test.shape[0]-1, 0, key="lime_idx_detailed")
        exp = explainer.explain_instance(X_test[idx], model.predict_proba, num_features=8)
        exp_list = exp.as_list()
        lime_df = pd.DataFrame(exp_list, columns=["Feature", "Contribution"])
        lime_df["abs_contrib"] = lime_df["Contribution"].abs()
        lime_df = lime_df.sort_values("abs_contrib", ascending=True)
        fig = px.bar(lime_df, x="Contribution", y="Feature", orientation="h",
                     title="LIME Feature Contributions",
                     color="Contribution", color_continuous_scale=["#EF4444","#1E293B","#10B981"])
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color=C["text"], height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Install LIME for detailed explanations.")


def alert_center_statistics(C):
    if not st.session_state.alerts: return
    df_al = pd.DataFrame(st.session_state.alerts)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f"""<div class="kpi-card"><div class="kpi-value" style="color:{C["danger"]};">{(df_al["severity"]=="Critical").sum()}</div><div class="kpi-label">Critical</div></div>""", unsafe_allow_html=True)
    with c2: st.markdown(f"""<div class="kpi-card"><div class="kpi-value" style="color:{C["warning"]};">{(df_al["severity"]=="High").sum()}</div><div class="kpi-label">High</div></div>""", unsafe_allow_html=True)
    with c3: st.markdown(f"""<div class="kpi-card"><div class="kpi-value" style="color:{C["accent"]};">{(df_al["severity"]=="Medium").sum()}</div><div class="kpi-label">Medium</div></div>""", unsafe_allow_html=True)
    with c4: st.markdown(f"""<div class="kpi-card"><div class="kpi-value" style="color:{C["success"]};">{(df_al["severity"]=="Low").sum()}</div><div class="kpi-label">Low</div></div>""", unsafe_allow_html=True)


def forecasting_detailed_projections(C, df):
    months = list(range(1, 7))
    base_churn = (df["Churn"]=="Yes").mean() * 100
    np.random.seed(42)
    churn_forecast = base_churn + np.cumsum(np.random.uniform(-0.5, 1.0, 6))
    churn_forecast = np.maximum(churn_forecast, 0)
    rev_at_risk = df[df["Churn"]=="Yes"]["TotalCharges"].sum()
    rev_forecast = rev_at_risk * (1 + np.random.uniform(-0.02, 0.05, 6))
    forecast_df = pd.DataFrame({
        "Month": [f"Month {i}" for i in months],
        "Churn Rate (%)": churn_forecast,
        "Revenue at Risk ($)": rev_forecast,
        "Confidence Lower": churn_forecast * 0.85,
        "Confidence Upper": churn_forecast * 1.15
    })
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=forecast_df["Confidence Upper"], mode="lines",
                             name="Upper Bound", line=dict(width=0), showlegend=False))
    fig.add_trace(go.Scatter(x=months, y=forecast_df["Confidence Lower"], mode="lines",
                             name="Lower Bound", line=dict(width=0), fill="tonexty",
                             fillcolor="rgba(37,99,235,0.15)"))
    fig.add_trace(go.Scatter(x=months, y=churn_forecast, mode="lines+markers",
                             name="Churn Rate Forecast",
                             line=dict(color=C["danger"], width=3)))
    fig.update_layout(title="6-Month Churn Rate Forecast with Confidence Bands",
                      template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)", font_color=C["text"], height=400)
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(forecast_df.round(2), use_container_width=True)


def cohort_analysis_heatmap(C, df):
    d = engineer_features(df)
    d["tenure_cohort"] = pd.cut(d["tenure"], bins=range(0, 80, 12), labels=[f"{i}-{i+11}" for i in range(0, 72, 12)])
    cohort_matrix = d.groupby(["tenure_cohort","Contract"], observed=True)["Churn"].apply(lambda x: (x=="Yes").mean()*100).reset_index()
    pivot = cohort_matrix.pivot(index="tenure_cohort", columns="Contract", values="Churn")
    fig = px.imshow(pivot, text_auto=".1f", aspect="auto",
                    title="Churn Rate Heatmap: Tenure vs Contract",
                    color_continuous_scale=["#10B981","#F59E0B","#EF4444"],
                    labels=dict(x="Contract", y="Tenure Cohort", color="Churn Rate %"))
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color=C["text"], height=400)
    st.plotly_chart(fig, use_container_width=True)


def customer_journey_detailed_flow(C):
    df = load_data()
    d = engineer_features(df)
    nodes = ["Signup", "Month-to-month", "One Year", "Two Year",
             "Online Security", "No Online Security",
             "Tech Support", "No Tech Support",
             "Electronic Check", "Other Payment",
             "Stayed", "Churned"]
    colors = [C["accent"], C["warning"], C["neon"], C["success"],
              C["success"], C["danger"],
              C["success"], C["danger"],
              C["warning"], C["success"],
              C["success"], C["danger"]]
    sources = []
    targets = []
    values = []
    m2m_ct = (d["Contract"]=="Month-to-month").sum()
    oy_ct = (d["Contract"]=="One year").sum()
    ty_ct = (d["Contract"]=="Two year").sum()
    sources.extend([0,0,0]); targets.extend([1,2,3]); values.extend([m2m_ct, oy_ct, ty_ct])
    m2m_os = d[(d["Contract"]=="Month-to-month") & (d["OnlineSecurity"]=="Yes")].shape[0]
    m2m_nos = d[(d["Contract"]=="Month-to-month") & (d["OnlineSecurity"]=="No")].shape[0]
    sources.extend([1,1]); targets.extend([4,5]); values.extend([m2m_os, m2m_nos])
    sources.extend([4,5]); targets.extend([10,11]); values.extend([m2m_os-50, m2m_nos-30])
    fig = go.Figure(data=[go.Sankey(
        node=dict(pad=15, thickness=20, label=nodes, color=colors),
        link=dict(source=sources, target=targets, value=values)
    )])
    fig.update_layout(title="Enhanced Customer Journey Flow", template="plotly_dark",
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color=C["text"], height=650, font_size=11)
    st.plotly_chart(fig, use_container_width=True)


def campaign_manager_analytics(C):
    if not st.session_state.campaigns: return
    camp_df = pd.DataFrame(st.session_state.campaigns)
    c1, c2, c3 = st.columns(3)
    with c1:
        active = (camp_df["status"]=="Active").sum()
        st.markdown(f"""<div class="kpi-card"><div class="kpi-value" style="color:{C["success"]};">{active}</div><div class="kpi-label">Active Campaigns</div></div>""", unsafe_allow_html=True)
    with c2:
        total_reach = camp_df["reach"].sum()
        st.markdown(f"""<div class="kpi-card"><div class="kpi-value" style="color:{C["neon"]};">{total_reach:,}</div><div class="kpi-label">Total Reach</div></div>""", unsafe_allow_html=True)
    with c3:
        avg_conv = camp_df[camp_df["status"]=="Active"]["conversion"].mean()
        st.markdown(f"""<div class="kpi-card"><div class="kpi-value" style="color:{C["accent"]};">{avg_conv:.1f}%</div><div class="kpi-label">Avg Conversion</div></div>""", unsafe_allow_html=True)
    fig = px.pie(camp_df, values="reach", names="channel", title="Campaign Channel Distribution",
                 color_discrete_sequence=[C["accent"],C["neon"],C["success"],C["warning"]])
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color=C["text"], height=350)
    st.plotly_chart(fig, use_container_width=True)


def drift_monitor_trend(C):
    features = ["tenure","MonthlyCharges","TotalCharges","service_count","avg_monthly"]
    time_periods = ["Week 1","Week 2","Week 3","Week 4","Week 5","Week 6"]
    drift_trend_data = []
    np.random.seed(42)
    for f in features:
        base = np.random.uniform(0.02, 0.08)
        for i, tp in enumerate(time_periods):
            drift_trend_data.append({"Feature": f, "Week": tp, "PSI": base + np.random.uniform(-0.01, 0.04) * (i+1)})
    trend_df = pd.DataFrame(drift_trend_data)
    fig = px.line(trend_df, x="Week", y="PSI", color="Feature", markers=True,
                  title="PSI Drift Trend Over Time",
                  color_discrete_sequence=px.colors.qualitative.Set2)
    fig.add_hline(y=0.1, line_dash="dash", line_color=C["warning"], annotation_text="Warning")
    fig.add_hline(y=0.2, line_dash="dash", line_color=C["danger"], annotation_text="Drift")
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color=C["text"], height=400)
    st.plotly_chart(fig, use_container_width=True)


def audit_logs_statistics(C):
    if not st.session_state.audit_logs: return
    al_df = pd.DataFrame(st.session_state.audit_logs)
    c1, c2, c3 = st.columns(3)
    with c1:
        unique_users = al_df["user"].nunique()
        st.markdown(f"""<div class="kpi-card"><div class="kpi-value" style="color:{C["neon"]};">{unique_users}</div><div class="kpi-label">Active Users</div></div>""", unsafe_allow_html=True)
    with c2:
        unique_actions = al_df["action"].nunique()
        st.markdown(f"""<div class="kpi-card"><div class="kpi-value" style="color:{C["accent"]};">{unique_actions}</div><div class="kpi-label">Unique Actions</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-value" style="color:{C["success"]};">{len(al_df)}</div><div class="kpi-label">Total Entries</div></div>""", unsafe_allow_html=True)
    action_counts = al_df["action"].value_counts().reset_index()
    action_counts.columns = ["Action","Count"]
    fig = px.bar(action_counts, x="Action", y="Count", color="Count",
                 title="Audit Log: Actions Distribution",
                 color_continuous_scale=["#2563EB","#06B6D4","#10B981"])
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color=C["text"], height=350)
    st.plotly_chart(fig, use_container_width=True)


def segment_summary_table(C, df_clustered):
    seg_df = df_clustered.copy()
    if "Churn" not in seg_df.columns:
        seg_df["Churn"] = "No"
    profile = seg_df.groupby("Cluster").agg({
        "tenure": ["mean","std"], "MonthlyCharges": ["mean","std"],
        "TotalCharges": ["mean","std"], "service_count": "mean",
        "Churn": lambda x: (x=="Yes").mean()*100 if x.dtype == "object" else 0,
        "customerID": "count"
    }).round(2)
    profile.columns = ["Tenure Mean","Tenure Std","Monthly Mean","Monthly Std",
                       "Total Mean","Total Std","Avg Services","Churn Rate %","Count"]
    profile.index = [f"Segment {i}" for i in range(len(profile))]
    return profile


def export_full_report():
    df = load_data()
    d = engineer_features(df)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Raw Data", index=False)
        d.to_excel(writer, sheet_name="Enriched Data", index=False)
        summary = d.groupby(["Contract","Churn"]).agg({"customerID":"count","MonthlyCharges":"mean","TotalCharges":"sum"}).reset_index()
        summary.to_excel(writer, sheet_name="Summary", index=False)
    return output.getvalue()


def display_data_quality_report(C):
    df = load_data()
    dq = pd.DataFrame({
        "Column": df.columns,
        "Type": df.dtypes.values,
        "Non-Null": df.count().values,
        "Null": df.isnull().sum().values,
        "Unique": [df[c].nunique() for c in df.columns],
        "Sample": [str(df[c].dropna().iloc[0]) if len(df[c].dropna())>0 else "" for c in df.columns]
    })
    st.markdown(f"""<div class="glow-card"><h3>Data Quality Assessment</h3></div>""", unsafe_allow_html=True)
    st.dataframe(dq, use_container_width=True, height=400)
    total_cells = df.size
    null_cells = df.isnull().sum().sum()
    completeness = ((total_cells - null_cells) / total_cells) * 100
    st.markdown(f"""<div style="display:flex;gap:16px;margin-top:8px;">
        <div class="kpi-card"><div class="kpi-value" style="color:{C["success"]};">{completeness:.1f}%</div><div class="kpi-label">Completeness</div></div>
        <div class="kpi-card"><div class="kpi-value" style="color:{C["danger"]};">{null_cells}</div><div class="kpi-label">Missing Values</div></div>
        <div class="kpi-card"><div class="kpi-value" style="color:{C["neon"]};">{len(df)}</div><div class="kpi-label">Total Records</div></div>
    </div>""", unsafe_allow_html=True)
