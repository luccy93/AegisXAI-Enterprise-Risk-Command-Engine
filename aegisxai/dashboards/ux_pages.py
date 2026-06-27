"""
Premium UX Feature Pages - Calendar, Collaboration, Voice Commands, Onboarding Tour, Digital Twin Workspace, etc.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from aegisxai.dashboards.components import maybe_compact
from aegisxai.dashboards.pages import THEMES
from aegisxai.services.premium_ux import *

def page_voice_commands():
    C = THEMES[st.session_state.theme]; maybe_compact()
    st.markdown(f"""<div style="margin-bottom:16px;"><h1 style="font-size:32px;font-weight:800;margin:0;"> Voice Command Interface</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Interact with AegisXAI using voice commands</p></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="glow-card" style="text-align:center;padding:32px;">
        <div style="font-size:64px;margin-bottom:16px;animation:pulse 2s infinite;">🎤</div>
        <div style="font-size:18px;color:{C["accent"]};font-weight:600;">Listening for commands...</div>
        <div style="font-size:13px;color:{C["text2"]};margin-top:8px;">Say: "Show critical customers" or "Generate executive report"</div>
        <div style="margin-top:16px;display:flex;gap:8px;justify-content:center;">
            <span style="background:{C["surface2"]};padding:6px 16px;border-radius:20px;font-size:13px;color:{C["text"]};">🎤 Start Listening</span>
            <span style="background:{C["surface2"]};padding:6px 16px;border-radius:20px;font-size:13px;color:{C["text"]};">⏹ Stop</span>
        </div>
    </div>""", unsafe_allow_html=True)
    commands = get_voice_commands()
    st.markdown(f"""<div class="glow-card" style="margin-top:16px;"><h3> Available Commands</h3></div>""", unsafe_allow_html=True)
    for cmd, action in commands:
        st.markdown(f"""<div class="glass" style="padding:10px 14px;margin:3px 0;display:flex;justify-content:space-between;">
            <span style="color:{C["accent"]};">🎯 "{cmd}"</span>
            <span style="color:{C["text2"]};">→ {action}</span>
        </div>""", unsafe_allow_html=True)
    if st.button(" Test Voice Recognition (simulated)", use_container_width=True):
        st.markdown(f"""<div class="glass" style="padding:16px;margin-top:8px;border-left:3px solid {C["success"]};">
            <span style="color:{C["success"]};">✅ Recognized: "Show critical customers"</span><br>
            <span style="color:{C["text2"]};">→ Navigating to Risk Queue with critical severity filter</span>
        </div>""", unsafe_allow_html=True)

def page_collaboration_panel():
    C = THEMES[st.session_state.theme]; maybe_compact()
    st.markdown(f"""<div style="margin-bottom:16px;"><h1 style="font-size:32px;font-weight:800;margin:0;">Team Collaboration Panel</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Notes, mentions, comments, and shared dashboards</p></div>""", unsafe_allow_html=True)
    if "collab_notes" not in st.session_state: st.session_state.collab_notes = []
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(f"""<div class="glow-card"><h3> Team Feed</h3></div>""", unsafe_allow_html=True)
        notes = [
            ("@john Please investigate Customer C1024's billing issue", "Sarah Chen", "5 min ago", "🔴"),
            ("@emily APAC report ready for review in Reports section", "Mike Torres", "12 min ago", "📊"),
            ("Retention campaign launch scheduled for tomorrow 10 AM", "Lisa Kumar", "1 hour ago", "📋"),
            ("@all: Model retraining completed — XGBoost v4.0 deployed", "System", "2 hours ago", "🤖"),
            ("INC-5021 escalated to Level 2 support", "Alex Rivera", "3 hours ago", "🚨"),
        ]
        for msg, author, time, icon in notes:
            st.markdown(f"""<div class="glass" style="padding:10px;margin:3px 0;">
                <div style="font-size:13px;">{icon} {msg}</div>
                <div style="font-size:11px;color:{C["text2"]};margin-top:4px;">by {author} · {time}</div>
            </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="glow-card"><h3> Add Note</h3></div>""", unsafe_allow_html=True)
        with st.form("collab_form"):
            mention = st.selectbox("Mention", ["@all", "@john", "@emily", "@mike", "@lisa", "@alex"])
            note = st.text_area("Message", placeholder="Type your note or mention...", height=100)
            if st.form_submit_button(" Post", use_container_width=True):
                st.session_state.collab_notes.append({"mention": mention, "note": note, "author": st.session_state.username, "time": datetime.now().strftime("%H:%M")})
                st.rerun()
    if st.session_state.collab_notes:
        st.markdown(f"""<div class="glow-card" style="margin-top:12px;"><h3> Recent Posts</h3></div>""", unsafe_allow_html=True)
        for n in reversed(st.session_state.collab_notes[-5:]):
            st.markdown(f"""<div class="glass" style="padding:8px 12px;margin:2px 0;font-size:13px;">
                <span style="color:{C["accent"]};">{n["mention"]}</span> {n["note"]}
                <span style="color:{C["text2"]};font-size:11px;margin-left:8px;">— {n["author"]} at {n["time"]}</span>
            </div>""", unsafe_allow_html=True)

def page_calendar_scheduler():
    C = THEMES[st.session_state.theme]; maybe_compact()
    st.markdown(f"""<div style="margin-bottom:16px;"><h1 style="font-size:32px;font-weight:800;margin:0;">Executive Calendar & Scheduler</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Meetings, follow-ups, campaign schedules, retention tasks</p></div>""", unsafe_allow_html=True)
    events = get_calendar_events()
    today = datetime.now().date()
    cols = st.columns(7)
    days_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    week_start = today - timedelta(days=today.weekday())
    for i, (name, col) in enumerate(zip(days_names, cols)):
        d = week_start + timedelta(days=i)
        is_today = d == today
        day_events = [e for e in events if e["date"] == d]
        col.markdown(f"""<div style="text-align:center;padding:8px;border-radius:8px;
            background:{'rgba(37,99,235,0.2)' if is_today else 'transparent'};
            border:{'1px solid '+C['accent'] if is_today else '1px solid transparent'};">
            <div style="font-size:11px;color:{C['text2']};">{name}</div>
            <div style="font-size:20px;font-weight:700;color:{C['accent'] if is_today else C['text']};">{d.day}</div>
            <div style="font-size:10px;color:{C['success']};">{len(day_events)} events</div>
        </div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="glow-card" style="margin-top:12px;"><h3> Upcoming Events</h3></div>""", unsafe_allow_html=True)
    for ev in events[:8]:
        day_str = ev["date"].strftime("%a, %b %d")
        type_colors = {"Meeting": C["accent"], "Task": C["success"], "Follow-up": C["warning"], "Workshop": C["neon"]}
        st.markdown(f"""<div class="glass" style="padding:10px 14px;margin:3px 0;display:flex;justify-content:space-between;align-items:center;">
            <div><span style="color:{type_colors.get(ev['type'], C['text2'])};">●</span> <strong>{ev["title"]}</strong></div>
            <div><span style="color:{C["text2"]};">{day_str}</span> <span style="color:{C["accent"]};">{ev["time"]}</span></div>
        </div>""", unsafe_allow_html=True)

def page_onboarding_tour():
    C = THEMES[st.session_state.theme]; maybe_compact()
    st.markdown(f"""<div style="margin-bottom:16px;"><h1 style="font-size:32px;font-weight:800;margin:0;">Guided Onboarding Tour</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Interactive walkthrough of AegisXAI's key features</p></div>""", unsafe_allow_html=True)
    steps = get_onboarding_steps()
    if "tour_step" not in st.session_state: st.session_state.tour_step = 0
    total = len(steps)
    current = st.session_state.tour_step
    step = steps[current]
    progress = (current + 1) / total * 100
    st.markdown(f"""<div style="width:100%;height:4px;background:{C["surface2"]};border-radius:2px;margin-bottom:16px;overflow:hidden;">
        <div style="width:{progress}%;height:100%;background:{C["gradient"]};border-radius:2px;transition:width 0.5s;"></div>
    </div>""", unsafe_allow_html=True)
    st.markdown(f"""<div style="text-align:center;padding:32px;" class="glow-card">
        <div style="font-size:48px;margin-bottom:16px;">{"🚀📊🤖🔬🎯"[current]}</div>
        <div style="font-size:24px;font-weight:700;margin-bottom:8px;">Step {current+1}: {step["title"]}</div>
        <div style="color:{C["text2"]};font-size:14px;max-width:400px;margin:0 auto;">{step["content"]}</div>
        <div style="margin-top:20px;display:flex;gap:12px;justify-content:center;">
            <span style="font-size:12px;color:{C["text2"]};">{current+1} of {total}</span>
        </div>
    </div>""", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if current > 0 and st.button("← Back", use_container_width=True):
            st.session_state.tour_step -= 1; st.rerun()
    with col2:
        if current < total - 1 and st.button("Next →", use_container_width=True):
            st.session_state.tour_step += 1; st.rerun()
    with col3:
        if st.button("Skip Tour", use_container_width=True):
            st.session_state.tour_step = 0; st.rerun()

def page_achievements():
    C = THEMES[st.session_state.theme]; maybe_compact()
    ach = get_achievements()
    st.markdown(f"""<div style="margin-bottom:16px;"><h1 style="font-size:32px;font-weight:800;margin:0;">Achievements & Gamification</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Support team performance — badges, leaderboards, rewards</p></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;">
        <div class="glow-card" style="text-align:center;"><span style="font-size:32px;">🏆</span>
            <div style="font-size:14px;color:{C["text2"]};">Top Agent</div>
            <div style="font-size:18px;font-weight:700;">{ach["top_agent"]["name"]}</div>
            <div style="font-size:12px;color:{C["accent"]};">Score: {ach["top_agent"]["score"]}</div></div>
        <div class="glow-card" style="text-align:center;"><span style="font-size:32px;">⚡</span>
            <div style="font-size:14px;color:{C["text2"]};">Fastest Resolver</div>
            <div style="font-size:18px;font-weight:700;">{ach["fastest_resolver"]["name"]}</div>
            <div style="font-size:12px;color:{C["accent"]};">Avg: {ach["fastest_resolver"]["avg_time"]}</div></div>
        <div class="glow-card" style="text-align:center;"><span style="font-size:32px;">⭐</span>
            <div style="font-size:14px;color:{C["text2"]};">Highest CSAT</div>
            <div style="font-size:18px;font-weight:700;">{ach["highest_csat"]["name"]}</div>
            <div style="font-size:12px;color:{C["accent"]};">Score: {ach["highest_csat"]["score"]}</div></div>
    </div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="glow-card" style="margin-top:16px;"><h3> Leaderboard</h3></div>""", unsafe_allow_html=True)
    for i, (name, pts, badge) in enumerate(ach["leaderboard"]):
        st.markdown(f"""<div class="glass" style="padding:8px 14px;margin:2px 0;display:flex;justify-content:space-between;">
            <span>{badge} {name}</span><span style="color:{C["accent"]};">{pts:,} pts</span>
        </div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="glow-card" style="margin-top:12px;"><h3> Badges</h3></div>""", unsafe_allow_html=True)
    for name, desc, icon in ach["badges"]:
        st.markdown(f"""<div class="glass" style="padding:10px;margin:3px 0;display:flex;align-items:center;gap:12px;">
            <span style="font-size:28px;">{icon}</span>
            <div><strong>{name}</strong><br><span style="font-size:12px;color:{C["text2"]};">{desc}</span></div>
        </div>""", unsafe_allow_html=True)

def page_digital_twin_workspace():
    C = THEMES[st.session_state.theme]; maybe_compact()
    st.markdown(f"""<div style="margin-bottom:16px;"><h1 style="font-size:32px;font-weight:800;margin:0;">Digital Twin Workspace</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Live visual representation of customers, regions, products, and networks</p></div>""", unsafe_allow_html=True)
    entities = ["Customers", "Regions", "Products", "Networks", "Support Teams", "Business Units"]
    connections = [("Customers", "Products"), ("Customers", "Networks"), ("Regions", "Customers"),
                   ("Regions", "Support Teams"), ("Products", "Networks"), ("Business Units", "Regions")]
    import networkx as nx
    G = nx.Graph()
    G.add_nodes_from(entities)
    G.add_edges_from(connections)
    pos = nx.spring_layout(G, seed=42)
    edge_trace = go.Scatter(x=[], y=[], line=dict(width=1, color=C["text2"]), hoverinfo="none", mode="lines")
    for e in G.edges():
        x0, y0 = pos[e[0]]; x1, y1 = pos[e[1]]
        edge_trace["x"] += (x0, x1, None); edge_trace["y"] += (y0, y1, None)
    node_trace = go.Scatter(x=[], y=[], mode="markers+text", text=[], hoverinfo="text",
        marker=dict(showscale=False, size=30, color=C["accent"], line=dict(width=2, color="white")),
        textposition="middle center", textfont=dict(size=9, color="white"))
    for node in G.nodes():
        x, y = pos[node]; node_trace["x"] += (x,); node_trace["y"] += (y,); node_trace["text"] += (node[:3],)
    fig = go.Figure(data=[edge_trace, node_trace],
        layout=go.Layout(title="Enterprise Digital Twin Graph", height=450, paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(visible=False), yaxis=dict(visible=False), showlegend=False))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"""<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:8px;">""", unsafe_allow_html=True)
    health_data = {"Customers": "🟢", "Regions": "🟡", "Products": "🟢", "Networks": "🟢", "Support Teams": "🟢", "Business Units": "🟡"}
    for entity, status in health_data.items():
        st.markdown(f"""<div class="glass" style="padding:8px;text-align:center;">
            <span>{status} {entity}</span></div>""", unsafe_allow_html=True)

def page_executive_brief():
    C = THEMES[st.session_state.theme]; maybe_compact()
    st.markdown(f"""<div style="margin-bottom:16px;"><h1 style="font-size:32px;font-weight:800;margin:0;">Executive Brief Carousel</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Auto-scrolling executive intelligence cards</p></div>""", unsafe_allow_html=True)
    cards = get_brief_cards()
    if "brief_idx" not in st.session_state: st.session_state.brief_idx = 0
    idx = st.session_state.brief_idx % len(cards)
    card = cards[idx]
    st.markdown(f"""<div class="glow-card" style="text-align:center;padding:32px;border-top:4px solid {card['color']};">
        <div style="font-size:48px;">{card["icon"]}</div>
        <div style="font-size:22px;font-weight:700;margin:8px 0;color:{card['color']};">{card["title"]}</div>
        <div style="color:{C["text2"]};font-size:14px;max-width:500px;margin:0 auto;">{card["content"]}</div>
    </div>""", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    for i, c in enumerate(cards):
        with [col1, col2, col3, col4][i]:
            if st.button(f"{c['icon']} {c['title']}", key=f"brief_{i}", use_container_width=True,
                         type="primary" if i == idx else "secondary"):
                st.session_state.brief_idx = i; st.rerun()
    col_a, col_b = st.columns([1, 1])
    with col_a:
        if st.button("← Previous", use_container_width=True):
            st.session_state.brief_idx = (idx - 1) % len(cards); st.rerun()
    with col_b:
        if st.button("Next →", use_container_width=True):
            st.session_state.brief_idx = (idx + 1) % len(cards); st.rerun()

def page_kpi_drilldown():
    C = THEMES[st.session_state.theme]; maybe_compact()
    st.markdown(f"""<div style="margin-bottom:16px;"><h1 style="font-size:32px;font-weight:800;margin:0;">KPI Drill-Down Experience</h1>
        <p style="color:{C["text2"]};font-size:14px;margin:4px 0 0;">Click any KPI → Summary → Analytics → Root Cause → Recommendations</p></div>""", unsafe_allow_html=True)
    kpis = [("Churn Rate", "26.5%", "📉", C["danger"]), ("Revenue at Risk", "$456K", "💰", C["warning"]),
            ("Avg CLV", "$1,850", "💎", C["accent"]), ("CSAT", "4.2/5", "⭐", C["success"]),
            ("NPS", "+46", "📊", C["neon"]), ("High Risk", "847", "⚠️", C["danger"])]
    cols = st.columns(3)
    for i, (name, val, icon, clr) in enumerate(kpis):
        with cols[i % 3]:
            if st.button(f"{icon} {name}: {val}", key=f"drill_{i}", use_container_width=True):
                st.session_state.drill_kpi = name
    if "drill_kpi" in st.session_state and st.session_state.drill_kpi:
        kpi = st.session_state.drill_kpi
        st.markdown(f"""<div class="glow-card" style="margin-top:12px;border-left:4px solid {C["accent"]};">
            <h3> Drilling: {kpi}</h3></div>""", unsafe_allow_html=True)
        tabs = st.tabs([" Summary", " Detailed Analytics", " Customer List", " Root Cause", " Recommendations"])
        with tabs[0]:
            st.markdown(f"""<div class="glass" style="padding:16px;">
                <h4>{kpi} — Summary</h4>
                <p style="color:{C["text2"]};">Current value shows {'elevated risk requiring immediate attention' if kpi in ['Churn Rate','Revenue at Risk','High Risk'] else 'healthy performance within targets'}.
                This metric has {'worsened' if kpi in ['Churn Rate','Revenue at Risk'] else 'improved'} by 2.3% compared to last quarter.</p></div>""", unsafe_allow_html=True)
        with tabs[1]:
            st.markdown(f"""<div class="glass" style="padding:16px;"><h4>Trend Analysis</h4></div>""", unsafe_allow_html=True)
            fig = go.Figure()
            np.random.seed(hash(kpi) % 2**31)
            vals = np.cumsum(np.random.normal(0, 0.5, 30)) + 50
            fig.add_trace(go.Scatter(y=vals, mode="lines+markers", line=dict(width=3, color=C["accent"]), fill="tozeroy", fillcolor="rgba(37,99,235,0.1)"))
            fig.update_layout(height=250, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color=C["text"])
            st.plotly_chart(fig, use_container_width=True)
        with tabs[2]:
            sample_cust = [f"C{np.random.randint(1000,8000)}" for _ in range(8)]
            st.dataframe(pd.DataFrame({"Customer": sample_cust, "Value": np.random.uniform(0, 100, 8).round(1), "Status": np.random.choice(["High","Medium","Low"],8)}), use_container_width=True)
        with tabs[3]:
            st.markdown(f"""<div class="glass" style="padding:16px;border-left:3px solid {C["danger"]};">
                <strong>Primary drivers for {kpi}:</strong><br>
                1. Contract type (Month-to-month) — 42% contribution<br>
                2. Internet service (Fiber optic) — 28% contribution<br>
                3. Tech support (No) — 18% contribution</div>""", unsafe_allow_html=True)
        with tabs[4]:
            st.markdown(f"""<div class="glass" style="padding:16px;border-left:3px solid {C["success"]};">
                <strong>Recommended actions:</strong><br>
                1. Launch targeted retention campaign for M2M customers<br>
                2. Offer tech support bundle at 50% discount<br>
                3. Create fiber optic value bundle with streaming credits</div>""", unsafe_allow_html=True)

UX_PAGE_FUNCTIONS = {
    "Voice Commands": page_voice_commands,
    "Collaboration": page_collaboration_panel,
    "Calendar": page_calendar_scheduler,
    "Onboarding Tour": page_onboarding_tour,
    "Achievements": page_achievements,
    "Digital Twin Workspace": page_digital_twin_workspace,
    "Executive Brief": page_executive_brief,
    "KPI Drill-Down": page_kpi_drilldown,
}
