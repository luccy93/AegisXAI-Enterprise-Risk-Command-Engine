# ⚡ AEGIS-XAI

**Enterprise-Grade Churn Prediction & Risk Command Engine**

[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0+-EC1C24?logo=xgboost&logoColor=white)](https://xgboost.readthedocs.io)
[![LightGBM](https://img.shields.io/badge/LightGBM-4.0+-7CFC00?logo=lightgbm&logoColor=black)](https://lightgbm.readthedocs.io)
[![SHAP](https://img.shields.io/badge/SHAP-0.44+-FF6F00?logo=shap&logoColor=white)](https://shap.readthedocs.io)
[![LIME](https://img.shields.io/badge/LIME-0.2+-FF69B4)](https://github.com/marcotcr/lime)
[![Optuna](https://img.shields.io/badge/Optuna-3.4+-3199FF?logo=optuna&logoColor=white)](https://optuna.org)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)](https://docker.com)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Key Features

- **🤖 AI Copilot** — Conversational churn analysis assistant
- **🔬 Diagnostic Chamber** — SHAP, LIME & Counterfactual explanations
- **📊 29 Core Dashboards** — Risk Queue, Customer 360, Campaigns, Retention & more
- **🧠 7 CXI Modules** — Sentiment, NPS, VOC, Service Quality, Loyalty, Engagement
- **📈 8 Enterprise Modules** — CLV, Anomaly Detection, Integration Hub, Pipeline, Compliance
- **⚡ Real-time Predictions** — Batch & single-customer inference
- **🔐 Role-Based Access** — Admin, Executive, Scientist, Agent
- **🎨 Glassmorphism UI** — 4 themes, Bloomberg-terminal aesthetics
- **🐳 Docker Ready** — One-command deployment
- **📋 Model Registry** — Version tracking & performance monitoring

---

## Quick Start

```bash
pip install -r aegisxai/requirements.txt
python generate_large_dataset.py
streamlit run app.py
```

Login: `admin` / `admin123`

---

## Architecture

```
├── app.py                        # Entry point
├── aegisxai/                     # Core package
│   ├── config/                   # Settings & environment
│   ├── auth/                     # Authentication & RBAC
│   ├── models/                   # ML pipeline (features, train, registry)
│   ├── services/                 # 18 service modules
│   ├── dashboards/               # 9 dashboard modules (84+ pages)
│   ├── utils/                    # Logging, caching, helpers
│   └── tests/                    # 40+ unit tests
├── scripts/                      # CLI & setup scripts
├── .streamlit/                   # Streamlit config
├── Dockerfile                    # Container build
└── docker-compose.yml            # Multi-service orchestration
```

---

## Modules

| Module | Pages | Description |
|--------|-------|-------------|
| **Core** | 29 | Risk Queue, XAI Diagnostic, Customer 360, Predictions, Retention, Campaigns |
| **CXI** | 5 | Customer Experience, Sentiment & NPS, Service Quality, VOC, Loyalty |
| **Enterprise** | 8 | CLV, Anomaly Detection, Integration Hub, Pipeline, Compliance, Reports |
| **AI** | 4 | Copilot, Forecasting, Retention Agent, Recommendation Engine |
| **Ops** | 4 | Global Ops, Digital Twin, Network Graph, Streaming Analytics |
| **Business** | 4 | Revenue Intel, Hyper-Personalization, Team Perf, Gamification |
| **Corporate** | 8 | Governance, Knowledge, Search, Experimentation, Innovation, Voice, ESG, Mobile |
| **Premium** | 22 | Executive Command, AI Command Center, Risk Intel, Scenario Lab, etc. |
| **UX** | 8 | Voice Commands, Collaboration, Calendar, Onboarding, Achievements, etc. |

---

## Tech Stack

- **Frontend**: Streamlit 1.50+, Plotly 6.8+, Custom CSS (Glassmorphism)
- **ML**: XGBoost 3.0+, LightGBM 4.6+, Optuna 4.9+, scikit-learn
- **XAI**: SHAP 0.47+, LIME 0.2+, Counterfactual Analysis
- **Backend**: Python 3.11+, Pandas, NumPy, Joblib
- **Infra**: Docker, docker-compose, GitHub Actions CI/CD

---

## Deployment

| Platform | Instructions |
|----------|-------------|
| **Streamlit Cloud** | Connect repo → select `app.py` → Deploy |
| **Docker** | `docker-compose up --build` |
| **Linux VM** | `scripts/setup.sh` |
| **Windows** | `scripts/setup.ps1` |

---

## License

MIT — see [LICENSE](aegisxai/LICENSE).
