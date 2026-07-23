"""Static hydronic configurations for TROVIS Anlage 5.x."""

from __future__ import annotations

from .definitions import ConfigurationDefinition, ConfigurationTopology

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
