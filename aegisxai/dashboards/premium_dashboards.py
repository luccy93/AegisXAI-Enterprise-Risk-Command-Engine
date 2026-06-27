"""
ENTERPRISE PREMIUM DASHBOARD SUITE
All 22 flagship dashboard pages for the Executive Command Engine
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import io, base64, random, json

from aegisxai.dashboards.components import maybe_compact
from aegisxai.dashboards.pages import THEMES
from aegisxai.services.premium_services import *

def holographic_kpi(label, value, delta=None, color=None, fmt=".0f", icon=""):
    C = THEMES[st.session_state.theme]
    clr = color or C["accent"]
    val_str = f"{value:{fmt}}" if isinstance(value, (int, float)) else str(value)
    delta_str = f"<div style='font-size:12px;color:{C['success'] if delta and delta>0 else C['danger']};'>{'+' if delta and delta>0 else ''}{delta or ''}</div>" if delta is not None else ""
    return f"""<div class="glow-card holographic" style="padding:16px;text-align:center;position:relative;overflow:hidden;min-width:130px;">
        <div class="holographic-shine" style="position:absolute;top:-50%;left:-50%;width:200%;height:200%;
            background:conic-gradient(from 0deg, transparent, rgba(255,255,255,0.03), transparent, rgba(255,255,255,0.03), transparent);
            animation: holographicRotate 6s linear infinite;"></div>
        <div style="position:relative;z-index:1;">
            <div style="font-size:11px;color:{C['text2']};margin-bottom:4px;">{icon} {label}</div>
            <div style="font-size:24px;font-weight:800;color:{clr};text-shadow:0 0 20px {clr}44;">{val_str}</div>
            {delta_str}
        </div>
    </div>"""

def gauge_chart(value, max_val, title, color="#10B981", height=200):
    fig = go.Figure(go.Indicator(mode="gauge+number+delta", value=value, title={"text": title, "font": {"size": 14, "color": "rgba(255,255,255,0.7)"}},
        number={"font": {"size": 28, "color": color}}, delta={"reference": max_val * 0.5},
        gauge={"axis": {"range": [0, max_val], "tickcolor": "rgba(255,255,255,0.3)", "tickfont": {"size": 10, "color": "rgba(255,255,255,0.5)"}},
               "bar": {"color": color}, "bgcolor": "rgba(0,0,0,0)",
               "steps": [{"range": [0, max_val*0.5], "color": "rgba(239,68,68,0.1)"}, {"range": [max_val*0.5, max_val*0.8], "color": "rgba(245,158,11,0.1)"}, {"range": [max_val*0.8, max_val], "color": "rgba(16,185,129,0.1)"}]}))
    fig.update_layout(height=height, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor="rgba(0,0,0,0)", font={"color": "rgba(255,255,255,0.7)"})
    return fig

def sparkline_chart(data, height=60, color=None, fill=True):
    C = THEMES[st.session_state.theme]
    clr = color or C["accent"]
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=data, mode="lines", line=dict(width=2, color=clr), fill="tozeroy" if fill else None,
                  fillcolor=f"rgba{tuple(int(clr.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + (0.1,)}" if clr.startswith("#") else "rgba(37,99,235,0.1)",
                  showlegend=False))
    fig.update_layout(height=height, margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      xaxis=dict(visible=False), yaxis=dict(visible=False))
    return fig

# ─── PAGE 1: EXECUTIVE COMMAND DASHBOARD ───
def page_executive_command():
    C = THEMES[st.session_state.theme]; maybe_compact()
    kpis = get_executive_kpis(); trends = get_kpi_sparklines()
    st.markdown(f"""<div style="margin-bottom:16px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Executive Command Dashboard</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Enterprise Risk Command Engine — Real-time intelligence overview</p>
    </div>""", unsafe_allow_html=True)
    st.markdown(f"""<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:8px;margin-bottom:16px;">
        {holographic_kpi("Total Customers", kpis["total_customers"], icon="👥", color=C["accent"])}
        {holographic_kpi("Active", kpis["active_customers"], icon="✅", color=C["success"])}
        {holographic_kpi("High Risk", kpis["high_risk"], icon="⚠️", color=C["danger"])}
        {holographic_kpi("Churn Rate", f'{kpis["churn_rate"]}%', icon="📉", color="#F59E0B")}
        {holographic_kpi("Rev at Risk", f'${kpis["revenue_at_risk"]:,.0f}', icon="💰", color=C["danger"])}
        {holographic_kpi("Avg CLV", f'${kpis["clv_avg"]:,.0f}', icon="💎", color=C["neon"])}
        {holographic_kpi("Retention", f'{kpis["retention_rate"]}%', icon="🔄", color=C["success"])}
        {holographic_kpi("CSAT", kpis["csat"], icon="⭐", color=C["accent"])}
        {holographic_kpi("NPS", kpis["nps"], icon="📊", color=C["success"])}
        {holographic_kpi("Happiness", f'{kpis["happiness_index"]}%', icon="😊", color=C["neon"])}
    </div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="glow-card"><h3> KPI Trend Sparklines (90 days)</h3></div>""", unsafe_allow_html=True)
    cols = st.columns(5)
    for i, (name, key) in enumerate([("Churn Rate", "churn_rate"), ("Revenue", "revenue"), ("CSAT", "csat"), ("NPS", "nps"), ("Happiness", "happiness")]):
        with cols[i]:
            df = trends[key]
            val = df["value"].iloc[-1]
            delta = val - df["value"].iloc[0]
            st.markdown(f"""<div style="text-align:center;"><span style="font-size:12px;color:{C["text2"]};">{name}</span>
                <div style="font-size:18px;font-weight:700;color:{C["accent"]};">{val:.1f}</div></div>""", unsafe_allow_html=True)
            st.plotly_chart(sparkline_chart(df["value"].values, color={"churn_rate":C["danger"],"revenue":C["success"],"csat":C["accent"],"nps":C["neon"],"happiness":C["success"]}.get(key,"#10B981")), use_container_width=True)
    st.markdown(f"""<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-top:12px;">""", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.plotly_chart(gauge_chart(kpis["retention_rate"], 100, "Retention Rate", C["success"]), use_container_width=True)
    with col2:
        st.plotly_chart(gauge_chart(kpis["csat"] * 20, 100, "CSAT Score", C["accent"]), use_container_width=True)
    with col3:
        st.plotly_chart(gauge_chart(max(0, kpis["nps"] + 50), 150, "NPS Score", C["neon"]), use_container_width=True)

# ─── PAGE 2: AI COMMAND CENTER ───
def page_ai_command_center():
    C = THEMES[st.session_state.theme]; maybe_compact()
    ai = get_ai_status()
    status_clr = {"ONLINE": C["success"], "DEGRADED": C["warning"], "OFFLINE": C["danger"]}.get(ai["status"], C["text"])
    st.markdown(f"""<div style="margin-bottom:16px;"><h1 style="font-size:32px;font-weight:800;margin:0;">AI Command Center</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Live AI infrastructure monitoring and model health</p></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="glow-card" style="text-align:center;border:2px solid {status_clr}44;">
        <div style="display:flex;align-items:center;justify-content:center;gap:16px;">
            <div style="width:16px;height:16px;border-radius:50%;background:{status_clr};box-shadow:0 0 20px {status_clr};animation:pulse 1.5s infinite;"></div>
            <span style="font-size:28px;font-weight:800;color:{status_clr};">AI STATUS: {ai["status"]}</span>
        </div>
    </div>""", unsafe_allow_html=True)
    st.markdown(f"""<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:8px;margin-top:12px;">
        {holographic_kpi("Model", ai["model_version"], icon="🧠", color=C["accent"])}
        {holographic_kpi("Latency", f'{ai["inference_latency_ms"]}ms', icon="⚡", color=C["neon"])}
        {holographic_kpi("Throughput", f'{ai["predictions_per_minute"]:,}/min', icon="📊", color=C["success"])}
        {holographic_kpi("Confidence", f'{ai["model_confidence"]}%', icon="🎯", color=C["accent"])}
        {holographic_kpi("Drift", ai["drift_status"], icon="🔄", color={"Stable":C["success"],"Warning":C["warning"],"Critical":C["danger"]}.get(ai["drift_status"],C["text"]))}
        {holographic_kpi("Uptime", f'{ai["uptime_hours"]}h', icon="⏱️", color=C["success"])}
        {holographic_kpi("Predictions", f'{ai["total_predictions"]:,}', icon="🔢", color=C["neon"])}
        {holographic_kpi("Queue", f'{ai["queue_depth"]}', icon="📨", color={"Normal":C["success"],"High":C["warning"],"Critical":C["danger"]}.get(ai["queue_status"],C["text"]))}
    </div>""", unsafe_allow_html=True)
    st.markdown(f"""<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-top:12px;">""", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: st.plotly_chart(gauge_chart(100 - ai["cpu_util"], 100, "CPU Available", C["neon"]), use_container_width=True)
    with c2: st.plotly_chart(gauge_chart(100 - ai["memory_util"], 100, "Memory Available", C["accent"]), use_container_width=True)
    with c3: st.plotly_chart(gauge_chart(100 - ai["gpu_util"], 100, "GPU Available", C["success"]), use_container_width=True)
    st.markdown(f"""<div class="glass" style="padding:12px;margin-top:8px;display:flex;justify-content:space-between;">
        <span>Last trained: <strong>{ai["last_trained"]}</strong></span>
        <span>Total predictions: <strong>{ai["total_predictions"]:,}</strong></span>
        <span>Queue: <strong style="color:{C["success"]};">{ai["queue_status"]}</strong></span>
    </div>""", unsafe_allow_html=True)

# ─── PAGE 3: GLOBAL RISK INTELLIGENCE ───
def page_global_risk_intel():
    C = THEMES[st.session_state.theme]; maybe_compact()
    df = get_regional_risk()
    st.markdown(f"""<div style="margin-bottom:16px;"><h1 style="font-size:32px;font-weight:800;margin:0;">Global Risk Intelligence Center</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Regional churn hotspots, revenue exposure, customer density</p></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:8px;margin-bottom:12px;">
        {holographic_kpi("Regions", len(df), icon="🌍", color=C["accent"])}
        {holographic_kpi("Total Customers", df["customers"].sum(), icon="👥", color=C["success"])}
        {holographic_kpi("Avg Churn", f'{df["churn"].mean():.1f}%', icon="📉", color=C["danger"])}
        {holographic_kpi("High Risk Regions", len(df[df["risk"]=="High"]), icon="🔴", color=C["danger"])}
    </div>""", unsafe_allow_html=True)
    fig = go.Figure()
    for _, row in df.iterrows():
        clr = {"Low": "#10B981", "Medium": "#F59E0B", "High": "#EF4444"}.get(row["risk"], "#6B7280")
        fig.add_trace(go.Scattergeo(lon=[row["lon"]], lat=[row["lat"]], text=f"<b>{row['region']}</b><br>Churn: {row['churn']}%<br>CSAT: {row['csat']}<br>Revenue: ${row['revenue']:,.0f}",
            mode="markers+text", marker=dict(size=row["customers"]/150, color=clr, line=dict(width=2,color="white"), cmin=0, cmax=1), name=row["region"],
            textposition="top center", textfont=dict(size=10, color=C["text"])))
    fig.update_layout(title="Global Risk Map", height=450, geo=dict(showland=True, landcolor=C["surface2"], coastlinecolor=C["text2"],
        showocean=True, oceancolor=C["surface"], projection_type="natural earth", showframe=False),
        paper_bgcolor="rgba(0,0,0,0)", font=dict(color=C["text"]))
    st.plotly_chart(fig, use_container_width=True)
    fig = px.treemap(df, path=["region"], values="revenue", color="churn", color_continuous_scale="RdYlGn_r",
                     title="Revenue Exposure Treemap", hover_data={"customers":True,"csat":True})
    fig.update_layout(height=350, paper_bgcolor="rgba(0,0,0,0)", font=dict(color=C["text"]))
    st.plotly_chart(fig, use_container_width=True)

# ─── PAGE 4: REVENUE INTELLIGENCE ───
def page_revenue_intel_premium():
    C = THEMES[st.session_state.theme]; maybe_compact()
    kpis = get_executive_kpis()
    st.markdown(f"""<div style="margin-bottom:16px;"><h1 style="font-size:32px;font-weight:800;margin:0;">Revenue Intelligence Dashboard</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Revenue trends, CLV, forecasts, upsell/cross-sell potential</p></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:8px;">
        {holographic_kpi("Monthly Revenue", f'${kpis["monthly_revenue"]:,.0f}', icon="💰", color=C["success"])}
        {holographic_kpi("Rev at Risk", f'${kpis["revenue_at_risk"]:,.0f}', icon="⚠️", color=C["danger"])}
        {holographic_kpi("Avg CLV", f'${kpis["clv_avg"]:,.0f}', icon="💎", color=C["accent"])}
        {holographic_kpi("Upsell Potential", f'${kpis["upsell_potential"]:,.0f}', icon="📈", color=C["neon"])}
        {holographic_kpi("Cross-Sell Potential", f'${kpis["cross_sell_potential"]:,.0f}', icon="🔗", color=C["warning"])}
    </div>""", unsafe_allow_html=True)
    trends = get_kpi_sparklines()
    df = trends["revenue"]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["date"], y=df["value"], mode="lines", line=dict(width=3, color=C["success"]), name="Revenue", fill="tozeroy", fillcolor="rgba(16,185,129,0.1)"))
    fig.update_layout(title="Revenue Trend (90 days)", height=350, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color=C["text"])
    st.plotly_chart(fig, use_container_width=True)
    seg_df = get_segment_data()
    fig = px.bar(seg_df, x="segment", y="avg_clv", color="avg_clv", text_auto=True, title="CLV by Segment",
                 color_continuous_scale="Viridis", height=350)
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color=C["text"])
    st.plotly_chart(fig, use_container_width=True)

# ─── PAGE 5: CX INTELLIGENCE PREMIUM ───
def page_cx_intel_premium():
    C = THEMES[st.session_state.theme]; maybe_compact()
    kpis = get_executive_kpis()
    st.markdown(f"""<div style="margin-bottom:16px;"><h1 style="font-size:32px;font-weight:800;margin:0;">Customer Experience Intelligence</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Satisfaction, NPS, sentiment, happiness, and engagement</p></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:8px;">
        {holographic_kpi("CSAT", kpis["csat"], icon="⭐", color=C["accent"])}
        {holographic_kpi("NPS", kpis["nps"], icon="📊", color=C["success"])}
        {holographic_kpi("Happiness", f'{kpis["happiness_index"]}%', icon="😊", color=C["neon"])}
        {holographic_kpi("Retention", f'{kpis["retention_rate"]}%', icon="🔄", color=C["success"])}
    </div>""", unsafe_allow_html=True)
    trends = get_kpi_sparklines()
    fig = make_subplots(rows=2, cols=2, subplot_titles=("CSAT Trend", "NPS Trend", "Happiness Trend", "Retention Trend"))
    for i, (key, name, clr) in enumerate([("csat", "CSAT", C["accent"]), ("nps", "NPS", C["success"]), ("happiness", "Happiness", C["neon"]), ("retention", "Retention", C["success"])]):
        df = trends[key]; r, c = i // 2 + 1, i % 2 + 1
        fig.add_trace(go.Scatter(y=df["value"].values, mode="lines", line=dict(width=2,color=clr), name=name, showlegend=False), row=r, col=c)
    fig.update_layout(height=450, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color=C["text"])
    st.plotly_chart(fig, use_container_width=True)
    segments = ["Very Satisfied", "Satisfied", "Neutral", "Dissatisfied", "Very Dissatisfied"]
    scores = [np.random.randint(300, 2000) for _ in range(5)]
    fig = px.pie(values=scores, names=segments, hole=0.4, title="Customer Sentiment Distribution",
                 color_discrete_sequence=px.colors.sequential.RdYlGn)
    fig.update_layout(height=350, paper_bgcolor="rgba(0,0,0,0)", font=dict(color=C["text"]))
    cols = st.columns(2)
    with cols[0]: st.plotly_chart(fig, use_container_width=True)
    with cols[1]:
        st.plotly_chart(gauge_chart(kpis["csat"]*20, 100, "Overall CSAT", C["accent"]), use_container_width=True)

# ─── PAGE 6: SEGMENTATION PREMIUM ───
def page_segmentation_premium():
    C = THEMES[st.session_state.theme]; maybe_compact()
    df = get_segment_data()
    st.markdown(f"""<div style="margin-bottom:16px;"><h1 style="font-size:32px;font-weight:800;margin:0;">Customer Segmentation</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Treemap, sunburst, and bubble chart — segment intelligence</p></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:8px;">
        {holographic_kpi("Champions", f'{df[df["segment"]=="Champions"]["count"].values[0]:,}', icon="🏆", color="#10B981")}
        {holographic_kpi("At Risk", f'{df[df["segment"]=="At Risk"]["count"].values[0]:,}', icon="⚠️", color="#F59E0B")}
        {holographic_kpi("Lost", f'{df[df["segment"]=="Lost Customers"]["count"].values[0]:,}', icon="❌", color="#EF4444")}
    </div>""", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        fig = px.treemap(df, path=["segment"], values="count", color="churn_rate", color_continuous_scale="RdYlGn_r",
                         title="Segment Treemap", hover_data={"avg_clv":True})
        fig.update_layout(height=400, paper_bgcolor="rgba(0,0,0,0)", font=dict(color=C["text"]))
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.sunburst(df, path=["segment"], values="count", color="churn_rate", color_continuous_scale="RdYlGn_r",
                          title="Segment Sunburst")
        fig.update_layout(height=400, paper_bgcolor="rgba(0,0,0,0)", font=dict(color=C["text"]))
        st.plotly_chart(fig, use_container_width=True)
    fig = px.scatter(df, x="churn_rate", y="avg_clv", size="count", color="segment", text="segment",
                     title="Segment Bubble Chart", size_max=80, color_discrete_sequence=df["color"].tolist())
    fig.update_traces(textposition="middle center", textfont=dict(size=11, color="white"))
    fig.update_layout(height=400, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color=C["text"])
    st.plotly_chart(fig, use_container_width=True)

# ─── PAGE 7: CUSTOMER JOURNEY PREMIUM ───
def page_journey_premium():
    C = THEMES[st.session_state.theme]; maybe_compact()
    funnel = get_journey_funnel(); sankey = get_sankey_data()
    st.markdown(f"""<div style="margin-bottom:16px;"><h1 style="font-size:32px;font-weight:800;margin:0;">Customer Journey Analytics</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Funnel analysis, Sankey diagram, drop-off points</p></div>""", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        fig = go.Figure(go.Funnel(y=funnel["stage"], x=funnel["count"], textinfo="value+percent initial",
            marker=dict(color=[C["accent"], C["success"], C["neon"], C["warning"], "#8B5CF6", C["danger"]],
            line=dict(width=2, color="white"))))
        fig.update_layout(title="Customer Journey Funnel", height=400, paper_bgcolor="rgba(0,0,0,0)", font=dict(color=C["text"]))
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        labels = list(dict.fromkeys(sankey["source"] + sankey["target"]))
        label_indices = {l: i for i, l in enumerate(labels)}
        fig = go.Figure(go.Sankey(
            node=dict(label=labels, color=[C["accent"], C["danger"], C["success"], C["neon"], C["warning"], C["text2"], "#8B5CF6"],
                      pad=15, thickness=20, line=dict(color="white", width=1)),
            link=dict(source=[label_indices[s] for s in sankey["source"]],
                      target=[label_indices[t] for t in sankey["target"]],
                      value=sankey["value"])))
        fig.update_layout(title="Customer Flow Sankey", height=400, paper_bgcolor="rgba(0,0,0,0)", font=dict(color=C["text"]))
        st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"""<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:8px;">""", unsafe_allow_html=True)
    for _, row in funnel.iterrows():
        st.markdown(f"""<div class="glass" style="padding:10px;display:flex;justify-content:space-between;">
            <span><strong>{row["stage"]}</strong></span>
            <span><span style="color:{C["accent"]};">{row["count"]:,}</span> customers · <span style="color:{C["danger"]};">{row["dropoff"]:,} drop-off</span></span>
        </div>""", unsafe_allow_html=True)

# ─── PAGE 8: VOICE OF CUSTOMER PREMIUM ───
def page_voc_premium():
    C = THEMES[st.session_state.theme]; maybe_compact()
    voc = get_voice_of_customer(); words = get_word_cloud_data()
    st.markdown(f"""<div style="margin-bottom:16px;"><h1 style="font-size:32px;font-weight:800;margin:0;">Voice of Customer</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Reviews, surveys, tickets, emails, chats — sentiment & topic analysis</p></div>""", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""<div class="glow-card"><h3>⚠️ Top Complaints</h3></div>""", unsafe_allow_html=True)
        for issue, count in sorted(voc["complaints"].items(), key=lambda x: x[1], reverse=True):
            bar_pct = count / max(voc["complaints"].values()) * 100
            st.markdown(f"""<div style="margin:4px 0;"><div style="display:flex;justify-content:space-between;font-size:13px;">
                <span>{issue}</span><span style="color:{C["accent"]};">{count}</span></div>
                <div style="height:4px;background:{C["surface2"]};border-radius:2px;overflow:hidden;">
                <div style="width:{bar_pct}%;height:100%;background:{C["danger"]};border-radius:2px;"></div></div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="glow-card"><h3>🌟 Top Praises</h3></div>""", unsafe_allow_html=True)
        for issue, count in sorted(voc["praises"].items(), key=lambda x: x[1], reverse=True):
            bar_pct = count / max(voc["praises"].values()) * 100
            st.markdown(f"""<div style="margin:4px 0;"><div style="display:flex;justify-content:space-between;font-size:13px;">
                <span>{issue}</span><span style="color:{C["success"]};">{count}</span></div>
                <div style="height:4px;background:{C["surface2"]};border-radius:2px;overflow:hidden;">
                <div style="width:{bar_pct}%;height:100%;background:{C["success"]};border-radius:2px;"></div></div></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="glow-card" style="margin-top:12px;"><h3> Topic Distribution</h3></div>""", unsafe_allow_html=True)
    topics_df = pd.DataFrame(list(voc["topics"].items()), columns=["Topic", "Share"])
    fig = px.pie(topics_df, values="Share", names="Topic", hole=0.4,
                 color_discrete_sequence=px.colors.sequential.Viridis_r)
    fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", font=dict(color=C["text"]))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"""<div class="glow-card" style="margin-top:12px;"><h3> Word Cloud (Frequency)</h3></div>""", unsafe_allow_html=True)
    wc_html = "".join(f"""<span style="display:inline-block;font-size:{10 + count//10}px;color:{C["accent"]};margin:4px 6px;opacity:{0.3 + count/500};">{word}</span>""" for word, count in words[:40])
    st.markdown(f"""<div class="glass" style="padding:16px;text-align:center;line-height:2;">{wc_html}</div>""", unsafe_allow_html=True)

# ─── PAGE 9: EXPLAINABLE AI DIAGNOSTIC CHAMBER V2 ───
def page_diagnostic_v2():
    C = THEMES[st.session_state.theme]; maybe_compact()
    st.markdown(f"""<div style="margin-bottom:16px;"><h1 style="font-size:32px;font-weight:800;margin:0;">Explainable AI Diagnostic Chamber</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">SHAP waterfall, force plots, counterfactual, and customer A/B comparison</p></div>""", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1: cust_a = st.text_input("Customer A", "C1001", key="diag_a")
    with col2: cust_b = st.text_input("Customer B", "C1042", key="diag_b")
    st.markdown(f"""<div class="glow-card"><h3> SHAP Waterfall Explanation</h3></div>""", unsafe_allow_html=True)
    shap = get_shap_waterfall(0)
    fig = go.Figure(go.Waterfall(name="SHAP", orientation="h",
        measure=["relative"] * len(shap["features"]) + ["total"],
        y=shap["features"] + ["Prediction"],
        x=shap["shap_values"] + [shap["final_value"]],
        text=[f"{v:+.3f}" for v in shap["shap_values"]] + [f"{shap['final_value']:.3f}"],
        connector={"line": {"color": "rgba(255,255,255,0.3)"}},
        decreasing={"marker": {"color": C["danger"]}},
        increasing={"marker": {"color": C["success"]}},
        totals={"marker": {"color": C["accent"]}}))
    fig.update_layout(title=f"SHAP Waterfall — {cust_a}", height=450, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color=C["text"], xaxis=dict(tickfont=dict(color=C["text2"])), yaxis=dict(tickfont=dict(color=C["text2"])))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"""<div class="glow-card" style="margin-top:12px;"><h3> A/B Comparison: {cust_a} vs {cust_b}</h3></div>""", unsafe_allow_html=True)
    c360_a = get_customer_360(cust_a); c360_b = get_customer_360(cust_b)
    compare_df = pd.DataFrame({
        "Attribute": ["Contract", "Tenure", "Monthly Charges", "Tech Support", "Churn Risk", "CSAT", "Engagement"],
        cust_a: [c360_a["contract"], c360_a["tenure_months"], f'${c360_a["monthly_charges"]}', c360_a["tech_support"], f'{c360_a["churn_risk"]:.0%}', c360_a["csat"], f'{c360_a["engagement_score"]:.0f}%'],
        cust_b: [c360_b["contract"], c360_b["tenure_months"], f'${c360_b["monthly_charges"]}', c360_b["tech_support"], f'{c360_b["churn_risk"]:.0%}', c360_b["csat"], f'{c360_b["engagement_score"]:.0f}%'],
    })
    st.dataframe(compare_df, use_container_width=True, hide_index=True)
    higher_risk = "Customer A" if c360_a["churn_risk"] > c360_b["churn_risk"] else "Customer B"
    st.markdown(f"""<div class="glass" style="padding:16px;margin-top:8px;border-left:3px solid {C["accent"]};">
        <strong style="color:{C["accent"]};">Why did {cust_a} churn while {cust_b} remained loyal?</strong><br>
        <span style="color:{C["text2"]};">{higher_risk} has {'a month-to-month contract' if compare_df.loc[0, higher_risk]=='Month-to-month' else 'a long-term contract'} 
        and {'no tech support' if compare_df.loc[3, higher_risk]=='No' else 'tech support'}, with {'$' + str(c360_a["monthly_charges"]) if higher_risk==cust_a else '$' + str(c360_b["monthly_charges"])} monthly charges.
        The SHAP analysis shows contract type and monthly charges are the top drivers of churn risk.</span>
    </div>""", unsafe_allow_html=True)

# ─── PAGE 10: AI COPILOT PREMIUM ───
def page_ai_copilot_premium():
    C = THEMES[st.session_state.theme]; maybe_compact()
    from aegisxai.services.copilot_service import CopilotEngine
    st.markdown(f"""<div style="margin-bottom:16px;"><h1 style="font-size:32px;font-weight:800;margin:0;">AI Executive Copilot</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Natural language analytics — ask anything about your business</p></div>""", unsafe_allow_html=True)
    if "premium_copilot" not in st.session_state: st.session_state.premium_copilot = []
    if "copilot_engine" not in st.session_state: st.session_state.copilot_engine = CopilotEngine()
    suggestions = ["Why did churn increase this week?", "Show top 10 high-risk customers",
                   "Which region has the highest risk?", "Summarize today's business risks"]
    st.markdown(f"""<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:8px;">""", unsafe_allow_html=True)
    cols = st.columns(4)
    for i, s in enumerate(suggestions):
        with cols[i]:
            if st.button(s, key=f"sug_{i}", use_container_width=True):
                st.session_state["copilot_input_trigger"] = s
                st.rerun()
    engine = st.session_state.copilot_engine
    trigger = st.session_state.get("copilot_input_trigger", "")
    question = st.chat_input("Ask a business question...", key="copilot_premium_input")
    if trigger and not question:
        question = trigger
        st.session_state["copilot_input_trigger"] = ""
    if question:
        st.session_state.premium_copilot.append({"role": "user", "content": question})
        answer, viz = engine.ask(question)
        with st.chat_message("assistant"):
            st.markdown(f"""<div class="glass" style="padding:16px;">{answer}</div>""", unsafe_allow_html=True)
            if isinstance(viz, pd.DataFrame) and not viz.empty:
                fig = px.bar(viz.head(10) if "RiskScore" in viz.columns else viz, x=viz.columns[0], y=viz.columns[1],
                             color=viz.columns[1] if len(viz.columns) > 1 else None, height=300,
                             color_continuous_scale="Viridis")
                fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color=C["text"])
                st.plotly_chart(fig, use_container_width=True)
        st.session_state.premium_copilot.append({"role": "assistant", "content": answer[:200]})
    for msg in st.session_state.premium_copilot[-6:]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"][:300] if msg["role"] == "assistant" else msg["content"])

# ─── PAGE 11: SCENARIO SIMULATION LAB V2 ───
def page_scenario_v2():
    C = THEMES[st.session_state.theme]; maybe_compact()
    st.markdown(f"""<div style="margin-bottom:16px;"><h1 style="font-size:32px;font-weight:800;margin:0;">Scenario Simulation Lab</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">What-if analysis — adjust levers and see churn/revenue impact</p></div>""", unsafe_allow_html=True)
    levers = get_scenario_simulation()
    st.markdown(f"""<div class="glow-card"><h3> Simulation Levers</h3></div>""", unsafe_allow_html=True)
    values = {}
    cols = st.columns(3)
    for i, (key, lever) in enumerate(levers.items()):
        with cols[i % 3]:
            lbl = f"{key} ({lever['unit']})" if lever["unit"] else key
            if isinstance(lever["current"], float):
                values[key] = st.slider(lbl, float(lever["min"]), float(lever["max"]), float(lever["current"]), key=f"sim_{key}")
            else:
                values[key] = st.slider(lbl, lever["min"], lever["max"], lever["current"], key=f"sim_{key}")
    result = calculate_scenario_impact(levers, values)
    st.markdown(f"""<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:8px;margin-top:12px;">
        {holographic_kpi("Current Churn", f'{result["base_churn"]}%', icon="📊", color=C["text2"])}
        {holographic_kpi("Projected Churn", f'{result["new_churn"]}%', icon="🎯", color=C["accent"])}
        {holographic_kpi("Change", f'{result["churn_change"]:+.1f}%', icon="📈", color=C["success"] if result["churn_change"] < 0 else C["danger"])}
        {holographic_kpi("Revenue Impact", f'${result["revenue_impact"]:,.0f}', icon="💰", color=C["success"] if result["revenue_impact"] < 0 else C["danger"])}
        {holographic_kpi("Customers Saved", f'{abs(result["customers_saved"]):.0f}', icon="👥", color=C["success"])}
    </div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="glow-card" style="margin-top:12px;"><h3> Impact Breakdown</h3></div>""", unsafe_allow_html=True)
    for key, detail in result["details"].items():
        st.markdown(f"""<div class="glass" style="padding:8px 12px;margin:3px 0;font-size:13px;">{detail}</div>""", unsafe_allow_html=True)

# ─── PAGE 12: LIVE OPERATIONS COMMAND CENTER ───
def page_live_ops():
    C = THEMES[st.session_state.theme]; maybe_compact()
    st.markdown(f"""<div style="margin-bottom:16px;"><h1 style="font-size:32px;font-weight:800;margin:0;">Live Operations Command Center</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Real-time event stream, live counters, and system health</p></div>""", unsafe_allow_html=True)
    if "live_events" not in st.session_state: st.session_state.live_events = pd.DataFrame()
    auto = st.checkbox("Auto-refresh (3s)", value=True)
    if auto or st.button(" Refresh Now"):
        new = get_live_events(10)
        st.session_state.live_events = pd.concat([st.session_state.live_events, new]).drop_duplicates(subset="id").tail(50)
    events = st.session_state.live_events
    if not events.empty:
        ecounts = events["type"].value_counts()
        st.markdown(f"""<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:8px;">""", unsafe_allow_html=True)
        for etype, count in ecounts.items():
            clr = {"Network Failure":C["danger"],"App Crash":C["danger"],"Payment Issue":C["warning"],
                   "Login Failure":C["warning"],"Sentiment Spike":C["success"],"Data Sync":C["accent"]}.get(etype, C["text"])
            st.markdown(holographic_kpi(etype, count, icon="📡", color=clr), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        active = events[events["status"] == "Active"]
        st.markdown(f"""<div class="glass" style="padding:12px;margin-top:8px;border-left:3px solid {C["danger"]};">Active incidents: {len(active)}</div>""", unsafe_allow_html=True)
        st.markdown(f"""<div class="glow-card" style="margin-top:12px;"><h3> Live Event Feed</h3></div>""", unsafe_allow_html=True)
        for _, evt in events.tail(15).iterrows():
            sc = {"Active": C["danger"], "Investigating": C["warning"], "Resolved": C["success"]}
            st.markdown(f"""<div class="glass" style="padding:6px 12px;margin:2px 0;display:flex;justify-content:space-between;font-size:13px;">
                <span><span style="color:{sc.get(evt["status"], C["text2"])};font-weight:600;">●</span> {evt["type"]}</span>
                <span><span style="color:{C["text2"]};">{evt["message"]}</span> <span style="color:{C["accent"]};">{evt["timestamp"]}</span></span>
            </div>""", unsafe_allow_html=True)
        if auto: st.rerun()

# ─── PAGE 13: ALERT MANAGEMENT CENTER ───
def page_alert_mgmt():
    C = THEMES[st.session_state.theme]; maybe_compact()
    df = get_alerts()
    st.markdown(f"""<div style="margin-bottom:16px;"><h1 style="font-size:32px;font-weight:800;margin:0;">Alert Management Center</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Critical alerts, escalation workflow, SLA monitoring</p></div>""", unsafe_allow_html=True)
    sev_counts = df["severity"].value_counts()
    st.markdown(f"""<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:8px;">
        {holographic_kpi("Critical", sev_counts.get("Critical",0), icon="🔴", color=C["danger"])}
        {holographic_kpi("High", sev_counts.get("High",0), icon="🟠", color=C["warning"])}
        {holographic_kpi("Medium", sev_counts.get("Medium",0), icon="🟡", color=C["accent"])}
        {holographic_kpi("Low", sev_counts.get("Low",0), icon="🟢", color=C["success"])}
    </div>""", unsafe_allow_html=True)
    sla_counts = df["sla"].value_counts()
    fig = px.pie(values=sla_counts.values, names=sla_counts.index, hole=0.4, title="SLA Compliance",
                 color_discrete_map={"Within SLA":C["success"],"At Risk":C["warning"],"Breached":C["danger"]})
    fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", font=dict(color=C["text"]))
    cols = st.columns([1, 2])
    with cols[0]: st.plotly_chart(fig, use_container_width=True)
    with cols[1]:
        st.markdown(f"""<div class="glow-card"><h3> Recent Alerts</h3></div>""", unsafe_allow_html=True)
        for _, alert in df.sort_values("created", ascending=False).head(8).iterrows():
            sc = {"Critical": C["danger"], "High": C["warning"], "Medium": C["accent"], "Low": C["success"]}
            st.markdown(f"""<div class="glass" style="padding:6px 12px;margin:2px 0;display:flex;justify-content:space-between;font-size:12px;">
                <span><span style="color:{sc.get(alert["severity"], C["text2"])};font-weight:700;">●</span> {alert["title"][:40]}</span>
                <span><span style="color:{C["text2"]};">{alert["status"]}</span> <span style="color:{C["accent"]};">{alert["sla"]}</span></span>
            </div>""", unsafe_allow_html=True)

# ─── PAGE 14: INCIDENT MANAGEMENT ───
def page_incident_mgmt():
    C = THEMES[st.session_state.theme]; maybe_compact()
    df = get_incident_data()
    st.markdown(f"""<div style="margin-bottom:16px;"><h1 style="font-size:32px;font-weight:800;margin:0;">Incident Management Dashboard</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Track, triage, and resolve incidents with SLA monitoring</p></div>""", unsafe_allow_html=True)
    status_counts = df["status"].value_counts()
    st.markdown(f"""<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:8px;">
        {holographic_kpi("Open", status_counts.get("Open",0), icon="📂", color=C["danger"])}
        {holographic_kpi("In Progress", status_counts.get("In Progress",0), icon="🔄", color=C["warning"])}
        {holographic_kpi("Resolved", status_counts.get("Resolved",0), icon="✅", color=C["success"])}
        {holographic_kpi("Escalated", status_counts.get("Escalated",0), icon="⬆️", color="#8B5CF6")}
    </div>""", unsafe_allow_html=True)
    sev_df = df["severity"].value_counts().reset_index()
    sev_df.columns = ["Severity", "Count"]
    fig = px.bar(sev_df, x="Severity", y="Count", color="Severity", text_auto=True, height=300,
                 color_discrete_map={"Critical":C["danger"],"High":C["warning"],"Medium":C["accent"],"Low":C["success"]})
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color=C["text"])
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"""<div class="glow-card"><h3> Incident List</h3></div>""", unsafe_allow_html=True)
    for _, inc in df.sort_values("created", ascending=False).head(10).iterrows():
        sc = {"Critical": C["danger"], "High": C["warning"], "Medium": C["accent"], "Low": C["success"]}
        sla_clr = {"Within SLA": C["success"], "At Risk": C["warning"], "Breached": C["danger"]}
        st.markdown(f"""<div class="glass" style="padding:8px 12px;margin:2px 0;display:flex;justify-content:space-between;font-size:13px;">
            <div><span style="color:{sc.get(inc["severity"], C["text2"])};font-weight:700;">●</span> <strong>{inc["id"]}</strong> — {inc["title"]}</div>
            <div><span style="color:{C["text2"]};">{inc["owner"]}</span> · <span style="color:{C["accent"]};">{inc["status"]}</span></div>
        </div>""", unsafe_allow_html=True)

# ─── PAGE 15: MODEL INTELLIGENCE CENTER ───
def page_model_intel():
    C = THEMES[st.session_state.theme]; maybe_compact()
    metrics = get_model_metrics()
    st.markdown(f"""<div style="margin-bottom:16px;"><h1 style="font-size:32px;font-weight:800;margin:0;">Model Intelligence Center</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Accuracy, precision, recall, ROC-AUC, confusion matrix, drift</p></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:8px;">
        {holographic_kpi("Accuracy", f'{metrics["accuracy"]:.1%}', icon="🎯", color=C["accent"])}
        {holographic_kpi("Precision", f'{metrics["precision"]:.1%}', icon="📊", color=C["success"])}
        {holographic_kpi("Recall", f'{metrics["recall"]:.1%}', icon="🔍", color=C["neon"])}
        {holographic_kpi("F1 Score", f'{metrics["f1"]:.1%}', icon="⚖️", color=C["warning"])}
        {holographic_kpi("ROC-AUC", f'{metrics["roc_auc"]:.1%}', icon="📈", color=C["success"])}
        {holographic_kpi("PR-AUC", f'{metrics["pr_auc"]:.1%}', icon="📉", color=C["accent"])}
    </div>""", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=metrics["fpr"], y=metrics["tpr"], mode="lines", name="ROC (AUC={:.3f})".format(metrics["roc_auc"]),
                      line=dict(width=3, color=C["accent"]), fill="tozeroy", fillcolor="rgba(37,99,235,0.1)"))
        fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines", line=dict(dash="dash", color=C["text2"]), name="Random"))
        fig.update_layout(title="ROC Curve", height=350, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color=C["text"])
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        cm = metrics["confusion_matrix"]
        fig = px.imshow(cm, text_auto=True, color_continuous_scale="Blues", title="Confusion Matrix",
                        x=["Predicted No", "Predicted Yes"], y=["Actual No", "Actual Yes"])
        fig.update_layout(height=350, paper_bgcolor="rgba(0,0,0,0)", font=dict(color=C["text"]))
        st.plotly_chart(fig, use_container_width=True)

# ─── PAGE 16: DRIFT DETECTION ───
def page_drift_detection():
    C = THEMES[st.session_state.theme]; maybe_compact()
    df = get_drift_data()
    st.markdown(f"""<div style="margin-bottom:16px;"><h1 style="font-size:32px;font-weight:800;margin:0;">Drift Detection Dashboard</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Data drift, feature drift, prediction drift — early warning system</p></div>""", unsafe_allow_html=True)
    status_counts = df["status"].value_counts()
    st.markdown(f"""<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:8px;">
        {holographic_kpi("Stable", status_counts.get("Stable",0), icon="✅", color=C["success"])}
        {holographic_kpi("Warning", status_counts.get("Warning",0), icon="⚠️", color=C["warning"])}
        {holographic_kpi("Critical", status_counts.get("Critical",0), icon="🔴", color=C["danger"])}
    </div>""", unsafe_allow_html=True)
    fig = px.bar(df, x="feature", y="drift_score", color="status", text_auto=".2f", title="Feature Drift Scores",
                 color_discrete_map={"Stable":C["success"],"Warning":C["warning"],"Critical":C["danger"]}, height=400)
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color=C["text"])
    fig.add_hline(y=0.1, line_dash="dash", line_color=C["success"], annotation_text="Warning Threshold")
    fig.add_hline(y=0.2, line_dash="dash", line_color=C["danger"], annotation_text="Critical Threshold")
    st.plotly_chart(fig, use_container_width=True)
    fig = px.imshow([df["drift_score"].values], y=["Drift"], x=df["feature"], color_continuous_scale="RdYlGn_r",
                    title="Feature Drift Heatmap", text_auto=".2f", height=150)
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color=C["text"]))
    st.plotly_chart(fig, use_container_width=True)

# ─── PAGE 17: CUSTOMER 360 PREMIUM ───
def page_c360_premium():
    C = THEMES[st.session_state.theme]; maybe_compact()
    st.markdown(f"""<div style="margin-bottom:16px;"><h1 style="font-size:32px;font-weight:800;margin:0;">Customer 360°</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Complete customer profile — history, risk, satisfaction, revenue</p></div>""", unsafe_allow_html=True)
    cust_id = st.text_input("Customer ID", "C1001", key="c360_id")
    c360 = get_customer_360(cust_id)
    risk_clr = {0: C["success"], 1: C["warning"], 2: C["danger"]}[min(2, int(c360["churn_risk"] * 3))]
    st.markdown(f"""<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:8px;">
        {holographic_kpi("Churn Risk", f'{c360["churn_risk"]:.0%}', icon="🎯", color=risk_clr)}
        {holographic_kpi("Tenure", f'{c360["tenure_months"]}mo', icon="📅", color=C["accent"])}
        {holographic_kpi("Monthly", f'${c360["monthly_charges"]}', icon="💰", color=C["success"])}
        {holographic_kpi("CLV", f'${c360["lifetime_value"]}', icon="💎", color=C["neon"])}
        {holographic_kpi("CSAT", c360["csat"], icon="⭐", color=C["accent"])}
        {holographic_kpi("Engagement", f'{c360["engagement_score"]:.0f}%', icon="📊", color=C["success"])}
        {holographic_kpi("Loyalty", c360["loyalty_tier"], icon="🏅", color={"Bronze":"#CD7F32","Silver":"#C0C0C0","Gold":"#FFD700","Platinum":"#E5E4E2"}.get(c360["loyalty_tier"], C["text"]))}
    </div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="glow-card" style="margin-top:12px;"><h3> Profile Details</h3></div>""", unsafe_allow_html=True)
    cols = st.columns(3)
    details = [
        ("Gender", c360["gender"]), ("Contract", c360["contract"]), ("Internet", c360["internet_service"]),
        ("Tech Support", c360["tech_support"]), ("Payment", c360["payment_method"]), ("Age", c360["age"]),
        ("Total Charges", f'${c360["total_charges"]}'), ("Tickets (30d)", c360["tickets_30d"]), ("Services", c360["service_count"]),
    ]
    for i, (label, val) in enumerate(details):
        with cols[i % 3]: st.markdown(f"""<div class="glass" style="padding:8px;text-align:center;">
            <div style="font-size:11px;color:{C["text2"]};">{label}</div><div style="font-size:16px;font-weight:600;">{val}</div></div>""", unsafe_allow_html=True)

# ─── PAGE 18: TEAM PERFORMANCE PREMIUM ───
def page_team_perf_premium():
    C = THEMES[st.session_state.theme]; maybe_compact()
    df = get_team_perf_premium()
    st.markdown(f"""<div style="margin-bottom:16px;"><h1 style="font-size:32px;font-weight:800;margin:0;">Team Performance Analytics</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Agent productivity, resolution quality, ratings, and rankings</p></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:8px;">
        {holographic_kpi("Teams", len(df), icon="👥", color=C["accent"])}
        {holographic_kpi("Avg Quality", f'{df["quality"].mean():.1f}%', icon="⭐", color=C["success"])}
        {holographic_kpi("Avg Rating", f'{df["rating"].mean():.2f}', icon="📊", color=C["neon"])}
        {holographic_kpi("Avg Resolution", f'{df["resolution_time"].mean():.0f}min', icon="⏱️", color=C["warning"])}
    </div>""", unsafe_allow_html=True)
    fig = px.bar(df.sort_values("quality", ascending=True), y="team", x="quality", orientation="h", text="quality",
                 color="quality", color_continuous_scale="Viridis", title="Team Quality Rankings", height=400)
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color=C["text"])
    st.plotly_chart(fig, use_container_width=True)
    fig = px.scatter(df, x="resolution_time", y="satisfaction", size="resolved", color="team",
                     text="team", title="Resolution Time vs Satisfaction", height=350)
    fig.update_traces(textposition="top center")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color=C["text"])
    st.plotly_chart(fig, use_container_width=True)

# ─── PAGE 19: RETENTION CAMPAIGN ───
def page_retention_campaign():
    C = THEMES[st.session_state.theme]; maybe_compact()
    df = get_campaigns()
    st.markdown(f"""<div style="margin-bottom:16px;"><h1 style="font-size:32px;font-weight:800;margin:0;">Retention Campaign Dashboard</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Campaign reach, conversion, ROI, and retention improvement</p></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:8px;">
        {holographic_kpi("Total Reach", f'{df["reach"].sum():,}', icon="📢", color=C["accent"])}
        {holographic_kpi("Total Conversions", f'{df["conversions"].sum():,}', icon="✅", color=C["success"])}
        {holographic_kpi("Avg ROI", f'{df["roi"].mean():.1f}x', icon="💰", color=C["neon"])}
        {holographic_kpi("Avg Retention Lift", f'{df["retention_improvement"].mean():.1f}%', icon="📈", color=C["success"])}
    </div>""", unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Reach", x=df["name"], y=df["reach"], marker_color=C["accent"]))
    fig.add_trace(go.Bar(name="Conversions", x=df["name"], y=df["conversions"], marker_color=C["success"]))
    fig.update_layout(title="Campaign Performance", height=350, barmode="group",
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color=C["text"])
    st.plotly_chart(fig, use_container_width=True)
    fig = px.bar(df, x="name", y="roi", color="roi", text_auto=".1f", title="Campaign ROI",
                 color_continuous_scale="Viridis", height=350)
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color=C["text"])
    st.plotly_chart(fig, use_container_width=True)

# ─── PAGE 20: SECURITY & GOVERNANCE ───
def page_security_governance():
    C = THEMES[st.session_state.theme]; maybe_compact()
    sec = get_security_data()
    st.markdown(f"""<div style="margin-bottom:16px;"><h1 style="font-size:32px;font-weight:800;margin:0;">Security & Governance Dashboard</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">GDPR, SOC2, ISO 27001 — security monitoring, compliance, model fairness</p></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:8px;">
        {holographic_kpi("Login Attempts (24h)", f'{sec["login_attempts_24h"]:,}', icon="🔑", color=C["accent"])}
        {holographic_kpi("Failed Logins", sec["failed_logins"], icon="🚫", color=C["danger"])}
        {holographic_kpi("MFA Enabled", f'{sec["mfa_enabled"]}%', icon="🔐", color=C["success"])}
        {holographic_kpi("GDPR Compliance", f'{sec["gdpr_compliance"]}%', icon="📋", color=C["success"])}
        {holographic_kpi("Model Fairness", f'{sec["model_fairness"]:.0%}', icon="⚖️", color=C["accent"])}
        {holographic_kpi("Consent Rate", f'{sec["consent_rate"]}%', icon="✅", color=C["neon"])}
    </div>""", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        compliance_items = {"GDPR": sec["gdpr_compliance"], "SOC2": 96.0, "ISO 27001": 98.5, "Consent": sec["consent_rate"]}
        fig.add_trace(go.Bar(x=list(compliance_items.keys()), y=list(compliance_items.values()), marker_color=[C["accent"], C["success"], C["neon"], C["warning"]],
                             text=[f"{v}%" for v in compliance_items.values()], textposition="outside"))
        fig.update_layout(title="Compliance Scorecard", height=300, yaxis=dict(range=[0, 100]),
                          paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color=C["text"])
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown(f"""<div class="glow-card"><h3> Certifications & Status</h3></div>""", unsafe_allow_html=True)
        st.markdown(f"""<div class="glass" style="padding:12px;margin:4px 0;border-left:3px solid {C["success"]};">
            <strong style="color:{C["success"]};">SOC2</strong> — {sec["soc2_status"]}</div>
            <div class="glass" style="padding:12px;margin:4px 0;border-left:3px solid {C["neon"]};">
            <strong style="color:{C["neon"]};">ISO 27001</strong> — {sec["iso27001_status"]}</div>
            <div class="glass" style="padding:12px;margin:4px 0;border-left:3px solid {sec['data_breaches_30d']==0 and C['success'] or C['danger']};">
            <strong>Data Breaches (30d)</strong> — {sec["data_breaches_30d"]} · Active Privacy Requests: {sec["privacy_requests"]}</div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="glass" style="padding:12px;margin-top:8px;text-align:center;border:1px solid {C["success"]}22;">
        <span style="color:{C["success"]};font-weight:600;"> All systems compliant</span> — Audit trail complete. Last audit: {(datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")}
    </div>""", unsafe_allow_html=True)

# ─── PAGE 21: REPORTING CENTER ───
def page_reporting_center():
    C = THEMES[st.session_state.theme]; maybe_compact()
    st.markdown(f"""<div style="margin-bottom:16px;"><h1 style="font-size:32px;font-weight:800;margin:0;">Reporting Center</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Generate PDF, Excel, and CSV reports with KPIs, charts, and XAI insights</p></div>""", unsafe_allow_html=True)
    report_type = st.selectbox("Report Type", ["Executive Summary", "Churn Analysis", "Revenue Report", "Model Performance", "Full Audit"])
    report_format = st.selectbox("Format", ["PDF", "Excel", "CSV", "HTML"])
    include_sections = []
    col1, col2, col3 = st.columns(3)
    with col1: include_sections.append(st.checkbox("KPIs", True))
    with col2: include_sections.append(st.checkbox("Charts", True))
    with col3: include_sections.append(st.checkbox("XAI Insights", True))
    if st.button(" Generate Report", use_container_width=True):
        kpis = get_executive_kpis()
        html = f"""<html><body style="font-family:sans-serif;padding:40px;background:#fff;color:#111;">
            <h1 style="color:#2563EB;border-bottom:3px solid #2563EB;padding-bottom:12px;">{report_type}</h1>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | AegisXAI v4.0</p>
            <hr><h2>Executive KPIs</h2><table style="width:100%;border-collapse:collapse;">
            <tr><th style="text-align:left;border-bottom:2px solid #2563EB;padding:8px;">Metric</th>
            <th style="text-align:right;border-bottom:2px solid #2563EB;padding:8px;">Value</th></tr>"""
        for k, v in [("Total Customers", kpis["total_customers"]), ("Churn Rate", f'{kpis["churn_rate"]}%'),
                     ("Revenue at Risk", f'${kpis["revenue_at_risk"]:,.0f}'), ("Avg CLV", f'${kpis["clv_avg"]:,.0f}'),
                     ("CSAT", kpis["csat"]), ("NPS", kpis["nps"]), ("Retention Rate", f'{kpis["retention_rate"]}%')]:
            html += f'<tr><td style="padding:6px;border-bottom:1px solid #eee;">{k}</td><td style="text-align:right;padding:6px;border-bottom:1px solid #eee;font-weight:bold;">{v}</td></tr>'
        html += "</table><hr><p style='color:#999;font-size:12px;'>AegisXAI Enterprise Risk Command Engine | Confidential</p></body></html>"
        buf = io.BytesIO()
        buf.write(html.encode())
        b64 = base64.b64encode(buf.getvalue()).decode()
        sfx = {"PDF":"pdf","Excel":"xlsx","CSV":"csv","HTML":"html"}[report_format]
        st.markdown(f"""<div class="glass" style="padding:20px;margin-top:16px;text-align:center;">
            <span style="font-size:18px;color:{C["success"]};"> Report generated!</span>
            <div style="margin-top:12px;">
                <a href="data:text/html;base64,{b64}" download="aegisxai_report.{sfx}"
                   style="background:{C["accent"]};color:white;padding:10px 32px;border-radius:8px;text-decoration:none;font-weight:600;display:inline-block;">
                   Download {report_format}</a></div></div>""", unsafe_allow_html=True)

# ─── PAGE 22: PREMIUM WIDGETS ───
def page_premium_widgets():
    C = THEMES[st.session_state.theme]; maybe_compact()
    st.markdown(f"""<div style="margin-bottom:16px;"><h1 style="font-size:32px;font-weight:800;margin:0;">Premium Dashboard Widgets</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Floating AI Core, holographic cards, global clock, notifcations, search, and more</p></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="glow-card" style="text-align:center;padding:24px;position:relative;overflow:hidden;">
        <div style="position:absolute;top:50%;left:50%;width:200px;height:200px;margin:-100px 0 0 -100px;border-radius:50%;
            background:conic-gradient(from 0deg, {C["accent"]}, {C["neon"]}, {C["success"]}, {C["accent"]});
            animation:spin 4s linear infinite;opacity:0.15;"></div>
        <div style="position:relative;z-index:1;">
            <div style="font-size:14px;color:{C["text2"]};">⚡ AI Core Status</div>
            <div style="font-size:48px;font-weight:800;background:{C["gradient"]};-webkit-background-clip:text;-webkit-text-fill-color:transparent;">
            AEGIS-XAI</div>
            <div style="display:flex;justify-content:center;gap:24px;margin-top:12px;font-size:13px;color:{C["text2"]};">
                <span>🧠 Model: <strong style="color:{C["accent"]};">XGBoost v4</strong></span>
                <span>⚡ Latency: <strong style="color:{C["neon"]};">14ms</strong></span>
                <span>📊 Throughput: <strong style="color:{C["success"]};">14,200/min</strong></span>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)
    import pytz
    timezones = {"NY": "America/New_York", "LDN": "Europe/London", "DXB": "Asia/Dubai", "TKY": "Asia/Tokyo", "SYD": "Australia/Sydney"}
    st.markdown(f"""<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:8px;margin-top:12px;">
        {holographic_kpi("Local", datetime.now().strftime("%H:%M"), icon="🕐", color=C["accent"])}""", unsafe_allow_html=True)
    for city, tz in timezones.items():
        try:
            t = datetime.now(pytz.timezone(tz)).strftime("%H:%M")
        except:
            t = "--:--"
        st.markdown(holographic_kpi(city, t, icon="🌍", color=C["neon"]), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown(f"""<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:12px;">""", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""<div class="glow-card"><h3> Recent Activities</h3></div>""", unsafe_allow_html=True)
        activities = ["Model retrained successfully", "APAC churn alert triggered", "Report generated: Executive Summary",
                      "New customer segment: 142 At Risk", "Data drift detected: Contract feature", "SLA breached: INC-5021",
                      "Campaign launched: Loyalty Rewards", "User login: admin@aegisxai.io"]
        for act in activities:
            st.markdown(f"""<div class="glass" style="padding:6px 10px;margin:2px 0;font-size:12px;display:flex;align-items:center;gap:6px;">
                <span style="color:{C["accent"]};">▸</span> {act}</div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="glow-card"><h3> Notification Center</h3></div>""", unsafe_allow_html=True)
        notifications = [
            ("🔴", "Critical: Churn risk >90% for 47 customers", "5 min ago"),
            ("🟡", "Warning: APAC churn rate increased 2.1%", "12 min ago"),
            ("🟢", "Resolved: Payment issue cluster", "23 min ago"),
            ("🔵", "Info: Weekly report ready for review", "1 hour ago"),
            ("⚪", "System: Backup completed successfully", "2 hours ago"),
        ]
        for icon, msg, time in notifications:
            st.markdown(f"""<div class="glass" style="padding:6px 10px;margin:2px 0;display:flex;justify-content:space-between;font-size:12px;">
                <span>{icon} {msg}</span><span style="color:{C["text2"]};">{time}</span></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="glow-card" style="margin-top:12px;"><h3> Quick Actions</h3></div>""", unsafe_allow_html=True)
    cols = st.columns(4)
    actions = [(" Generate Report", "file"), (" Run Analysis", "search"), ("  Configure", "settings"), ("  Help Center", "info")]
    for i, (label, _) in enumerate(actions):
        with cols[i]:
            if st.button(label, use_container_width=True):
                st.toast(f"Action triggered: {label.strip()}")

PREMIUM_PAGE_FUNCTIONS = {
    "Executive Command": page_executive_command,
    "AI Command Center": page_ai_command_center,
    "Global Risk Intel": page_global_risk_intel,
    "Revenue Intel Premium": page_revenue_intel_premium,
    "CX Intel Premium": page_cx_intel_premium,
    "Segmentation Premium": page_segmentation_premium,
    "Journey Premium": page_journey_premium,
    "Voice of Customer": page_voc_premium,
    "XAI Diagnostic v2": page_diagnostic_v2,
    "AI Copilot Premium": page_ai_copilot_premium,
    "Scenario Lab v2": page_scenario_v2,
    "Live Ops Center": page_live_ops,
    "Alert Management": page_alert_mgmt,
    "Incident Management": page_incident_mgmt,
    "Model Intel Center": page_model_intel,
    "Drift Detection": page_drift_detection,
    "Customer 360": page_c360_premium,
    "Team Perf Premium": page_team_perf_premium,
    "Retention Campaigns": page_retention_campaign,
    "Security & Governance": page_security_governance,
    "Reporting Center": page_reporting_center,
    "Premium Widgets": page_premium_widgets,
}
