"""trovis-modbus — read a Samson Trovis 557x heating controller over Modbus.

Construct ``Trovis557x(unit)`` with a ``modbus_connection.ModbusUnit``, call
``await device.async_update()``, then read its sub-systems as normal Python
objects::

    device.sensors.af1
    device.hk1.room_setpoint_active
    device.ww.storage_tank_charging_pump_running

Shared infrastructure remains at package level. Controller domains live in
``subsystems``; model descriptions and hydronic configurations have dedicated
packages for the upcoming model and capability work. The public imports and
``Trovis557x`` object API remain unchanged.
"""

from .addresses import coil_address, register_address
from .data_model import DEFAULT_WRITE_ACCESS_CODE
from .device_info import DeviceInformation
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
from .metadata import (
    BooleanMetadata,
    DatapointMetadata,
    EnumMetadata,
    NumberMetadata,
    OptionMetadata,
    TemporalMetadata,
)
from .subsystems import (
    Clock,
    Controller,
    DomesticHotWater,
    HeatingCircuit,
    Sensors,
)
from .trovis import Trovis557x
from .utils import (
    OUTDOOR_TEMPERATURES,
    MonthDay,
    TemperatureRange,
    heating_curve,
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
    "heating_curve",
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
