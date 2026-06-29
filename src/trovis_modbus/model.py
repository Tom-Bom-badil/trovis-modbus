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


from __future__ import annotations

from typing import Any

from modbus_connection.model import Component, RegisterField, gauge

from .exceptions import TrovisWriteAccessDisabledError
from .ranges import COIL_RANGES, REGISTER_RANGES

NAN_INT16 = 0x7FFF  # the value the controller returns for an absent sensor

DEFAULT_WRITE_ACCESS_CODE = 1732
WRITE_ACCESS_REGISTER = 144
WRITE_ACCESS_DISABLE_CODE = 0

# Manufacturer CL4, zero-based Modbus coil address 3.
# False/0 = GLT, True/1 = AUTARK.
GLOBAL_LEVEL_COIL = 3
LEVEL_GLT = False
LEVEL_AUTARK = True


async def async_read_writing_enabled(unit: Any) -> bool:
    """Return whether the controller is currently in GLT/write mode."""
    return (await unit.read_coils(GLOBAL_LEVEL_COIL, 1))[0] is LEVEL_GLT


async def async_enable_writing(
    unit: Any,
    access_code: int = DEFAULT_WRITE_ACCESS_CODE,
) -> None:
    """Enable TROVIS writing globally."""
    await unit.write_register(WRITE_ACCESS_REGISTER, access_code)
    await unit.write_coil(GLOBAL_LEVEL_COIL, LEVEL_GLT)


async def async_disable_writing(unit: Any) -> None:
    """Disable TROVIS writing globally."""
    # Set AUTARK while writing is still enabled, then clear the access code.
    await unit.write_coil(GLOBAL_LEVEL_COIL, LEVEL_AUTARK)
    await unit.write_register(WRITE_ACCESS_REGISTER, WRITE_ACCESS_DISABLE_CODE)


async def async_ensure_writing_enabled(
    unit: Any,
    access_code: int = DEFAULT_WRITE_ACCESS_CODE,
) -> None:
    """Ensure that a normal data point write may proceed."""
    if not await async_read_writing_enabled(unit):
        raise TrovisWriteAccessDisabledError("Please enable writing for changes!")

    # Keep the modem/write access alive for the actual value write.
    await unit.write_register(WRITE_ACCESS_REGISTER, access_code)


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
            await self._unit.write_coil(address + stride * (self._index - 1), LEVEL_GLT)

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