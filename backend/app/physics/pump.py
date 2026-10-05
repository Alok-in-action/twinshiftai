"""
Downhole Sucker Rod Pump (SRP) Model and Quasi-Static Load Engine.

Equations:
A_plunger [m²] = (pi / 4) * d_p²
q_theoretical [m³/d] = A_plunger * Stroke_length [m] * SPM * (1440 min/day)
q_actual [m³/d] = q_theoretical * Fillage_fraction * (1 - Slippage_fraction)

Quasi-Static Loads:
PPRL = Weight_rod_in_fluid + Fluid_load_on_plunger + Dynamic_accel_load
MPRL = Weight_rod_in_fluid - Dynamic_decel_load - Friction
"""

import math


def calculate_theoretical_displacement_m3d(
    pump_diameter_in: float,
    stroke_length_in: float,
    spm: float
) -> float:
    """Calculates 100% 1D theoretical pump displacement in m³/day."""
    if pump_diameter_in <= 0 or stroke_length_in <= 0 or spm <= 0:
        return 0.0

    d_p_m = pump_diameter_in * 0.0254
    stroke_m = stroke_length_in * 0.0254
    area_m2 = (math.pi / 4.0) * (d_p_m ** 2)

    strokes_per_day = spm * 1440.0
    q_theoretical_m3d = area_m2 * stroke_m * strokes_per_day
    return max(0.0, float(q_theoretical_m3d))

def calculate_actual_production_m3d(
    pump_diameter_in: float,
    stroke_length_in: float,
    spm: float,
    fillage_fraction: float = 0.85,
    slippage_fraction: float = 0.05
) -> dict[str, float]:
    """Calculates actual produced fluid rate given pump fillage and slippage."""
    q_theo = calculate_theoretical_displacement_m3d(pump_diameter_in, stroke_length_in, spm)
    eff_fillage = max(0.0, min(1.0, fillage_fraction))
    eff_slip = max(0.0, min(0.9, slippage_fraction))

    q_actual = q_theo * eff_fillage * (1.0 - eff_slip)
    volumetric_efficiency = eff_fillage * (1.0 - eff_slip)

    return {
        "theoretical_rate_m3d": q_theo,
        "actual_rate_m3d": q_actual,
        "volumetric_efficiency": volumetric_efficiency
    }

def calculate_quasistatic_rod_loads(
    rod_weight_air_lbs: float,
    fluid_density_kg_m3: float,
    pump_depth_m: float,
    pump_diameter_in: float,
    stroke_length_in: float,
    spm: float,
    steel_density_kg_m3: float = 7850.0
) -> dict[str, float]:
    """
    Computes quasi-static peak (PPRL) and minimum (MPRL) polished rod loads in lbs.
    """
    # 1. Buoyant rod weight
    buoyancy_factor = 1.0 - (fluid_density_kg_m3 / steel_density_kg_m3)
    rod_weight_fluid_lbs = rod_weight_air_lbs * max(0.1, buoyancy_factor)

    # 2. Fluid load on plunger (lbs)
    d_p_m = pump_diameter_in * 0.0254
    area_plunger_m2 = (math.pi / 4.0) * (d_p_m ** 2)
    # Hydrostatic pressure on plunger: P = rho * g * depth
    p_hydrostatic_pa = fluid_density_kg_m3 * 9.81 * pump_depth_m
    fluid_force_n = p_hydrostatic_pa * area_plunger_m2
    fluid_load_lbs = fluid_force_n * 0.224809  # N to lbs

    # 3. Dynamic impulse acceleration factor: C_acc = (SPM² * S_in) / 70500
    accel_factor = (spm ** 2 * stroke_length_in) / 70500.0

    pprl_lbs = rod_weight_fluid_lbs * (1.0 + accel_factor) + fluid_load_lbs
    mprl_lbs = rod_weight_fluid_lbs * (1.0 - accel_factor)

    return {
        "rod_weight_fluid_lbs": float(rod_weight_fluid_lbs),
        "fluid_load_lbs": float(fluid_load_lbs),
        "pprl_lbs": max(0.0, float(pprl_lbs)),
        "mprl_lbs": max(0.0, float(mprl_lbs)),
        "load_range_lbs": max(0.0, float(pprl_lbs - mprl_lbs))
    }
