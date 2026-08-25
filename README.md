# `trovis-modbus` Python library

[![CI](https://github.com/Tom-Bom-badil/trovis-modbus/actions/workflows/ci.yml/badge.svg?branch=develop)](https://github.com/Tom-Bom-badil/trovis-modbus/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/trovis-modbus.svg)](https://pypi.org/project/trovis-modbus/)
[![Python](https://img.shields.io/pypi/pyversions/trovis-modbus.svg)](https://pypi.org/project/trovis-modbus/)
[![License](https://img.shields.io/github/license/Tom-Bom-badil/trovis-modbus.svg)](LICENSE)

<img width="100%" alt="SAMSON TROVIS controllers" src="https://github.com/Tom-Bom-badil/trovis-modbus/wiki/images/trovis-lib-pic.png" />

<br/>`trovis-modbus` is an asynchronous, transport-independent Python library for communicating with **SAMSON TROVIS 557x** heating and district heating controllers and compatible OEM variants over Modbus.

The library was developed primarily as the backend for the corresponding Home Assistant integration [`trovis-modbus-hass`](https://github.com/Tom-Bom-badil/trovis-modbus-hass). As it is kept independent of Home Assistant, it can also be used by other Python applications and projects.

## Purpose and scope

`trovis-modbus` is intended for operational monitoring and occasional fine tuning of already commissioned heating systems. It does **not** attempt to reproduce every controller menu, parameter level, special function, register, or coil (there are thousands of them). It is also not intended as an initial commissioning tool for new heating systems - please use the free SAMSON TROVIS-VIEW software for this.

The library:

* provides the auto-discovery and auto-configuration logic required to determine the controller model and its capabilities, the configured hydronic system, sensor and input assignments, and the relevant controller functions, parameters, and configuration settings,

* contains the controller-specific data model, including valid registers and coils, their data types and metadata, and the rules required for safe reads and writes,

* determines which datapoints are valid for the actual installation based on the detected controller model, configured hydronic system, active functions and parameters, and physical sensor/input assignments,

* does **not** create or own the Modbus transport. Applications using the library provide a [`modbus_connection.ModbusUnit`](https://github.com/home-assistant-libs/modbus-connection) and may use any backend supported by `modbus-connection` (pymodbus, tmodbus, ...).

An example script `query.py` in the code of the library shows how to build an application that can query any TROVIS heating controller by using Modbus/TCP, Modbus/RTU with ser2net, or direct serial connection.

## Supported controllers

| Controller               | Rk1-Rk3 / Heating | Rk4 / DHW | Hydronic systems | Comments                             |
| :----------------------- | :---------------: | :-------: | :--------------: | :----------------------------------- |
| SAMSON TROVIS 5573       |         2         |     x     |        29        |                                      |
| SAMSON TROVIS 5573-1     |         2         |     x     |        29        |                                      |
| SAMSON TROVIS 5575       |         2         |     x     |        33        |                                      |
| SAMSON TROVIS 5576       |         2         |     x     |        52        |                                      |
| SAMSON TROVIS 5578       |         3         |     x     |        90        |                                      |
| SAMSON TROVIS 5578-E     |         3         |     x     |        95        |                                      |
| SAMSON TROVIS 5579       |         3         |     x     |        85        |                                      |
| SAUTER EQJW126F001       |         1         |           |         1        | TROVIS 5573, Rk1 and Anlage 1.0 only |
| SAUTER EQJW146F001       |         2         |     x     |        29        | TROVIS 5573                          |
| SAUTER EQJW146F002       |         2         |     x     |        29        | TROVIS 5573-1                        |
| SAUTER EQJW246F002       |         3         |     x     |        90        | TROVIS 5578                          |
| SAUTER EQJW246F003       |         3         |     x     |        95        | TROVIS 5578-E                        |
| YADOS YADO|MATIC 01      |         2         |     x     |        33        | TROVIS 5575                          |
| YADOS YADO|MATIC 01-0003 |         2         |     x     |        33        | TROVIS 5575                          |
| YADOS YADO|MATIC 03      |         2         |     x     |        29        | TROVIS 5573                          |
| YADOS YADO|MATIC 03-1003 |         2         |     x     |        29        | TROVIS 5573-1                        |
| YADOS YADO|MATIC 08      |         3         |     x     |        90        | TROVIS 5578-1114                     |
| PEWO PCR06               |         2         |     x     |        33        | TROVIS 5575                          |

<sup>Note: Not all non-SAMSON models have yet been tested. The figures are based on the currently available documentation.</sup>

## Data provided by the library

Depending on the controller model and its configuration, `trovis-modbus` provides:

* controller identity, firmware, hardware, serial, and system information,

* the current hydronic system,

* measured temperatures and other physical sensor inputs (analog, pulse, etc.),

* controller-wide functions and parameters,

* technical control circuits Rk1 through Rk4 together with their hydronic roles and data
  (known roles: pre-control, heating, domestic hot water, buffer, solar),

* operating modes, setpoints, pump and valve states, and controller date/time,

* derived operating information, including automatically calculated heating curves for all applicable heating circuits and an overall controller status indicator,

* neutral datapoint metadata such as unit, scale, limits, step, enum options, invalid values, and writable state,

* grouped reads and validated writes, including TROVIS write-access handling and the mechanisms required to write-enable special/protected registers.

The exact datapoints exposed for a controller therefore reflect the capabilities and configuration of the actual installation rather than a static model-wide register list.

## Testing and validation

All releases of the library are tested with the following hardware setup:

* 1× `TROVIS 5578`: dedicated testing device, Anlage 6.1 (fully equipped with 17 Pt1000 sensors),

* 1× `TROVIS 5579`: dedicated testing device, Anlage 5.1 (fully equipped with 17 Pt1000 sensors),

* 1× `TROVIS 5576`: live heating controller, Anlage 2.1 (4 required + 4 additional Pt1000 sensors).

Additional software-based tests are part of the project to ensure code quality and consistency.

## Documentation, development and contribution guidelines

Detailed architecture, usage examples, datapoint behavior, development setup, branch workflow, contribution guidance, and known limitations are documented in the [project wiki](https://github.com/Tom-Bom-badil/trovis-modbus/wiki).

Support and documentation specific to the Home Assistant integration are maintained separately in [`trovis-modbus-hass`](https://github.com/Tom-Bom-badil/trovis-modbus-hass).
