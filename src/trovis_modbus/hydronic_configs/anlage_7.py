"""Static hydronic configurations for TROVIS Anlage 7.x."""

from __future__ import annotations

from .definitions import ConfigurationDefinition, ConfigurationTopology

# ########### Anlage 7.1 #############
ANLAGE_7_1 = ConfigurationDefinition(
    code=71,
    display_code="7.1",
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
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 7.2 #############
ANLAGE_7_2 = ConfigurationDefinition(
    code=72,
    display_code="7.2",
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
        "sf1",
        "sf2",
    ),
)


ANLAGEN_7 = (
    ANLAGE_7_1,
    ANLAGE_7_2,
)
