"""
AEGIS-XAI Customer Experience Intelligence Dashboard Pages
5 executive dashboards for CSAT, NPS, Sentiment, VOC, Loyalty
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from collections import Counter

from aegisxai.models.features import load_data
from aegisxai.utils.helpers import audit_log
from aegisxai.cx.satisfaction import (
    generate_csat_data, generate_nps_data, calculate_happiness_index
)
from aegisxai.cx.sentiment import generate_sentiment_data, analyze_comment_sentiment
from aegisxai.cx.engagement import (
    generate_engagement_data, predict_loyalty, get_loyalty_tiers, generate_loyalty_data
)
from aegisxai.cx.service_quality import (
    generate_service_quality_data, generate_ticket_satisfaction
)
from aegisxai.cx.voc import generate_voc_data, classify_complaint, generate_complaint_data
from aegisxai.cx.recommendations import (
    generate_cx_recommendations, get_customer_360_satisfaction, generate_ai_insight
)
from aegisxai.dashboards.pages import THEMES, CSV_PATH


def page_cx_intelligence():
    C = THEMES[st.session_state.theme]
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Customer Experience Intelligence</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Executive dashboard measuring CSAT, NPS, Happiness, and overall CX health</p>
    </div>""", unsafe_allow_html=True)

    csat = generate_csat_data()
    nps = generate_nps_data()
    happiness = calculate_happiness_index()

    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        delta = "+0.1" if csat["overall_score"] > 4.0 else "-0.1"
        st.metric("CSAT Score", f'{csat["overall_score"]:.1f} / 5', delta)
    with k2:
        delta_nps = f'+{nps["overall_nps"]}' if nps["overall_nps"] > 0 else str(nps["overall_nps"])
        st.metric("Net Promoter Score", delta_nps, "+2 vs last month")
    with k3:
        st.metric("Happiness Index", f'{happiness["overall_happiness"]}/100',
                  "Excellent" if happiness["overall_happiness"] > 75 else "Good")
    with k4:
        eng = generate_engagement_data()
        st.metric("Engagement Rate", f'{eng["feature_adoption_rate"]:.0f}%', "+3%")
    with k5:
        sq = generate_service_quality_data()
        st.metric("SLA Compliance", f'{sq["sla_compliance"]:.0f}%', "+1%")

    row1, row2 = st.columns(2)
    with row1:
        st.markdown(f"""<div class="glow-card"><h3>CSAT Gauge</h3></div>""", unsafe_allow_html=True)
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=csat["overall_score"],
            number={"suffix": " / 5", "font": {"color": C["text"], "size": 24}},
            delta={"reference": 4.0, "font": {"color": C["success"]}},
            gauge={
                "axis": {"range": [0, 5], "tickcolor": C["text2"], "tickfont": {"color": C["text2"]}},
                "bar": {"color": C["accent"]},
                "steps": [
                    {"range": [0, 2], "color": "rgba(239, 68, 68, 0.3)"},
                    {"range": [2, 3.5], "color": "rgba(245, 158, 11, 0.3)"},
                    {"range": [3.5, 5], "color": "rgba(16, 185, 129, 0.3)"}
                ],
                "threshold": {"line": {"color": C["success"], "width": 4}, "thickness": 0.75, "value": 4.0}
            }, domain={"x": [0, 1], "y": [0, 1]}
        ))
        fig.update_layout(height=250, paper_bgcolor="rgba(0,0,0,0)", font={"color": C["text"]}, margin=dict(l=30, r=30, t=30, b=30))
        st.plotly_chart(fig, use_container_width=True)

    with row2:
        st.markdown(f"""<div class="glow-card"><h3>CSAT Distribution</h3></div>""", unsafe_allow_html=True)
        dist = csat["distribution"]
        fig = px.pie(values=dist, names=["Excellent", "Good", "Poor"],
                      color=["Excellent", "Good", "Poor"],
                      color_discrete_map={"Excellent": C["success"], "Good": C["accent"], "Poor": C["danger"]},
                      hole=0.5)
        fig.update_layout(height=250, paper_bgcolor="rgba(0,0,0,0)", font={"color": C["text"]},
                          legend=dict(font=dict(color=C["text2"])))
        st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""<div class="glow-card"><h3>NPS Gauge</h3></div>""", unsafe_allow_html=True)
        nps_val = nps["overall_nps"]
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=nps_val,
            number={"suffix": "", "font": {"color": C["text"], "size": 28}},
            gauge={
                "axis": {"range": [-100, 100], "tickcolor": C["text2"], "tickfont": {"color": C["text2"]}},
                "bar": {"color": C["accent"]},
                "steps": [
                    {"range": [-100, 0], "color": "rgba(239, 68, 68, 0.3)"},
                    {"range": [0, 30], "color": "rgba(245, 158, 11, 0.3)"},
                    {"range": [30, 70], "color": "rgba(16, 185, 129, 0.3)"},
                    {"range": [70, 100], "color": "rgba(6, 182, 212, 0.3)"}
                ]
            }, domain={"x": [0, 1], "y": [0, 1]}
        ))
        fig.add_annotation(text=f'Promoters: {nps["promoters_pct"]:.0f}%  |  Passives: {nps["passives_pct"]:.0f}%  |  Detractors: {nps["detractors_pct"]:.0f}%',
                           x=0.5, y=0.15, showarrow=False, font=dict(size=11, color=C["text2"]))
        fig.update_layout(height=280, paper_bgcolor="rgba(0,0,0,0)", font={"color": C["text"]}, margin=dict(l=30, r=30, t=30, b=50))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown(f"""<div class="glow-card"><h3>CSAT by Department</h3></div>""", unsafe_allow_html=True)
        dept_df = pd.DataFrame(list(csat["department_scores"].items()), columns=["Department", "Score"])
        fig = px.bar(dept_df, x="Department", y="Score", color="Score",
                     color_continuous_scale=["#EF4444", "#F59E0B", "#10B981"], text_auto=".2f",
                     range_y=[0, 5])
        fig.update_layout(height=280, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color=C["text"], xaxis=dict(tickfont=dict(color=C["text2"])),
                          coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""<div class="glow-card"><h3>Happiness Index Components</h3></div>""", unsafe_allow_html=True)
    comps = happiness["components"]
    comp_df = pd.DataFrame(list(comps.items()), columns=["Component", "Score"])
    comp_df["Max"] = 100
    comp_df["Pct"] = comp_df["Score"]
    fig = px.bar(comp_df, x="Component", y="Pct", color="Pct",
                 color_continuous_scale=["#EF4444", "#F59E0B", "#10B981"],
                 text_auto=".0f", range_y=[0, 100],
                 title=f'Overall Happiness: {happiness["overall_happiness"]}/100 ({happiness["score_category"]})')
    fig.update_layout(height=350, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color=C["text"], xaxis=dict(tickfont=dict(color=C["text2"])),
                      coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)


def page_sentiment_nps():
    C = THEMES[st.session_state.theme]
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Sentiment & NPS Analytics</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">AI-powered sentiment analysis, emotion classification, and promoter tracking</p>
    </div>""", unsafe_allow_html=True)

    sent = generate_sentiment_data()
    nps = generate_nps_data()

    k1, k2, k3, k4 = st.columns(4)
    with k1: st.metric("Overall Sentiment", sent["overall_sentiment"], "+2%")
    with k2: st.metric("Positive", f'{sent["sentiment_distribution"]["Positive"]}%', "+3%")
    with k3: st.metric("NPS Score", f'+{nps["overall_nps"]}', "+2 vs last qtr")
    with k4: st.metric("Promoters", f'{nps["promoters_pct"]:.0f}%', "+2%")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""<div class="glow-card"><h3>Sentiment Distribution</h3></div>""", unsafe_allow_html=True)
        sd = sent["sentiment_distribution"]
        fig = px.pie(values=list(sd.values()), names=list(sd.keys()),
                      color=list(sd.keys()),
                      color_discrete_map={"Positive": C["success"], "Neutral": C["accent"], "Negative": C["danger"]},
                      hole=0.5)
        fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", font={"color": C["text"]},
                          legend=dict(font=dict(color=C["text2"])))
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.markdown(f"""<div class="glow-card"><h3>Emotion Breakdown</h3></div>""", unsafe_allow_html=True)
        emo = sent["emotion_distribution"]
        emo_df = pd.DataFrame(list(emo.items()), columns=["Emotion", "Pct"])
        colors = {"Happy": C["success"], "Satisfied": C["neon"], "Frustrated": C["warning"],
                  "Angry": C["danger"], "Confused": C["accent"], "Disappointed": "#FF6B6B"}
        fig = px.bar(emo_df, x="Emotion", y="Pct", color="Emotion",
                     color_discrete_map=colors, text_auto=".0f")
        fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color=C["text"], xaxis=dict(tickfont=dict(color=C["text2"])),
                          showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""<div class="glow-card"><h3>Sentiment Trend (Monthly)</h3></div>""", unsafe_allow_html=True)
    trend = sent["monthly_trend"]
    trend_df = pd.DataFrame(trend)
    fig = go.Figure()
    for col, color in [("positive", C["success"]), ("neutral", C["accent"]), ("negative", C["danger"])]:
        fig.add_trace(go.Scatter(x=trend_df["month"], y=trend_df[col], mode="lines+markers",
                                 name=col.capitalize(), line=dict(color=color, width=3)))
    fig.update_layout(height=350, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color=C["text"], xaxis=dict(tickfont=dict(color=C["text2"])),
                      yaxis=dict(tickfont=dict(color=C["text2"]), title="%"),
                      legend=dict(font=dict(color=C["text2"])))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""<div class="glow-card" style="margin-top:16px;"><h3>NPS by Segment</h3></div>""", unsafe_allow_html=True)
    nps_seg = pd.DataFrame(list(nps["segment_nps"].items()), columns=["Segment", "NPS"])
    fig = px.bar(nps_seg, x="Segment", y="NPS", color="NPS",
                 color_continuous_scale=["#EF4444", "#F59E0B", "#10B981"],
                 text_auto=".0f", range_y=[0, 80])
    fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color=C["text"], xaxis=dict(tickfont=dict(color=C["text2"])),
                      coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

    with st.expander(" Simulate Comment Sentiment Analysis", expanded=False):
        col_a, col_b = st.columns([3, 1])
        with col_a:
            comment = st.text_input("Enter customer comment", placeholder="e.g., Your service has been excellent lately...")
        with col_b:
            if st.button("Analyze", use_container_width=True):
                if comment:
                    result = analyze_comment_sentiment(comment)
                    sc = {"Positive": C["success"], "Neutral": C["accent"], "Negative": C["danger"]}
                    st.markdown(f"""<div class="glass" style="padding:16px;margin-top:8px;">
                        <div style="display:flex;gap:16px;align-items:center;">
                            <span style="font-size:14px;color:{C["text2"]};">Sentiment:</span>
                            <span style="font-size:18px;font-weight:700;color:{sc.get(result['sentiment'], C['text'])};">{result['sentiment']}</span>
                            <span style="font-size:14px;color:{C["text2"]};">Emotion:</span>
                            <span style="font-size:16px;color:{C["neon"]};">{result['emotion']}</span>
                            <span style="font-size:14px;color:{C["text2"]};">Score:</span>
                            <span style="font-size:16px;color:{C["accent"]};">{result['score']:.2f}</span>
                        </div>
                    </div>""", unsafe_allow_html=True)


def page_service_quality():
    C = THEMES[st.session_state.theme]
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Service Quality Dashboard</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Support metrics, ticket satisfaction, SLA monitoring and resolution tracking</p>
    </div>""", unsafe_allow_html=True)

    sq = generate_service_quality_data()
    tickets = generate_ticket_satisfaction()

    k1, k2, k3, k4, k5 = st.columns(5)
    with k1: st.metric("Avg Response", f'{sq["avg_response_time_hours"]:.1f}h', "-0.3h")
    with k2: st.metric("Avg Resolution", f'{sq["avg_resolution_time_hours"]:.1f}h', "-0.5h")
    with k3: st.metric("FCR Rate", f'{sq["fcr_rate"]:.0f}%', "+2%")
    with k4: st.metric("SLA Compliance", f'{sq["sla_compliance"]:.0f}%', "+1%")
    with k5: st.metric("Reopen Rate", f'{sq["reopen_rate"]:.0f}%', "-0.5%")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""<div class="glow-card"><h3>Service Quality Metrics</h3></div>""", unsafe_allow_html=True)
        metrics = ["Response Time", "Resolution Time", "FCR Rate", "SLA Compliance"]
        values = [sq["avg_response_time_hours"]/5*100, sq["avg_resolution_time_hours"]/10*100,
                  sq["fcr_rate"], sq["sla_compliance"]]
        fig = go.Figure()
        for i, (m, v) in enumerate(zip(metrics, values)):
            fig.add_trace(go.Indicator(
                mode="gauge+number", value=min(v, 100),
                number={"suffix": "%", "font": {"size": 16, "color": C["text"]}},
                title={"text": m, "font": {"size": 12, "color": C["text2"]}},
                gauge={"axis": {"range": [0, 100], "tickfont": {"color": C["text2"], "size": 8}},
                       "bar": {"color": C["accent"]},
                       "steps": [{"range": [0, 50], "color": "rgba(239,68,68,0.2)"},
                                 {"range": [50, 80], "color": "rgba(245,158,11,0.2)"},
                                 {"range": [80, 100], "color": "rgba(16,185,129,0.2)"}]},
                domain={"row": i//2, "column": i%2}
            ))
        fig.update_layout(grid={"rows": 2, "columns": 2}, height=350,
                          paper_bgcolor="rgba(0,0,0,0)", font={"color": C["text"]},
                          margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown(f"""<div class="glow-card"><h3>Department Resolution Time</h3></div>""", unsafe_allow_html=True)
        dept = sq["department_quality"]
        dept_df = pd.DataFrame(list(dept.items()), columns=["Department", "Avg Hours"])
        fig = px.bar(dept_df, x="Department", y="Avg Hours", color="Avg Hours",
                     color_continuous_scale=["#10B981", "#F59E0B", "#EF4444"], text_auto=".1f")
        fig.update_layout(height=350, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color=C["text"], xaxis=dict(tickfont=dict(color=C["text2"])),
                          coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""<div class="glow-card" style="margin-top:16px;"><h3>Monthly Service Quality Trend</h3></div>""", unsafe_allow_html=True)
    mtrend = sq["monthly_trend"]
    mdf = pd.DataFrame(mtrend)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=mdf["month"], y=mdf["avg_resolution_time"], mode="lines+markers",
                             name="Resolution Time (hrs)", line=dict(color=C["danger"], width=2)))
    fig.add_trace(go.Scatter(x=mdf["month"], y=mdf["avg_response_time"], mode="lines+markers",
                             name="Response Time (hrs)", line=dict(color=C["accent"], width=2)))
    fig.add_trace(go.Scatter(x=mdf["month"], y=mdf["fcr_rate"], mode="lines+markers",
                             name="FCR Rate %", line=dict(color=C["success"], width=2), yaxis="y2"))
    fig.update_layout(height=350, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color=C["text"], xaxis=dict(tickfont=dict(color=C["text2"])),
                      yaxis=dict(tickfont=dict(color=C["text2"]), title="Hours"),
                      yaxis2=dict(tickfont=dict(color=C["text2"]), title="FCR %", overlaying="y", side="right"),
                      legend=dict(font=dict(color=C["text2"])))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""<div class="glow-card" style="margin-top:16px;"><h3>Recent Ticket Satisfaction Ratings</h3></div>""", unsafe_allow_html=True)
    tdf = pd.DataFrame(tickets)
    tdf["Stars"] = tdf["rating"].apply(lambda r: "★" * r + "☆" * (5 - r))
    st.dataframe(tdf[["ticket_id", "rating", "agent_rating", "feedback_text", "time_to_resolve"]].head(10),
                 use_container_width=True, height=350)

    avg_rating = np.mean([t["rating"] for t in tickets])
    avg_agent = np.mean([t["agent_rating"] for t in tickets])
    st.markdown(f"""<div style="display:flex;gap:16px;margin-top:8px;">
        <div class="kpi-card"><div class="kpi-value" style="color:{C["success"]};">{avg_rating:.2f}</div><div class="kpi-label">Avg Ticket Rating</div></div>
        <div class="kpi-card"><div class="kpi-value" style="color:{C["neon"]};">{avg_agent:.2f}</div><div class="kpi-label">Avg Agent Rating</div></div>
        <div class="kpi-card"><div class="kpi-value" style="color:{C["accent"]};">{len(tickets)}</div><div class="kpi-label">Total Tickets</div></div>
    </div>""", unsafe_allow_html=True)


def page_voc_analytics():
    C = THEMES[st.session_state.theme]
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Voice of Customer Analytics</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Aggregated feedback intelligence, complaint root cause analysis, and emerging concern detection</p>
    </div>""", unsafe_allow_html=True)

    voc = generate_voc_data()
    complaints = generate_complaint_data()

    k1, k2, k3 = st.columns(3)
    with k1: st.metric("Total Complaints", f'{sum(c["count"] for c in voc["top_complaints"])}', "-5% MoM")
    with k2: st.metric("Categories Tracked", len(voc["complaint_categories"]))
    with k3: st.metric("Emerging Concerns", len(voc["emerging_concerns"]), "NEW")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""<div class="glow-card"><h3> Top Complaints</h3></div>""", unsafe_allow_html=True)
        for i, comp in enumerate(voc["top_complaints"]):
            trend_icon = {"up": " _upward", "down": " _downward", "stable": " _rightward"}
            tc = C["danger"] if comp["trend"] == "up" else C["success"] if comp["trend"] == "down" else C["text2"]
            st.markdown(f"""<div class="glass" style="padding:10px 14px;margin:4px 0;display:flex;justify-content:space-between;">
                <span style="font-size:14px;">{i+1}. {comp['issue']}</span>
                <span style="color:{tc};font-size:13px;font-weight:600;">{comp['count']} cases</span>
            </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""<div class="glow-card"><h3> Top Praises</h3></div>""", unsafe_allow_html=True)
        for i, p in enumerate(voc.get("top_praises", [])):
            st.markdown(f"""<div class="glass" style="padding:10px 14px;margin:4px 0;display:flex;justify-content:space-between;">
                <span style="font-size:14px;color:{C["success"]};">{i+1}. {p['feature']}</span>
                <span style="color:{C["neon"]};font-size:13px;">{p['count']} mentions</span>
            </div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class="glow-card" style="margin-top:16px;"><h3>Complaint Category Distribution</h3></div>""", unsafe_allow_html=True)
    cats = voc["complaint_categories"]
    cat_df = pd.DataFrame(list(cats.items()), columns=["Category", "%"])
    fig = px.bar(cat_df, x="Category", y="%", color="%",
                 color_continuous_scale=px.colors.sequential.Viridis, text_auto=".0f",
                 title="Root Cause Breakdown")
    fig.update_layout(height=350, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color=C["text"], xaxis=dict(tickfont=dict(color=C["text2"])),
                      coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""<div class="glow-card" style="margin-top:16px;"><h3>Monthly Complaint Trend</h3></div>""", unsafe_allow_html=True)
    mcomp = voc["monthly_complaints"]
    mdf = pd.DataFrame(mcomp)
    cats_list = list(cats.keys())
    fig = go.Figure()
    for cat in cats_list:
        cat_data = [c for c in mcomp if c["category"] == cat]
        if cat_data:
            df_cat = pd.DataFrame(cat_data)
            fig.add_trace(go.Scatter(x=df_cat["month"], y=df_cat["count"], mode="lines+markers",
                                     name=cat, stackgroup="one"))
    fig.update_layout(height=350, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color=C["text"], xaxis=dict(tickfont=dict(color=C["text2"])),
                      yaxis=dict(tickfont=dict(color=C["text2"])),
                      legend=dict(font=dict(color=C["text2"])))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""<div class="glow-card" style="margin-top:16px;"><h3> Emerging Concerns</h3></div>""", unsafe_allow_html=True)
    for concern in voc["emerging_concerns"]:
        st.markdown(f"""<div class="glass" style="padding:8px 14px;margin:3px 0;font-size:14px;">
            <span style="color:{C["warning"]};">⚠</span> {concern}
        </div>""", unsafe_allow_html=True)

    with st.expander(" Classify a Complaint", expanded=False):
        col_a, col_b = st.columns([3, 1])
        with col_a:
            comp_text = st.text_input("Enter complaint text", placeholder="e.g., My internet keeps disconnecting...",
                                      key="comp_classify")
        with col_b:
            if st.button("Classify", key="classify_btn", use_container_width=True):
                if comp_text:
                    cat = classify_complaint(comp_text)
                    st.markdown(f"""<div class="glass" style="padding:12px;margin-top:8px;">
                        <span style="color:{C["text2"]};">Category: </span>
                        <span style="color:{C["neon"]};font-weight:700;font-size:16px;">{cat}</span>
                    </div>""", unsafe_allow_html=True)


def page_loyalty_engagement():
    C = THEMES[st.session_state.theme]
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Loyalty & Engagement</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Customer loyalty prediction, engagement tracking, and rewards program management</p>
    </div>""", unsafe_allow_html=True)

    eng = generate_engagement_data()
    loyalty = predict_loyalty()
    tiers = get_loyalty_tiers()
    loy_data = generate_loyalty_data()

    k1, k2, k3, k4 = st.columns(4)
    with k1: st.metric("Loyalty Rate", f'{loy_data["loyalty_rate"]:.0f}%', "+1%")
    with k2: st.metric("Advocates", f'{loyalty["loyalty_distribution"]["Advocate"]}%', "+2%")
    with k3: st.metric("Engagement Rate", f'{eng["feature_adoption_rate"]:.0f}%', "+3%")
    with k4: st.metric("Inactive", f'{eng["engagement_distribution"]["Inactive"]}%', "-1%")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""<div class="glow-card"><h3>Loyalty Distribution</h3></div>""", unsafe_allow_html=True)
        ld = loyalty["loyalty_distribution"]
        ldf = pd.DataFrame(list(ld.items()), columns=["Status", "%"])
        colors = {"Advocate": C["success"], "Loyal": C["neon"], "Neutral": C["accent"],
                  "At Risk": C["warning"], "Detractor": C["danger"]}
        fig = px.bar(ldf, x="Status", y="%", color="Status", color_discrete_map=colors, text_auto=".0f")
        fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color=C["text"], xaxis=dict(tickfont=dict(color=C["text2"])),
                          showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown(f"""<div class="glow-card"><h3>Engagement Distribution</h3></div>""", unsafe_allow_html=True)
        ed = eng["engagement_distribution"]
        edf = pd.DataFrame(list(ed.items()), columns=["Level", "%"])
        ecolors = {"Highly Engaged": C["success"], "Moderately Engaged": C["accent"],
                   "Disengaged": C["warning"], "Inactive": C["danger"]}
        fig = px.pie(edf, values="%", names="Level", color="Level",
                     color_discrete_map=ecolors, hole=0.5)
        fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", font={"color": C["text"]},
                          legend=dict(font=dict(color=C["text2"])))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""<div class="glow-card" style="margin-top:16px;"><h3>Retention Curve (Cohort)</h3></div>""", unsafe_allow_html=True)
    rc = eng["retention_curve"]
    rdf = pd.DataFrame(rc)
    fig = px.line(rdf, x="month", y="retention_rate", markers=True,
                  title="Retention by Month",
                  labels={"retention_rate": "Retention %", "month": "Month"})
    fig.update_traces(line=dict(color=C["accent"], width=3))
    fig.update_layout(height=350, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color=C["text"], xaxis=dict(tickfont=dict(color=C["text2"])),
                      yaxis=dict(tickfont=dict(color=C["text2"]), range=[0, 100]))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""<div class="glow-card" style="margin-top:16px;"><h3>Loyalty Program Tiers</h3></div>""", unsafe_allow_html=True)
    tdf = pd.DataFrame(tiers)
    tcolors = {"Bronze": "#CD7F32", "Silver": "#C0C0C0", "Gold": "#FFD700",
               "Platinum": "#E5E4E2", "Diamond": "#B9F2FF"}
    fig = px.bar(tdf, x="tier", y="customers", color="tier",
                 color_discrete_map=tcolors, text_auto=".0f",
                 title="Customers by Loyalty Tier")
    fig.update_layout(height=350, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color=C["text"], xaxis=dict(tickfont=dict(color=C["text2"])),
                      showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""<div class="glow-card" style="margin-top:16px;"><h3>360° Satisfaction Profile</h3></div>""", unsafe_allow_html=True)
    df = load_data()
    customers = df["customerID"].tolist() if len(df) > 0 else ["C1001", "C1024", "C1087"]
    selected = st.selectbox("Select a customer", customers, key="cx_customer_360")
    profile = get_customer_360_satisfaction(df if len(df) > 0 else None, selected)
    if profile:
        pc = {"Excellent": C["success"], "Good": C["neon"], "Neutral": C["accent"],
              "At Risk": C["warning"], "Critical": C["danger"]}
        st.markdown(f"""<div class="glass" style="padding:20px;margin-top:8px;">
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;">
                <div><span style="color:{C["text2"]};">CSAT:</span> <span style="color:{C["neon"]};">{profile['csat']}/5</span></div>
                <div><span style="color:{C["text2"]};">NPS:</span> <span style="color:{C["neon"]};">{profile['nps']}</span></div>
                <div><span style="color:{C["text2"]};">Sentiment:</span> <span style="color:{C["neon"]};">{profile['sentiment']}</span></div>
                <div><span style="color:{C["text2"]};">Happiness:</span> <span style="color:{C["neon"]};">{profile['happiness_index']}/100</span></div>
                <div><span style="color:{C["text2"]};">Engagement:</span> <span style="color:{C["neon"]};">{profile['engagement_score']}/100</span></div>
                <div><span style="color:{C["text2"]};">Tier:</span> <span style="color:{C["warning"]};">{profile['loyalty_tier']}</span></div>
                <div><span style="color:{C["text2"]};">Open Tickets:</span> <span style="color:{C["danger"]};">{profile['open_tickets']}</span></div>
                <div><span style="color:{C["text2"]};">Churn Risk:</span> <span style="color:{pc.get(profile['churn_risk'], C['text'])};">{profile['churn_risk']}</span></div>
                <div><span style="color:{C["text2"]};">Tier:</span> <span style="color:{C["warning"]};">{profile.get("recommended_actions",["N/A"])[0] if profile.get("recommended_actions") else "N/A"}</span></div>
            </div>
        </div>""", unsafe_allow_html=True)
        if profile.get("recommended_actions"):
            st.markdown(f"""<div style="margin-top:12px;"><span style="color:{C["accent"]};font-weight:600;">Recommended Actions:</span></div>""", unsafe_allow_html=True)
            for ra in profile["recommended_actions"]:
                st.markdown(f"""<div class="glass" style="padding:6px 12px;margin:3px 0;font-size:13px;">{ra}</div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class="glow-card" style="margin-top:16px;"><h3>Monthly Active Users</h3></div>""", unsafe_allow_html=True)
    mau = eng["monthly_active_users"]
    mdf = pd.DataFrame(mau)
    fig = px.line(mdf, x="month", y="maus", markers=True, title="Monthly Active Users",
                  labels={"maus": "Users", "month": "Month"})
    fig.update_traces(line=dict(color=C["success"], width=3))
    fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color=C["text"], xaxis=dict(tickfont=dict(color=C["text2"])),
                      yaxis=dict(tickfont=dict(color=C["text2"])))
    st.plotly_chart(fig, use_container_width=True)


CX_PAGE_FUNCTIONS = {
    "Customer Experience": page_cx_intelligence,
    "Sentiment & NPS": page_sentiment_nps,
    "Service Quality": page_service_quality,
    "VOC Analytics": page_voc_analytics,
    "Loyalty & Engagement": page_loyalty_engagement,
}
