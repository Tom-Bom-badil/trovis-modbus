"""Static hydronic configurations for TROVIS Anlage 11.x."""

from __future__ import annotations

from .definitions import ConfigurationDefinition, ConfigurationTopology

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
