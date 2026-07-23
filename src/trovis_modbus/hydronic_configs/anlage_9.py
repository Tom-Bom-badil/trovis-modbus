"""Static hydronic configurations for TROVIS Anlage 9.x."""

from __future__ import annotations

from .definitions import ConfigurationDefinition, ConfigurationTopology

# ########### Anlage 9.1 #############
ANLAGE_9_1 = ConfigurationDefinition(
    code=91,
    display_code="9.1",
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


# ########### Anlage 9.2 #############
ANLAGE_9_2 = ConfigurationDefinition(
    code=92,
    display_code="9.2",
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


# ########### Anlage 9.5 #############
ANLAGE_9_5 = ConfigurationDefinition(
    code=95,
    display_code="9.5",
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


# ########### Anlage 9.6 #############
ANLAGE_9_6 = ConfigurationDefinition(
    code=96,
    display_code="9.6",
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


ANLAGEN_9 = (
    ANLAGE_9_1,
    ANLAGE_9_2,
    ANLAGE_9_5,
    ANLAGE_9_6,
)
