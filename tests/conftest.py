"""Fixtures: a Trovis557x over modbus-connection's in-memory mock backend.

The mock backend and its fixtures ship with ``modbus-connection``. They are
imported explicitly below so the test suite does not depend on pytest entry-point
autoloading. There is no real server, socket, or backend here — just an
address-keyed store loaded with TROVIS-shaped register and coil values.
"""

from __future__ import annotations

import pytest
from modbus_connection.mock import MockModbusUnit
from modbus_connection.pytest_plugin import (
    mock_modbus_connection as mock_modbus_connection,
    mock_modbus_unit as mock_modbus_unit,
)

from trovis_modbus import Trovis557x

# run: PYTHONPATH=src:/config/dev/modbus-connection/src python -m pytest

# Raw register words keyed by their (protocol) address; decoded view inline.
HOLDING: dict[int, int] = {
    0: 5579,  # model
    1: 21,  # system -> 2.1
    2: 305,  # firmware -> 3.05
    3: 110,  # hardware -> 1.10
    5: 12345,  # serial
    9: 0x10000 - 50,  # sensors.af1 -> -5.0 (signed, outdoor temperature)
    12: 300,  # sensors.vf1 -> 30.0 -> unsigned, the water in your pipes
    19: 200,  # sensors.rf1 -> 20.0
    22: 450,  # sensors.sf1 -> 45.0
    23: 0x7FFF,  # sensors.sf2 -> NaN -> None
    24: 650,  # sensors.sf3 -> 65.0
    25: 952,  # sensors.ae1 / sensors.fg1 -> 95.2
    26: 3250,  # sensors.ae2 / sensors.fg2 -> 325.0
    27: 125,  # sensors.ae3 / sensors.fg3 -> 12.5
    28: 240,  # sensors.pulse_rate -> 240 Imp/h
    41: 735,  # sensors.analog_input_voltage -> 7.35 V / current view -> 147.0 mA
    42: 185,  # sensors.summer_outdoor_temperature_average -> 18.5 °C
    98: 900,  # max flow setpoint -> 90.0
    99: 1430,  # time -> 14:30
    100: 2106,  # date -> 21.06
    101: 2026,  # year
    102: 1,  # switch_top -> AUTOMATIC
    105: 1,  # hk1 mode -> AUTOMATIC
    106: 42,  # hk1 control signal -> 42 %
    112: 1505,  # summer start -> 15.05
    113: 3009,  # summer end -> 30.09
    114: 2,  # summer_days_on
    115: 3,  # summer_days_off
    120: 50,  # temperature monitoring deviation -> 5.0 K
    121: 30,  # temperature monitoring window -> 30 min
    123: 0x10000 - 200,  # 0 V outdoor-temperature range -> -20.0 °C
    124: 500,  # 10 V outdoor-temperature range -> 50.0 °C
    149: 0,  # error status
    999: 550,  # hk1 flow_setpoint -> 55.0
    1000: 800,  # hk1 maximum_flow_temperature -> 80.0
    1001: 200,  # hk1 minimum_flow_temperature -> 20.0
    1002: 210,  # hk1 room_setpoint_day -> 21.0
    1003: 180,  # hk1 room_setpoint_night -> 18.0
    1004: 210,  # hk1 room_setpoint_active -> 21.0
    1005: 12,  # hk1 gradient -> 1.2
    1006: 0,  # hk1 level -> 0.0
    1199: 480,  # hk2 flow_setpoint -> 48.0
    1799: 500,  # ww setpoint_day -> 50.0
    1802: 50,  # ww hysteresis -> 5.0 K
    1806: 450,  # ww setpoint_night -> 45.0 °C
    1807: 500,  # ww setpoint_active -> 50.0
    1837: 670,  # ww active_charging_setpoint -> 67.0
    1830: 3,  # disinfection weekday -> WEDNESDAY
    1831: 1900,  # disinfection start -> 19:00
    1832: 2100,  # disinfection stop -> 21:00
    1838: 30,  # disinfection hold -> 30 min
}

COILS: dict[int, bool] = {
    3: True,  # CL4 / Sammel_Ebenenbit -> AUTARK by default
    56: True,  # hk1 pump
    158: False,  # CL159 / GLT timeout inactive
    999: True,  # hk1 automatic
    1000: True,  # hk1 day active
    1799: True,  # ww automatic
    59: True,  # WW storage tank charging pump
}


@pytest.fixture
def trovis(mock_modbus_unit: MockModbusUnit) -> Trovis557x:
    """A Trovis557x over the mock unit, preloaded with device values."""
    mock_modbus_unit.holding.update(HOLDING)
    mock_modbus_unit.coils.update(COILS)
    return Trovis557x(mock_modbus_unit)
