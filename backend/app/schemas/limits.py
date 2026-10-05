
from pydantic import BaseModel, Field


class WellOperatingLimits(BaseModel):
    max_peak_polished_rod_load_lbs: float = Field(25000.0, gt=0)
    min_polished_rod_load_lbs: float = Field(1000.0, ge=0)
    max_spm: float = Field(12.0, gt=0)
    min_spm: float = Field(1.0, gt=0)
    max_stroke_length_in: float = Field(144.0, gt=0)
    min_stroke_length_in: float = Field(24.0, gt=0)
    max_steam_injection_rate_m3d: float = Field(200.0, gt=0)
    max_steam_pressure_kpa: float = Field(12000.0, gt=0)
    max_steam_temperature_c: float = Field(325.0, gt=0)
    max_goodman_stress_ratio: float = Field(0.90, gt=0, le=1.0)
    min_rod_floating_margin_lbs: float = Field(500.0, ge=0)

class ApprovedOperatingConstraints(BaseModel):
    limits_version: str = Field("1.0.0")
    approved_by: str = Field("Lead Petroleum Engineer")
    well_limits: WellOperatingLimits
    required_parameters: list[str]
