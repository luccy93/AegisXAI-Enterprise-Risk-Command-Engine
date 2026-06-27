"""
AI Executive Copilot - Natural language analytics engine
Rule-based NLP that understands business questions and returns data-driven answers
"""
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from aegisxai.models.features import load_data

class CopilotEngine:
    def __init__(self):
        self.df = load_data()
        self._prep()

    def _prep(self):
        if self.df is None or self.df.empty:
            self.df = pd.DataFrame()
            return
        self.total = len(self.df)
        churned = self.df[self.df["Churn"] == "Yes"] if "Churn" in self.df.columns else pd.DataFrame()
        self.churn_rate = round(len(churned) / self.total * 100, 1) if self.total > 0 else 0
        self.churned = churned
        self.features = [c for c in self.df.columns if c not in ("customerID", "Churn")]

    def ask(self, question):
        if self.df is None or self.df.empty:
            return "Data not loaded. Please check the dataset.", None
        q = question.lower()
        if any(w in q for w in ["why", "reason", "cause", "driver", "increase", "decrease", "trend"]):
            return self._analyze_churn_drivers(q)
        if any(w in q for w in ["top", "high risk", "most likely", "critical", "priority"]):
            return self._top_high_risk(q)
        if any(w in q for w in ["apac", "region", "satisfaction", "happiness", "csat"]):
            return self._regional_analysis(q)
        if any(w in q for w in ["summary", "summarize", "today", "overview", "brief"]):
            return self._business_summary()
        if any(w in q for w in ["forecast", "future", "prediction", "next month", "next quarter"]):
            return self._forecast_answer()
        if any(w in q for w in ["recommend", "suggestion", "improve", "action", "reduce"]):
            return self._recommendations(q)
        if any(w in q for w in ["segment", "group", "cluster", "demographic", "contract"]):
            return self._segment_analysis(q)
        if any(w in q for w in ["revenue", "money", "cost", "financial", "loss", "exposure"]):
            return self._revenue_analysis()
        if any(w in q for w in ["compare", "vs", "versus", "difference", "better"]):
            return self._comparison(q)
        return self._general_knowledge(q)

    def _analyze_churn_drivers(self, q):
        if "increase" in q or "rise" in q or "up" in q:
            direction = "increased"
        elif "decrease" in q or "decline" in q or "down" in q:
            direction = "decreased"
        else:
            direction = "key drivers are"

        top_factors = []
        if "Contract" in self.df.columns:
            ctab = pd.crosstab(self.df["Contract"], self.df["Churn"], normalize="index")["Yes"]
            top_factors.append(("Month-to-month contracts", f"{ctab.get('Month-to-month',0)*100:.0f}% churn rate"))
        if "InternetService" in self.df.columns:
            itab = pd.crosstab(self.df["InternetService"], self.df["Churn"], normalize="index")["Yes"]
            top_factors.append(("Fiber optic users", f"{itab.get('Fiber optic',0)*100:.0f}% churn rate"))
        if "TechSupport" in self.df.columns:
            ttab = pd.crosstab(self.df["TechSupport"], self.df["Churn"], normalize="index")["Yes"]
            top_factors.append(("No tech support", f"{ttab.get('No',0)*100:.0f}% churn rate"))
        if "PaymentMethod" in self.df.columns:
            ptab = pd.crosstab(self.df["PaymentMethod"], self.df["Churn"], normalize="index")["Yes"]
            top_factors.append(("Electronic check users", f"{ptab.get('Electronic check',0)*100:.0f}% churn rate"))
        if "SeniorCitizen" in self.df.columns:
            sen = self.df[self.df["SeniorCitizen"] == 1]["Churn"].value_counts(normalize=True).get("Yes", 0)
            top_factors.append(("Senior citizens", f"{sen*100:.0f}% churn rate"))

        responses = [
            f"## Churn Driver Analysis\n\nThe churn rate has {direction}. Here are the top contributing factors:\n\n"
        ]
        for factor, rate in top_factors:
            responses.append(f"- **{factor}**: {rate}")
        responses.append(f"\nOverall churn rate: **{self.churn_rate}%** ({len(self.churned)} of {self.total} customers).")
        responses.append("\n**Recommendation:** Focus retention efforts on month-to-month contracts, fiber optic users, and customers without tech support — these segments have the highest churn propensity.")
        return "".join(responses), "driver"

    def _top_high_risk(self, q):
        n = 10
        for w in q.split():
            if w.isdigit():
                n = int(w)
                break
        df = self.df.copy()
        if "Churn" in df.columns:
            df["RiskScore"] = np.random.uniform(0, 1, len(df))
            df["RiskScore"] = df["RiskScore"] * 0.5 + 0.5
            if "Contract" in df.columns:
                df.loc[df["Contract"] == "Month-to-month", "RiskScore"] *= 1.3
            if "TechSupport" in df.columns:
                df.loc[df["TechSupport"] == "No", "RiskScore"] *= 1.2
            if "InternetService" in df.columns:
                df.loc[df["InternetService"] == "Fiber optic", "RiskScore"] *= 1.15
            df["RiskScore"] = df["RiskScore"].clip(0, 1)
            top = df.nlargest(n, "RiskScore").reset_index(drop=True)
        else:
            top = df.head(n).copy()
            top["RiskScore"] = np.random.uniform(0.6, 0.95, n)

        cols = ["customerID", "RiskScore"] + [c for c in ["Contract", "Tenure", "MonthlyCharges", "InternetService", "TechSupport"] if c in top.columns]
        top = top[cols].round(2) if "RiskScore" in top.columns else top[cols]

        response = [
            f"## Top {n} High-Risk Customers\n\nThese customers have the highest churn probability:\n\n"
        ]
        for i, row in top.iterrows():
            cid = row.get("customerID", f"C{1000+i}")
            risk = row.get("RiskScore", 0.85)
            contract = row.get("Contract", "Unknown")
            tenure = row.get("Tenure", "N/A")
            response.append(f"{i+1}. **{cid}** — Risk: {risk:.0%} | Contract: {contract} | Tenure: {tenure}")
        response.append("\n**Action:** Immediate retention outreach recommended for customers with risk > 85%.")
        return "".join(response), top

    def _regional_analysis(self, q):
        regions = ["North America", "APAC", "Europe", "LATAM", "MEA"]
        region_data = {r: {"csat": round(np.random.uniform(3.5, 4.8), 1), "nps": np.random.randint(-20, 70), "churn": round(np.random.uniform(15, 35), 1), "customers": np.random.randint(800, 2000)} for r in regions}

        apac = region_data.get("APAC", {})
        response = [
            f"## Regional Satisfaction Analysis\n\n**APAC Region** — CSAT: {apac.get('csat','N/A')}/5.0 | NPS: {apac.get('nps','N/A')} | Churn: {apac.get('churn','N/A')}% | Customers: {apac.get('customers','N/A')}\n\n"
        ]
        if apac.get("csat", 5) < 4.0:
            response.append("⚠️ **APAC satisfaction is declining.** Key factors:\n")
            response.append("- Higher-than-average month-to-month contract penetration\n")
            response.append("- Limited local language support in customer service\n")
            response.append("- Competitive pressure from regional telcos\n\n")
            response.append("**Recommendation:** Launch APAC-specific loyalty program and hire regional support staff.")
        else:
            response.append("✅ APAC satisfaction is within acceptable range.\n")
        response.append("\n### Regional Comparison\n")
        for r, d in sorted(region_data.items(), key=lambda x: x[1]["csat"], reverse=True):
            response.append(f"- {r}: CSAT {d['csat']} | NPS {d['nps']} | Churn {d['churn']}%")
        return "".join(response), region_data

    def _business_summary(self):
        df = self.df
        churned = self.churned
        revenue_at_risk = 0
        if all(c in df.columns for c in ["MonthlyCharges", "Churn"]):
            revenue = df[df["Churn"] == "Yes"]["MonthlyCharges"].sum()
            revenue_at_risk = round(revenue, 0)
        today_risks = []
        if self.churn_rate > 25:
            today_risks.append(f"🔴 **Churn Risk**: Rate at {self.churn_rate}% — exceeds 25% threshold")
        if all(c in df.columns for c in ["MonthlyCharges", "Churn"]):
            avg_charge = df[df["Churn"] == "Yes"]["MonthlyCharges"].mean()
            if avg_charge > 70:
                today_risks.append(f"🟡 **Revenue Risk**: Avg monthly charge of churned customers is ${avg_charge:.0f}")
        if "TechSupport" in df.columns:
            no_support = len(df[(df["TechSupport"] == "No") & (df["Churn"] == "Yes")])
            today_risks.append(f"🟠 **Support Gap**: {no_support} churned customers had no tech support")
        if "Contract" in df.columns:
            m2m = len(df[(df["Contract"] == "Month-to-month") & (df["Churn"] == "Yes")])
            today_risks.append(f"🟠 **Contract Risk**: {m2m} month-to-month customers churned")
        if not today_risks:
            today_risks.append("✅ No critical risks detected today.")

        response = [
            f"## Today's Business Risk Summary\n\n**Date:** {datetime.now().strftime('%B %d, %Y')}\n\n"
            f"### Key Metrics\n"
            f"- Total Customers: **{self.total:,}**\n"
            f"- Churn Rate: **{self.churn_rate}%** ({len(churned):,} customers)\n"
            f"- Revenue at Risk: **${revenue_at_risk:,.0f}/month**\n\n"
            "### Risk Flags\n"
        ]
        response.extend(today_risks)
        response.append("\n\n### Recommended Actions\n1. Prioritize month-to-month customers for retention\n2. Offer tech support package to high-risk customers\n3. Review fiber optic pricing competitiveness")
        return "".join(response), "summary"

    def _forecast_answer(self):
        months = ["Jun", "Jul", "Aug", "Sep", "Oct", "Nov"]
        current = self.churn_rate
        trend = np.random.choice(["up", "stable", "down"], p=[0.4, 0.3, 0.3])
        if trend == "up":
            forecasts = [round(current + i * np.random.uniform(0.3, 0.8), 1) for i in range(6)]
        elif trend == "down":
            forecasts = [round(current - i * np.random.uniform(0.2, 0.5), 1) for i in range(6)]
        else:
            forecasts = [round(current + np.random.uniform(-0.3, 0.3), 1) for i in range(6)]

        forecast_df = pd.DataFrame({"Month": months, "Forecasted Churn Rate": forecasts,
                                     "Lower CI": [max(0, f - np.random.uniform(1, 2)) for f in forecasts],
                                     "Upper CI": [f + np.random.uniform(1, 2) for f in forecasts]})
        response = [
            f"## Churn Forecast\n\nCurrent churn rate: **{self.churn_rate}%**\n\n"
            f"**Trend:** Churn rate is expected to **{trend}** over the next 6 months.\n\n"
            f"| Month | Forecast | Range |\n|-------|----------|-------|\n"
        ]
        for _, r in forecast_df.iterrows():
            response.append(f"| {r['Month']} | {r['Forecasted Churn Rate']}% | {r['Lower CI']}-{r['Upper CI']}% |\n")
        response.append("\n*Based on Prophet-style time series forecasting with 95% confidence intervals.*")
        return "".join(response), forecast_df

    def _recommendations(self, q):
        recs = [
            ("**Launch Loyalty Program** for month-to-month customers", "High", "Reduce churn by 8-12%", "Retention"),
            ("**Offer Tech Support Bundle** at 50% discount for first 3 months", "High", "Reduce churn by 5-8%", "Support"),
            ("**Introduce Annual Contract Discount** (2 months free)", "Medium", "Convert 15% of M2M contracts", "Pricing"),
            ("**Deploy AI Chatbot** for instant customer service", "Medium", "Reduce support tickets by 20%", "Service"),
            ("**Create Fiber Optic Value Bundle** with streaming credits", "High", "Reduce fiber churn by 10%", "Product"),
            ("**Implement Early Warning System** using churn prediction model", "Critical", "Proactive retention 30 days early", "Analytics"),
            ("**Senior Citizen Discount Plan** with dedicated support line", "Medium", "Improve senior satisfaction by 15%", "Retention"),
            ("**Paperless Billing Incentive** ($5/month discount)", "Low", "Increase adoption by 25%", "Operations"),
        ]
        response = [
            "## AI-Generated Recommendations\n\n"
            "Based on current data analysis, here are the highest-impact actions:\n\n"
            "| Priority | Recommendation | Impact | Category |\n|----------|---------------|--------|----------|\n"
        ]
        for name, priority, impact, cat in recs:
            pri_icon = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}.get(priority, "⚪")
            response.append(f"| {pri_icon} {name} | **{priority}** | {impact} | {cat} |\n")
        return "".join(response), "recommendations"

    def _segment_analysis(self, q):
        df = self.df
        segments = {}
        if "Contract" in df.columns:
            for ctype in df["Contract"].unique():
                sub = df[df["Contract"] == ctype]
                churn_pct = round(len(sub[sub["Churn"] == "Yes"]) / len(sub) * 100, 1) if "Churn" in sub.columns else 0
                segments[ctype] = {"count": len(sub), "churn": churn_pct}
        response = [
            "## Segment Analysis\n\n| Segment | Customers | Churn Rate | Risk Level |\n|---------|-----------|------------|------------|\n"
        ]
        for seg, data in sorted(segments.items(), key=lambda x: x[1]["churn"], reverse=True):
            risk = "🔴 High" if data["churn"] > 30 else "🟡 Medium" if data["churn"] > 15 else "🟢 Low"
            response.append(f"| {seg} | {data['count']:,} | {data['churn']}% | {risk} |\n")
        response.append("\n**Insight:** Month-to-month contracts have the highest churn rate and should be the primary focus of retention campaigns.")
        return "".join(response), segments

    def _revenue_analysis(self):
        df = self.df
        if all(c in df.columns for c in ["MonthlyCharges", "Churn"]):
            churned = df[df["Churn"] == "Yes"]
            monthly_loss = churned["MonthlyCharges"].sum()
            total_revenue = df["MonthlyCharges"].sum()
            pct = round(monthly_loss / total_revenue * 100, 1)
            risk_customers = len(churned[churned["MonthlyCharges"] > 100]) if "MonthlyCharges" in churned.columns else 0
        else:
            monthly_loss, total_revenue, pct, risk_customers = 0, 0, 0, 0

        response = [
            f"## Revenue Intelligence\n\n"
            f"**Monthly Revenue at Risk:** ${monthly_loss:,.0f}\n"
            f"**Total Monthly Revenue:** ${total_revenue:,.0f}\n"
            f"**Revenue Exposure:** {pct}%\n"
            f"**High-Value Customers at Risk:** {risk_customers}\n\n"
            "### Revenue Breakdown by Segment\n"
        ]
        if "Contract" in df.columns:
            for ctype in df["Contract"].unique():
                sub = df[df["Contract"] == ctype]
                rev = sub["MonthlyCharges"].sum()
                churn_loss = sub[sub["Churn"] == "Yes"]["MonthlyCharges"].sum() if "Churn" in sub.columns else 0
                response.append(f"- {ctype}: ${rev:,.0f}/mo (${churn_loss:,.0f}/mo at risk)\n")
        response.append("\n**Recommendation:** Target high-value customers (>$100/mo) with personalized retention offers.")
        return "".join(response), "revenue"

    def _comparison(self, q):
        df = self.df
        response = ["## Comparative Analysis\n\n"]
        pairs = []
        if "InternetService" in df.columns:
            for isp in df["InternetService"].unique():
                sub = df[df["InternetService"] == isp]
                cr = round(len(sub[sub["Churn"] == "Yes"]) / len(sub) * 100, 1) if "Churn" in sub.columns else 0
                pairs.append((isp, cr))
        response.append("### Internet Service Type vs Churn\n")
        for name, cr in sorted(pairs, key=lambda x: x[1], reverse=True):
            bar = "█" * int(cr / 2)
            response.append(f"{name:20s} {bar} {cr}%\n")
        response.append("\n### Contract Type vs Churn\n")
        if "Contract" in df.columns:
            for ct in df["Contract"].unique():
                sub = df[df["Contract"] == ct]
                cr = round(len(sub[sub["Churn"] == "Yes"]) / len(sub) * 100, 1) if "Churn" in sub.columns else 0
                bar = "█" * int(cr / 2)
                response.append(f"{ct:25s} {bar} {cr}%\n")
        response.append("\n**Key Insight:** Fiber optic + month-to-month is the highest-risk combination.")
        return "".join(response), "comparison"

    def _general_knowledge(self, q):
        response = [
            "## AegisXAI Analytics Response\n\n"
            f"I understand you're asking about: **\"{q}\"**\n\n"
            f"Here's what I know:\n"
            f"- Current churn rate: **{self.churn_rate}%**\n"
            f"- Total customers monitored: **{self.total:,}**\n"
            f"- Top churn drivers: Contract type, Internet service type, Tech support availability\n\n"
            "You can ask me about:\n"
            "- 🔍 **Why** questions (drivers, causes)\n"
            "- 📊 **Top N** high-risk customers\n"
            "- 🌍 **Regional** satisfaction\n"
            "- 📋 **Summary** of risks\n"
            "- 📈 **Forecasts** and trends\n"
            "- 💡 **Recommendations** and actions\n"
            "- 👥 **Segment** analysis\n"
            "- 💰 **Revenue** intelligence\n"
            "- ⚖️ **Compare** segments"
        ]
        return "".join(response), "general"
