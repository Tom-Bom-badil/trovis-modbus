"""Static hydronic configurations for TROVIS Anlage 4.x."""

from __future__ import annotations

from .definitions import ConfigurationDefinition, ConfigurationTopology

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
