"""Cross-check the catalog against the original Trovis 557x YAML package.

This is the /goal verification: every register, coil and (device-meaningful)
template sensor in the upstream YAML must be reproduced — same address, scale,
data type, unit and NaN sentinel.

The reference repo is cloned to /tmp/trovis-ref. If it is absent the parity
tests skip (the rest of the suite still runs).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import yaml

from trovis_modbus.catalog import COILS_BY_KEY, DERIVED, REGISTERS_BY_KEY

REF = Path("/tmp/trovis-ref/HomeAssistant/trovis557x")

pytestmark = pytest.mark.skipif(
    not REF.exists(), reason="reference YAML not cloned to /tmp/trovis-ref"
)


class _IgnoreSecret(yaml.SafeLoader):
    pass


_IgnoreSecret.add_constructor("!secret", lambda loader, node: f"secret:{node.value}")


def _load_entities(subdir: str) -> list[dict[str, Any]]:
    entities: list[dict[str, Any]] = []
    for path in sorted((REF / subdir).glob("*.yaml")):
        loaded = yaml.load(path.read_text(), Loader=_IgnoreSecret)
        if isinstance(loaded, list):
            entities.extend(item for item in loaded if isinstance(item, dict))
    return entities


def _template_unique_ids() -> set[str]:
    ids: set[str] = set()
    for name in ("template_sensors.yaml", "heating_curves.yaml"):
        loaded = yaml.load((REF / name).read_text(), Loader=_IgnoreSecret)
        for block in loaded:
            for sensor in (block.get("sensors") or {}).values():
                if isinstance(sensor, dict) and "unique_id" in sensor:
                    ids.add(sensor["unique_id"])
    return ids


# Pure-dashboard template sensors that are not device data (they read other HA
# entities / input_number helpers, not the controller). Intentionally excluded.
EXCLUDED_UI_KEYS = {
    "trovis_r_gesamtstatus",
    "trovis_r_button_1_click",
    "trovis_r_button_1_doubleclick",
    "trovis_r_button_2_click",
    "trovis_r_button_2_doubleclick",
    "trovis_r_button_3_click",
    "trovis_r_button_3_doubleclick",
}


def test_every_register_reproduced() -> None:
    yaml_registers = _load_entities("registers")
    yaml_keys = {e["unique_id"] for e in yaml_registers}
    assert yaml_keys == set(REGISTERS_BY_KEY), (
        f"missing: {yaml_keys - set(REGISTERS_BY_KEY)}; "
        f"extra: {set(REGISTERS_BY_KEY) - yaml_keys}"
    )


def test_every_coil_reproduced() -> None:
    yaml_coils = _load_entities("coils")
    yaml_keys = {e["unique_id"] for e in yaml_coils}
    assert yaml_keys == set(COILS_BY_KEY), (
        f"missing: {yaml_keys - set(COILS_BY_KEY)}; "
        f"extra: {set(COILS_BY_KEY) - yaml_keys}"
    )


@pytest.mark.parametrize(
    "entity", _load_entities("registers"), ids=lambda e: e["unique_id"]
)
def test_register_attributes_match(entity: dict[str, Any]) -> None:
    register = REGISTERS_BY_KEY[entity["unique_id"]]
    assert register.address == entity["address"]
    assert register.scale == entity.get("scale", 1.0)
    assert register.nan_value == entity.get("nan_value")
    assert register.unit == entity.get("unit_of_measurement")
    assert register.precision == entity.get("precision")
    if "data_type" in entity:
        assert register.data_type == entity["data_type"]
    if "min_value" in entity:
        assert register.min_value == entity["min_value"]
    if "max_value" in entity:
        assert register.max_value == entity["max_value"]


@pytest.mark.parametrize(
    "entity", _load_entities("coils"), ids=lambda e: e["unique_id"]
)
def test_coil_attributes_match(entity: dict[str, Any]) -> None:
    coil = COILS_BY_KEY[entity["unique_id"]]
    assert coil.address == entity["address"]


def test_template_sensors_accounted_for() -> None:
    template_ids = _template_unique_ids()
    derived_keys = {d.key for d in DERIVED}
    unaccounted = template_ids - derived_keys - EXCLUDED_UI_KEYS
    assert not unaccounted, (
        f"template sensors neither derived nor excluded: {unaccounted}"
    )
