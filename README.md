# trovis-modbus

A standalone Python library that reads a **Samson Trovis 557x** heating
controller over Modbus.

It is a faithful port of the well-known
[`samson_trovis_557x`](https://github.com/Tom-Bom-badil/samson_trovis_557x)
Home Assistant YAML package: every sensor, register address, data type, scaling
factor, unit and enum mapping is reproduced — keyed by the original YAML
`unique_id` so the surfaces line up one-to-one.

## Design

- It **consumes the connection abstraction**, not a backend. The API accepts a
  [`modbus_connection.ModbusUnit`](../modbus-connection) (the per-device handle)
  and reads/writes Trovis registers through it. The library depends only on the
  `modbus-connection` *protocol* — you choose the backend (pymodbus, tmodbus, …).
- Values are exposed by their original YAML `unique_id` (e.g.
  `trovis_f_AF1`, `trovis_hk1_vlsoll`, `trovis_hk4_ladetemperatur`).

## What it exposes

| Group | Examples |
| --- | --- |
| Controller (`regler`) | model, firmware, error status, rotary switches, summer-limit |
| Sensors (`messwerte`) | 17 temperature probes: outside, flow, return, room, storage, remote |
| Heating circuits 1–3 | mode, 3-point signal, flow/return setpoints, slope, level |
| Hot water (`hk4`) | setpoints, hysteresis, charge/hold/disinfection temps, pumps |
| Date/time (`zeit`) | clock, date, summer-mode windows, disinfection schedule |
| Coils | hand/auto/day/night/standby/frost flags, circulation & charge pumps |
| Derived | formatted date/time, mode text, hot-water ranges, charge temp, heating curves |

Pure-dashboard template sensors from the YAML (status-image picker, button-tap
helpers, the `input_number` "what-if" simulators) are **not** device data and
are intentionally not reproduced.

## Use

```python
import asyncio
from modbus_connection.pymodbus import connect_tcp
from trovis_modbus import Trovis557x


async def main() -> None:
    conn = await connect_tcp("192.168.1.50", port=502)
    try:
        device = Trovis557x(conn.for_unit(1))   # unit 1 = the controller's Modbus address
        await device.async_update()

        print("Outside:", device.get("trovis_f_AF1"), "°C")
        print("HK1 flow setpoint:", device.get("trovis_hk1_vlsoll"), "°C")
        print("HK1 mode:", device.get("trovis_hk1_betriebsart_formatiert"))
        print("Hot-water charge temp:", device.get("trovis_hk4_ladetemperatur"), "°C")
        print("HK1 heating curve:", device.heating_curve(1))

        # Writable setpoints / switches
        await device.async_set_register("trovis_hk1_raumsoll_tag", 21.5)
        await device.async_set_coil("trovis_hk1_standby", True)
    finally:
        await conn.close()


asyncio.run(main())
```

`device.values` returns the full decoded mapping; `Trovis557x.all_keys`
enumerates everything (registers + coils + derived).

## Develop

```bash
uv sync
uv run pytest
```

The test suite cross-checks the catalog against the upstream YAML (cloned to
`/tmp/trovis-ref`) and exercises decoding/derived values against a real
in-process Modbus server.

Formatting/linting is [ruff](https://docs.astral.sh/ruff/), enforced in CI. Install
the commit hook with [prek](https://github.com/j178/prek):

```bash
uvx prek install          # format on commit
uvx prek run --all-files  # format + lint everything now
```
