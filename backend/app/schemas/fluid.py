
from pydantic import BaseModel, Field


class ViscosityPoint(BaseModel):
    temperature_c: float = Field(..., description="Temperature in °C")
    viscosity_cp: float = Field(..., gt=0, description="Dynamic viscosity in cP")

class FluidPVTProperties(BaseModel):
    well_id: str = Field(..., description="Unique well identifier")
    oil_api_gravity: float = Field(..., description="Oil API gravity [°API]")
    water_specific_gravity: float | None = Field(1.0, gt=0, description="Water specific gravity")
    gas_specific_gravity: float | None = Field(0.7, gt=0, description="Gas specific gravity")
    andrade_coeff_a: float | None = Field(None, description="Andrade equation coefficient A")
    andrade_coeff_b: float | None = Field(None, description="Andrade equation coefficient B")
    viscosity_table: list[ViscosityPoint] = Field(..., min_length=1, description="Viscosity-temperature measured curve")
