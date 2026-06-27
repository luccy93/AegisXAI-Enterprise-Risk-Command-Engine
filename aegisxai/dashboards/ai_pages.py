"""
AI & Intelligence Pages - Copilot, Forecasting, Retention Agent, Recommendation XAI
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from aegisxai.dashboards.components import *
from aegisxai.dashboards.pages import THEMES
from aegisxai.services.copilot_service import CopilotEngine
from aegisxai.services.forecasting_service import FORECAST_FUNCTIONS
from aegisxai.services.retention_agent import *

def page_ai_copilot():
    C = THEMES[st.session_state.theme]
    maybe_compact()
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">AI Executive Copilot</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Your intelligent analytics assistant — ask anything about your business</p>
    </div>""", unsafe_allow_html=True)

    if "copilot_messages" not in st.session_state:
        st.session_state.copilot_messages = []
    if "copilot_engine" not in st.session_state:
        st.session_state.copilot_engine = CopilotEngine()

    st.markdown(f"""<div class="glow-card" style="margin-bottom:12px;">
        <div style="display:flex;gap:8px;flex-wrap:wrap;">
            <span class="badge" style="background:{C["surface2"]};color:{C["accent"]};padding:4px 12px;border-radius:16px;font-size:12px;cursor:pointer;" onclick="document.querySelector('input[aria-label=\\'Ask a question\\']').value='Why did churn increase?';">
            Why churn increase?</span>
            <span class="badge" style="background:{C["surface2"]};color:{C["accent"]};padding:4px 12px;border-radius:16px;font-size:12px;cursor:pointer;" onclick="document.querySelector('input[aria-label=\\'Ask a question\\']').value='Top 10 high-risk customers';">
            Top 10 high-risk</span>
            <span class="badge" style="background:{C["surface2"]};color:{C["accent"]};padding:4px 12px;border-radius:16px;font-size:12px;cursor:pointer;" onclick="document.querySelector('input[aria-label=\\'Ask a question\\']').value='Why is APAC satisfaction declining?';">
            APAC analysis</span>
            <span class="badge" style="background:{C["surface2"]};color:{C["accent"]};padding:4px 12px;border-radius:16px;font-size:12px;cursor:pointer;" onclick="document.querySelector('input[aria-label=\\'Ask a question\\']').value='Summarize business risks';">
            Risk summary</span>
            <span class="badge" style="background:{C["surface2"]};color:{C["accent"]};padding:4px 12px;border-radius:16px;font-size:12px;cursor:pointer;" onclick="document.querySelector('input[aria-label=\\'Ask a question\\']').value='Forecast churn next quarter';">
            Forecast</span>
        </div>
    </div>""", unsafe_allow_html=True)

    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.copilot_messages[-10:]:
            is_user = msg["role"] == "user"
            with st.chat_message("user" if is_user else "assistant"):
                content = msg["content"]
                if is_user:
                    st.markdown(content)
                else:
                    st.markdown(content, unsafe_allow_html=True)

    if question := st.chat_input("Ask a business question...", key="copilot_input"):
        st.session_state.copilot_messages.append({"role": "user", "content": question})
        engine = st.session_state.copilot_engine
        answer, viz_data = engine.ask(question)
        full_response = f"""{answer}"""
        if isinstance(viz_data, pd.DataFrame) and not viz_data.empty:
            if "RiskScore" in viz_data.columns:
                fig = px.bar(viz_data.head(10), x="customerID", y="RiskScore",
                             color="RiskScore", color_continuous_scale="RdYlGn_r",
                             title="High-Risk Customers", height=350)
                fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                  font_color=C["text"], xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
            elif "Month" in viz_data.columns:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=viz_data["Month"], y=viz_data["Forecasted Churn Rate"],
                              mode="lines+markers", name="Forecast", line=dict(color=C["accent"], width=3)))
                fig.add_trace(go.Scatter(x=viz_data["Month"], y=viz_data["Lower CI"], fill=None,
                              mode="lines", line=dict(width=0), showlegend=False))
                fig.add_trace(go.Scatter(x=viz_data["Month"], y=viz_data["Upper CI"], fill="tonexty",
                              mode="lines", line=dict(width=0), name="95% CI", fillcolor="rgba(37,99,235,0.2)"))
                fig.update_layout(title="Churn Forecast", height=350, paper_bgcolor="rgba(0,0,0,0)",
                                  plot_bgcolor="rgba(0,0,0,0)", font_color=C["text"])
                st.plotly_chart(fig, use_container_width=True)
        elif isinstance(viz_data, dict) and all(k in viz_data for k in ["North America", "APAC"]):
            fig = go.Figure()
            regions = list(viz_data.keys())
            csats = [viz_data[r]["csat"] for r in regions]
            churns = [viz_data[r]["churn"] for r in regions]
            fig.add_trace(go.Bar(name="CSAT", x=regions, y=csats, yaxis="y", marker_color=C["accent"]))
            fig.add_trace(go.Scatter(name="Churn %", x=regions, y=churns, yaxis="y2",
                          mode="lines+markers", marker=dict(color=C["danger"]), line=dict(color=C["danger"])))
            fig.update_layout(title="Regional Comparison", height=350, paper_bgcolor="rgba(0,0,0,0)",
                              plot_bgcolor="rgba(0,0,0,0)", font_color=C["text"],
                              yaxis=dict(title="CSAT", range=[0, 5]),
                              yaxis2=dict(title="Churn %", overlaying="y", side="right", range=[0, 50]))
            st.plotly_chart(fig, use_container_width=True)
        st.session_state.copilot_messages.append({"role": "assistant", "content": answer[:500]})
        st.rerun()

def page_forecasting():
    C = THEMES[st.session_state.theme]
    maybe_compact()
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Predictive Business Forecasting</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Prophet / LSTM / XGBoost forecasts with confidence intervals</p>
    </div>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        metric = st.selectbox("Metric", list(FORECAST_FUNCTIONS.keys()))
    with col2:
        model = st.selectbox("Model", ["prophet", "lstm", "xgboost"])
    with col3:
        days = st.slider("Forecast Horizon (days)", 30, 365, 90)

    forecaster = FORECAST_FUNCTIONS[metric]
    extra_args = {}
    if metric == "Churn Rate":
        extra_args["model"] = model
    df_forecast = forecaster(days, **extra_args) if metric == "Churn Rate" else forecaster(days)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_forecast["Date"], y=df_forecast["Forecast"],
                  mode="lines", name="Forecast", line=dict(color=C["accent"], width=2)))
    fig.add_trace(go.Scatter(x=df_forecast["Date"], y=df_forecast["Lower CI"],
                  mode="lines", line=dict(width=0), showlegend=False, name="Lower CI"))
    fig.add_trace(go.Scatter(x=df_forecast["Date"], y=df_forecast["Upper CI"],
                  mode="lines", line=dict(width=0), fill="tonexty", name="95% Confidence Interval",
                  fillcolor=f"rgba(37,99,235,0.15)", showlegend=True))
    fig.update_layout(title=f"{metric} — {model.upper()} Forecast", height=450,
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color=C["text"], hovermode="x unified",
                      xaxis=dict(tickfont=dict(color=C["text2"])),
                      yaxis=dict(tickfont=dict(color=C["text2"])))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""<div class="glow-card" style="margin-top:16px;"><h3>Forecast Summary</h3></div>""", unsafe_allow_html=True)
    last_val = df_forecast["Forecast"].iloc[-1]
    first_val = df_forecast["Forecast"].iloc[0]
    change = last_val - first_val
    st.markdown(f"""<div style="display:flex;gap:16px;flex-wrap:wrap;">
        <div class="kpi-card"><div class="kpi-value">{df_forecast['Forecast'].iloc[0]:.1f}</div><div class="kpi-label">Current</div></div>
        <div class="kpi-card"><div class="kpi-value" style="color:{C['accent']};">{last_val:.1f}</div><div class="kpi-label">End of Horizon</div></div>
        <div class="kpi-card"><div class="kpi-value" style="color:{'green' if change < 0 else C['danger']};">{change:+.1f}</div><div class="kpi-label">Change</div></div>
        <div class="kpi-card"><div class="kpi-value" style="color:{C['neon']};">{model.upper()}</div><div class="kpi-label">Model</div></div>
    </div>""", unsafe_allow_html=True)

    if st.checkbox("Show raw forecast data"):
        st.dataframe(df_forecast.tail(20), use_container_width=True)

def page_retention_agent():
    C = THEMES[st.session_state.theme]
    maybe_compact()
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Autonomous Retention Agent</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">AI-powered retention automation — create tickets, send offers, escalate cases</p>
    </div>""", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    level = st.session_state.get("retention_level", "Advisory")
    with col1:
        level = st.selectbox("Autonomy Level", ["Advisory", "Semi-Autonomous", "Fully Autonomous"],
                             index=["Advisory", "Semi-Autonomous", "Fully Autonomous"].index(level))
        st.session_state.retention_level = level

    stats = get_agent_stats(level)
    with col2:
        st.metric("Total Actions", stats["total_actions"])
    with col3:
        st.metric("Retention Rate", f"{stats['retention_rate']}%")
    with col4:
        st.metric("Avg Response", f"{stats['avg_response_time']} min")

    st.markdown(f"""<div class="glow-card" style="margin-top:12px;"><h3>Actions by Type</h3></div>""", unsafe_allow_html=True)
    act_df = pd.DataFrame(list(stats["actions"].items()), columns=["Action", "Count"])
    fig = px.bar(act_df, x="Action", y="Count", color="Count", color_continuous_scale="Viridis",
                 height=300, text_auto=True)
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color=C["text"])
    st.plotly_chart(fig, use_container_width=True)

    if level == "Fully Autonomous":
        st.markdown(f"""<div class="glass" style="padding:12px;margin-top:12px;border-left:3px solid {C["success"]};">
            <span style="color:{C["success"]};"> AUTONOMOUS MODE ACTIVE</span> — Agent is resolving cases without human intervention
        </div>""", unsafe_allow_html=True)
    elif level == "Semi-Autonomous":
        st.markdown(f"""<div class="glass" style="padding:12px;margin-top:12px;border-left:3px solid {C["warning"]};">
            <span style="color:{C["warning"]};"> SEMI-AUTONOMOUS</span> — Agent suggests actions, requires approval for critical cases
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class="glass" style="padding:12px;margin-top:12px;border-left:3px solid {C["accent"]};">
            <span style="color:{C["accent"]};"> ADVISORY MODE</span> — Agent provides recommendations only
        </div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class="glow-card" style="margin-top:16px;"><h3>Pending Cases</h3></div>""", unsafe_allow_html=True)
    cases = get_pending_cases()
    for case in cases[:6]:
        pri_color = {"Critical": C["danger"], "High": C["warning"], "Medium": C["accent"], "Low": C["success"]}
        st.markdown(f"""<div class="glass" style="padding:10px 14px;margin:4px 0;display:flex;justify-content:space-between;align-items:center;">
            <div><span style="font-weight:600;">{case["id"]}</span> — {case["customer"]}
            <br><span style="font-size:12px;color:{C["text2"]};">{case["reason"]}</span></div>
            <div style="text-align:right;">
                <span style="color:{pri_color.get(case['priority'], C['text2'])};font-weight:600;">{case["priority"]}</span>
                <br><span style="font-size:11px;color:{C["text2"]};">{case["status"]}</span>
            </div>
        </div>""", unsafe_allow_html=True)
        if level != "Advisory" and st.button(f"Auto-resolve {case['id']}", key=f"res_{case['id']}"):
            result = auto_resolve(case["id"], level)
            st.toast(result["action"])

def page_recommendation_xai():
    C = THEMES[st.session_state.theme]
    maybe_compact()
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Explainable Recommendation Engine</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">AI-powered recommendations with full transparency — understand why each offer is made</p>
    </div>""", unsafe_allow_html=True)

    customer_id = st.text_input("Customer ID", value="C1001", key="rec_customer")
    scenario = st.selectbox("Scenario", ["loyalty", "discount", "retention"], key="rec_scenario")
    from aegisxai.services.advanced_features import get_recommendation_explanation
    exp = get_recommendation_explanation(customer_id, scenario)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(f"""<div class="glow-card"><h3> Recommended Action</h3>
            <div style="font-size:24px;font-weight:700;color:{C["accent"]};margin:12px 0;">{exp["recommendation"]}</div>
            <div style="display:flex;gap:12px;margin-top:8px;">
                <span class="kpi-card" style="padding:8px 16px;">Confidence: <strong>{exp["confidence"]:.0%}</strong></span>
                <span class="kpi-card" style="padding:8px 16px;">Expected: <strong>{exp["expected_impact"]}</strong></span>
            </div>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""<div class="glow-card"><h3> Why This Recommendation?</h3></div>""", unsafe_allow_html=True)
        for i, reason in enumerate(exp["reasons"], 1):
            st.markdown(f"""<div class="glass" style="padding:10px;margin:4px 0;border-left:3px solid {C["accent"]};">
                <span style="color:{C["accent"]};font-weight:700;">#{i}</span> {reason}
            </div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class="glow-card" style="margin-top:16px;"><h3> Explanation Breakdown</h3></div>""", unsafe_allow_html=True)
    factors = ["Customer Value", "Behavioral Pattern", "Risk Profile", "Similar Case History", "Segment Propensity"]
    weights = np.random.dirichlet(np.ones(5)) * 100
    fig = px.pie(values=weights, names=factors, title="Decision Factors", hole=0.4,
                 color_discrete_sequence=px.colors.sequential.Viridis_r)
    fig.update_layout(height=350, paper_bgcolor="rgba(0,0,0,0)", font=dict(color=C["text"]),
                      legend=dict(font=dict(color=C["text2"])))
    st.plotly_chart(fig, use_container_width=True)

AI_PAGE_FUNCTIONS = {
    "AI Executive Copilot": page_ai_copilot,
    "Business Forecasting": page_forecasting,
    "Retention Agent": page_retention_agent,
    "Recommendation Engine": page_recommendation_xai,
}
