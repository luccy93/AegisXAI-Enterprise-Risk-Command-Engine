.PHONY: install run test lint clean data docker-up docker-down

install:
	pip install -r aegisxai/requirements.txt

run:
	streamlit run app.py --server.port 8501

data:
	python generate_large_dataset.py

test:
	cd aegisxai && pytest tests/ -v

lint:
	@if command -v ruff &> /dev/null; then \
		ruff check aegisxai/ app.py; \
	else \
		echo "ruff not installed — install with: pip install ruff"; \
	fi
	@echo "--- Syntax check ---"
	python -m py_compile app.py
	python -m py_compile aegisxai/app.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

docker-up:
	docker-compose up --build -d

docker-down:
	docker-compose down

all: install data run
