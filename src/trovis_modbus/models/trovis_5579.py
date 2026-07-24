"""Static logical sensor definition for the TROVIS 5579."""

from ..enums import ControllerModel
from .common import COMMON_INDIVIDUAL_SENSOR_VARIANTS, THREE_CIRCUIT_SENSOR_KEYS
from .definitions import ModelDefinition, sensor_variant

TROVIS_5579 = ModelDefinition(
    model=ControllerModel.TROVIS_5579,
    heating_circuits=3,
    sensor_keys=THREE_CIRCUIT_SENSOR_KEYS,
    sensor_variants=COMMON_INDIVIDUAL_SENSOR_VARIANTS
    + (sensor_variant("sf3", "fg3", "analog_input_voltage"),),
)
