#!/usr/bin/env bash
set -euo pipefail

echo "=== AegisXAI Setup ==="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "[FAIL] Python3 not found. Install Python 3.10+"
    exit 1
fi
echo "[OK] Python: $(python3 --version)"

# Create virtual environment
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi
source .venv/bin/activate
echo "[OK] Virtual environment activated"

# Install dependencies
echo "Installing dependencies..."
pip install -r aegisxai/requirements.txt -q
echo "[OK] Dependencies installed"

# Generate dataset
if [ ! -f "aegisxai/data/WA_Fn-UseC_-Telco-Customer-Churn.csv" ]; then
    echo "Generating synthetic dataset..."
    python3 generate_large_dataset.py
fi

# Run checks
echo "Running syntax checks..."
python3 -m py_compile app.py
python3 -m py_compile aegisxai/app.py
echo "[OK] Syntax checks passed"

echo ""
echo "=== Setup Complete ==="
echo "Run: streamlit run app.py"
