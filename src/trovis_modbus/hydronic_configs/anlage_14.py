"""Static hydronic configurations for TROVIS Anlage 14.x."""

from __future__ import annotations

from .definitions import ConfigurationDefinition, ConfigurationTopology

# ########### Anlage 14.1 #############
ANLAGE_14_1 = ConfigurationDefinition(
    code=141,
    display_code="14.1",
    topology=ConfigurationTopology(
        hk1=True,
        ww=True,
        circulation=True,
        buffer_storage=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf1",
        "vf4",
        "ruef1",
        "sf1",
        "sf2",
        "sf3",
    ),
)


# ########### Anlage 14.2 #############
ANLAGE_14_2 = ConfigurationDefinition(
    code=142,
    display_code="14.2",
    topology=ConfigurationTopology(
        hk1=True,
        ww=True,
        circulation=True,
        buffer_storage=True,
        heat_exchanger=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf1",
        "vf4",
        "ruef1",
        "sf1",
        "sf2",
        "sf3",
    ),
)


# ########### Anlage 14.3 #############
ANLAGE_14_3 = ConfigurationDefinition(
    code=143,
    display_code="14.3",
    topology=ConfigurationTopology(
        hk1=True,
        ww=True,
        circulation=True,
        solar=True,
        buffer_storage=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf1",
        "vf3",
        "vf4",
        "ruef1",
        "sf1",
        "sf2",
        "sf3",
    ),
)


ANLAGEN_14 = (
    ANLAGE_14_1,
    ANLAGE_14_2,
    ANLAGE_14_3,
)
