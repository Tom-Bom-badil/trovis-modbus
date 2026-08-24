"""Tests for operational/status datapoints added from the 5578 final tables."""

from __future__ import annotations

import pytest

from trovis_modbus import (
    OUTDOOR_TEMPERATURES,
    BufferTankCircuit,
    BufferTankStatus,
    HeatingCircuitControlMode,
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

    assert rk1._address(rk1.declared_fields["valve_closing"]) == 61
    assert rk2._address(rk2.declared_fields["valve_closing"]) == 63
    assert rk3._address(rk3.declared_fields["valve_closing"]) == 65

    assert rk1._address(rk1.declared_fields["fixed_setpoint_day"]) == 1041
    assert rk2._address(rk2.declared_fields["fixed_setpoint_day"]) == 1241
    assert rk3._address(rk3.declared_fields["fixed_setpoint_day"]) == 1441

    assert rk1._address(rk1.declared_fields["trovis_5570_room_control_unit"]) == 702
    assert rk2._address(rk2.declared_fields["trovis_5570_room_control_unit"]) == 703
    assert rk3._address(rk3.declared_fields["trovis_5570_room_control_unit"]) == 704

    assert rk1._address(rk1.declared_fields["four_point_outdoor_temperature_1"]) == 1012
    assert rk2._address(rk2.declared_fields["four_point_outdoor_temperature_1"]) == 1212
    assert rk3._address(rk3.declared_fields["four_point_outdoor_temperature_1"]) == 1412
    assert (
        rk1._address(rk1.declared_fields["four_point_return_flow_temperature_4"])
        == 1027
    )
    assert (
        rk2._address(rk2.declared_fields["four_point_return_flow_temperature_4"])
        == 1227
    )
    assert (
        rk3._address(rk3.declared_fields["four_point_return_flow_temperature_4"])
        == 1427
    )

    assert rk1._address(rk1.declared_fields["room_setpoint_control_autonomous"]) == 121
    assert rk2._address(rk2.declared_fields["room_setpoint_control_autonomous"]) == 122
    assert rk3._address(rk3.declared_fields["room_setpoint_control_autonomous"]) == 123


def test_return_characteristic_parameters_are_writable() -> None:
    """Expose PA P11 to P14 as writable return-flow configuration."""
    device = Trovis557x(unit=None)  # type: ignore[arg-type]

    for circuit in (device.rk1, device.rk2, device.rk3):
        for field in (
            "return_flow_gradient",
            "return_flow_level",
            "return_flow_base_point",
            "maximum_return_flow_temperature",
        ):
            descriptor = circuit.declared_fields[field]
            metadata = circuit.require_metadata_for(field)

            assert descriptor.writable
            assert metadata.writable is True


def test_heating_circuit_outdoor_sensor_function_selectors() -> None:
    device = Trovis557x(unit=None)  # type: ignore[arg-type]
    functions = device.functions

    assert (
        functions._address(
            functions.declared_fields["heating_circuit_1_outdoor_sensor_enabled"]
        )
        == 1025
    )
    assert (
        functions._address(
            functions.declared_fields["heating_circuit_2_outdoor_sensor_enabled"]
        )
        == 1225
    )
    assert (
        functions._address(
            functions.declared_fields["heating_circuit_3_outdoor_sensor_enabled"]
        )
        == 1425
    )

    assert device.heating_circuit_uses_outdoor_sensor(1) is None
    with pytest.raises(ValueError, match="Rk4 is not available"):
        device.heating_circuit_uses_outdoor_sensor(4)


def test_heating_circuit_four_point_function_selectors() -> None:
    device = Trovis557x(unit=None)  # type: ignore[arg-type]
    functions = device.functions

    for index, address in ((1, 1034), (2, 1234), (3, 1434)):
        field = f"heating_circuit_{index}_four_point_characteristic_enabled"
        assert functions._address(functions.declared_fields[field]) == address

    assert device.heating_circuit_uses_four_point_characteristic(1) is None
    with pytest.raises(ValueError, match="Rk4 is not available"):
        device.heating_circuit_uses_four_point_characteristic(4)


async def test_gradient_heating_and_return_curves(trovis: Trovis557x) -> None:
    """Calculate flow and return curves for the gradient characteristic."""
    await trovis.async_update()

    operating_mode = trovis.heating_circuit_operating_mode(1)
    assert operating_mode is HeatingCircuitControlMode.HEATING_CURVE

    flow_curve = trovis.rk1.heating_curve(operating_mode=operating_mode)
    night_flow_curve = trovis.rk1.heating_curve(
        mode="night",
        operating_mode=operating_mode,
    )
    return_curve = trovis.rk1.heating_curve(
        operating_mode=operating_mode,
        curve="return",
    )
    day_return_curve = trovis.rk1.heating_curve(
        mode="day",
        operating_mode=operating_mode,
        curve="return",
    )
    night_return_curve = trovis.rk1.heating_curve(
        mode="night",
        operating_mode=operating_mode,
        curve="return",
    )

    assert flow_curve is not None
    assert night_flow_curve is not None
    assert return_curve is not None
    assert day_return_curve is not None
    assert night_return_curve is not None
    assert return_curve == day_return_curve
    assert day_return_curve != night_return_curve
    assert len(flow_curve) == len(OUTDOOR_TEMPERATURES) == 41
    assert len(return_curve) == len(night_return_curve) == 41
    assert flow_curve[0] == pytest.approx(78.32)
    assert flow_curve[20] == pytest.approx(57.08)
    assert flow_curve[-1] == pytest.approx(26.4)
    assert night_flow_curve[0] == pytest.approx(71.12)
    assert night_flow_curve[20] == pytest.approx(49.88)
    assert night_flow_curve[-1] == pytest.approx(20.0)
    assert return_curve[0] == pytest.approx(55.0)
    assert return_curve[20] == pytest.approx(47.3)
    assert return_curve[-1] == pytest.approx(33.0)
    assert night_return_curve[0] == pytest.approx(54.2)
    assert night_return_curve[20] == pytest.approx(44.3)
    assert night_return_curve[-1] == pytest.approx(30.0)


async def test_equal_return_base_and_max_produce_fixed_limit(
    trovis: Trovis557x,
    mock_modbus_unit,  # noqa: ANN001
) -> None:
    """Use a constant return limit when P13 and P14 are equal."""
    mock_modbus_unit.holding[1010] = 500  # HR41011 / P14 -> 50.0 °C
    mock_modbus_unit.holding[1011] = 500  # HR41012 / P13 -> 50.0 °C
    await trovis.async_update()

    operating_mode = trovis.heating_circuit_operating_mode(1)
    assert operating_mode is HeatingCircuitControlMode.HEATING_CURVE
    return_curve = trovis.rk1.heating_curve(
        operating_mode=operating_mode,
        curve="return",
    )
    night_return_curve = trovis.rk1.heating_curve(
        mode="night",
        operating_mode=operating_mode,
        curve="return",
    )
    assert return_curve == night_return_curve == [50.0] * len(OUTDOOR_TEMPERATURES)


async def test_fixed_setpoint_heating_and_return_curves(
    trovis: Trovis557x,
    mock_modbus_unit,  # noqa: ANN001
) -> None:
    """Return constant flow and return curves for fixed set point control."""
    mock_modbus_unit.coils[1025] = False
    await trovis.async_update()

    operating_mode = trovis.heating_circuit_operating_mode(1)
    assert operating_mode is HeatingCircuitControlMode.FIXED_SETPOINT

    flow_curve = trovis.rk1.heating_curve(operating_mode=operating_mode)
    night_flow_curve = trovis.rk1.heating_curve(
        mode="night",
        operating_mode=operating_mode,
    )
    return_curve = trovis.rk1.heating_curve(
        operating_mode=operating_mode,
        curve="return",
    )
    day_return_curve = trovis.rk1.heating_curve(
        mode="day",
        operating_mode=operating_mode,
        curve="return",
    )
    night_return_curve = trovis.rk1.heating_curve(
        mode="night",
        operating_mode=operating_mode,
        curve="return",
    )

    assert flow_curve == [60.0] * 41
    assert night_flow_curve == [50.0] * 41
    assert return_curve == day_return_curve == night_return_curve == [45.0] * 41


async def test_four_point_heating_and_return_curves(
    trovis: Trovis557x,
    mock_modbus_unit,  # noqa: ANN001
) -> None:
    """Interpolate the active four-point characteristics with flat ends."""
    mock_modbus_unit.coils[1034] = True
    await trovis.async_update()

    operating_mode = trovis.heating_circuit_operating_mode(1)
    assert operating_mode is HeatingCircuitControlMode.FOUR_POINT

    flow_curve = trovis.rk1.heating_curve(operating_mode=operating_mode)
    night_flow_curve = trovis.rk1.heating_curve(
        mode="night",
        operating_mode=operating_mode,
    )
    return_curve = trovis.rk1.heating_curve(
        operating_mode=operating_mode,
        curve="return",
    )
    day_return_curve = trovis.rk1.heating_curve(
        mode="day",
        operating_mode=operating_mode,
        curve="return",
    )
    night_return_curve = trovis.rk1.heating_curve(
        mode="night",
        operating_mode=operating_mode,
        curve="return",
    )

    assert flow_curve is not None
    assert night_flow_curve is not None
    assert return_curve is not None
    assert flow_curve[0] == pytest.approx(70.0)
    assert flow_curve[5] == pytest.approx(70.0)
    assert flow_curve[-1] == pytest.approx(25.0)
    assert night_flow_curve[0] == pytest.approx(60.0)
    assert night_flow_curve[5] == pytest.approx(60.0)
    assert night_flow_curve[-1] == pytest.approx(20.0)
    assert return_curve == day_return_curve == night_return_curve == [65.0] * 41


async def test_four_point_curve_rejects_invalid_outdoor_axis(
    trovis: Trovis557x,
    mock_modbus_unit,  # noqa: ANN001
) -> None:
    """Report a calculation error for duplicate or unordered outdoor points."""
    mock_modbus_unit.coils[1034] = True
    mock_modbus_unit.holding[1013] = 0xFF6A  # P2 duplicates P1 (-15.0 °C)
    await trovis.async_update()

    operating_mode = trovis.heating_circuit_operating_mode(1)
    assert operating_mode is HeatingCircuitControlMode.FOUR_POINT
    assert trovis.rk1.heating_curve(operating_mode=operating_mode) is None
    assert (
        trovis.rk1.heating_curve(
            operating_mode=operating_mode,
            curve="return",
        )
        is None
    )


def test_four_point_characteristic_fields_have_expected_limits() -> None:
    device = Trovis557x(unit=None)  # type: ignore[arg-type]
    rk1 = device.rk1

    expected_ranges = {
        "four_point_outdoor_temperature_1": (-50, 50),
        "four_point_flow_temperature_day_1": (-5, 150),
        "four_point_flow_temperature_night_1": (-5, 150),
        "four_point_return_flow_temperature_1": (5, 90),
    }
    for field, (minimum, maximum) in expected_ranges.items():
        metadata = rk1.require_metadata_for(field)
        assert metadata.writable is True
        assert metadata.number is not None
        assert metadata.number.min_value == minimum
        assert metadata.number.max_value == maximum
        assert metadata.number.step == 1


def test_domestic_hot_water_special_setpoint_is_distinct_from_active_setpoint() -> None:
    device = Trovis557x(unit=None)  # type: ignore[arg-type]
    rk4 = device.rk4

    assert rk4._address(rk4.declared_fields["setpoint_active"]) == 1807
    assert rk4._address(rk4.declared_fields["special_setpoint"]) == 1808
    assert rk4.ebene_coils["special_setpoint"] == (112, 0)


def test_new_writable_fields_have_expected_limits() -> None:
    device = Trovis557x(unit=None)  # type: ignore[arg-type]

    fixed = device.rk1.require_metadata_for("fixed_setpoint_day")
    assert fixed.writable is True
    assert fixed.number is not None
    assert fixed.number.min_value == -5
    assert fixed.number.max_value == 130
    assert fixed.number.step == 1

    special = device.rk4.require_metadata_for("special_setpoint")
    assert special.writable is True
    assert special.number is not None
    assert special.number.min_value == 5
    assert special.number.max_value == 90
    assert fixed.number.step == 1


def test_legacy_gap_registers_and_intermediate_heating_points() -> None:
    device = Trovis557x(unit=None)  # type: ignore[arg-type]

    controller = device.controller
    rk4 = device.rk4

    assert controller._address(controller.declared_fields["special_functions"]) == 4

    overrun = rk4.require_metadata_for("storage_tank_charging_pump_lag_factor")
    assert (
        rk4._address(rk4.declared_fields["storage_tank_charging_pump_lag_factor"])
        == 1804
    )
    assert overrun.writable is True
    assert overrun.number is not None
    assert overrun.number.min_value == pytest.approx(0.1)
    assert overrun.number.max_value == pytest.approx(10.0)
    assert overrun.number.step == pytest.approx(0.1)

    assert (
        rk4._address(rk4.declared_fields["intermediate_heating_function_enabled"])
        == 406
    )

    disinfection = rk4.require_metadata_for("disinfection_enabled")
    assert rk4._address(rk4.declared_fields["disinfection_enabled"]) == 413
    assert disinfection.writable is True

    assert rk4._address(rk4.declared_fields["intermediate_heating_operation"]) == 1830


def test_additional_5578_sensor_addresses() -> None:
    sensors = Sensors(unit=None)  # type: ignore[arg-type]

    assert sensors._address(sensors.declared_fields["af2"]) == 10
    assert sensors._address(sensors.declared_fields["sf3"]) == 24
    assert sensors._address(sensors.declared_fields["ae1"]) == 25
    assert sensors._address(sensors.declared_fields["fg1"]) == 25
    assert sensors._address(sensors.declared_fields["ae2"]) == 26
    assert sensors._address(sensors.declared_fields["fg2"]) == 26
    assert sensors._address(sensors.declared_fields["ae3"]) == 27
    assert sensors._address(sensors.declared_fields["fg3"]) == 27
    assert sensors._address(sensors.declared_fields["pulse_rate"]) == 28
    assert sensors._address(sensors.declared_fields["analog_input_voltage"]) == 41
    assert sensors._address(sensors.declared_fields["analog_input_current"]) == 41

    assert "ae1_fg1" not in sensors.declared_fields
    assert "ae2_fg2" not in sensors.declared_fields
    assert "ae3_fg3" not in sensors.declared_fields

    for field in ("ae1", "ae2", "ae3"):
        metadata = sensors.require_metadata_for(field)
        assert metadata.number is not None
        assert metadata.number.min_value == pytest.approx(-5)
        assert metadata.number.max_value == pytest.approx(2000)
        assert metadata.number.raw_min == -50
        assert metadata.number.raw_max == 20000
        assert metadata.number.step == pytest.approx(0.1)
        assert metadata.number.unit is None

    for field in ("fg1", "fg2", "fg3"):
        metadata = sensors.require_metadata_for(field)
        assert metadata.number is not None
        # Keep the canonical register descriptor at scale 0.1. Trovis557x
        # applies the role-aware conversion for resistance remotes (x10 -> ohms).
        assert metadata.number.min_value == pytest.approx(-5)
        assert metadata.number.max_value == pytest.approx(2000)
        assert metadata.number.raw_min == -50
        assert metadata.number.raw_max == 20000
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
    assert controller._address(controller.declared_fields["glt_timeout_active"]) == 158

    assert (
        controller._address(
            controller.declared_fields["summer_outdoor_temperature_average"]
        )
        == 42
    )


def test_solar_circuit_uses_dedicated_register_and_coil_block() -> None:
    solar = SolarCircuit(unit=None)  # type: ignore[arg-type]

    assert (
        solar._address(solar.declared_fields["pump_on_temperature_difference"]) == 1809
    )
    assert (
        solar._address(solar.declared_fields["pump_off_temperature_difference"]) == 1810
    )
    assert solar._address(solar.declared_fields["maximum_storage_temperature"]) == 1811
    assert solar._address(solar.declared_fields["operating_hours"]) == 1812
    assert solar._address(solar.declared_fields["pump_running"]) == 1807

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

    assert "solar_operating_hours" not in device.rk4.declared_fields
    assert "solar_circuit_pump_running" not in device.rk4.declared_fields
    assert "operating_hours" in device.solar.declared_fields
    assert "pump_running" in device.solar.declared_fields


def test_buffer_tank_status_enum_matches_firmware_values() -> None:
    assert tuple(map(int, BufferTankStatus)) == tuple(range(7))


def test_buffer_tank_circuit_uses_rk1_extension_registers() -> None:
    buffer_tank = BufferTankCircuit(unit=None)  # type: ignore[arg-type]

    assert (
        buffer_tank._address(buffer_tank.declared_fields["minimum_charging_setpoint"])
        == 1099
    )
    assert (
        buffer_tank._address(buffer_tank.declared_fields["charging_end_temperature"])
        == 1100
    )
    assert (
        buffer_tank._address(buffer_tank.declared_fields["charging_temperature_boost"])
        == 1101
    )
    assert (
        buffer_tank._address(buffer_tank.declared_fields["charging_pump_lag_factor"])
        == 1102
    )
    assert buffer_tank._address(buffer_tank.declared_fields["status"]) == 1103

    minimum = buffer_tank.require_metadata_for("minimum_charging_setpoint")
    assert minimum.writable is True
    assert minimum.number is not None
    assert minimum.number.min_value == pytest.approx(0.0)
    assert minimum.number.max_value == pytest.approx(90.0)
    assert minimum.number.step == 1

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

    assert set(device.buffer_tank.declared_fields).isdisjoint(
        device.rk1.declared_fields
    )
