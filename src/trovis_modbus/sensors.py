"""Global physical and analog sensor inputs."""

from __future__ import annotations

from .model import NAN_INT16, TrovisComponent, gauge, integer, temperature


class Sensors(TrovisComponent):
    """Physical sensor inputs, e.g. Pt1000 and optional analog inputs.

    Naming follows the manufacturer abbreviations.
    """

    af1 = temperature(40010)  # Außenfühler 1
    af2 = temperature(40011)  # Außenfühler 2

    vf1 = temperature(40013)  # Vorlauffühler 1
    vf2 = temperature(40014)  # Vorlauffühler 2
    vf3 = temperature(40015)  # Vorlauffühler 3
    vf4 = temperature(40016)  # Vorlauffühler 4

    ruef1 = temperature(40017)  # Rücklauffühler 1
    ruef2 = temperature(40018)  # Rücklauffühler 2
    ruef3 = temperature(40019)  # Rücklauffühler 3

    rf1 = temperature(40020)  # Raumfühler 1
    rf2 = temperature(40021)  # Raumfühler 2
    rf3 = temperature(40022)  # Raumfühler 3

    sf1 = temperature(40023)  # Speicherfühler 1
    sf2 = temperature(40024)  # Speicherfühler 2
    sf3_fg3 = temperature(40025)  # Speicherfühler/Ferngeber 3

    fg1 = temperature(40026, unit="K")  # Ferngeber 1 / AE1 on 5578-E
    fg2 = temperature(40027, unit="K")  # Ferngeber 2 / AE2 on 5578-E
    ae3_fg3 = gauge(
        40028,
        0.1,
        signed=True,
        nan=NAN_INT16,
        digits=1,
        maker_key="AE3_FG3",
        maker_category="FÜH-FG",
        description="Analogeingang AE3 (5578-E) / Ferngeber FG3",
    )
    pulse_rate = integer(
        40029,
        signed=False,
        min_value=0,
        max_value=1000,
        digits=0,
        unit="Imp/h",
        maker_key="Meßwert_Imp-h",
        maker_category="ALG-VOL",
        description="Impulsrate am Eingang Klemme 17/18",
    )
    analog_input_voltage = gauge(
        40042,
        0.01,
        signed=False,
        min_value=0,
        max_value=10,
        digits=2,
        unit="V",
        maker_key="AE_0-10V",
        maker_category="FÜH-EA",
        description="Analogeingang 0 bis 10 V",
    )
    summer_outside_average = temperature(
        40043,
        maker_key="Sommer_AT-Mittel",
        maker_category="ALG-SON",
        description="Tagesdurchschnittstemperatur während Sommerbetrieb",
    )

    @property
    def detected_sensor_names(self) -> tuple[str, ...]:
        """Return sensor fields that currently have a valid value."""
        return tuple(
            name for name in self._register_fields if getattr(self, name) is not None
        )
