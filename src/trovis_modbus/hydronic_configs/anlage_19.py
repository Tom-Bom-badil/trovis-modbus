"""Static hydronic configurations for TROVIS Anlage 19.x.
Note: The current manuals skip 19.x and jump from Anlage 18.1 to Anlage 20.0.
"""

from __future__ import annotations

from .definitions import ConfigurationDefinition, ConfigurationTopology

# ########### Anlage 19.0 #############
ANLAGE_19_0 = ConfigurationDefinition(
    code=190,
    display_code="19.0",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
        buffer_storage=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "ruef1",
        "ruef2",
        "rf1",
        "rf2",
        "sf3",
    ),
)


ANLAGEN_19 = (ANLAGE_19_0,)
