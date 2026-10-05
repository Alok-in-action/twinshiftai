"""
Reservoir Inflow Engine (Darcy Radial Flow Model).

Equation:
q_o [m³/s] = (2 * pi * k [m²] * h [m] * (P_r - P_wf) [Pa]) / (mu_o [Pa·s] * B_o * (ln(r_e / r_w) + S))
"""

import math


def calculate_darcy_inflow_m3d(
    p_reservoir_kpa: float,
    p_wf_kpa: float,
    temp_c: float,
    viscosity_cp: float,
    permeability_md: float = 500.0,
    pay_thickness_m: float = 15.0,
    drainage_radius_m: float = 200.0,
    wellbore_radius_m: float = 0.108,
    skin_factor: float = 0.0,
    formation_volume_factor_bo: float = 1.05
) -> float:
    """
    Calculates oil inflow rate in m³/day using radial Darcy flow.
    Returns 0.0 if drawdown is zero or negative (P_wf >= P_r).
    """
    drawdown_kpa = p_reservoir_kpa - p_wf_kpa
    if drawdown_kpa <= 0 or viscosity_cp <= 0:
        return 0.0

    # Conversions to SI
    k_m2 = permeability_md * 9.869233e-16  # convert mD to m²
    delta_p_pa = drawdown_kpa * 1000.0     # convert kPa to Pa
    visc_pas = viscosity_cp / 1000.0       # convert cP to Pa·s

    ln_term = math.log(drainage_radius_m / wellbore_radius_m) + skin_factor
    if ln_term <= 0:
        raise ValueError("Invalid drainage/wellbore radius geometry")

    # Flow rate in m³/s
    q_m3s = (2.0 * math.pi * k_m2 * pay_thickness_m * delta_p_pa) / (
        visc_pas * formation_volume_factor_bo * ln_term
    )

    # Convert m³/s to m³/day
    q_m3d = q_m3s * 86400.0
    return max(0.0, float(q_m3d))
