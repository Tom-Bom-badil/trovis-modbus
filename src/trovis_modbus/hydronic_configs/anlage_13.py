"""Static hydronic configurations for TROVIS Anlage 13.x."""

from __future__ import annotations

from .definitions import ConfigurationDefinition, ConfigurationTopology

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
