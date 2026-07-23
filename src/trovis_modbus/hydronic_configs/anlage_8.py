"""Static hydronic configurations for TROVIS Anlage 8.x."""

from __future__ import annotations

from .definitions import ConfigurationDefinition, ConfigurationTopology

# ########### Anlage 8.1 #############
ANLAGE_8_1 = ConfigurationDefinition(
    code=81,
    display_code="8.1",
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


# ########### Anlage 8.2 #############
ANLAGE_8_2 = ConfigurationDefinition(
    code=82,
    display_code="8.2",
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


ANLAGEN_8 = (
    ANLAGE_8_1,
    ANLAGE_8_2,
)
