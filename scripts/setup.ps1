# AegisXAI Setup Script for Windows / PowerShell
Write-Host "=== AegisXAI Setup ===" -ForegroundColor Cyan

# Check Python
try {
    $pyVersion = python --version 2>&1
    Write-Host "[OK] Python: $pyVersion" -ForegroundColor Green
} catch {
    Write-Host "[FAIL] Python not found. Install Python 3.10+ from python.org" -ForegroundColor Red
    exit 1
}

# Create virtual environment
if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
}

# Activate
.\.venv\Scripts\Activate.ps1
Write-Host "[OK] Virtual environment activated" -ForegroundColor Green

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r aegisxai/requirements.txt -q
if ($?) {
    Write-Host "[OK] Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "[FAIL] pip install failed" -ForegroundColor Red
    exit 1
}

# Generate dataset
if (-not (Test-Path "aegisxai/data/WA_Fn-UseC_-Telco-Customer-Churn.csv")) {
    Write-Host "Generating synthetic dataset..." -ForegroundColor Yellow
    python generate_large_dataset.py
}

# Run checks
Write-Host "Running syntax checks..." -ForegroundColor Yellow
python -m py_compile app.py
python -m py_compile aegisxai/app.py
Write-Host "[OK] Syntax checks passed" -ForegroundColor Green

Write-Host ""
Write-Host "=== Setup Complete ===" -ForegroundColor Cyan
Write-Host "Run: streamlit run app.py" -ForegroundColor White
