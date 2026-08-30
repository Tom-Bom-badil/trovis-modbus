"""Tests for public controller identity values."""

from __future__ import annotations

from trovis_modbus import Trovis557x


async def test_device_information_exposes_model_code(
    trovis: Trovis557x,
) -> None:
    """Expose HR40001 independently from the selected controller profile."""
    await trovis.async_update()

    assert trovis.info.model_code is not None
    assert trovis.info.model == f"TROVIS {trovis.info.model_code}"
