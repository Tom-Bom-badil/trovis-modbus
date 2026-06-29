"""Trovis-specific pieces layered on the ``modbus_connection.model`` framework."""

# --- original comment: ---
# """Trovis-specific pieces layered on the ``modbus_connection.model`` framework.

# The generic ``Component`` base, the field descriptors and the typed factories
# (including ``enum`` for operating modes / weekdays) come straight from
# ``modbus_connection.model`` — sub-systems import those directly. This module adds
# only what is specific to the Trovis 557x:

# - :class:`TrovisComponent`, a ``Component`` preset with the controller's readable
#   address ranges and the "Ebene" write-unlock sequencing;
# - :func:`temperature`, a 0.1-scaled register with the controller's NaN sentinel.

# Shaping the framework has no native type for (the controller's packed HHMM times
# and day/month dates) stays a private raw field plus a normal ``@property`` on the
# sub-system.
# """

from typing import Any

from modbus_connection import ModbusError
from modbus_connection.model import (
    Component,
    RegisterField,
    coil as _modbus_coil,
    gauge,
)

from .exceptions import TrovisWriteAccessError
from .ranges import COIL_RANGES, REGISTER_RANGES


NAN_INT16 = 0x7FFF  # the value the controller returns for an absent sensor

DEFAULT_WRITE_ACCESS_CODE = 1732
WRITE_ACCESS_REGISTER = 144
WRITE_ACCESS_DISABLE_CODE = 0

LEVEL_GLT = False
LEVEL_AUTARK = True


def coil_address(cl_number: int) -> int:
    """Return the zero-based Modbus address for a TROVIS CL number.
    Manufacturer coil lists use CL numbers starting at 1. Modbus PDU addresses
    are zero-based, so CL137 is sent as address 136.
    """
    if cl_number < 1:
        raise ValueError(f"Invalid TROVIS coil number: {cl_number}")

    return cl_number - 1


def coil(
    cl_number: int,
    *,
    stride: int = 0,
    writable: bool = False,
):
    """Create a coil field from a manufacturer TROVIS CL number."""
    return _modbus_coil(
        coil_address(cl_number),
        stride=stride,
        writable=writable,
    )


async def async_read_writing_enabled(unit: Any) -> bool:
    """Return whether TROVIS write access appears to be active."""
    try:
        return (
            await unit.read_holding_registers(WRITE_ACCESS_REGISTER, 1)
        )[0] != WRITE_ACCESS_DISABLE_CODE
    except ModbusError as err:
        raise TrovisWriteAccessError(
            "Could not read TROVIS write access state"
        ) from err


async def async_enable_writing(
    unit: Any,
    access_code: int = DEFAULT_WRITE_ACCESS_CODE,
) -> None:
    """Enable TROVIS writing globally."""
    try:
        await unit.write_register(WRITE_ACCESS_REGISTER, access_code)
    except ModbusError as err:
        raise TrovisWriteAccessError(
            "Could not enable TROVIS write access"
        ) from err


async def async_disable_writing(unit: Any) -> None:
    """Disable TROVIS writing globally."""
    try:
        await unit.write_register(WRITE_ACCESS_REGISTER, WRITE_ACCESS_DISABLE_CODE)
    except ModbusError as err:
        raise TrovisWriteAccessError(
            "Could not reset TROVIS write access"
        ) from err


async def async_ensure_writing_enabled(
    unit: Any,
    access_code: int = DEFAULT_WRITE_ACCESS_CODE,
) -> None:
    """Ensure that the TROVIS access code is active for the next write."""
    try:
        await unit.write_register(WRITE_ACCESS_REGISTER, access_code)
    except ModbusError as err:
        raise TrovisWriteAccessError(
            "Could not refresh TROVIS write access"
        ) from err


class TrovisComponent(Component):
    """A Trovis sub-system: readable ranges + the Ebene write-unlock quirk.

    Some writable values are ignored over Modbus unless their "Ebene" override
    coil is first released to 0 (= GLT / remote control). Subclasses list those
    in :attr:`ebene_coils`.
    """

    # --- original comment: ---
    # """A Trovis sub-system: readable ranges + the Ebene write-unlock quirk.

    # Some writable values are ignored over Modbus unless their "Ebene" override
    # coil is first released to 0 (= remote control). Subclasses list those in
    # :attr:`ebene_coils` (``field name -> (coil address, per-index stride)``); the
    # framework removed the built-in ``level_coil`` support in 3.0, so this is the
    # recommended consumer-side ``write`` override.
    # """

    register_ranges = REGISTER_RANGES
    coil_ranges = COIL_RANGES

    # Writable fields whose write must first release an override coil to 0.
    ebene_coils: dict[str, tuple[int, int]] = {}

    async def write(self, field: str, value: Any) -> None:
        """Write a field, applying field-specific TROVIS preconditions."""
        if (override := self.ebene_coils.get(field)) is not None:
            address, stride = override
            await self._unit.write_coil(
                coil_address(address + stride * (self._index - 1)),
                LEVEL_GLT,
            )

        await super().write(field, value)

    async def async_write_datapoint(
        self,
        field: str,
        value: Any,
        *,
        access_code: int = DEFAULT_WRITE_ACCESS_CODE,
    ) -> None:
        """Write a TROVIS data point.

        This is the public write entry point for integrations. It checks the
        global TROVIS write mode, refreshes the access code and then delegates
        to the generic component write path.
        """
        await async_ensure_writing_enabled(self._unit, access_code)
        await self.write(field, value)


def temperature(
    address: int,
    *,
    stride: int = 0,
    writable: bool = False,
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
        unit=unit,
    )