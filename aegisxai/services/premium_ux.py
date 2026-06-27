"""
Premium UX Services - Data & logic for all 20 UI/UX enhancement modules
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def get_boot_sequence():
    return [
        {"label": "INITIALIZING AEGISXAI...", "status": "done"},
        {"label": "Loading Intelligence Engine...", "status": "done"},
        {"label": "Loading Risk Models...", "status": "done"},
        {"label": "Loading Executive Workspace...", "status": "done"},
        {"label": "Connecting AI Core...", "status": "active"},
        {"label": "System Ready ✓", "status": "pending"},
    ]

def get_notifications():
    return {
        "Critical Alerts": [
            {"title": "Churn risk > 90% for 47 customers", "time": "5 min ago", "icon": "🔴", "color": "error"},
            {"title": "APAC revenue drop detected", "time": "12 min ago", "icon": "🔴", "color": "error"},
        ],
        "Recommendations": [
            {"title": "Retention campaign for high-risk segment", "time": "1 hour ago", "icon": "💡", "color": "warning"},
            {"title": "Increase tech support capacity", "time": "2 hours ago", "icon": "💡", "color": "warning"},
        ],
        "System Events": [
            {"title": "Model retrained: XGBoost v4.0", "time": "3 hours ago", "icon": "ℹ️", "color": "success"},
            {"title": "Weekly backup completed", "time": "5 hours ago", "icon": "ℹ️", "color": "success"},
        ],
        "Team Mentions": [
            {"title": "@admin: Review INC-5021 escalation", "time": "20 min ago", "icon": "👤", "color": "accent"},
            {"title": "@analyst: APAC report ready", "time": "45 min ago", "icon": "👤", "color": "accent"},
        ],
    }

def get_activities(n=15):
    actions = [
        {"icon": "🚨", "text": "Customer C1024 flagged as high risk", "time": "2 min ago"},
        {"icon": "📊", "text": "Executive report generated", "time": "5 min ago"},
        {"icon": "🔔", "text": "Alert escalated to team lead", "time": "8 min ago"},
        {"icon": "📝", "text": "Case CAS-1042 updated", "time": "12 min ago"},
        {"icon": "🤖", "text": "AI Copilot: Query analyzed", "time": "15 min ago"},
        {"icon": "📈", "text": "Revenue forecast refreshed", "time": "22 min ago"},
        {"icon": "🎯", "text": "Campaign 'Loyalty Rewards' launched", "time": "30 min ago"},
        {"icon": "⚡", "text": "Model inference batch completed", "time": "35 min ago"},
        {"icon": "👤", "text": "User admin@aegisxai.io logged in", "time": "40 min ago"},
        {"icon": "🔄", "text": "Data sync: APAC region", "time": "45 min ago"},
        {"icon": "📋", "text": "Compliance audit snapshot taken", "time": "1 hour ago"},
        {"icon": "🧠", "text": "SHAP analysis run on 500 customers", "time": "1.2 hours ago"},
        {"icon": "📉", "text": "Churn rate updated: 26.5%", "time": "1.5 hours ago"},
        {"icon": "✅", "text": "System health check passed", "time": "2 hours ago"},
        {"icon": "🔒", "text": "Security audit: all clear", "time": "3 hours ago"},
    ]
    return actions[:n]

def get_world_clocks():
    import pytz
    zones = [
        ("New York", "America/New_York"),
        ("London", "Europe/London"),
        ("Singapore", "Asia/Singapore"),
        ("Tokyo", "Asia/Tokyo"),
        ("Chennai", "Asia/Kolkata"),
        ("Dubai", "Asia/Dubai"),
        ("Sydney", "Australia/Sydney"),
        ("São Paulo", "America/Sao_Paulo"),
    ]
    results = []
    for city, tz_name in zones:
        try:
            t = datetime.now(pytz.timezone(tz_name)).strftime("%H:%M")
        except:
            t = "--:--"
        results.append((city, t, tz_name))
    return results

def get_calendar_events():
    today = datetime.now().date()
    events = [
        {"date": today, "title": "Executive Review", "time": "09:00", "type": "Meeting"},
        {"date": today, "title": "Retention Campaign Review", "time": "11:00", "type": "Meeting"},
        {"date": today + timedelta(days=1), "title": "APAC Risk Assessment", "time": "10:00", "type": "Follow-up"},
        {"date": today + timedelta(days=1), "title": "Model Retraining", "time": "14:00", "type": "Task"},
        {"date": today + timedelta(days=2), "title": "Monthly Board Report", "time": "08:00", "type": "Meeting"},
        {"date": today + timedelta(days=2), "title": "Team Performance Review", "time": "15:00", "type": "Meeting"},
        {"date": today + timedelta(days=3), "title": "QBR Preparation", "time": "09:00", "type": "Task"},
        {"date": today + timedelta(days=4), "title": "Customer 360 Workshop", "time": "13:00", "type": "Workshop"},
        {"date": today + timedelta(days=7), "title": "Quarterly Business Review", "time": "09:00", "type": "Meeting"},
    ]
    return sorted(events, key=lambda x: x["date"])

def get_mini_metrics():
    return {
        "cpu": round(np.random.uniform(25, 85), 0),
        "memory": round(np.random.uniform(40, 90), 0),
        "sessions": np.random.randint(12, 89),
        "predictions_today": np.random.randint(5000, 50000),
        "open_alerts": np.random.randint(3, 25),
        "active_models": np.random.randint(2, 8),
    }

def get_achievements():
    return {
        "top_agent": {"name": "Sarah Chen", "score": 98.5, "badge": "🏆"},
        "fastest_resolver": {"name": "Mike Torres", "avg_time": "3.2 min", "badge": "⚡"},
        "highest_csat": {"name": "Emily Watson", "score": 4.9, "badge": "⭐"},
        "leaderboard": [
            ("Sarah Chen", 9850, "🥇"), ("Mike Torres", 9200, "🥈"), ("Emily Watson", 8900, "🥉"),
            ("James Park", 8450, "4th"), ("Lisa Kumar", 8100, "5th"), ("Alex Rivera", 7800, "6th"),
        ],
        "badges": [
            ("Resolution Master", "Resolved 500+ tickets", "🎖️"),
            ("Customer Champion", "Perfect CSAT for 30 days", "🏅"),
            ("Speed Demon", "Fastest resolver 2 weeks running", "⚡"),
            ("Knowledge Guru", "Top contributor to KB", "📚"),
        ],
    }

def get_onboarding_steps():
    return [
        {"step": 1, "title": "Dashboard Overview", "target": "Dashboard",
         "content": "This is your executive command center. View real-time KPIs, trends, and system health at a glance."},
        {"step": 2, "title": "Risk Queue", "target": "Risk Queue",
         "content": "Monitor high-risk customers sorted by churn probability. Take proactive retention actions."},
        {"step": 3, "title": "AI Copilot", "target": "AI Copilot",
         "content": "Ask natural language questions about your business. Example: 'Why did churn increase?'"},
        {"step": 4, "title": "XAI Diagnostic Chamber", "target": "Diagnostic Chamber",
         "content": "Understand exactly why each customer is at risk using SHAP and LIME explanations."},
        {"step": 5, "title": "Premium Suite", "target": "Executive Command",
         "content": "Explore the 22 premium dashboards for deep-dive analytics across every business dimension."},
    ]

def get_voice_commands():
    return [
        ("Show critical customers", "Navigating to Risk Queue with critical filter"),
        ("Generate executive report", "Opening Reporting Center"),
        ("Open diagnostic chamber", "Navigating to XAI Diagnostic Chamber"),
        ("What is today's churn rate?", "Querying AI Copilot for churn rate"),
        ("Show APAC region", "Navigating to Global Risk Map"),
        ("Run what-if analysis", "Opening Scenario Simulation Lab"),
    ]

def get_brief_cards():
    return [
        {"title": "Today's Risks", "icon": "🚨", "color": "#EF4444",
         "content": "47 high-risk customers detected. APAC region shows 31.5% churn rate — 5% above global average."},
        {"title": "Revenue Exposure", "icon": "💰", "color": "#F59E0B",
         "content": "$456K monthly revenue at risk. Premium segment customers >$100/mo account for 62% of exposure."},
        {"title": "Critical Customers", "icon": "👤", "color": "#8B5CF6",
         "content": "C1024, C2048, C3072 flagged for immediate retention. Combined CLV: $12,400 at risk."},
        {"title": "AI Insights", "icon": "🧠", "color": "#06B6D4",
         "content": "SHAP analysis: Contract type (0.245) and Tenure (0.182) remain top churn predictors. Model confidence: 98.6%."},
    ]

def get_model_health_status():
    return {"accuracy": round(np.random.uniform(0.78, 0.95), 3), "drift": round(np.random.uniform(0.01, 0.12), 3)}

def get_system_status():
    return {
        "health": "Healthy", "database": "Connected", "model": "Online",
        "latency_ms": 12, "users_online": np.random.randint(15, 80),
        "uptime": "23d 14h", "last_backup": (datetime.now() - timedelta(hours=6)).strftime("%H:%M"),
        "cpu": round(np.random.uniform(25, 85), 0),
        "memory": round(np.random.uniform(40, 90), 0),
        "sessions": np.random.randint(12, 89),
    }

def get_search_results(query):
    q = query.lower()
    results = []
    customers = [("C1001", "John Smith", "High Risk"), ("C1042", "Jane Doe", "Loyal"),
                 ("C2048", "Bob Wilson", "At Risk"), ("C3072", "Alice Park", "Champions")]
    reports = [("Executive Summary", "KPI Overview"), ("Churn Analysis", "Deep Dive"),
               ("Revenue Report", "Financial"), ("Model Performance", "Technical")]
    tickets = [("TKT-1001", "Billing Issue"), ("TKT-1002", "Technical Support"), ("TKT-1003", "Account Change")]
    for cid, name, seg in customers:
        if any(w in cid.lower() or w in name.lower() for w in q.split()):
            results.append(("Customer", f"{cid} — {name}", seg))
    if "report" in q or "summary" in q:
        for title, cat in reports:
            results.append(("Report", title, cat))
    if "alert" in q or "critical" in q:
        results.append(("Alert", "Critical Churn Alert — 47 customers", "Active"))
    if not results:
        results = [("Customer", f"C{np.random.randint(1000,8000)} — Search result", "Matched")]
    return results
