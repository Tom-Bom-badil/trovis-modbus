"""Tests for operational/status datapoints added from the 5578 final tables."""

from __future__ import annotations

import pytest

from trovis_modbus import StorageStatus, Trovis557x


def test_storage_status_enum_matches_firmware_values() -> None:
    assert tuple(map(int, StorageStatus)) == tuple(range(7))


def test_heating_circuit_stride_patterns() -> None:
    device = Trovis557x(unit=None)  # type: ignore[arg-type]

    hk1 = device.hk1
    hk2 = device.hk2
    hk3 = device.hk3

    assert hk1._address(hk1._bit_fields["valve_closing"]) == 61
    assert hk2._address(hk2._bit_fields["valve_closing"]) == 63
    assert hk3._address(hk3._bit_fields["valve_closing"]) == 65

    assert hk1._address(hk1._register_fields["fixed_setpoint_day"]) == 1041
    assert hk2._address(hk2._register_fields["fixed_setpoint_day"]) == 1241
    assert hk3._address(hk3._register_fields["fixed_setpoint_day"]) == 1441

    assert hk1._address(hk1._bit_fields["room_setpoint_control_autonomous"]) == 121
    assert hk2._address(hk2._bit_fields["room_setpoint_control_autonomous"]) == 122
    assert hk3._address(hk3._bit_fields["room_setpoint_control_autonomous"]) == 123


def test_domestic_hot_water_special_setpoint_is_distinct_from_active_setpoint() -> None:
    device = Trovis557x(unit=None)  # type: ignore[arg-type]
    ww = device.ww

    assert ww._address(ww._register_fields["setpoint_active"]) == 1807
    assert ww._address(ww._register_fields["special_setpoint"]) == 1808
    assert ww.ebene_coils["special_setpoint"] == (112, 0)


def test_new_writable_fields_have_expected_limits() -> None:
    device = Trovis557x(unit=None)  # type: ignore[arg-type]

    fixed = device.hk1.require_metadata_for("fixed_setpoint_day")
    assert fixed.writable is True
    assert fixed.number is not None
    assert fixed.number.min_value == -5
    assert fixed.number.max_value == 130
    assert fixed.number.step == pytest.approx(0.1)

    special = device.ww.require_metadata_for("special_setpoint")
    assert special.writable is True
    assert special.number is not None
    assert special.number.min_value == 5
    assert special.number.max_value == 90
    assert special.number.step == pytest.approx(0.1)


def test_legacy_gap_registers_and_intermediate_heating_points() -> None:
    device = Trovis557x(unit=None)  # type: ignore[arg-type]

    controller = device.controller
    ww = device.ww

    assert controller._address(controller._register_fields["special_functions"]) == 4

    overrun = ww.require_metadata_for("storage_tank_charging_pump_lag_factor")
    assert (
        ww._address(ww._register_fields["storage_tank_charging_pump_lag_factor"])
        == 1804
    )
    assert overrun.writable is True
    assert overrun.number is not None
    assert overrun.number.min_value == pytest.approx(0.1)
    assert overrun.number.max_value == pytest.approx(10.0)
    assert overrun.number.step == pytest.approx(0.1)

    assert ww._address(ww._bit_fields["intermediate_heating_function_enabled"]) == 406
    assert ww._address(ww._bit_fields["intermediate_heating_operation"]) == 1830


def test_additional_5578_sensor_addresses() -> None:
    device = Trovis557x(unit=None)  # type: ignore[arg-type]
    sensors = device.sensors

    assert sensors._address(sensors._register_fields["af2"]) == 10
    assert sensors._address(sensors._register_fields["ruef4"]) == 10
    assert sensors._address(sensors._register_fields["sf3"]) == 24
    assert sensors._address(sensors._register_fields["ae1"]) == 25
    assert sensors._address(sensors._register_fields["fg1"]) == 25
    assert sensors._address(sensors._register_fields["ae2"]) == 26
    assert sensors._address(sensors._register_fields["fg2"]) == 26
    assert sensors._address(sensors._register_fields["ae3"]) == 27
    assert sensors._address(sensors._register_fields["fg3"]) == 27
    assert sensors._address(sensors._register_fields["pulse_rate"]) == 28
    assert sensors._address(sensors._register_fields["analog_input_voltage"]) == 41
    assert sensors._address(sensors._register_fields["analog_input_current"]) == 41

    assert "ae1_fg1" not in sensors._register_fields
    assert "ae2_fg2" not in sensors._register_fields
    assert "ae3_fg3" not in sensors._register_fields

    for field in ("ae1", "fg1", "ae2", "fg2", "ae3", "fg3"):
        metadata = sensors.require_metadata_for(field)
        assert metadata.number is not None
        assert metadata.number.min_value == pytest.approx(-5)
        assert metadata.number.max_value == pytest.approx(2000)
        assert metadata.number.step == pytest.approx(0.1)
        assert metadata.number.unit is None

    current = sensors.require_metadata_for("analog_input_current")
    assert current.number is not None
    assert current.number.min_value == 0
    assert current.number.max_value == 20
    assert current.number.step == pytest.approx(0.1)
    assert current.number.unit == "mA"


def test_controller_monitoring_metadata_and_timeout() -> None:
    device = Trovis557x(unit=None)  # type: ignore[arg-type]
    controller = device.controller

    deviation = controller.require_metadata_for("temperature_monitoring_deviation")
    assert deviation.writable is True
    assert deviation.number is not None
    assert deviation.number.min_value == 1
    assert deviation.number.max_value == 30
    assert deviation.number.step == pytest.approx(0.1)
    assert deviation.number.unit == "K"

    window = controller.require_metadata_for("temperature_monitoring_window")
    assert window.writable is True
    assert window.number is not None
    assert window.number.min_value == 1
    assert window.number.max_value == 120
    assert window.number.unit == "min"

    timeout = controller.require_metadata_for("glt_timeout_active")
    assert timeout.writable is True
    assert controller._address(controller._bit_fields["glt_timeout_active"]) == 158

    assert (
        controller._address(
            controller._register_fields["summer_outdoor_temperature_average"]
        )
        == 42
    )
