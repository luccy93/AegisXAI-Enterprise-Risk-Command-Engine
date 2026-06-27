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
- **📊 Real-time Monitoring** — Live event stream, drift detection, system health
- **🎯 Risk Queue** — ML-scored customer risk prioritization
- **🧠 Customer Segmentation** — KMeans clustering with PCA visualization
- **📈 Forecasting** — 6-month churn & revenue projections
- **🔄 A/B Model Comparison** — XGBoost vs LightGBM side-by-side
- **🔐 Role-Based Access** — Admin, Analyst, Manager, Viewer
- **🎨 5 Themes** — Quantum Aurora, Cyber Command, Neo Corporate, Dark Glass, Holographic Blue
- **📋 29 Dashboards** — Comprehensive enterprise coverage

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | Streamlit 1.28+ |
| ML Models | XGBoost, LightGBM |
| Hyperparameter Tuning | Optuna (TPE Sampler) |
| Explainability | SHAP (TreeExplainer), LIME |
| Data Processing | Pandas, NumPy, Scikit-learn |
| Visualization | Plotly Express, Plotly Graph Objects |
| Security | SHA-256, Role-Based Access Control |
| Containerization | Docker |
| CI/CD | GitHub Actions |

## Quick Start

```bash
git clone <repo-url>
cd aegisxai
pip install -r requirements.txt
streamlit run app.py
```

## Docker

```bash
docker build -t aegisxai .
docker run -p 8501:8501 aegisxai
```

## Authentication

| Role | Username | Password | Access Level |
|------|----------|----------|-------------|
| Admin | admin | admin123 | Full system access |
| Analyst | analyst | analyst123 | Analytics & reports |
| Manager | manager | manager123 | Team oversight |
| Viewer | viewer | viewer123 | Read-only access |

## Architecture

```
aegisxai/
├── app.py                 # Main entry point
├── auth/                  # Authentication module
├── config/                # Configuration & settings
├── dashboards/            # Page modules & components
├── models/                # ML feature engineering & registry
├── services/              # Prediction, alerts, recommendations
├── utils/                 # Logging, helpers, audit
├── tests/                 # Pytest test suite
├── data/                  # Dataset storage
├── models/                # Serialized model artifacts
├── reports/               # Generated reports
├── assets/                # Static assets
├── .streamlit/            # Streamlit configuration
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Screenshots

> Screenshots will be added in a future release.

## License

MIT License — see [LICENSE](LICENSE) for details.
