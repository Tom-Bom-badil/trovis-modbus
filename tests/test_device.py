"""End-to-end decoding + derived-value tests over a real Modbus server."""

from __future__ import annotations

import pytest

from trovis_modbus import Trovis557x


async def test_scaling_and_types(trovis: Trovis557x) -> None:
    await trovis.async_update()
    assert trovis.get("trovis_r_modell") == 5579
    assert trovis.get("trovis_r_anlage") == pytest.approx(2.1)
    assert trovis.get("trovis_r_firmware") == pytest.approx(3.05)
    assert trovis.get("trovis_f_AF1") == pytest.approx(12.3)


async def test_int16_negative(trovis: Trovis557x) -> None:
    await trovis.async_update()
    assert trovis.get("trovis_f_VF1") == pytest.approx(-5.0)


async def test_nan_sentinel_becomes_none(trovis: Trovis557x) -> None:
    await trovis.async_update()
    assert trovis.get("trovis_f_SF2") is None


async def test_coils(trovis: Trovis557x) -> None:
    await trovis.async_update()
    assert trovis.get("trovis_hk1_up1") is True
    assert trovis.get("trovis_hk1_tagbetrieb") is True
    assert trovis.get("trovis_r_sammelstoerung") is False


async def test_derived_datetime(trovis: Trovis557x) -> None:
    await trovis.async_update()
    assert trovis.get("trovis_z_datum_formatiert") == "21.06.2026"
    assert trovis.get("trovis_z_uhrzeit_formatiert") == "14:30"
    assert trovis.get("trovis_z_sommerbetrieb_ein_formatiert") == "15.05."
    assert trovis.get("trovis_z_hk4_desinfektionstag_formatiert") == "Mi"
    assert trovis.get("trovis_z_hk4_desinfektionsstart_formatiert") == "19:00"


async def test_derived_switch_and_mode(trovis: Trovis557x) -> None:
    await trovis.async_update()
    assert trovis.get("trovis_r_schalter_oben_formatiert") == "Auto"
    assert trovis.get("trovis_hk1_betriebsart_formatiert") == "Auto"


async def test_derived_hot_water(trovis: Trovis557x) -> None:
    await trovis.async_update()
    # soll 50, schaltdifferenz 10 -> "50-60°"; haltewert 48 -> "48-58°"
    assert trovis.get("trovis_hk4_tagestemperaturen") == "50-60°"
    assert trovis.get("trovis_hk4_nachttemperaturen") == "48-58°"
    # SF1 45.0 + Ueberhoehung 22.0
    assert trovis.get("trovis_hk4_ladetemperatur") == pytest.approx(67.0)


async def test_heating_curve(trovis: Trovis557x) -> None:
    await trovis.async_update()
    curve = trovis.heating_curve(1)
    assert curve is not None
    assert len(curve) == 41
    # day mode on, soll=20, niveau=0, steigung=1.0, clamp [20, 80]
    assert curve[0] == pytest.approx(68.0)   # outside -20 °C
    assert curve[-1] == pytest.approx(24.0)  # outside +20 °C
    assert trovis.curve_x_values == list(range(-20, 21))


async def test_write_register_roundtrip(trovis: Trovis557x) -> None:
    await trovis.async_update()
    await trovis.async_set_register("trovis_hk1_raumsoll_tag", 21.5)
    await trovis.async_update()
    assert trovis.get("trovis_hk1_raumsoll_tag") == pytest.approx(21.5)


async def test_write_coil_roundtrip(trovis: Trovis557x) -> None:
    await trovis.async_update()
    await trovis.async_set_coil("trovis_hk1_standby", True)
    await trovis.async_update()
    assert trovis.get("trovis_hk1_standby") is True


async def test_all_keys_present_after_update(trovis: Trovis557x) -> None:
    await trovis.async_update()
    values = trovis.values
    for key in Trovis557x.all_keys:
        assert key in values
