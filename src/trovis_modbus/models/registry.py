"""Registry for static TROVIS controller-model definitions."""

from __future__ import annotations

from types import MappingProxyType

from .definitions import ControllerModel, ModelDefinition
from .trovis_5573 import TROVIS_5573
from .trovis_5573_1 import TROVIS_5573_1
from .trovis_5575 import TROVIS_5575
from .trovis_5576 import TROVIS_5576
from .trovis_5578 import TROVIS_5578
from .trovis_5578_e import TROVIS_5578_E
from .trovis_5579 import TROVIS_5579

MODEL_DEFINITIONS = MappingProxyType(
    {
        definition.model: definition
        for definition in (
            TROVIS_5573,
            TROVIS_5573_1,
            TROVIS_5575,
            TROVIS_5576,
            TROVIS_5578,
            TROVIS_5578_E,
            TROVIS_5579,
        )
    }
)

# Register 40002 is assumed to report the concrete raw model values below.
# In particular, 55731 identifies TROVIS 5573-1 and 55781 identifies TROVIS 5578-E
_REPORTED_MODEL_CANDIDATES = MappingProxyType(
    {
        5573: (TROVIS_5573,),
        55731: (TROVIS_5573_1,),
        5575: (TROVIS_5575,),
        5576: (TROVIS_5576,),
        5578: (TROVIS_5578,),
        55781: (TROVIS_5578_E,),
        5579: (TROVIS_5579,),
    }
)


def get_model_definition(model: ControllerModel | str) -> ModelDefinition:
    """Return the exact static definition for a concrete controller model."""

    try:
        controller_model = ControllerModel(model)
    except ValueError as err:
        raise KeyError(f"unsupported TROVIS model: {model!r}") from err

    try:
        return MODEL_DEFINITIONS[controller_model]
    except KeyError as err:
        raise KeyError(
            f"model definition not implemented yet: {controller_model.value}"
        ) from err


def model_candidates_for_reported_model(
    reported_model: int,
) -> tuple[ModelDefinition, ...]:
    """Return static candidates for the raw model value read from register 40002."""

    return _REPORTED_MODEL_CANDIDATES.get(reported_model, ())
