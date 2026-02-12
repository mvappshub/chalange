.PHONY: install lint test run

install:
	python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

lint:
	ruff check .
	mypy app scripts || true

test:
	PYTHONPATH=. pytest --cov=app --cov-report=term-missing

run:
	uvicorn app.main:app --reload
