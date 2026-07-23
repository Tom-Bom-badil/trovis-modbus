"""Static hydronic configurations for TROVIS Anlage 21.x."""

from __future__ import annotations

from .definitions import ConfigurationDefinition, ConfigurationTopology

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
