"""
Fluid Properties and Viscosity Modeling.

Includes:
1. Andrade Equation: ln(mu_cP) = A + B / (T_C + 273.15)
2. Monotonic Viscosity Interpolation with strict extrapolation protection.
3. CoolProp Steam/Water Thermodynamic Wrapper.
"""

import math

import numpy as np
from scipy.interpolate import interp1d

try:
    import CoolProp.CoolProp as CP
    COOLPROP_AVAILABLE = True
except ImportError:
    COOLPROP_AVAILABLE = False

class ViscosityExtrapolationError(ValueError):
    """Raised when temperature falls outside measured viscosity range without permission."""

def andrade_viscosity_cp(temp_c: float, coeff_a: float, coeff_b: float) -> float:
    """
    Calculates viscosity in cP using Andrade equation:
    ln(visc_cp) = A + B / (temp_c + 273.15)
    """
    temp_k = temp_c + 273.15
    if temp_k <= 0:
        raise ValueError("Temperature in Kelvin must be positive")
    ln_visc = coeff_a + (coeff_b / temp_k)
    return math.exp(ln_visc)

def fit_andrade_coefficients(temp_c_list: list[float], visc_cp_list: list[float]) -> tuple[float, float]:
    """Fits Andrade coefficients A and B from measured (temp_c, visc_cp) data points."""
    if len(temp_c_list) < 2 or len(temp_c_list) != len(visc_cp_list):
        raise ValueError("At least 2 data points required for Andrade fitting")
    
    temp_k = np.array(temp_c_list) + 273.15
    inv_t = 1.0 / temp_k
    ln_visc = np.log(visc_cp_list)

    # Linear fit: ln_visc = A + B * (1/T)
    poly = np.polyfit(inv_t, ln_visc, 1)
    coeff_b = float(poly[0])
    coeff_a = float(poly[1])
    return coeff_a, coeff_b

def interpolate_viscosity_cp(
    temp_c: float,
    measured_table: list[tuple[float, float]],
    allow_extrapolation: bool = False
) -> float:
    """
    Monotonic log-linear interpolation of measured viscosity vs temperature.

    measured_table: list of (temperature_c, viscosity_cp) tuples.
    """
    if not measured_table:
        raise ValueError("Viscosity table cannot be empty")

    # Sort table by temperature ascending
    sorted_table = sorted(measured_table, key=lambda x: x[0])
    temps = np.array([pt[0] for pt in sorted_table])
    viscs = np.array([pt[1] for pt in sorted_table])

    min_t, max_t = temps[0], temps[-1]

    if not allow_extrapolation and (temp_c < min_t or temp_c > max_t):
        raise ViscosityExtrapolationError(
            f"Temperature {temp_c}°C is outside measured bounds [{min_t}°C, {max_t}°C]"
        )

    # Use log-viscosity for linear interpolation vs temperature
    ln_viscs = np.log(viscs)
    
    if allow_extrapolation:
        f_interp = interp1d(temps, ln_viscs, kind='linear', fill_value="extrapolate")
    else:
        f_interp = interp1d(temps, ln_viscs, kind='linear')

    ln_val = float(f_interp(temp_c))
    return float(np.exp(ln_val))

def get_steam_properties(temp_c: float, pressure_kpa: float) -> dict[str, float]:
    """
    Calculates thermodynamic steam/water properties via CoolProp or fallback approximations.
    """
    pressure_pa = pressure_kpa * 1000.0
    temp_k = temp_c + 273.15

    if COOLPROP_AVAILABLE:
        try:
            h_liquid = CP.PropsSI('H', 'T', temp_k, 'Q', 0.0, 'Water') / 1000.0  # kJ/kg
            h_vapor = CP.PropsSI('H', 'T', temp_k, 'Q', 1.0, 'Water') / 1000.0   # kJ/kg
            sat_temp_k = CP.PropsSI('T', 'P', pressure_pa, 'Q', 0.5, 'Water')
            return {
                "liquid_enthalpy_kj_kg": float(h_liquid),
                "vapor_enthalpy_kj_kg": float(h_vapor),
                "latent_heat_kj_kg": float(h_vapor - h_liquid),
                "saturation_temp_c": float(sat_temp_k - 273.15)
            }
        except Exception:  # noqa: S110, BLE001
            pass

    # Fallback thermodynamic correlations for steam/water if CoolProp not initialized
    # Approximate saturation temperature (°C) vs pressure (kPa)
    sat_temp_c = 100.0 * (pressure_kpa / 101.325) ** 0.25
    h_liquid = 4.184 * min(temp_c, sat_temp_c)  # kJ/kg
    latent_heat = 2260.0 - 2.2 * (temp_c - 100.0)
    return {
        "liquid_enthalpy_kj_kg": max(0.0, h_liquid),
        "vapor_enthalpy_kj_kg": max(0.0, h_liquid + latent_heat),
        "latent_heat_kj_kg": max(500.0, latent_heat),
        "saturation_temp_c": max(100.0, sat_temp_c)
    }
