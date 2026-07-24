"""Static logical sensor definition for the TROVIS 5573."""

from ..enums import ControllerModel
from .common import COMMON_SENSOR_KEYS, TROVIS_5573_FAMILY_SENSOR_VARIANTS
from .definitions import ModelDefinition

TROVIS_5573 = ModelDefinition(
    model=ControllerModel.TROVIS_5573,
    heating_circuits=2,
    sensor_keys=COMMON_SENSOR_KEYS,
    sensor_variants=TROVIS_5573_FAMILY_SENSOR_VARIANTS,
)
