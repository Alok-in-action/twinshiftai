"""
Phase 2 Verification Tests: Surface/Downhole Dynamometer Contracts, Gibbs Wave Equation Solver,
Pump Fillage, Pattern Classification, and Equipment Limit Diagnostics.
"""

import pytest
import numpy as np

from backend.app.schemas.dynamometer import SurfaceDynamometerCard, DownholeDynamometerCard, EquipmentLimitsConfig
from backend.app.physics.rod_wave import calculate_gibbs_downhole_card
from backend.app.physics.diagnostics import (
    calculate_card_area_in_lbs,
    calculate_pump_fillage_fraction,
    classify_dynamometer_pattern,
    evaluate_equipment_limits,
    analyze_dynamometer_card
)

def test_surface_dynamometer_schema() -> None:
    card = SurfaceDynamometerCard(
        well_id="BW-01",
        stroke_length_in=100.0,
        spm=6.0,
        time_s=[0.0, 1.0, 2.0, 3.0, 4.0],
        position_in=[0.0, 50.0, 100.0, 50.0, 0.0],
        load_lbs=[12000.0, 18000.0, 17000.0, 9000.0, 12000.0]
    )
    assert card.well_id == "BW-01"
    assert card.spm == 6.0
    assert len(card.position_in) == 5

def test_gibbs_rod_wave_solution() -> None:
    N = 50
    t = np.linspace(0, 10.0, N)
    u_s = list(50.0 * (1.0 - np.cos(2 * np.pi * 0.1 * t)))
    F_s = list(15000.0 + 5000.0 * np.sin(2 * np.pi * 0.1 * t))

    res = calculate_gibbs_downhole_card(
        surface_position_in=u_s,
        surface_load_lbs=F_s,
        spm=6.0,
        pump_depth_ft=3000.0,
        rod_diameter_in=0.875
    )

    assert "downhole_position_in" in res
    assert "downhole_load_lbs" in res
    assert res["plunger_stroke_in"] > 0.0

def test_card_area_and_power() -> None:
    u = [0.0, 100.0, 100.0, 0.0, 0.0]
    F = [10000.0, 10000.0, 20000.0, 20000.0, 10000.0]

    area = calculate_card_area_in_lbs(u, F)
    assert area > 0.0

def test_pump_fillage_fraction() -> None:
    u_p = list(np.linspace(0, 100, 100))
    F_p = [5000.0]*20 + [18000.0]*50 + [5000.0]*30

    fillage = calculate_pump_fillage_fraction(list(float(x) for x in u_p), F_p)
    assert 0.0 <= fillage <= 1.0

def test_pattern_classification() -> None:
    pattern_normal = classify_dynamometer_pattern(0.92, 20000.0, 10000.0, 10000.0)
    assert pattern_normal == "NORMAL"

    pattern_pound = classify_dynamometer_pattern(0.55, 20000.0, 10000.0, 10000.0)
    assert pattern_pound == "FLUID_POUND"

def test_equipment_limits_and_overload_detection() -> None:
    limits = EquipmentLimitsConfig(max_pprl_lbs=25000.0, max_gearbox_torque_in_lbs=320000.0)
    res = evaluate_equipment_limits(pprl_lbs=28000.0, mprl_lbs=10000.0, spm=6.0, stroke_length_in=100.0, limits_config=limits)

    assert res["is_equipment_overloaded"]
    assert any("PPRL" in r for r in res["overload_reasons"])

def test_full_card_analysis() -> None:
    N = 40
    u_s = list(float(x) for x in np.linspace(0, 100, N))
    F_s = list(float(x) for x in (15000.0 + 5000.0 * np.sin(np.linspace(0, 2*np.pi, N))))
    u_d = list(float(x) for x in np.linspace(0, 90, N))
    F_d = list(float(x) for x in (12000.0 + 4000.0 * np.sin(np.linspace(0, 2*np.pi, N))))

    diag = analyze_dynamometer_card(
        well_id="BW-01",
        surface_position_in=u_s,
        surface_load_lbs=F_s,
        downhole_position_in=u_d,
        downhole_load_lbs=F_d,
        spm=6.0,
        stroke_length_in=100.0
    )

    assert diag.well_id == "BW-01"
    assert 0.0 <= diag.pump_fillage_fraction <= 1.0
