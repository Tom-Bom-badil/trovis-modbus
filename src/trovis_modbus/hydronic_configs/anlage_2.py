"""Static hydronic configurations for TROVIS Anlage 2.x."""

from __future__ import annotations

from .definitions import ConfigurationDefinition, ConfigurationTopology

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
