"""Shared logical sensor capabilities of the TROVIS 557x family."""

from __future__ import annotations

from .definitions import SensorVariant, sensor_variant

# Logical sensor registers available throughout the supported 557x family.
# Their electrical terminals are deliberately not part of the library model.
COMMON_SENSOR_KEYS = (
    "af1",
    "vf1",
    "vf2",
    "vf3",
    "vf4",
    "ruef1",
    "ruef2",
    "rf1",
    "rf2",
    "sf1",
    "sf2",
    "fg1",
    "fg2",
    "analog_input_voltage",
)

# Additional logical sensors used by the three-heating-circuit models.
THREE_CIRCUIT_SENSOR_KEYS = COMMON_SENSOR_KEYS + (
    "af2",
    "ruef3",
    "rf3",
    "sf3",
    "fg3",
)

# These sensors are individually configurable on the larger controller family.
# A one-key variant means that another configuration of the same input is not a
# sensor exposed by the first library/integration version, for example a binary
# input. The specific selection will later be resolved from functions and coils.
COMMON_INDIVIDUAL_SENSOR_VARIANTS: tuple[SensorVariant, ...] = tuple(
    sensor_variant(sensor_key)
    for sensor_key in (
        "rf2",
        "vf2",
        "vf3",
        "vf4",
        "sf2",
        "fg1",
        "fg2",
    )
)

# TROVIS 5573 and 5573-1 share the same reduced logical sensor matrix.
TROVIS_5573_FAMILY_SENSOR_VARIANTS = (
    sensor_variant("sf2", "rf2"),
    sensor_variant("vf2", "vf3", "vf4"),
    sensor_variant("fg1"),
    sensor_variant("fg2"),
)
