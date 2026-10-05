from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, Field, model_validator


class Well(BaseModel):
    well_id: str
    coordinates: tuple[float, float]
    depth: float = Field(..., gt=0.0, description="Measured depth in meters")
    deviation: float = Field(..., ge=0.0, le=90.0)
    completion: str
    perforations: list[tuple[float, float]]
    tubing_id: float = Field(..., gt=0.0, description="Tubing inner diameter in meters")
    casing_id: float = Field(..., gt=0.0, description="Casing inner diameter in meters")

class ReservoirProperties(BaseModel):
    net_pay: float = Field(..., gt=0.0, description="Net pay thickness in meters")
    porosity: float = Field(..., gt=0.0, lt=1.0)
    permeability: float = Field(..., gt=0.0, description="Permeability in mD")
    pressure: float = Field(..., gt=0.0, description="Reservoir pressure in Pa")
    temperature: float = Field(..., gt=0.0, description="Reservoir temperature in Kelvin")
    sw: float = Field(..., ge=0.0, le=1.0, description="Water saturation")

class FluidPVT(BaseModel):
    timestamp: datetime
    temperature: float = Field(..., gt=0.0, description="Temperature in Kelvin")
    pressure: float = Field(..., gt=0.0, description="Pressure in Pa")
    viscosity: float = Field(..., gt=0.0, description="Viscosity in Pa.s")
    density: float = Field(..., gt=0.0, description="Density in kg/m3")
    bo: float = Field(..., gt=0.0, description="Formation volume factor m3/m3")
    water_cut: float = Field(..., ge=0.0, le=1.0)
    gas_data: dict[str, Any] | None = None

class CSSCycle(BaseModel):
    well_id: str
    cycle_number: int = Field(..., gt=0)
    injection_start: datetime
    injection_end: datetime
    steam_cwe: float = Field(..., gt=0.0, description="Cold water equivalent volume in m3")
    steam_quality: float = Field(..., ge=0.0, le=1.0)
    steam_pressure: float = Field(..., gt=0.0, description="Pressure in Pa")
    steam_temperature: float = Field(..., gt=0.0, description="Temperature in Kelvin")
    soak_start: datetime
    soak_end: datetime
    production_restart: datetime
    
    @model_validator(mode='after')
    def check_chronology(self) -> 'CSSCycle':
        if self.injection_start >= self.injection_end:
            raise ValueError("injection_start must be before injection_end")
        if self.soak_start >= self.soak_end:
            raise ValueError("soak_start must be before soak_end")
        if self.injection_end > self.soak_start:
            raise ValueError("injection must end before or when soak starts")
        if self.soak_end > self.production_restart:
            raise ValueError("soak must end before or when production restarts")
        return self

class ProductionDaily(BaseModel):
    well_id: str
    timestamp: datetime
    oil: float = Field(..., ge=0.0, description="Oil rate in m3/d")
    water: float = Field(..., ge=0.0, description="Water rate in m3/d")
    gas: float = Field(..., ge=0.0, description="Gas rate in m3/d")
    fluid: float = Field(..., ge=0.0, description="Total fluid rate in m3/d")
    hours_online: float = Field(..., ge=0.0, le=24.0)
    pressure: float = Field(..., gt=0.0, description="Pressure in Pa")
    temperature: float = Field(..., gt=0.0, description="Temperature in Kelvin")

class SRPTelemetry(BaseModel):
    timestamp: datetime
    spm: float = Field(..., ge=0.0, description="Strokes per minute")
    stroke: float = Field(..., gt=0.0, description="Stroke length in meters")
    vfd_hz: float = Field(..., ge=0.0)
    current: float = Field(..., ge=0.0)
    voltage: float = Field(..., ge=0.0)
    power: float = Field(..., ge=0.0)
    torque: float = Field(..., ge=0.0)
    surface_load_reference: float
    position_reference: float

class Constraints(BaseModel):
    parameter: str
    lower_limit: float
    upper_limit: float
    unit: str
    source: str
    approval_date: date
    well_applicability: list[str]
    
    @model_validator(mode='after')
    def check_limits(self) -> 'Constraints':
        if self.lower_limit > self.upper_limit:
            raise ValueError("lower_limit must be <= upper_limit")
        return self
