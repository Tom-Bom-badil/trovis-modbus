"""trovis-modbus — read a Samson Trovis 557x heating controller over Modbus.

Construct ``Trovis557x(unit)`` with a ``modbus_connection.ModbusUnit``, call
``await device.async_update()``, then read its sub-systems as normal Python
objects::

    device.sensors.af1
    device.hk1.room_setpoint_active
    device.ww.storage_tank_charging_pump_running

The library is organized by sub-system — one file each for ``device_info``,
``controller``, ``clock``, ``sensors``, ``heating_circuit`` and ``domestic_hot_water`` —
built on the generic ``Component`` / ``RegisterField`` / ``CoilField`` framework
in ``modbus_connection.model``.
"""

from .addresses import coil_address, register_address
from .clock import Clock
from .controller import Controller
from .device_info import DeviceInformation
from .domestic_hot_water import DomesticHotWater
from .enums import (
    EnergyUnit,
    FlowRateUnit,
    HeatMeterReadMode,
    OperatingMode,
    PowerUnit,
    StorageStatus,
    SystemActivity,
    VolumeUnit,
    Weekday,
)
from .exceptions import (
    TrovisValueValidationError,
    TrovisWriteAccessDisabledError,
    TrovisWriteAccessError,
    TrovisWriteNotImplementedError,
)
from .heating_circuit import HeatingCircuit
from .metadata import (
    BooleanMetadata,
    DatapointMetadata,
    EnumMetadata,
    NumberMetadata,
    OptionMetadata,
    TemporalMetadata,
)
from .model import DEFAULT_WRITE_ACCESS_CODE
from .sensors import Sensors
from .trovis import Trovis557x
from .utils import (
    OUTDOOR_TEMPERATURES,
    MonthDay,
    TemperatureRange,
    heating_characteristic,
)

__all__ = [
    "coil_address",
    "register_address",
    "OUTDOOR_TEMPERATURES",
    "Clock",
    "Controller",
    "DeviceInformation",
    "EnergyUnit",
    "FlowRateUnit",
    "HeatingCircuit",
    "HeatMeterReadMode",
    "DomesticHotWater",
    "MonthDay",
    "TemperatureRange",
    "OperatingMode",
    "SystemActivity",
    "PowerUnit",
    "Sensors",
    "StorageStatus",
    "Trovis557x",
    "VolumeUnit",
    "Weekday",
    "heating_characteristic",
    "DEFAULT_WRITE_ACCESS_CODE",
    "TrovisWriteNotImplementedError",
    "TrovisWriteAccessDisabledError",
    "TrovisWriteAccessError",
    "TrovisValueValidationError",
    "BooleanMetadata",
    "DatapointMetadata",
    "EnumMetadata",
    "NumberMetadata",
    "OptionMetadata",
    "TemporalMetadata",
]
