"""trovis-modbus — read a Samson Trovis 557x heating controller over Modbus.

Construct ``Trovis557x(unit)`` with a ``modbus_connection.ModbusUnit``, call
``await device.async_update()``, then read its sub-systems as normal Python
objects::

    device.sensors.outside_1
    device.heating_circuit_1.room_setpoint_active
    device.hot_water.charge_pump_running

The library is organized by sub-system — one file each for ``device_info``,
``controller``, ``clock``, ``sensors``, ``heating_circuit`` and ``hot_water`` —
built on the generic ``Component`` / ``RegisterField`` / ``CoilField`` framework
in ``modbus_connection.model``.
"""


from .trovis import Trovis557x
from .addresses import coil_address, register_address
from .clock import Clock
from .controller import Controller
from .device_info import DeviceInformation
from .heating_circuit import HeatingCircuit
from .hot_water import HotWater
from .model import DEFAULT_WRITE_ACCESS_CODE
from .sensors import Sensors
from .enums import (
    EnergyUnit,
    FlowRateUnit,
    HeatMeterReadMode,
    OperatingMode,
    PlantActivity,
    PowerUnit,
    StorageStatus,
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
from .utils import (
    OUTSIDE_TEMPERATURES,
    MonthDay,
    TemperatureRange,
    heating_curve,
)


__all__ = [
    "coil_address",
    "register_address",
    "OUTSIDE_TEMPERATURES",
    "Clock",
    "Controller",
    "DeviceInformation",
    "EnergyUnit",
    "FlowRateUnit",
    "HeatingCircuit",
    "HeatMeterReadMode",
    "HotWater",
    "MonthDay",
    "TemperatureRange",
    "OperatingMode",
    "PlantActivity",
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
