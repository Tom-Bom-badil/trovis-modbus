"""Tests for the TROVIS operating-mode Ebene semantics."""

from __future__ import annotations

from trovis_modbus import OperatingMode, Trovis557x
from trovis_modbus.options import OPERATING_MODE_OPTIONS


def test_circuits_share_operating_mode_metadata(trovis: Trovis557x) -> None:
    """Heating and hot-water modes expose the same central options."""
    heating_metadata = trovis.heating_circuit_1.require_metadata_for("mode")
    hot_water_metadata = trovis.hot_water.require_metadata_for("mode")

    assert heating_metadata.enum is not None
    assert hot_water_metadata.enum is not None
    assert heating_metadata.enum.options == OPERATING_MODE_OPTIONS
    assert hot_water_metadata.enum.options == OPERATING_MODE_OPTIONS


async def test_heating_automatic_restores_autark_without_register_write(
    trovis: Trovis557x,
) -> None:
    """Automatic mode is selected through the Ebene coil, not the mode HR."""
    unit = trovis.heating_circuit_1._unit
    await unit.write_register(105, int(OperatingMode.DAY))
    await unit.write_coil(88, False)

    await trovis.heating_circuit_1.set_mode(OperatingMode.AUTOMATIC)

    assert (await unit.read_coils(88, 1))[0] is True
    assert (await unit.read_holding_registers(105, 1))[0] == int(OperatingMode.DAY)


async def test_hot_water_automatic_uses_its_own_ebene_coil(
    trovis: Trovis557x,
) -> None:
    """Hot water restores AUTARK through CL95 and leaves HR40112 intact."""
    unit = trovis.hot_water._unit
    await unit.write_register(111, int(OperatingMode.NIGHT))
    await unit.write_coil(94, False)

    await trovis.hot_water.set_mode(OperatingMode.AUTOMATIC)

    assert (await unit.read_coils(94, 1))[0] is True
    assert (await unit.read_holding_registers(111, 1))[0] == int(OperatingMode.NIGHT)
