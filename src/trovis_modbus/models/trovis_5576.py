"""Static logical sensor definition for the TROVIS 5576."""

from ..enums import ControllerModel
from .common import COMMON_INDIVIDUAL_SENSOR_VARIANTS, COMMON_SENSOR_KEYS
from .definitions import ModelDefinition, sensor_variant

TROVIS_5576 = ModelDefinition(
    model=ControllerModel.TROVIS_5576,
    heating_circuits=2,
    sensor_keys=COMMON_SENSOR_KEYS + ("af2", "sf3"),
    sensor_variants=COMMON_INDIVIDUAL_SENSOR_VARIANTS
    + (sensor_variant("sf3", "analog_input_voltage"),),
)
