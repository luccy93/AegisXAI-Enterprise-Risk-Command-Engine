# AEGIS-XAI Architecture

## Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Frontend (app.py)              │
│  ┌─────────┐ ┌──────────┐ ┌─────────┐ ┌───────────────┐  │
│  │  Login  │ │  Header  │ │ Sidebar │ │ 29 Dashboard  │  │
│  │  (MFA)  │ │  (RBAC)  │ │ (Nav +  │ │    Pages      │  │
│  │         │ │          │ │ Shortcut)│ │               │  │
│  └─────────┘ └──────────┘ └─────────┘ └───────────────┘  │
│                          │                                   │
└──────────────────────────┼──────────────────────────────────┘
                           │
┌──────────────────────────┼──────────────────────────────────┐
│           aegisxai/      │    Core Package                   │
│  ┌──────────┐ ┌─────────┐ ┌──────────┐ ┌───────────────┐  │
│  │ config/  │ │ auth/   │ │ models/  │ │ services/     │  │
│  │ settings │ │ RBAC    │ │ features │ │ prediction    │  │
│  │ .env     │ │ users   │ │ train    │ │ XAI (SHAP/    │  │
│  │          │ │ roles   │ │ registry │ │ LIME)         │  │
│  └──────────┘ └─────────┘ └──────────┘ │ alerts        │  │
│  ┌──────────┐ ┌─────────┐              │ recommend     │  │
│  │ utils/   │ │ assets/ │              └───────────────┘  │
│  │ helpers  │ │ static  │                                  │
│  │ logging  │ │ files   │  ┌──────────┐ ┌───────────────┐  │
│  │ caching  │ │         │  │ data/    │ │ dashboards/   │  │
│  └──────────┘ └─────────┘  │ Telco    │ │ components    │  │
│                            │ CSV      │ │ pages (29)    │  │
│                            └──────────┘ └───────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           │
┌──────────────────────────┼──────────────────────────────────┐
│         Backend API (backend/)  FastAPI                     │
│  ┌──────────┐ ┌─────────┐ ┌──────────┐ ┌───────────────┐  │
│  │ api/     │ │ services│ │ database/│ │ xai/           │  │
│  │ 12       │ │ 9       │ │ 18       │ │ SHAP/LIME/     │  │
│  │ routers  │ │ modules │ │ tables   │ │ drift          │  │
│  └──────────┘ └─────────┘ └──────────┘ └───────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

1. **User authenticates** via login form → session state stores role + permissions
2. **Navigation** via sidebar or keyboard shortcuts (Ctrl+D, Ctrl+R, etc.)
3. **Dashboard pages** load data from CSV cache (`@st.cache_data`) or ML models
4. **ML Pipeline**: Feature engineering → XGBoost/LightGBM → SHAP/LIME explanations
5. **Export**: Reports generated as PDF, Excel, CSV via openpyxl/reportlab

## Component Architecture

### Frontend (Streamlit)
- `app.py` - Entry point, routing, CSS, login, header, sidebar
- `dashboards/pages.py` - 29 individual page functions
- `dashboards/components.py` - 20 reusable UI components
- `auth/auth.py` - User authentication and RBAC
- `utils/` - Logging, caching, helper functions

### ML Layer
- `models/features.py` - Feature engineering pipeline
- `models/train.py` - XGBoost (Optuna) + LightGBM training
- `services/xai_service.py` - SHAP, LIME, counterfactual explanations
- `services/prediction_service.py` - KMeans clustering, churn probability

### Backend (FastAPI, optional)
- 12 API routers (auth, customers, predict, explain, alerts, etc.)
- 18 SQLAlchemy database tables
- SQLite (dev) / PostgreSQL (prod)

## Key Design Decisions

- **Single-page architecture**: Streamlit session state manages all UI state
- **Modular but unified**: All page functions share the same theme/CSS system
- **Caching**: `@st.cache_data` for data, `@st.cache_resource` for models
- **No external API deps**: Simulated LLM copilot, no OpenAI key required
- **Glassmorphism UI**: backdrop-filter blur, neon glow, GPU-accelerated animations
