# Requirements

## 1. Project Overview
Build an engineering-grade MVP named "Baghewala CSS-SRP Digital Twin". It is a human-in-the-loop decision-support system for heavy-oil wells using cyclic steam stimulation (CSS) and sucker-rod pumps (SRP).

## 2. Core Functional Requirements
- Simulate CSS heating/cooling, heavy-oil viscosity changes, reservoir inflow.
- Simulate wellbore pressure/heat loss, SRP kinematics, rod/pump loads.
- Compute production, steam use, electricity, and failure-risk indicators.
- Jointly optimize CSS and SRP parameters.

## 3. Data Ingestion
- Ingest historical data (CSV/Excel format initially).
- Data types: production history, CSS-cycle records, steam data, VFD/SRP telemetry, dynamometer cards, failures, well completions, reservoir properties.

## 4. Safety & Operational constraints (Non-negotiable)
- Must be advisory only (no direct writes to SCADA, PLC, etc).
- Configuration/schemas must be used instead of hard-coded field values.
- Must refuse to run optimization if essential constraints/inputs are missing.
- Every recommendation requires a human approval loop.
- Independent constraint validator must check optimization outputs.

## 5. Non-Functional Requirements
- Internally use SI units with Pint for boundary conversions.
- FastAPI backend, PostgreSQL database, React/Plotly frontend.
- Provide explicit assumptions, calibration state, extrapolation flags, and model validity.
