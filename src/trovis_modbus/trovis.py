"""The top-level Trovis557x device object."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import TYPE_CHECKING

from modbus_connection.model import Component, ComponentGroup

from .addresses import register_address
from .configurations.address_ranges import (
    heating_circuit_count,
    ranges_for_model,
)
from .configurations.hydronic_systems import (
    ConfigurationTopology,
    get_configuration_definition,
)
from .configurations.sensor_variants import (
    SensorVariantResolution,
    SensorVariantStatus,
    resolve_sensor_variants,
)
from .configurations.settings import Functions, Parameters
from .configurations.trovis_models import get_model_definition_for_reported_model
from .data_model import (
    DEFAULT_WRITE_ACCESS_CODE,
    async_disable_writing,
    async_enable_writing,
    async_read_writing_enabled,
)
from .device_info import DeviceInformation
from .enums import ControlCircuitRole, SystemActivity
from .subsystems import (
    Clock,
    Controller,
    DomesticHotWater,
    HeatingCircuit,
    Sensors,
)

if TYPE_CHECKING:
    from modbus_connection import ModbusUnit


@dataclass(frozen=True)
class TrovisProbe:
    """Result of the safe setup probe."""

    model: int
    detected_sensors: tuple[str, ...]

    @property
    def model_name(self) -> str:
        """Return the user-facing model name."""
        return f"Trovis {self.model}"


class Trovis557x:
    """A Samson TROVIS 557x heating controller."""

    def __init__(
        self,
        unit: ModbusUnit,
        *,
        model: int = 5578,
        detected_sensors: Iterable[str] = (),
    ) -> None:
        self._unit = unit
        self.model = model
        self.model_definition = get_model_definition_for_reported_model(model)

        # Probe results may contain several descriptor views of the same raw
        # register. Keep only logical sensor keys supported by this model. This
        # also sanitizes existing config entries created before ModelDefinition
        # became the authoritative model filter.
        self.probed_sensors = frozenset(detected_sensors)
        self.detected_sensors = frozenset(
            sensor_key
            for sensor_key in self.probed_sensors
            if self.model_definition.supports_sensor(sensor_key)
        )
        self.unsupported_detected_sensors = self.probed_sensors - self.detected_sensors

        self.info = DeviceInformation(unit)
        self.controller = Controller(unit)
        self.clock = Clock(unit)
        self.functions = Functions(unit)
        self.parameters = Parameters(unit)
        self.sensors = Sensors(unit)

        self.hk1 = HeatingCircuit(unit, index=1)
        self.hk2 = HeatingCircuit(unit, index=2)
        self.hk3 = HeatingCircuit(unit, index=3)

        self.ww = DomesticHotWater(unit)
        self._writing_enabled = False

        all_components = (
            self.info,
            self.controller,
            self.clock,
            self.functions,
            self.parameters,
            self.sensors,
            self.hk1,
            self.hk2,
            self.hk3,
            self.ww,
        )

        register_ranges, coil_ranges = ranges_for_model(model)
        for component in all_components:
            component.configure_readable_ranges(register_ranges, coil_ranges)

        # Ranges describe address availability. ModelDefinition additionally
        # limits logical sensor views that may share one readable register.
        self.sensors.configure_readable_fields(self.model_definition.sensor_keys)

        self._heating_circuits = (
            self.hk1,
            self.hk2,
            self.hk3,
        )[: heating_circuit_count(model)]

        self._group = ComponentGroup(unit, self.components)

    @classmethod
    async def async_probe(cls, unit: ModbusUnit) -> TrovisProbe:
        """Read only safe identity and sensor data for setup."""
        model = int(
            (
                await unit.read_holding_registers(
                    register_address(40001),
                    1,
                )
            )[0]
        )

        register_ranges, coil_ranges = ranges_for_model(model)
        model_definition = get_model_definition_for_reported_model(model)

        sensors = Sensors(unit)
        sensors.configure_readable_ranges(register_ranges, coil_ranges)
        sensors.configure_readable_fields(model_definition.sensor_keys)
        await sensors.async_update()

        detected_sensors = tuple(
            sensor_key
            for sensor_key in sensors.detected_sensor_names
            if model_definition.supports_sensor(sensor_key)
        )

        return TrovisProbe(
            model=model,
            detected_sensors=detected_sensors,
        )

    @property
    def heating_circuits(self) -> tuple[HeatingCircuit, ...]:
        """Return the built-in heating circuits for this model."""
        return self._heating_circuits

    @property
    def configuration_topology(self) -> ConfigurationTopology | None:
        """Return the known hydronic topology reported by the controller."""
        system_code = self.info.system_code
        if system_code is None:
            return None

        try:
            return get_configuration_definition(round(system_code * 10)).topology
        except KeyError:
            return None

    def control_circuit_role(self, index: int) -> ControlCircuitRole:
        """Return the role of technical slot Rk1 through Rk4."""
        if not 1 <= index <= 4:
            raise ValueError("control circuit index must be in range 1..4")

        if index <= 3 and index > len(self._heating_circuits):
            return ControlCircuitRole.UNUSED

        topology = self.configuration_topology
        if topology is not None:
            return topology.control_circuit_role(index)

        if index <= len(self._heating_circuits):
            return ControlCircuitRole.HEATING
        if index == 4:
            return ControlCircuitRole.DOMESTIC_HOT_WATER
        return ControlCircuitRole.UNUSED

    @property
    def control_circuit_indices(self) -> tuple[int, ...]:
        """Return technical Rk slots enabled by model and hydronic topology."""
        return tuple(
            index
            for index in range(1, 5)
            if self.control_circuit_role(index) is not ControlCircuitRole.UNUSED
        )

    @property
    def heating_circuit_indices(self) -> tuple[int, ...]:
        """Return Rk1 through Rk3 currently classified as heating circuits."""
        return tuple(
            index
            for index in range(1, len(self._heating_circuits) + 1)
            if self.control_circuit_role(index) is ControlCircuitRole.HEATING
        )

    @property
    def has_rk4(self) -> bool:
        """Return whether Rk4/WW is present or retained as safe fallback."""
        return self.control_circuit_role(4) is ControlCircuitRole.DOMESTIC_HOT_WATER

    @property
    def components(self) -> tuple[Component, ...]:
        """Return every actively polled subsystem."""
        return (
            self.info,
            self.controller,
            self.clock,
            self.functions,
            self.parameters,
            self.sensors,
            *self.heating_circuits,
            self.ww,
        )

    @property
    def sensor_variant_resolution(self) -> SensorVariantResolution:
        """Return the current configuration-only sensor-variant diagnosis."""
        return resolve_sensor_variants(
            self.model_definition,
            self.functions,
            self.parameters,
        )

    @property
    def canonical_sensor_keys(self) -> frozenset[str]:
        """Return model-supported sensor keys with an unambiguous role.

        Fixed sensors and conclusively resolved variants are included.
        Inactive and unresolved variants are excluded without guessing from
        their values.
        """
        return frozenset(self.sensor_variant_resolution.canonical_sensor_keys)

    @property
    def available_sensor_keys(self) -> frozenset[str]:
        """Return detected sensors that are safe to expose as normal entities."""
        resolution = self.sensor_variant_resolution

        unresolved_single_role_keys = frozenset(
            result.variant_sensor_keys[0]
            for result in resolution.variants
            if result.status is SensorVariantStatus.UNRESOLVED
            and len(result.variant_sensor_keys) == 1
        )

        return self.detected_sensors & (
            frozenset(resolution.canonical_sensor_keys) | unresolved_single_role_keys
        )

    @property
    def unresolved_detected_sensor_keys(self) -> frozenset[str]:
        """Return detected role-specific views kept only for diagnostics."""
        return self.detected_sensors & frozenset(
            self.sensor_variant_resolution.unresolved_sensor_keys
        )

    @property
    def inactive_detected_sensor_keys(self) -> frozenset[str]:
        """Return detected views whose input is configured for non-sensor use."""
        return self.detected_sensors & frozenset(
            self.sensor_variant_resolution.inactive_sensor_keys
        )

    @property
    def system_activity(self) -> SystemActivity | None:
        """Return combined heating and WW system activity from pump states."""
        heating_states = tuple(
            circuit.pump_running for circuit in self.heating_circuits
        )
        ww_state = self.ww.storage_tank_charging_pump_running

        if all(state is None for state in (*heating_states, ww_state)):
            return None

        heating = any(state is True for state in heating_states)
        ww_active = ww_state is True
        if heating and ww_active:
            return SystemActivity.HEATING_AND_DOMESTIC_HOT_WATER
        if heating:
            return SystemActivity.HEATING
        if ww_active:
            return SystemActivity.DOMESTIC_HOT_WATER
        return SystemActivity.IDLE

    @property
    def writing_enabled(self) -> bool:
        """Whether writing is enabled by the integration safety switch."""
        return self._writing_enabled

    async def async_update(self) -> None:
        """Refresh all active subsystems in pooled Modbus reads."""
        await self._group.async_update()

    async def async_read_writing_enabled(self) -> bool:
        """Read the current write-enabled state directly from the controller."""
        return await async_read_writing_enabled(self._unit)

    async def async_enable_writing(
        self,
        access_code: int = DEFAULT_WRITE_ACCESS_CODE,
    ) -> None:
        """Enable TROVIS writing globally."""
        await async_enable_writing(self._unit, access_code)
        self._writing_enabled = True

    async def async_disable_writing(self) -> None:
        """Disable TROVIS writing globally."""
        try:
            await async_disable_writing(self._unit)
        finally:
            self._writing_enabled = False
