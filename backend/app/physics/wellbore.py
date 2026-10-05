"""
Segmented Wellbore Hydraulics and Thermal Loss Engine.
"""

import math


def calculate_wellbore_intake_pressure_kpa(
    surface_pressure_kpa: float,
    fluid_density_kg_m3: float,
    depth_m: float,
    flow_rate_m3d: float = 20.0,
    tubing_id_m: float = 0.076
) -> float:
    """
    Calculates bottomhole pump intake pressure (kPa) given hydrostatic head and friction loss.
    P_intake = P_surface + rho * g * depth - P_friction
    """
    g = 9.81
    hydrostatic_pa = fluid_density_kg_m3 * g * depth_m

    # Tubing cross-sectional area
    area_m2 = math.pi * (tubing_id_m / 2.0) ** 2
    q_m3s = flow_rate_m3d / 86400.0
    velocity_m_s = q_m3s / area_m2 if area_m2 > 0 else 0.0

    # Simplified Darcy-Weisbach friction loss in tubing (Pa)
    f_factor = 0.02
    friction_pa = f_factor * (depth_m / tubing_id_m) * (fluid_density_kg_m3 * velocity_m_s ** 2 / 2.0)

    p_intake_pa = (surface_pressure_kpa * 1000.0) + hydrostatic_pa - friction_pa
    return max(100.0, float(p_intake_pa / 1000.0))  # returned in kPa
