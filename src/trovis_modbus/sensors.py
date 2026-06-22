"""Temperature inputs (only those wired to a probe report a value)."""

from __future__ import annotations

from .component import Component, temperature


class Sensors(Component):
    """All temperature inputs of the controller."""

    outside_1 = temperature(9, doc="Outside sensor AF1")
    outside_2 = temperature(10, doc="Outside sensor AF2")
    flow_1 = temperature(12, doc="Flow sensor VF1")
    flow_2 = temperature(13, doc="Flow sensor VF2")
    flow_3 = temperature(14, doc="Flow sensor VF3")
    flow_4 = temperature(15, doc="Flow sensor VF4")
    return_1 = temperature(16, doc="Return sensor RüF1")
    return_2 = temperature(17, doc="Return sensor RüF2")
    return_3 = temperature(18, doc="Return sensor RüF3")
    room_1 = temperature(19, doc="Room sensor RF1")
    room_2 = temperature(20, doc="Room sensor RF2")
    room_3 = temperature(21, doc="Room sensor RF3")
    storage_1 = temperature(22, doc="Storage sensor SF1")
    storage_2 = temperature(23, doc="Storage sensor SF2")
    storage_3 = temperature(24, doc="Storage/remote sensor SF3/FG3")
    remote_1 = temperature(25, unit="K", doc="Remote adjuster FG1")
    remote_2 = temperature(26, unit="K", doc="Remote adjuster FG2")
