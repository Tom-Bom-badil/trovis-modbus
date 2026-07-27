"""Tests for shared TROVIS settings descriptors."""

from __future__ import annotations

import pytest
from modbus_connection.mock import MockModbusUnit

from trovis_modbus import Functions, Parameters, Trovis557x


def test_functions_and_parameters_are_public() -> None:
    assert Functions.__name__ == "Functions"
    assert Parameters.__name__ == "Parameters"


async def test_shared_functions_and_parameters(trovis: Trovis557x) -> None:
    await trovis.async_update()

    assert trovis.functions.input_01_is_binary is False
    assert trovis.functions.input_02_is_binary is True
    assert trovis.functions.input_03_is_binary is False
    assert trovis.functions.input_15_is_binary is False
    assert trovis.functions.input_16_is_binary is True
    assert trovis.functions.input_17_is_binary is False
    assert trovis.functions.pulse_input_enabled is False
    assert trovis.functions.storage_sensor_2_enabled is False
    assert trovis.functions.flow_sensor_2_enabled is False
    assert trovis.functions.flow_sensor_4_enabled_cl405 is False
    assert trovis.functions.flow_sensor_4_enabled_cl1829 is False
    assert trovis.functions.flow_sensor_4_enabled is False
    assert trovis.functions.analog_setpoint_correction_enabled is True
    assert trovis.functions.buffer_storage_bottom_sensor_enabled is False

    assert trovis.functions.input_is_binary(1) is False
    assert trovis.functions.input_is_binary(2) is True
    with pytest.raises(KeyError):
        trovis.functions.input_is_binary(7)

    assert trovis.parameters.analog_input_selection == 5
    assert trovis.parameters.selected_analog_inputs == (1, 3)
    assert trovis.parameters.storage_tank_charging_pump_sensor_input == 15


def test_three_circuit_ranges_select_all_known_co8_inputs(
    mock_modbus_unit: MockModbusUnit,
) -> None:
    device = Trovis557x(mock_modbus_unit, model=5579)

    assert device.functions.readable_input_numbers == (
        1,
        2,
        3,
        4,
        5,
        6,
        9,
        10,
        11,
        12,
        13,
        15,
        16,
        17,
    )
    assert device.functions.is_field_readable("pulse_input_enabled")
    assert device.functions.is_field_readable("storage_sensor_2_enabled")
    assert device.functions.is_field_readable("flow_sensor_2_enabled")
    assert device.functions.is_field_readable("flow_sensor_4_enabled_cl405")
    assert device.functions.is_field_readable("flow_sensor_4_enabled_cl1829")
    assert device.functions.is_field_readable("buffer_storage_bottom_sensor_enabled")
    assert device.parameters.is_field_readable("analog_input_selection")
    assert device.parameters.is_field_readable(
        "storage_tank_charging_pump_sensor_input"
    )


async def test_two_circuit_ranges_filter_unavailable_fields(
    mock_modbus_unit: MockModbusUnit,
) -> None:
    mock_modbus_unit.holding.update({2001: 7, 2002: 17})
    mock_modbus_unit.coils.update(
        {
            401: True,
            404: False,
            800: False,
            801: True,
            802: True,
            906: False,
            1828: True,
        }
    )
    device = Trovis557x(mock_modbus_unit, model=5573)

    assert device.functions.readable_input_numbers == (1, 2)
    assert device.functions.is_field_readable("input_01_is_binary")
    assert device.functions.is_field_readable("input_02_is_binary")
    assert not device.functions.is_field_readable("input_03_is_binary")
    # CL139 is in the shared 2-HC address range, but 5573 has no IMP variant.
    assert device.functions.is_field_readable("pulse_input_enabled")
    assert device.functions.is_field_readable("storage_sensor_2_enabled")
    assert device.functions.is_field_readable("flow_sensor_2_enabled")
    assert device.functions.is_field_readable("flow_sensor_4_enabled_cl405")
    assert device.functions.is_field_readable("flow_sensor_4_enabled_cl1829")
    assert not device.functions.is_field_readable(
        "buffer_storage_bottom_sensor_enabled"
    )
    assert not device.parameters.is_field_readable("analog_input_selection")
    assert not device.parameters.is_field_readable(
        "storage_tank_charging_pump_sensor_input"
    )

    await device.async_update()

    assert device.functions.input_01_is_binary is False
    assert device.functions.input_02_is_binary is True
    assert device.functions.input_03_is_binary is None
    assert device.functions.pulse_input_enabled is False
    assert device.functions.storage_sensor_2_enabled is True
    assert device.functions.flow_sensor_2_enabled is False
    assert device.functions.flow_sensor_4_enabled is True
    assert device.parameters.analog_input_selection is None
    assert device.parameters.selected_analog_inputs == ()

    # Metadata remains available for the globally declared datapoint even when
    # the current model range excludes it from reads.
    metadata = device.parameters.require_metadata_for("analog_input_selection")
    assert metadata.number is not None
    assert metadata.number.min_value == 1
    assert metadata.number.max_value == 7
