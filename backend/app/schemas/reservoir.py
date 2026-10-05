
from pydantic import BaseModel, Field


class ReservoirProperties(BaseModel):
    well_id: str = Field(..., description="Unique well identifier")
    initial_pressure_kpa: float = Field(..., gt=0, description="Initial reservoir pressure in kPa")
    initial_temperature_c: float = Field(..., description="Initial reservoir temperature in °C")
    porosity: float | None = Field(None, ge=0.0, le=1.0, description="Reservoir porosity (fraction)")
    permeability_md: float | None = Field(None, gt=0, description="Permeability in milliDarcy [mD]")
    pay_thickness_m: float = Field(..., gt=0, description="Net pay thickness in meters [m]")
    drainage_radius_m: float | None = Field(None, gt=0, description="Drainage radius in meters [m]")
    wellbore_radius_m: float | None = Field(None, gt=0, description="Wellbore radius in meters [m]")
    rock_heat_capacity_j_kg_k: float | None = Field(2100.0, gt=0, description="Rock heat capacity [J/kg/K]")
    rock_density_kg_m3: float | None = Field(2650.0, gt=0, description="Rock density [kg/m³]")
