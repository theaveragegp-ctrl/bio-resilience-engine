.PHONY: help install test lint format clean docker-build docker-up docker-down

help:
	@echo "Bio-Resilience Engine - Development Commands"
	@echo ""
	@echo "install        Install dependencies"
	@echo "test           Run test suite"
	@echo "test-fast      Run tests excluding slow tests"
	@echo "lint           Run linters (ruff, mypy)"
	@echo "format         Format code with black"
	@echo "clean          Clean build artifacts"
	@echo "docker-build   Build Docker images"
	@echo "docker-up      Start Docker stack"
	@echo "docker-down    Stop Docker stack"
	@echo "edge-run       Run edge node locally"
	@echo "api-run        Run API server locally"

install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pre-commit install

test:
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term

test-fast:
	pytest tests/ -v -m "not slow" --cov=src

lint:
	ruff check src/ tests/
	mypy src/

format:
	black src/ tests/
	ruff check --fix src/ tests/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .coverage htmlcov/ .pytest_cache/

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

edge-run:
	python -m src.edge_node.main \
		--model models/yolov8n-pose.pt \
		--source 0 \
		--mqtt-broker localhost \
		--device cuda

api-run:
	uvicorn src.cloud_fusion.main:app --reload --host 0.0.0.0 --port 8000

migration-create:
	alembic revision --autogenerate -m "$(msg)"

migration-run:
	alembic upgrade head

docs-serve:
	mkdocs serve

docs-build:
	mkdocs build
