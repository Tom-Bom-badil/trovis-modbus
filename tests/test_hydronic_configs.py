"""Tests for static TROVIS hydronic-configuration definitions."""

from types import MappingProxyType

import pytest

from trovis_modbus.hydronic_configs import (
    FUNCTIONAL_SENSOR_ROLE_KEYS,
    HYDRONIC_CONFIGURATIONS,
    ConfigurationDefinition,
    ConfigurationTopology,
    get_configuration_definition,
)

EXPECTED_SYSTEM_CODES = {
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    21,
    22,
    23,
    24,
    30,
    31,
    32,
    33,
    34,
    35,
    37,
    38,
    39,
    40,
    41,
    42,
    43,
    45,
    50,
    51,
    52,
    59,
    60,
    61,
    71,
    72,
    81,
    82,
    91,
    92,
    95,
    96,
    100,
    101,
    102,
    103,
    105,
    110,
    111,
    112,
    113,
    114,
    115,
    116,
    119,
    120,
    121,
    122,
    129,
    130,
    131,
    132,
    136,
    139,
    141,
    142,
    143,
    150,
    151,
    152,
    153,
    154,
    155,
    160,
    161,
    162,
    163,
    164,
    165,
    166,
    167,
    168,
    171,
    178,
    181,
    190,
    200,
    210,
    211,
    212,
    219,
    250,
    255,
    271,
    278,
}


def test_registry_contains_all_system_codes_from_5578_e_sources() -> None:
    assert set(HYDRONIC_CONFIGURATIONS) == EXPECTED_SYSTEM_CODES
    assert isinstance(HYDRONIC_CONFIGURATIONS, MappingProxyType)


@pytest.mark.parametrize("system_code", sorted(EXPECTED_SYSTEM_CODES))
def test_configuration_codes_and_display_codes_match(system_code: int) -> None:
    definition = get_configuration_definition(system_code)

    assert definition.code == system_code
    assert definition.display_code == f"{system_code // 10}.{system_code % 10}"


def test_unknown_system_code_is_rejected() -> None:
    with pytest.raises(KeyError, match="unsupported TROVIS system code number"):
        get_configuration_definition(999)


@pytest.mark.parametrize(
    ("system_code", "expected_topology"),
    (
        (
            10,
            ConfigurationTopology(hk1=True),
        ),
        (
            22,
            ConfigurationTopology(
                hk1=True,
                ww=True,
                circulation=True,
                heat_exchanger=True,
            ),
        ),
        (
            23,
            ConfigurationTopology(
                hk1=True,
                ww=True,
                circulation=True,
                solar=True,
            ),
        ),
        (
            39,
            ConfigurationTopology(
                hk1=True,
                hk2=True,
                ww=True,
                circulation=True,
                buffer_storage=True,
            ),
        ),
        (
            50,
            ConfigurationTopology(hk1=True, hk2=True, hk3=True),
        ),
        (
            116,
            ConfigurationTopology(
                hk1=True,
                ww=True,
                circulation=True,
                heat_exchanger=True,
            ),
        ),
        (
            163,
            ConfigurationTopology(
                hk1=True,
                solar=True,
                buffer_storage=True,
            ),
        ),
    ),
)
def test_representative_topologies(
    system_code: int,
    expected_topology: ConfigurationTopology,
) -> None:
    assert get_configuration_definition(system_code).topology == expected_topology


def test_functional_sensor_roles_are_known_and_unique() -> None:
    allowed_roles = set(FUNCTIONAL_SENSOR_ROLE_KEYS)

    for definition in HYDRONIC_CONFIGURATIONS.values():
        assert len(definition.functional_sensor_roles) == len(
            set(definition.functional_sensor_roles)
        )
        assert set(definition.functional_sensor_roles) <= allowed_roles


def test_anlage_2_sensor_roles_follow_the_source_matrix() -> None:
    assert get_configuration_definition(21).functional_sensor_roles == (
        "af1",
        "vf1",
        "vf4",
        "ruef1",
        "rf1",
        "sf1",
        "sf2",
    )
    assert get_configuration_definition(23).functional_sensor_roles == (
        "af1",
        "vf1",
        "vf3",
        "vf4",
        "ruef1",
        "rf1",
        "sf1",
        "sf2",
        "sf3",
    )


def test_definition_rejects_unknown_sensor_role() -> None:
    with pytest.raises(ValueError, match="unsupported functional sensor roles"):
        ConfigurationDefinition(
            code=10,
            display_code="1.0",
            topology=ConfigurationTopology(hk1=True),
            functional_sensor_roles=("hk11",),
        )
