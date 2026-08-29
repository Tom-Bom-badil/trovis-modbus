"""Tests for the parameter-driven TROVIS heating-curve calculator."""

from __future__ import annotations

import pytest

from trovis_modbus import Trovis557x, utils
from trovis_modbus.enums import HeatingCircuitControlMode
from trovis_modbus.heating_curve import (
    HeatingCurveParameters,
    calculate_heating_curve,
)


def _parameters(**overrides: object) -> HeatingCurveParameters:
    values: dict[str, object] = {
        "day_active": True,
        "minimum_flow_temperature": 20.0,
        "maximum_flow_temperature": 80.0,
        "room_setpoint_day": 21.0,
        "room_setpoint_night": 18.0,
        "gradient": 1.2,
        "level": 0.0,
        "return_flow_gradient": 1.0,
        "return_flow_level": 0.0,
        "maximum_return_flow_temperature": 65.0,
        "return_flow_base_point": 45.0,
        "return_flow_temperature_setpoint": 50.0,
        "four_point_outdoor_temperature_1": -15.0,
        "four_point_outdoor_temperature_2": -5.0,
        "four_point_outdoor_temperature_3": 5.0,
        "four_point_outdoor_temperature_4": 15.0,
        "four_point_flow_temperature_day_1": 70.0,
        "four_point_flow_temperature_day_2": 55.0,
        "four_point_flow_temperature_day_3": 40.0,
        "four_point_flow_temperature_day_4": 25.0,
        "four_point_flow_temperature_night_1": 60.0,
        "four_point_flow_temperature_night_2": 45.0,
        "four_point_flow_temperature_night_3": 30.0,
        "four_point_flow_temperature_night_4": 20.0,
        "four_point_return_flow_temperature_1": 60.0,
        "four_point_return_flow_temperature_2": 50.0,
        "four_point_return_flow_temperature_3": 40.0,
        "four_point_return_flow_temperature_4": 30.0,
        "fixed_setpoint_day": 50.0,
        "fixed_setpoint_night": 35.0,
    }
    values.update(overrides)
    return HeatingCurveParameters(**values)


def test_gradient_characteristic_matches_existing_formula() -> None:
    """The pure calculator keeps the established gradient calculation."""
    parameters = _parameters()

    result = calculate_heating_curve(parameters, "day")

    assert result == utils.heating_curve(
        room_setpoint=21.0,
        slope=1.2,
        offset=0.0,
        minimum_flow_temperature=20.0,
        maximum_flow_temperature=80.0,
        base_temperature=24.0,
    )
    assert result is not None
    assert len(result) == 41
    assert result[-1] == pytest.approx(26.4)


def test_active_mode_uses_snapshot_day_state() -> None:
    """Active mode selects day/night from the snapshot instead of live I/O."""
    day_result = calculate_heating_curve(_parameters(day_active=True), "active")
    night_result = calculate_heating_curve(_parameters(day_active=False), "active")

    assert day_result == calculate_heating_curve(_parameters(), "day")
    assert night_result == calculate_heating_curve(_parameters(), "night")
    assert day_result != night_result


def test_return_gradient_characteristic_uses_return_parameters() -> None:
    """Return curves use P9/P10/P13/P14 and the common room setpoint."""
    parameters = _parameters()

    result = calculate_heating_curve(parameters, "day", curve="return")

    assert result == utils.heating_curve(
        room_setpoint=21.0,
        slope=1.0,
        offset=0.0,
        minimum_flow_temperature=45.0,
        maximum_flow_temperature=65.0,
        base_temperature=45.0,
    )


def test_fixed_setpoint_flow_is_clamped() -> None:
    """Fixed flow setpoints remain limited by min/max flow temperatures."""
    parameters = _parameters(
        fixed_setpoint_day=90.0,
        maximum_flow_temperature=80.0,
    )

    result = calculate_heating_curve(
        parameters,
        "day",
        operating_mode=HeatingCircuitControlMode.FIXED_SETPOINT,
    )

    assert result == [80.0] * 41


def test_fixed_setpoint_return_uses_effective_return_limit() -> None:
    """Fixed-setpoint return characteristic stays constant."""
    parameters = _parameters(return_flow_temperature_setpoint=52.5)

    result = calculate_heating_curve(
        parameters,
        "night",
        operating_mode=HeatingCircuitControlMode.FIXED_SETPOINT,
        curve="return",
    )

    assert result == [52.5] * 41


def test_four_point_curve_interpolates_and_clamps_flow() -> None:
    """Four-point interpolation preserves the current extrapolation/clamp rules."""
    parameters = _parameters(maximum_flow_temperature=60.0)

    result = calculate_heating_curve(
        parameters,
        "day",
        operating_mode=HeatingCircuitControlMode.FOUR_POINT,
    )

    assert result is not None
    assert len(result) == 41
    assert result[0] == 60.0  # -20 °C: first point 70 °C, clamped to max 60 °C
    assert result[20] == 47.5  # 0 °C between (-5, 55) and (5, 40)
    assert result[-1] == 25.0  # +20 °C: held at last point


def test_four_point_return_is_not_flow_clamped() -> None:
    """The return four-point curve keeps its dedicated point values."""
    parameters = _parameters(maximum_flow_temperature=40.0)

    result = calculate_heating_curve(
        parameters,
        "day",
        operating_mode=HeatingCircuitControlMode.FOUR_POINT,
        curve="return",
    )

    assert result is not None
    assert result[0] == 60.0
    assert result[-1] == 30.0


def test_four_point_rejects_unsorted_outdoor_axis() -> None:
    """Invalid four-point x axes still return None."""
    parameters = _parameters(
        four_point_outdoor_temperature_2=10.0,
        four_point_outdoor_temperature_3=5.0,
    )

    assert (
        calculate_heating_curve(
            parameters,
            "day",
            operating_mode=HeatingCircuitControlMode.FOUR_POINT,
        )
        is None
    )


def test_missing_required_value_returns_none() -> None:
    """Incomplete snapshots remain non-calculable instead of guessing values."""
    parameters = _parameters(gradient=None)

    assert calculate_heating_curve(parameters, "day") is None


async def test_live_circuit_snapshot_keeps_existing_curve_result(
    trovis: Trovis557x,
) -> None:
    """A live circuit snapshot reproduces the existing public curve result."""
    await trovis.async_update()
    circuit = trovis.rk1

    parameters = circuit.heating_curve_parameters()

    assert calculate_heating_curve(parameters) == circuit.heating_curve()
    assert calculate_heating_curve(parameters, "day") == circuit.heating_curve("day")
    assert calculate_heating_curve(parameters, "night") == circuit.heating_curve(
        "night"
    )


async def test_live_circuit_snapshot_copies_values_without_mutating_circuit(
    trovis: Trovis557x,
) -> None:
    """The snapshot contains detached values suitable for later simulation."""
    await trovis.async_update()
    circuit = trovis.rk1

    parameters = circuit.heating_curve_parameters()

    assert parameters.day_active is circuit.day_active
    assert parameters.room_setpoint_day == circuit.room_setpoint_day
    assert parameters.room_setpoint_night == circuit.room_setpoint_night
    assert parameters.gradient == circuit.gradient
    assert parameters.level == circuit.level
    assert parameters.minimum_flow_temperature == circuit.minimum_flow_temperature
    assert parameters.maximum_flow_temperature == circuit.maximum_flow_temperature
