from datetime import datetime

from pydantic import BaseModel, Field


class SteamInjectionTelemetry(BaseModel):
    well_id: str = Field(..., description="Unique well identifier")
    timestamp: datetime = Field(..., description="Measurement timestamp")
    steam_rate_m3d_cwe: float = Field(..., ge=0, description="Steam rate in m³/d CWE")
    steam_mass_kg_s: float | None = Field(None, ge=0, description="Steam mass flow rate in kg/s")
    steam_quality: float = Field(..., ge=0, le=1, description="Steam quality fraction (0 to 1)")
    injection_pressure_kpa: float = Field(..., ge=0, description="Injection pressure in kPa")
    injection_temperature_c: float | None = Field(None, description="Injection temperature in °C")
