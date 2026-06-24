"""Trovis-specific pieces layered on the ``modbus_connection.model`` framework.

The generic ``Component`` base, the field descriptors and the typed factories
come straight from ``modbus_connection.model`` (sub-systems import those
directly). This module adds only what is specific to the Trovis 557x:

- :class:`TrovisComponent`, a ``Component`` preset with the controller's readable
  address ranges, so every sub-system reads without crossing an unreadable gap;
- :func:`temperature`, a 0.1-scaled register with the controller's NaN sentinel;
- :func:`operating_mode` / :func:`weekday_value`, enum registers decoded natively
  to :class:`~trovis_modbus.enums.OperatingMode` / ``Weekday`` via the framework's
  ``enum_type`` mapping.

Shaping the framework has no native type for (the controller's packed HHMM times
and day/month dates) stays a private raw field plus a normal ``@property`` on the
sub-system.
"""

from __future__ import annotations

from modbus_connection.model import Component, RegisterField, gauge
from modbus_connection.model.fields import NumberField

from .enums import OperatingMode, Weekday
from .ranges import COIL_RANGES, REGISTER_RANGES

NAN_INT16 = 0x7FFF  # the value the controller returns for an absent sensor


class TrovisComponent(Component):
    """A Trovis sub-system, preset with the controller's readable address ranges."""

    register_ranges = REGISTER_RANGES
    coil_ranges = COIL_RANGES


def temperature(
    address: int,
    *,
    stride: int = 0,
    writable: bool = False,
    level_coil: int | None = None,
    level_coil_stride: int = 0,
    unit: str = "°C",
) -> RegisterField[float]:
    """A signed 0.1-scaled temperature register with the Trovis NaN sentinel."""
    return gauge(
        address,
        0.1,
        signed=True,
        nan=NAN_INT16,
        stride=stride,
        writable=writable,
        level_coil=level_coil,
        level_coil_stride=level_coil_stride,
        unit=unit,
    )


def operating_mode(
    address: int,
    *,
    stride: int = 0,
    writable: bool = False,
    level_coil: int | None = None,
    level_coil_stride: int = 0,
) -> RegisterField[OperatingMode]:
    """An operating-mode register decoded to :class:`OperatingMode`.

    An unknown code (e.g. an absent value) decodes to ``None``.
    """
    return NumberField[OperatingMode](
        address,
        signed=False,
        enum_type=OperatingMode,
        stride=stride,
        writable=writable,
        level_coil=level_coil,
        level_coil_stride=level_coil_stride,
    )


def weekday_value(address: int, *, writable: bool = False) -> RegisterField[Weekday]:
    """A weekday register decoded to :class:`Weekday` (``OFF`` = disabled)."""
    return NumberField[Weekday](
        address, signed=False, enum_type=Weekday, writable=writable
    )
