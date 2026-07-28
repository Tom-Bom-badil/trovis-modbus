"""Configuration-only sensor-variant resolver tests."""

from __future__ import annotations

import pytest
from modbus_connection.mock import MockModbusUnit

from trovis_modbus import SensorVariantStatus, Trovis557x, resolve_sensor_variants
from trovis_modbus.configurations import (
    TROVIS_5573,
    TROVIS_5573_1,
    TROVIS_5578,
    TROVIS_5578_E,
    TROVIS_5579,
    get_model_definition_for_reported_model,
)

from .conftest import COILS, HOLDING


async def _updated_device(
    unit: MockModbusUnit,
    *,
    model: int,
    holding: dict[int, int] | None = None,
    coils: dict[int, bool] | None = None,
) -> Trovis557x:
    unit.holding.update(HOLDING)
    unit.coils.update(COILS)
    if holding:
        unit.holding.update(holding)
    if coils:
        unit.coils.update(coils)
    device = Trovis557x(unit, model=model)
    await device.async_update()
    return device


def test_reported_model_lookup_is_unique() -> None:
    assert get_model_definition_for_reported_model(5573) is TROVIS_5573
    assert get_model_definition_for_reported_model(55731) is TROVIS_5573_1
    assert get_model_definition_for_reported_model(5578) is TROVIS_5578
    assert get_model_definition_for_reported_model(55781) is TROVIS_5578_E
    assert get_model_definition_for_reported_model(5579) is TROVIS_5579


def test_unknown_reported_model_is_rejected() -> None:
    with pytest.raises(KeyError, match="unsupported reported TROVIS model"):
        get_model_definition_for_reported_model(9999)


@pytest.mark.asyncio
async def test_5579_resolves_fg3_from_f25_and_analog_selector(
    mock_modbus_unit: MockModbusUnit,
) -> None:
    device = await _updated_device(
        mock_modbus_unit,
        model=5579,
        holding={2001: 5579, 2002: 5579},
        coils={904: False, 2124: False},
    )
    resolution = device.sensor_variant_resolution

    for sensor_key in ("sf2", "rf2", "vf2", "vf3", "vf4", "fg1"):
        result = resolution.result_for(sensor_key)
        assert result is not None
        assert result.status is SensorVariantStatus.RESOLVED
        assert result.selected_sensor_key == sensor_key

    fg2 = resolution.result_for("fg2")
    assert fg2 is not None
    assert fg2.status is SensorVariantStatus.INACTIVE

    input_17 = resolution.result_for("sf3")
    assert input_17 is not None
    assert input_17.status is SensorVariantStatus.RESOLVED
    assert input_17.selected_sensor_key == "fg3"
    assert input_17.candidate_sensor_keys == ("fg3",)
    assert ("buffer_tank_bottom_sensor_enabled", False) in input_17.evidence
    assert ("analog_setpoint_correction_enabled", False) in input_17.evidence


@pytest.mark.asyncio
async def test_5579_keeps_voltage_current_unresolved_in_analog_mode(
    mock_modbus_unit: MockModbusUnit,
) -> None:
    device = await _updated_device(
        mock_modbus_unit,
        model=5579,
        coils={904: True, 2124: False},
    )
    result = device.sensor_variant_resolution.result_for("sf3")

    assert result is not None
    assert result.status is SensorVariantStatus.UNRESOLVED
    assert result.candidate_sensor_keys == (
        "analog_input_voltage",
        "analog_input_current",
    )


@pytest.mark.asyncio
async def test_binary_mode_disables_complete_multi_role_input(
    mock_modbus_unit: MockModbusUnit,
) -> None:
    device = await _updated_device(
        mock_modbus_unit,
        model=5579,
        coils={816: True},
    )
    result = device.sensor_variant_resolution.result_for("sf3")

    assert result is not None
    assert result.status is SensorVariantStatus.INACTIVE
    assert result.candidate_sensor_keys == ()


@pytest.mark.asyncio
async def test_5578_resolves_fg3_when_sf3_function_is_inactive(
    mock_modbus_unit: MockModbusUnit,
) -> None:
    device = await _updated_device(mock_modbus_unit, model=5578, coils={2124: False})
    result = device.sensor_variant_resolution.result_for("sf3")

    assert result is not None
    assert result.status is SensorVariantStatus.RESOLVED
    assert result.selected_sensor_key == "fg3"


@pytest.mark.asyncio
async def test_5578_resolves_sf3_when_f25_is_enabled(
    mock_modbus_unit: MockModbusUnit,
) -> None:
    device = await _updated_device(mock_modbus_unit, model=5578, coils={2124: True})
    result = device.sensor_variant_resolution.result_for("sf3")

    assert result is not None
    assert result.status is SensorVariantStatus.RESOLVED
    assert result.selected_sensor_key == "sf3"


@pytest.mark.asyncio
async def test_5578_e_keeps_multi_role_inputs_open_until_selector_is_verified(
    mock_modbus_unit: MockModbusUnit,
) -> None:
    device = await _updated_device(mock_modbus_unit, model=55781)
    resolution = device.sensor_variant_resolution

    ae1 = resolution.result_for("ae1")
    assert ae1 is not None
    assert ae1.status is SensorVariantStatus.UNRESOLVED
    assert ae1.candidate_sensor_keys == ("ae1", "fg1")

    ae2 = resolution.result_for("ae2")
    assert ae2 is not None
    assert ae2.status is SensorVariantStatus.INACTIVE

    ae3 = resolution.result_for("ae3")
    assert ae3 is not None
    assert ae3.status is SensorVariantStatus.UNRESOLVED
    assert ae3.candidate_sensor_keys == ("ae3", "fg3")


@pytest.mark.asyncio
@pytest.mark.parametrize("model", (5573, 55731))
async def test_5573_family_resolves_sf_rf_and_default_vf3(
    mock_modbus_unit: MockModbusUnit,
    model: int,
) -> None:
    device = await _updated_device(
        mock_modbus_unit,
        model=model,
        coils={401: False, 404: False, 906: False, 1828: False},
    )
    resolution = device.sensor_variant_resolution

    sf2_rf2 = resolution.result_for("sf2")
    assert sf2_rf2 is not None
    assert sf2_rf2.status is SensorVariantStatus.RESOLVED
    assert sf2_rf2.selected_sensor_key == "rf2"

    vf2_vf3_vf4 = resolution.result_for("vf2")
    assert vf2_vf3_vf4 is not None
    assert vf2_vf3_vf4.status is SensorVariantStatus.RESOLVED
    assert vf2_vf3_vf4.selected_sensor_key == "vf3"

    fg1 = resolution.result_for("fg1")
    assert fg1 is not None
    assert fg1.status is SensorVariantStatus.RESOLVED
    assert fg1.selected_sensor_key == "fg1"

    fg2 = resolution.result_for("fg2")
    assert fg2 is not None
    assert fg2.status is SensorVariantStatus.INACTIVE


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("coils", "expected"),
    (
        ({906: True, 404: False, 1828: False}, "vf2"),
        ({906: True, 404: True, 1828: True}, "vf2"),
        ({906: False, 404: True, 1828: False}, "vf4"),
        ({906: False, 404: False, 1828: True}, "vf4"),
        ({906: False, 404: False, 1828: False}, "vf3"),
    ),
)
async def test_5573_family_resolves_vf2_vf3_vf4(
    mock_modbus_unit: MockModbusUnit,
    coils: dict[int, bool],
    expected: str,
) -> None:
    device = await _updated_device(
        mock_modbus_unit,
        model=5573,
        coils=coils,
    )
    result = device.sensor_variant_resolution.result_for("vf2")

    assert result is not None
    assert result.status is SensorVariantStatus.RESOLVED
    assert result.selected_sensor_key == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("sf2_enabled", "expected"),
    ((True, "sf2"), (False, "rf2")),
)
async def test_5573_family_resolves_sf2_or_rf2(
    mock_modbus_unit: MockModbusUnit,
    sf2_enabled: bool,
    expected: str,
) -> None:
    device = await _updated_device(
        mock_modbus_unit,
        model=5573,
        coils={401: sf2_enabled},
    )
    result = device.sensor_variant_resolution.result_for("sf2")

    assert result is not None
    assert result.status is SensorVariantStatus.RESOLVED
    assert result.selected_sensor_key == expected


@pytest.mark.asyncio
@pytest.mark.parametrize("model", (5575, 5576, 5578, 55781, 5579))
async def test_documented_models_resolve_imp_when_fb10_is_enabled(
    mock_modbus_unit: MockModbusUnit,
    model: int,
) -> None:
    device = await _updated_device(
        mock_modbus_unit,
        model=model,
        coils={138: True},
    )
    result = device.sensor_variant_resolution.result_for("pulse_rate")

    assert result is not None
    assert result.status is SensorVariantStatus.RESOLVED
    assert result.selected_sensor_key == "pulse_rate"
    assert ("pulse_input_enabled", True) in result.evidence


@pytest.mark.asyncio
async def test_fb10_pulse_selection_takes_precedence_over_co8_binary_mode(
    mock_modbus_unit: MockModbusUnit,
) -> None:
    device = await _updated_device(
        mock_modbus_unit,
        model=5579,
        coils={138: True, 816: True},
    )
    result = device.sensor_variant_resolution.result_for("pulse_rate")

    assert result is not None
    assert result.status is SensorVariantStatus.RESOLVED
    assert result.selected_sensor_key == "pulse_rate"


@pytest.mark.asyncio
@pytest.mark.parametrize("model", (5573, 55731))
async def test_5573_family_has_no_imp_variant(
    mock_modbus_unit: MockModbusUnit,
    model: int,
) -> None:
    device = await _updated_device(
        mock_modbus_unit,
        model=model,
        coils={138: True},
    )

    assert device.sensor_variant_resolution.result_for("pulse_rate") is None


def test_unavailable_selector_stays_unresolved_instead_of_being_guessed() -> None:
    class FunctionsWithoutValues:
        @staticmethod
        def input_is_binary(input_number: int) -> None:
            return None

    class ParametersWithoutValues:
        pass

    resolution = resolve_sensor_variants(
        TROVIS_5578,
        FunctionsWithoutValues(),
        ParametersWithoutValues(),
    )
    result = resolution.result_for("rf2")

    assert result is not None
    assert result.status is SensorVariantStatus.UNRESOLVED
    assert result.selected_sensor_key is None
