"""Reusable TROVIS option metadata."""


from __future__ import annotations

from .metadata import OptionMetadata
from .enums import (
    EnergyUnit,
    FlowRateUnit,
    HeatMeterReadMode,
    OperatingMode,
    PowerUnit,
    VolumeUnit,
    Weekday,
)


# All heating and hot-water circuits share one writable operating-mode list.
# PROGRAM remains readable through OperatingMode, but it is a timer-program
# state rather than a normal mode selected through a writable field.
OPERATING_MODE_OPTIONS = (
    OptionMetadata("automatic", int(OperatingMode.AUTOMATIC), "Auto"),
    OptionMetadata("standby", int(OperatingMode.STANDBY), "Standby"),
    OptionMetadata("manual", int(OperatingMode.MANUAL), "Hand"),
    OptionMetadata("day", int(OperatingMode.DAY), "Sonne"),
    OptionMetadata("night", int(OperatingMode.NIGHT), "Mond"),
)


WEEKDAY_OPTIONS = (
    OptionMetadata("off", int(Weekday.OFF), "Aus"),
    OptionMetadata("monday", int(Weekday.MONDAY), "Montag"),
    OptionMetadata("tuesday", int(Weekday.TUESDAY), "Dienstag"),
    OptionMetadata("wednesday", int(Weekday.WEDNESDAY), "Mittwoch"),
    OptionMetadata("thursday", int(Weekday.THURSDAY), "Donnerstag"),
    OptionMetadata("friday", int(Weekday.FRIDAY), "Freitag"),
    OptionMetadata("saturday", int(Weekday.SATURDAY), "Samstag"),
    OptionMetadata("sunday", int(Weekday.SUNDAY), "Sonntag"),
)


HEAT_METER_READ_MODE_OPTIONS = (
    OptionMetadata("hours_24", int(HeatMeterReadMode.HOURS_24), "24h"),
    OptionMetadata("continuous", int(HeatMeterReadMode.CONTINUOUS), "Cont"),
    OptionMetadata("coil", int(HeatMeterReadMode.COIL), "Coil"),
)


VOLUME_UNIT_OPTIONS = (
    OptionMetadata("cubic_meters", int(VolumeUnit.CUBIC_METERS), "m³"),
    OptionMetadata("liters", int(VolumeUnit.LITERS), "l"),
)


ENERGY_UNIT_OPTIONS = (
    OptionMetadata("megawatt_hours", int(EnergyUnit.MEGAWATT_HOURS), "MWh"),
    OptionMetadata("kilowatt_hours", int(EnergyUnit.KILOWATT_HOURS), "kWh"),
    OptionMetadata("gigajoules", int(EnergyUnit.GIGAJOULES), "GJ"),
)


POWER_UNIT_OPTIONS = (
    OptionMetadata("kilowatts", int(PowerUnit.KILOWATTS), "kW"),
    OptionMetadata("megawatts", int(PowerUnit.MEGAWATTS), "MW"),
)


FLOW_RATE_UNIT_OPTIONS = (
    OptionMetadata(
        "cubic_meters_per_hour",
        int(FlowRateUnit.CUBIC_METERS_PER_HOUR),
        "m³/h",
    ),
    OptionMetadata(
        "liters_per_hour",
        int(FlowRateUnit.LITERS_PER_HOUR),
        "l/h",
    ),
)