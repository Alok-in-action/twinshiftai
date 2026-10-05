# AGENTS.md

## 1. Architecture Rules
- Use a Modular Monolith architecture.
- Keep Physics, ML, Optimization, API, and DB separate in code.
- Do not add Kubernetes, Kafka, or microservices.
- Ensure FastAPI routes only orchestrate; logic goes into service/physics layers.

## 2. Coding Standards
- Python 3.12.
- Pre-commit hooks for Ruff, Black, and Mypy.
- Enforce type hints on all functions.
- Write pure mathematical functions in `backend/app/physics` that are independent of Pydantic and SQLAlchemy.

## 3. Units
- Strictly use `pint` for all boundary conversions (API in/out).
- Core equations must be in SI units internally.
- Preserve and store the original units in the raw ingestion database.

## 4. Safety Constraints (Non-Negotiable)
- **NO DIRECT CONTROL**: The application is strictly human-in-the-loop advisory.
- **NO HARDCODING**: Field constraints, viscosity parameters, and equipment specifications must come from configuration files or database schemas.
- **NO EXTRAPOLATION**: Refuse optimization if inputs fall outside the validated bounds of fluid properties or operational limits.
- An independent feasibility check function must validate the optimizer's output before returning to the UI.

## 5. Verification Commands
- Unit Tests: `make test` or `pytest tests/`
- Linting: `make lint` or `ruff check . && black --check .`
- Type Checking: `make typecheck` or `mypy .`
- Run Backend: `docker-compose up --build`
