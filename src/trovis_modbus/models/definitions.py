"""Static controller-model and physical-input definitions."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from ..enums import ControllerModel


class InputRole(StrEnum):
    """Possible electrical role of one physical controller input."""

    RESISTANCE_SENSOR = "resistance_sensor"
    BINARY_INPUT = "binary_input"
    ANALOG_VOLTAGE = "analog_voltage"
    ANALOG_CURRENT = "analog_current"
    POTENTIOMETER = "potentiometer"
    PULSE_INPUT = "pulse_input"


@dataclass(frozen=True, slots=True)
class RegisterViewDefinition:
    """One firmware register view of a physical input.

    ``measurement_key`` names the existing descriptor exposed by
    :class:`trovis_modbus.subsystems.sensors.Sensors`. A register view may be
    valid for more than one electrical role. This is needed, for example, when
    the same measured voltage represents a 0-to-10-V input directly or a
    0(4)-to-20-mA input through the documented shunt resistor.
    """

    measurement_key: str
    register: int
    roles: tuple[InputRole, ...]

    def __post_init__(self) -> None:
        if not self.measurement_key:
            raise ValueError("measurement_key must not be empty")
        if not 40001 <= self.register <= 49999:
            raise ValueError(
                f"register must be a holding-register reference: {self.register}"
            )
        if not self.roles:
            raise ValueError("a register view must support at least one input role")
        if len(set(self.roles)) != len(self.roles):
            raise ValueError(
                f"duplicate roles for register view {self.measurement_key!r}"
            )


@dataclass(frozen=True, slots=True)
class PhysicalInputDefinition:
    """Static electrical description of one physical controller input."""

    terminal: int
    paired_common: int | None
    manufacturer_labels: tuple[str, ...]
    possible_roles: tuple[InputRole, ...]
    conflict_group: str
    register_views: tuple[RegisterViewDefinition, ...]

    def __post_init__(self) -> None:
        if self.terminal <= 0:
            raise ValueError("terminal must be positive")
        if self.paired_common is not None and self.paired_common <= 0:
            raise ValueError("paired_common must be positive")
        if self.paired_common == self.terminal:
            raise ValueError("paired_common must differ from terminal")
        if not self.manufacturer_labels:
            raise ValueError("manufacturer_labels must not be empty")
        if not self.possible_roles:
            raise ValueError("possible_roles must not be empty")
        if len(set(self.possible_roles)) != len(self.possible_roles):
            raise ValueError(
                f"duplicate roles in conflict group {self.conflict_group!r}"
            )
        if not self.conflict_group:
            raise ValueError("conflict_group must not be empty")

        measurement_keys = [view.measurement_key for view in self.register_views]
        if len(set(measurement_keys)) != len(measurement_keys):
            raise ValueError(
                f"duplicate measurement keys in conflict group {self.conflict_group!r}"
            )

        possible_roles = set(self.possible_roles)
        for view in self.register_views:
            unsupported = set(view.roles) - possible_roles
            if unsupported:
                raise ValueError(
                    f"register view {view.measurement_key!r} uses unsupported roles: "
                    f"{sorted(role.value for role in unsupported)}"
                )

    def view_for_key(self, measurement_key: str) -> RegisterViewDefinition | None:
        """Return the register view for ``measurement_key``, if present."""
        return next(
            (
                view
                for view in self.register_views
                if view.measurement_key == measurement_key
            ),
            None,
        )


@dataclass(frozen=True, slots=True)
class ModelDefinition:
    """Static hardware definition for one TROVIS controller model."""

    model: ControllerModel
    heating_circuits: int
    inputs: tuple[PhysicalInputDefinition, ...]

    def __post_init__(self) -> None:
        if self.heating_circuits not in (2, 3):
            raise ValueError("heating_circuits must be 2 or 3")
        if not self.inputs:
            raise ValueError("a model definition must contain physical inputs")

        terminals = [input_definition.terminal for input_definition in self.inputs]
        if len(set(terminals)) != len(terminals):
            raise ValueError(f"duplicate terminals in model {self.model.value}")

        conflict_groups = [
            input_definition.conflict_group for input_definition in self.inputs
        ]
        if len(set(conflict_groups)) != len(conflict_groups):
            raise ValueError(f"duplicate conflict groups in model {self.model.value}")

        measurement_keys = [
            view.measurement_key
            for input_definition in self.inputs
            for view in input_definition.register_views
        ]
        if len(set(measurement_keys)) != len(measurement_keys):
            raise ValueError(f"duplicate measurement keys in model {self.model.value}")

    def input_for_terminal(self, terminal: int) -> PhysicalInputDefinition | None:
        """Return the physical input starting at ``terminal``, if present."""
        return next(
            (
                input_definition
                for input_definition in self.inputs
                if input_definition.terminal == terminal
            ),
            None,
        )

    def input_for_measurement(
        self, measurement_key: str
    ) -> PhysicalInputDefinition | None:
        """Return the physical input that exposes ``measurement_key``."""
        return next(
            (
                input_definition
                for input_definition in self.inputs
                if input_definition.view_for_key(measurement_key) is not None
            ),
            None,
        )


def register_view(
    measurement_key: str,
    register: int,
    *roles: InputRole,
) -> RegisterViewDefinition:
    """Create a concise immutable register-view definition."""
    return RegisterViewDefinition(measurement_key, register, roles)


def physical_input(
    terminal: int,
    *manufacturer_labels: str,
    possible_roles: tuple[InputRole, ...],
    register_views: tuple[RegisterViewDefinition, ...],
    paired_common: int | None = None,
) -> PhysicalInputDefinition:
    """Create a physical input with a stable terminal-based conflict group."""
    paired_suffix = f"_{paired_common}" if paired_common is not None else ""
    return PhysicalInputDefinition(
        terminal=terminal,
        paired_common=paired_common,
        manufacturer_labels=manufacturer_labels,
        possible_roles=possible_roles,
        conflict_group=f"terminal_{terminal}{paired_suffix}",
        register_views=register_views,
    )
