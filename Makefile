.PHONY: help install install-dev test lint format clean run

help:
	@echo "Available commands:"
	@echo "  make install       - Install dependencies"
	@echo "  make install-dev   - Install development dependencies"
	@echo "  make test          - Run tests"
	@echo "  make lint          - Run linting checks"
	@echo "  make format        - Format code with black"
	@echo "  make clean         - Clean up cache and build files"
	@echo "  make run           - Run the application"
	@echo "  make db-init       - Initialize the database"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install pytest pytest-cov flake8 black mypy

test:
	pytest tests/ --cov=src --cov-report=html --cov-report=term

lint:
	flake8 src tests
	mypy src --ignore-missing-imports

format:
	black src tests

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} +
	find . -type d -name '.pytest_cache' -exec rm -rf {} +
	find . -type d -name '.mypy_cache' -exec rm -rf {} +
	find . -type d -name 'htmlcov' -exec rm -rf {} +
	rm -f .coverage

run:
	python -m flask run --host=0.0.0.0 --port=5000

db-init:
	python -c "from src.app import create_app; app = create_app(); app.app_context().push()"
