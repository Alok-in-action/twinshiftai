"""
Safety and Quality Engine for Operating Constraints and Advisory Controls.

Non-Negotiable Safety Rules:
1. Software is human-in-the-loop advisory ONLY.
2. Refuse optimization when required limits or essential field parameters are absent.
3. Every recommendation must be verified by an independent post-solve feasibility check.
"""

from typing import Any

from backend.app.schemas.limits import ApprovedOperatingConstraints


class OptimizationRefusalException(Exception):
    """Raised when optimization is refused due to missing constraints or parameters."""

def check_optimization_prerequisites(
    well_config: dict[str, Any],
    limits_config: ApprovedOperatingConstraints
) -> tuple[bool, list[str]]:
    """
    Verifies that all required parameters and approved operating limits are present before running optimization.

    Returns:
        (is_ready: bool, missing_or_invalid_fields: List[str])
    """
    missing_fields = []
    
    # Verify required parameters in well configuration
    for req_param in limits_config.required_parameters:
        if req_param not in well_config or well_config[req_param] is None:
            missing_fields.append(f"Missing required parameter: {req_param}")

    # Verify well limits are valid
    wl = limits_config.well_limits
    if wl.max_peak_polished_rod_load_lbs <= wl.min_polished_rod_load_lbs:
        missing_fields.append("Invalid rod load limits: max must be greater than min")
    if wl.max_spm <= wl.min_spm:
        missing_fields.append("Invalid SPM limits: max must be greater than min")

    is_ready = len(missing_fields) == 0
    return is_ready, missing_fields

def validate_operating_limits(
    candidate_controls: dict[str, Any],
    limits_config: ApprovedOperatingConstraints
) -> tuple[bool, list[str]]:
    """
    Independent post-solve constraint validator. Checks candidate controls against approved operating bounds.

    Returns:
        (is_feasible: bool, violations: List[str])
    """
    violations = []
    wl = limits_config.well_limits

    spm = candidate_controls.get("spm")
    if spm is not None and (spm < wl.min_spm or spm > wl.max_spm):
        violations.append(f"SPM {spm} outside allowed bounds [{wl.min_spm}, {wl.max_spm}]")

    stroke_len = candidate_controls.get("stroke_length_in")
    if stroke_len is not None and (stroke_len < wl.min_stroke_length_in or stroke_len > wl.max_stroke_length_in):
        violations.append(f"Stroke length {stroke_len}in outside allowed bounds [{wl.min_stroke_length_in}, {wl.max_stroke_length_in}]")

    steam_rate = candidate_controls.get("steam_injection_rate_m3d")
    if steam_rate is not None and (steam_rate < 0 or steam_rate > wl.max_steam_injection_rate_m3d):
        violations.append(f"Steam injection rate {steam_rate} m³/d exceeds max limit {wl.max_steam_injection_rate_m3d}")

    steam_press = candidate_controls.get("steam_pressure_kpa")
    if steam_press is not None and (steam_press < 0 or steam_press > wl.max_steam_pressure_kpa):
        violations.append(f"Steam pressure {steam_press} kPa exceeds max limit {wl.max_steam_pressure_kpa}")

    pprl = candidate_controls.get("predicted_pprl_lbs")
    if pprl is not None and (pprl > wl.max_peak_polished_rod_load_lbs):
        violations.append(f"Predicted PPRL {pprl} lbs exceeds max limit {wl.max_peak_polished_rod_load_lbs}")

    mprl = candidate_controls.get("predicted_mprl_lbs")
    if mprl is not None and (mprl < wl.min_polished_rod_load_lbs):
        violations.append(f"Predicted MPRL {mprl} lbs below min limit {wl.min_polished_rod_load_lbs}")

    is_feasible = len(violations) == 0
    return is_feasible, violations
