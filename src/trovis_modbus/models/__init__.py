"""Logical sensor capabilities of supported TROVIS controller models."""

from ..enums import ControllerModel
from .common import (
    COMMON_INDIVIDUAL_SENSOR_VARIANTS,
    COMMON_SENSOR_KEYS,
    THREE_CIRCUIT_SENSOR_KEYS,
    TROVIS_5573_FAMILY_SENSOR_VARIANTS,
)
from .definitions import ModelDefinition, SensorVariant, sensor_variant
from .registry import (
    MODEL_DEFINITIONS,
    get_model_definition,
    model_candidates_for_reported_model,
)
from .trovis_5573 import TROVIS_5573
from .trovis_5573_1 import TROVIS_5573_1
from .trovis_5575 import TROVIS_5575
from .trovis_5576 import TROVIS_5576
from .trovis_5578 import TROVIS_5578
from .trovis_5578_e import TROVIS_5578_E
from .trovis_5579 import TROVIS_5579

__all__ = [
    "COMMON_INDIVIDUAL_SENSOR_VARIANTS",
    "COMMON_SENSOR_KEYS",
    "MODEL_DEFINITIONS",
    "THREE_CIRCUIT_SENSOR_KEYS",
    "TROVIS_5573",
    "TROVIS_5573_1",
    "TROVIS_5573_FAMILY_SENSOR_VARIANTS",
    "TROVIS_5575",
    "TROVIS_5576",
    "TROVIS_5578",
    "TROVIS_5578_E",
    "TROVIS_5579",
    "ControllerModel",
    "ModelDefinition",
    "SensorVariant",
    "get_model_definition",
    "model_candidates_for_reported_model",
    "sensor_variant",
]
