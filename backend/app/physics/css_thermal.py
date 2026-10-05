"""
CSS Thermal Engine: Reduced-Order Energy Balance for Heated Reservoir Temperature.

Equation:
C_eff * dT_h/dt = Q_steam - U * A * (T_h - T_far) - m_prod * c_p * (T_h - T_ref)
"""

from typing import Any

import numpy as np
from scipy.integrate import solve_ivp


def simulate_css_thermal_trajectory(
    phase_durations_days: dict[str, float],
    steam_injection_rate_m3d_cwe: float,
    steam_temperature_c: float,
    initial_temp_c: float = 48.0,
    far_field_temp_c: float = 48.0,
    produced_fluid_rate_m3d: float = 15.0,
    heated_volume_m3: float = 5000.0,
    rock_density_kg_m3: float = 2650.0,
    rock_heat_cap_j_kg_k: float = 2100.0,
    overall_heat_transfer_coeff_w_m2_k: float = 15.0,
    heat_loss_area_m2: float = 2000.0
) -> dict[str, Any]:
    """
    Simulates heated zone temperature over time across INJECTION, SOAK, and PRODUCTION phases using solve_ivp.
    Returns timestamps (days) and temperature array (°C).
    """
    c_eff = heated_volume_m3 * rock_density_kg_m3 * rock_heat_cap_j_kg_k  # J/K

    # Steam enthalpy input rate: 1 m³ CWE = 1000 kg water
    steam_heat_per_m3_j = 2.5e9
    q_steam_w = (steam_injection_rate_m3d_cwe * steam_heat_per_m3_j) / 86400.0  # Watts (J/s)

    # Heat loss coefficient U*A (W/K)
    ua_loss_w_k = overall_heat_transfer_coeff_w_m2_k * heat_loss_area_m2

    # Produced fluid heat removal per m³ liquid
    fluid_heat_cap_j_m3_k = 4.184e6
    prod_heat_removal_w_k = (produced_fluid_rate_m3d * fluid_heat_cap_j_m3_k) / 86400.0  # W/K

    inj_days = phase_durations_days.get("injection_days", 10.0)
    soak_days = phase_durations_days.get("soak_days", 5.0)
    prod_days = phase_durations_days.get("production_days", 90.0)

    # 1. Injection phase ODE
    def ode_injection(t: float, y: Any) -> list[float]:
        temp = float(y[0])
        q_loss = ua_loss_w_k * (temp - far_field_temp_c)
        dTdt = (q_steam_w - q_loss) / c_eff
        return [dTdt * 86400.0]

    t_eval_inj = np.linspace(0, inj_days, max(2, int(inj_days) + 1))
    sol_inj = solve_ivp(ode_injection, [0, inj_days], [initial_temp_c], t_eval=t_eval_inj)

    temp_after_inj = sol_inj.y[0][-1]

    # 2. Soak phase ODE
    def ode_soak(t: float, y: Any) -> list[float]:
        temp = float(y[0])
        q_loss = ua_loss_w_k * (temp - far_field_temp_c)
        dTdt = (-q_loss) / c_eff
        return [dTdt * 86400.0]

    t_eval_soak = np.linspace(0, soak_days, max(2, int(soak_days) + 1))
    sol_soak = solve_ivp(ode_soak, [0, soak_days], [temp_after_inj], t_eval=t_eval_soak)

    temp_after_soak = sol_soak.y[0][-1]

    # 3. Production phase ODE
    def ode_prod(t: float, y: Any) -> list[float]:
        temp = float(y[0])
        q_loss = ua_loss_w_k * (temp - far_field_temp_c)
        q_prod = prod_heat_removal_w_k * (temp - far_field_temp_c)
        dTdt = (-q_loss - q_prod) / c_eff
        return [dTdt * 86400.0]

    t_eval_prod = np.linspace(0, prod_days, max(2, int(prod_days) + 1))
    sol_prod = solve_ivp(ode_prod, [0, prod_days], [temp_after_soak], t_eval=t_eval_prod)

    # Combine trajectories
    t_inj = sol_inj.t
    t_soak = sol_inj.t[-1] + sol_soak.t[1:]
    t_prod = t_soak[-1] + sol_prod.t[1:]

    time_days = np.concatenate([t_inj, t_soak, t_prod])
    temps_c = np.concatenate([sol_inj.y[0], sol_soak.y[0][1:], sol_prod.y[0][1:]])

    return {
        "time_days": time_days.tolist(),
        "temperature_c": temps_c.tolist(),
        "peak_temperature_c": float(np.max(temps_c)),
        "end_temperature_c": float(temps_c[-1])
    }
