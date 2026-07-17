"""Tests for central TROVIS enums and reusable option metadata."""

from __future__ import annotations

from trovis_modbus import (
    EnergyUnit,
    FlowRateUnit,
    HeatMeterReadMode,
    OperatingMode,
    PowerUnit,
    VolumeUnit,
)
from trovis_modbus.metadata import OptionMetadata
from trovis_modbus.options import (
    ENERGY_UNIT_OPTIONS,
    FLOW_RATE_UNIT_OPTIONS,
    HEAT_METER_READ_MODE_OPTIONS,
    OPERATING_MODE_OPTIONS,
    POWER_UNIT_OPTIONS,
    VOLUME_UNIT_OPTIONS,
)


def _option_values(options: tuple[OptionMetadata, ...]) -> tuple[int, ...]:
    return tuple(option.value for option in options)


def _option_keys(options: tuple[OptionMetadata, ...]) -> tuple[str, ...]:
    return tuple(option.key for option in options)


def test_operating_mode_options_are_shared_and_complete() -> None:
    """Every circuit gets one common selectable operating-mode subset."""
    assert _option_keys(OPERATING_MODE_OPTIONS) == (
        "automatic",
        "standby",
        "manual",
        "day",
        "night",
    )
    assert _option_values(OPERATING_MODE_OPTIONS) == (
        int(OperatingMode.AUTOMATIC),
        int(OperatingMode.STANDBY),
        int(OperatingMode.MANUAL),
        int(OperatingMode.DAY),
        int(OperatingMode.NIGHT),
    )
    assert int(OperatingMode.PROGRAM) not in _option_values(OPERATING_MODE_OPTIONS)


def test_heat_meter_read_mode_options_match_controller_values() -> None:
    assert _option_values(HEAT_METER_READ_MODE_OPTIONS) == tuple(
        map(int, HeatMeterReadMode)
    )


def test_heat_meter_unit_options_match_controller_values() -> None:
    assert _option_values(FLOW_RATE_UNIT_OPTIONS) == tuple(map(int, FlowRateUnit))
    assert _option_values(VOLUME_UNIT_OPTIONS) == tuple(map(int, VolumeUnit))
    assert _option_values(ENERGY_UNIT_OPTIONS) == tuple(map(int, EnergyUnit))
    assert _option_values(POWER_UNIT_OPTIONS) == tuple(map(int, PowerUnit))
