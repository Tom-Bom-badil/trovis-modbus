"""Tests for TROVIS address ranges as field-availability maps."""

from __future__ import annotations

from trovis_modbus.configurations.address_ranges import (
    COIL_RANGES_3_RK,
    REGISTER_RANGES_3_RK,
    control_circuit_count,
    is_span_readable,
    ranges_for_model,
)


def test_span_must_fit_completely_inside_one_range() -> None:
    ranges = ((0, 5), (10, 20))

    assert is_span_readable(0, 1, ranges)
    assert is_span_readable(3, 3, ranges)
    assert is_span_readable(10, 11, ranges)
    assert not is_span_readable(5, 2, ranges)
    assert not is_span_readable(6, 1, ranges)


def test_extended_model_raw_values_use_family_ranges() -> None:
    assert ranges_for_model(55781) == (REGISTER_RANGES_3_RK, COIL_RANGES_3_RK)
    assert control_circuit_count(55781) == 3
    assert control_circuit_count(55731) == 2


def test_ranges_must_be_configured_before_read_layout(
    mock_modbus_unit,
) -> None:
    from trovis_modbus import Functions

    functions = Functions(mock_modbus_unit)
    _ = functions._read_items  # build and cache the read layout

    register_ranges, coil_ranges = ranges_for_model(5578)
    try:
        functions.configure_readable_ranges(register_ranges, coil_ranges)
    except RuntimeError as err:
        assert "before the first read layout" in str(err)
    else:
        raise AssertionError("late range configuration must fail")
