# Changelog

## v4.0.0 (2026-06-30)

### Added
- 84+ interactive dashboard pages across 9 modules (Core, CXI, Enterprise, AI, Ops, Biz, Corporate, Premium, UX)
- XGBoost + Optuna ML pipeline with SHAP, LIME, and counterfactual explainability
- AI Executive Copilot with rule-based NLP query engine
- 500K-row synthetic customer dataset generator
- 22 premium dashboards (Executive Command, AI Command Center, Global Risk Intel, Scenario Lab v2, etc.)
- 20 global UI/UX modules (holographic welcome screen, command palette, status bar, notification panel, quick actions dock, mini analytics widgets)
- RBAC with 4 roles (Admin, Executive, Scientist, Agent) — SHA-256 hashed auth
- 4 glassmorphism themes (Quantum Aurora, Midnight Carbon, Platinum Edge, Crimson Protocol)
- 18 backend service modules (prediction, XAI, alerts, CLV, anomaly, compliance, copilot, forecasting, retention, integration, pipeline, recommendation, premium, UX)
- 8 dashboard page function modules
- Customer Experience Intelligence layer (5 services + 5 dashboards)
- Docker + docker-compose deployment with healthchecks
- CI/CD pipeline (syntax → test → lint → docker push to ghcr.io)
- Comprehensive test suite (40+ tests across auth, services, profiler, export, premium dashboards, UX, utils)
- Data profiler and validation utilities
- CSV/JSON/HTML/Markdown export utilities
- CLI scripts (train_model, batch_predict)
- Setup scripts for Windows (PowerShell) and Linux/macOS (Bash)
- Open-source governance (CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md, issue templates)
- pyproject.toml with project metadata
- Streamlit Community Cloud deployment support (bootstrap, root config)
- .editorconfig, .pre-commit-config.yaml, Dependabot config
- AUTHORS.md contributor attribution

### Changed
- `features.py` — auto-generates dataset on cold start if CSV missing
- `aegisxai/.gitignore` — removed `!data/*.csv` negation that caused CSV re-staging
- Root `.gitignore` — expanded with additional patterns (pkl, venv, cache dirs)

### Fixed
- `TypeError: tuple indices must be integers or slices, not str` in `show_welcome_screen()` — boot sequence, notifications, and activities now return dicts instead of tuples
- `KeyError: 'cpu'` in `show_status_bar()` — added cpu/memory/sessions keys to `get_system_status()`
- `StreamlitDuplicateElementKey("nav_voc")` — renamed premium VOC key from `"voc"` to `"voc_prem"`
- DataFrame iteration in notification panel and sidebar widgets — switched to `.iterrows()` and vectorized `.sum()`
