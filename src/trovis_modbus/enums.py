"""Enumerations used across the TROVIS model."""

from __future__ import annotations

from enum import IntEnum


class OperatingMode(IntEnum):
    """Operating mode of a heating circuit, hot water, or rotary switch.

    Matches the controller's complete switch list (``Liste_Schalter``). The
    writable option list intentionally excludes :attr:`PROGRAM`, while every
    heating and hot-water circuit uses the same enum.
    """

    PROGRAM = 0  # timer program ("PA")
    AUTOMATIC = 1
    STANDBY = 2
    MANUAL = 3  # manual mode / "Hand"
    DAY = 4  # daytime settings / "Sonne"
    NIGHT = 5  # nighttime settings / "Mond"


class Weekday(IntEnum):
    """Weekday for the thermal-disinfection schedule (0 = disabled)."""

    OFF = 0
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


class HeatMeterReadMode(IntEnum):
    """Read mode used by a connected heat meter."""

    HOURS_24 = 0
    CONTINUOUS = 1
    COIL = 2


class FlowRateUnit(IntEnum):
    """Unit selector for heat-meter flow-rate values."""

    CUBIC_METERS_PER_HOUR = 0
    LITERS_PER_HOUR = 1


class VolumeUnit(IntEnum):
    """Unit selector for heat-meter volume values."""

    CUBIC_METERS = 0
    LITERS = 1


class EnergyUnit(IntEnum):
    """Unit selector for heat-meter energy values."""

    MEGAWATT_HOURS = 0
    KILOWATT_HOURS = 1
    GIGAJOULES = 2


class PowerUnit(IntEnum):
    """Unit selector for heat-meter power values."""

    KILOWATTS = 0
    MEGAWATTS = 1


class StorageStatus(IntEnum):
    """Current domestic-hot-water storage operating state (HR41827)."""

    STANDBY = 0
    MONITORING = 1
    CIRCULATION = 2
    DEMAND = 3
    CHARGING = 4
    PUMP_OVERRUN = 5
    DISCHARGE_PROTECTION = 6
