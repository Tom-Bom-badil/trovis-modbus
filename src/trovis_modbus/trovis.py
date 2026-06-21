"""The Trovis557x device library — reads a Samson Trovis 557x over Modbus."""

from __future__ import annotations

from typing import TYPE_CHECKING

from modbus_connection import ModbusExceptionError

from . import derived
from .catalog import (
    COILS,
    COILS_BY_KEY,
    DERIVED,
    REGISTERS,
    REGISTERS_BY_KEY,
)

if TYPE_CHECKING:
    from modbus_connection import ModbusUnit

ValueType = float | int | bool | str | list[float] | None


class Trovis557x:
    """A Samson Trovis 557x heating controller reached through a ``ModbusUnit``.

    Call :meth:`async_update` to refresh, then read values by their (original
    YAML) ``unique_id`` key via :meth:`get`, the :attr:`values` mapping, or the
    convenience accessors. Writable setpoints/switches are written with
    :meth:`async_set_register` / :meth:`async_set_coil`.
    """

    def __init__(self, unit: ModbusUnit) -> None:
        self._unit = unit
        self._raw: dict[str, int | bool | None] = {}
        self._values: dict[str, ValueType] = {}

    # -- catalog (class-level, for enumeration / cross-checking) --------------

    register_keys: tuple[str, ...] = tuple(r.key for r in REGISTERS)
    coil_keys: tuple[str, ...] = tuple(c.key for c in COILS)
    derived_keys: tuple[str, ...] = tuple(d.key for d in DERIVED)
    all_keys: tuple[str, ...] = register_keys + coil_keys + derived_keys

    # -- update ---------------------------------------------------------------

    async def async_update(self) -> None:
        """Read every register and coil, decode, and compute derived values.

        Per-entity ``ModbusExceptionError`` (e.g. an unpopulated sensor) sets that
        value to ``None``; connection/timeout errors propagate so the caller can
        mark the whole device unavailable.
        """
        for register in REGISTERS:
            try:
                word = (await self._unit.read_holding_registers(register.address, 1))[0]
            except ModbusExceptionError:
                self._raw[register.key] = None
                self._values[register.key] = None
                continue
            self._raw[register.key] = word
            self._values[register.key] = register.decode(word)

        for coil in COILS:
            try:
                bit = (await self._unit.read_coils(coil.address, 1))[0]
            except ModbusExceptionError:
                self._raw[coil.key] = None
                self._values[coil.key] = None
                continue
            self._raw[coil.key] = bit
            self._values[coil.key] = bit

        self._compute_derived()

    # -- access ---------------------------------------------------------------

    @property
    def values(self) -> dict[str, ValueType]:
        """A copy of every decoded value, keyed by its YAML ``unique_id``."""
        return dict(self._values)

    def get(self, key: str) -> ValueType:
        """Decoded value for ``key`` (raises ``KeyError`` for unknown keys)."""
        if key not in self.all_keys:
            raise KeyError(key)
        return self._values.get(key)

    def raw(self, key: str) -> int | bool | None:
        """The undecoded register word / coil bit for ``key``."""
        return self._raw.get(key)

    def as_dict(self) -> dict[str, ValueType]:
        return dict(self._values)

    # -- writes ---------------------------------------------------------------

    async def async_set_register(self, key: str, value: float) -> None:
        """Write a holding register, reversing its scale/sign encoding."""
        register = REGISTERS_BY_KEY[key]
        if register.scale != 1.0:
            word = round(value / register.scale)
        else:
            word = int(value)
        if register.data_type == "int16" and word < 0:
            word &= 0xFFFF
        await self._unit.write_register(register.address, word)

    async def async_set_coil(self, key: str, value: bool) -> None:
        """Write a coil."""
        await self._unit.write_coil(COILS_BY_KEY[key].address, bool(value))

    # -- convenience accessors ------------------------------------------------

    @property
    def model(self) -> int | None:
        return self._int("trovis_r_modell")

    @property
    def firmware(self) -> float | None:
        return self._float("trovis_r_firmware")

    @property
    def outside_temperature(self) -> float | None:
        """Outside sensor AF1 (°C)."""
        return self._float("trovis_f_AF1")

    @property
    def error_status(self) -> int | None:
        return self._int("trovis_r_fehlerstatus")

    @property
    def collective_fault(self) -> bool | None:
        value = self._values.get("trovis_r_sammelstoerung")
        return value if isinstance(value, bool) else None

    def heating_curve(self, circuit: int, mode: str = "current") -> list[float] | None:
        """Flow-temperature curve for heating circuit 1-3.

        ``mode`` is ``"current"`` (follow the day/night state), ``"tag"`` (day) or
        ``"nacht"`` (night). Returns ``None`` if inputs are missing. The matching
        outside-temperature x-axis is :data:`derived.CURVE_X_VALUES`.
        """
        return self._heating_curve(circuit, mode)

    @property
    def curve_x_values(self) -> list[int]:
        return list(derived.CURVE_X_VALUES)

    # -- internals ------------------------------------------------------------

    def _int(self, key: str) -> int | None:
        value = self._values.get(key)
        return (
            int(value)
            if isinstance(value, (int, float)) and not isinstance(value, bool)
            else None
        )

    def _float(self, key: str) -> float | None:
        value = self._values.get(key)
        return (
            float(value)
            if isinstance(value, (int, float)) and not isinstance(value, bool)
            else None
        )

    def _heating_curve(self, circuit: int, mode: str) -> list[float] | None:
        if circuit not in (1, 2, 3):
            raise ValueError(f"heating circuit must be 1, 2 or 3, not {circuit}")
        try:
            niveau = self._values[f"trovis_hk{circuit}_niveau"]
            steigung = self._values[f"trovis_hk{circuit}_steigung"]
            vl_min = self._values[f"trovis_hk{circuit}_vl_min"]
            vl_max = self._values[f"trovis_hk{circuit}_vl_max"]
            tagsoll = self._values[f"trovis_hk{circuit}_raumsoll_tag"]
            nachtsoll = self._values[f"trovis_hk{circuit}_raumsoll_nacht"]
        except KeyError:
            return None
        if None in (niveau, steigung, vl_min, vl_max, tagsoll, nachtsoll):
            return None
        if mode == "tag":
            day = True
        elif mode == "nacht":
            day = False
        else:
            day = bool(self._values.get(f"trovis_hk{circuit}_tagbetrieb"))
        soll = int(tagsoll) if day else int(nachtsoll)  # type: ignore[arg-type]
        return derived.heating_curve(
            soll=soll,
            niveau=float(niveau),  # type: ignore[arg-type]
            steigung=float(steigung),  # type: ignore[arg-type]
            vl_min=float(vl_min),  # type: ignore[arg-type]
            vl_max=float(vl_max),  # type: ignore[arg-type]
        )

    def _compute_derived(self) -> None:
        v = self._values
        v["trovis_z_datum_formatiert"] = derived.format_date(
            self._raw_int("trovis_z_datum"), self._raw_int("trovis_z_jahr")
        )
        v["trovis_z_sommerbetrieb_ein_formatiert"] = derived.format_ddmm(
            self._raw_int("trovis_z_hk123_sommer_ein")
        )
        v["trovis_z_sommerbetrieb_aus_formatiert"] = derived.format_ddmm(
            self._raw_int("trovis_z_hk123_sommer_aus")
        )
        v["trovis_z_uhrzeit_formatiert"] = derived.format_time(
            self._raw_int("trovis_z_uhrzeit")
        )
        v["trovis_z_hk4_desinfektionstag_formatiert"] = derived.format_weekday(
            self._raw_int("trovis_z_hk4_desinfektionstag")
        )
        v["trovis_z_hk4_desinfektionsstart_formatiert"] = derived.format_time(
            self._raw_int("trovis_z_hk4_desinfektionsstart")
        )
        v["trovis_z_hk4_desinfektionsende_formatiert"] = derived.format_time(
            self._raw_int("trovis_z_hk4_desinfektionsende")
        )
        v["trovis_z_hk4_desinfektionsdauer_formatiert"] = derived.format_time(
            self._raw_int("trovis_z_hk4_desinfektionsdauer")
        )
        v["trovis_r_schalter_oben_formatiert"] = derived.format_switch(
            self._raw_int("trovis_r_schalteroben")
        )
        v["trovis_r_schalter_mitte_formatiert"] = derived.format_switch(
            self._raw_int("trovis_r_schaltermitte")
        )
        v["trovis_r_schalter_unten_formatiert"] = derived.format_switch(
            self._raw_int("trovis_r_schalterunten")
        )
        for circuit in (1, 2, 3, 4):
            v[f"trovis_hk{circuit}_betriebsart_formatiert"] = derived.format_switch(
                self._raw_int(f"trovis_hk{circuit}_betriebsart")
            )

        v["trovis_hk4_tagestemperaturen"] = self._range_text(
            "trovis_hk4_soll", "trovis_hk4_schaltdifferenz"
        )
        v["trovis_hk4_nachttemperaturen"] = self._range_text(
            "trovis_hk4_haltewert", "trovis_hk4_schaltdifferenz"
        )
        v["trovis_hk4_ladetemperatur"] = self._charge_temperature()
        v["trovis_hk123_heizkurven"] = self._heating_curve(1, "current")

    def _raw_int(self, key: str) -> int | None:
        value = self._values.get(key)
        return (
            int(value)
            if isinstance(value, (int, float)) and not isinstance(value, bool)
            else None
        )

    def _range_text(self, low_key: str, span_key: str) -> str | None:
        low = self._raw_int(low_key)
        span = self._raw_int(span_key)
        if low is None or span is None:
            return None
        return f"{low}-{low + span}°"

    def _charge_temperature(self) -> float | None:
        sf1 = self._float("trovis_f_SF1")
        ueberhoehung = self._float("trovis_hk4_ueberhoehung")
        if sf1 is None or ueberhoehung is None:
            return None
        return round(sf1 + ueberhoehung, 1)
