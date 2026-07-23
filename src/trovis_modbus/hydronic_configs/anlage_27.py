"""Static hydronic configurations for TROVIS Anlage 27.x."""

from __future__ import annotations

from .definitions import ConfigurationDefinition, ConfigurationTopology

# ########### Anlage 27.1 #############
ANLAGE_27_1 = ConfigurationDefinition(
    code=271,
    display_code="27.1",
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
        "ruef1",
        "ruef2",
        "rf2",
        "sf1",
        "sf2",
        "sf3",
    ),
)


# ########### Anlage 27.8 #############
ANLAGE_27_8 = ConfigurationDefinition(
    code=278,
    display_code="27.8",
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
        "ruef1",
        "ruef2",
        "ruef3",
        "rf2",
        "rf3",
        "sf1",
        "sf2",
        "sf3",
    ),
)


ANLAGEN_27 = (
    ANLAGE_27_1,
    ANLAGE_27_8,
)
