"""Static logical sensor definition for the TROVIS 5575."""

from ..enums import ControllerModel
from .common import COMMON_SENSOR_KEYS
from .definitions import ModelDefinition, sensor_variant

TROVIS_5575 = ModelDefinition(
    model=ControllerModel.TROVIS_5575,
    heating_circuits=2,
    sensor_keys=COMMON_SENSOR_KEYS,
    sensor_variants=(
        sensor_variant("sf2", "rf2", "analog_input_voltage"),
        sensor_variant("vf2", "vf3", "vf4"),
        sensor_variant("fg1"),
        sensor_variant("fg2"),
    ),
)
