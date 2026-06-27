"""
Autonomous Retention Agent - Creates tickets, sends offers, escalates cases
"""
import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def get_retention_levels():
    return {"Advisory": 1, "Semi-Autonomous": 2, "Fully Autonomous": 3}

def get_agent_stats(level="Advisory"):
    levels = get_retention_levels()
    lvl = levels.get(level, 1)
    actions = ["Support Ticket Created", "Retention Offer Sent", "Case Escalated", "Team Notified", "Discount Applied"]
    counts = {}
    for a in actions:
        counts[a] = int(np.random.randint(5, 30) * lvl)
    return {
        "total_actions": sum(counts.values()),
        "customers_helped": int(np.random.randint(50, 200) * lvl),
        "retention_rate": round(np.random.uniform(60, 92), 1),
        "avg_response_time": round(np.random.uniform(2, 15) / lvl, 1),
        "actions": counts,
        "level": level,
        "level_num": lvl,
    }

def get_pending_cases(n=8):
    names = ["Alice M.", "Bob K.", "Carol S.", "Dave W.", "Eve J.", "Frank L.", "Grace P.", "Hank N."]
    reasons = ["High churn risk (91%)", "Multiple support tickets", "Billing dispute", "Contract expiring",
               "Service outage complaint", "Competitor offer received", "Price sensitivity", "Poor support experience"]
    cases = []
    for i in range(n):
        cases.append({
            "id": f"CAS-{1000+i}", "customer": names[i % len(names)], "reason": reasons[i % len(reasons)],
            "status": np.random.choice(["Open", "In Progress", "Resolved", "Escalated"], p=[0.4, 0.3, 0.2, 0.1]),
            "priority": np.random.choice(["Critical", "High", "Medium", "Low"], p=[0.2, 0.4, 0.3, 0.1]),
            "created": (datetime.now() - timedelta(hours=np.random.randint(1, 72))).strftime("%Y-%m-%d %H:%M"),
        })
    return cases

def auto_resolve(case_id, level="Advisory"):
    levels = get_retention_levels()
    if levels.get(level, 1) >= 2:
        return {"success": True, "action": f"Auto-resolved {case_id}", "note": "Offer sent, customer contacted"}
    return {"success": False, "action": f"Case {case_id} queued for human review", "note": "Advisory mode - manual approval needed"}
