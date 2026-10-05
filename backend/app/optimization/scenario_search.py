"""
Scenario Grid Generation & Economic Objective Function for Optimization.
"""

from typing import List, Dict, Any, Optional
import itertools
from pydantic import BaseModel, Field
import numpy as np

class DecisionSpaceBounds(BaseModel):
    spm_min: float = 4.0
    spm_max: float = 12.0
    stroke_length_min_in: float = 80.0
    stroke_length_max_in: float = 140.0
    steam_rate_min_m3d: float = 10.0
    steam_rate_max_m3d: float = 50.0
    soak_days_min: float = 3.0
    soak_days_max: float = 10.0

class ScenarioConfig(BaseModel):
    spm: float
    stroke_length_in: float
    steam_injection_rate_m3d: float
    soak_days: float

    def to_dict(self) -> Dict[str, float]:
        return {
            "spm": self.spm,
            "stroke_length_in": self.stroke_length_in,
            "steam_injection_rate_m3d": self.steam_injection_rate_m3d,
            "soak_days": self.soak_days
        }

OperationalScenario = ScenarioConfig

def generate_scenario_grid(bounds: DecisionSpaceBounds = DecisionSpaceBounds(), num_samples_per_dim: int = 2) -> List[ScenarioConfig]:
    spms = np.linspace(bounds.spm_min, bounds.spm_max, num_samples_per_dim)
    strokes = np.linspace(bounds.stroke_length_min_in, bounds.stroke_length_max_in, num_samples_per_dim)
    steams = np.linspace(bounds.steam_rate_min_m3d, bounds.steam_rate_max_m3d, num_samples_per_dim)
    soaks = np.linspace(bounds.soak_days_min, bounds.soak_days_max, num_samples_per_dim)

    scenarios = []
    for spm, stroke, steam, soak in itertools.product(spms, strokes, steams, soaks):
        scenarios.append(ScenarioConfig(
            spm=float(spm),
            stroke_length_in=float(stroke),
            steam_injection_rate_m3d=float(steam),
            soak_days=float(soak)
        ))
    return scenarios

def evaluate_economic_objective(
    cumulative_oil_bbl: float,
    steam_used_m3: float,
    electricity_kwh: float,
    r_failure: float = 0.0,
    r_float: float = 0.0,
    r_impact: float = 0.0,
    oil_price_usd_bbl: float = 75.0,
    steam_cost_usd_m3: float = 15.0,
    elec_cost_usd_kwh: float = 0.10,
    c_m_usd: float = 10000.0,
    lambda_1: float = 2000.0,
    lambda_2: float = 2000.0
) -> float:
    """
    Evaluates the joint multi-term economic and engineering objective function.
    J = R_o * Q_o - C_s * M_s - C_e * E - C_m * R_failure - lambda_1 * R_float - lambda_2 * R_impact
    """
    revenue = cumulative_oil_bbl * oil_price_usd_bbl
    steam_cost = steam_used_m3 * steam_cost_usd_m3
    elec_cost = electricity_kwh * elec_cost_usd_kwh
    maintenance_cost = c_m_usd * r_failure
    float_penalty = lambda_1 * r_float
    impact_penalty = lambda_2 * r_impact

    net_val = revenue - steam_cost - elec_cost - maintenance_cost - float_penalty - impact_penalty
    return float(net_val)
