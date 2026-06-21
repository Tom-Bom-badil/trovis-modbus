"""Derived-value helpers — faithful ports of the YAML template sensors."""

from __future__ import annotations

from .model import SWITCH_POSITIONS, WEEKDAYS


def format_date(datum: int | None, jahr: int | None) -> str | None:
    """``day*100+month`` + year -> ``DD.MM.YYYY`` (matches the YAML template)."""
    if datum is None or jahr is None:
        return None
    value = int(datum)
    text = str(value)
    year = int(jahr)
    if value < 1000:
        return f"0{text[:1]}.{text[-2:]}.{year}"
    return f"{text[:2]}.{text[-2:]}.{year}"


def format_ddmm(value: int | None) -> str | None:
    """``day*100+month`` -> ``DD.MM.`` (summer-mode on/off dates)."""
    if value is None:
        return None
    number = int(value)
    text = str(number)
    if number < 1000:
        return f"0{text[:1]}.{text[-2:]}."
    return f"{text[:2]}.{text[-2:]}."


def format_time(value: int | None) -> str | None:
    """``hour*100+minute`` -> ``HH:MM`` (matches the YAML padding ladder)."""
    if value is None:
        return None
    number = int(value)
    text = str(number)
    if number < 10:
        return f"00:0{text}"
    if number < 60:
        return f"00:{text}"
    if number < 1000:
        return f"0{text[:1]}:{text[-2:]}"
    return f"{text[:2]}:{text[-2:]}"


def format_weekday(value: int | None) -> str | None:
    """Disinfection weekday index -> text (0 = off)."""
    if value is None:
        return None
    index = int(value)
    if 0 <= index < len(WEEKDAYS):
        return WEEKDAYS[index]
    return None


def format_switch(value: int | None) -> str | None:
    """Operating-mode / rotary-switch index -> text."""
    if value is None:
        return None
    index = int(value)
    if 0 <= index < len(SWITCH_POSITIONS):
        return SWITCH_POSITIONS[index]
    return None


def heating_curve(
    *,
    soll: float,
    niveau: float,
    steigung: float,
    vl_min: float,
    vl_max: float,
) -> list[float]:
    """Return the 41-point flow-temperature curve for outside temps -20..20 °C.

    Reproduces the exact formula from ``heating_curves.yaml`` (including its
    ``(x - 20)`` reference shift), clamped to ``[vl_min, vl_max]``.
    """
    curve: list[float] = []
    for x in range(-20, 21):
        shifted = x - 20
        vl = (
            24
            + niveau
            + 2 * steigung * (soll - 20)
            - (0.1 + 0.9 * steigung) * (1.5 * shifted + 0.01 * (shifted * shifted))
        )
        vl = max(vl_min, min(vl_max, vl))
        curve.append(round(vl, 2))
    return curve


# Outside-temperature x-axis shared by every heating curve.
CURVE_X_VALUES: list[int] = list(range(-20, 21))
