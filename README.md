# trovis-modbus

[![CI](https://github.com/Tom-Bom-badil/trovis-modbus/actions/workflows/ci.yml/badge.svg?branch=develop)](https://github.com/Tom-Bom-badil/trovis-modbus/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/trovis-modbus.svg)](https://pypi.org/project/trovis-modbus/)
[![Python](https://img.shields.io/pypi/pyversions/trovis-modbus.svg)](https://pypi.org/project/trovis-modbus/)
[![License](https://img.shields.io/github/license/Tom-Bom-badil/trovis-modbus.svg)](LICENSE)

> [!IMPORTANT]
> Additional documentation and contributor instructions are available in the
> [project wiki](https://github.com/Tom-Bom-badil/trovis-modbus/wiki).

`trovis-modbus` is an asynchronous Python library for reading and writing
Samson TROVIS 557x heating controllers over Modbus.

The library is backend-neutral: it consumes a
[`modbus_connection.ModbusUnit`](https://github.com/home-assistant-libs/modbus-connection)
and does not create or own the transport itself. Applications may therefore use
`tmodbus`, `pymodbus`, or another backend supported by `modbus-connection`.

The Home Assistant integration is maintained separately in
[`trovis-modbus-hass`](https://github.com/Tom-Bom-badil/trovis-modbus-hass).

## Features

- Object-oriented access to controller, sensor, heating-circuit, hot-water, and clock data
- Automatic controller-model probe and physical-sensor detection
- Conservative model-specific register and coil profiles
- Grouped, range-aware reads with a maximum span of 50 registers or coils
- Read and write support with TROVIS write-access handling
- Field-specific validation and TROVIS-specific write preconditions
- Neutral metadata for units, limits, steps, enums, value types, and writable state
- Complete operating-mode and control-level modelling
- Native Python `date` and `time` values plus year-independent `MonthDay` values
- Operational status values for heating circuits and domestic hot water
- Derived plant activity and hot-water temperature ranges
- Central handling of scaling, signed values, and TROVIS invalid-value sentinels

## Supported model profiles

| Models | Heating circuits | Register and coil profile |
| --- | ---: | --- |
| TROVIS 5573, 5573-1, 5575, 5576 | 2 | TROVIS 5573 Rev. 2.54 |
| TROVIS 5578, 5578-E, 5579 | 3 | TROVIS 5578 Rev. 2.62 final |

Known gaps and manufacturer block boundaries are preserved. Reads are never
planned across those boundaries.

## Device structure

A `Trovis557x` object exposes the following subsystems:

| Attribute | Description |
| --- | --- |
| `info` | Model, firmware, hardware version, and serial information |
| `controller` | Controller-wide status and settings |
| `clock` | Native controller date and time |
| `sensors` | Physical temperature, analog, pulse, and remote-control inputs |
| `heating_circuit_1` | Heating circuit Rk1 |
| `heating_circuit_2` | Heating circuit Rk2 |
| `heating_circuit_3` | Heating circuit Rk3 on supported models |
| `hot_water` | Domestic-hot-water circuit Rk4 |
| `activity` | Combined heating and hot-water activity |

`device.heating_circuits` contains only the heating circuits supported by the
detected model.

## Basic usage

Install the library together with the desired `modbus-connection` backend.
This example uses `tmodbus` and transparent RTU over TCP:

```python
import asyncio

from modbus_connection.tmodbus import connect_tcp
from trovis_modbus import Trovis557x


async def main() -> None:
    connection = await connect_tcp(
        "192.168.1.50",
        port=502,
        framer="rtu",
    )

    try:
        unit = connection.for_unit(246)
        probe = await Trovis557x.async_probe(unit)

        device = Trovis557x(
            unit,
            model=probe.model,
            detected_sensors=probe.detected_sensors,
        )

        await device.async_update()
        print("Model:", device.model)
        print("Outside temperature:", device.sensors.af1)
        print("Controller date:", device.clock.date)
        print("Plant activity:", device.activity)

        await device.async_enable_writing()
        try:
            await device.heating_circuit_1.set_room_setpoint_day(21.5)
        finally:
            await device.async_disable_writing()
    finally:
        await connection.close()


asyncio.run(main())
```

For native Modbus TCP with MBAP framing, use `framer="socket"`. Serial
transports are opened through the selected backend.

## Metadata and writes

The library is the source of truth for neutral TROVIS datapoint metadata,
including register or coil reference, scaling, unit, limits, step, enum options,
invalid values, and writable state.

Generic writes use:

```python
await component.async_write_datapoint(field, value)
```

The library refreshes TROVIS write access, validates the value, and performs
required device-specific preconditions before writing.

Catalog definitions use manufacturer references such as `HR40145` and `CL137`.
Conversion to zero-based Modbus addresses is centralized in the library.

## Command-line query tool

The repository contains `script/query.py` for querying a controller without
Home Assistant.

```bash
python -m pip install -e ".[cli]"
python script/query.py tcp 192.168.1.50 --unit 246
python script/query.py serial /dev/ttyUSB0 --unit 246
```

Use `--framer rtu` for transparent RTU over TCP or `--framer socket` for native
Modbus TCP.

## Development and tests

Using `uv`:

```bash
uv sync
uv run pytest
uvx prek run --all-files
```

Alternatively, install the project in editable mode and use the repository
scripts:

```bash
python -m pip install -e .
script/libtest.sh
script/libcheck.sh
```

- `libtest.sh` runs the pytest suite with the `modbus-connection` mock backend.
- `libcheck.sh` checks Ruff formatting and linting, compiles the sources, runs
  the tests, and builds the source distribution and wheel.

No physical controller or external Modbus server is required for the normal
unit tests. Details about the local `modbus-connection` checkout, development
branches, and contribution workflow are documented in the
[project wiki](https://github.com/Tom-Bom-badil/trovis-modbus/wiki).