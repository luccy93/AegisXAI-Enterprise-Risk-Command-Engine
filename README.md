# ⚡ AegisXAI — Enterprise Risk Command Engine

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://aegisxai-enterprise-risk-command-engine-aqfb3dpxmxp3rzp5pswydm.streamlit.app)

**AegisXAI** is a production-grade, enterprise churn prediction and risk mitigation platform with Bloomberg-terminal aesthetics, 84+ interactive dashboards, and a fully modular 60+ file Python architecture.

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r aegisxai/requirements.txt

# 2. Generate the 500K-row dataset
python generate_large_dataset.py

# 3. Launch the platform
streamlit run app.py
```

Open **http://localhost:8501** — login with `admin / admin123`.

---

## 📊 Platform Overview

| Module | Pages | Description |
|--------|-------|-------------|
| **Core** | 29 | Original dashboards — Risk Queue, XAI Diagnostic, Predictions, Customer 360, Retention, Campaigns, etc. |
| **Customer Intelligence (CXI)** | 5 | Customer Experience, Sentiment & NPS, Service Quality, VOC Analytics, Loyalty & Engagement |
| **Enterprise** | 8 | CLV Dashboard, Anomaly Detection, Integration Hub, Pipeline Monitor, Compliance, Executive Reports, Alert Webhooks, Model Explainability |
| **AI Features** | 4 | AI Executive Copilot, Business Forecasting, Retention Agent, Recommendation Engine |
| **Operations** | 4 | Global Operations Center, Digital Twin, Network Graph, Streaming Analytics |
| **Business** | 4 | Revenue Intelligence, Hyper-Personalization, Team Performance, Gamification |
| **Corporate** | 8 | Governance, Knowledge Management, Advanced Search, Experimentation Lab, Innovation Lab, Voice Analytics, ESG Dashboard, Mobile Companion |
| **Premium Dashboards** | 22 | Executive Command (holographic KPI), AI Command Center, Global Risk Intel, Revenue Intel, CX Intel, Segmentation Premium, Journey Premium, XAI Diagnostic v2, Scenario Lab v2, Live Ops, Alerts, Incidents, Model Intel, Drift Detection, Customer 360 Premium, Team Perf, Retention Campaigns, Security & Governance, Reporting Center, Premium Widgets |
| **UX Experience** | 8 | Voice Commands, Collaboration Panel, Calendar Scheduler, Onboarding Tour, Achievements, Digital Twin Workspace, Executive Brief Carousel, KPI Drill-Down |
| **Global UI** | 10 | Holographic Welcome Screen, Status Bar, Notification Panel, Quick Actions Dock, Command Palette (Ctrl+K), Mini Analytics Widgets, Activity Feed, Enterprise Header, Universal Search |

**Total: 84+ unique page functions** across 8 dashboard modules + global UI layer.

---

## 🔐 Roles & Access

| Role | Credentials | Access |
|------|-------------|--------|
| Admin | `admin` / `admin123` | Full access, all pages, all features |
| Executive | `exec` / `admin123` | Premium dashboards + strategic views |
| Data Scientist | `sci` / `sci123` | XAI diagnostic, model intel, drift |
| Agent | `agent` / `agent123` | Risk queue, alerts, cases |

---

## 🏛 Architecture

```
├── app.py                        # Main entry point — login, CSS, routing, global UI
├── aegisxai/
│   ├── config/settings.py        # Environment config
│   ├── auth/auth.py              # SHA-256 hashed authentication + RBAC
│   ├── models/
│   │   ├── features.py           # Data loading + engineering
│   │   ├── train.py              # XGBoost + Optuna training pipeline
│   │   └── registry.py           # Model version registry
│   ├── services/                 # 18 service modules
│   │   ├── prediction_service.py
│   │   ├── xai_service.py        # SHAP, LIME, counterfactual explanations
│   │   ├── alert_service.py
│   │   ├── copilot_service.py    # AI Executive Copilot NLP engine
│   │   ├── forecasting_service.py
│   │   ├── retention_agent.py    # 3-level autonomous retention agent
│   │   ├── premium_services.py   # Data for 22 premium dashboards
│   │   ├── premium_ux.py         # Data for 20 UI/UX modules
│   │   └── ... (10 more)
│   ├── dashboards/               # 8 dashboard modules
│   │   ├── pages.py              # 29 original page functions
│   │   ├── cx_pages.py           # 5 CX pages
│   │   ├── enterprise_pages.py   # 8 enterprise pages
│   │   ├── ai_pages.py           # 4 AI pages
│   │   ├── ops_pages.py          # 4 Ops pages
│   │   ├── biz_pages.py          # 4 Biz pages
│   │   ├── corp_pages.py         # 8 Corporate pages
│   │   ├── premium_dashboards.py # 22 premium dashboards
│   │   └── ux_pages.py           # 8 UX pages
│   ├── utils/                    # Logging, caching, helpers
│   └── tests/                    # Test suite
├── .streamlit/config.toml        # Streamlit server config
├── Dockerfile                    # Container deployment
├── docker-compose.yml            # Multi-service orchestration
└── generate_large_dataset.py     # Synthetic 500K-row dataset generator
```

---

## 🎨 Design System

- **Glassmorphism** — backdrop-filter blur, translucent panels
- **Neon glow** — animated borders, gradient text, conic gradient overlays
- **Holographic** — `@keyframes holographicRotate`, conic-gradient sweep
- **Bloomberg-inspired** — dark theme, monospace data, status bars
- **4 themes** — Quantum Aurora (default), Midnight Carbon, Platinum Edge, Crimson Protocol

---

## 🧠 ML Pipeline

- **Algorithm**: XGBoost with Optuna hyperparameter tuning
- **Features**: 21 columns (tenure, contract type, internet service, payment method, etc.)
- **Explainability**: SHAP waterfall/summary/force plots, LIME explanations, counterfactual what-if analysis
- **Monitoring**: Drift detection, model registry with versioning, accuracy tracking
- **Data**: 500,000 synthetic customers (~45% churn rate, configurable)

---

## 🐳 Docker Deployment

```bash
docker-compose up --build
```

Exposed on port 8501.

---

## 🧪 Testing

```bash
cd aegisxai
pytest tests/ -v
```

---

## ☁️ Deploy on Streamlit Community Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) and click **New app**
3. Select your repo, branch (`master`), and main file (`app.py`)
4. Click **Deploy**

The app auto-generates a 50K-row dataset on first cold start (the full 500K can be regenerated via `python generate_large_dataset.py`).

**Optional secrets** (set via Streamlit Cloud dashboard → Advanced settings):
- `CSV_PATH` — custom dataset path
- `LOG_LEVEL` — `DEBUG`, `INFO`, `WARNING`

---

## 📄 License

MIT — see `aegisxai/LICENSE`.
