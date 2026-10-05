"""
Unit Registry and Canonical SI Unit Converter using Pint.

SI Canonical Units in Digital Twin:
- Length: meter (m)
- Depth: meter (m)
- Mass: kilogram (kg)
- Time: second (s)
- Temperature: Celsius (°C) / Kelvin (K)
- Pressure: Pascal (Pa) / kiloPascal (kPa)
- Dynamic Viscosity: Pascal-second (Pa·s) [1 Pa·s = 1000 cP]
- Volumetric Flow Rate: m³/s [or m³/day canonical conversion]
- Mass Flow Rate: kg/s
- Force / Rod Load: Newton (N)
- Energy: Joule (J)
- Power: Watt (W)
"""

from typing import Any

import pint

# Global unit registry
ureg = pint.UnitRegistry()
# Enable common aliases if needed
ureg.define("cwe = 1 * m**3")  # Cold water equivalent unit helper
Q_ = ureg.Quantity

class UnitConversionError(ValueError):
    """Raised when unit conversion fails or dimensions are incompatible."""

def convert_to_si(value: float, from_unit_str: str, target_dimension: str) -> tuple[float, str]:
    """
    Convert a value from raw input unit to canonical SI unit.

    Supported target dimensions:
    - 'length': converts to meter (m)
    - 'pressure': converts to kiloPascal (kPa)
    - 'temperature': converts to Celsius (°C)
    - 'viscosity': converts to centipoise (cP) or Pa·s
    - 'flow_rate_liquid': converts to m³/day
    - 'force': converts to Newton (N) or lbs (canonical output: Newton)
    """
    try:
        qty = Q_(value, from_unit_str)
    except Exception as e:  # noqa: BLE001
        raise UnitConversionError(f"Invalid unit format '{from_unit_str}': {e!s}")

    if target_dimension == "length":
        converted = qty.to(ureg.meter)
        return converted.magnitude, "m"
    elif target_dimension == "pressure":
        converted = qty.to(ureg.kilopascal)
        return converted.magnitude, "kPa"
    elif target_dimension == "temperature":
        converted = qty.to(ureg.degC)
        return converted.magnitude, "°C"
    elif target_dimension == "viscosity":
        converted = qty.to(ureg.centipoise)
        return converted.magnitude, "cP"
    elif target_dimension == "flow_rate_liquid":
        converted = qty.to(ureg.meter**3 / ureg.day)
        return converted.magnitude, "m³/d"
    elif target_dimension == "force":
        converted = qty.to(ureg.newton)
        return converted.magnitude, "N"
    elif target_dimension == "power":
        converted = qty.to(ureg.kilowatt)
        return converted.magnitude, "kW"
    else:
        raise UnitConversionError(f"Unsupported target dimension: {target_dimension}")

def lbs_to_newtons(force_lbs: float) -> float:
    """Convert force in lbs to Newtons (N)."""
    return float(Q_(force_lbs, ureg.pound_force).to(ureg.newton).magnitude)

def newtons_to_lbs(force_n: float) -> float:
    """Convert force in Newtons (N) to lbs."""
    return float(Q_(force_n, ureg.newton).to(ureg.pound_force).magnitude)

def in_to_m(length_in: float) -> float:
    """Convert inches to meters."""
    return float(Q_(length_in, ureg.inch).to(ureg.meter).magnitude)

def m_to_in(length_m: float) -> float:
    """Convert meters to inches."""
    return float(Q_(length_m, ureg.meter).to(ureg.inch).magnitude)

def cp_to_pas(visc_cp: float) -> float:
    """Convert centipoise (cP) to Pascal-seconds (Pa·s)."""
    return visc_cp / 1000.0

def pas_to_cp(visc_pas: float) -> float:
    """Convert Pascal-seconds (Pa·s) to centipoise (cP)."""
    return visc_pas * 1000.0

def api_to_density(api_gravity: float) -> float:
    """
    Calculate oil density (kg/m³) at 60°F from °API gravity.
    Specific Gravity (SG) = 141.5 / (API + 131.5)
    Density = SG * 999.01 kg/m³
    """
    if api_gravity <= -131.5:
        raise ValueError("Invalid API gravity value")
    sg = 141.5 / (api_gravity + 131.5)
    return sg * 999.01

def validate_units_exist(data: dict[str, Any], required_fields: list[str]) -> bool:
    """Verify all required numeric fields in incoming data dictionary have explicit numeric values."""
    for field in required_fields:
        if field not in data or data[field] is None:
            return False
    return True
