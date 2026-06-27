# AEGIS-XAI Deployment Guide

## Prerequisites

- Python 3.11+
- Docker & Docker Compose (optional)
- Git

## Local Development

```bash
# Clone repository
git clone <repo-url>
cd aegisxai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

Access at `http://localhost:8501`

## Docker Deployment

```bash
# Build image
docker build -t aegisxai:latest .

# Run container
docker run -d -p 8501:8501 --name aegisxai aegisxai:latest

# With docker-compose (full stack)
docker-compose up --build
```

## Streamlit Community Cloud

1. Push repository to GitHub
2. Log in to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Select repository, branch, and set `app.py` as entry point
5. Deploy

## Cloud VM Deployment (AWS EC2 / Azure VM / DigitalOcean)

```bash
# SSH into VM
ssh user@your-vm-ip

# Install Docker
curl -fsSL https://get.docker.com | sh

# Run container
docker run -d -p 8501:8501 \
  --restart unless-stopped \
  -e APP_ENV=production \
  ghcr.io/your-org/aegisxai:latest
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_ENV` | `development` | Environment mode |
| `DB_HOST` | `localhost` | Database host |
| `DB_PORT` | `5432` | Database port |
| `DB_NAME` | `aegisxai` | Database name |
| `DB_USER` | `admin` | Database user |
| `DB_PASSWORD` | `changeme` | Database password |
| `SECRET_KEY` | *(see .env)* | JWT signing key |
| `MODEL_VERSION` | `v4.0.0` | Active model version |
| `CSV_PATH` | `data/WA_Fn-UseC_-Telco-Customer-Churn.csv` | Data file path |

## Production Checklist

- [ ] Set strong `SECRET_KEY` in `.env`
- [ ] Change all default passwords
- [ ] Enable PostgreSQL (disable SQLite)
- [ ] Set `APP_ENV=production`
- [ ] Configure reverse proxy (Nginx/Caddy)
- [ ] Enable HTTPS with Let's Encrypt
- [ ] Set up log rotation
- [ ] Configure monitoring (Prometheus/Grafana)
- [ ] Run tests: `pytest tests/`
- [ ] Build and push Docker image to registry

## Troubleshooting

**App won't start:**
```bash
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
```

**Missing dependencies:**
```bash
pip install -r requirements.txt --upgrade
```

**Port already in use:**
```bash
# Change port in .env
STREAMLIT_SERVER_PORT=8502
```

**Database connection error:**
```bash
# Ensure PostgreSQL is running
docker-compose up postgres -d
```
