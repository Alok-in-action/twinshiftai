.PHONY: install dev test lint typecheck format

install:
	pip install -e .[dev]

dev:
	uvicorn backend.app.main:app --reload

test:
	pytest tests/

lint:
	ruff check .

typecheck:
	mypy backend/app tests/

format:
	ruff format .
