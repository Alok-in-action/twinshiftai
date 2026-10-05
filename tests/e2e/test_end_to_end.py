"""
Phase 5 End-to-End Integration Tests.
"""

import pytest
import httpx
from backend.app.main import app

@pytest.mark.anyio
async def test_e2e_health_check() -> None:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        assert response.json()["status"] == "HEALTHY"

@pytest.mark.anyio
async def test_e2e_simulation_workflow() -> None:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "well_id": "BW-01",
            "spm": 6.0,
            "stroke_length_in": 100.0,
            "steam_injection_rate_m3d": 20.0,
            "soak_days": 5.0,
            "production_days": 90.0
        }
        response = await client.post("/api/v1/simulate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "SUCCESS"
        assert "thermal" in data["data"]
        assert "production" in data["data"]
        assert "kpis" in data["data"]

@pytest.mark.anyio
async def test_e2e_dynamometer_diagnostics_workflow() -> None:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "well_id": "BW-01",
            "stroke_length_in": 100.0,
            "spm": 6.0,
            "position_in": [0.0, 50.0, 100.0, 50.0, 0.0],
            "load_lbs": [12000.0, 18000.0, 17000.0, 9000.0, 12000.0]
        }
        response = await client.post("/api/v1/diagnostics/dynamometer", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "SUCCESS"
        assert "pump_fillage_fraction" in data["diagnostics"]

@pytest.mark.anyio
async def test_e2e_optimization_workflow() -> None:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "well_id": "BW-01",
            "oil_price_usd_bbl": 75.0,
            "steam_cost_usd_m3": 15.0
        }
        response = await client.post("/api/v1/optimize", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "SUCCESS"
        assert "top_recommendations" in data
        assert len(data["top_recommendations"]) > 0
