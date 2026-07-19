"""Overall controller state: faults, rotary switches, summer mode, locks."""


from __future__ import annotations

from .enums import OperatingMode
from .model import (
    TrovisComponent,
    coil,
    enum,
    gauge,
    integer,
    month_day_value,
    temperature,
)
from .utils import MonthDay


class Controller(TrovisComponent):
    """Controller-wide status and settings."""

    ##### registers

    special_functions = integer(
        40005,
        signed=False,
        min_value=0,
        max_value=6000,
        raw_min=0,
        raw_max=6000,
        digits=0,
        maker_key="Sonderfunktionen",
        maker_category="ALG-ID",
        description="Reglerupdate via Modbus / Reglerneustart",
    )

    max_flow_setpoint = temperature(
        40099,
        min_value=5,
        max_value=130,
        raw_min=50,
        raw_max=1300,
        digits=1,
        maker_key="MaxVorlSollw",
        maker_category="SOL-VL",
        description="Maximaler Vorlaufsollwert des Reglers",
    )

    # The three front-panel rotary switches, top to bottom (RK1 / RK2 / hot water).
    switch_top = enum(40103, OperatingMode)

    switch_middle = enum(40104, OperatingMode)

    switch_bottom = enum(40105, OperatingMode)

    summer_start = month_day_value(
        40113,
        writable=True,
        min_value=MonthDay(1, 1),
        max_value=MonthDay(31, 12),
        raw_min=101,
        raw_max=3112,
        maker_key="Sommer_Dat_Anf",
        maker_category="ALG-SON",
        description="Datum Beginn Sommerzeitraum",
    )

    summer_end = month_day_value(
        40114,
        writable=True,
        min_value=MonthDay(1, 1),
        max_value=MonthDay(31, 12),
        raw_min=101,
        raw_max=3112,
        maker_key="Sommer_Dat_End",
        maker_category="ALG-SON",
        description="Datum Ende Sommerzeitraum",
    )

    summer_days_on = integer(
        40115,
        signed=False,
        writable=True,
        min_value=1,
        max_value=3,
        raw_min=1,
        raw_max=3,
        digits=0,
        maker_key="Sommer_Tagz_ein",
        maker_category="ALG-SON",
        description="Anzahl Tage für Sommerbetrieb ein",
    )

    summer_days_off = integer(
        40116,
        signed=False,
        writable=True,
        min_value=1,
        max_value=3,
        raw_min=1,
        raw_max=3,
        digits=0,
        maker_key="Sommer_Tagz_aus",
        maker_category="ALG-SON",
        description="Anzahl Tage für Sommerbetrieb aus",
    )

    summer_outside_limit = temperature(
        40117,
        writable=True,
        min_value=0,
        max_value=30,
        raw_min=0,
        raw_max=300,
        digits=1,
        maker_key="Sommer_AT-Wert",
        maker_category="ALG-SON",
        description="Außentemperatur-Grenzwert für den Sommerbetrieb",
    )

    outside_delay = gauge(
        40118,
        0.1,
        writable=True,
        min_value=1,
        max_value=6,
        step=1,
        digits=0,
        unit="K/h",
        raw_min=10,
        raw_max=60,
        maker_key="AT_Verzögerung",
        maker_category="ALG-SON",
        description="Verzögerung der Außentemperatur-Anpassung",
    )

    temperature_monitoring_deviation = gauge(
        40121,
        0.1,
        signed=False,
        writable=True,
        min_value=1,
        max_value=30,
        raw_min=10,
        raw_max=300,
        digits=1,
        unit="K",
        maker_key="TempüwAbweichung",
        maker_category="ALG-SON",
        description="Temperaturüberwachung: Regelabweichung",
    )

    temperature_monitoring_window = integer(
        40122,
        signed=False,
        writable=True,
        min_value=1,
        max_value=120,
        raw_min=1,
        raw_max=120,
        digits=0,
        unit="min",
        maker_key="TempüwZeitfenstr",
        maker_category="ALG-SON",
        description="Temperaturüberwachung: Zeitfenster",
    )

    frost_limit = temperature(
        40123,
        writable=True,
        min_value=-15,
        max_value=3,
        raw_min=-150,
        raw_max=30,
        digits=1,
        maker_key="Frostschutz_GW",
        maker_category="ALG-SON",
        description="Frostschutzgrenzwert",
    )

    outside_input_range_start = temperature(
        40124,
        writable=True,
        min_value=-50,
        max_value=100,
        raw_min=-500,
        raw_max=1000,
        digits=1,
        maker_key="Anfang_AT_0V",
        maker_category="FÜH-EA",
        description="Übertragungsbereichsanfang Außentemperatur bei 0 V",
    )

    outside_input_range_end = temperature(
        40125,
        writable=True,
        min_value=-50,
        max_value=100,
        raw_min=-500,
        raw_max=1000,
        digits=1,
        maker_key="Ende_AT_10V",
        maker_category="FÜH-EA",
        description="Übertragungsbereichsende Außentemperatur bei 10 V",
    )

    station_address = integer(
        40143,
        signed=False,
        min_value=1,
        max_value=32000,
        raw_min=1,
        raw_max=32000,
        digits=0,
        maker_key="Stationsadresse",
        maker_category="ALG-MOD",
        description="Stationsadresse",
    )

    error_status = integer(
        40150,
        signed=False,
        min_value=0,
        max_value=65535,
        raw_min=0,
        raw_max=65535,
        digits=0,
        maker_key="FehlerstatusReg",
        maker_category="ALG-ERO",
        description="Fehlerstatusregister",
    )

    error_count = integer(
        40154,
        signed=False,
        min_value=0,
        max_value=65535,
        raw_min=0,
        raw_max=65535,
        digits=0,
        maker_key="FehlerzählerReg",
        maker_category="ALG-ERO",
        description="Fehlerzählerregister",
    )

    ##### coils

    general_fault = coil(1)

    data_entry_active = coil(2)

    data_entry_performed = coil(3)

    global_level_autark = coil(
        4,
        false_key="glt",
        true_key="autonomous",
        false_label="GLT",
        true_label="Autark",
        maker_key="Sammel_Ebenenbit",
        maker_category="ALG-BTR",
        description="Sammel-Ebenenbit CL88 bis CL121",
    )

    summer_active = coil(9)

    outside_temperature_control_autonomous = coil(
        88,
        false_key="glt",
        true_key="autonomous",
        false_label="GLT",
        true_label="Autark",
        maker_key="EBN_Außentem_AF1",
        maker_category="EBN-AT",
        description="Steuerungsebene Außentemperatur AF1",
    )

    glt_timeout_active = coil(
        159,
        writable=True,
        false_key="inactive",
        true_key="active",
        false_label="Inaktiv",
        true_label="Aktiv",
        maker_key="FB07_Timeout_GLT",
        maker_category="CON-MOD",
        description="Leitsystemüberwachung / GLT-Timeout",
    )

    any_circuit_not_automatic = coil(
        998,
        maker_key="Btr_nicht_Auto",
        maker_category="ALG-BTR",
        description="Mindestens ein Regelkreis ist nicht in Automatik",
    )

    rotary_switch_not_automatic = coil(
        999,
        maker_key="BtrS_nicht_Auto",
        maker_category="ALG-BTR",
        description=(
            "Mindestens ein Regelkreis ist über den Betriebsschalter nicht in Automatik"
        ),
    )

    delayed_outside_temp_adjustment_falling = coil(134, writable=True)

    delayed_outside_temp_adjustment_rising = coil(135, writable=True)

    auto_daylight_saving = coil(
        137,
        writable=True,
        false_key="inactive",
        true_key="active",
        false_label="Inaktiv",
        true_label="Aktiv",
        maker_key="FB08_AutSommZeit",
        description="Automatische Sommer-/Winterzeitumschaltung",
    )

    manual_levels_locked = coil(150, writable=True)

    rotary_switch_locked = coil(151, writable=True)


    async def set_summer_start(self, value: MonthDay) -> None:
        """Set the recurring summer-mode start date."""
        await self.async_write_datapoint("summer_start", value)

    async def set_summer_end(self, value: MonthDay) -> None:
        """Set the recurring summer-mode end date."""
        await self.async_write_datapoint("summer_end", value)
