import pytest
from pydantic import ValidationError
from datetime import datetime
from backend.app.schemas.domain import Well, ReservoirProperties, FluidPVT, CSSCycle, ProductionDaily, SRPTelemetry, Constraints

def test_well_schema_valid() -> None:
    well = Well(
        well_id="W-101",
        coordinates=(27.5, 71.5),
        depth=1200.0,
        deviation=0.0,
        completion="cased_hole",
        perforations=[(1100.0, 1120.0)],
        tubing_id=0.076,
        casing_id=0.152
    )
    assert well.well_id == "W-101"
    assert well.depth == 1200.0

def test_well_schema_invalid_depth() -> None:
    with pytest.raises(ValidationError):
        Well(
            well_id="W-101",
            coordinates=(27.5, 71.5),
            depth=-100.0,  # invalid
            deviation=0.0,
            completion="cased_hole",
            perforations=[(1100.0, 1120.0)],
            tubing_id=0.076,
            casing_id=0.152
        )

def test_reservoir_properties_valid() -> None:
    props = ReservoirProperties(
        net_pay=15.0,
        porosity=0.25,
        permeability=500.0,
        pressure=3000000.0,
        temperature=320.0,
        sw=0.3
    )
    assert props.porosity == 0.25

def test_css_cycle_chronology() -> None:
    # Injection ends after it starts
    cycle = CSSCycle(
        well_id="W-101",
        cycle_number=1,
        injection_start=datetime(2023, 1, 1),
        injection_end=datetime(2023, 1, 15),
        steam_cwe=5000.0,
        steam_quality=0.8,
        steam_pressure=4000000.0,
        steam_temperature=523.15,
        soak_start=datetime(2023, 1, 15),
        soak_end=datetime(2023, 1, 20),
        production_restart=datetime(2023, 1, 20)
    )
    assert cycle.cycle_number == 1

def test_css_cycle_invalid_chronology() -> None:
    with pytest.raises(ValidationError):
        CSSCycle(
            well_id="W-101",
            cycle_number=1,
            injection_start=datetime(2023, 1, 15),
            injection_end=datetime(2023, 1, 1), # End before start
            steam_cwe=5000.0,
            steam_quality=0.8,
            steam_pressure=4000000.0,
            steam_temperature=523.15,
            soak_start=datetime(2023, 1, 15),
            soak_end=datetime(2023, 1, 20),
            production_restart=datetime(2023, 1, 20)
        )

def test_constraints_schema() -> None:
    constraint = Constraints(
        parameter="max_injection_pressure",
        lower_limit=0.0,
        upper_limit=8000000.0,
        unit="Pa",
        source="Engineering Limits Doc v1",
        approval_date=datetime(2023, 1, 1).date(),
        well_applicability=["W-101"]
    )
    assert constraint.upper_limit == 8000000.0
