"""Static logical sensor capabilities for TROVIS controller models."""

from __future__ import annotations

from dataclasses import dataclass

from ..enums import ControllerModel


@dataclass(frozen=True, slots=True)
class SensorVariant:
    """Logical sensors whose meaning depends on the controller configuration.

    A variant may contain one sensor key. In that case, the sensor is available
    only for one of the configurable input modes; another mode may use the same
    input for a non-sensor function such as a binary input.

    A variant with several sensor keys describes alternative logical sensor
    meanings. The later resolver selects the active sensor from the controller's
    configuration, functions, parameters, and relevant coils.
    """

    sensor_keys: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.sensor_keys:
            raise ValueError("sensor variant must contain at least one sensor key")
        if any(not sensor_key for sensor_key in self.sensor_keys):
            raise ValueError("sensor variant keys must not be empty")
        if len(set(self.sensor_keys)) != len(self.sensor_keys):
            raise ValueError("sensor variant keys must be unique")

    def contains(self, sensor_key: str) -> bool:
        """Return whether this variant contains ``sensor_key``."""
        return sensor_key in self.sensor_keys


@dataclass(frozen=True, slots=True)
class ModelDefinition:
    """Static logical sensor capabilities of one TROVIS controller model."""

    model: ControllerModel
    heating_circuits: int
    sensor_keys: tuple[str, ...]
    sensor_variants: tuple[SensorVariant, ...] = ()

    def __post_init__(self) -> None:
        if self.heating_circuits not in (2, 3):
            raise ValueError("heating_circuits must be 2 or 3")
        if not self.sensor_keys:
            raise ValueError("a model definition must contain sensor keys")
        if any(not sensor_key for sensor_key in self.sensor_keys):
            raise ValueError("sensor keys must not be empty")
        if len(set(self.sensor_keys)) != len(self.sensor_keys):
            raise ValueError(f"duplicate sensor keys in model {self.model.value}")

        supported_sensor_keys = set(self.sensor_keys)
        variant_sensor_keys: set[str] = set()
        variant_signatures: set[tuple[str, ...]] = set()

        for variant in self.sensor_variants:
            unsupported = set(variant.sensor_keys) - supported_sensor_keys
            if unsupported:
                raise ValueError(
                    f"sensor variant in model {self.model.value} contains "
                    f"unsupported sensor keys: {sorted(unsupported)}"
                )

            signature = variant.sensor_keys
            if signature in variant_signatures:
                raise ValueError(
                    f"duplicate sensor variant in model {self.model.value}: "
                    f"{signature!r}"
                )
            variant_signatures.add(signature)

            duplicate_membership = variant_sensor_keys & set(variant.sensor_keys)
            if duplicate_membership:
                raise ValueError(
                    f"sensor keys occur in several variants in model "
                    f"{self.model.value}: {sorted(duplicate_membership)}"
                )
            variant_sensor_keys.update(variant.sensor_keys)

    @property
    def measurement_keys(self) -> tuple[str, ...]:
        """Return the supported logical sensor keys.

        ``measurement_keys`` remains as a neutral read-only alias while callers
        move to the more precise :attr:`sensor_keys` name.
        """
        return self.sensor_keys

    @property
    def variant_sensor_keys(self) -> frozenset[str]:
        """Return sensor keys whose meaning or availability is configurable."""
        return frozenset(
            sensor_key
            for variant in self.sensor_variants
            for sensor_key in variant.sensor_keys
        )

    @property
    def fixed_sensor_keys(self) -> frozenset[str]:
        """Return sensor keys that are not part of a configurable variant."""
        return frozenset(self.sensor_keys) - self.variant_sensor_keys

    def supports_sensor(self, sensor_key: str) -> bool:
        """Return whether the controller model exposes ``sensor_key``."""
        return sensor_key in self.sensor_keys

    def sensor_variant_for(self, sensor_key: str) -> SensorVariant | None:
        """Return the configurable variant containing ``sensor_key``."""
        return next(
            (
                variant
                for variant in self.sensor_variants
                if variant.contains(sensor_key)
            ),
            None,
        )


def sensor_variant(*sensor_keys: str) -> SensorVariant:
    """Create one concise immutable sensor variant."""
    return SensorVariant(sensor_keys=sensor_keys)
