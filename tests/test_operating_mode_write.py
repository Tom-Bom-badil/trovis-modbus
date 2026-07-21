"""Tests for the TROVIS operating-mode Ebene semantics."""

from __future__ import annotations

from trovis_modbus import OperatingMode, Trovis557x
from trovis_modbus.options import OPERATING_MODE_OPTIONS


def test_circuits_share_operating_mode_metadata(trovis: Trovis557x) -> None:
    """Heating-circuit and domestic-hot-water modes expose the same central options."""
    heating_metadata = trovis.hk1.require_metadata_for("mode")
    ww_metadata = trovis.ww.require_metadata_for("mode")

    assert heating_metadata.enum is not None
    assert ww_metadata.enum is not None
    assert heating_metadata.enum.options == OPERATING_MODE_OPTIONS
    assert ww_metadata.enum.options == OPERATING_MODE_OPTIONS


async def test_heating_automatic_restores_autark_without_register_write(
    trovis: Trovis557x,
) -> None:
    """Automatic mode is selected through the Ebene coil, not the mode HR."""
    unit = trovis.hk1._unit
    await unit.write_register(105, int(OperatingMode.DAY))
    await unit.write_coil(88, False)

    await trovis.hk1.set_mode(OperatingMode.AUTOMATIC)

    assert (await unit.read_coils(88, 1))[0] is True
    assert (await unit.read_holding_registers(105, 1))[0] == int(OperatingMode.DAY)


async def test_domestic_hot_water_automatic_uses_its_own_ebene_coil(
    trovis: Trovis557x,
) -> None:
    """Domestic hot water restores AUTARK through CL95 and leaves HR40112 intact."""
    unit = trovis.ww._unit
    await unit.write_register(111, int(OperatingMode.NIGHT))
    await unit.write_coil(94, False)

    await trovis.ww.set_mode(OperatingMode.AUTOMATIC)

    assert (await unit.read_coils(94, 1))[0] is True
    assert (await unit.read_holding_registers(111, 1))[0] == int(OperatingMode.NIGHT)
