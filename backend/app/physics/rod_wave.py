"""
1D Damped Rod String Wave Equation Engine (Gibbs Method).

Equation:
d²u/dt² = a² d²u/dx² - c du/dt + g * (1 - rho_f / rho_s)

where:
a = speed of sound in steel (~5000 m/s = 16400 ft/s)
c = damping factor (s⁻¹)
"""

import math
from typing import Any

import numpy as np


def calculate_gibbs_downhole_card(
    surface_position_in: list[float],
    surface_load_lbs: list[float],
    spm: float,
    pump_depth_ft: float = 3600.0,
    rod_diameter_in: float = 0.875,
    damping_factor_c: float = 0.5,
    num_harmonics: int = 8
) -> dict[str, Any]:
    """
    Computes downhole plunger card (position in inches, load in lbs) from surface card
    using a Fourier series truncation solution of the Gibbs 1D damped wave equation.
    """
    if len(surface_position_in) != len(surface_load_lbs):
        raise ValueError("Position and load arrays must be of equal length")

    n_pts = len(surface_position_in)
    pos_arr = np.array(surface_position_in, dtype=float)
    load_arr = np.array(surface_load_lbs, dtype=float)

    # Convert units to US Customary for standard Gibbs formulation
    # a: Speed of sound in steel ~16300 ft/s
    a_speed = 16300.0
    rod_area_in2 = (math.pi / 4.0) * (rod_diameter_in ** 2)
    youngs_modulus_psi = 30.0e6  # Steel E = 30x10⁶ psi

    omega_0 = (2.0 * math.pi * spm) / 60.0  # Fundamental frequency rad/s

    # FFT of surface position u(0, t) and tension F(0, t)
    u_fft = np.fft.rfft(pos_arr) / n_pts
    f_fft = np.fft.rfft(load_arr) / n_pts

    downhole_pos_fft = np.zeros_like(u_fft, dtype=complex)
    downhole_load_fft = np.zeros_like(f_fft, dtype=complex)

    # Mean static offset
    downhole_pos_fft[0] = u_fft[0]
    downhole_load_fft[0] = f_fft[0]

    # Fourier mode propagation for harmonics
    max_k = min(num_harmonics, len(u_fft) - 1)
    for k in range(1, max_k + 1):
        omega_k = k * omega_0
        # Complex wave number gamma_k = sqrt(-omega_k² + i * c * omega_k) / a
        val = complex(-omega_k ** 2, damping_factor_c * omega_k)
        gamma_k = np.sqrt(val) / a_speed

        x_L = pump_depth_ft
        cosh_gL = np.cosh(gamma_k * x_L)
        sinh_gL = np.sinh(gamma_k * x_L)

        u0_k = u_fft[k]
        # Force to strain: eps_0 = F_0 / (E * A)
        eps0_k = f_fft[k] / (youngs_modulus_psi * rod_area_in2)

        # Gibbs propagation solution at depth L
        u_L_k = u0_k * cosh_gL - (eps0_k / gamma_k) * sinh_gL
        eps_L_k = -u0_k * gamma_k * sinh_gL + eps0_k * cosh_gL

        downhole_pos_fft[k] = u_L_k
        downhole_load_fft[k] = eps_L_k * (youngs_modulus_psi * rod_area_in2)

    # Inverse FFT to rebuild time series
    dh_pos = np.fft.irfft(downhole_pos_fft, n=n_pts) * n_pts
    dh_load = np.fft.irfft(downhole_load_fft, n=n_pts) * n_pts

    # Plunger stroke length is max(pos) - min(pos)
    plunger_stroke_in = float(np.max(dh_pos) - np.min(dh_pos))

    return {
        "plunger_stroke_in": max(0.0, plunger_stroke_in),
        "downhole_position_in": np.real(dh_pos).tolist(),
        "downhole_load_lbs": np.real(dh_load).tolist()
    }
