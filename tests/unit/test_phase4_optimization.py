"""
Phase 4 Verification Tests: Bounded Scenario Search, Economic Objective,
and Independent Post-Solve Safety Constraint Verification.
"""

import pytest
from backend.app.optimization.scenario_search import generate_scenario_grid, evaluate_economic_objective, DecisionSpaceBounds
from backend.app.optimization.constraint_checker import OptimizationSafetyValidator
from backend.app.schemas.dynamometer import EquipmentLimitsConfig, DiagnosticMetrics

def test_scenario_grid_bounds() -> None:
    bounds = DecisionSpaceBounds()
    scenarios = generate_scenario_grid(bounds=bounds, num_samples_per_dim=2)
    assert len(scenarios) == 16  # 2^4 combinations

    for sc in scenarios:
        assert bounds.spm_min <= sc.spm <= bounds.spm_max
        assert bounds.stroke_length_min_in <= sc.stroke_length_in <= bounds.stroke_length_max_in
        assert bounds.steam_rate_min_m3d <= sc.steam_injection_rate_m3d <= bounds.steam_rate_max_m3d
        assert bounds.soak_days_min <= sc.soak_days <= bounds.soak_days_max

def test_economic_objective_function() -> None:
    net_val = evaluate_economic_objective(
        cumulative_oil_bbl=1000.0,
        steam_used_m3=100.0,
        electricity_kwh=500.0,
        peak_gearbox_torque_pct=70.0,
        oil_price_usd_bbl=75.0,
        steam_cost_usd_m3=15.0,
        elec_cost_usd_kwh=0.12
    )

    # revenue = 75,000, steam_cost = 1,500, elec_cost = 60, wear_penalty = 0 -> Net = 73,440
    assert net_val == 73440.0

def test_post_solve_safety_constraint_blocking() -> None:
    limits = EquipmentLimitsConfig(max_pprl_lbs=25000.0, max_gearbox_torque_in_lbs=320000.0, min_rod_floating_margin_lbs=500.0)
    validator = OptimizationSafetyValidator(limits=limits)

    safe_metrics = DiagnosticMetrics(
        well_id="BW-01",
        pump_fillage_fraction=0.85,
        card_area_in_lbs=45000.0,
        indicated_hydraulic_power_hp=12.5,
        pprl_lbs=22000.0,
        mprl_lbs=11000.0,
        peak_gearbox_torque_in_lbs=280000.0,
        rod_floating_margin_lbs=800.0,
        card_pattern="NORMAL",
        is_equipment_overloaded=False,
        overload_reasons=[]
    )

    res_safe = validator.validate_scenario_metrics(safe_metrics, max_allowed_temp_c=250.0, simulated_temp_c=120.0)
    assert res_safe["is_safe"]
    assert len(res_safe["violations"]) == 0

    unsafe_metrics = DiagnosticMetrics(
        well_id="BW-01",
        pump_fillage_fraction=0.85,
        card_area_in_lbs=45000.0,
        indicated_hydraulic_power_hp=12.5,
        pprl_lbs=27000.0,  # Exceeds 25000
        mprl_lbs=11000.0,
        peak_gearbox_torque_in_lbs=350000.0,  # Exceeds 320000
        rod_floating_margin_lbs=200.0,  # Below 500
        card_pattern="FLUID_POUND",
        is_equipment_overloaded=True,
        overload_reasons=["PPRL Exceeded"]
    )

    res_unsafe = validator.validate_scenario_metrics(unsafe_metrics, max_allowed_temp_c=250.0, simulated_temp_c=120.0)
    assert not res_unsafe["is_safe"]
    assert res_unsafe["blocked_from_recommendation"]
    assert len(res_unsafe["violations"]) == 3
