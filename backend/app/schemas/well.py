
from pydantic import BaseModel, Field


class WellAndCompletionGeometry(BaseModel):
    well_id: str = Field(..., description="Unique well identifier")
    well_name: str | None = None
    surface_latitude: float | None = None
    surface_longitude: float | None = None
    measured_depth_m: float = Field(..., gt=0, description="Total measured depth in meters [m]")
    true_vertical_depth_m: float | None = Field(None, gt=0, description="True vertical depth in meters [m]")
    casing_outer_diameter_m: float | None = Field(None, gt=0, description="Casing outer diameter in meters [m]")
    tubing_inner_diameter_m: float = Field(..., gt=0, description="Tubing inner diameter in meters [m]")
    pump_depth_m: float = Field(..., gt=0, description="Downhole pump set depth in meters [m]")
    perforation_top_m: float | None = Field(None, gt=0, description="Perforation top depth in meters [m]")
    perforation_bottom_m: float | None = Field(None, gt=0, description="Perforation bottom depth in meters [m]")
