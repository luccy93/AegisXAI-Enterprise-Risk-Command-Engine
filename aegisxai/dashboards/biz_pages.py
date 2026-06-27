"""
Business Analytics Pages - Revenue Intel, Hyper-Personalization, Team Performance, Gamification
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from aegisxai.dashboards.components import *
from aegisxai.dashboards.pages import THEMES
from aegisxai.services.advanced_features import *

def page_revenue_intel():
    C = THEMES[st.session_state.theme]
    maybe_compact()
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Revenue Intelligence Engine</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">CLV, upsell/cross-sell potential, revenue risk, and quarterly forecasts</p>
    </div>""", unsafe_allow_html=True)

    df = get_revenue_intel()
    total_rev_at_risk = df["revenue_at_risk"].sum()
    total_expected_q = df["expected_q_revenue"].sum()

    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Revenue at Risk", f"${total_rev_at_risk:,.0f}")
    with col2: st.metric("Expected Q Revenue", f"${total_expected_q:,.0f}")
    with col3: st.metric("Avg CLV", f"${df['avg_clv'].mean():,.0f}")
    with col4: st.metric("Upsell Potential", f"${df['upsell_potential'].sum():,.0f}")

    st.markdown(f"""<div class="glow-card" style="margin-top:12px;"><h3>Segment Analysis</h3></div>""", unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Avg CLV", x=df["segment"], y=df["avg_clv"], marker_color=C["accent"]))
    fig.add_trace(go.Bar(name="Upsell Potential", x=df["segment"], y=df["upsell_potential"], marker_color=C["neon"]))
    fig.add_trace(go.Bar(name="Cross-Sell Potential", x=df["segment"], y=df["cross_sell_potential"], marker_color=C["warning"]))
    fig.update_layout(title="Revenue by Segment", height=400, barmode="group",
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color=C["text"],
                      xaxis=dict(tickfont=dict(color=C["text2"])), yaxis=dict(tickfont=dict(color=C["text2"])))
    st.plotly_chart(fig, use_container_width=True)

    fig = px.bar(df, x="segment", y="revenue_at_risk", color="revenue_at_risk",
                 title="Revenue at Risk by Segment", text_auto=True, height=350,
                 color_continuous_scale="RdYlGn_r")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color=C["text"])
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""<div class="glass" style="padding:12px;margin-top:12px;">
        <span style="color:{C["accent"]};font-weight:600;">Insight:</span> Premium segment has highest CLV but also significant revenue at risk.
        Prioritize retention for high-value premium customers.
    </div>""", unsafe_allow_html=True)

def page_hyper_personalization():
    C = THEMES[st.session_state.theme]
    maybe_compact()
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Hyper-Personalization Engine</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Predict optimal channel, time, offer, and support mode for each customer</p>
    </div>""", unsafe_allow_html=True)

    df = get_personalization(20)
    col1, col2 = st.columns([1, 2])
    with col1:
        selected_customer = st.selectbox("Select Customer", df["customer_id"].tolist())
    with col2:
        search_customer = st.text_input("Search Customer ID", placeholder="e.g., C2005")

    cust = df[df["customer_id"] == selected_customer].iloc[0] if not df.empty else df.iloc[0]
    st.markdown(f"""<div class="glow-card" style="margin-top:12px;">
        <h3> Customer 360° Personalization</h3>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:12px;">
            <div class="glass" style="padding:12px;text-align:center;">
                <div style="font-size:12px;color:{C["text2"]};">Best Channel</div>
                <div style="font-size:22px;font-weight:700;color:{C["accent"]};">{cust["channel"]}</div>
            </div>
            <div class="glass" style="padding:12px;text-align:center;">
                <div style="font-size:12px;color:{C["text2"]};">Best Time</div>
                <div style="font-size:22px;font-weight:700;color:{C["success"]};">{cust["best_time"]}</div>
            </div>
            <div class="glass" style="padding:12px;text-align:center;">
                <div style="font-size:12px;color:{C["text2"]};">Best Offer</div>
                <div style="font-size:22px;font-weight:700;color:{C["warning"]};">{cust["best_offer"]}</div>
            </div>
            <div class="glass" style="padding:12px;text-align:center;">
                <div style="font-size:12px;color:{C["text2"]};">Support Mode</div>
                <div style="font-size:22px;font-weight:700;color:{C["neon"]};">{cust["support_mode"]}</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class="glow-card" style="margin-top:16px;"><h3>Channel Distribution</h3></div>""", unsafe_allow_html=True)
    channel_counts = df["channel"].value_counts().reset_index()
    channel_counts.columns = ["Channel", "Count"]
    fig = px.pie(channel_counts, values="Count", names="Channel", hole=0.4, title="Preferred Channels",
                 color_discrete_sequence=px.colors.sequential.Viridis_r)
    fig.update_layout(height=350, paper_bgcolor="rgba(0,0,0,0)", font=dict(color=C["text"]),
                      legend=dict(font=dict(color=C["text2"])))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""<div class="glow-card" style="margin-top:12px;"><h3>All Customer Profiles</h3></div>""", unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True, height=300)

def page_team_performance():
    C = THEMES[st.session_state.theme]
    maybe_compact()
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Team Performance Analytics</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Measure agent productivity, resolution quality, and customer satisfaction</p>
    </div>""", unsafe_allow_html=True)

    df = get_team_performance()
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Teams", len(df))
    with col2: st.metric("Total Agents", df["agents"].sum())
    with col3: st.metric("Avg Quality", f'{df["quality_score"].mean():.1f}%')
    with col4: st.metric("Avg Rating", f'{df["customer_rating"].mean():.2f}')

    st.markdown(f"""<div class="glow-card" style="margin-top:12px;"><h3>Team Rankings</h3></div>""", unsafe_allow_html=True)
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Quality Score", "Customer Rating"))
    fig.add_trace(go.Bar(y=df["team"], x=df["quality_score"], orientation="h",
                  marker_color=px.colors.sequential.Viridis_r, text=df["quality_score"], textposition="outside"),
                  row=1, col=1)
    fig.add_trace(go.Bar(y=df["team"], x=df["customer_rating"], orientation="h",
                  marker_color=px.colors.sequential.Plasma_r, text=df["customer_rating"], textposition="outside"),
                  row=1, col=2)
    fig.update_layout(height=400, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color=C["text"], showlegend=False)
    fig.update_xaxes(tickfont=dict(color=C["text2"]))
    fig.update_yaxes(tickfont=dict(color=C["text2"]))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""<div class="glow-card" style="margin-top:12px;"><h3>Resolution Efficiency</h3></div>""", unsafe_allow_html=True)
    fig = px.scatter(df, x="avg_resolution_time", y="satisfaction", size="cases_resolved",
                     color="team", text="team", hover_data=["agents", "quality_score"],
                     title="Resolution Time vs Satisfaction", height=350)
    fig.update_traces(textposition="top center")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color=C["text"])
    st.plotly_chart(fig, use_container_width=True)

def page_gamification():
    C = THEMES[st.session_state.theme]
    maybe_compact()
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Gamification System</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Reward points, achievements, badges, challenges, and leaderboards</p>
    </div>""", unsafe_allow_html=True)

    data = get_gamification()
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(f"""<div class="glow-card"><h3> Badges</h3></div>""", unsafe_allow_html=True)
        for badge, info in data["badges"].items():
            st.markdown(f"""<div class="glass" style="padding:10px;margin:4px 0;display:flex;justify-content:space-between;">
                <span style="font-weight:600;">{badge}</span>
                <span><span style="color:{C["accent"]};">{info["earned"]:,}</span> earned · {info["points"]:,} pts</span>
            </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""<div class="glow-card"><h3> Challenges</h3></div>""", unsafe_allow_html=True)
        for challenge, info in data["challenges"].items():
            st.markdown(f"""<div class="glass" style="padding:10px;margin:4px 0;display:flex;justify-content:space-between;">
                <span style="font-weight:600;">{challenge}</span>
                <span><span style="color:{C["success"]};">{info["completed"]:,}</span> done · <span style="color:{C["warning"]};">{info["active"]:,}</span> active</span>
            </div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class="glow-card" style="margin-top:12px;"><h3> Leaderboard — Top 10</h3></div>""", unsafe_allow_html=True)
    lb = data["leaderboard"][:10]
    for i, entry in enumerate(lb, 1):
        medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, f"{i}.")
        st.markdown(f"""<div class="glass" style="padding:8px 14px;margin:2px 0;display:flex;justify-content:space-between;">
            <span>{medal} {entry["customer"]}</span>
            <span style="color:{C["accent"]};font-weight:700;">{entry["points"]:,} pts</span>
        </div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class="glow-card" style="margin-top:16px;"><h3>Points Distribution</h3></div>""", unsafe_allow_html=True)
    pts_df = pd.DataFrame(data["leaderboard"])
    fig = px.histogram(pts_df, x="points", nbins=20, title="Points Distribution",
                       color_discrete_sequence=[C["accent"]], height=300)
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color=C["text"])
    st.plotly_chart(fig, use_container_width=True)

BIZ_PAGE_FUNCTIONS = {
    "Revenue Intelligence": page_revenue_intel,
    "Hyper-Personalization": page_hyper_personalization,
    "Team Performance": page_team_performance,
    "Gamification": page_gamification,
}
