import pytest
from datetime import datetime
import json
import os

from backend.app.physics.units import (
    convert_to_si,
    lbs_to_newtons,
    newtons_to_lbs,
    in_to_m,
    m_to_in,
    cp_to_pas,
    pas_to_cp,
    api_to_density,
    UnitConversionError
)
from backend.app.schemas.well import WellAndCompletionGeometry
from backend.app.schemas.reservoir import ReservoirProperties
from backend.app.schemas.fluid import FluidPVTProperties, ViscosityPoint
from backend.app.schemas.css import CSSCycleRecord
from backend.app.schemas.production import ProductionTimeSeries
from backend.app.schemas.steam import SteamInjectionTelemetry
from backend.app.schemas.telemetry import SRPVFDTelemetry
from backend.app.schemas.dynamometer import DynamometerCardData
from backend.app.schemas.equipment import EquipmentSpecifications, RodSectionSpec
from backend.app.schemas.limits import ApprovedOperatingConstraints, WellOperatingLimits
from backend.app.quality.safety import check_optimization_prerequisites, validate_operating_limits

def test_unit_conversions() -> None:
    # Test length conversion
    val, unit = convert_to_si(100.0, "inch", "length")
    assert abs(val - 2.54) < 1e-4
    assert unit == "m"

    # Test pressure conversion
    val, unit = convert_to_si(100.0, "psi", "pressure")
    assert abs(val - 689.476) < 1e-2
    assert unit == "kPa"

    # Test force conversions
    n = lbs_to_newtons(1000.0)
    assert abs(n - 4448.22) < 1.0
    lbs = newtons_to_lbs(n)
    assert abs(lbs - 1000.0) < 1e-2

    # Test viscosity conversions
    assert cp_to_pas(1000.0) == 1.0
    assert pas_to_cp(1.0) == 1000.0

    # Test API gravity density
    density = api_to_density(18.0)  # Baghewala crude ~17-19 °API
    assert 940.0 < density < 960.0

    # Test invalid unit error handling
    with pytest.raises(UnitConversionError):
        convert_to_si(10.0, "invalid_unit_string", "length")

def test_pydantic_schemas_valid() -> None:
    well = WellAndCompletionGeometry(
        well_id="BW-01",
        measured_depth_m=1200.0,
        true_vertical_depth_m=1200.0,
        casing_outer_diameter_m=0.1778,
        tubing_inner_diameter_m=0.076,
        pump_depth_m=1100.0,
        perforation_top_m=1150.0,
        perforation_bottom_m=1180.0
    )
    assert well.well_id == "BW-01"

    fluid = FluidPVTProperties(
        well_id="BW-01",
        oil_api_gravity=18.0,
        water_specific_gravity=1.05,
        gas_specific_gravity=0.65,
        andrade_coeff_a=None,
        andrade_coeff_b=None,
        viscosity_table=[
            ViscosityPoint(temperature_c=48.0, viscosity_cp=5000.0),
            ViscosityPoint(temperature_c=100.0, viscosity_cp=150.0)
        ]
    )
    assert len(fluid.viscosity_table) == 2

    card = DynamometerCardData(
        well_id="BW-01",
        card_id="CARD-001",
        timestamp=datetime.now(),
        card_type="surface",
        stroke_length_in=100.0,
        spm=6.0,
        position_in=[0.0, 50.0, 100.0, 50.0, 0.0],
        load_lbs=[5000.0, 18000.0, 20000.0, 12000.0, 5000.0],
        downhole_position_in=None,
        downhole_load_lbs=None,
        num_samples=5
    )
    assert card.card_type == "surface"

def test_optimization_prerequisites_blocking() -> None:
    limits = ApprovedOperatingConstraints(
        limits_version="1.0.0",
        approved_by="Test Lead",
        well_limits=WellOperatingLimits(
            max_peak_polished_rod_load_lbs=25000.0,
            min_polished_rod_load_lbs=2000.0,
            max_spm=10.0,
            min_spm=2.0,
            max_stroke_length_in=120.0,
            min_stroke_length_in=60.0,
            max_steam_injection_rate_m3d=100.0,
            max_steam_pressure_kpa=10000.0,
            max_steam_temperature_c=300.0,
            max_goodman_stress_ratio=0.9,
            min_rod_floating_margin_lbs=500.0
        ),
        required_parameters=["well_id", "pump_depth_m", "crank_radius_m"]
    )

    # Complete well configuration
    complete_well = {
        "well_id": "BW-01",
        "pump_depth_m": 1100.0,
        "crank_radius_m": 1.5
    }
    is_ready, missing = check_optimization_prerequisites(complete_well, limits)
    assert is_ready is True
    assert len(missing) == 0

    # Incomplete well configuration (missing crank_radius_m)
    incomplete_well = {
        "well_id": "BW-01",
        "pump_depth_m": 1100.0
    }
    is_ready, missing = check_optimization_prerequisites(incomplete_well, limits)
    assert is_ready is False
    assert len(missing) == 1
    assert "Missing required parameter: crank_radius_m" in missing[0]

def test_constraint_validation() -> None:
    limits = ApprovedOperatingConstraints(
        limits_version="1.0.0",
        approved_by="Test Lead",
        well_limits=WellOperatingLimits(
            max_peak_polished_rod_load_lbs=25000.0,
            min_polished_rod_load_lbs=2000.0,
            max_spm=10.0,
            min_spm=2.0,
            max_stroke_length_in=120.0,
            min_stroke_length_in=60.0,
            max_steam_injection_rate_m3d=100.0,
            max_steam_pressure_kpa=10000.0,
            max_steam_temperature_c=300.0,
            max_goodman_stress_ratio=0.9,
            min_rod_floating_margin_lbs=500.0
        ),
        required_parameters=["well_id"]
    )

    valid_controls = {
        "spm": 6.0,
        "stroke_length_in": 100.0,
        "predicted_pprl_lbs": 20000.0
    }
    feasible, violations = validate_operating_limits(valid_controls, limits)
    assert feasible is True
    assert len(violations) == 0

    invalid_controls = {
        "spm": 15.0,  # Exceeds max 10.0
        "predicted_pprl_lbs": 30000.0  # Exceeds max 25000.0
    }
    feasible, violations = validate_operating_limits(invalid_controls, limits)
    assert feasible is False
    assert len(violations) == 2
