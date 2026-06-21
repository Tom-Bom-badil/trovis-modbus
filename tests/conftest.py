"""Fixtures: a real Modbus TCP server preloaded with Trovis-shaped values."""

from __future__ import annotations

import asyncio
import socket
from collections.abc import AsyncIterator

import pytest
from modbus_connection.pymodbus import connect_tcp
from pymodbus.datastore import (
    ModbusDeviceContext,
    ModbusSequentialDataBlock,
    ModbusServerContext,
)
from pymodbus.server import ModbusTcpServer

from trovis_modbus import Trovis557x

UNIT_ID = 1

# Raw register words keyed by address (see test_device.py for the decoded view).
HOLDING: dict[int, int] = {
    0: 5579,  # model
    1: 21,  # Anlage -> 2.1
    2: 305,  # firmware -> 3.05
    9: 123,  # AF1 -> 12.3 °C
    12: 0x10000 - 50,  # VF1 -> -5.0 °C (int16 negative)
    22: 450,  # SF1 -> 45.0 °C
    23: 32767,  # SF2 -> NaN sentinel -> None
    99: 1430,  # time -> 14:30
    100: 2106,  # date -> 21.06
    101: 2026,  # year
    102: 1,  # switch top -> Auto
    105: 1,  # hk1 Betriebsart -> Auto
    112: 1505,  # summer-on date -> 15.05
    1000: 800,  # hk1 vl_max -> 80.0
    1001: 200,  # hk1 vl_min -> 20.0
    1002: 200,  # hk1 raumsoll_tag -> 20.0
    1003: 150,  # hk1 raumsoll_nacht -> 15.0
    1005: 10,  # hk1 steigung -> 1.0
    1006: 0,  # hk1 niveau -> 0.0
    1799: 500,  # hk4 soll -> 50.0
    1802: 100,  # hk4 schaltdifferenz -> 10.0
    1803: 220,  # hk4 ueberhoehung -> 22.0
    1806: 480,  # hk4 haltewert -> 48.0
    1830: 3,  # disinfection weekday -> Mi
    1831: 1900,  # disinfection start -> 19:00
}

COILS: dict[int, bool] = {
    56: True,  # hk1 circulation pump
    1000: True,  # hk1 day mode (drives heating-curve soll selection)
}


def _block(
    mapping: dict[int, int | bool], size: int = 2100
) -> ModbusSequentialDataBlock:
    values = [0] * (size + 1)
    for address, value in mapping.items():
        values[address + 1] = int(value)  # pymodbus datastore is 1-based
    return ModbusSequentialDataBlock(0, values)


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


@pytest.fixture
async def trovis() -> AsyncIterator[Trovis557x]:
    device = ModbusDeviceContext(
        co=_block(COILS), hr=_block(HOLDING), di=_block({}), ir=_block({})
    )
    context = ModbusServerContext(devices={UNIT_ID: device}, single=False)
    host, port = "127.0.0.1", _free_port()
    server = ModbusTcpServer(context, address=(host, port))
    task = asyncio.create_task(server.serve_forever())
    for _ in range(100):
        try:
            _, writer = await asyncio.open_connection(host, port)
        except OSError:
            await asyncio.sleep(0.02)
            continue
        writer.close()
        await writer.wait_closed()
        break

    conn = await connect_tcp(host, port=port)
    device_api = Trovis557x(conn.for_unit(UNIT_ID))
    try:
        yield device_api
    finally:
        await conn.close()
        await server.shutdown()
        task.cancel()
        try:
            await task
        except (asyncio.CancelledError, Exception):
            pass
