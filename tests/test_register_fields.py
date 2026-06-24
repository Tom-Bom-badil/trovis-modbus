"""Multi-register (32-bit) field support: decode, encode, and block planning."""

from __future__ import annotations

import struct

import pytest
from modbus_connection.mock import MockModbusConnection, MockModbusUnit

from trovis_modbus.component import (
    Component,
    _plan_blocks,
    float32,
    int32,
    integer,
    uint32,
)


class _Meter(Component):
    """A throwaway component exercising 32-bit fields (all read-only)."""

    energy = uint32(100, doc="Cumulative energy")
    energy_le = uint32(102, word_order="little", doc="Same, little word order")
    balance = int32(104, doc="Signed counter")
    flow = float32(106, doc="IEEE-754 flow")
    flow_scaled = float32(108, scale=10, doc="Scaled float")
    neighbour = integer(110, signed=False, doc="A plain 16-bit neighbour")


class _WritableMeter(Component):
    """Writable 32-bit fields, to exercise the multi-register write path."""

    energy = uint32(100, writable=True)
    balance = int32(104, writable=True)
    flow = float32(106, writable=True)


def _meter(values: dict[int, int]) -> _Meter:
    unit = MockModbusConnection().for_unit(1)
    unit.holding.update(values)
    return _Meter(unit)


async def test_uint32_decodes_two_registers() -> None:
    meter = _meter({100: 0x0001, 101: 0x86A0})  # 0x000186A0 = 100000
    await meter.async_update()
    assert meter.energy == 100000


async def test_uint32_word_order_little() -> None:
    meter = _meter({102: 0x86A0, 103: 0x0001})  # same value, low word first
    await meter.async_update()
    assert meter.energy_le == 100000


async def test_int32_negative() -> None:
    raw = (-12345) & 0xFFFFFFFF
    meter = _meter({104: raw >> 16, 105: raw & 0xFFFF})
    await meter.async_update()
    assert meter.balance == -12345


async def test_float32_decode() -> None:
    hi, lo = struct.unpack(">HH", struct.pack(">f", 3.14))
    meter = _meter({106: hi, 107: lo})
    await meter.async_update()
    assert meter.flow == pytest.approx(3.14, rel=1e-6)


async def test_float32_scaled() -> None:
    hi, lo = struct.unpack(">HH", struct.pack(">f", 1.5))
    meter = _meter({108: hi, 109: lo})
    await meter.async_update()
    assert meter.flow_scaled == pytest.approx(15.0)


async def test_write_roundtrip_32bit() -> None:
    """Writing a 32-bit field issues a multi-register write; read-back agrees."""
    unit = MockModbusConnection().for_unit(1)
    meter = _WritableMeter(unit)

    await meter.write("energy", 100000)
    await meter.write("balance", -12345)
    await meter.write("flow", 2.5)
    await meter.async_update()

    assert meter.energy == 100000
    assert meter.balance == -12345
    assert meter.flow == pytest.approx(2.5)
    # Each 32-bit write landed two consecutive registers.
    assert 100 in unit.holding and 101 in unit.holding


async def test_consolidated_read_fetches_meter_in_one_block() -> None:
    """A full read pools all fields (incl. the uint32) into a single call."""
    inner = MockModbusConnection().for_unit(1)
    inner.holding.update({100: 0x0001, 101: 0x86A0, 110: 7})

    class CountingUnit:
        def __init__(self, wrapped: MockModbusUnit) -> None:
            self._w = wrapped
            self.calls: list[tuple[int, int]] = []

        async def read_holding_registers(self, address: int, count: int) -> list[int]:
            self.calls.append((address, count))
            return await self._w.read_holding_registers(address, count)

        def __getattr__(self, name: str) -> object:
            return getattr(self._w, name)

    unit = CountingUnit(inner)
    meter = _Meter(unit)  # type: ignore[arg-type]
    await meter.async_update()

    # Addresses 100..111 are adjacent, so one block covers them — and the uint32
    # at 100 is fully inside it.
    assert len(unit.calls) == 1
    start, count = unit.calls[0]
    assert start == 100 and start + count >= 111  # covers 100..110 (neighbour)
    assert meter.energy == 100000
    assert meter.neighbour == 7


def test_plan_blocks_keeps_multiregister_whole_at_span_limit() -> None:
    """A 2-register value at the span boundary stays in one block, never split."""
    # 99 single registers (0..98) then a uint32 at 99 spanning 99 and 100. The old
    # single-address planner would cut at the 100-register span limit, splitting
    # the value; the span-aware planner keeps it whole.
    spans = [(address, 1) for address in range(99)] + [(99, 2)]
    blocks = _plan_blocks(spans)
    field_block = next(b for b in blocks if b[0] <= 99 < b[0] + b[1])
    assert field_block[0] <= 100 < field_block[0] + field_block[1]
