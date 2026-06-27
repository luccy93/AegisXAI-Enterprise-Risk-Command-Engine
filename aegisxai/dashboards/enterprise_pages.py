"""
AEGIS-XAI Enterprise Feature Pages
CLV, Anomaly, Integration Hub, Pipeline Monitor, Compliance
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import io, base64, random

from aegisxai.models.features import load_data
from aegisxai.utils.helpers import audit_log, format_currency
from aegisxai.services.clv_service import generate_clv_data, predict_clv_for_customer
from aegisxai.services.anomaly_service import generate_anomaly_data, detect_anomalies, get_anomaly_alerts
from aegisxai.services.compliance_service import generate_compliance_data, get_data_map
from aegisxai.services.integration_service import generate_integration_data, run_sync, get_integration_health
from aegisxai.services.pipeline_service import generate_pipeline_data, get_data_quality_score
from aegisxai.dashboards.pages import THEMES


def page_clv_dashboard():
    C = THEMES[st.session_state.theme]
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Customer Lifetime Value</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Predict, segment, and protect high-value customer revenue</p>
    </div>""", unsafe_allow_html=True)
    clv = generate_clv_data()
    k1, k2, k3, k4 = st.columns(4)
    with k1: st.metric("Average CLV", format_currency(clv["avg_clv"]), "+2.3%")
    with k2: st.metric("High Value", f'{clv["segments"]["High Value"]}%', "+1%")
    with k3: st.metric("Threshold", format_currency(clv["high_value_threshold"]), "")
    with k4: st.metric("At-Risk HV Customers", len(clv["at_risk_high_value"]), "⚠ Alert")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""<div class="glow-card"><h3>CLV Distribution</h3></div>""", unsafe_allow_html=True)
        fig = px.histogram(clv["clv_distribution"], nbins=30, title="Customer Lifetime Value Distribution",
                           labels={"value": "CLV ($)", "count": "Customers"},
                           color_discrete_sequence=[C["accent"]])
        fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color=C["text"], xaxis=dict(tickfont=dict(color=C["text2"])),
                          yaxis=dict(tickfont=dict(color=C["text2"])))
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.markdown(f"""<div class="glow-card"><h3>CLV Segments</h3></div>""", unsafe_allow_html=True)
        seg_df = pd.DataFrame(list(clv["segments"].items()), columns=["Segment", "%"])
        colors = {"High Value": C["success"], "Medium Value": C["accent"], "Low Value": C["warning"]}
        fig = px.pie(seg_df, values="%", names="Segment", color="Segment",
                     color_discrete_map=colors, hole=0.5)
        fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", font={"color": C["text"]},
                          legend=dict(font=dict(color=C["text2"])))
        st.plotly_chart(fig, use_container_width=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""<div class="glow-card"><h3>CLV by Contract</h3></div>""", unsafe_allow_html=True)
        bc_df = pd.DataFrame(list(clv["clv_by_contract"].items()), columns=["Contract", "Avg CLV"])
        fig = px.bar(bc_df, x="Contract", y="Avg CLV", color="Avg CLV",
                     color_continuous_scale=["#F59E0B", "#10B981"], text_auto=".0f")
        fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color=C["text"], xaxis=dict(tickfont=dict(color=C["text2"])),
                          coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.markdown(f"""<div class="glow-card"><h3>CLV by Region</h3></div>""", unsafe_allow_html=True)
        br_df = pd.DataFrame(list(clv["clv_by_region"].items()), columns=["Region", "Avg CLV"])
        fig = px.bar(br_df, x="Region", y="Avg CLV", color="Avg CLV",
                     color_continuous_scale=px.colors.sequential.Viridis, text_auto=".0f")
        fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color=C["text"], xaxis=dict(tickfont=dict(color=C["text2"])),
                          coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"""<div class="glow-card" style="margin-top:16px;"><h3>At-Risk High Value Customers</h3></div>""", unsafe_allow_html=True)
    at_risk = clv["at_risk_high_value"]
    if at_risk:
        ar_df = pd.DataFrame(at_risk)
        st.dataframe(ar_df, use_container_width=True, height=300)
    st.markdown(f"""<div class="glow-card" style="margin-top:16px;"><h3>CLV Simulator</h3></div>""", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1: tenure_in = st.slider("Tenure (months)", 1, 72, 12)
    with col2: contract_in = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
    with col3: monthly_in = st.slider("Monthly Charges ($)", 20.0, 120.0, 65.0)
    total_in = monthly_in * tenure_in
    result = predict_clv_for_customer(tenure_in, contract_in, monthly_in, total_in)
    sc = {"High Value": C["success"], "Medium Value": C["accent"], "Low Value": C["warning"]}
    st.markdown(f"""<div class="glass" style="padding:20px;margin-top:8px;display:flex;gap:24px;align-items:center;">
        <div><span style="color:{C["text2"]};">Predicted CLV:</span>
             <span style="font-size:28px;font-weight:800;color:{C["neon"]};">{format_currency(result['predicted_clv'])}</span></div>
        <div><span style="color:{C["text2"]};">Segment:</span>
             <span style="font-size:18px;font-weight:600;color:{sc.get(result['segment'], C['text'])};">{result['segment']}</span></div>
        <div><span style="color:{C["text2"]};">Confidence:</span>
             <span style="font-size:16px;color:{C["accent"]};">{result['confidence_interval'][0]:.0f}-{result['confidence_interval'][1]:.0f}</span></div>
    </div>""", unsafe_allow_html=True)


def page_anomaly_detection():
    C = THEMES[st.session_state.theme]
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Anomaly Detection Engine</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Unsupervised behavioral anomaly detection using Isolation Forest</p>
    </div>""", unsafe_allow_html=True)
    anom = generate_anomaly_data()
    k1, k2, k3, k4 = st.columns(4)
    with k1: st.metric("Total Anomalies", anom["total_anomalies"], "+3 vs yesterday")
    with k2: st.metric("Anomaly Rate", f'{anom["anomaly_rate"]:.1f}%', "+0.2%")
    with k3: st.metric("Critical", anom["severity_distribution"]["Critical"], "⚠ Needs attention")
    with k4: st.metric("High", anom["severity_distribution"]["High"], "")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""<div class="glow-card"><h3>Anomaly by Type</h3></div>""", unsafe_allow_html=True)
        bt_df = pd.DataFrame(list(anom["by_type"].items()), columns=["Type", "Count"])
        fig = px.bar(bt_df, x="Type", y="Count", color="Count",
                     color_continuous_scale=["#10B981", "#F59E0B", "#EF4444"], text_auto=".0f")
        fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color=C["text"], xaxis=dict(tickfont=dict(color=C["text2"])),
                          coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.markdown(f"""<div class="glow-card"><h3>Severity Distribution</h3></div>""", unsafe_allow_html=True)
        sev_df = pd.DataFrame(list(anom["severity_distribution"].items()), columns=["Severity", "Count"])
        sc = {"Critical": C["danger"], "High": C["warning"], "Medium": C["accent"]}
        fig = px.pie(sev_df, values="Count", names="Severity", color="Severity",
                     color_discrete_map=sc, hole=0.5)
        fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", font={"color": C["text"]},
                          legend=dict(font=dict(color=C["text2"])))
        st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"""<div class="glow-card"><h3>30-Day Anomaly Trend</h3></div>""", unsafe_allow_html=True)
    trend_df = pd.DataFrame(anom["daily_trend"])
    fig = px.line(trend_df, x="date", y="anomalies", markers=True,
                  title="Daily Anomaly Count", labels={"anomalies": "Anomalies", "date": "Date"})
    fig.update_traces(line=dict(color=C["danger"], width=2))
    fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color=C["text"], xaxis=dict(tickfont=dict(color=C["text2"])),
                      yaxis=dict(tickfont=dict(color=C["text2"])))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"""<div class="glow-card" style="margin-top:16px;"><h3>Recent Anomalies</h3></div>""", unsafe_allow_html=True)
    recent = anom["recent_anomalies"]
    if recent:
        rdf = pd.DataFrame(recent)
        st.dataframe(rdf, use_container_width=True, height=350)
    st.markdown(f"""<div class="glow-card" style="margin-top:16px;"><h3>Anomaly Detector Simulator</h3></div>""", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        usage_drop = st.slider("Usage Drop (%)", 0, 100, 30, key="anom_usage")
        support_tickets = st.slider("Support Tickets (30d)", 0, 20, 8, key="anom_tickets")
    with col2:
        sentiment_drop = st.slider("Sentiment Change", -1.0, 1.0, -0.3, step=0.1, key="anom_sentiment")
        payment_failures = st.slider("Payment Failures", 0, 10, 2, key="anom_payments")
    if st.button("Run Detection", key="detect_btn", use_container_width=True):
        input_data = {"usage_drop": usage_drop, "support_tickets": support_tickets,
                      "sentiment_change": sentiment_drop, "payment_failures": payment_failures}
        result = detect_anomalies(input_data)
        sc2 = {"Critical": C["danger"], "High": C["warning"], "Medium": C["accent"], "Low": C["text2"]}
        st.markdown(f"""<div class="glass" style="padding:16px;margin-top:8px;">
            <div style="display:flex;gap:20px;align-items:center;">
                <span style="font-size:16px;color:{C["text2"]};">Anomaly:</span>
                <span style="font-size:20px;font-weight:700;color:{sc2.get(result['severity'], C['text'])};">{'⚠ DETECTED' if result['is_anomaly'] else '✅ CLEAR'}</span>
                <span style="font-size:14px;color:{C["text2"]};">Score:</span>
                <span style="font-size:18px;color:{C["neon"]};">{result['anomaly_score']:.2f}</span>
                <span style="font-size:14px;color:{C["text2"]};">Type:</span>
                <span style="font-size:16px;color:{C["accent"]};">{result['anomaly_type']}</span>
                <span style="font-size:14px;color:{C["text2"]};">Severity:</span>
                <span style="font-size:16px;color:{sc2.get(result['severity'], C['text'])};">{result['severity']}</span>
            </div>
        </div>""", unsafe_allow_html=True)


def page_integration_hub():
    C = THEMES[st.session_state.theme]
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Integration Hub</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Connected services, data pipelines, and sync status</p>
    </div>""", unsafe_allow_html=True)
    integ = generate_integration_data()
    k1, k2, k3, k4 = st.columns(4)
    with k1: st.metric("Integrations", len(integ["integrations"]), "")
    with k2: st.metric("Records Synced", f'{integ["total_records_synced"]/1e6:.1f}M', "+12K today")
    with k3: st.metric("Sync Frequency", integ["sync_frequency"], "")
    with k4: st.metric("Failed (24h)", integ["failed_syncs_24h"], "⚠")
    st.markdown(f"""<div class="glow-card"><h3>Integration Status</h3></div>""", unsafe_allow_html=True)
    for integration in integ["integrations"]:
        sc = {"Connected": C["success"], "Disconnected": C["danger"], "Error": C["warning"]}
        hc = {"Healthy": C["success"], "Degraded": C["warning"], "Down": C["danger"]}
        status_color = sc.get(integration["status"], C["text2"])
        health_color = hc.get(integration["health"], C["text2"])
        st.markdown(f"""<div class="glass" style="padding:12px 16px;margin:4px 0;display:flex;justify-content:space-between;align-items:center;">
            <div style="display:flex;align-items:center;gap:12px;">
                <span style="font-size:16px;">{integration["name"]}</span>
                <span style="background:{status_color};color:white;padding:1px 8px;border-radius:4px;font-size:10px;font-weight:600;">{integration["status"]}</span>
                <span style="font-size:11px;color:{C["text2"]};">{integration["connection_type"]}</span>
            </div>
            <div style="display:flex;align-items:center;gap:16px;font-size:12px;color:{C["text2"]};">
                <span>Health: <span style="color:{health_color};">{integration["health"]}</span></span>
                <span>Last: {integration["last_sync"]}</span>
                <span>Records: {integration["records_imported"]:,}</span>
            </div>
        </div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="glow-card" style="margin-top:16px;"><h3>Sync History</h3></div>""", unsafe_allow_html=True)
    sync_df = pd.DataFrame(integ["sync_history"])
    st.dataframe(sync_df, use_container_width=True, height=250)


def page_pipeline_monitor():
    C = THEMES[st.session_state.theme]
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Data Pipeline Monitor</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Real-time pipeline health, data freshness, and data quality scoring</p>
    </div>""", unsafe_allow_html=True)
    pipe = generate_pipeline_data()
    dq = get_data_quality_score()
    k1, k2, k3, k4 = st.columns(4)
    with k1: st.metric("Rows Today", f'{pipe["total_rows_processed_today"]:,}', "+12%")
    with k2: st.metric("Avg Duration", pipe["avg_pipeline_duration"], "-0.3 min")
    with k3: st.metric("Failed Today", pipe["failed_pipelines_today"], "⚠")
    with k4: st.metric("Data Quality", f'{dq["overall"]}%', "+2%")
    st.markdown(f"""<div class="glow-card"><h3>Pipeline Status</h3></div>""", unsafe_allow_html=True)
    for p in pipe["pipelines"]:
        sc = {"Running": C["success"], "Failed": C["danger"], "Paused": C["warning"]}
        st.markdown(f"""<div class="glass" style="padding:12px 16px;margin:4px 0;display:flex;justify-content:space-between;align-items:center;">
            <div style="display:flex;align-items:center;gap:12px;">
                <span style="font-size:14px;font-weight:500;">{p["name"]}</span>
                <span style="background:{sc.get(p["status"], C["text2"])};color:white;padding:1px 8px;border-radius:4px;font-size:10px;font-weight:600;">{p["status"]}</span>
            </div>
            <div style="font-size:12px;color:{C["text2"]};display:flex;gap:16px;">
                <span>Rows: {p["rows_processed"]:,}</span>
                <span>Duration: {p["duration"]}</span>
                <span>Freshness: {p.get("freshness_min", "N/A")} min</span>
            </div>
        </div>""", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""<div class="glow-card" style="margin-top:16px;"><h3>Data Quality Score</h3></div>""", unsafe_allow_html=True)
        dq_df = pd.DataFrame(list(dq.items()), columns=["Dimension", "Score"])
        fig = px.bar(dq_df, x="Dimension", y="Score", color="Score",
                     color_continuous_scale=["#EF4444", "#F59E0B", "#10B981"],
                     text_auto=".0f", range_y=[0, 100])
        fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color=C["text"], xaxis=dict(tickfont=dict(color=C["text2"])),
                          coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.markdown(f"""<div class="glow-card" style="margin-top:16px;"><h3>Data Freshness</h3></div>""", unsafe_allow_html=True)
        fresh = pipe["data_freshness"]
        fdf = pd.DataFrame(fresh)
        fdf["staleness_hours"] = fdf["staleness_hours"].astype(float)
        fig = px.bar(fdf, x="table", y="staleness_hours", color="status",
                     color_discrete_map={"Fresh": C["success"], "Stale": C["warning"], "Critical": C["danger"]},
                     text_auto=".1f", labels={"staleness_hours": "Hours Since Update", "table": "Table"})
        fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color=C["text"], xaxis=dict(tickfont=dict(color=C["text2"])),
                          yaxis=dict(tickfont=dict(color=C["text2"])), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"""<div class="glow-card" style="margin-top:16px;"><h3>Pipeline Runs (Last 30)</h3></div>""", unsafe_allow_html=True)
    runs_df = pd.DataFrame(pipe["pipeline_runs"])
    st.dataframe(runs_df, use_container_width=True, height=250)


def maybe_compact():
    if st.session_state.get("mobile_layout", False):
        st.markdown("<style>.main .block-container{padding:1rem 0.5rem!important;max-width:100%!important;}</style>", unsafe_allow_html=True)

def page_executive_report_builder():
    C = THEMES[st.session_state.theme]; maybe_compact()
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Executive Report Builder</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Select KPIs and generate a board-ready PDF report</p>
    </div>""", unsafe_allow_html=True)
    available_cards = [
        ("Churn Rate", "pie", True), ("CSAT Score", "gauge", True),
        ("NPS", "gauge", True), ("Revenue at Risk", "bar", True),
        ("Customer Happiness", "number", True), ("Anomaly Count", "number", True),
        ("CLV Distribution", "histogram", False), ("Sentiment Breakdown", "pie", False),
        ("SLA Compliance", "gauge", False), ("Engagement Rate", "number", False)
    ]
    st.markdown(f"""<div class="glow-card"><h3>Select KPIs for Report</h3></div>""", unsafe_allow_html=True)
    cols = st.columns(2)
    selected = []
    for i, (name, ctype, default) in enumerate(available_cards):
        with cols[i % 2]:
            if st.checkbox(name, value=default, key=f"rb_{i}"):
                selected.append(name)
    st.markdown(f"""<div style="display:flex;gap:12px;margin-top:16px;">""", unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        report_title = st.text_input("Report Title", "AegisXAI Executive Summary", key="rb_title")
    with col_b:
        report_format = st.selectbox("Format", ["PDF", "HTML", "CSV"], key="rb_format")
    with col_c:
        include_charts = st.checkbox("Include Charts", True, key="rb_charts")
    if st.button(" Generate Report", use_container_width=True):
        if not selected:
            st.warning("Select at least one KPI")
        else:
            buf = io.BytesIO()
            html = f"""<html><body style="font-family:sans-serif;padding:40px;background:#fff;">
                <h1 style="color:#2563EB;">{report_title}</h1>
                <p style="color:#666;">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
                <p style="color:#666;">KPIs: {', '.join(selected)}</p>
                <hr>
                <table style="width:100%;border-collapse:collapse;">
                    <tr><th style="text-align:left;padding:8px;border-bottom:2px solid #2563EB;">Metric</th>
                        <th style="text-align:right;padding:8px;border-bottom:2px solid #2563EB;">Value</th></tr>
            """
            values = {"Churn Rate":"26.5%", "CSAT Score":"4.2/5", "NPS":"+46", "Revenue at Risk":"$1.2M",
                      "Customer Happiness":"74%", "Anomaly Count":"47", "CLV Distribution":"$1,850 avg",
                      "Sentiment Breakdown":"58% Positive", "SLA Compliance":"94%", "Engagement Rate":"67%"}
            for s in selected:
                v = values.get(s, "N/A")
                html += f'<tr><td style="padding:6px;border-bottom:1px solid #eee;">{s}</td><td style="padding:6px;border-bottom:1px solid #eee;text-align:right;font-weight:bold;">{v}</td></tr>'
            html += "</table><hr><p style='color:#999;font-size:12px;'>AegisXAI v4.0 | Confidential</p></body></html>"
            buf.write(html.encode())
            b64 = base64.b64encode(buf.getvalue()).decode()
            sfx = "html" if report_format == "HTML" else "pdf"
            st.markdown(f"""<div class="glass" style="padding:20px;margin-top:16px;text-align:center;">
                <span style="font-size:18px;color:{C["success"]};"> Report generated!</span>
                <div style="margin-top:12px;">
                    <a href="data:text/html;base64,{b64}" download="report.{sfx}"
                       style="background:{C["accent"]};color:white;padding:8px 24px;border-radius:8px;text-decoration:none;font-weight:600;">
                       Download {report_format}</a>
                </div>
            </div>""", unsafe_allow_html=True)

def page_alert_webhooks():
    C = THEMES[st.session_state.theme]; maybe_compact()
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Alert Webhooks</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Real-time simulated Slack webhook notifications</p>
    </div>""", unsafe_allow_html=True)
    if not st.session_state.get("slack_webhooks"):
        st.session_state.slack_webhooks = [
            {"channel": "#alerts", "message": "Critical churn risk detected for C1024 (91%)", "time": "3 min ago", "status": "sent"},
            {"channel": "#monitoring", "message": "Data drift warning: Model AUC dropped 2.1%", "time": "12 min ago", "status": "sent"},
            {"channel": "#cx-team", "message": "CSAT score dropped to 4.1 in APAC region", "time": "28 min ago", "status": "sent"},
        ]
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"""<div class="glow-card"><h3> Webhook Stream</h3></div>""", unsafe_allow_html=True)
        for wh in reversed(st.session_state.slack_webhooks[-15:]):
            sc = {"sent": C["success"], "failed": C["danger"], "pending": C["warning"]}
            st.markdown(f"""<div class="glass" style="padding:10px 14px;margin:4px 0;display:flex;justify-content:space-between;align-items:center;">
                <div style="display:flex;align-items:center;gap:10px;">
                    <span style="background:{C["surface2"]};padding:2px 8px;border-radius:4px;font-size:11px;color:{C["accent"]};">{wh["channel"]}</span>
                    <span style="font-size:13px;">{wh["message"]}</span>
                </div>
                <div style="display:flex;align-items:center;gap:8px;">
                    <span style="font-size:11px;color:{C["text2"]};">{wh["time"]}</span>
                    <span style="color:{sc.get(wh['status'], C['text2'])};">{"●" if wh["status"]=="sent" else "○"}</span>
                </div>
            </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="glow-card"><h3> Send Test Webhook</h3></div>""", unsafe_allow_html=True)
        with st.form("webhook_form"):
            channel = st.selectbox("Channel", ["#alerts", "#monitoring", "#cx-team", "#general", "#engineering"])
            severity = st.selectbox("Severity", ["Critical", "High", "Medium", "Info"])
            custom_msg = st.text_input("Message", placeholder="e.g., Customer churn alert...")
            if st.form_submit_button(" Send", use_container_width=True):
                msg = custom_msg or f"Test {severity} alert from AegisXAI"
                st.session_state.slack_webhooks.append({
                    "channel": channel, "message": msg,
                    "time": "Just now", "status": "sent"
                })
                audit_log("WEBHOOK", f"Sent webhook to {channel}: {msg}", st.session_state.username)
                st.rerun()
    st.markdown(f"""<div class="glow-card" style="margin-top:16px;"><h3>Webhook Statistics</h3></div>""", unsafe_allow_html=True)
    whs = st.session_state.slack_webhooks
    sent = sum(1 for w in whs if w["status"] == "sent")
    st.markdown(f"""<div style="display:flex;gap:16px;">
        <div class="kpi-card"><div class="kpi-value" style="color:{C["success"]};">{sent}</div><div class="kpi-label">Sent</div></div>
        <div class="kpi-card"><div class="kpi-value" style="color:{C["neon"]};">{len(whs)}</div><div class="kpi-label">Total</div></div>
        <div class="kpi-card"><div class="kpi-value" style="color:{C["accent"]};">3</div><div class="kpi-label">Channels</div></div>
    </div>""", unsafe_allow_html=True)

def page_model_explainability_report():
    C = THEMES[st.session_state.theme]; maybe_compact()
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Model Explainability Report</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Auto-generated SHAP summary, feature importance, and performance metrics</p>
    </div>""", unsafe_allow_html=True)
    metrics = {"Accuracy": 0.796, "Precision": 0.782, "Recall": 0.641, "F1": 0.704, "ROC AUC": 0.847}
    st.markdown(f"""<div class="glow-card"><h3>Model Performance</h3></div>""", unsafe_allow_html=True)
    mdf = pd.DataFrame(list(metrics.items()), columns=["Metric", "Value"])
    fig = px.bar(mdf, x="Metric", y="Value", color="Value", text_auto=".3f",
                 color_continuous_scale=["#EF4444", "#F59E0B", "#10B981"], range_y=[0, 1])
    fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color=C["text"], xaxis=dict(tickfont=dict(color=C["text2"])),
                      coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"""<div class="glow-card" style="margin-top:16px;"><h3>Top 10 Feature Importance (SHAP)</h3></div>""", unsafe_allow_html=True)
    features = ["Contract", "Tenure", "MonthlyCharges", "InternetService", "TechSupport",
                "OnlineSecurity", "PaymentMethod", "TotalCharges", "ServiceCount", "PaperlessBilling"]
    importance = [0.245, 0.182, 0.128, 0.095, 0.072, 0.058, 0.046, 0.038, 0.025, 0.018]
    fidf = pd.DataFrame({"Feature": features, "Importance": importance})
    fig = px.bar(fidf, x="Importance", y="Feature", orientation="h", color="Importance",
                 color_continuous_scale=["#2563EB", "#06B6D4", "#10B981"],
                 text_auto=".3f", title="Mean |SHAP Value|")
    fig.update_layout(height=400, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color=C["text"], yaxis=dict(tickfont=dict(color=C["text2"]), autorange="reversed"),
                      xaxis=dict(tickfont=dict(color=C["text2"])), coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"""<div class="glow-card" style="margin-top:16px;"><h3>Confusion Matrix</h3></div>""", unsafe_allow_html=True)
    cm = np.array([[982, 108], [154, 278]])
    fig = px.imshow(cm, text_auto=True, color_continuous_scale="Blues",
                    x=["Predicted No", "Predicted Yes"], y=["Actual No", "Actual Yes"],
                    title="Confusion Matrix")
    fig.update_layout(height=350, paper_bgcolor="rgba(0,0,0,0)", font={"color": C["text"]},
                      xaxis=dict(tickfont=dict(color=C["text2"])), yaxis=dict(tickfont=dict(color=C["text2"])))
    st.plotly_chart(fig, use_container_width=True)
    if st.button(" Export Explainability Report (HTML)", use_container_width=True):
        buf = io.BytesIO()
        html = f"""<html><body style="font-family:sans-serif;padding:40px;">
            <h1>AegisXAI Model Explainability Report</h1>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
            <hr><h2>Model Performance</h2><table border=1>
            <tr><th>Metric</th><th>Value</th></tr>"""
        for k, v in metrics.items():
            html += f"<tr><td>{k}</td><td>{v:.3f}</td></tr>"
        html += "</table><hr><h2>Top Features</h2><ol>"
        for f, imp in zip(features[:10], importance[:10]):
            html += f"<li>{f}: {imp:.3f}</li>"
        html += "</ol><hr><p>AegisXAI v4.0 | XGBoost+Optuna</p></body></html>"
        buf.write(html.encode())
        b64 = base64.b64encode(buf.getvalue()).decode()
        st.markdown(f"""<div style="margin-top:8px;"><a href="data:text/html;base64,{b64}" download="model_explainability.html"
            style="background:{C["accent"]};color:white;padding:8px 24px;border-radius:8px;text-decoration:none;font-weight:600;">
            Download Report</a></div>""", unsafe_allow_html=True)

def page_compliance_dashboard():
    C = THEMES[st.session_state.theme]; maybe_compact()
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Compliance & Governance</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">GDPR data map, consent tracking, retention policies, and privacy request management</p>
    </div>""", unsafe_allow_html=True)
    comp = generate_compliance_data()
    k1, k2, k3, k4 = st.columns(4)
    with k1: st.metric("GDPR Compliance", f'{comp["gdpr_compliance_pct"]:.0f}%', "+2%")
    with k2: st.metric("Consent Rate", f'{comp["consent_rate"]:.0f}%', "+1%")
    with k3: st.metric("Active Activities", len(comp["active_processing_activities"]), "")
    with k4: st.metric("Privacy Requests", len(comp["privacy_requests"]), "+2 new")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""<div class="glow-card"><h3>Data Categories</h3></div>""", unsafe_allow_html=True)
        dc_df = pd.DataFrame(list(comp["data_categories"].items()), columns=["Category", "%"])
        fig = px.pie(dc_df, values="%", names="Category", hole=0.5,
                     color_discrete_sequence=[C["accent"], C["danger"], C["warning"], C["success"]])
        fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", font={"color": C["text"]},
                          legend=dict(font=dict(color=C["text2"])))
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.markdown(f"""<div class="glow-card"><h3>Consent by Purpose</h3></div>""", unsafe_allow_html=True)
        cp_df = pd.DataFrame(list(comp["consent_by_purpose"].items()), columns=["Purpose", "Rate"])
        fig = px.bar(cp_df, x="Purpose", y="Rate", color="Rate",
                     color_continuous_scale=["#EF4444", "#F59E0B", "#10B981"],
                     text_auto=".0f", range_y=[0, 100])
        fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color=C["text"], xaxis=dict(tickfont=dict(color=C["text2"])),
                          coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"""<div class="glow-card" style="margin-top:16px;"><h3>Data Retention</h3></div>""", unsafe_allow_html=True)
    rt = comp["data_retention_summary"]
    rdf = pd.DataFrame(list(rt.items()), columns=["Status", "%"])
    colors = {"Compliant": C["success"], "Expiring Soon": C["warning"], "Overdue": C["danger"]}
    fig = px.pie(rdf, values="%", names="Status", color="Status",
                 color_discrete_map=colors, hole=0.5)
    fig.update_layout(height=250, paper_bgcolor="rgba(0,0,0,0)", font={"color": C["text"]},
                      legend=dict(font=dict(color=C["text2"])))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"""<div class="glow-card" style="margin-top:16px;"><h3>Processing Activities</h3></div>""", unsafe_allow_html=True)
    pa_df = pd.DataFrame(comp["active_processing_activities"])
    st.dataframe(pa_df, use_container_width=True, height=250)
    st.markdown(f"""<div class="glow-card" style="margin-top:16px;"><h3>Recent Access Logs</h3></div>""", unsafe_allow_html=True)
    al_df = pd.DataFrame(comp["access_logs_recent"])
    st.dataframe(al_df, use_container_width=True, height=250)


ENTERPRISE_PAGE_FUNCTIONS = {
    "CLV Dashboard": page_clv_dashboard,
    "Anomaly Detection": page_anomaly_detection,
    "Integration Hub": page_integration_hub,
    "Pipeline Monitor": page_pipeline_monitor,
    "Compliance": page_compliance_dashboard,
    "Executive Reports": page_executive_report_builder,
    "Alert Webhooks": page_alert_webhooks,
    "Model Explainability": page_model_explainability_report,
}
