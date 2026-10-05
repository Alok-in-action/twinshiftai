# Project: Well-to-Surface Digital Twin (CSS + SRP), SIH26120, Baghewala heavy-oil field

## Goal
Calibrated, physics-based digital twin that couples reservoir (CSS thermal), wellbore, SRP and surface, with AI optimization and closed-loop SPM/VFD control.

## Stack
Backend: Python 3.11+, FastAPI, WebSockets, SQLite, NumPy, SciPy, pandas, scikit-learn, XGBoost, Optuna, SHAP, pytest.
Frontend: Next.js 14 + TypeScript + Tailwind + Recharts.
SRP wave equation: use libzrod if it installs; otherwise implement Gibbs finite-difference in /backend/physics/srp_wave.py.

## Rules
- Physics first: no hard-coded outputs. Every displayed number must come from a model or a dataset.
- Label every dataset "synthetic" or "field". Never present synthetic metrics as real.
- Calibrate on the first 70% of cycles and report MAPE/RMSE/R2 on the held-out 30%.
- All models return uncertainty (P10/P50/P90 or prediction intervals).
- Any setpoint change needs operator approval and must pass safety checks (no rod floating, peak load < limit, pump fillage > threshold).
- Add pytest tests for each physics module (units, monotonicity, energy balance).
- Keep modules small; type hints and docstrings; units in variable names (e.g. temp_c, rate_bpd).
- Before editing, produce an implementation plan and wait for approval. Finish each phase with a walkthrough and passing tests.

## Layout
/backend/{physics,data,ml,optimizer,control,api,tests}  /frontend  /data/{raw,synthetic}  /docs