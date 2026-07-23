"""Static hydronic configurations for TROVIS Anlage 25.x."""

from __future__ import annotations

from .definitions import ConfigurationDefinition, ConfigurationTopology

# ########### Anlage 25.0 #############
ANLAGE_25_0 = ConfigurationDefinition(
    code=250,
    display_code="25.0",
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


# ########### Anlage 25.5 #############
ANLAGE_25_5 = ConfigurationDefinition(
    code=255,
    display_code="25.5",
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
    ),
)


ANLAGEN_25 = (
    ANLAGE_25_0,
    ANLAGE_25_5,
)
