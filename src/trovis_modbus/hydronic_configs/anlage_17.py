"""Static hydronic configurations for TROVIS Anlage 17.x."""

from __future__ import annotations

from .definitions import ConfigurationDefinition, ConfigurationTopology

# ########### Anlage 17.1 #############
ANLAGE_17_1 = ConfigurationDefinition(
    code=171,
    display_code="17.1",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
        ww=True,
        circulation=True,
        buffer_storage=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf4",
        "ruef1",
        "ruef2",
        "rf2",
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 17.8 #############
ANLAGE_17_8 = ConfigurationDefinition(
    code=178,
    display_code="17.8",
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


ANLAGEN_17 = (
    ANLAGE_17_1,
    ANLAGE_17_8,
)
