"""Tests for static TROVIS hydronic-system definitions."""

from types import MappingProxyType

import pytest

from trovis_modbus import ControlCircuitRole
from trovis_modbus.configurations import (
    BUFFER_TANK_CHARGING_SYSTEM_CODES_BY_MODEL,
    FUNCTIONAL_SENSOR_ROLE_KEYS,
    HYDRONIC_CONFIGURATIONS,
    MODEL_DEFINITIONS,
    SUPPORTED_MODELS_BY_SYSTEM_CODE,
    SUPPORTED_SYSTEM_CODES_BY_MODEL,
    UNDOCUMENTED_SYSTEM_CODES,
    ConfigurationDefinition,
    ConfigurationTopology,
    ControllerModel,
    get_configuration_definition,
)

EXPECTED_SYSTEM_CODES_BY_MODEL = {
    ControllerModel.TROVIS_5573: frozenset(
        {
            10,
            11,
            12,
            13,
            15,
            16,
            19,
            20,
            21,
            22,
            23,
            30,
            35,
            40,
            41,
            45,
            100,
            110,
            111,
            112,
            115,
            116,
            119,
            160,
            161,
            162,
            163,
            164,
            166,
        }
    ),
    ControllerModel.TROVIS_5573_1: frozenset(
        {
            10,
            11,
            12,
            13,
            15,
            16,
            19,
            20,
            21,
            22,
            23,
            30,
            35,
            40,
            41,
            45,
            100,
            110,
            111,
            112,
            115,
            116,
            119,
            160,
            161,
            162,
            163,
            164,
            166,
        }
    ),
    ControllerModel.TROVIS_5575: frozenset(
        {
            10,
            11,
            12,
            13,
            15,
            16,
            19,
            20,
            21,
            22,
            23,
            30,
            31,
            32,
            35,
            40,
            41,
            45,
            100,
            101,
            105,
            110,
            111,
            112,
            115,
            116,
            119,
            160,
            161,
            162,
            163,
            164,
            166,
        }
    ),
    ControllerModel.TROVIS_5576: frozenset(
        {
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
            40,
            41,
            42,
            43,
            45,
            71,
            72,
            81,
            82,
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
            141,
            142,
            143,
            160,
            161,
            162,
            163,
            164,
            166,
        }
    ),
    ControllerModel.TROVIS_5578: frozenset(
        {
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
            210,
            211,
            212,
            219,
            250,
            255,
        }
    ),
    ControllerModel.TROVIS_5578_E: frozenset(
        {
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
    ),
    ControllerModel.TROVIS_5579: frozenset(
        {
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
            40,
            41,
            42,
            43,
            45,
            50,
            51,
            52,
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
            210,
            211,
            212,
            219,
            250,
            255,
        }
    ),
}

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

ROLE_GROUPS = (
    (
        (
            ControlCircuitRole.HEATING,
            ControlCircuitRole.UNUSED,
            ControlCircuitRole.UNUSED,
            ControlCircuitRole.UNUSED,
        ),
        {
            10,
        },
    ),
    (
        (
            ControlCircuitRole.HEATING,
            ControlCircuitRole.UNUSED,
            ControlCircuitRole.UNUSED,
            ControlCircuitRole.DOMESTIC_HOT_WATER,
        ),
        {
            11,
            12,
            13,
            14,
            20,
            21,
            22,
            23,
            24,
            81,
            82,
            110,
            111,
            112,
            113,
            114,
            115,
            116,
            119,
        },
    ),
    (
        (
            ControlCircuitRole.PRECONTROL,
            ControlCircuitRole.UNUSED,
            ControlCircuitRole.UNUSED,
            ControlCircuitRole.DOMESTIC_HOT_WATER,
        ),
        {
            15,
            16,
            17,
            18,
            71,
            72,
        },
    ),
    (
        (
            ControlCircuitRole.UNUSED,
            ControlCircuitRole.UNUSED,
            ControlCircuitRole.UNUSED,
            ControlCircuitRole.DOMESTIC_HOT_WATER,
        ),
        {
            19,
            37,
        },
    ),
    (
        (
            ControlCircuitRole.PRECONTROL,
            ControlCircuitRole.HEATING,
            ControlCircuitRole.UNUSED,
            ControlCircuitRole.UNUSED,
        ),
        {
            30,
        },
    ),
    (
        (
            ControlCircuitRole.PRECONTROL,
            ControlCircuitRole.HEATING,
            ControlCircuitRole.UNUSED,
            ControlCircuitRole.DOMESTIC_HOT_WATER,
        ),
        {
            31,
            32,
            33,
            34,
        },
    ),
    (
        (
            ControlCircuitRole.PRECONTROL,
            ControlCircuitRole.UNUSED,
            ControlCircuitRole.UNUSED,
            ControlCircuitRole.UNUSED,
        ),
        {
            35,
        },
    ),
    (
        (
            ControlCircuitRole.BUFFER_TANK,
            ControlCircuitRole.HEATING,
            ControlCircuitRole.UNUSED,
            ControlCircuitRole.DOMESTIC_HOT_WATER,
        ),
        {
            38,
            39,
            171,
            181,
            271,
        },
    ),
    (
        (
            ControlCircuitRole.HEATING,
            ControlCircuitRole.HEATING,
            ControlCircuitRole.UNUSED,
            ControlCircuitRole.UNUSED,
        ),
        {
            40,
            100,
            190,
        },
    ),
    (
        (
            ControlCircuitRole.HEATING,
            ControlCircuitRole.HEATING,
            ControlCircuitRole.UNUSED,
            ControlCircuitRole.DOMESTIC_HOT_WATER,
        ),
        {
            41,
            42,
            43,
            45,
            101,
            102,
            103,
        },
    ),
    (
        (
            ControlCircuitRole.PRECONTROL,
            ControlCircuitRole.HEATING,
            ControlCircuitRole.HEATING,
            ControlCircuitRole.UNUSED,
        ),
        {
            50,
        },
    ),
    (
        (
            ControlCircuitRole.PRECONTROL,
            ControlCircuitRole.HEATING,
            ControlCircuitRole.HEATING,
            ControlCircuitRole.DOMESTIC_HOT_WATER,
        ),
        {
            51,
            52,
        },
    ),
    (
        (
            ControlCircuitRole.BUFFER_TANK,
            ControlCircuitRole.HEATING,
            ControlCircuitRole.HEATING,
            ControlCircuitRole.DOMESTIC_HOT_WATER,
        ),
        {
            59,
            178,
            278,
        },
    ),
    (
        (
            ControlCircuitRole.HEATING,
            ControlCircuitRole.HEATING,
            ControlCircuitRole.HEATING,
            ControlCircuitRole.UNUSED,
        ),
        {
            60,
            250,
        },
    ),
    (
        (
            ControlCircuitRole.HEATING,
            ControlCircuitRole.HEATING,
            ControlCircuitRole.HEATING,
            ControlCircuitRole.DOMESTIC_HOT_WATER,
        ),
        {
            61,
        },
    ),
    (
        (
            ControlCircuitRole.PRECONTROL,
            ControlCircuitRole.UNUSED,
            ControlCircuitRole.HEATING,
            ControlCircuitRole.DOMESTIC_HOT_WATER,
        ),
        {
            91,
            92,
            120,
            121,
            122,
            129,
        },
    ),
    (
        (
            ControlCircuitRole.HEATING,
            ControlCircuitRole.UNUSED,
            ControlCircuitRole.HEATING,
            ControlCircuitRole.DOMESTIC_HOT_WATER,
        ),
        {
            95,
            96,
            130,
            131,
            132,
            136,
            139,
            210,
            211,
            212,
            219,
        },
    ),
    (
        (
            ControlCircuitRole.PRECONTROL,
            ControlCircuitRole.PRECONTROL,
            ControlCircuitRole.UNUSED,
            ControlCircuitRole.UNUSED,
        ),
        {
            105,
        },
    ),
    (
        (
            ControlCircuitRole.BUFFER_TANK,
            ControlCircuitRole.UNUSED,
            ControlCircuitRole.UNUSED,
            ControlCircuitRole.DOMESTIC_HOT_WATER,
        ),
        {
            141,
            142,
            143,
        },
    ),
    (
        (
            ControlCircuitRole.BUFFER_TANK,
            ControlCircuitRole.UNUSED,
            ControlCircuitRole.HEATING,
            ControlCircuitRole.DOMESTIC_HOT_WATER,
        ),
        {
            150,
            151,
            152,
            153,
            154,
            155,
            200,
        },
    ),
    (
        (
            ControlCircuitRole.BUFFER_TANK,
            ControlCircuitRole.UNUSED,
            ControlCircuitRole.UNUSED,
            ControlCircuitRole.UNUSED,
        ),
        {
            160,
            162,
            163,
            164,
        },
    ),
    (
        (
            ControlCircuitRole.BUFFER_TANK,
            ControlCircuitRole.HEATING,
            ControlCircuitRole.UNUSED,
            ControlCircuitRole.UNUSED,
        ),
        {
            161,
            166,
        },
    ),
    (
        (
            ControlCircuitRole.BUFFER_TANK,
            ControlCircuitRole.UNUSED,
            ControlCircuitRole.HEATING,
            ControlCircuitRole.UNUSED,
        ),
        {
            165,
            167,
        },
    ),
    (
        (
            ControlCircuitRole.BUFFER_TANK,
            ControlCircuitRole.HEATING,
            ControlCircuitRole.HEATING,
            ControlCircuitRole.UNUSED,
        ),
        {
            168,
        },
    ),
    (
        (
            ControlCircuitRole.PRECONTROL,
            ControlCircuitRole.PRECONTROL,
            ControlCircuitRole.PRECONTROL,
            ControlCircuitRole.UNUSED,
        ),
        {
            255,
        },
    ),
)

EXPECTED_CONTROL_CIRCUIT_ROLES = {
    code: roles for roles, system_codes in ROLE_GROUPS for code in system_codes
}


def test_registry_contains_all_system_codes_from_5578_e_sources() -> None:
    assert set(HYDRONIC_CONFIGURATIONS) == EXPECTED_SYSTEM_CODES
    assert isinstance(HYDRONIC_CONFIGURATIONS, MappingProxyType)


def test_documented_system_codes_match_current_model_manuals() -> None:
    assert dict(SUPPORTED_SYSTEM_CODES_BY_MODEL) == (EXPECTED_SYSTEM_CODES_BY_MODEL)
    assert isinstance(SUPPORTED_SYSTEM_CODES_BY_MODEL, MappingProxyType)
    assert isinstance(SUPPORTED_MODELS_BY_SYSTEM_CODE, MappingProxyType)


def test_each_definition_exposes_its_documented_models() -> None:
    for system_code, definition in HYDRONIC_CONFIGURATIONS.items():
        expected_models = frozenset(
            model
            for model, supported_codes in (EXPECTED_SYSTEM_CODES_BY_MODEL.items())
            if system_code in supported_codes
        )
        assert definition.supported_models == expected_models
        assert (
            SUPPORTED_MODELS_BY_SYSTEM_CODE.get(system_code, frozenset())
            == expected_models
        )
        for model in ControllerModel:
            assert definition.supports_model(model) is (model in expected_models)


def test_only_anlage_19_0_is_not_in_current_model_manuals() -> None:
    assert UNDOCUMENTED_SYSTEM_CODES == frozenset({190})
    assert get_configuration_definition(190).supported_models == frozenset()


def test_supported_systems_do_not_exceed_model_rk_capacity() -> None:
    for model, system_codes in SUPPORTED_SYSTEM_CODES_BY_MODEL.items():
        capacity = MODEL_DEFINITIONS[model].control_circuits
        for system_code in system_codes:
            used_rk_slots = tuple(
                index
                for index in get_configuration_definition(
                    system_code
                ).topology.control_circuit_indices
                if index <= 3
            )
            assert max(used_rk_slots, default=0) <= capacity


@pytest.mark.parametrize("system_code", sorted(EXPECTED_SYSTEM_CODES))
def test_configuration_codes_and_display_codes_match(system_code: int) -> None:
    definition = get_configuration_definition(system_code)

    assert definition.code == system_code
    assert definition.display_code == f"{system_code // 10}.{system_code % 10}"


@pytest.mark.parametrize("system_code", sorted(EXPECTED_SYSTEM_CODES))
def test_control_circuit_role_matrix(system_code: int) -> None:
    topology = get_configuration_definition(system_code).topology

    assert topology.control_circuit_roles == EXPECTED_CONTROL_CIRCUIT_ROLES[system_code]


def test_role_matrix_covers_each_system_code_once() -> None:
    grouped_codes = [code for _, system_codes in ROLE_GROUPS for code in system_codes]

    assert set(grouped_codes) == EXPECTED_SYSTEM_CODES
    assert len(grouped_codes) == len(set(grouped_codes))


def test_unknown_system_code_is_rejected() -> None:
    with pytest.raises(KeyError, match="unsupported TROVIS system code number"):
        get_configuration_definition(999)


@pytest.mark.parametrize(
    ("system_code", "expected_topology"),
    (
        (
            10,
            ConfigurationTopology(
                rk1_role=ControlCircuitRole.HEATING,
            ),
        ),
        (
            22,
            ConfigurationTopology(
                rk1_role=ControlCircuitRole.HEATING,
                rk4_role=ControlCircuitRole.DOMESTIC_HOT_WATER,
                circulation=True,
                heat_exchanger=True,
            ),
        ),
        (
            23,
            ConfigurationTopology(
                rk1_role=ControlCircuitRole.HEATING,
                rk4_role=ControlCircuitRole.DOMESTIC_HOT_WATER,
                circulation=True,
                solar=True,
            ),
        ),
        (
            39,
            ConfigurationTopology(
                rk1_role=ControlCircuitRole.BUFFER_TANK,
                rk2_role=ControlCircuitRole.HEATING,
                rk4_role=ControlCircuitRole.DOMESTIC_HOT_WATER,
                circulation=True,
                buffer_tank=True,
            ),
        ),
        (
            50,
            ConfigurationTopology(
                rk1_role=ControlCircuitRole.PRECONTROL,
                rk2_role=ControlCircuitRole.HEATING,
                rk3_role=ControlCircuitRole.HEATING,
            ),
        ),
        (
            116,
            ConfigurationTopology(
                rk1_role=ControlCircuitRole.HEATING,
                rk4_role=ControlCircuitRole.DOMESTIC_HOT_WATER,
                heat_exchanger=True,
            ),
        ),
        (
            136,
            ConfigurationTopology(
                rk1_role=ControlCircuitRole.HEATING,
                rk3_role=ControlCircuitRole.HEATING,
                rk4_role=ControlCircuitRole.DOMESTIC_HOT_WATER,
                heat_exchanger=True,
            ),
        ),
        (
            163,
            ConfigurationTopology(
                rk1_role=ControlCircuitRole.BUFFER_TANK,
                solar=True,
                buffer_tank=True,
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


def test_solar_buffer_system_sensor_roles_follow_current_manuals() -> None:
    assert get_configuration_definition(143).functional_sensor_roles == (
        "af1",
        "vf1",
        "vf4",
        "ruef1",
        "ruef2",
        "sf1",
        "sf2",
        "sf3",
        "sf4",
    )
    assert get_configuration_definition(153).functional_sensor_roles == (
        "af1",
        "af2",
        "vf1",
        "vf3",
        "vf4",
        "ruef1",
        "ruef2",
        "ruef3",
        "rf3",
        "sf1",
        "sf2",
        "sf3",
        "sf4",
    )


def test_definition_rejects_unknown_sensor_role() -> None:
    with pytest.raises(ValueError, match="unsupported functional sensor roles"):
        ConfigurationDefinition(
            code=10,
            display_code="1.0",
            topology=ConfigurationTopology(
                rk1_role=ControlCircuitRole.HEATING,
            ),
            functional_sensor_roles=("hk11",),
        )


def test_topology_exposes_role_native_views() -> None:
    topology = ConfigurationTopology(
        rk1_role=ControlCircuitRole.PRECONTROL,
        rk3_role=ControlCircuitRole.HEATING,
        rk4_role=ControlCircuitRole.DOMESTIC_HOT_WATER,
    )

    assert topology.control_circuit_roles == (
        ControlCircuitRole.PRECONTROL,
        ControlCircuitRole.UNUSED,
        ControlCircuitRole.HEATING,
        ControlCircuitRole.DOMESTIC_HOT_WATER,
    )
    assert topology.control_circuit_indices == (1, 3, 4)
    assert topology.room_heating_circuit_indices == (3,)
    assert topology.has_rk4 is True
    assert topology.control_circuit_role(1) is ControlCircuitRole.PRECONTROL
    assert topology.control_circuit_role(2) is ControlCircuitRole.UNUSED
    assert topology.control_circuit_role(3) is ControlCircuitRole.HEATING
    assert topology.control_circuit_role(4) is ControlCircuitRole.DOMESTIC_HOT_WATER


def test_buffer_tank_role_uses_rk1() -> None:
    topology = ConfigurationTopology(
        rk1_role=ControlCircuitRole.BUFFER_TANK,
    )

    assert topology.control_circuit_indices == (1,)
    assert topology.control_circuit_role(1) is ControlCircuitRole.BUFFER_TANK
    assert topology.room_heating_circuit_indices == ()


@pytest.mark.parametrize(
    ("kwargs", "message"),
    (
        (
            {"rk1_role": ControlCircuitRole.DOMESTIC_HOT_WATER},
            "unsupported role for Rk1",
        ),
        (
            {"rk2_role": ControlCircuitRole.BUFFER_TANK},
            "unsupported role for Rk2",
        ),
        (
            {"rk3_role": ControlCircuitRole.BUFFER_TANK},
            "unsupported role for Rk3",
        ),
        (
            {"rk4_role": ControlCircuitRole.HEATING},
            "unsupported role for Rk4",
        ),
    ),
)
def test_topology_rejects_roles_on_invalid_slots(
    kwargs: dict[str, ControlCircuitRole],
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        ConfigurationTopology(**kwargs)


def test_topology_rejects_invalid_control_circuit_index() -> None:
    topology = ConfigurationTopology(
        rk1_role=ControlCircuitRole.HEATING,
    )

    with pytest.raises(
        ValueError,
        match="control circuit index must be in range 1..4",
    ):
        topology.control_circuit_role(0)

    with pytest.raises(
        ValueError,
        match="control circuit index must be in range 1..4",
    ):
        topology.control_circuit_role(5)


def test_buffer_tank_charging_parameter_support_matches_manuals() -> None:
    expected = {
        ControllerModel.TROVIS_5573: {160, 161, 162, 163, 164, 166},
        ControllerModel.TROVIS_5573_1: {160, 161, 162, 163, 164, 166},
        ControllerModel.TROVIS_5575: {160, 161, 162, 163, 164, 166},
        ControllerModel.TROVIS_5576: {160, 161, 162, 163, 164, 166},
        ControllerModel.TROVIS_5578: {
            39,
            59,
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
        },
        ControllerModel.TROVIS_5578_E: {
            38,
            39,
            59,
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
            200,
        },
        ControllerModel.TROVIS_5579: {
            160,
            161,
            162,
            163,
            164,
            165,
            166,
            167,
            168,
        },
    }

    assert {
        model: set(codes)
        for model, codes in BUFFER_TANK_CHARGING_SYSTEM_CODES_BY_MODEL.items()
    } == expected

    assert HYDRONIC_CONFIGURATIONS[161].supports_buffer_tank_charging_parameters(
        ControllerModel.TROVIS_5576
    )
    assert not HYDRONIC_CONFIGURATIONS[141].supports_buffer_tank_charging_parameters(
        ControllerModel.TROVIS_5576
    )
    assert not HYDRONIC_CONFIGURATIONS[271].supports_buffer_tank_charging_parameters(
        ControllerModel.TROVIS_5578_E
    )
