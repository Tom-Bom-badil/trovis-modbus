"""Static hydronic configurations for TROVIS Anlage 16.x."""

from __future__ import annotations

from .definitions import ConfigurationDefinition, ConfigurationTopology

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
