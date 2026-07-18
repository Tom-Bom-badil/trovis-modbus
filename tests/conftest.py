"""Fixtures: a Trovis557x over modbus-connection's in-memory mock backend.

The mock backend (and its ``mock_modbus_unit`` fixture) ship with
``modbus-connection`` as an auto-registered pytest plugin, so there is no real
server, socket, or backend here — just an address-keyed store the test loads
with Trovis-shaped register/coil values.
"""

from __future__ import annotations

import pytest
from modbus_connection.mock import MockModbusUnit

from trovis_modbus import Trovis557x

# pytest_plugins = ("modbus_connection.pytest_plugin",)
# run: PYTHONPATH=src:/config/dev/modbus-connection/src python -m pytest

# Raw register words keyed by their (protocol) address; decoded view inline.
HOLDING: dict[int, int] = {
    0: 5579,  # model
    1: 21,  # system -> 2.1
    2: 305,  # firmware -> 3.05
    3: 110,  # hardware -> 1.10
    5: 12345,  # serial
    9: 0x10000 - 50,  # sensors.af1 -> -5.0 (signed, outside)
    12: 300,  # sensors.vf1 -> 30.0 -> unsigned, the water in your pipes
    19: 200,  # sensors.rf1 -> 20.0
    22: 450,  # sensors.sf1 -> 45.0
    23: 0x7FFF,  # sensors.sf2 -> NaN -> None
    27: 125,  # sensors.ae3_fg3 -> 12.5
    28: 240,  # sensors.pulse_rate -> 240 Imp/h
    41: 735,  # sensors.analog_input_voltage -> 7.35 V
    42: 185,  # sensors.summer_outside_average -> 18.5 °C
    98: 900,  # max flow setpoint -> 90.0
    99: 1430,  # time -> 14:30
    100: 2106,  # date -> 21.06
    101: 2026,  # year
    102: 1,  # switch_top -> AUTOMATIC
    105: 1,  # hc1 mode -> AUTOMATIC
    106: 42,  # hc1 control signal -> 42 %
    112: 1505,  # summer start -> 15.05
    113: 3009,  # summer end -> 30.09
    114: 2,  # summer_days_on
    115: 3,  # summer_days_off
    120: 50,  # temperature monitoring deviation -> 5.0 K
    121: 30,  # temperature monitoring window -> 30 min
    123: 0x10000 - 200,  # 0 V outside-temperature range -> -20.0 °C
    124: 500,  # 10 V outside-temperature range -> 50.0 °C
    149: 0,  # error status
    999: 550,  # hc1 flow_setpoint -> 55.0
    1000: 800,  # hc1 flow_max -> 80.0
    1001: 200,  # hc1 flow_min -> 20.0
    1002: 210,  # hc1 room_setpoint_day -> 21.0
    1003: 180,  # hc1 room_setpoint_night -> 18.0
    1004: 210,  # hc1 room_setpoint_active -> 21.0
    1005: 12,  # hc1 slope -> 1.2
    1006: 0,  # hc1 level -> 0.0
    1199: 480,  # hc2 flow_setpoint -> 48.0
    1799: 500,  # hot_water setpoint_day -> 50.0
    1802: 50,  # hot_water hysteresis -> 5.0 K
    1806: 450,  # hot_water hold_value -> 45.0 °C
    1807: 500,  # hot_water setpoint_active -> 50.0
    1837: 670,  # hot_water active_charge_setpoint -> 67.0
    1830: 3,  # disinfection weekday -> WEDNESDAY
    1831: 1900,  # disinfection start -> 19:00
    1832: 2100,  # disinfection stop -> 21:00
    1838: 30,  # disinfection hold -> 30 min
}

COILS: dict[int, bool] = {
    3: True,  # CL4 / Sammel_Ebenenbit -> AUTARK by default
    56: True,  # hc1 pump
    158: False,  # CL159 / GLT timeout inactive
    999: True,  # hc1 automatic
    1000: True,  # hc1 day active
    1799: True,  # hot_water automatic
    59: True,  # hot_water charge pump
}


@pytest.fixture
def trovis(mock_modbus_unit: MockModbusUnit) -> Trovis557x:
    """A Trovis557x over the mock unit, preloaded with device values."""
    mock_modbus_unit.holding.update(HOLDING)
    mock_modbus_unit.coils.update(COILS)
    return Trovis557x(mock_modbus_unit)
