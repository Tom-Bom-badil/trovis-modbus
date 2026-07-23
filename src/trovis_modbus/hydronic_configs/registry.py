"""Registry for static TROVIS hydronic configurations."""

from __future__ import annotations

from types import MappingProxyType

from .anlage_1 import ANLAGEN_1
from .anlage_2 import ANLAGEN_2
from .anlage_3 import ANLAGEN_3
from .anlage_4 import ANLAGEN_4
from .anlage_5 import ANLAGEN_5
from .anlage_6 import ANLAGEN_6
from .anlage_7 import ANLAGEN_7
from .anlage_8 import ANLAGEN_8
from .anlage_9 import ANLAGEN_9
from .anlage_10 import ANLAGEN_10
from .anlage_11 import ANLAGEN_11
from .anlage_12 import ANLAGEN_12
from .anlage_13 import ANLAGEN_13
from .anlage_14 import ANLAGEN_14
from .anlage_15 import ANLAGEN_15
from .anlage_16 import ANLAGEN_16
from .anlage_17 import ANLAGEN_17
from .anlage_18 import ANLAGEN_18
from .anlage_19 import ANLAGEN_19
from .anlage_20 import ANLAGEN_20
from .anlage_21 import ANLAGEN_21
from .anlage_25 import ANLAGEN_25
from .anlage_27 import ANLAGEN_27
from .definitions import ConfigurationDefinition

_ALL_CONFIGURATIONS = (
    *ANLAGEN_1,
    *ANLAGEN_2,
    *ANLAGEN_3,
    *ANLAGEN_4,
    *ANLAGEN_5,
    *ANLAGEN_6,
    *ANLAGEN_7,
    *ANLAGEN_8,
    *ANLAGEN_9,
    *ANLAGEN_10,
    *ANLAGEN_11,
    *ANLAGEN_12,
    *ANLAGEN_13,
    *ANLAGEN_14,
    *ANLAGEN_15,
    *ANLAGEN_16,
    *ANLAGEN_17,
    *ANLAGEN_18,
    *ANLAGEN_19,
    *ANLAGEN_20,
    *ANLAGEN_21,
    *ANLAGEN_25,
    *ANLAGEN_27,
)


HYDRONIC_CONFIGURATIONS = MappingProxyType(
    {definition.code: definition for definition in _ALL_CONFIGURATIONS}
)


if len(HYDRONIC_CONFIGURATIONS) != len(_ALL_CONFIGURATIONS):
    raise RuntimeError("duplicate TROVIS system code numbers in hydronic registry")


def get_configuration_definition(system_code: int) -> ConfigurationDefinition:
    """Return the static hydronic definition for a raw system code number."""
    try:
        return HYDRONIC_CONFIGURATIONS[system_code]
    except KeyError as err:
        raise KeyError(
            f"unsupported TROVIS system code number: {system_code!r}"
        ) from err
