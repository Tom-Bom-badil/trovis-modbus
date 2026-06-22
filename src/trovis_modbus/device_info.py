"""Device identity: the controller's model, versions and serial number."""

from __future__ import annotations

from dataclasses import dataclass

from .component import Component, gauge, integer


@dataclass(frozen=True, slots=True)
class DeviceInfo:
    """Static identity of a Trovis controller.

    Maps cleanly onto Home Assistant's ``DeviceInfo`` (manufacturer, model,
    sw_version, hw_version, serial_number).
    """

    manufacturer: str
    model: str
    serial_number: str | None
    firmware_version: str | None
    hardware_version: str | None


class DeviceInformation(Component):
    """Controller identity and firmware/hardware versions."""

    system = gauge(1, 0.1, signed=False, doc="Hydraulic system code")
    _model_raw = integer(0, signed=False)
    _firmware_raw = gauge(2, 0.01, signed=False)
    _hardware_raw = gauge(3, 0.01, signed=False)
    _serial_raw = integer(5, signed=False)

    @property
    def model(self) -> str:
        """Model name, e.g. 'Trovis 5579'."""
        value = self._model_raw
        return f"Trovis {value}" if value else "Trovis 557x"

    @property
    def firmware_version(self) -> str | None:
        """Firmware version, e.g. '3.05'."""
        value = self._firmware_raw
        return f"{value:.2f}" if value is not None else None

    @property
    def hardware_version(self) -> str | None:
        """Hardware version."""
        value = self._hardware_raw
        return f"{value:.2f}" if value is not None else None

    @property
    def serial_number(self) -> str | None:
        """Internal controller ID / serial number."""
        value = self._serial_raw
        return str(value) if value is not None else None

    @property
    def device_info(self) -> DeviceInfo:
        """A static identity snapshot for Home Assistant."""
        return DeviceInfo(
            manufacturer="Samson",
            model=self.model,
            serial_number=self.serial_number,
            firmware_version=self.firmware_version,
            hardware_version=self.hardware_version,
        )
