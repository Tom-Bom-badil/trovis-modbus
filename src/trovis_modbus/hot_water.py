"""The domestic hot water circuit (HK4 / TW): setpoints and disinfection."""

from __future__ import annotations

import datetime

from .enums import OperatingMode, StorageStatus, Weekday
from .model import (
    TrovisComponent,
    coil,
    enum,
    gauge,
    integer,
    raw_register,
    temperature,
)
from .options import OPERATING_MODE_OPTIONS, WEEKDAY_OPTIONS
from .utils import time_from_hhmm


class HotWater(TrovisComponent):
    """Domestic hot water: setpoints, charging and thermal disinfection."""

    # Override coils released before a write (no per-index stride here).
    ebene_coils = {
        "mode": (95, 0),
        "charge_pump_running": (99, 0),
        "circulation_pump_running": (100, 0),
        "special_setpoint": (112, 0),
    }

    ### registers

    mode = enum(
        40112,
        OperatingMode,
        writable=True,
        options=OPERATING_MODE_OPTIONS,
        maker_key="BetriebsArt_TW",
        maker_category="ALG-BTR",
        description="Betriebsart Trinkwasser",
    )

    setpoint_day = temperature(
        41800,
        writable=True,
        min_value=20,
        max_value=90,
        digits=1,
        maker_key="TW_Sollw",
        maker_category="SOL-WW",
        description="Trinkwasser Sollwert",
    )

    setpoint_active = temperature(
        41808,
        maker_key="Aktiver_TW_Sollw",
        maker_category="SOL-WW",
        description="Aktiver Trinkwassersollwert",
    )
    special_setpoint = temperature(
        41809,
        writable=True,
        min_value=5,
        max_value=90,
        digits=1,
        maker_key="Sonder_TW_Sollw",
        maker_category="SOL-WW",
        description="Sonder-Trinkwassersollwert",
    )

    setpoint_max = temperature(
        41801,
        writable=True,
        min_value=20,
        max_value=90,
        digits=1,
    )

    setpoint_min = temperature(
        41802,
        writable=True,
        min_value=20,
        max_value=90,
        digits=1,
    )

    hysteresis = gauge(
        41803,
        0.1,
        unit="K",
        writable=True,
    )

    charge_overshoot = gauge(
        41804,
        0.1,
        unit="K",
        writable=True,
    )

    max_charge_temp = temperature(41806, writable=True)

    hold_value = temperature(
        41807,
        writable=True,
        min_value=20,
        max_value=90,
        digits=1,
        maker_key="TW_Haltewert",
        maker_category="SOL-WW",
        description="Haltewert Trinkwasser",
    )

    solar_operating_hours = integer(
        41813,
        signed=False,
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

    active_charge_setpoint = temperature(41838)

    return_max = temperature(41828, writable=True)
    disinfection_temp = temperature(41830, writable=True)

    disinfection_weekday = enum(
        41831,
        Weekday,
        writable=True,
        options=WEEKDAY_OPTIONS,
    )

    _disinfection_start_raw = raw_register(41832, writable=True)
    _disinfection_stop_raw = raw_register(41833, writable=True)
    disinfection_hold = integer(41839, writable=True, unit="min")
    control_deviation = gauge(
        41863,
        0.1,
        signed=True,
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
    intermediate_heating_operation = coil(
        407,
        writable=True,
        maker_key="FB07_Zwischenheizen",
        description="Zwischenheizbetrieb",
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

    @property
    def disinfection_start(self) -> datetime.time | None:
        """Start time of the thermal-disinfection window."""
        return time_from_hhmm(self._disinfection_start_raw)

    @property
    def disinfection_stop(self) -> datetime.time | None:
        """End time of the thermal-disinfection window."""
        return time_from_hhmm(self._disinfection_stop_raw)

    async def set_setpoint(self, celsius: float) -> None:
        """Set the hot-water day setpoint (°C)."""
        await self.async_write_datapoint("setpoint_day", celsius)

    async def set_mode(self, mode: OperatingMode) -> None:
        """Set the operating mode."""
        await self.async_write_datapoint("mode", mode)

    async def start_forced_charge(self) -> None:
        """Trigger a one-off storage charge."""
        await self.async_write_datapoint("forced_charge", True)
