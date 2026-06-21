"""trovis-modbus — read a Samson Trovis 557x heating controller over Modbus.

Consumes a ``modbus_connection.ModbusUnit`` (the per-device handle): construct
``Trovis557x(unit)``, call ``await device.async_update()``, then read values by
their original YAML ``unique_id`` key.
"""

from .catalog import COILS, DERIVED, REGISTERS
from .model import (
    SWITCH_POSITIONS,
    WEEKDAYS,
    CoilDef,
    DerivedDef,
    RegisterDef,
)
from .trovis import Trovis557x

__all__ = [
    "COILS",
    "DERIVED",
    "REGISTERS",
    "SWITCH_POSITIONS",
    "WEEKDAYS",
    "CoilDef",
    "DerivedDef",
    "RegisterDef",
    "Trovis557x",
]
