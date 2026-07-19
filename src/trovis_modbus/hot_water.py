"""The DHW domestic hot water circuit (HK4 / RK4 / WW)."""

from __future__ import annotations

from datetime import time

from .enums import OperatingMode, StorageStatus, Weekday
from .model import (
    TrovisComponent,
    coil,
    enum,
    gauge,
    integer,
    temperature,
    time_value,
)
from .options import OPERATING_MODE_OPTIONS, WEEKDAY_OPTIONS
from .utils import TemperatureRange


class HotWater(TrovisComponent):
    """Domestic hot water: setpoints, charging and thermal disinfection."""

    ### registers

    setpoint_day = temperature(
        41800,
        writable=True,
        min_value=20,
        max_value=90,
        raw_min=200,
        raw_max=900,
        digits=1,
        maker_key="TW_Sollw",
        maker_category="SOL-WW",
        description="Trinkwasser Sollwert",
    )

    setpoint_max = temperature(
        41801,
        writable=True,
        min_value=5,
        max_value=90,
        raw_min=50,
        raw_max=900,
        digits=1,
        maker_key="MaxTW_Sollw",
        maker_category="SOL-WW",
        description="Maximale Einstellgrenztemperatur Trinkwassersollwert",
    )

    setpoint_min = temperature(
        41802,
        writable=True,
        min_value=5,
        max_value=90,
        raw_min=50,
        raw_max=900,
        digits=1,
        maker_key="MinTW_Sollw",
        maker_category="SOL-WW",
        description="Minimale Einstellgrenztemperatur Trinkwassersollwert",
    )

    hysteresis = gauge(
        41803,
        0.1,
        signed=False,
        writable=True,
        min_value=0,
        max_value=30,
        raw_min=0,
        raw_max=300,
        digits=1,
        unit="K",
        maker_key="Schaltdiff_TW",
        maker_category="SOL-WW",
        description="Schaltdifferenz Trinkwasser",
    )

    charge_overshoot = gauge(
        41804,
        0.1,
        signed=False,
        writable=True,
        min_value=0,
        max_value=50,
        raw_min=0,
        raw_max=500,
        digits=1,
        unit="K",
        maker_key="LadTempdiff_TW",
        maker_category="SOL-WW",
        description="Ladetemperaturüberhöhung",
    )

    charge_pump_overrun_factor = gauge(
        41805,
        0.1,
        signed=False,
        writable=True,
        min_value=0.1,
        max_value=10,
        raw_min=1,
        raw_max=100,
        digits=1,
        maker_key="Nachlauf_SLP",
        maker_category="SOL-WW",
        description="Nachlauffaktor der Speicherladepumpe",
    )

    max_charge_temp = temperature(
        41806,
        writable=True,
        min_value=0,
        max_value=90,
        raw_min=0,
        raw_max=900,
        digits=1,
        maker_key="Max_Lade_TW",
        maker_category="SOL-WW",
        description="Maximale Ladetemperatur Trinkwasser",
    )

    hold_value = temperature(
        41807,
        writable=True,
        min_value=20,
        max_value=90,
        raw_min=200,
        raw_max=900,
        digits=1,
        maker_key="TW_Haltewert",
        maker_category="SOL-WW",
        description="Haltewert Trinkwasser",
    )

    setpoint_active = temperature(
        41808,
        min_value=5,
        max_value=90,
        raw_min=50,
        raw_max=900,
        digits=1,
        maker_key="Aktiver_TW_Sollw",
        maker_category="SOL-WW",
        description="Aktiver Trinkwassersollwert",
    )

    special_setpoint = temperature(
        41809,
        writable=True,
        min_value=5,
        max_value=90,
        raw_min=50,
        raw_max=900,
        digits=1,
        maker_key="Sonder_TW_Sollw",
        maker_category="SOL-WW",
        description="Sonder-Trinkwassersollwert",
    )

    mode = enum(
        40112,
        OperatingMode,
        writable=True,
        options=OPERATING_MODE_OPTIONS,
        maker_key="BetriebsArt_TW",
        maker_category="ALG-BTR",
        description="Betriebsart Trinkwasser",
    )

    solar_operating_hours = integer(
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
        description="Solarkreisbetriebsstunden",
    )

    storage_status = enum(
        41827,
        StorageStatus,
        maker_key="Speicherstatus",
        maker_category="ALG-BTR",
        description="Betriebszustand der Trinkwasserspeicherung",
    )

    return_max = temperature(
        41828,
        writable=True,
        min_value=5,
        max_value=90,
        raw_min=50,
        raw_max=900,
        digits=1,
        maker_key="RücklSollw_TW",
        maker_category="SOL-RL",
        description="Maximale Rücklauftemperatur Trinkwasser",
    )

    disinfection_temp = temperature(
        41830,
        writable=True,
        min_value=60,
        max_value=90,
        raw_min=600,
        raw_max=900,
        digits=1,
        maker_key="ThermDes_Sollw",
        maker_category="SOL-WW",
        description="Desinfektionstemperatur",
    )

    disinfection_weekday = enum(
        41831,
        Weekday,
        writable=True,
        options=WEEKDAY_OPTIONS,
        maker_key="ThermDes_Tag",
        maker_category="SOL-WW",
        description="Wochentag der thermischen Desinfektion",
    )

    disinfection_start = time_value(
        41832,
        writable=True,
        min_value=time(0, 0),
        max_value=time(23, 45),
        raw_min=0,
        raw_max=2345,
        maker_key="ThermDes_Start",
        maker_category="SOL-WW",
        description="Startzeit der thermischen Desinfektion",
    )

    disinfection_stop = time_value(
        41833,
        writable=True,
        min_value=time(0, 0),
        max_value=time(23, 45),
        raw_min=0,
        raw_max=2345,
        maker_key="ThermDes_Stop",
        maker_category="SOL-WW",
        description="Stoppzeit der thermischen Desinfektion",
    )

    active_charge_setpoint = temperature(
        41838,
        min_value=20,
        max_value=90,
        raw_min=200,
        raw_max=900,
        digits=1,
        maker_key="Aktiver_Lade_Soll",
        maker_category="SOL-WW",
        description="Aktiver Ladetemperatur-Sollwert",
    )

    disinfection_hold = integer(
        41839,
        signed=False,
        writable=True,
        min_value=0,
        max_value=255,
        raw_min=0,
        raw_max=255,
        digits=0,
        unit="min",
        maker_key="ThermDes_Halte",
        maker_category="SOL-WW",
        description="Haltezeit der Desinfektionstemperatur",
    )

    control_deviation = gauge(
        41863,
        0.1,
        signed=True,
        min_value=-100,
        max_value=100,
        raw_min=-1000,
        raw_max=1000,
        digits=1,
        unit="K",
        maker_key="Regeldiff_TW",
        maker_category="RPA-SON",
        description="Regeldifferenz Trinkwasserkreis",
    )

    ### coils

    manual_active = coil(8)

    charge_pump_running = coil(60, writable=True)

    circulation_pump_running = coil(61, writable=True)

    charge_pump_control_autonomous = coil(
        99,
        false_key="glt",
        true_key="autonomous",
        false_label="GLT",
        true_label="Autark",
        maker_key="EBN_Binär_BA4",
        maker_category="EBN-BA",
        description="Steuerungsebene Speicherladepumpe",
    )

    mode_control_autonomous = coil(
        95,
        false_key="glt",
        true_key="autonomous",
        false_label="GLT",
        true_label="Autark",
        maker_key="EBN_BetrArt_TW",
        maker_category="EBN-BTR",
        description="Steuerungsebene Betriebsart Trinkwasser",
    )

    circulation_pump_control_autonomous = coil(
        100,
        false_key="glt",
        true_key="autonomous",
        false_label="GLT",
        true_label="Autark",
        maker_key="EBN_Binär_BA5",
        maker_category="EBN-BA",
        description="Steuerungsebene Zirkulationspumpe",
    )

    special_setpoint_control_autonomous = coil(
        112,
        false_key="glt",
        true_key="autonomous",
        false_label="GLT",
        true_label="Autark",
        maker_key="EBN_Son_TW_Sollw",
        maker_category="EBN-VL",
        description="Steuerungsebene Sonder-Trinkwassersollwert",
    )

    intermediate_heating_function_enabled = coil(
        407,
        writable=True,
        maker_key="FB07_Zwischenhzg",
        maker_category="CON-WW",
        description="Funktionsblock CO4-FB07 Zwischenheizbetrieb",
    )

    automatic = coil(1800)

    disinfection_active = coil(1801)

    priority = coil(1802)

    max_charge_limit_active = coil(1803)

    return_limit_active = coil(1804)

    standby = coil(1805)

    frost_protection = coil(1806)

    forced_charge = coil(1807, writable=True)

    solar_pump_running = coil(1808)

    forced_charge_uses_sensor_2 = coil(
        1809,
        writable=True,
        false_key="inactive",
        true_key="active",
        false_label="Inaktiv",
        true_label="Aktiv",
        maker_key="SF2_anstatt_SF1",
        maker_category="ALG-BTR",
        description="Zwangsladung durch Umschaltung von SF1 auf SF2",
    )

    storage_charging_active = coil(
        1810,
        false_key="inactive",
        true_key="active",
        false_label="Inaktiv",
        true_label="Aktiv",
        maker_key="Speicherlad_TW",
        maker_category="ALG-SON",
        description="Speicherladung aktiv",
    )

    storage_charging_enabled = coil(
        1811,
        writable=True,
        false_key="inactive",
        true_key="active",
        false_label="Inaktiv",
        true_label="Aktiv",
        maker_key="Speicherlad_En",
        maker_category="ALG-SON",
        description="Freigabe Speicherladung",
    )

    storage_charging_locked = coil(
        1812,
        false_key="inactive",
        true_key="active",
        false_label="Inaktiv",
        true_label="Aktiv",
        maker_key="SpeicherladSperr",
        maker_category="ALG-SON",
        description="Speicherladung durch Entladeschutz gesperrt",
    )

    intermediate_heating_operation = coil(
        1831,
        writable=True,
        maker_key="FB07_Zwischenhzg",
        maker_category="CON-WW",
        description=(
            "Zwischenheizbetrieb; von der 55Pro-App und der bewährten "
            "Legacy-Konfiguration verwendeter Spiegelpunkt"
        ),
    )

    # Override coils released before a write (no per-index stride here).
    ebene_coils = {
        "mode": (95, 0),
        "charge_pump_running": (99, 0),
        "circulation_pump_running": (100, 0),
        "special_setpoint": (112, 0),
    }

    @property
    def day_temperature_range(self) -> TemperatureRange | None:
        """Day setpoint range implied by setpoint and hysteresis."""
        if self.setpoint_day is None or self.hysteresis is None:
            return None
        return TemperatureRange(
            minimum=self.setpoint_day,
            maximum=round(self.setpoint_day + self.hysteresis, 1),
        )

    @property
    def night_temperature_range(self) -> TemperatureRange | None:
        """Night/holding range implied by hold value and hysteresis."""
        if self.hold_value is None or self.hysteresis is None:
            return None
        return TemperatureRange(
            minimum=self.hold_value,
            maximum=round(self.hold_value + self.hysteresis, 1),
        )

    async def set_setpoint(self, celsius: float) -> None:
        """Set the hot-water day setpoint (°C)."""
        await self.async_write_datapoint("setpoint_day", celsius)

    async def set_mode(self, mode: OperatingMode) -> None:
        """Set the operating mode."""
        await self.async_write_datapoint("mode", mode)

    async def set_disinfection_start(self, value: time) -> None:
        """Set the start of the thermal-disinfection window."""
        await self.async_write_datapoint("disinfection_start", value)

    async def set_disinfection_stop(self, value: time) -> None:
        """Set the end of the thermal-disinfection window."""
        await self.async_write_datapoint("disinfection_stop", value)

    async def start_forced_charge(self) -> None:
        """Trigger a one-off storage charge."""
        await self.async_write_datapoint("forced_charge", True)
