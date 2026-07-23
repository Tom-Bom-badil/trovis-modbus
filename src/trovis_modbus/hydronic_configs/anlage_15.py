"""Static hydronic configurations for TROVIS Anlage 15.x."""

from __future__ import annotations

from .definitions import ConfigurationDefinition, ConfigurationTopology

# ########### Anlage 15.0 #############
ANLAGE_15_0 = ConfigurationDefinition(
    code=150,
    display_code="15.0",
    topology=ConfigurationTopology(
        hk1=True,
        hk3=True,
        ww=True,
        circulation=True,
        buffer_storage=True,
        heat_exchanger=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf3",
        "vf4",
        "ruef1",
        "ruef3",
        "rf3",
        "sf1",
        "sf2",
        "sf3",
    ),
)


# ########### Anlage 15.1 #############
ANLAGE_15_1 = ConfigurationDefinition(
    code=151,
    display_code="15.1",
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
        "vf1",
        "vf3",
        "vf4",
        "ruef1",
        "ruef3",
        "rf3",
        "sf1",
        "sf2",
        "sf3",
    ),
)


# ########### Anlage 15.2 #############
ANLAGE_15_2 = ConfigurationDefinition(
    code=152,
    display_code="15.2",
    topology=ConfigurationTopology(
        hk1=True,
        hk3=True,
        ww=True,
        circulation=True,
        buffer_storage=True,
        heat_exchanger=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf3",
        "vf4",
        "ruef1",
        "ruef3",
        "rf3",
        "sf1",
        "sf2",
        "sf3",
    ),
)


# ########### Anlage 15.3 #############
ANLAGE_15_3 = ConfigurationDefinition(
    code=153,
    display_code="15.3",
    topology=ConfigurationTopology(
        hk1=True,
        hk3=True,
        ww=True,
        circulation=True,
        solar=True,
        buffer_storage=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf3",
        "vf4",
        "ruef1",
        "ruef3",
        "rf3",
        "sf1",
        "sf2",
        "sf3",
    ),
)


# ########### Anlage 15.4 #############
ANLAGE_15_4 = ConfigurationDefinition(
    code=154,
    display_code="15.4",
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
        "vf1",
        "vf3",
        "vf4",
        "ruef1",
        "ruef3",
        "rf3",
        "sf1",
        "sf2",
        "sf3",
    ),
)


# ########### Anlage 15.5 #############
ANLAGE_15_5 = ConfigurationDefinition(
    code=155,
    display_code="15.5",
    topology=ConfigurationTopology(
        hk1=True,
        hk3=True,
        ww=True,
        circulation=True,
        buffer_storage=True,
        heat_exchanger=True,
    ),
    functional_sensor_roles=(
        "af1",
        "af2",
        "vf1",
        "vf3",
        "vf4",
        "ruef1",
        "ruef3",
        "rf3",
        "sf1",
        "sf2",
        "sf3",
    ),
)


ANLAGEN_15 = (
    ANLAGE_15_0,
    ANLAGE_15_1,
    ANLAGE_15_2,
    ANLAGE_15_3,
    ANLAGE_15_4,
    ANLAGE_15_5,
)
