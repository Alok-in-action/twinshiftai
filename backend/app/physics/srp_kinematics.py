"""
Sucker Rod Pump (SRP) Surface Kinematics Engine.

Equations (Sinusoidal MVP Kinematics):
omega [rad/s] = 2 * pi * SPM / 60
x_s(t) [m] = (S_m / 2) * (1 - cos(omega * t))
v_s(t) [m/s] = (S_m * omega / 2) * sin(omega * t)
a_s(t) [m/s²] = (S_m * omega² / 2) * cos(omega * t)
"""

import math
from typing import Any

import numpy as np


def calculate_srp_kinematics(
    stroke_length_in: float,
    spm: float,
    num_points: int = 101
) -> dict[str, Any]:
    """
    Computes polished rod position, velocity, and acceleration over one stroke cycle (t = 0 to T_cycle).
    Ensures exact midpoint and endpoint sampling.
    """
    if stroke_length_in <= 0 or spm <= 0:
        raise ValueError("Stroke length and SPM must be positive")

    stroke_m = stroke_length_in * 0.0254
    omega_rad_s = (2.0 * math.pi * spm) / 60.0
    period_s = 60.0 / spm

    time_array_s = np.linspace(0.0, period_s, num_points)
    
    # Position: 0 to stroke_m
    pos_m = (stroke_m / 2.0) * (1.0 - np.cos(omega_rad_s * time_array_s))
    pos_in = pos_m / 0.0254

    # Velocity: m/s
    vel_m_s = (stroke_m * omega_rad_s / 2.0) * np.sin(omega_rad_s * time_array_s)

    # Acceleration: m/s²
    acc_m_s2 = (stroke_m * (omega_rad_s ** 2) / 2.0) * np.cos(omega_rad_s * time_array_s)

    return {
        "period_s": float(period_s),
        "omega_rad_s": float(omega_rad_s),
        "time_s": time_array_s.tolist(),
        "position_in": pos_in.tolist(),
        "velocity_m_s": vel_m_s.tolist(),
        "acceleration_m_s2": acc_m_s2.tolist()
    }
