"""Static hydronic configurations selected by TROVIS system code numbers.

All supported Anlagenkennziffern are intentionally kept in one module. The
manufacturer-oriented comments above every definition remain the navigation
anchors for this large configuration table.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType

FUNCTIONAL_SENSOR_ROLE_KEYS = (
    "af1",
    "af2",
    "vf1",
    "vf2",
    "vf3",
    "vf4",
    "ruef1",
    "ruef2",
    "ruef3",
    "rf1",
    "rf2",
    "rf3",
    "sf1",
    "sf2",
    "sf3",
)

_FUNCTIONAL_SENSOR_ROLE_KEY_SET = frozenset(FUNCTIONAL_SENSOR_ROLE_KEYS)


@dataclass(frozen=True, slots=True)
class ConfigurationTopology:
    """Static hydronic topology selected by one system code number."""

    hk1: bool = False
    hk2: bool = False
    hk3: bool = False
    ww: bool = False
    circulation: bool = False
    solar: bool = False
    buffer_storage: bool = False
    heat_exchanger: bool = False

    def __post_init__(self) -> None:
        if not any(
            (
                self.hk1,
                self.hk2,
                self.hk3,
                self.ww,
                self.circulation,
                self.solar,
                self.buffer_storage,
                self.heat_exchanger,
            )
        ):
            raise ValueError(
                "a configuration topology must contain at least one feature"
            )


@dataclass(frozen=True, slots=True)
class ConfigurationDefinition:
    """Static meaning of one TROVIS system code number.

    ``functional_sensor_roles`` lists sensor roles that may be used by the
    selected hydronic configuration. It does not describe which physical
    sensors are connected and must not hide additional free measurements.
    """

    code: int
    display_code: str
    topology: ConfigurationTopology
    functional_sensor_roles: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.code <= 0:
            raise ValueError("code must be positive")

        expected_display_code = f"{self.code // 10}.{self.code % 10}"
        if self.display_code != expected_display_code:
            raise ValueError(
                f"display_code {self.display_code!r} does not match code "
                f"{self.code}: expected {expected_display_code!r}"
            )

        if len(set(self.functional_sensor_roles)) != len(self.functional_sensor_roles):
            raise ValueError(
                f"duplicate functional sensor roles for Anlage {self.display_code}"
            )

        unsupported_roles = (
            set(self.functional_sensor_roles) - _FUNCTIONAL_SENSOR_ROLE_KEY_SET
        )
        if unsupported_roles:
            raise ValueError(
                f"unsupported functional sensor roles for Anlage "
                f"{self.display_code}: {sorted(unsupported_roles)}"
            )


# ---------------------------------------------------------------------------
# Anlagenkennziffern
# ---------------------------------------------------------------------------

# ########### Anlage 1.0 #############
ANLAGE_1_0 = ConfigurationDefinition(
    code=10,
    display_code="1.0",
    topology=ConfigurationTopology(
        hk1=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf1",
        "ruef1",
        "rf1",
    ),
)


# ########### Anlage 1.1 #############
ANLAGE_1_1 = ConfigurationDefinition(
    code=11,
    display_code="1.1",
    topology=ConfigurationTopology(
        hk1=True,
        ww=True,
        circulation=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf1",
        "vf4",
        "ruef1",
        "rf1",
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 1.2 #############
ANLAGE_1_2 = ConfigurationDefinition(
    code=12,
    display_code="1.2",
    topology=ConfigurationTopology(
        hk1=True,
        ww=True,
        circulation=True,
        heat_exchanger=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf1",
        "vf4",
        "ruef1",
        "rf1",
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 1.3 #############
ANLAGE_1_3 = ConfigurationDefinition(
    code=13,
    display_code="1.3",
    topology=ConfigurationTopology(
        hk1=True,
        ww=True,
        circulation=True,
        solar=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf1",
        "vf3",
        "vf4",
        "ruef1",
        "rf1",
        "sf1",
        "sf2",
        "sf3",
    ),
)


# ########### Anlage 1.4 #############
ANLAGE_1_4 = ConfigurationDefinition(
    code=14,
    display_code="1.4",
    topology=ConfigurationTopology(
        hk1=True,
        ww=True,
        circulation=True,
        solar=True,
        heat_exchanger=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf1",
        "vf3",
        "vf4",
        "ruef1",
        "rf1",
        "sf1",
        "sf2",
        "sf3",
    ),
)


# ########### Anlage 1.5 #############
ANLAGE_1_5 = ConfigurationDefinition(
    code=15,
    display_code="1.5",
    topology=ConfigurationTopology(
        hk1=True,
        ww=True,
        circulation=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf1",
        "vf4",
        "ruef1",
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 1.6 #############
ANLAGE_1_6 = ConfigurationDefinition(
    code=16,
    display_code="1.6",
    topology=ConfigurationTopology(
        hk1=True,
        ww=True,
        circulation=True,
        heat_exchanger=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf1",
        "vf4",
        "ruef1",
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 1.7 #############
ANLAGE_1_7 = ConfigurationDefinition(
    code=17,
    display_code="1.7",
    topology=ConfigurationTopology(
        hk1=True,
        ww=True,
        circulation=True,
        solar=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf1",
        "vf3",
        "vf4",
        "ruef1",
        "sf1",
        "sf2",
        "sf3",
    ),
)


# ########### Anlage 1.8 #############
ANLAGE_1_8 = ConfigurationDefinition(
    code=18,
    display_code="1.8",
    topology=ConfigurationTopology(
        hk1=True,
        ww=True,
        circulation=True,
        solar=True,
        heat_exchanger=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf1",
        "vf3",
        "vf4",
        "ruef1",
        "sf1",
        "sf2",
        "sf3",
    ),
)


# ########### Anlage 1.9 #############
ANLAGE_1_9 = ConfigurationDefinition(
    code=19,
    display_code="1.9",
    topology=ConfigurationTopology(
        ww=True,
        circulation=True,
        heat_exchanger=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf2",
        "vf4",
        "ruef2",
        "sf1",
        "sf2",
    ),
)


ANLAGEN_1 = (
    ANLAGE_1_0,
    ANLAGE_1_1,
    ANLAGE_1_2,
    ANLAGE_1_3,
    ANLAGE_1_4,
    ANLAGE_1_5,
    ANLAGE_1_6,
    ANLAGE_1_7,
    ANLAGE_1_8,
    ANLAGE_1_9,
)

# ########### Anlage 2.0 #############
ANLAGE_2_0 = ConfigurationDefinition(
    code=20,
    display_code="2.0",
    topology=ConfigurationTopology(
        hk1=True,
        ww=True,
        circulation=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf1",
        "vf4",
        "ruef1",
        "rf1",
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 2.1 #############
ANLAGE_2_1 = ConfigurationDefinition(
    code=21,
    display_code="2.1",
    topology=ConfigurationTopology(
        hk1=True,
        ww=True,
        circulation=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf1",
        "vf4",
        "ruef1",
        "rf1",
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 2.2 #############
ANLAGE_2_2 = ConfigurationDefinition(
    code=22,
    display_code="2.2",
    topology=ConfigurationTopology(
        hk1=True,
        ww=True,
        circulation=True,
        heat_exchanger=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf1",
        "vf4",
        "ruef1",
        "rf1",
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 2.3 #############
ANLAGE_2_3 = ConfigurationDefinition(
    code=23,
    display_code="2.3",
    topology=ConfigurationTopology(
        hk1=True,
        ww=True,
        circulation=True,
        solar=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf1",
        "vf3",
        "vf4",
        "ruef1",
        "rf1",
        "sf1",
        "sf2",
        "sf3",
    ),
)


# ########### Anlage 2.4 #############
ANLAGE_2_4 = ConfigurationDefinition(
    code=24,
    display_code="2.4",
    topology=ConfigurationTopology(
        hk1=True,
        ww=True,
        circulation=True,
        solar=True,
        heat_exchanger=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf1",
        "vf3",
        "vf4",
        "ruef1",
        "rf1",
        "sf1",
        "sf2",
        "sf3",
    ),
)


ANLAGEN_2 = (
    ANLAGE_2_0,
    ANLAGE_2_1,
    ANLAGE_2_2,
    ANLAGE_2_3,
    ANLAGE_2_4,
)

# ########### Anlage 3.0 #############
ANLAGE_3_0 = ConfigurationDefinition(
    code=30,
    display_code="3.0",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "ruef1",
        "ruef2",
        "rf2",
    ),
)


# ########### Anlage 3.1 #############
ANLAGE_3_1 = ConfigurationDefinition(
    code=31,
    display_code="3.1",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
        ww=True,
        circulation=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf4",
        "ruef1",
        "ruef2",
        "rf2",
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 3.2 #############
ANLAGE_3_2 = ConfigurationDefinition(
    code=32,
    display_code="3.2",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
        ww=True,
        circulation=True,
        heat_exchanger=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf4",
        "ruef1",
        "ruef2",
        "rf2",
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 3.3 #############
ANLAGE_3_3 = ConfigurationDefinition(
    code=33,
    display_code="3.3",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
        ww=True,
        circulation=True,
        solar=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf3",
        "vf4",
        "ruef1",
        "ruef2",
        "rf2",
        "sf1",
        "sf2",
        "sf3",
    ),
)


# ########### Anlage 3.4 #############
ANLAGE_3_4 = ConfigurationDefinition(
    code=34,
    display_code="3.4",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
        ww=True,
        circulation=True,
        solar=True,
        heat_exchanger=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf3",
        "vf4",
        "ruef1",
        "ruef2",
        "rf2",
        "sf1",
        "sf2",
        "sf3",
    ),
)


# ########### Anlage 3.5 #############
ANLAGE_3_5 = ConfigurationDefinition(
    code=35,
    display_code="3.5",
    topology=ConfigurationTopology(
        hk1=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf1",
        "ruef1",
    ),
)


# ########### Anlage 3.7 #############
ANLAGE_3_7 = ConfigurationDefinition(
    code=37,
    display_code="3.7",
    topology=ConfigurationTopology(
        ww=True,
        circulation=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf4",
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 3.8 #############
ANLAGE_3_8 = ConfigurationDefinition(
    code=38,
    display_code="3.8",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
        ww=True,
        circulation=True,
        buffer_storage=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf4",
        "ruef1",
        "ruef2",
        "rf2",
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 3.9 #############
ANLAGE_3_9 = ConfigurationDefinition(
    code=39,
    display_code="3.9",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
        ww=True,
        circulation=True,
        buffer_storage=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf4",
        "ruef1",
        "ruef2",
        "rf2",
        "sf1",
        "sf2",
    ),
)


ANLAGEN_3 = (
    ANLAGE_3_0,
    ANLAGE_3_1,
    ANLAGE_3_2,
    ANLAGE_3_3,
    ANLAGE_3_4,
    ANLAGE_3_5,
    ANLAGE_3_7,
    ANLAGE_3_8,
    ANLAGE_3_9,
)

# ########### Anlage 4.0 #############
ANLAGE_4_0 = ConfigurationDefinition(
    code=40,
    display_code="4.0",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "ruef1",
        "ruef2",
        "rf1",
        "rf2",
    ),
)


# ########### Anlage 4.1 #############
ANLAGE_4_1 = ConfigurationDefinition(
    code=41,
    display_code="4.1",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
        ww=True,
        circulation=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf4",
        "ruef1",
        "ruef2",
        "rf1",
        "rf2",
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 4.2 #############
ANLAGE_4_2 = ConfigurationDefinition(
    code=42,
    display_code="4.2",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
        ww=True,
        circulation=True,
        heat_exchanger=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf4",
        "ruef1",
        "ruef2",
        "rf1",
        "rf2",
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 4.3 #############
ANLAGE_4_3 = ConfigurationDefinition(
    code=43,
    display_code="4.3",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
        ww=True,
        circulation=True,
        solar=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf3",
        "vf4",
        "ruef1",
        "ruef2",
        "rf1",
        "rf2",
        "sf1",
        "sf2",
        "sf3",
    ),
)


# ########### Anlage 4.5 #############
ANLAGE_4_5 = ConfigurationDefinition(
    code=45,
    display_code="4.5",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
        ww=True,
        circulation=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf4",
        "ruef1",
        "ruef2",
        "rf1",
        "rf2",
        "sf1",
        "sf2",
    ),
)


ANLAGEN_4 = (
    ANLAGE_4_0,
    ANLAGE_4_1,
    ANLAGE_4_2,
    ANLAGE_4_3,
    ANLAGE_4_5,
)

# ########### Anlage 5.0 #############
ANLAGE_5_0 = ConfigurationDefinition(
    code=50,
    display_code="5.0",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
        hk3=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf3",
        "ruef1",
        "ruef2",
        "ruef3",
        "rf2",
        "rf3",
    ),
)


# ########### Anlage 5.1 #############
ANLAGE_5_1 = ConfigurationDefinition(
    code=51,
    display_code="5.1",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
        hk3=True,
        ww=True,
        circulation=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf3",
        "vf4",
        "ruef1",
        "ruef2",
        "ruef3",
        "rf2",
        "rf3",
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 5.2 #############
ANLAGE_5_2 = ConfigurationDefinition(
    code=52,
    display_code="5.2",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
        hk3=True,
        ww=True,
        circulation=True,
        heat_exchanger=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf3",
        "vf4",
        "ruef1",
        "ruef2",
        "ruef3",
        "rf2",
        "rf3",
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 5.9 #############
ANLAGE_5_9 = ConfigurationDefinition(
    code=59,
    display_code="5.9",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
        hk3=True,
        ww=True,
        circulation=True,
        buffer_storage=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf3",
        "vf4",
        "ruef1",
        "ruef2",
        "ruef3",
        "rf2",
        "rf3",
        "sf1",
        "sf2",
    ),
)


ANLAGEN_5 = (
    ANLAGE_5_0,
    ANLAGE_5_1,
    ANLAGE_5_2,
    ANLAGE_5_9,
)

# ########### Anlage 6.0 #############
ANLAGE_6_0 = ConfigurationDefinition(
    code=60,
    display_code="6.0",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
        hk3=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf3",
        "ruef1",
        "ruef2",
        "ruef3",
        "rf1",
        "rf2",
        "rf3",
    ),
)


# ########### Anlage 6.1 #############
ANLAGE_6_1 = ConfigurationDefinition(
    code=61,
    display_code="6.1",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
        hk3=True,
        ww=True,
        circulation=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf3",
        "vf4",
        "ruef1",
        "ruef2",
        "ruef3",
        "rf1",
        "rf2",
        "rf3",
        "sf1",
        "sf2",
    ),
)


ANLAGEN_6 = (
    ANLAGE_6_0,
    ANLAGE_6_1,
)

# ########### Anlage 7.1 #############
ANLAGE_7_1 = ConfigurationDefinition(
    code=71,
    display_code="7.1",
    topology=ConfigurationTopology(
        hk1=True,
        ww=True,
        circulation=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf1",
        "vf2",
        "vf4",
        "ruef1",
        "ruef2",
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 7.2 #############
ANLAGE_7_2 = ConfigurationDefinition(
    code=72,
    display_code="7.2",
    topology=ConfigurationTopology(
        hk1=True,
        ww=True,
        circulation=True,
        heat_exchanger=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf1",
        "vf2",
        "vf4",
        "ruef1",
        "ruef2",
        "sf1",
        "sf2",
    ),
)


ANLAGEN_7 = (
    ANLAGE_7_1,
    ANLAGE_7_2,
)

# ########### Anlage 8.1 #############
ANLAGE_8_1 = ConfigurationDefinition(
    code=81,
    display_code="8.1",
    topology=ConfigurationTopology(
        hk1=True,
        ww=True,
        circulation=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf1",
        "vf2",
        "vf4",
        "ruef1",
        "ruef2",
        "rf1",
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 8.2 #############
ANLAGE_8_2 = ConfigurationDefinition(
    code=82,
    display_code="8.2",
    topology=ConfigurationTopology(
        hk1=True,
        ww=True,
        circulation=True,
        heat_exchanger=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf1",
        "vf2",
        "vf4",
        "ruef1",
        "ruef2",
        "rf1",
        "sf1",
        "sf2",
    ),
)


ANLAGEN_8 = (
    ANLAGE_8_1,
    ANLAGE_8_2,
)

# ########### Anlage 9.1 #############
ANLAGE_9_1 = ConfigurationDefinition(
    code=91,
    display_code="9.1",
    topology=ConfigurationTopology(
        hk1=True,
        hk3=True,
        ww=True,
        circulation=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf3",
        "vf4",
        "ruef1",
        "ruef2",
        "ruef3",
        "rf3",
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 9.2 #############
ANLAGE_9_2 = ConfigurationDefinition(
    code=92,
    display_code="9.2",
    topology=ConfigurationTopology(
        hk1=True,
        hk3=True,
        ww=True,
        circulation=True,
        heat_exchanger=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf3",
        "vf4",
        "ruef1",
        "ruef2",
        "ruef3",
        "rf3",
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 9.5 #############
ANLAGE_9_5 = ConfigurationDefinition(
    code=95,
    display_code="9.5",
    topology=ConfigurationTopology(
        hk1=True,
        hk3=True,
        ww=True,
        circulation=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf3",
        "vf4",
        "ruef1",
        "ruef2",
        "ruef3",
        "rf1",
        "rf3",
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 9.6 #############
ANLAGE_9_6 = ConfigurationDefinition(
    code=96,
    display_code="9.6",
    topology=ConfigurationTopology(
        hk1=True,
        hk3=True,
        ww=True,
        circulation=True,
        heat_exchanger=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf3",
        "vf4",
        "ruef1",
        "ruef2",
        "ruef3",
        "rf1",
        "rf3",
        "sf1",
        "sf2",
    ),
)


ANLAGEN_9 = (
    ANLAGE_9_1,
    ANLAGE_9_2,
    ANLAGE_9_5,
    ANLAGE_9_6,
)

# ########### Anlage 10.0 #############
ANLAGE_10_0 = ConfigurationDefinition(
    code=100,
    display_code="10.0",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "ruef1",
        "ruef2",
        "rf1",
        "rf2",
    ),
)


# ########### Anlage 10.1 #############
ANLAGE_10_1 = ConfigurationDefinition(
    code=101,
    display_code="10.1",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
        ww=True,
        circulation=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf4",
        "ruef1",
        "ruef2",
        "rf1",
        "rf2",
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 10.2 #############
ANLAGE_10_2 = ConfigurationDefinition(
    code=102,
    display_code="10.2",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
        ww=True,
        circulation=True,
        heat_exchanger=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf4",
        "ruef1",
        "ruef2",
        "rf1",
        "rf2",
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 10.3 #############
ANLAGE_10_3 = ConfigurationDefinition(
    code=103,
    display_code="10.3",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
        ww=True,
        circulation=True,
        solar=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf3",
        "vf4",
        "ruef1",
        "ruef2",
        "rf1",
        "rf2",
        "sf1",
        "sf2",
        "sf3",
    ),
)


# ########### Anlage 10.5 #############
ANLAGE_10_5 = ConfigurationDefinition(
    code=105,
    display_code="10.5",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "ruef1",
        "ruef2",
    ),
)


ANLAGEN_10 = (
    ANLAGE_10_0,
    ANLAGE_10_1,
    ANLAGE_10_2,
    ANLAGE_10_3,
    ANLAGE_10_5,
)

# ########### Anlage 11.0 #############
ANLAGE_11_0 = ConfigurationDefinition(
    code=110,
    display_code="11.0",
    topology=ConfigurationTopology(
        hk1=True,
        ww=True,
        circulation=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf1",
        "vf4",
        "ruef1",
        "ruef2",
        "rf1",
        "sf1",
    ),
)


# ########### Anlage 11.1 #############
ANLAGE_11_1 = ConfigurationDefinition(
    code=111,
    display_code="11.1",
    topology=ConfigurationTopology(
        hk1=True,
        ww=True,
        circulation=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf1",
        "vf2",
        "vf4",
        "ruef1",
        "ruef2",
        "rf1",
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 11.2 #############
ANLAGE_11_2 = ConfigurationDefinition(
    code=112,
    display_code="11.2",
    topology=ConfigurationTopology(
        hk1=True,
        ww=True,
        circulation=True,
        heat_exchanger=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf1",
        "vf2",
        "vf4",
        "ruef1",
        "ruef2",
        "rf1",
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 11.3 #############
ANLAGE_11_3 = ConfigurationDefinition(
    code=113,
    display_code="11.3",
    topology=ConfigurationTopology(
        hk1=True,
        ww=True,
        circulation=True,
        solar=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf1",
        "vf3",
        "vf4",
        "ruef1",
        "ruef2",
        "rf1",
        "sf1",
        "sf3",
    ),
)


# ########### Anlage 11.4 #############
ANLAGE_11_4 = ConfigurationDefinition(
    code=114,
    display_code="11.4",
    topology=ConfigurationTopology(
        hk1=True,
        ww=True,
        circulation=True,
        solar=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf1",
        "vf2",
        "vf3",
        "vf4",
        "ruef1",
        "ruef2",
        "rf1",
        "sf1",
        "sf2",
        "sf3",
    ),
)


# ########### Anlage 11.5 #############
ANLAGE_11_5 = ConfigurationDefinition(
    code=115,
    display_code="11.5",
    topology=ConfigurationTopology(
        hk1=True,
        ww=True,
        circulation=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf1",
        "vf2",
        "vf4",
        "ruef1",
        "ruef2",
        "rf1",
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 11.6 #############
ANLAGE_11_6 = ConfigurationDefinition(
    code=116,
    display_code="11.6",
    topology=ConfigurationTopology(
        hk1=True,
        ww=True,
        circulation=True,
        heat_exchanger=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf1",
        "vf2",
        "vf4",
        "ruef1",
        "ruef2",
        "rf1",
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 11.9 #############
ANLAGE_11_9 = ConfigurationDefinition(
    code=119,
    display_code="11.9",
    topology=ConfigurationTopology(
        hk1=True,
        ww=True,
        circulation=True,
        heat_exchanger=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf1",
        "vf2",
        "vf4",
        "ruef1",
        "ruef2",
        "rf1",
        "sf1",
        "sf2",
    ),
)


ANLAGEN_11 = (
    ANLAGE_11_0,
    ANLAGE_11_1,
    ANLAGE_11_2,
    ANLAGE_11_3,
    ANLAGE_11_4,
    ANLAGE_11_5,
    ANLAGE_11_6,
    ANLAGE_11_9,
)

# ########### Anlage 12.0 #############
ANLAGE_12_0 = ConfigurationDefinition(
    code=120,
    display_code="12.0",
    topology=ConfigurationTopology(
        hk1=True,
        hk3=True,
        ww=True,
        circulation=True,
    ),
    functional_sensor_roles=(
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
    ),
)


# ########### Anlage 12.1 #############
ANLAGE_12_1 = ConfigurationDefinition(
    code=121,
    display_code="12.1",
    topology=ConfigurationTopology(
        hk1=True,
        hk3=True,
        ww=True,
        circulation=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf3",
        "vf4",
        "ruef1",
        "ruef2",
        "ruef3",
        "rf3",
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 12.2 #############
ANLAGE_12_2 = ConfigurationDefinition(
    code=122,
    display_code="12.2",
    topology=ConfigurationTopology(
        hk1=True,
        hk3=True,
        ww=True,
        circulation=True,
        heat_exchanger=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf3",
        "vf4",
        "ruef1",
        "ruef2",
        "ruef3",
        "rf3",
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 12.9 #############
ANLAGE_12_9 = ConfigurationDefinition(
    code=129,
    display_code="12.9",
    topology=ConfigurationTopology(
        hk1=True,
        hk3=True,
        ww=True,
        circulation=True,
        heat_exchanger=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf3",
        "vf4",
        "ruef1",
        "ruef2",
        "ruef3",
        "rf3",
        "sf1",
        "sf2",
    ),
)


ANLAGEN_12 = (
    ANLAGE_12_0,
    ANLAGE_12_1,
    ANLAGE_12_2,
    ANLAGE_12_9,
)

# ########### Anlage 13.0 #############
ANLAGE_13_0 = ConfigurationDefinition(
    code=130,
    display_code="13.0",
    topology=ConfigurationTopology(
        hk1=True,
        hk3=True,
        ww=True,
        circulation=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf3",
        "vf4",
        "ruef1",
        "ruef2",
        "ruef3",
        "rf1",
        "rf3",
        "sf1",
    ),
)


# ########### Anlage 13.1 #############
ANLAGE_13_1 = ConfigurationDefinition(
    code=131,
    display_code="13.1",
    topology=ConfigurationTopology(
        hk1=True,
        hk3=True,
        ww=True,
        circulation=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf3",
        "vf4",
        "ruef1",
        "ruef2",
        "ruef3",
        "rf1",
        "rf3",
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 13.2 #############
ANLAGE_13_2 = ConfigurationDefinition(
    code=132,
    display_code="13.2",
    topology=ConfigurationTopology(
        hk1=True,
        hk3=True,
        ww=True,
        circulation=True,
        heat_exchanger=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf3",
        "vf4",
        "ruef1",
        "ruef2",
        "ruef3",
        "rf1",
        "rf3",
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 13.6 #############
ANLAGE_13_6 = ConfigurationDefinition(
    code=136,
    display_code="13.6",
    topology=ConfigurationTopology(
        hk1=True,
        hk3=True,
        ww=True,
        circulation=True,
        heat_exchanger=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf3",
        "vf4",
        "ruef1",
        "ruef2",
        "ruef3",
        "rf1",
        "rf3",
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 13.9 #############
ANLAGE_13_9 = ConfigurationDefinition(
    code=139,
    display_code="13.9",
    topology=ConfigurationTopology(
        hk1=True,
        hk3=True,
        ww=True,
        circulation=True,
        heat_exchanger=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf3",
        "vf4",
        "ruef1",
        "ruef2",
        "ruef3",
        "rf1",
        "rf3",
        "sf1",
        "sf2",
    ),
)


ANLAGEN_13 = (
    ANLAGE_13_0,
    ANLAGE_13_1,
    ANLAGE_13_2,
    ANLAGE_13_6,
    ANLAGE_13_9,
)

# ########### Anlage 14.1 #############
ANLAGE_14_1 = ConfigurationDefinition(
    code=141,
    display_code="14.1",
    topology=ConfigurationTopology(
        hk1=True,
        ww=True,
        circulation=True,
        buffer_storage=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf1",
        "vf4",
        "ruef1",
        "sf1",
        "sf2",
        "sf3",
    ),
)


# ########### Anlage 14.2 #############
ANLAGE_14_2 = ConfigurationDefinition(
    code=142,
    display_code="14.2",
    topology=ConfigurationTopology(
        hk1=True,
        ww=True,
        circulation=True,
        buffer_storage=True,
        heat_exchanger=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf1",
        "vf4",
        "ruef1",
        "sf1",
        "sf2",
        "sf3",
    ),
)


# ########### Anlage 14.3 #############
ANLAGE_14_3 = ConfigurationDefinition(
    code=143,
    display_code="14.3",
    topology=ConfigurationTopology(
        hk1=True,
        ww=True,
        circulation=True,
        solar=True,
        buffer_storage=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf1",
        "vf3",
        "vf4",
        "ruef1",
        "sf1",
        "sf2",
        "sf3",
    ),
)


ANLAGEN_14 = (
    ANLAGE_14_1,
    ANLAGE_14_2,
    ANLAGE_14_3,
)

# ########### Anlage 15.0 #############
ANLAGE_15_0 = ConfigurationDefinition(
    code=150,
    display_code="15.0",
    topology=ConfigurationTopology(
        hk1=True,
        hk3=True,
        ww=True,
        circulation=True,
        buffer_storage=True,
        heat_exchanger=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf3",
        "vf4",
        "ruef1",
        "ruef3",
        "rf3",
        "sf1",
        "sf2",
        "sf3",
    ),
)


# ########### Anlage 15.1 #############
ANLAGE_15_1 = ConfigurationDefinition(
    code=151,
    display_code="15.1",
    topology=ConfigurationTopology(
        hk1=True,
        hk3=True,
        ww=True,
        circulation=True,
        buffer_storage=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf3",
        "vf4",
        "ruef1",
        "ruef3",
        "rf3",
        "sf1",
        "sf2",
        "sf3",
    ),
)


# ########### Anlage 15.2 #############
ANLAGE_15_2 = ConfigurationDefinition(
    code=152,
    display_code="15.2",
    topology=ConfigurationTopology(
        hk1=True,
        hk3=True,
        ww=True,
        circulation=True,
        buffer_storage=True,
        heat_exchanger=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf3",
        "vf4",
        "ruef1",
        "ruef3",
        "rf3",
        "sf1",
        "sf2",
        "sf3",
    ),
)


# ########### Anlage 15.3 #############
ANLAGE_15_3 = ConfigurationDefinition(
    code=153,
    display_code="15.3",
    topology=ConfigurationTopology(
        hk1=True,
        hk3=True,
        ww=True,
        circulation=True,
        solar=True,
        buffer_storage=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf3",
        "vf4",
        "ruef1",
        "ruef3",
        "rf3",
        "sf1",
        "sf2",
        "sf3",
    ),
)


# ########### Anlage 15.4 #############
ANLAGE_15_4 = ConfigurationDefinition(
    code=154,
    display_code="15.4",
    topology=ConfigurationTopology(
        hk1=True,
        hk3=True,
        ww=True,
        circulation=True,
        buffer_storage=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf3",
        "vf4",
        "ruef1",
        "ruef3",
        "rf3",
        "sf1",
        "sf2",
        "sf3",
    ),
)


# ########### Anlage 15.5 #############
ANLAGE_15_5 = ConfigurationDefinition(
    code=155,
    display_code="15.5",
    topology=ConfigurationTopology(
        hk1=True,
        hk3=True,
        ww=True,
        circulation=True,
        buffer_storage=True,
        heat_exchanger=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf3",
        "vf4",
        "ruef1",
        "ruef3",
        "rf3",
        "sf1",
        "sf2",
        "sf3",
    ),
)


ANLAGEN_15 = (
    ANLAGE_15_0,
    ANLAGE_15_1,
    ANLAGE_15_2,
    ANLAGE_15_3,
    ANLAGE_15_4,
    ANLAGE_15_5,
)

# ########### Anlage 16.0 #############
ANLAGE_16_0 = ConfigurationDefinition(
    code=160,
    display_code="16.0",
    topology=ConfigurationTopology(
        hk1=True,
        buffer_storage=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf1",
        "ruef1",
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 16.1 #############
ANLAGE_16_1 = ConfigurationDefinition(
    code=161,
    display_code="16.1",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
        buffer_storage=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "ruef1",
        "ruef2",
        "rf2",
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 16.2 #############
ANLAGE_16_2 = ConfigurationDefinition(
    code=162,
    display_code="16.2",
    topology=ConfigurationTopology(
        hk1=True,
        buffer_storage=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf1",
        "ruef1",
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 16.3 #############
ANLAGE_16_3 = ConfigurationDefinition(
    code=163,
    display_code="16.3",
    topology=ConfigurationTopology(
        hk1=True,
        solar=True,
        buffer_storage=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf1",
        "vf3",
        "ruef1",
        "sf1",
        "sf2",
        "sf3",
    ),
)


# ########### Anlage 16.4 #############
ANLAGE_16_4 = ConfigurationDefinition(
    code=164,
    display_code="16.4",
    topology=ConfigurationTopology(
        hk1=True,
        solar=True,
        buffer_storage=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf1",
        "vf3",
        "ruef1",
        "sf1",
        "sf2",
        "sf3",
    ),
)


# ########### Anlage 16.5 #############
ANLAGE_16_5 = ConfigurationDefinition(
    code=165,
    display_code="16.5",
    topology=ConfigurationTopology(
        hk1=True,
        hk3=True,
        buffer_storage=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf3",
        "ruef1",
        "ruef3",
        "rf3",
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 16.6 #############
ANLAGE_16_6 = ConfigurationDefinition(
    code=166,
    display_code="16.6",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
        solar=True,
        buffer_storage=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf3",
        "ruef1",
        "ruef2",
        "rf2",
        "sf1",
        "sf2",
        "sf3",
    ),
)


# ########### Anlage 16.7 #############
ANLAGE_16_7 = ConfigurationDefinition(
    code=167,
    display_code="16.7",
    topology=ConfigurationTopology(
        hk1=True,
        hk3=True,
        solar=True,
        buffer_storage=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf3",
        "ruef1",
        "ruef3",
        "rf3",
        "sf1",
        "sf2",
        "sf3",
    ),
)


# ########### Anlage 16.8 #############
ANLAGE_16_8 = ConfigurationDefinition(
    code=168,
    display_code="16.8",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
        hk3=True,
        buffer_storage=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf3",
        "ruef1",
        "ruef2",
        "ruef3",
        "rf2",
        "rf3",
        "sf1",
        "sf2",
    ),
)


ANLAGEN_16 = (
    ANLAGE_16_0,
    ANLAGE_16_1,
    ANLAGE_16_2,
    ANLAGE_16_3,
    ANLAGE_16_4,
    ANLAGE_16_5,
    ANLAGE_16_6,
    ANLAGE_16_7,
    ANLAGE_16_8,
)

# ########### Anlage 17.1 #############
ANLAGE_17_1 = ConfigurationDefinition(
    code=171,
    display_code="17.1",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
        ww=True,
        circulation=True,
        buffer_storage=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf4",
        "ruef1",
        "ruef2",
        "rf2",
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 17.8 #############
ANLAGE_17_8 = ConfigurationDefinition(
    code=178,
    display_code="17.8",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
        hk3=True,
        ww=True,
        circulation=True,
        buffer_storage=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf3",
        "vf4",
        "ruef1",
        "ruef2",
        "ruef3",
        "rf2",
        "rf3",
        "sf1",
        "sf2",
    ),
)


ANLAGEN_17 = (
    ANLAGE_17_1,
    ANLAGE_17_8,
)

# ########### Anlage 18.1 #############
ANLAGE_18_1 = ConfigurationDefinition(
    code=181,
    display_code="18.1",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
        ww=True,
        circulation=True,
        buffer_storage=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf4",
        "ruef1",
        "ruef2",
        "rf2",
        "sf1",
        "sf2",
    ),
)


ANLAGEN_18 = (ANLAGE_18_1,)

# Static hydronic configurations for TROVIS Anlage 19.x.
#
# Anlage 19.0 is sourced from ``layout_expert.xml``. The current EB 5578-E
# 3.10.xx appendix sequence jumps from Anlage 18.1 to Anlage 20.0.

# ########### Anlage 19.0 #############
ANLAGE_19_0 = ConfigurationDefinition(
    code=190,
    display_code="19.0",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
        buffer_storage=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "ruef1",
        "ruef2",
        "rf1",
        "rf2",
        "sf3",
    ),
)


ANLAGEN_19 = (ANLAGE_19_0,)

# ########### Anlage 20.0 #############
ANLAGE_20_0 = ConfigurationDefinition(
    code=200,
    display_code="20.0",
    topology=ConfigurationTopology(
        hk1=True,
        hk3=True,
        ww=True,
        circulation=True,
        buffer_storage=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf2",
        "vf3",
        "vf4",
        "ruef1",
        "ruef2",
        "ruef3",
        "rf3",
        "sf1",
        "sf2",
    ),
)


ANLAGEN_20 = (ANLAGE_20_0,)

# ########### Anlage 21.0 #############
ANLAGE_21_0 = ConfigurationDefinition(
    code=210,
    display_code="21.0",
    topology=ConfigurationTopology(
        hk1=True,
        hk3=True,
        ww=True,
        circulation=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf3",
        "vf4",
        "ruef1",
        "ruef2",
        "ruef3",
        "rf1",
        "rf3",
        "sf1",
    ),
)


# ########### Anlage 21.1 #############
ANLAGE_21_1 = ConfigurationDefinition(
    code=211,
    display_code="21.1",
    topology=ConfigurationTopology(
        hk1=True,
        hk3=True,
        ww=True,
        circulation=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf3",
        "vf4",
        "ruef1",
        "ruef2",
        "ruef3",
        "rf1",
        "rf3",
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 21.2 #############
ANLAGE_21_2 = ConfigurationDefinition(
    code=212,
    display_code="21.2",
    topology=ConfigurationTopology(
        hk1=True,
        hk3=True,
        ww=True,
        circulation=True,
        heat_exchanger=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf3",
        "vf4",
        "ruef1",
        "ruef2",
        "ruef3",
        "rf1",
        "rf3",
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 21.9 #############
ANLAGE_21_9 = ConfigurationDefinition(
    code=219,
    display_code="21.9",
    topology=ConfigurationTopology(
        hk1=True,
        hk3=True,
        ww=True,
        circulation=True,
        heat_exchanger=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf3",
        "vf4",
        "ruef1",
        "ruef2",
        "ruef3",
        "rf1",
        "rf3",
        "sf1",
        "sf2",
    ),
)


ANLAGEN_21 = (
    ANLAGE_21_0,
    ANLAGE_21_1,
    ANLAGE_21_2,
    ANLAGE_21_9,
)

# ########### Anlage 25.0 #############
ANLAGE_25_0 = ConfigurationDefinition(
    code=250,
    display_code="25.0",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
        hk3=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf3",
        "ruef1",
        "ruef2",
        "ruef3",
        "rf1",
        "rf2",
        "rf3",
    ),
)


# ########### Anlage 25.5 #############
ANLAGE_25_5 = ConfigurationDefinition(
    code=255,
    display_code="25.5",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
        hk3=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf3",
        "ruef1",
        "ruef2",
        "ruef3",
    ),
)


ANLAGEN_25 = (
    ANLAGE_25_0,
    ANLAGE_25_5,
)

# ########### Anlage 27.1 #############
ANLAGE_27_1 = ConfigurationDefinition(
    code=271,
    display_code="27.1",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
        ww=True,
        circulation=True,
        buffer_storage=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "ruef1",
        "ruef2",
        "rf2",
        "sf1",
        "sf2",
        "sf3",
    ),
)


# ########### Anlage 27.8 #############
ANLAGE_27_8 = ConfigurationDefinition(
    code=278,
    display_code="27.8",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
        hk3=True,
        ww=True,
        circulation=True,
        buffer_storage=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf3",
        "ruef1",
        "ruef2",
        "ruef3",
        "rf2",
        "rf3",
        "sf1",
        "sf2",
        "sf3",
    ),
)


ANLAGEN_27 = (
    ANLAGE_27_1,
    ANLAGE_27_8,
)

# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

_ALL_CONFIGURATIONS = (
    *ANLAGEN_1,
    *ANLAGEN_2,
    *ANLAGEN_3,
    *ANLAGEN_4,
    *ANLAGEN_5,
    *ANLAGEN_6,
    *ANLAGEN_7,
    *ANLAGEN_8,
    *ANLAGEN_9,
    *ANLAGEN_10,
    *ANLAGEN_11,
    *ANLAGEN_12,
    *ANLAGEN_13,
    *ANLAGEN_14,
    *ANLAGEN_15,
    *ANLAGEN_16,
    *ANLAGEN_17,
    *ANLAGEN_18,
    *ANLAGEN_19,
    *ANLAGEN_20,
    *ANLAGEN_21,
    *ANLAGEN_25,
    *ANLAGEN_27,
)

HYDRONIC_CONFIGURATIONS = MappingProxyType(
    {definition.code: definition for definition in _ALL_CONFIGURATIONS}
)

if len(HYDRONIC_CONFIGURATIONS) != len(_ALL_CONFIGURATIONS):
    raise RuntimeError("duplicate TROVIS system code numbers in hydronic registry")


def get_configuration_definition(system_code: int) -> ConfigurationDefinition:
    """Return the static hydronic definition for a raw system code number."""
    try:
        return HYDRONIC_CONFIGURATIONS[system_code]
    except KeyError as err:
        raise KeyError(
            f"unsupported TROVIS system code number: {system_code!r}"
        ) from err


__all__ = [
    "FUNCTIONAL_SENSOR_ROLE_KEYS",
    "HYDRONIC_CONFIGURATIONS",
    "ConfigurationDefinition",
    "ConfigurationTopology",
    "get_configuration_definition",
]
