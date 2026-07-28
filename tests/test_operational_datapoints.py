"""Tests for operational/status datapoints added from the 5578 final tables."""

from __future__ import annotations

import pytest

from trovis_modbus import (
    BufferTankCircuit,
    BufferTankStatus,
    Sensors,
    SolarCircuit,
    StorageStatus,
    Trovis557x,
)


def test_storage_status_enum_matches_firmware_values() -> None:
    assert tuple(map(int, StorageStatus)) == tuple(range(7))


def test_heating_circuit_stride_patterns() -> None:
    device = Trovis557x(unit=None)  # type: ignore[arg-type]

    rk1 = device.rk1
    rk2 = device.rk2
    rk3 = device.rk3

    assert rk1._address(rk1._bit_fields["valve_closing"]) == 61
    assert rk2._address(rk2._bit_fields["valve_closing"]) == 63
    assert rk3._address(rk3._bit_fields["valve_closing"]) == 65

    assert rk1._address(rk1._register_fields["fixed_setpoint_day"]) == 1041
    assert rk2._address(rk2._register_fields["fixed_setpoint_day"]) == 1241
    assert rk3._address(rk3._register_fields["fixed_setpoint_day"]) == 1441

    assert rk1._address(rk1._bit_fields["room_setpoint_control_autonomous"]) == 121
    assert rk2._address(rk2._bit_fields["room_setpoint_control_autonomous"]) == 122
    assert rk3._address(rk3._bit_fields["room_setpoint_control_autonomous"]) == 123


def test_domestic_hot_water_special_setpoint_is_distinct_from_active_setpoint() -> None:
    device = Trovis557x(unit=None)  # type: ignore[arg-type]
    rk4 = device.rk4

    assert rk4._address(rk4._register_fields["setpoint_active"]) == 1807
    assert rk4._address(rk4._register_fields["special_setpoint"]) == 1808
    assert rk4.ebene_coils["special_setpoint"] == (112, 0)


def test_new_writable_fields_have_expected_limits() -> None:
    device = Trovis557x(unit=None)  # type: ignore[arg-type]

    fixed = device.rk1.require_metadata_for("fixed_setpoint_day")
    assert fixed.writable is True
    assert fixed.number is not None
    assert fixed.number.min_value == -5
    assert fixed.number.max_value == 130
    assert fixed.number.step == pytest.approx(0.1)

    special = device.rk4.require_metadata_for("special_setpoint")
    assert special.writable is True
    assert special.number is not None
    assert special.number.min_value == 5
    assert special.number.max_value == 90
    assert special.number.step == pytest.approx(0.1)


def test_legacy_gap_registers_and_intermediate_heating_points() -> None:
    device = Trovis557x(unit=None)  # type: ignore[arg-type]

    controller = device.controller
    rk4 = device.rk4

    assert controller._address(controller._register_fields["special_functions"]) == 4

    overrun = rk4.require_metadata_for("storage_tank_charging_pump_lag_factor")
    assert (
        rk4._address(rk4._register_fields["storage_tank_charging_pump_lag_factor"])
        == 1804
    )
    assert overrun.writable is True
    assert overrun.number is not None
    assert overrun.number.min_value == pytest.approx(0.1)
    assert overrun.number.max_value == pytest.approx(10.0)
    assert overrun.number.step == pytest.approx(0.1)

    assert rk4._address(rk4._bit_fields["intermediate_heating_function_enabled"]) == 406
    assert rk4._address(rk4._bit_fields["intermediate_heating_operation"]) == 1830


def test_additional_5578_sensor_addresses() -> None:
    sensors = Sensors(unit=None)  # type: ignore[arg-type]

    assert sensors._address(sensors._register_fields["af2"]) == 10
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


def test_solar_circuit_uses_dedicated_register_and_coil_block() -> None:
    solar = SolarCircuit(unit=None)  # type: ignore[arg-type]

    assert (
        solar._address(solar._register_fields["pump_on_temperature_difference"]) == 1809
    )
    assert (
        solar._address(solar._register_fields["pump_off_temperature_difference"])
        == 1810
    )
    assert solar._address(solar._register_fields["maximum_storage_temperature"]) == 1811
    assert solar._address(solar._register_fields["operating_hours"]) == 1812
    assert solar._address(solar._bit_fields["pump_running"]) == 1807

    pump_on = solar.require_metadata_for("pump_on_temperature_difference")
    assert pump_on.writable is True
    assert pump_on.number is not None
    assert pump_on.number.min_value == pytest.approx(1.0)
    assert pump_on.number.max_value == pytest.approx(30.0)
    assert pump_on.number.unit == "K"

    pump_off = solar.require_metadata_for("pump_off_temperature_difference")
    assert pump_off.writable is True
    assert pump_off.number is not None
    assert pump_off.number.min_value == pytest.approx(0.0)
    assert pump_off.number.max_value == pytest.approx(30.0)
    assert pump_off.number.unit == "K"

    maximum_storage = solar.require_metadata_for("maximum_storage_temperature")
    assert maximum_storage.writable is True
    assert maximum_storage.number is not None
    assert maximum_storage.number.min_value == pytest.approx(20.0)
    assert maximum_storage.number.max_value == pytest.approx(90.0)


def test_solar_datapoints_are_no_longer_owned_by_rk4() -> None:
    device = Trovis557x(unit=None)  # type: ignore[arg-type]

    assert "solar_operating_hours" not in device.rk4._register_fields
    assert "solar_circuit_pump_running" not in device.rk4._bit_fields
    assert "operating_hours" in device.solar._register_fields
    assert "pump_running" in device.solar._bit_fields


def test_buffer_tank_status_enum_matches_firmware_values() -> None:
    assert tuple(map(int, BufferTankStatus)) == tuple(range(7))


def test_buffer_tank_circuit_uses_rk1_extension_registers() -> None:
    buffer_tank = BufferTankCircuit(unit=None)  # type: ignore[arg-type]

    assert (
        buffer_tank._address(buffer_tank._register_fields["minimum_charging_setpoint"])
        == 1099
    )
    assert (
        buffer_tank._address(buffer_tank._register_fields["charging_end_temperature"])
        == 1100
    )
    assert (
        buffer_tank._address(buffer_tank._register_fields["charging_temperature_boost"])
        == 1101
    )
    assert (
        buffer_tank._address(buffer_tank._register_fields["charging_pump_lag_factor"])
        == 1102
    )
    assert buffer_tank._address(buffer_tank._register_fields["status"]) == 1103

    minimum = buffer_tank.require_metadata_for("minimum_charging_setpoint")
    assert minimum.writable is True
    assert minimum.number is not None
    assert minimum.number.min_value == pytest.approx(0.0)
    assert minimum.number.max_value == pytest.approx(90.0)
    assert minimum.number.step == pytest.approx(0.1)

    end = buffer_tank.require_metadata_for("charging_end_temperature")
    assert end.writable is True
    assert end.number is not None
    assert end.number.min_value == pytest.approx(0.0)
    assert end.number.max_value == pytest.approx(90.0)

    boost = buffer_tank.require_metadata_for("charging_temperature_boost")
    assert boost.writable is True
    assert boost.number is not None
    assert boost.number.min_value == pytest.approx(0.0)
    assert boost.number.max_value == pytest.approx(50.0)
    assert boost.number.unit == "K"

    lag = buffer_tank.require_metadata_for("charging_pump_lag_factor")
    assert lag.writable is True
    assert lag.number is not None
    assert lag.number.min_value == pytest.approx(0.0)
    assert lag.number.max_value == pytest.approx(10.0)
    assert lag.number.step == pytest.approx(0.1)


def test_buffer_tank_extension_does_not_duplicate_rk1_fields() -> None:
    device = Trovis557x(unit=None)  # type: ignore[arg-type]

    assert set(device.buffer_tank._register_fields).isdisjoint(
        device.rk1._register_fields
    )
