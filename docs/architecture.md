# Architecture

## 1. Overview
The MVP uses a modular monolith architecture.
The digital twin has separate layers for data ingestion, physics-based simulation, ML residuals, optimization, and human-in-the-loop approval.

## 2. Components
### 2.1 Backend (Python 3.12, FastAPI, SQLAlchemy)
- **Ingestion & Validation**: Pydantic schemas validating tabular inputs.
- **Physics Engine**: Pure functions and SciPy ODE solvers (`scipy.integrate.solve_ivp`). Includes modules for CSS thermal, wellbore, inflow, SRP kinematics, pump dynamics, and energy.
- **ML Layer**: `scikit-learn` based models for residual correction, anomaly detection, and failure risk prediction.
- **Optimization Layer**: Enumeration or `scipy.optimize` with bounded scenarios, followed by an independent constraint validator.

### 2.2 Database (PostgreSQL)
- Relational schema for well definitions, completion geometry, CSS cycles, and configuration limits.
- Time-series capable for telemetry, production data, and dynamometer cards.

### 2.3 Frontend (React, TypeScript, Vite, Plotly)
- Engineering dashboard with well status, CSS planner, SRP diagnostics, and joint optimization views.

## 3. Data Flow
1. **Ingestion**: Raw data -> Schema Validation -> SI Unit conversion.
2. **State Estimation**: Build features and estimate current well state.
3. **Simulation**: Run Physics Twin (CSS + SRP).
4. **Correction**: Apply ML residual/risk models.
5. **Optimization**: Run constrained optimizer for candidate controls.
6. **Recommendation**: Return feasible options with confidence/explanations.
7. **Approval**: Human operator accepts or rejects recommendation.
