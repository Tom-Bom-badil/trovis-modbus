"""The heating circuits (Hk (Heizkreis) 1-3, also called Rk (Regelkreis) 1-3)."""

from __future__ import annotations

from . import utils
from .enums import OperatingMode
from .model import TrovisComponent, coil, enum, gauge, integer, temperature
from .options import OPERATING_MODE_OPTIONS


class HeatingCircuit(TrovisComponent):
    """One heating circuit. Construct with ``index`` 1, 2 or 3.

    Addresses follow the controller's offset pattern: the 1000-block steps by
    200 per circuit, mode/control-signal by 2, pumps/manual status by 1. Because
    those per-field strides differ, each circuit stays a per-``index`` instance
    with a field-level ``stride`` — not a ``repeating_group`` / ``base_offset``
    block, which shifts every address of an instance by one uniform amount and
    so can't express the 200/2/1 mix.
    """

    ### registers

    mode = enum(
        40106,
        OperatingMode,
        stride=2,
        writable=True,
        options=OPERATING_MODE_OPTIONS,
        maker_key="BetriebsArt_Rk1",
        maker_category="ALG-BTR",
        description="Betriebsart Rk",
    )

    valve_setpoint = integer(
        40107,
        signed=False,
        stride=2,
        min_value=0,
        max_value=100,
        raw_min=0,
        raw_max=100,
        digits=0,
        unit="%",
        maker_key="Stellsignal_Rk1",
        maker_category="ALG-BTR",
        description="Stellsignal Rk",
    )

    flow_setpoint = temperature(
        41000,
        stride=200,
        min_value=5,
        max_value=150,
        raw_min=50,
        raw_max=1500,
        digits=1,
        maker_key="VorlSollw_Rk1",
        maker_category="SOL-VL",
        description="Vorlaufsollwert Rk",
    )

    flow_max = temperature(
        41001,
        stride=200,
        writable=True,
        min_value=5,
        max_value=150,
        raw_min=50,
        raw_max=1500,
        digits=1,
        maker_key="MaxVorl_Rk1",
        maker_category="SOL-VL",
        description="Maximale Vorlauftemperatur Rk",
    )

    flow_min = temperature(
        41002,
        stride=200,
        writable=True,
        min_value=-5,
        max_value=150,
        raw_min=-50,
        raw_max=1500,
        digits=1,
        maker_key="MinVorl_Rk1",
        maker_category="SOL-VL",
        description="Minimale Vorlauftemperatur Rk",
    )

    room_setpoint_day = temperature(
        41003,
        stride=200,
        writable=True,
        min_value=0,
        max_value=40,
        raw_min=0,
        raw_max=400,
        digits=1,
        maker_key="Tag_Soll_Rk1",
        maker_category="SOL-RT",
        description="Raumsollwert Tag",
    )

    room_setpoint_night = temperature(
        41004,
        stride=200,
        writable=True,
        min_value=0,
        max_value=40,
        raw_min=0,
        raw_max=400,
        digits=1,
        maker_key="Nacht_Soll_Rk1",
        maker_category="SOL-RT",
        description="Raumsollwert Nacht",
    )

    # HR41005 is present in the established device model but not described in
    # the final 5578 register table. Do not invent manufacturer limits here.
    room_setpoint_active = temperature(41005, stride=200)

    slope = gauge(
        41006,
        0.1,
        stride=200,
        writable=True,
        min_value=0.2,
        max_value=3.2,
        raw_min=2,
        raw_max=32,
        digits=1,
        maker_key="Steig_HeizKL_Rk1",
        maker_category="KNL-VL",
        description="Steigung VL Heizkennlinie",
    )

    level = gauge(
        41007,
        0.1,
        stride=200,
        writable=True,
        min_value=-30,
        max_value=30,
        raw_min=-300,
        raw_max=300,
        digits=1,
        unit="K",
        maker_key="Niv_HeizKL_Rk1",
        maker_category="KNL-VL",
        description="Niveau VL Heizkennlinie",
    )

    return_slope = gauge(
        41009,
        0.1,
        stride=200,
        min_value=0.2,
        max_value=3.2,
        raw_min=2,
        raw_max=32,
        digits=1,
        maker_key="Stg_RücklKL_Rk1",
        maker_category="KNL-RL",
        description="Steigung Rücklaufkennlinie",
    )

    return_level = gauge(
        41010,
        0.1,
        stride=200,
        min_value=-30,
        max_value=30,
        raw_min=-300,
        raw_max=300,
        digits=1,
        unit="K",
        maker_key="Niv_RücklKL_Rk1",
        maker_category="KNL-RL",
        description="Niveau Rücklaufkennlinie",
    )

    return_max = temperature(
        41011,
        stride=200,
        writable=True,
        min_value=5,
        max_value=90,
        raw_min=50,
        raw_max=900,
        digits=1,
        maker_key="MaxRückl_Rk1",
        maker_category="SOL-RL",
        description="Maximale Rücklauftemperatur Rk",
    )

    return_base_point = temperature(
        41012,
        stride=200,
        min_value=5,
        max_value=90,
        raw_min=50,
        raw_max=900,
        digits=1,
        maker_key="Fuß_Rückl_Rk1",
        maker_category="SOL-RL",
        description="Fußpunkt Rücklauftemperatur Rk",
    )

    return_setpoint = temperature(
        41033,
        stride=200,
        min_value=5,
        max_value=90,
        raw_min=50,
        raw_max=900,
        digits=1,
        maker_key="RücklSollw_Rk1",
        maker_category="SOL-RL",
        description="Rücklaufsollwert Rk",
    )

    fixed_setpoint_day = temperature(
        41042,
        stride=200,
        writable=True,
        min_value=-5,
        max_value=130,
        raw_min=-50,
        raw_max=1300,
        digits=1,
        maker_key="TagSoll_FW_Rk1",
        maker_category="SOL-SON",
        description="Sollwert Tagbetrieb bei Festwertregelung",
    )

    fixed_setpoint_night = temperature(
        41043,
        stride=200,
        writable=True,
        min_value=-5,
        max_value=130,
        raw_min=-50,
        raw_max=1300,
        digits=1,
        maker_key="NachtSoll_FW_Rk1",
        maker_category="SOL-SON",
        description="Sollwert Nachtbetrieb bei Festwertregelung",
    )

    flow_deviation = gauge(
        41063,
        0.1,
        stride=200,
        signed=True,
        min_value=-100,
        max_value=100,
        raw_min=-1000,
        raw_max=1000,
        digits=1,
        unit="K",
        maker_key="Regeldiff_Vorl_Rk1",
        maker_category="RPA-SON",
        description="Regeldifferenz Vorlauf Rk",
    )

    ### coils

    manual_active = coil(5, stride=1)

    pump_running = coil(57, stride=1, writable=True)

    valve_closing = coil(
        62,
        stride=2,
        false_key="stopped",
        true_key="closing",
        false_label="Halt",
        true_label="Zu",
        maker_key="Binärausg_BA6",
        maker_category="BEA-BA",
        description="Dreipunkt-Stellsignal Schließen",
    )

    valve_opening = coil(
        63,
        stride=2,
        false_key="stopped",
        true_key="opening",
        false_label="Halt",
        true_label="Auf",
        maker_key="Binärausg_BA7",
        maker_category="BEA-BA",
        description="Dreipunkt-Stellsignal Öffnen",
    )

    mode_control_autonomous = coil(
        89,
        stride=2,
        false_key="glt",
        true_key="autonomous",
        false_label="GLT",
        true_label="Autark",
        maker_key="EBN_BetrArt_Rk1",
        maker_category="EBN-BTR",
        description="Steuerungsebene Betriebsart",
    )

    valve_control_autonomous = coil(
        90,
        stride=2,
        false_key="glt",
        true_key="autonomous",
        false_label="GLT",
        true_label="Autark",
        maker_key="EBN_Stellsig_Rk1",
        maker_category="EBN-BTR",
        description="Steuerungsebene Stellsignal",
    )

    pump_control_autonomous = coil(
        96,
        stride=1,
        false_key="glt",
        true_key="autonomous",
        false_label="GLT",
        true_label="Autark",
        maker_key="EBN_Binär_BA1",
        maker_category="EBN-BA",
        description="Steuerungsebene Umwälzpumpe",
    )

    flow_setpoint_control_autonomous = coil(
        116,
        stride=2,
        false_key="glt",
        true_key="autonomous",
        false_label="GLT",
        true_label="Autark",
        maker_key="EBN_VorlSoll_Rk1",
        maker_category="EBN-VL",
        description="Steuerungsebene Vorlaufsollwert",
    )

    return_setpoint_control_autonomous = coil(
        117,
        stride=2,
        false_key="glt",
        true_key="autonomous",
        false_label="GLT",
        true_label="Autark",
        maker_key="EBN_RückSoll_Rk1",
        maker_category="EBN-RL",
        description="Steuerungsebene Rücklaufsollwert",
    )

    room_setpoint_control_autonomous = coil(
        122,
        stride=1,
        false_key="glt",
        true_key="autonomous",
        false_label="GLT",
        true_label="Autark",
        maker_key="EBN_RaumSoll_Rk1",
        maker_category="EBN-RT",
        description="Steuerungsebene aktiver Raumsollwert",
    )

    room_control_unit = coil(703, stride=1, writable=True)

    automatic = coil(1000, stride=200)

    day_active = coil(1001, stride=200)

    night_active = coil(1002, stride=200)

    hold_active = coil(1003, stride=200)

    setback_active = coil(1004, stride=200)

    heat_up_active = coil(1005, stride=200)

    return_limit_active = coil(1006, stride=200)

    outside_shutdown = coil(1007, stride=200)

    standby = coil(1008, stride=200)

    frost_protection = coil(1009, stride=200)

    optimization = coil(
        2107,
        stride=100,
        writable=True,
        maker_key="FB07_Optimierung_Rk1",
        description="Optimierung Rk",
    )

    adaptation = coil(
        2108,
        stride=100,
        writable=True,
        maker_key="FB08_Adaption_Rk1",
        description="Adaption Rk",
    )

    # Override coils (mode 89+2n, pump 96+1n) released before a write.
    ebene_coils = {"mode": (89, 2), "pump_running": (96, 1)}

    def heating_curve(self, mode: str = "active") -> list[float] | None:
        """Flow-temperature curve over outside temps -20..20 °C.

        ``mode``: ``"active"`` (follow day/night state), ``"day"`` or
        ``"night"``. Returns ``None`` if a required value is missing.
        """
        if mode == "day" or (mode == "active" and self.day_active):
            room = self.room_setpoint_day
        else:
            room = self.room_setpoint_night

        slope, level = self.slope, self.level
        flow_min, flow_max = self.flow_min, self.flow_max

        if None in (room, slope, level, flow_min, flow_max):
            return None

        return utils.heating_curve(
            room_setpoint=room,  # type: ignore[arg-type]
            slope=slope,  # type: ignore[arg-type]
            level=level,  # type: ignore[arg-type]
            flow_min=flow_min,  # type: ignore[arg-type]
            flow_max=flow_max,  # type: ignore[arg-type]
        )

    async def set_mode(self, mode: OperatingMode) -> None:
        """Set the operating mode."""
        await self.async_write_datapoint("mode", mode)

    async def set_room_setpoint_day(self, celsius: float) -> None:
        """Set the day room setpoint (°C)."""
        await self.async_write_datapoint("room_setpoint_day", celsius)

    async def set_room_setpoint_night(self, celsius: float) -> None:
        """Set the night room setpoint (°C)."""
        await self.async_write_datapoint("room_setpoint_night", celsius)
