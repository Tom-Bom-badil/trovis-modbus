"""Static hydronic configurations for TROVIS Anlage 10.x."""

from __future__ import annotations

from .definitions import ConfigurationDefinition, ConfigurationTopology

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
