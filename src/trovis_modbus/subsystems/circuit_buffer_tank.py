"""Buffer-tank-specific extensions of the technical Rk1 circuit."""

from __future__ import annotations

from ..data_model import TrovisComponent, enum, gauge, temperature
from ..enums import BufferTankStatus


class BufferTankCircuit(TrovisComponent):
    """Buffer-tank-specific PA1 values and operating state for Rk1.

    The common control-circuit datapoints remain on :class:`HeatingCircuit`
    through ``device.rk1``. This component only adds the buffer-tank-specific
    register extension and therefore does not duplicate the Rk1 block.

    A raw value of ``0`` in ``minimum_charging_setpoint`` and
    ``charging_end_temperature`` represents the controller setting ``AUTO``/``AT``.
    """

    minimum_charging_setpoint = temperature(
        41100,
        writable=True,
        min_value=0,
        max_value=90,
        raw_min=0,
        raw_max=900,
        digits=1,
        maker_key="PufferladMinSoll",
        maker_category="SOL-VL",
        description="Minimaler Sollwert Pufferladung; 0 = AUTO/AT",
    )

    charging_end_temperature = temperature(
        41101,
        writable=True,
        min_value=0,
        max_value=90,
        raw_min=0,
        raw_max=900,
        digits=1,
        maker_key="Pufferlad_Ende",
        maker_category="SOL-VL",
        description="Pufferladung beenden; 0 = AUTO/AT",
    )

    charging_temperature_boost = gauge(
        41102,
        0.1,
        signed=False,
        writable=True,
        min_value=0,
        max_value=50,
        raw_min=0,
        raw_max=500,
        digits=1,
        unit="K",
        maker_key="PufferladÜberhöh",
        maker_category="SOL-VL",
        description="Überhöhung Ladetemperatur Pufferladung",
    )

    charging_pump_lag_factor = gauge(
        41103,
        0.1,
        signed=False,
        writable=True,
        min_value=0,
        max_value=10,
        raw_min=0,
        raw_max=100,
        digits=1,
        maker_key="Pufferlad_Nachl",
        maker_category="SOL-VL",
        description="Faktor Nachlaufzeit Pufferladung",
    )

    status = enum(
        41104,
        BufferTankStatus,
        maker_key="Pufferstatus",
        maker_category="ALG-BTR",
        description="Betriebszustand der Pufferspeicherladung",
    )
