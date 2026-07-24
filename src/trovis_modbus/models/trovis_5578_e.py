"""Static logical sensor definition for the TROVIS 5578-E."""

from ..enums import ControllerModel
from .common import THREE_CIRCUIT_SENSOR_KEYS
from .definitions import ModelDefinition, sensor_variant

TROVIS_5578_E = ModelDefinition(
    model=ControllerModel.TROVIS_5578_E,
    heating_circuits=3,
    sensor_keys=THREE_CIRCUIT_SENSOR_KEYS + ("ae1", "ae2", "ae3"),
    sensor_variants=(
        sensor_variant("rf2"),
        sensor_variant("vf2"),
        sensor_variant("vf3"),
        sensor_variant("vf4"),
        sensor_variant("sf2"),
        sensor_variant("ae1", "fg1"),
        sensor_variant("ae2", "fg2"),
        sensor_variant("ae3", "fg3", "sf3"),
    ),
)
