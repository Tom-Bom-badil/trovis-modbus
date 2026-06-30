"""The controller's readable Modbus address ranges.

Definitions use manufacturer references:
- HR numbers for holding registers, e.g. 40102
- CL numbers for coils, e.g. 137

The helpers convert these to zero-based Modbus PDU addresses for the block
planner.
"""

from __future__ import annotations

from .addresses import cl_range, hr_range

# (low, high) inclusive — sorted, non-overlapping.

REGISTER_RANGES: tuple[tuple[int, int], ...] = (
    hr_range(40001, 40007),
    hr_range(40010, 40041),
    hr_range(40099, 40155),
    hr_range(40160, 40167),
    hr_range(40201, 40215),
    hr_range(40300, 40320),
    hr_range(41000, 41045),
    hr_range(41054, 41072),
    hr_range(41090, 41096),
    hr_range(41200, 41244),
    hr_range(41256, 41272),
    hr_range(41400, 41444),
    hr_range(41456, 41472),
    hr_range(41800, 41813),
    hr_range(41828, 41840),
    hr_range(41856, 41871),
    hr_range(46470, 46526),
)

COIL_RANGES: tuple[tuple[int, int], ...] = (
    cl_range(1, 40),
    cl_range(57, 69),
    cl_range(88, 113),
    cl_range(116, 124),
    cl_range(130, 168),
    cl_range(176, 215),
    cl_range(222, 238),
    cl_range(245, 309),
    cl_range(322, 338),
    cl_range(998, 1009),
    cl_range(1017, 1019),
    cl_range(1025, 1045),
    cl_range(1200, 1209),
    cl_range(1212, 1213),
    cl_range(1217, 1219),
    cl_range(1225, 1238),
    cl_range(1400, 1409),
    cl_range(1412, 1413),
    cl_range(1417, 1419),
    cl_range(1425, 1438),
    cl_range(1800, 1809),
    cl_range(1825, 1845),
)
