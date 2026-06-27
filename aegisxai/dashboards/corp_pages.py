"""
Corporate & Enterprise Pages - Governance, Knowledge, Search, Experimentation, Innovation, Voice, ESG, Mobile
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
from aegisxai.dashboards.components import *
from aegisxai.dashboards.pages import THEMES
from aegisxai.services.advanced_features import *

def page_governance():
    C = THEMES[st.session_state.theme]
    maybe_compact()
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Enterprise Governance Center</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">GDPR, SOC2, ISO 27001 — data privacy, compliance, model fairness, bias detection</p>
    </div>""", unsafe_allow_html=True)

    gov = get_governance_data()
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("GDPR Compliance", f'{gov["gdpr_compliance"]}%')
    with col2: st.metric("Consent Rate", f'{gov["consent_rate"]}%')
    with col3: st.metric("Model Fairness", f'{gov["model_fairness"]}%')
    with col4: st.metric("Bias Audit", f'{gov["bias_audit_score"]}%')

    st.markdown(f"""<div class="glow-card" style="margin-top:12px;"><h3>Compliance Scorecard</h3></div>""", unsafe_allow_html=True)
    metrics = {
        "GDPR Compliance": gov["gdpr_compliance"],
        "Data Consent Rate": gov["consent_rate"],
        "Retention Compliance": gov["data_retention_compliant"],
        "Model Fairness": gov["model_fairness"],
        "Bias Detection": gov["bias_audit_score"],
    }
    mdf = pd.DataFrame(list(metrics.items()), columns=["Area", "Score"])
    fig = px.bar(mdf, x="Area", y="Score", color="Score", text_auto=".0f",
                 color_continuous_scale="RdYlGn", range_y=[0, 100], height=350,
                 title="Compliance Health")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color=C["text"])
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""<div class="glow-card" style="margin-top:12px;"><h3>Audit & Privacy Requests</h3></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div style="display:flex;gap:16px;flex-wrap:wrap;">
        <div class="glass" style="padding:16px;flex:1;">
            <span style="color:{C["text2"]};">Active Privacy Requests</span>
            <div style="font-size:28px;font-weight:700;color:{C["warning"]};">{gov["active_privacy_requests"]}</div>
        </div>
        <div class="glass" style="padding:16px;flex:1;">
            <span style="color:{C["text2"]};">Data Breaches (30 days)</span>
            <div style="font-size:28px;font-weight:700;color:{'green' if gov['breaches']==0 else C['danger']};">{gov["breaches"]}</div>
        </div>
        <div class="glass" style="padding:16px;flex:1;">
            <span style="color:{C["text2"]};">Last Audit</span>
            <div style="font-size:16px;font-weight:600;">{gov["last_audit"]}</div>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class="glass" style="padding:12px;margin-top:12px;border-left:3px solid {"green" if gov["audit_trail_complete"] else C["danger"]};">
        <span style="font-weight:600;">Audit Trail: {"COMPLETE ✅" if gov["audit_trail_complete"] else "INCOMPLETE ❌"}</span>
        <span style="color:{C["text2"]};"> — All model predictions, data access, and user actions are logged</span>
    </div>""", unsafe_allow_html=True)

def page_knowledge_mgmt():
    C = THEMES[st.session_state.theme]
    maybe_compact()
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Knowledge Management System</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">FAQs, best practices, runbooks — AI suggests solutions automatically</p>
    </div>""", unsafe_allow_html=True)

    df = get_knowledge_base()
    col1, col2, col3 = st.columns(3)
    with col1:
        category_filter = st.multiselect("Category", df["category"].unique(), default=df["category"].unique())
    with col2:
        search_kb = st.text_input("Search Knowledge Base", placeholder="e.g., billing, retention...")
    with col3:
        sort_by = st.selectbox("Sort by", ["views", "helpful"], index=0)

    filtered = df[df["category"].isin(category_filter)]
    if search_kb:
        filtered = filtered[filtered["title"].str.contains(search_kb, case=False, na=False)]
    filtered = filtered.sort_values(sort_by, ascending=False)

    st.markdown(f"""<div class="glow-card" style="margin-top:12px;"><h3>Articles ({len(filtered)})</h3></div>""", unsafe_allow_html=True)
    for _, article in filtered.iterrows():
        helpful_pct = article["helpful"]
        st.markdown(f"""<div class="glass" style="padding:12px;margin:4px 0;">
            <div style="display:flex;justify-content:space-between;">
                <span style="font-weight:600;color:{C["accent"]};">{article["id"]}</span>
                <span style="font-size:12px;color:{C["text2"]};">{article["category"]}</span>
            </div>
            <div style="margin:4px 0;">{article["title"]}</div>
            <div style="font-size:12px;color:{C["text2"]};">
                {article["views"]:,} views · {helpful_pct}% helpful
                <span style="margin-left:12px;">{'★' * (helpful_pct // 20)}{'☆' * (5 - helpful_pct // 20)}</span>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class="glow-card" style="margin-top:16px;"><h3>Category Distribution</h3></div>""", unsafe_allow_html=True)
    cat_counts = df["category"].value_counts().reset_index()
    cat_counts.columns = ["Category", "Count"]
    fig = px.pie(cat_counts, values="Count", names="Category", hole=0.4, title="Knowledge Categories",
                 color_discrete_sequence=px.colors.sequential.Viridis_r)
    fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", font=dict(color=C["text"]))
    st.plotly_chart(fig, use_container_width=True)

def page_search_engine():
    C = THEMES[st.session_state.theme]
    maybe_compact()
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Advanced Search Engine</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Semantic and natural language search across customers, tickets, reports, alerts, predictions</p>
    </div>""", unsafe_allow_html=True)

    query = st.text_input("Search everything...", placeholder="e.g., high risk customer, churn report, C1001...", key="search_query")
    if query:
        with st.spinner("Searching..."):
            results = search_everything(query)
        st.markdown(f"""<div class="glow-card"><h3>Results ({len(results)})</h3></div>""", unsafe_allow_html=True)
        for _, res in results.iterrows():
            type_colors = {"Customer": C["accent"], "Ticket": C["warning"], "Report": C["success"],
                           "Alert": C["danger"], "Prediction": C["neon"]}
            st.markdown(f"""<div class="glass" style="padding:10px 14px;margin:3px 0;display:flex;justify-content:space-between;align-items:center;">
                <span><span style="color:{type_colors.get(res["type"], C["text2"])};font-weight:600;">{res["type"]}</span>
                <span style="margin-left:8px;">{res["id"]}</span></span>
                <span style="font-size:12px;color:{C["text2"]};">{res["match"]}</span>
            </div>""", unsafe_allow_html=True)
    else:
        st.info("Enter a search query above to search across all data sources.")

    st.markdown(f"""<div class="glow-card" style="margin-top:16px;"><h3>Searchable Sources</h3></div>""", unsafe_allow_html=True)
    sources_html = ""
    for src in ["Customers (ID, Name, Segment)", "Support Tickets", "Reports & Dashboards", "Alerts & Notifications",
                "ML Predictions", "Knowledge Articles", "Audit Logs", "Campaigns & Events"]:
        sources_html += f"""<div class="glass" style="padding:8px 14px;margin:3px 0;">🔍 {src}</div>"""
    st.markdown(sources_html, unsafe_allow_html=True)

def page_experimentation():
    C = THEMES[st.session_state.theme]
    maybe_compact()
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Experimentation Lab</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">A/B testing, campaign testing, model comparison</p>
    </div>""", unsafe_allow_html=True)

    data = get_experimentation_data()
    campaigns = [c for c in data["campaigns"] if c["type"] in ("Email", "SMS")]
    models = [c for c in data["campaigns"] if c["type"] == "Model"]

    st.markdown(f"""<div class="glow-card"><h3>Campaign A/B Test</h3></div>""", unsafe_allow_html=True)
    camp_df = pd.DataFrame(campaigns)
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Conversions", x=camp_df["name"], y=camp_df["conversions"], marker_color=C["accent"]))
    fig.add_trace(go.Bar(name="Revenue", x=camp_df["name"], y=camp_df["revenue"] / 1000, marker_color=C["neon"],
                          yaxis="y2"))
    fig.update_layout(title="Email vs SMS Campaign", height=350, barmode="group",
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color=C["text"],
                      yaxis2=dict(overlaying="y", side="right", title="Revenue ($K)"),
                      xaxis=dict(tickfont=dict(color=C["text2"])))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""<div class="glow-card" style="margin-top:16px;"><h3>Model Comparison</h3></div>""", unsafe_allow_html=True)
    model_df = pd.DataFrame(models)
    fig = go.Figure()
    for metric in ["accuracy", "precision", "recall", "f1"]:
        fig.add_trace(go.Bar(name=metric.capitalize(), x=model_df["name"], y=model_df[metric]))
    fig.update_layout(title="XGBoost vs LightGBM", height=350, barmode="group",
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color=C["text"],
                      xaxis=dict(tickfont=dict(color=C["text2"])), yaxis=dict(tickfont=dict(color=C["text2"])))
    st.plotly_chart(fig, use_container_width=True)

def page_innovation():
    C = THEMES[st.session_state.theme]
    maybe_compact()
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Innovation Lab</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Future predictions, AI experiments, and research insights</p>
    </div>""", unsafe_allow_html=True)

    df = get_innovation_data()
    stage_order = {"Research": 0, "Prototype": 1, "Development": 2, "Testing": 3, "Production": 4}
    df["stage_num"] = df["stage"].map(stage_order)

    st.markdown(f"""<div class="glow-card"><h3> Active Experiments</h3></div>""", unsafe_allow_html=True)
    for _, exp in df.iterrows():
        stage_color = {"Research": C["text2"], "Prototype": C["warning"], "Development": C["accent"],
                       "Testing": C["success"]}.get(exp["stage"], C["text"])
        st.markdown(f"""<div class="glass" style="padding:12px;margin:4px 0;">
            <div style="display:flex;justify-content:space-between;">
                <span style="font-weight:600;">{exp["name"]}</span>
                <span style="color:{stage_color};font-size:12px;">{exp["stage"]}</span>
            </div>
            <div style="margin:4px 0;font-size:13px;color:{C["text2"]};">Team: {exp["team"]}</div>
            <div style="width:100%;height:6px;background:{C["surface2"]};border-radius:3px;overflow:hidden;">
                <div style="width:{exp["progress"]}%;height:100%;background:{C["accent"]};border-radius:3px;"></div>
            </div>
            <div style="font-size:11px;color:{C["text2"]};text-align:right;">{exp["progress"]}%</div>
        </div>""", unsafe_allow_html=True)

    fig = px.bar(df, x="name", y="progress", color="stage", text_auto=".0f",
                 title="Experiment Progress", height=350,
                 color_discrete_map={"Research": C["text2"], "Prototype": C["warning"],
                                     "Development": C["accent"], "Testing": C["success"]})
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color=C["text"])
    st.plotly_chart(fig, use_container_width=True)

def page_voice_analytics():
    C = THEMES[st.session_state.theme]
    maybe_compact()
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Voice Analytics</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Analyze call recordings, voice sentiment, and customer emotions</p>
    </div>""", unsafe_allow_html=True)

    df = get_voice_analytics()
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Total Calls", len(df))
    with col2: st.metric("Resolved", f'{len(df[df["resolution"]=="Resolved"])/len(df)*100:.0f}%')
    with col3: st.metric("Avg Duration", f'{df["duration_sec"].mean():.0f}s')
    with col4: st.metric("Satisfied", f'{len(df[df["sentiment"]=="Satisfied"])/len(df)*100:.0f}%')

    st.markdown(f"""<div class="glow-card" style="margin-top:12px;"><h3>Sentiment Distribution</h3></div>""", unsafe_allow_html=True)
    sent_df = df["sentiment"].value_counts().reset_index()
    sent_df.columns = ["Sentiment", "Count"]
    colors = {"Satisfied": "#10B981", "Happy": "#34D399", "Neutral": "#6B7280", "Frustrated": "#F59E0B", "Angry": "#EF4444"}
    fig = px.pie(sent_df, values="Count", names="Sentiment", hole=0.4, title="Call Sentiment",
                 color="Sentiment", color_discrete_map=colors)
    fig.update_layout(height=350, paper_bgcolor="rgba(0,0,0,0)", font=dict(color=C["text"]))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""<div class="glow-card" style="margin-top:12px;"><h3>Emotion Detection</h3></div>""", unsafe_allow_html=True)
    emo_df = df["emotion"].value_counts().reset_index()
    emo_df.columns = ["Emotion", "Count"]
    fig = px.bar(emo_df, x="Emotion", y="Count", color="Count", text_auto=True,
                 color_continuous_scale="RdYlGn_r", height=300)
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color=C["text"])
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""<div class="glow-card" style="margin-top:12px;"><h3>Recent Calls</h3></div>""", unsafe_allow_html=True)
    for _, call in df.tail(8).iterrows():
        st.markdown(f"""<div class="glass" style="padding:8px 12px;margin:2px 0;display:flex;justify-content:space-between;font-size:13px;">
            <span>{call["call_id"]} — {call["customer"]} with {call["agent"]}</span>
            <span>{call["sentiment"]} · {call["emotion"]} · {call["resolution"]}</span>
        </div>""", unsafe_allow_html=True)

def page_esg():
    C = THEMES[st.session_state.theme]
    maybe_compact()
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">ESG & Sustainability Dashboard</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Digital adoption, paperless interactions, energy consumption, sustainability score</p>
    </div>""", unsafe_allow_html=True)

    esg = get_esg_data()
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Digital Adoption", f'{esg["digital_adoption"]}%')
    with col2: st.metric("Paperless", f'{esg["paperless_percentage"]}%')
    with col3: st.metric("Energy Saved", f'{esg["energy_savings_kwh"]:,} kWh')
    with col4: st.metric("Carbon Reduced", f'{esg["carbon_reduction_tons"]}t')

    st.markdown(f"""<div class="glow-card" style="margin-top:12px;"><h3>Customer Sustainability Score</h3></div>""", unsafe_allow_html=True)
    scores = np.random.normal(72, 15, 7043)
    scores = np.clip(scores, 0, 100)
    fig = px.histogram(x=scores, nbins=40, title="Sustainability Score Distribution",
                       color_discrete_sequence=[C["success"]], height=350,
                       labels={"x": "Score", "y": "Customers"})
    fig.add_vline(x=esg["customer_sustainability_score"], line_dash="dash",
                  line_color=C["accent"], annotation_text=f'Avg: {esg["customer_sustainability_score"]:.0f}')
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color=C["text"])
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""<div class="glow-card" style="margin-top:12px;"><h3>Green Initiatives</h3></div>""", unsafe_allow_html=True)
    for initiative in esg["green_initiatives"]:
        st.markdown(f"""<div class="glass" style="padding:10px;margin:3px 0;display:flex;align-items:center;gap:8px;">
            <span style="font-size:20px;">{"✅" if np.random.random()>0.2 else "🔄"}</span>
            <span>{initiative}</span>
            <span style="margin-left:auto;color:{C["success"]};font-size:12px;">{np.random.randint(1000, 50000):,} customers</span>
        </div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class="glass" style="padding:12px;margin-top:12px;border-left:3px solid {C["success"]};">
        <span style="font-weight:600;"> Total Impact:</span> {esg["energy_savings_kwh"]:,} kWh saved = {esg["carbon_reduction_tons"]}t CO₂ reduced
        <span style="color:{C["text2"]};"> — equivalent to planting {int(esg["carbon_reduction_tons"]*50):,} trees 🌳</span>
    </div>""", unsafe_allow_html=True)

def page_mobile_companion():
    C = THEMES[st.session_state.theme]
    maybe_compact()
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Mobile Executive Companion</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Responsive mobile dashboard with push notifications and quick insights</p>
    </div>""", unsafe_allow_html=True)

    if st.button(" Enable Mobile Mode", use_container_width=True):
        st.session_state.mobile_layout = True
        st.rerun()
    if st.button(" Disable Mobile Mode", use_container_width=True):
        st.session_state.mobile_layout = False
        st.rerun()

    st.markdown(f"""<div class="glow-card"><h3> Push Notifications</h3></div>""", unsafe_allow_html=True)
    notifications = [
        ("🔴", "Critical churn risk for C1024 (91%)", "3 min ago"),
        ("🟡", "Data drift detected — model AUC dropped 2.1%", "12 min ago"),
        ("🟢", "APAC retention campaign improved CSAT by 8%", "1 hour ago"),
        ("🔵", "New report: Monthly Executive Summary ready", "2 hours ago"),
        ("⚪", "System health check passed — all services OK", "3 hours ago"),
    ]
    for icon, msg, time in notifications:
        st.markdown(f"""<div class="glass" style="padding:10px;margin:3px 0;display:flex;align-items:center;gap:8px;">
            <span style="font-size:18px;">{icon}</span>
            <div style="flex:1;"><span style="font-size:13px;">{msg}</span>
            <div style="font-size:11px;color:{C["text2"]};">{time}</div></div>
        </div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class="glow-card" style="margin-top:12px;"><h3> Quick Insights</h3></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
        <div class="kpi-card" style="padding:12px;"><div class="kpi-value" style="font-size:20px;">26.5%</div><div class="kpi-label">Churn Rate</div></div>
        <div class="kpi-card" style="padding:12px;"><div class="kpi-value" style="font-size:20px;color:{C["accent"]};">4.2</div><div class="kpi-label">CSAT</div></div>
        <div class="kpi-card" style="padding:12px;"><div class="kpi-value" style="font-size:20px;color:{C["success"]};">+46</div><div class="kpi-label">NPS</div></div>
        <div class="kpi-card" style="padding:12px;"><div class="kpi-value" style="font-size:20px;color:{C["danger"]};">$1.2M</div><div class="kpi-label">Revenue at Risk</div></div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class="glow-card" style="margin-top:12px;"><h3> Alert Approvals</h3></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="glass" style="padding:12px;display:flex;justify-content:space-between;align-items:center;">
        <div><span style="font-weight:600;">Escalate Case CAS-1042</span><br><span style="font-size:12px;color:{C["text2"]};">Priority: High</span></div>
        <div style="display:flex;gap:8px;">
            <span style="background:{C["success"]};padding:4px 12px;border-radius:6px;font-size:12px;cursor:pointer;">Approve</span>
            <span style="background:{C["danger"]};padding:4px 12px;border-radius:6px;font-size:12px;cursor:pointer;">Reject</span>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class="glass" style="padding:12px;margin-top:12px;text-align:center;color:{C["text2"]};">
        <span style="font-size:12px;">📱 Mobile-optimized view · Last synced: {datetime.now().strftime("%H:%M:%S")}</span>
    </div>""", unsafe_allow_html=True)

CORP_PAGE_FUNCTIONS = {
    "Governance Center": page_governance,
    "Knowledge Management": page_knowledge_mgmt,
    "Advanced Search": page_search_engine,
    "Experimentation Lab": page_experimentation,
    "Innovation Lab": page_innovation,
    "Voice Analytics": page_voice_analytics,
    "ESG Dashboard": page_esg,
    "Mobile Companion": page_mobile_companion,
}
