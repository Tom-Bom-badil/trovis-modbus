"""Static hydronic configurations for TROVIS Anlage 3.x."""

from __future__ import annotations

from .definitions import ConfigurationDefinition, ConfigurationTopology

# ########### Anlage 3.0 #############
ANLAGE_3_0 = ConfigurationDefinition(
    code=30,
    display_code="3.0",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf2",
        "ruef1",
        "ruef2",
        "rf2",
    ),
)


# ########### Anlage 3.1 #############
ANLAGE_3_1 = ConfigurationDefinition(
    code=31,
    display_code="3.1",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
        ww=True,
        circulation=True,
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


# ########### Anlage 3.2 #############
ANLAGE_3_2 = ConfigurationDefinition(
    code=32,
    display_code="3.2",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
        ww=True,
        circulation=True,
        heat_exchanger=True,
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


# ########### Anlage 3.3 #############
ANLAGE_3_3 = ConfigurationDefinition(
    code=33,
    display_code="3.3",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
        ww=True,
        circulation=True,
        solar=True,
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
        "rf2",
        "sf1",
        "sf2",
        "sf3",
    ),
)


# ########### Anlage 3.4 #############
ANLAGE_3_4 = ConfigurationDefinition(
    code=34,
    display_code="3.4",
    topology=ConfigurationTopology(
        hk1=True,
        hk2=True,
        ww=True,
        circulation=True,
        solar=True,
        heat_exchanger=True,
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
        "rf2",
        "sf1",
        "sf2",
        "sf3",
    ),
)


# ########### Anlage 3.5 #############
ANLAGE_3_5 = ConfigurationDefinition(
    code=35,
    display_code="3.5",
    topology=ConfigurationTopology(
        hk1=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf1",
        "ruef1",
    ),
)


# ########### Anlage 3.7 #############
ANLAGE_3_7 = ConfigurationDefinition(
    code=37,
    display_code="3.7",
    topology=ConfigurationTopology(
        ww=True,
        circulation=True,
    ),
    functional_sensor_roles=(
        "af1",
        "vf4",
        "sf1",
        "sf2",
    ),
)


# ########### Anlage 3.8 #############
ANLAGE_3_8 = ConfigurationDefinition(
    code=38,
    display_code="3.8",
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


# ########### Anlage 3.9 #############
ANLAGE_3_9 = ConfigurationDefinition(
    code=39,
    display_code="3.9",
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


ANLAGEN_3 = (
    ANLAGE_3_0,
    ANLAGE_3_1,
    ANLAGE_3_2,
    ANLAGE_3_3,
    ANLAGE_3_4,
    ANLAGE_3_5,
    ANLAGE_3_7,
    ANLAGE_3_8,
    ANLAGE_3_9,
)
