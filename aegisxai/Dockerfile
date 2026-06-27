FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY aegisxai/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY aegisxai/ aegisxai/
COPY app.py .
COPY generate_large_dataset.py .

RUN python generate_large_dataset.py && python -m py_compile app.py

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python aegisxai/healthcheck.py

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
