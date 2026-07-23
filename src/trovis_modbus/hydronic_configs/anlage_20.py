"""Static hydronic configurations for TROVIS Anlage 20.x."""

from __future__ import annotations

from .definitions import ConfigurationDefinition, ConfigurationTopology

# ########### Anlage 20.0 #############
ANLAGE_20_0 = ConfigurationDefinition(
    code=200,
    display_code="20.0",
    topology=ConfigurationTopology(
        hk1=True,
        hk3=True,
        ww=True,
        circulation=True,
        buffer_storage=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
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


ANLAGEN_20 = (ANLAGE_20_0,)
