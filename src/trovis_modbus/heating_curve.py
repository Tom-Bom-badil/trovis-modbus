"""Pure heating-curve calculation helpers.

This module deliberately contains no Modbus transport or Home Assistant logic.
It exposes the TROVIS heating-curve calculation as a parameter-driven function
so callers can calculate a curve from either live controller values or an
independent simulation snapshot.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from . import utils
from .enums import HeatingCircuitControlMode


@dataclass(frozen=True, slots=True)
class HeatingCurveParameters:
    """Values required to calculate TROVIS heating characteristics."""

    day_active: bool | None

    minimum_flow_temperature: float | None
    maximum_flow_temperature: float | None
    room_setpoint_day: float | None
    room_setpoint_night: float | None
    gradient: float | None
    level: float | None

    return_flow_gradient: float | None
    return_flow_level: float | None
    maximum_return_flow_temperature: float | None
    return_flow_base_point: float | None
    return_flow_temperature_setpoint: float | None

    four_point_outdoor_temperature_1: float | None
    four_point_outdoor_temperature_2: float | None
    four_point_outdoor_temperature_3: float | None
    four_point_outdoor_temperature_4: float | None

    four_point_flow_temperature_day_1: float | None
    four_point_flow_temperature_day_2: float | None
    four_point_flow_temperature_day_3: float | None
    four_point_flow_temperature_day_4: float | None

    four_point_flow_temperature_night_1: float | None
    four_point_flow_temperature_night_2: float | None
    four_point_flow_temperature_night_3: float | None
    four_point_flow_temperature_night_4: float | None

    four_point_return_flow_temperature_1: float | None
    four_point_return_flow_temperature_2: float | None
    four_point_return_flow_temperature_3: float | None
    four_point_return_flow_temperature_4: float | None

    fixed_setpoint_day: float | None
    fixed_setpoint_night: float | None


def calculate_heating_curve(
    parameters: HeatingCurveParameters,
    mode: Literal["active", "day", "night"] = "active",
    *,
    operating_mode: HeatingCircuitControlMode = HeatingCircuitControlMode.HEATING_CURVE,
    curve: Literal["flow", "return"] = "flow",
) -> list[float] | None:
    """Calculate one TROVIS characteristic for outdoor temperatures -20..20 °C.

    ``operating_mode`` selects gradient characteristic, four-point
    characteristic, or fixed set point control. ``curve`` selects the flow or
    return characteristic. ``mode`` follows ``parameters.day_active`` for
    ``"active"`` or explicitly selects day/night.

    Returns ``None`` if a required value is missing or a four-point x-axis is
    invalid.
    """
    if mode not in ("active", "day", "night"):
        raise ValueError("mode must be 'active', 'day', or 'night'")
    if curve not in ("flow", "return"):
        raise ValueError("curve must be 'flow' or 'return'")

    day_mode = mode == "day" or (mode == "active" and parameters.day_active is True)

    if operating_mode is HeatingCircuitControlMode.FIXED_SETPOINT:
        if curve == "flow":
            value = (
                parameters.fixed_setpoint_day
                if day_mode
                else parameters.fixed_setpoint_night
            )
            minimum = parameters.minimum_flow_temperature
            maximum = parameters.maximum_flow_temperature
            if None in (value, minimum, maximum):
                return None
            fixed_value = max(minimum, min(maximum, value))
        else:
            # Without outdoor compensation, the controller exposes one
            # currently effective return-flow limit.
            fixed_value = parameters.return_flow_temperature_setpoint
            if fixed_value is None:
                return None

        return [round(fixed_value, 2) for _ in utils.OUTDOOR_TEMPERATURES]

    if operating_mode is HeatingCircuitControlMode.FOUR_POINT:
        outdoor_values = (
            parameters.four_point_outdoor_temperature_1,
            parameters.four_point_outdoor_temperature_2,
            parameters.four_point_outdoor_temperature_3,
            parameters.four_point_outdoor_temperature_4,
        )

        if curve == "flow" and day_mode:
            curve_values = (
                parameters.four_point_flow_temperature_day_1,
                parameters.four_point_flow_temperature_day_2,
                parameters.four_point_flow_temperature_day_3,
                parameters.four_point_flow_temperature_day_4,
            )
        elif curve == "flow":
            curve_values = (
                parameters.four_point_flow_temperature_night_1,
                parameters.four_point_flow_temperature_night_2,
                parameters.four_point_flow_temperature_night_3,
                parameters.four_point_flow_temperature_night_4,
            )
        else:
            curve_values = (
                parameters.four_point_return_flow_temperature_1,
                parameters.four_point_return_flow_temperature_2,
                parameters.four_point_return_flow_temperature_3,
                parameters.four_point_return_flow_temperature_4,
            )

        if any(value is None for value in (*outdoor_values, *curve_values)):
            return None

        points = list(zip(outdoor_values, curve_values, strict=True))
        if any(
            points[index][0] >= points[index + 1][0] for index in range(len(points) - 1)
        ):
            return None

        if curve == "flow":
            minimum = parameters.minimum_flow_temperature
            maximum = parameters.maximum_flow_temperature
            if minimum is None or maximum is None:
                return None

        result: list[float] = []
        for outdoor_temperature in utils.OUTDOOR_TEMPERATURES:
            if outdoor_temperature <= points[0][0]:
                value = points[0][1]
            elif outdoor_temperature >= points[-1][0]:
                value = points[-1][1]
            else:
                left, right = points[0], points[1]
                for index in range(len(points) - 1):
                    left, right = points[index], points[index + 1]
                    if left[0] <= outdoor_temperature <= right[0]:
                        break

                fraction = (outdoor_temperature - left[0]) / (right[0] - left[0])
                value = left[1] + fraction * (right[1] - left[1])

            if curve == "flow":
                value = max(minimum, min(maximum, value))

            result.append(round(value, 2))

        return result

    if operating_mode is not HeatingCircuitControlMode.HEATING_CURVE:
        raise ValueError(f"unsupported heating-circuit mode: {operating_mode}")

    if curve == "flow":
        room_setpoint = (
            parameters.room_setpoint_day if day_mode else parameters.room_setpoint_night
        )
        slope = parameters.gradient
        offset = parameters.level
        base_temperature = 24.0
        minimum = parameters.minimum_flow_temperature
        maximum = parameters.maximum_flow_temperature
    else:
        # The return-flow limitation is a separate gradient characteristic.
        # It uses the same day/night room setpoints as the flow characteristic,
        # but P13 replaces the fixed 24 °C flow base. P13 also forms the lower
        # bound; P14 limits the characteristic above.
        room_setpoint = (
            parameters.room_setpoint_day if day_mode else parameters.room_setpoint_night
        )
        slope = parameters.return_flow_gradient
        offset = parameters.return_flow_level
        base_temperature = parameters.return_flow_base_point
        minimum = parameters.return_flow_base_point
        maximum = parameters.maximum_return_flow_temperature

    if None in (
        room_setpoint,
        slope,
        offset,
        base_temperature,
        minimum,
        maximum,
    ):
        return None

    return utils.heating_curve(
        room_setpoint=room_setpoint,
        slope=slope,
        offset=offset,
        minimum_flow_temperature=minimum,
        maximum_flow_temperature=maximum,
        base_temperature=base_temperature,
    )
