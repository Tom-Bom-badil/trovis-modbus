"""Static hydronic configurations for TROVIS Anlage 1.x."""

from __future__ import annotations

from .definitions import ConfigurationDefinition, ConfigurationTopology

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
