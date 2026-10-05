"""
Comprehensive Phase 1 Physics Verification Tests.

Tests equation accuracy, invariant guarantees, integration, and dimensional consistency.
"""

from typing import Any
import pytest
import math
from backend.app.physics.units import ureg
from backend.app.physics.css_state_machine import CSSStateMachine, CSSPhase
from backend.app.physics.fluid_properties import interpolate_viscosity_cp
from backend.app.physics.css_thermal import simulate_css_thermal_trajectory
from backend.app.physics.inflow import calculate_darcy_inflow_m3d
from backend.app.physics.wellbore import calculate_wellbore_intake_pressure_kpa
from backend.app.physics.srp_kinematics import calculate_srp_kinematics
from backend.app.physics.pump import calculate_theoretical_displacement_m3d, calculate_actual_production_m3d, calculate_quasistatic_rod_loads
from backend.app.physics.energy import calculate_sor, calculate_energy_kpis
from backend.app.physics.integrated_twin import run_integrated_css_srp_simulation

def test_css_state_machine_durations() -> None:
    sm = CSSStateMachine(10.0, 5.0, 90.0)
    durations = sm.calculate_cycle_durations(105.0)
    assert durations["injection_days"] == 10.0
    assert durations["soak_days"] == 5.0
    assert durations["production_days"] == 90.0

    assert sm.get_phase_at_time(5.0) == CSSPhase.INJECTION
    assert sm.get_phase_at_time(12.0) == CSSPhase.SOAK
    assert sm.get_phase_at_time(50.0) == CSSPhase.PRODUCTION
    assert sm.get_phase_at_time(110.0) == CSSPhase.CUTOFF

def test_viscosity_monotonicity() -> None:
    table = [(48.0, 5000.0), (100.0, 150.0), (200.0, 8.0)]
    v48 = interpolate_viscosity_cp(48.0, table)
    v100 = interpolate_viscosity_cp(100.0, table)
    v200 = interpolate_viscosity_cp(200.0, table)
    
    assert v48 == pytest.approx(5000.0)
    assert v48 > v100 > v200
    assert v200 == pytest.approx(8.0)

def test_thermal_simulation_trajectory() -> None:
    res = simulate_css_thermal_trajectory(
        phase_durations_days={"injection_days": 10.0, "soak_days": 5.0, "production_days": 30.0},
        steam_injection_rate_m3d_cwe=100.0,
        steam_temperature_c=300.0
    )
    temps = res["temperature_c"]
    assert len(temps) > 5
    # During injection, temp must increase
    assert temps[5] > temps[0]
    # Peak temperature should be higher than initial reservoir temp (48°C)
    assert res["peak_temperature_c"] > 48.0

def test_darcy_inflow_monotonicity() -> None:
    # As temperature rises, viscosity drops, so inflow rate MUST increase for constant pressure drawdown
    q_cold = calculate_darcy_inflow_m3d(p_reservoir_kpa=5000, p_wf_kpa=1000, temp_c=48, viscosity_cp=5000.0)
    q_hot = calculate_darcy_inflow_m3d(p_reservoir_kpa=5000, p_wf_kpa=1000, temp_c=150, viscosity_cp=30.0)
    
    assert q_hot > q_cold
    assert q_cold >= 0.0

def test_darcy_inflow_zero_drawdown() -> None:
    # No flow when drawdown is 0 or negative
    q_zero = calculate_darcy_inflow_m3d(p_reservoir_kpa=5000, p_wf_kpa=5000, temp_c=100, viscosity_cp=100.0)
    assert q_zero == 0.0

def test_wellbore_intake_pressure() -> None:
    p_intake = calculate_wellbore_intake_pressure_kpa(
        surface_pressure_kpa=300.0,
        fluid_density_kg_m3=950.0,
        depth_m=1100.0
    )
    # Hydrostatic ~ 950 * 9.81 * 1100 / 1000 = 10251 kPa + 300 kPa = ~10551 kPa
    assert p_intake > 5000.0

def test_srp_kinematics_bounds() -> None:
    kin = calculate_srp_kinematics(stroke_length_in=100.0, spm=6.0, num_points=101)
    positions = kin["position_in"]
    assert min(positions) >= 0.0
    assert max(positions) == pytest.approx(100.0, rel=1e-3)

def test_pump_displacement_and_loads() -> None:
    q_theo = calculate_theoretical_displacement_m3d(pump_diameter_in=1.75, stroke_length_in=100.0, spm=6.0)
    assert q_theo > 0.0

    prod = calculate_actual_production_m3d(pump_diameter_in=1.75, stroke_length_in=100.0, spm=6.0)
    assert prod["actual_rate_m3d"] <= prod["theoretical_rate_m3d"]

    loads = calculate_quasistatic_rod_loads(
        rod_weight_air_lbs=12000.0,
        fluid_density_kg_m3=950.0,
        pump_depth_m=1100.0,
        pump_diameter_in=1.75,
        stroke_length_in=100.0,
        spm=6.0
    )
    assert loads["pprl_lbs"] > loads["mprl_lbs"]
    assert loads["mprl_lbs"] > 0.0

def test_energy_kpis() -> None:
    sor = calculate_sor(total_steam_m3_cwe=1000.0, total_oil_produced_m3=200.0)
    assert sor == 5.0

    kpis = calculate_energy_kpis(total_steam_m3_cwe=1000.0, total_oil_produced_m3=200.0)
    assert kpis["sor_m3_m3"] == 5.0
    assert kpis["sec_mj_m3"] > 0.0

def test_pint_dimensional_consistency() -> None:
    # Verify Pint units conversion
    depth: Any = 1100.0 * ureg.meter
    density: Any = 950.0 * ureg.kilogram / (ureg.meter ** 3)
    g: Any = 9.81 * ureg.meter / (ureg.second ** 2)

    pressure_pa: Any = density * g * depth
    pressure_kpa = pressure_pa.to(ureg.kilopascal).magnitude
    assert pytest.approx(pressure_kpa, rel=1e-3) == 10251.45

def test_integrated_simulation() -> None:
    well_cfg = {
        "well_id": "BW-01",
        "pump_depth_m": 1100.0,
        "initial_pressure_kpa": 12000.0,
        "flowing_bottomhole_pressure_kpa": 3000.0,
        "viscosity_table": [(48.0, 5000.0), (100.0, 150.0), (200.0, 8.0)]
    }
    controls = {
        "injection_days": 5.0,
        "soak_days": 3.0,
        "production_days": 20.0,
        "steam_injection_rate_m3d": 120.0,
        "steam_temperature_c": 300.0,
        "spm": 6.0,
        "stroke_length_in": 100.0,
        "pump_plunger_diameter_in": 1.75,
        "rod_weight_air_lbs": 12000.0
    }

    res = run_integrated_css_srp_simulation(well_cfg, controls)
    assert res["well_id"] == "BW-01"
    assert res["total_oil_produced_m3"] > 0.0
    assert res["total_steam_injected_m3_cwe"] == 600.0
    assert res["sor_m3_m3"] > 0.0
    assert len(res["trajectory"]) > 0
