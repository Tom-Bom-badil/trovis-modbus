"""Small helpers shared across sub-systems: curves and native value types."""

from __future__ import annotations

from datetime import date, time
from typing import NamedTuple

# Outdoor-temperature x-axis shared by every heating characteristic.
OUTDOOR_TEMPERATURES: list[int] = list(range(-20, 21))


class MonthDay(NamedTuple):
    """A recurring day-of-year without a year (e.g. a summer boundary)."""

    day: int
    month: int

    def __str__(self) -> str:
        """Render as the controller displays it, e.g. ``15.05``."""
        return f"{self.day:02d}.{self.month:02d}"


class TemperatureRange(NamedTuple):
    """Lower and upper edge of a derived temperature interval."""

    minimum: float
    maximum: float


def time_from_hhmm(raw: int | None) -> time | None:
    """Decode the controller's packed HHMM time (e.g. 1430 -> 14:30)."""
    if raw is None:
        return None
    hour, minute = divmod(raw, 100)
    try:
        return time(hour=hour, minute=minute)
    except ValueError:
        return None


def time_to_hhmm(value: time) -> int:
    """Encode a naive, minute-resolution ``time`` as packed HHMM."""
    if not isinstance(value, time):
        raise TypeError(f"expected datetime.time, got {type(value).__name__}")
    if value.tzinfo is not None:
        raise ValueError("TROVIS clock values must not contain a timezone")
    if value.second or value.microsecond:
        raise ValueError("TROVIS clock values have one-minute resolution")
    return value.hour * 100 + value.minute


def month_day_from_ddmm(raw: int | None) -> MonthDay | None:
    """Decode a packed DDMM value into a validated recurring date."""
    if raw is None:
        return None
    day, month = divmod(raw, 100)
    try:
        # Leap year allows the recurring value 29 February.
        date(2000, month, day)
    except ValueError:
        return None
    return MonthDay(day=day, month=month)


def month_day_to_ddmm(value: MonthDay) -> int:
    """Encode a validated recurring date as packed DDMM."""
    if not isinstance(value, MonthDay):
        raise TypeError(f"expected MonthDay, got {type(value).__name__}")
    try:
        date(2000, value.month, value.day)
    except ValueError as err:
        raise ValueError(f"invalid recurring date: {value}") from err
    return value.day * 100 + value.month


def date_from_ddmm_year(raw_date: int | None, year: int | None) -> date | None:
    """Decode packed DDMM plus a separate year register."""
    if raw_date is None or year is None:
        return None
    recurring = month_day_from_ddmm(raw_date)
    if recurring is None:
        return None
    try:
        return date(year, recurring.month, recurring.day)
    except ValueError:
        return None


def date_to_ddmm_year(value: date) -> tuple[int, int]:
    """Encode a calendar date as ``(DDMM, year)``."""
    if not isinstance(value, date):
        raise TypeError(f"expected datetime.date, got {type(value).__name__}")
    return value.day * 100 + value.month, value.year


def heating_characteristic(
    *,
    room_setpoint: float,
    gradient: float,
    level: float,
    minimum_flow_temperature: float,
    maximum_flow_temperature: float,
) -> list[float]:
    """Flow temperatures for outdoor temperatures -20..20 °C, clamped to [min, max].
    Reproduces the formula from the upstream ``heating_characteristics.yaml`` exactly,
    including its ``(x - 20)`` reference shift. Pair element ``i`` with
    :data:`OUTDOOR_TEMPERATURES`\\ ``[i]``.
    """
    curve: list[float] = []
    for outdoor_temperature in OUTDOOR_TEMPERATURES:
        shifted = outdoor_temperature - 20
        flow = (
            24
            + level
            + 2 * gradient * (room_setpoint - 20)
            - (0.1 + 0.9 * gradient) * (1.5 * shifted + 0.01 * (shifted * shifted))
        )
        curve.append(
            round(max(minimum_flow_temperature, min(maximum_flow_temperature, flow)), 2)
        )
    return curve
