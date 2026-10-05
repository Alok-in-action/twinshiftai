# Validation Plan

## 1. Verification of Equations and Code (Unit/Property Tests)
- **Unit Consistency**: All physical equations must pass `pint` dimensional analysis.
- **Invariants**: Test for non-negative viscosity, strict chronology of CSS phases, monotonic theoretical pump displacement relative to stroke/SPM, and energy conservation.

## 2. Component Validation (Integration Tests)
- **Physics Core**: Simulate a synthetic but dimensionally correct CSS cycle (injection -> soak -> production) and verify continuity of temperature and pressure.
- **Rod Dynamics**: Verify rod floating and impact detection logic triggers correctly on boundary condition edge cases.

## 3. Safety and Constraint Validation
- **Missing Data**: Guarantee the optimizer throws a clear exception if approved constraints or PVT data are missing.
- **Feasibility Checker**: Post-optimization validator must flag any candidate that exceeds limits (e.g. stress, load, pressure).

## 4. ML Validation
- **Leakage Prevention**: Implement and test chronological, cycle-grouped, and well-grouped cross-validation.
- **Baselines**: ML residual models must measurably improve MAE/RMSE over the pure physics model on an unseen holdout cycle.

## 5. End-to-End Acceptance Criteria
- Full offline simulation of one historical Baghewala well over one complete CSS cycle, comparing measured production vs. simulated trends.
- The dashboard successfully displays dynamometer diagnostics, limits, and at least 3 constrained recommended scenarios (baseline, conservative, aggressive).
