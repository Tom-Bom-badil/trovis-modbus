"""Definitions for Trovis 557x registers, coils and derived values."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

RegisterType = Literal["int16", "uint16"]

# Operating-mode / rotary-switch positions (register raw value -> text).
SWITCH_POSITIONS: tuple[str, ...] = ("PA", "Auto", "Stdby", "Hand", "Sonne", "Mond")
# Disinfection weekday (register raw value -> text). Index 0 = off.
WEEKDAYS: tuple[str, ...] = ("aus", "Mo", "Di", "Mi", "Do", "Fr", "Sa", "So")


@dataclass(frozen=True, slots=True)
class RegisterDef:
    """A single Modbus holding register exposed by the controller."""

    key: str  # the original YAML unique_id; the canonical identifier
    name: str
    address: int
    group: str
    data_type: RegisterType = "uint16"
    scale: float = 1.0
    precision: int | None = None
    unit: str | None = None
    device_class: str | None = None
    nan_value: int | None = None
    min_value: float | None = None
    max_value: float | None = None
    writable: bool = False

    def decode(self, raw: int) -> float | int | None:
        """Turn a raw register word into the scaled value (or None if N/A)."""
        if self.nan_value is not None and raw == self.nan_value:
            return None
        if self.data_type == "int16" and raw >= 0x8000:
            raw -= 0x10000
        if self.precision is not None:
            return round(raw * self.scale, self.precision)
        if self.scale == 1.0:
            return int(raw)
        return raw * self.scale


@dataclass(frozen=True, slots=True)
class CoilDef:
    """A single Modbus coil exposed by the controller."""

    key: str  # the original YAML unique_id
    name: str
    address: int
    group: str
    writable: bool = False


@dataclass(frozen=True, slots=True)
class DerivedDef:
    """A value computed from one or more registers/coils (a template sensor)."""

    key: str  # the original YAML unique_id
    name: str
    group: str
