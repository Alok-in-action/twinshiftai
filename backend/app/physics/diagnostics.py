"""
Dynamometer Card Diagnostics and Equipment Limit Validation Engine.
"""

import math
from typing import Any

import numpy as np

from backend.app.schemas.dynamometer import DiagnosticMetrics, EquipmentLimitsConfig


def calculate_card_area_in_lbs(position_in: list[float], load_lbs: list[float]) -> float:
    """Calculates enclosed area of a dynamometer card (in-lbs) using Shoelace/Trapezoidal integration."""
    if len(position_in) != len(load_lbs) or len(position_in) < 3:
        return 0.0

    x = np.array(position_in, dtype=float)
    y = np.array(load_lbs, dtype=float)
    
    # Polygon enclosed area via trapezoidal integration around closed curve
    area = 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))
    return float(area)

def calculate_pump_fillage_fraction(downhole_position_in: list[float], downhole_load_lbs: list[float]) -> float:
    """
    Estimates pump fillage fraction (0.0 to 1.0) from downhole dynamometer card load pickup/dropoff points.
    """
    if len(downhole_position_in) < 4:
        return 1.0

    pos = np.array(downhole_position_in, dtype=float)
    load = np.array(downhole_load_lbs, dtype=float)
    
    stroke = np.max(pos) - np.min(pos)
    if stroke <= 0:
        return 0.0

    min_load = np.min(load)
    max_load = np.max(load)
    load_range = max_load - min_load

    if load_range <= 0:
        return 1.0

    # Threshold for load transfer completion during upstroke
    threshold = min_load + 0.5 * load_range
    high_load_mask = load > threshold

    if not np.any(high_load_mask):
        return 0.5

    high_load_positions = pos[high_load_mask]
    loaded_stroke = np.max(high_load_positions) - np.min(high_load_positions)

    fillage = loaded_stroke / stroke
    return max(0.0, min(1.0, float(fillage)))

def classify_dynamometer_pattern(fillage_fraction: float, pprl_lbs: float, mprl_lbs: float, load_range_lbs: float) -> str:
    """Classifies downhole card shape pattern into engineering diagnostic categories."""
    if mprl_lbs < 1000.0:
        return "ROD_FLOATING"
    elif fillage_fraction < 0.65:
        return "FLUID_POUND"
    elif fillage_fraction < 0.85:
        return "GAS_INTERFERENCE"
    elif load_range_lbs > 15000.0:
        return "HIGH_DRAG"
    else:
        return "NORMAL"

def evaluate_equipment_limits(
    pprl_lbs: float,
    mprl_lbs: float,
    spm: float,
    stroke_length_in: float,
    rod_diameter_in: float = 0.875,
    limits_config: EquipmentLimitsConfig | None = None
) -> dict[str, Any]:
    """
    Evaluates equipment operating parameters against structural, gearbox, and rod endurance limits.
    """
    if limits_config is None:
        limits_config = EquipmentLimitsConfig()

    rod_area_in2 = (math.pi / 4.0) * (rod_diameter_in ** 2)
    max_rod_stress_psi = pprl_lbs / rod_area_in2 if rod_area_in2 > 0 else 0.0

    # Peak Torque approximation: Peak Torque ~ (PPRL - MPRL) * Stroke / 4
    peak_gearbox_torque_in_lbs = (pprl_lbs - mprl_lbs) * (stroke_length_in / 4.0)

    # Rod-floating margin
    rod_floating_margin_lbs = mprl_lbs

    overload_reasons: list[str] = []
    is_overloaded = False

    if pprl_lbs > limits_config.max_pprl_lbs:
        is_overloaded = True
        overload_reasons.append(f"PPRL ({pprl_lbs:.0f} lbs) exceeds structural rating ({limits_config.max_pprl_lbs:.0f} lbs)")

    if peak_gearbox_torque_in_lbs > limits_config.max_gearbox_torque_in_lbs:
        is_overloaded = True
        overload_reasons.append(f"Peak Torque ({peak_gearbox_torque_in_lbs:.0f} in-lbs) exceeds gearbox rating ({limits_config.max_gearbox_torque_in_lbs:.0f} in-lbs)")

    if max_rod_stress_psi > limits_config.max_rod_stress_psi:
        is_overloaded = True
        overload_reasons.append(f"Max rod stress ({max_rod_stress_psi:.0f} psi) exceeds allowable limit ({limits_config.max_rod_stress_psi:.0f} psi)")

    if rod_floating_margin_lbs < limits_config.min_rod_floating_margin_lbs:
        is_overloaded = True
        overload_reasons.append(f"Rod floating margin ({rod_floating_margin_lbs:.0f} lbs) below safety minimum ({limits_config.min_rod_floating_margin_lbs:.0f} lbs)")

    return {
        "is_equipment_overloaded": is_overloaded,
        "overload_reasons": overload_reasons,
        "max_rod_stress_psi": float(max_rod_stress_psi),
        "peak_gearbox_torque_in_lbs": float(peak_gearbox_torque_in_lbs),
        "rod_floating_margin_lbs": float(rod_floating_margin_lbs)
    }

def analyze_dynamometer_card(
    well_id: str,
    surface_position_in: list[float],
    surface_load_lbs: list[float],
    downhole_position_in: list[float],
    downhole_load_lbs: list[float],
    spm: float,
    stroke_length_in: float,
    limits_config: EquipmentLimitsConfig | None = None
) -> DiagnosticMetrics:
    """
    Full Phase 2 diagnostic suite performing fillage estimation, card area, horsepower,
    pattern classification, and equipment limit evaluation.
    """
    if limits_config is None:
        limits_config = EquipmentLimitsConfig()

    card_area = calculate_card_area_in_lbs(downhole_position_in, downhole_load_lbs)
    
    # Indicated hydraulic HP = (Area [in-lbs] * SPM) / 396000
    indicated_hp = (card_area * spm) / 396000.0

    fillage = calculate_pump_fillage_fraction(downhole_position_in, downhole_load_lbs)

    pprl = float(np.max(surface_load_lbs)) if surface_load_lbs else 0.0
    mprl = float(np.min(surface_load_lbs)) if surface_load_lbs else 0.0
    load_range = pprl - mprl

    pattern = classify_dynamometer_pattern(fillage, pprl, mprl, load_range)
    eq_eval = evaluate_equipment_limits(pprl, mprl, spm, stroke_length_in, limits_config=limits_config)

    return DiagnosticMetrics(
        well_id=well_id,
        pump_fillage_fraction=fillage,
        card_area_in_lbs=card_area,
        indicated_hydraulic_power_hp=indicated_hp,
        pprl_lbs=pprl,
        mprl_lbs=mprl,
        peak_gearbox_torque_in_lbs=eq_eval["peak_gearbox_torque_in_lbs"],
        rod_floating_margin_lbs=eq_eval["rod_floating_margin_lbs"],
        card_pattern=pattern,
        is_equipment_overloaded=eq_eval["is_equipment_overloaded"],
        overload_reasons=eq_eval["overload_reasons"]
    )
