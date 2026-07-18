"""Tests for operational/status datapoints added from the 5578 final tables."""

from __future__ import annotations

import pytest

from trovis_modbus import StorageStatus, Trovis557x


def test_storage_status_enum_matches_firmware_values() -> None:
    assert tuple(map(int, StorageStatus)) == tuple(range(7))


def test_heating_circuit_stride_patterns() -> None:
    device = Trovis557x(unit=None)  # type: ignore[arg-type]

    hc1 = device.heating_circuit_1
    hc2 = device.heating_circuit_2
    hc3 = device.heating_circuit_3

    assert hc1._address(hc1._bit_fields["valve_closing"]) == 61
    assert hc2._address(hc2._bit_fields["valve_closing"]) == 63
    assert hc3._address(hc3._bit_fields["valve_closing"]) == 65

    assert hc1._address(hc1._register_fields["fixed_setpoint_day"]) == 1041
    assert hc2._address(hc2._register_fields["fixed_setpoint_day"]) == 1241
    assert hc3._address(hc3._register_fields["fixed_setpoint_day"]) == 1441

    assert hc1._address(hc1._bit_fields["room_setpoint_control_autonomous"]) == 121
    assert hc2._address(hc2._bit_fields["room_setpoint_control_autonomous"]) == 122
    assert hc3._address(hc3._bit_fields["room_setpoint_control_autonomous"]) == 123


def test_hot_water_special_setpoint_is_distinct_from_active_setpoint() -> None:
    device = Trovis557x(unit=None)  # type: ignore[arg-type]
    hot_water = device.hot_water

    assert hot_water._address(hot_water._register_fields["setpoint_active"]) == 1807
    assert hot_water._address(hot_water._register_fields["special_setpoint"]) == 1808
    assert hot_water.ebene_coils["special_setpoint"] == (112, 0)


def test_new_writable_fields_have_expected_limits() -> None:
    device = Trovis557x(unit=None)  # type: ignore[arg-type]

    fixed = device.heating_circuit_1.require_metadata_for("fixed_setpoint_day")
    assert fixed.writable is True
    assert fixed.number is not None
    assert fixed.number.min_value == -5
    assert fixed.number.max_value == 130
    assert fixed.number.step == pytest.approx(0.1)

    special = device.hot_water.require_metadata_for("special_setpoint")
    assert special.writable is True
    assert special.number is not None
    assert special.number.min_value == 5
    assert special.number.max_value == 90
    assert special.number.step == pytest.approx(0.1)
