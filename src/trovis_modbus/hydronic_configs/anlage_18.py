"""Static hydronic configurations for TROVIS Anlage 18.x."""

from __future__ import annotations

from .definitions import ConfigurationDefinition, ConfigurationTopology

# ########### Anlage 18.1 #############
ANLAGE_18_1 = ConfigurationDefinition(
    code=181,
    display_code="18.1",
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


ANLAGEN_18 = (ANLAGE_18_1,)
