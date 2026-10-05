
from pydantic import BaseModel, Field


class RodSectionSpec(BaseModel):
    section_index: int = Field(..., ge=0)
    rod_diameter_in: float = Field(..., gt=0, description="Rod diameter in inches")
    length_m: float = Field(..., gt=0, description="Section length in meters")
    material: str = Field("Steel", description="Rod material grade")
    density_kg_m3: float = Field(7850.0, gt=0, description="Material density kg/m³")
    elastic_modulus_pa: float = Field(2.0e11, gt=0, description="Elastic modulus in Pa")

class EquipmentSpecifications(BaseModel):
    well_id: str = Field(..., description="Unique well identifier")
    unit_geometry_type: str = Field("Conventional", description="Pumping unit geometry type")
    crank_radius_m: float | None = Field(1.5, gt=0, description="Crank radius in meters")
    stroke_length_in: float = Field(100.0, gt=0, description="Rated stroke length in inches")
    pump_plunger_diameter_in: float = Field(..., gt=0, description="Downhole pump plunger diameter in inches")
    rod_string_sections: list[RodSectionSpec] = Field(..., min_length=1, description="Rod string section taper details")
