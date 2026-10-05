from datetime import datetime

from pydantic import BaseModel, Field


class CSSCycleRecord(BaseModel):
    well_id: str = Field(..., description="Unique well identifier")
    cycle_number: int = Field(..., ge=1, description="Cycle sequence number")
    injection_start_time: datetime = Field(..., description="Timestamp injection started")
    soak_start_time: datetime = Field(..., description="Timestamp soak phase started")
    production_start_time: datetime = Field(..., description="Timestamp production started")
    cutoff_time: datetime | None = Field(None, description="Timestamp cycle terminated")
    total_steam_injected_m3_cwe: float | None = Field(None, ge=0, description="Total steam injected in m³ CWE")
    avg_steam_quality: float | None = Field(None, ge=0, le=1, description="Average steam quality (0 to 1)")
