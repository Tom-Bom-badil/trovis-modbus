"""Manufacturer range metadata tests."""

from __future__ import annotations

from datetime import date, time

import pytest

from trovis_modbus import MonthDay, Trovis557x


@pytest.mark.parametrize(
    ("component_name", "field", "minimum", "maximum", "raw_min", "raw_max"),
    [
        ("controller", "summer_outside_limit", 0, 30, 0, 300),
        ("controller", "outside_delay", 1, 6, 10, 60),
        ("controller", "frost_limit", -15, 3, -150, 30),
        ("heating_circuit_1", "flow_min", -5, 150, -50, 1500),
        ("heating_circuit_1", "flow_max", 5, 150, 50, 1500),
        ("heating_circuit_1", "return_max", 5, 90, 50, 900),
        ("hot_water", "hysteresis", 0, 30, 0, 300),
        ("hot_water", "charge_overshoot", 0, 50, 0, 500),
        ("hot_water", "max_charge_temp", 0, 90, 0, 900),
        ("hot_water", "return_max", 5, 90, 50, 900),
        ("hot_water", "disinfection_temp", 60, 90, 600, 900),
    ],
)
def test_number_ranges_from_reference_data(
    trovis: Trovis557x,
    component_name: str,
    field: str,
    minimum: float | int,
    maximum: float | int,
    raw_min: float | int,
    raw_max: float | int,
) -> None:
    component = getattr(trovis, component_name)
    metadata = component.require_metadata_for(field)

    assert metadata.number is not None
    assert metadata.number.min_value == minimum
    assert metadata.number.max_value == maximum
    assert metadata.number.raw_min == raw_min
    assert metadata.number.raw_max == raw_max


def test_corrected_hot_water_setpoint_limits(trovis: Trovis557x) -> None:
    for field in ("setpoint_min", "setpoint_max"):
        metadata = trovis.hot_water.require_metadata_for(field)
        assert metadata.number is not None
        assert metadata.number.min_value == 5
        assert metadata.number.max_value == 90
        assert metadata.number.raw_min == 50
        assert metadata.number.raw_max == 900


def test_outside_delay_uses_hardware_verified_scale(
    trovis: Trovis557x,
) -> None:
    field = trovis.controller._register_fields["outside_delay"]

    assert field.decode([30]) == pytest.approx(3.0)
    assert field.encode(3) == [30]


def test_all_writable_numbers_have_complete_ranges(trovis: Trovis557x) -> None:
    for component in trovis.components:
        for field in component._register_fields:
            metadata = component.require_metadata_for(field)
            if metadata.value_kind != "number" or not metadata.writable:
                continue

            assert metadata.number is not None
            assert metadata.number.min_value is not None, field
            assert metadata.number.max_value is not None, field
            assert metadata.number.step is not None, field
            assert metadata.number.raw_min is not None, field
            assert metadata.number.raw_max is not None, field


def test_all_writable_temporal_values_have_complete_ranges(
    trovis: Trovis557x,
) -> None:
    expected_types = {
        "date": date,
        "time": time,
        "month_day": MonthDay,
    }

    for component in trovis.components:
        for field in component._register_fields:
            metadata = component.require_metadata_for(field)
            expected_type = expected_types.get(metadata.value_kind)
            if expected_type is None or not metadata.writable:
                continue

            assert metadata.temporal is not None
            assert isinstance(metadata.temporal.min_value, expected_type), field
            assert isinstance(metadata.temporal.max_value, expected_type), field
            assert metadata.temporal.raw_min is not None, field
            assert metadata.temporal.raw_max is not None, field
