from datetime import datetime

from pydantic import BaseModel, Field


class SRPVFDTelemetry(BaseModel):
    well_id: str = Field(..., description="Unique well identifier")
    timestamp: datetime = Field(..., description="Measurement timestamp")
    spm: float = Field(..., ge=0, description="Strokes per minute")
    vfd_frequency_hz: float | None = Field(None, ge=0, description="VFD motor frequency in Hz")
    motor_current_amp: float | None = Field(None, ge=0, description="Motor current in Amps")
    motor_power_kw: float | None = Field(None, ge=0, description="Motor power in kW")
    peak_polished_rod_load_lbs: float | None = Field(None, description="Peak polished rod load in lbs")
    min_polished_rod_load_lbs: float | None = Field(None, description="Minimum polished rod load in lbs")
