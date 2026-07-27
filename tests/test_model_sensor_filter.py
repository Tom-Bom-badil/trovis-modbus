"""Model-aware filtering of logical sensor views."""

import pytest
from modbus_connection.mock import MockModbusUnit

from trovis_modbus import SensorVariantStatus, Trovis557x

from .conftest import COILS, HOLDING


def test_5578_filters_unsupported_sensor_views(
    mock_modbus_unit: MockModbusUnit,
) -> None:
    device = Trovis557x(
        mock_modbus_unit,
        model=5578,
        detected_sensors=(
            "af1",
            "sf3",
            "fg3",
            "ae1",
            "ae2",
            "ae3",
            "analog_input_voltage",
            "analog_input_current",
            "pulse_rate",
        ),
    )

    assert device.detected_sensors == {
        "af1",
        "sf3",
        "fg3",
        "analog_input_voltage",
        "pulse_rate",
    }
    assert device.unsupported_detected_sensors == {
        "ae1",
        "ae2",
        "ae3",
        "analog_input_current",
    }
    assert {"ae1", "ae2", "ae3", "analog_input_current"}.isdisjoint(
        device.sensors.readable_field_names
    )
    assert "pulse_rate" in device.sensors.readable_field_names


def test_5579_keeps_only_its_supported_analog_views(
    mock_modbus_unit: MockModbusUnit,
) -> None:
    device = Trovis557x(
        mock_modbus_unit,
        model=5579,
        detected_sensors=(
            "sf3",
            "fg3",
            "ae1",
            "analog_input_voltage",
            "analog_input_current",
            "pulse_rate",
        ),
    )

    assert device.detected_sensors == {
        "sf3",
        "fg3",
        "analog_input_voltage",
        "analog_input_current",
        "pulse_rate",
    }
    assert device.unsupported_detected_sensors == {"ae1"}
    assert {"ae1", "ae2", "ae3"}.isdisjoint(device.sensors.readable_field_names)
    assert {
        "sf3",
        "fg3",
        "analog_input_voltage",
        "analog_input_current",
        "pulse_rate",
    } <= device.sensors.readable_field_names


@pytest.mark.asyncio
async def test_5576_exposes_valid_free_flow_sensors_without_co8_selectors(
    mock_modbus_unit: MockModbusUnit,
) -> None:
    mock_modbus_unit.holding.update(HOLDING)
    mock_modbus_unit.holding.update(
        {
            13: 310,
            14: 320,
            15: 330,
        }
    )
    mock_modbus_unit.coils.update(COILS)

    device = Trovis557x(
        mock_modbus_unit,
        model=5576,
        detected_sensors=("vf2", "vf3", "vf4"),
    )

    await device.async_update()

    for sensor_key in ("vf2", "vf3", "vf4"):
        result = device.sensor_variant_resolution.result_for(sensor_key)
        assert result is not None
        assert result.status is SensorVariantStatus.UNRESOLVED

    assert device.available_sensor_keys == {
        "vf2",
        "vf3",
        "vf4",
    }


@pytest.mark.asyncio
async def test_5578_exposes_only_fixed_and_resolved_detected_sensors(
    mock_modbus_unit: MockModbusUnit,
) -> None:
    mock_modbus_unit.holding.update(HOLDING)
    mock_modbus_unit.coils.update(COILS)
    device = Trovis557x(
        mock_modbus_unit,
        model=5578,
        detected_sensors=(
            "af1",
            "rf2",
            "fg1",
            "fg2",
            "sf3",
            "fg3",
            "analog_input_voltage",
            "pulse_rate",
        ),
    )

    await device.async_update()

    assert device.available_sensor_keys == {
        "af1",
        "rf2",
        "fg1",
        "fg3",
        "analog_input_voltage",
    }
    assert device.unresolved_detected_sensor_keys == set()
    assert device.inactive_detected_sensor_keys == {"fg2"}


@pytest.mark.asyncio
async def test_5579_exposes_fg3_when_sf3_and_analog_functions_are_inactive(
    mock_modbus_unit: MockModbusUnit,
) -> None:
    mock_modbus_unit.holding.update(HOLDING)
    mock_modbus_unit.coils.update(COILS)
    mock_modbus_unit.coils.update({904: False, 2124: False})
    device = Trovis557x(
        mock_modbus_unit,
        model=5579,
        detected_sensors=(
            "af1",
            "sf3",
            "fg3",
            "analog_input_voltage",
            "analog_input_current",
            "pulse_rate",
        ),
    )

    await device.async_update()

    assert device.available_sensor_keys == {"af1", "fg3"}
    assert device.unresolved_detected_sensor_keys == set()
