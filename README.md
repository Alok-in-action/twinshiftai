# Baghewala Heavy Oil CSS–SRP Physics-Informed Digital Twin

> **TWIN LIFT AI / DIGITAL TWIN SYSTEM — ADVISORY ONLY**
>
> *Safety Disclaimer: This digital twin operates strictly in an advisory capacity with NO DIRECT CONTROL over field equipment, pumps, or steam valves. All operational recommendations must undergo independent engineering review before execution.*

---

## Overview

The **Baghewala Digital Twin** is a physics-informed hybrid simulation and decision-support system designed specifically for the heavy oil Cyclic Steam Stimulation (CSS) and Sucker Rod Pumping (SRP) operations in the Baghewala oil field (Rajasthan, India).

### Key Features

1. **Phase 0: Domain Contracts & Safety Engine**
   - Configurable limits schema (`configs/operating_limits.json`).
   - Hard post-solve safety constraint validator.
   - `Pint` unit registry for SI unit consistency.

2. **Phase 1: Integrated Physics Simulator**
   - CSS thermal balance & reservoir heating model.
   - Fluid viscosity thermal model ($15,000\ \text{cP}$ to $< 200\ \text{cP}$).
   - Darcy heavy-oil inflow and wellbore intake pressure dynamics.
   - SRP kinematics, pump displacement, and energy KPIs ($\text{kWh}/\text{bbl}$, $\text{SOR}$).

3. **Phase 2: Dynamometer Diagnostics & Gibbs Rod-Wave Engine**
   - Gibbs 1D Fourier damped wave equation transformation (Surface to Downhole cards).
   - Downhole pump fillage estimation & indicated hydraulic horsepower.
   - Automated card pattern classification (`NORMAL`, `FLUID_POUND`, `GAS_LOCKING`, `HIGH_DRAG`).
   - Structural load, gearbox torque, and downstroke rod-floating margin safety diagnostics.

4. **Phase 3: Hybrid Physics-Residual Machine Learning**
   - Leakage-safe time-series feature engineering.
   - Physics-residual regression ($y_{\text{hybrid}} = y_{\text{physics}} + f_{\text{residual}}(X)$).
   - Failure mode probability classification.
   - Chronological, CSS cycle, and well-based validation split strategies.

5. **Phase 4: Bounded Optimization & Scenario Search**
   - Multi-dimensional decision grid search ($\text{SPM}$, stroke length, steam rate, soak days).
   - Joint economic objective maximizing Net Present Value (NPV) while penalizing energy cost and equipment wear.
   - Independent post-solve safety constraint checker to block unsafe operational candidate recommendations.

6. **Phase 5: FastAPI Backend, React Dashboard UI & Deployment**
   - High-performance FastAPI backend routes (`/api/v1/simulate`, `/api/v1/diagnostics/dynamometer`, `/api/v1/optimize`).
   - Single-page React dashboard UI.
   - Containerized Docker & Docker Compose setup.

---

## Installation & Setup

### Prerequisites

- Python 3.12+
- Docker & Docker Compose (Optional for containerized deployment)

### Running Locally

```bash
# 1. Export PYTHONPATH
export PYTHONPATH="$(pwd):$PYTHONPATH"

# 2. Install dependencies
pip install -r pyproject.toml

# 3. Start FastAPI server
uvicorn backend.app.main:app --reload --port 8000
```

### Running with Docker

```bash
docker-compose up --build
```

---

## Running Unit & Integration Tests

```bash
export PYTHONPATH="$(pwd):$PYTHONPATH"
pytest -v
```

---

## Project Structure

```
baghewala-digital-twin/
├── backend/
│   └── app/
│       ├── main.py                     # FastAPI application routes
│       ├── ml/                         # Feature engineering, residual regressor & splits
│       ├── optimization/               # Scenario search & post-solve constraint checker
│       ├── physics/                    # CSS thermal, hydraulics, SRP kinematics & Gibbs rod wave
│       └── schemas/                    # Pydantic v2 domain schemas
├── configs/
│   └── operating_limits.json           # Safety & equipment rating thresholds
├── frontend/
│   └── index.html                      # Digital twin dashboard UI
├── tests/
│   ├── e2e/                            # End-to-end integration tests
│   └── unit/                           # Physics, diagnostic, ML & optimization unit tests
├── Dockerfile                          # Container specification
├── docker-compose.yml                  # Multi-container orchestration
├── pyproject.toml                      # Dependencies & project metadata
└── README.md                           # System documentation
```
