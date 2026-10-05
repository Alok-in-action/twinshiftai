from datetime import datetime

from pydantic import BaseModel, Field


class ProductionTimeSeries(BaseModel):
    well_id: str = Field(..., description="Unique well identifier")
    timestamp: datetime = Field(..., description="Measurement timestamp")
    oil_rate_m3d: float = Field(..., ge=0, description="Oil rate in m³/d")
    water_rate_m3d: float = Field(..., ge=0, description="Water rate in m³/d")
    gas_rate_m3d: float | None = Field(0.0, ge=0, description="Gas rate in m³/d")
    wellhead_temperature_c: float | None = Field(None, description="Wellhead temperature in °C")
    wellhead_pressure_kpa: float | None = Field(None, ge=0, description="Wellhead pressure in kPa")
