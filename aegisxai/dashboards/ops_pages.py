"""
Operations & Visualization Pages - Global Ops, Digital Twin, Network Graph, Streaming
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from aegisxai.dashboards.components import *
from aegisxai.dashboards.pages import THEMES
from aegisxai.services.advanced_features import *

def page_global_ops():
    C = THEMES[st.session_state.theme]
    maybe_compact()
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Global Operations Command Center</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Worldwide operations monitoring with regional risk analysis</p>
    </div>""", unsafe_allow_html=True)

    regions = get_global_ops_data()
    df_regions = pd.DataFrame(regions).T.reset_index().rename(columns={"index": "Region"})

    col1, col2, col3, col4 = st.columns(4)
    total_cust = sum(r["customers"] for r in regions.values())
    total_rev = sum(r["revenue"] for r in regions.values())
    avg_churn = np.mean([r["churn"] for r in regions.values()])
    with col1:
        st.metric("Total Customers", f"{total_cust:,}")
    with col2:
        st.metric("Total Revenue", f"${total_rev:,.0f}")
    with col3:
        st.metric("Avg Churn", f"{avg_churn:.1f}%")
    with col4:
        high_risk = sum(1 for r in regions.values() if r["risk"] == "High")
        st.metric("High Risk Regions", high_risk)

    fig = go.Figure()
    for name, data in regions.items():
        fig.add_trace(go.Scattergeo(
            lon=[data["lon"]], lat=[data["lat"]],
            text=f"{name}<br>Churn: {data['churn']}%<br>CSAT: {data['csat']}<br>Revenue: ${data['revenue']:,.0f}",
            mode="markers+text", name=name,
            marker=dict(size=data["customers"] / 150, sizemode="area",
                        color={"Low": "#10B981", "Medium": "#F59E0B", "High": "#EF4444"}.get(data["risk"], "#6B7280"),
                        line=dict(width=2, color="white")),
            textposition="top center", textfont=dict(size=9, color=C["text"]),
        ))
    fig.update_layout(title="Global Operations Map", height=500,
                      geo=dict(showland=True, landcolor=C["surface2"], coastlinecolor=C["text2"],
                               showocean=True, oceancolor=C["surface"],
                               projection_type="natural earth", showframe=False),
                      paper_bgcolor="rgba(0,0,0,0)", font=dict(color=C["text"]))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""<div class="glow-card" style="margin-top:12px;"><h3>Regional Details</h3></div>""", unsafe_allow_html=True)
    st.dataframe(df_regions[["Region", "customers", "churn", "csat", "revenue", "risk"]].round(1), use_container_width=True)

def page_digital_twin():
    C = THEMES[st.session_state.theme]
    maybe_compact()
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Enterprise Digital Twin</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Live digital replica of your organization — monitor status, risk propagation, dependencies</p>
    </div>""", unsafe_allow_html=True)

    entities, dependencies = get_digital_twin()
    status_emoji = {"Healthy": "🟢", "Warning": "🟡", "Critical": "🔴"}

    cols = st.columns(3)
    for i, (name, data) in enumerate(entities.items()):
        with cols[i % 3]:
            st.markdown(f"""<div class="glow-card" style="text-align:center;padding:16px;">
                <div style="font-size:36px;margin-bottom:8px;">{status_emoji.get(data['status'], '⚪')}</div>
                <div style="font-size:18px;font-weight:700;">{name}</div>
                <div style="font-size:28px;font-weight:800;color:{C['accent']};">{data['health']}%</div>
                <div style="font-size:12px;color:{C['text2']};">{data['status']} · {data.get('count', data.get('uptime', 'N/A'))}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class="glow-card" style="margin-top:16px;"><h3>Dependency Graph</h3></div>""", unsafe_allow_html=True)
    dep_df = pd.DataFrame(dependencies, columns=["Source", "Target"])
    fig = go.Figure()
    for src, tgt in dependencies:
        fig.add_annotation(x=hash(src) % 5, y=hash(tgt) % 5, text="→", showarrow=True,
                          ax=hash(src) % 5 + 0.3, ay=hash(tgt) % 5 + 0.3,
                          arrowhead=2, arrowsize=1.5, arrowwidth=2, arrowcolor=C["text2"])
    fig.update_layout(height=200, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      xaxis=dict(visible=False), yaxis=dict(visible=False))
    st.markdown(f"""<div class="glass" style="padding:12px;">
        <span style="color:{C["text2"]};">Dependencies: </span>
        {', '.join(f'<span style="color:{C["accent"]};">{s} → {t}</span>' for s, t in dependencies)}
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class="glow-card" style="margin-top:16px;"><h3>Risk Propagation Simulation</h3></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="glass" style="padding:16px;">
        <p>If <strong>Network</strong> goes down: <span style="color:{C["danger"]};">Customers (70%), Products (50%), Support Teams (30%)</span></p>
        <p>If <strong>APAC Region</strong> fails: <span style="color:{C["danger"]};">Business Units (25%), Customer Satisfaction (15%)</span></p>
        <p><span style="color:{C["text2"]};">Last sync: {datetime.now().strftime("%H:%M:%S")}</span></p>
    </div>""", unsafe_allow_html=True)

def page_network_graph():
    C = THEMES[st.session_state.theme]
    maybe_compact()
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Customer Relationship Network Graph</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Family connections, corporate accounts, shared subscriptions, referral chains</p>
    </div>""", unsafe_allow_html=True)

    G = get_network_graph(60)
    pos = get_network_positions(G)

    edge_trace = go.Scatter(
        x=[], y=[], line=dict(width=0.5, color=C["text2"]), hoverinfo="none", mode="lines")
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace["x"] += (x0, x1, None)
        edge_trace["y"] += (y0, y1, None)

    node_trace = go.Scatter(
        x=[], y=[], mode="markers+text", hoverinfo="text", text=[],
        marker=dict(showscale=True, colorscale="Viridis", size=[], color=[],
                    line=dict(width=1, color="white")), textposition="top center", textfont=dict(size=8, color=C["text"]))
    for node in G.nodes():
        x, y = pos[node]
        node_trace["x"] += (x,)
        node_trace["y"] += (y,)
        node_trace["marker"]["size"] += (10 + G.nodes[node]["churn_risk"] * 20,)
        node_trace["marker"]["color"] += (G.nodes[node]["churn_risk"],)
        ntype = G.nodes[node]["type"]
        node_trace["text"] += (f"{ntype[0]}",)

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(title="Customer Relationship Graph", height=550,
                                     paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                     xaxis=dict(visible=False), yaxis=dict(visible=False),
                                     hovermode="closest", showlegend=False))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""<div class="glow-card" style="margin-top:12px;"><h3>Network Statistics</h3></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div style="display:flex;gap:16px;">
        <div class="kpi-card"><div class="kpi-value">{G.number_of_nodes()}</div><div class="kpi-label">Nodes</div></div>
        <div class="kpi-card"><div class="kpi-value">{G.number_of_edges()}</div><div class="kpi-label">Edges</div></div>
        <div class="kpi-card"><div class="kpi-value">{sum(1 for n in G.nodes() if G.nodes[n]['type']=='Corporate')}</div><div class="kpi-label">Corporate</div></div>
        <div class="kpi-card"><div class="kpi-value">{sum(1 for n in G.nodes() if G.nodes[n]['type']=='Family')}</div><div class="kpi-label">Family</div></div>
    </div>""", unsafe_allow_html=True)

def page_streaming_analytics():
    C = THEMES[st.session_state.theme]
    maybe_compact()
    st.markdown(f"""<div style="margin-bottom:24px;">
        <h1 style="font-size:32px;font-weight:800;margin:0;">Real-Time Streaming Analytics</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Simulated Kafka/Event Hub/Kinesis event stream — continuous processing</p>
    </div>""", unsafe_allow_html=True)

    if "stream_running" not in st.session_state:
        st.session_state.stream_running = False
        st.session_state.stream_events = pd.DataFrame()

    col1, col2, col3 = st.columns(3)
    with col1:
        source_filter = st.multiselect("Sources", ["Mobile App", "Web Portal", "IVR", "Store", "Email", "SMS"],
                                       default=["Mobile App", "Web Portal"])
    with col2:
        auto_refresh = st.checkbox("Auto-refresh (3s)", value=False)
    with col3:
        if st.button("▶️ Start Stream" if not st.session_state.stream_running else "⏹ Stop Stream",
                     use_container_width=True):
            st.session_state.stream_running = not st.session_state.stream_running

    new_events = get_streaming_events(8)
    new_events = new_events[new_events["source"].isin(source_filter)] if source_filter else new_events
    if st.session_state.stream_running:
        st.session_state.stream_events = pd.concat([st.session_state.stream_events, new_events]).drop_duplicates(subset="id").tail(50)
        if auto_refresh:
            st.rerun()

    events = st.session_state.stream_events
    if not events.empty:
        fig = go.Figure()
        for src in events["source"].unique():
            sub = events[events["source"] == src]
            fig.add_trace(go.Scatter(x=sub.index, y=sub["value"], mode="lines+markers",
                          name=src, line=dict(width=2)))
        fig.update_layout(title="Event Stream (Value over Time)", height=300,
                          paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color=C["text"], xaxis=dict(tickfont=dict(color=C["text2"])),
                          yaxis=dict(tickfont=dict(color=C["text2"])))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""<div class="glow-card"><h3>Recent Events ({len(events)})</h3></div>""", unsafe_allow_html=True)
    for _, evt in events.tail(12).iterrows():
        status_c = {"Success": C["success"], "Failed": C["danger"], "Pending": C["warning"]}
        st.markdown(f"""<div class="glass" style="padding:6px 12px;margin:2px 0;display:flex;justify-content:space-between;font-size:13px;">
            <span><span style="color:{C["accent"]};">{evt["type"]}</span> from {evt["source"]} — {evt["customer"]}</span>
            <span><span style="color:{status_c.get(evt["status"], C["text2"])};">{evt["status"]}</span> ${evt["value"]:.0f} <span style="color:{C["text2"]};">{evt["timestamp"]}</span></span>
        </div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class="glow-card" style="margin-top:12px;"><h3>Throughput</h3></div>""", unsafe_allow_html=True)
    success = len(events[events["status"] == "Success"])
    failed = len(events[events["status"] == "Failed"])
    st.markdown(f"""<div style="display:flex;gap:16px;">
        <div class="kpi-card"><div class="kpi-value" style="color:{C["success"]};">{success}</div><div class="kpi-label">Processed</div></div>
        <div class="kpi-card"><div class="kpi-value" style="color:{C["danger"]};">{failed}</div><div class="kpi-label">Failed</div></div>
        <div class="kpi-card"><div class="kpi-value" style="color:{C["accent"]};">{len(events["type"].unique())}</div><div class="kpi-label">Event Types</div></div>
    </div>""", unsafe_allow_html=True)

OPS_PAGE_FUNCTIONS = {
    "Global Operations Center": page_global_ops,
    "Digital Twin": page_digital_twin,
    "Network Graph": page_network_graph,
    "Streaming Analytics": page_streaming_analytics,
}
