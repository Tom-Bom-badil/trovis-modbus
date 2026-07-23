"""Static hydronic configurations for TROVIS Anlage 6.x."""

from __future__ import annotations

from .definitions import ConfigurationDefinition, ConfigurationTopology

# ########### Anlage 6.0 #############
ANLAGE_6_0 = ConfigurationDefinition(
    code=60,
    display_code="6.0",
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
        "rf1",
        "rf2",
        "rf3",
    ),
)


# ########### Anlage 6.1 #############
ANLAGE_6_1 = ConfigurationDefinition(
    code=61,
    display_code="6.1",
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
        "rf1",
        "rf2",
        "rf3",
        "sf1",
        "sf2",
    ),
)


ANLAGEN_6 = (
    ANLAGE_6_0,
    ANLAGE_6_1,
)
