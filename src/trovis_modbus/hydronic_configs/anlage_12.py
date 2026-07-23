"""Static hydronic configurations for TROVIS Anlage 12.x."""

from __future__ import annotations

from .definitions import ConfigurationDefinition, ConfigurationTopology

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
