"""
Dynamometer Card and Diagnostic Data Schemas.
"""

from datetime import UTC, datetime

from pydantic import BaseModel, Field


class SurfaceDynamometerCard(BaseModel):
    well_id: str = Field(..., description="Well identifier")
    stroke_length_in: float = Field(..., gt=0, description="Surface stroke length in inches")
    spm: float = Field(..., gt=0, description="Strokes per minute")
    position_in: list[float] = Field(..., description="Polished rod position array (in)")
    load_lbs: list[float] = Field(..., description="Polished rod load array (lbs)")
    time_s: list[float] | None = Field(None, description="Time array (seconds)")

class DownholeDynamometerCard(BaseModel):
    well_id: str = Field(..., description="Well identifier")
    pump_depth_m: float = Field(..., gt=0, description="Pump depth in meters")
    plunger_stroke_in: float = Field(..., description="Effective downhole stroke length in inches")
    position_in: list[float] = Field(..., description="Plunger position array (in)")
    load_lbs: list[float] = Field(..., description="Plunger load array (lbs)")

class DynamometerCardData(BaseModel):
    well_id: str = Field("BW-01", description="Well ID")
    card_id: str | None = Field("CARD-001")
    timestamp: datetime | None = Field(default_factory=lambda: datetime.now(UTC))
    card_type: str = Field("surface")
    surface_position_in: list[float] = Field(default_factory=list)
    surface_load_lbs: list[float] = Field(default_factory=list)
    position_in: list[float] = Field(default_factory=list)
    load_lbs: list[float] = Field(default_factory=list)
    downhole_position_in: list[float] | None = Field(None)
    downhole_load_lbs: list[float] | None = Field(None)
    spm: float = Field(6.0, gt=0)
    stroke_length_in: float = Field(100.0, gt=0)
    num_samples: int | None = Field(None)

class DiagnosticMetrics(BaseModel):
    well_id: str
    pump_fillage_fraction: float = Field(..., ge=0.0, le=1.0)
    card_area_in_lbs: float = Field(..., description="Indicated pump stroke work (in-lbs)")
    indicated_hydraulic_power_hp: float = Field(..., ge=0.0)
    pprl_lbs: float = Field(..., ge=0.0)
    mprl_lbs: float = Field(..., ge=0.0)
    peak_gearbox_torque_in_lbs: float = Field(..., ge=0.0)
    rod_floating_margin_lbs: float = Field(..., description="Margin above zero downstroke tension")
    card_pattern: str = Field(..., description="Identified card diagnostic pattern (e.g. Normal, Fluid Pound, Gas Locking)")
    is_equipment_overloaded: bool = Field(False)
    overload_reasons: list[str] = Field(default_factory=list)

class EquipmentLimitsConfig(BaseModel):
    max_pprl_lbs: float = 25000.0
    max_gearbox_torque_in_lbs: float = 320000.0
    max_rod_stress_psi: float = 35000.0
    min_rod_floating_margin_lbs: float = 500.0
