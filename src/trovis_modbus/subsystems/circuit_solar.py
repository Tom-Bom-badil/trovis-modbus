"""The optional solar thermal circuit."""

from __future__ import annotations

from ..data_model import TrovisComponent, coil, gauge, integer, temperature


class SolarCircuit(TrovisComponent):
    """Solar-pump control and its essential operating parameters."""

    pump_on_temperature_difference = gauge(
        41810,
        0.1,
        signed=False,
        writable=True,
        min_value=1,
        max_value=30,
        raw_min=10,
        raw_max=300,
        digits=1,
        unit="K",
        maker_key="Solar_UP_EIN",
        maker_category="SOL-SON",
        description="Temperature difference for switching on the solar circuit pump",
    )

    pump_off_temperature_difference = gauge(
        41811,
        0.1,
        signed=False,
        writable=True,
        min_value=0,
        max_value=30,
        raw_min=0,
        raw_max=300,
        digits=1,
        unit="K",
        maker_key="Solar_UP_AUS",
        maker_category="SOL-SON",
        description="Temperature difference for switching off the solar circuit pump",
    )

    maximum_storage_temperature = temperature(
        41812,
        writable=True,
        min_value=20,
        max_value=90,
        raw_min=200,
        raw_max=900,
        digits=1,
        maker_key="Solar_max_Speich",
        maker_category="SOL-SON",
        description="Maximum storage tank temperature for solar charging",
    )

    operating_hours = integer(
        41813,
        signed=False,
        min_value=0,
        max_value=65535,
        raw_min=0,
        raw_max=65535,
        digits=0,
        unit="h",
        maker_key="Solarbetr_h",
        maker_category="SOL-SON",
        description="Solar circuit operating hours",
    )

    pump_running = coil(
        1808,
        maker_key="Solar_UP_TW",
        maker_category="ALG-BTR",
        description="Solar circuit pump active",
    )
