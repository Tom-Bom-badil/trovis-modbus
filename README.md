# trovis-modbus

[![CI](https://github.com/Tom-Bom-badil/trovis-modbus/actions/workflows/ci.yml/badge.svg?branch=develop)](https://github.com/Tom-Bom-badil/trovis-modbus/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/trovis-modbus.svg)](https://pypi.org/project/trovis-modbus/)
[![Python](https://img.shields.io/pypi/pyversions/trovis-modbus.svg)](https://pypi.org/project/trovis-modbus/)
[![License](https://img.shields.io/github/license/Tom-Bom-badil/trovis-modbus.svg)](LICENSE)

> [!IMPORTANT]
> Additional documentation and contributor instructions are available in the
> [project wiki](https://github.com/Tom-Bom-badil/trovis-modbus/wiki).

`trovis-modbus` is an asynchronous Python library for reading and writing
SAMSON TROVIS 557x heating controllers over Modbus.

The library is backend-neutral. It consumes a
[`modbus_connection.ModbusUnit`](https://github.com/home-assistant-libs/modbus-connection)
provided by the application and does not create or own the physical transport.
Applications may therefore use any backend supported by `modbus-connection`.

The Home Assistant integration is maintained separately in
[`trovis-modbus-hass`](https://github.com/Tom-Bom-badil/trovis-modbus-hass).

## Scope

The project provides a practical control and monitoring model for the essential
TROVIS functions. It is intended for automatic device discovery, operational
monitoring, and occasional fine adjustment of an already commissioned heating
system.

It does not attempt to reproduce every controller menu, parameter level,
special function, or possible hydraulic scenario.

## Features

- Automatic controller-model probe
- Automatic hydronic-system identification
- Documented model-to-hydronic-system compatibility metadata
- Role-aware technical control circuits `Rk1` through `Rk4`
- Hydronic roles for heating, pre-control, buffer-tank, domestic-hot-water, and
  unused circuits
- Automatic physical-sensor detection
- Resolution of configurable sensor, analog, current, and pulse inputs
- Dedicated solar-circuit subsystem
- Buffer-tank-specific extensions for `Rk1` without duplicating its common
  control-circuit block
- Conservative model-specific register and coil ranges
- Grouped, range-aware reads with preserved manufacturer block boundaries
- Read and write support with TROVIS write-access handling
- Field-specific validation and TROVIS-specific write preconditions
- Neutral metadata for units, limits, steps, enums, value types, and writable
  state
- Native Python `date` and `time` values plus year-independent `MonthDay`
  values
- Central handling of scaling, signed values, and TROVIS invalid-value
  sentinels
- Command-line query tool for diagnostics outside Home Assistant

## Supported controllers and hydronic systems

| Controller | Technical slots Rk1-Rk3 | Documented hydronic systems |
| --- | ---: | ---: |
| TROVIS 5573 | 2 | 29 |
| TROVIS 5573-1 | 2 | 29 |
| TROVIS 5575 | 2 | 33 |
| TROVIS 5576 | 2 | 52 |
| TROVIS 5578 | 3 | 90 |
| TROVIS 5578-E | 3 | 95 |
| TROVIS 5579 | 3 | 85 |

The library preserves known model gaps and manufacturer register or coil block
boundaries. Reads are never planned across those boundaries.

A globally known hydronic-system code may still be undocumented for a
particular controller model. Applications can inspect this through
`device.configuration_supported_by_model`.

## Control-circuit model

`Rk1` through `Rk4` are stable technical identities:

- `Rk1` to `Rk3` may act as a heating circuit, pre-control circuit,
  buffer-tank circuit, or remain unused.
- `Rk4` represents domestic hot water when the selected hydronic system
  includes DHW.
- A pre-control circuit uses the same technical Rk register block in the
  controller's demand-only mode.
- A buffer-tank circuit reuses the common `Rk1` block and adds only the
  buffer-specific extension registers.
- Solar is an independent subsystem and is not one of the Rk slots.

Useful topology properties include:

```python
device.control_circuit_indices
device.control_circuit_role(index)
device.room_heating_circuit_indices
device.has_rk4
device.has_solar
device.has_buffer_tank_circuit
device.configuration_supported_by_model
```

## Device structure

A `Trovis557x` object exposes the following main subsystems:

| Attribute | Description |
| --- | --- |
| `info` | Model, firmware, hardware version, and serial information |
| `controller` | Controller-wide status and settings |
| `clock` | Native controller date and time |
| `sensors` | Physical temperature, analog, current, pulse, and remote-control inputs |
| `rk1` | Technical control circuit Rk1 |
| `rk2` | Technical control circuit Rk2 |
| `rk3` | Technical control circuit Rk3 on supported models |
| `rk4` | Domestic-hot-water circuit Rk4 |
| `solar` | Optional solar-thermal circuit |
| `buffer_tank` | Optional buffer-tank-specific extension of Rk1 |
| `activity` | Combined plant activity |

Only the subsystems relevant to the detected controller model and hydronic
system are included in the active polling group.

## Basic usage

The application creates or obtains a `ModbusUnit` and injects it into the
library:

```python
from modbus_connection import ModbusUnit
from trovis_modbus import Trovis557x


async def inspect_controller(unit: ModbusUnit) -> None:
    probe = await Trovis557x.async_probe(unit)

    device = Trovis557x(
        unit,
        model=probe.model,
        detected_sensors=probe.detected_sensors,
    )

    await device.async_update()

    print("Model:", device.model)
    print("Hydronic system:", device.configuration_code)
    print("Rk1 role:", device.control_circuit_role(1))
    print("Outside temperature:", device.sensors.af1)
    print("Controller date:", device.clock.date)

    if device.has_rk4:
        print("Domestic hot water:", device.rk4)

    if device.has_solar:
        print("Solar operating hours:", device.solar.operating_hours)

    await device.async_enable_writing()
    try:
        await device.rk1.set_room_setpoint_day(21.5)
    finally:
        await device.async_disable_writing()
```

Connection creation, sharing, reconnect behavior, and transport lifecycle remain
the responsibility of the calling application.

## Metadata and writes

The library is the source of truth for neutral TROVIS datapoint metadata,
including:

- manufacturer register or coil reference
- zero-based Modbus address
- scaling and signed conversion
- unit and display precision
- minimum, maximum, and step
- enum options
- invalid-value handling
- readable and writable state
- TROVIS-specific write preconditions

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

Install the optional CLI backend and run the tool:

```bash
python -m pip install -e ".[cli]"
python script/query.py tcp 192.168.1.50 --unit 246
python script/query.py serial /dev/ttyUSB0 --unit 246
```

Use `--framer rtu` for transparent RTU over TCP or `--framer socket` for native
Modbus TCP.

## Breaking changes in version 2

Version 2 introduces a role-aware control-circuit model and intentionally
replaces the former public `hk1` to `hk3` and `ww` identities with `rk1` to
`rk4`.

Applications using the former attributes must update their component access and
tests. The configuration and subsystem modules were also reorganized:

```text
src/trovis_modbus/
├── configurations/
│   ├── address_ranges.py
│   ├── hydronic_systems.py
│   ├── sensor_variants.py
│   ├── settings.py
│   └── trovis_models.py
└── subsystems/
    ├── circuit_buffer_tank.py
    ├── circuit_dhw.py
    ├── circuit_heating.py
    ├── circuit_solar.py
    ├── controller.py
    ├── date_time.py
    ├── heat_meters.py
    └── sensors.py
```

## Development and tests

Install the project in editable mode:

```bash
python -m pip install -e .
```

Use the repository scripts:

```bash
script/format.sh
script/libtest.sh
script/libcheck.sh
```

- `format.sh` applies safe Ruff fixes and formats the repository.
- `libtest.sh` runs the pytest suite with the `modbus-connection` mock backend.
- `libcheck.sh` verifies formatting and linting, compiles the sources, runs the
  tests, and builds the source distribution and wheel.

No physical controller or external Modbus server is required for the normal
unit tests. Details about local development dependencies, branches, and the
contribution workflow are documented in the
[project wiki](https://github.com/Tom-Bom-badil/trovis-modbus/wiki).

## License

Apache-2.0
