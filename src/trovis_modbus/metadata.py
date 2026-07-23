"""Neutral TROVIS datapoint metadata."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, time
from enum import IntEnum
from typing import Any, Literal

from .utils import MonthDay

ValueKind = Literal[
    "number",
    "enum",
    "boolean",
    "raw",
    "date",
    "time",
    "month_day",
]
TemporalResolution = Literal["day", "minute"]
TemporalValue = date | time | MonthDay


@dataclass(frozen=True)
class NumberMetadata:
    """Metadata for numeric TROVIS values."""

    min_value: float | int | None = None
    max_value: float | int | None = None
    step: float | int | None = None
    digits: int | None = None
    unit: str | None = None
    raw_min: float | int | None = None
    raw_max: float | int | None = None


@dataclass(frozen=True)
class OptionMetadata:
    """Metadata for one discrete option."""

    key: str
    value: int
    label: str | None = None
    description: str | None = None


@dataclass(frozen=True)
class EnumMetadata:
    """Metadata for selectable / discrete register values."""

    enum_type: type[IntEnum]
    options: tuple[OptionMetadata, ...]


@dataclass(frozen=True)
class BooleanMetadata:
    """Metadata for boolean coil/register-like values."""

    false_key: str = "off"
    true_key: str = "on"
    false_label: str | None = None
    true_label: str | None = None
    inverted: bool = False


@dataclass(frozen=True)
class TemporalMetadata:
    """Metadata for native calendar and clock values."""

    resolution: TemporalResolution
    min_value: TemporalValue | None = None
    max_value: TemporalValue | None = None
    raw_min: int | None = None
    raw_max: int | None = None


@dataclass(frozen=True)
class DatapointMetadata:
    """Neutral metadata for one TROVIS datapoint."""

    value_kind: ValueKind
    maker_reference: int | None = None
    maker_key: str | None = None
    maker_category: str | None = None
    description: str | None = None
    writable: bool = False
    number: NumberMetadata | None = None
    enum: EnumMetadata | None = None
    boolean: BooleanMetadata | None = None
    temporal: TemporalMetadata | None = None


def step_from_digits(digits: int | None) -> float | int | None:
    """Return the natural UI/write step from decimal precision."""

    if digits is None:
        return None
    if digits <= 0:
        return 1
    return 10**-digits


def attach_metadata(field: Any, metadata: DatapointMetadata) -> Any:
    """Attach TROVIS metadata to a modbus-connection field."""

    field.trovis_metadata = metadata
    return field
