"""Resolve documented TROVIS sensor variants from controller configuration."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING

from ..enums import ControllerModel
from .trovis_models import ModelDefinition, SensorVariant

if TYPE_CHECKING:
    from .settings import Functions, Parameters


class SensorVariantStatus(StrEnum):
    """Outcome of resolving one configurable logical sensor variant."""

    RESOLVED = "resolved"
    INACTIVE = "inactive"
    UNRESOLVED = "unresolved"
    INCONSISTENT = "inconsistent"


EvidenceValue = bool | int | None
Evidence = tuple[tuple[str, EvidenceValue], ...]


@dataclass(frozen=True, slots=True)
class ResolvedSensorVariant:
    """Diagnostic resolution result for one model-defined sensor variant."""

    variant_sensor_keys: tuple[str, ...]
    status: SensorVariantStatus
    selected_sensor_key: str | None
    candidate_sensor_keys: tuple[str, ...]
    reason: str
    evidence: Evidence = ()

    def __post_init__(self) -> None:
        variant_keys = set(self.variant_sensor_keys)
        if not self.variant_sensor_keys:
            raise ValueError("variant_sensor_keys must not be empty")
        if self.selected_sensor_key is not None:
            if self.status is not SensorVariantStatus.RESOLVED:
                raise ValueError("only a resolved variant may select a sensor key")
            if self.selected_sensor_key not in variant_keys:
                raise ValueError("selected sensor key must belong to the variant")
        if not set(self.candidate_sensor_keys) <= variant_keys:
            raise ValueError("candidate sensor keys must belong to the variant")

    @property
    def is_resolved(self) -> bool:
        """Return whether one canonical logical sensor was selected."""
        return self.status is SensorVariantStatus.RESOLVED


@dataclass(frozen=True, slots=True)
class SensorVariantResolution:
    """Configuration-only sensor-variant result for one controller model."""

    model: ControllerModel
    sensor_keys: tuple[str, ...]
    fixed_sensor_keys: tuple[str, ...]
    variants: tuple[ResolvedSensorVariant, ...]

    @property
    def selected_sensor_keys(self) -> tuple[str, ...]:
        """Return canonical sensor keys selected from resolved variants."""
        selected = {
            result.selected_sensor_key
            for result in self.variants
            if result.selected_sensor_key is not None
        }
        return tuple(key for key in self.sensor_keys if key in selected)

    @property
    def configured_sensor_keys(self) -> tuple[str, ...]:
        """Return fixed plus conclusively selected logical sensor keys.

        Ambiguous multi-role variants are deliberately omitted. Their raw
        descriptor values remain available for diagnostics, but none of their
        role-specific keys is safe to expose as a normal entity until a
        verified selector resolves the variant.
        """
        configured = set(self.fixed_sensor_keys) | set(self.selected_sensor_keys)
        return tuple(key for key in self.sensor_keys if key in configured)

    @property
    def canonical_sensor_keys(self) -> tuple[str, ...]:
        """Return the unambiguous logical sensor keys for normal consumers."""
        return self.configured_sensor_keys

    @property
    def inactive_sensor_keys(self) -> tuple[str, ...]:
        """Return variant keys conclusively configured for non-sensor mode."""
        inactive = {
            key
            for result in self.variants
            if result.status is SensorVariantStatus.INACTIVE
            for key in result.variant_sensor_keys
        }
        return tuple(key for key in self.sensor_keys if key in inactive)

    @property
    def unresolved_sensor_keys(self) -> tuple[str, ...]:
        """Return keys whose canonical logical role is not yet known."""
        unresolved = {
            key
            for result in self.variants
            if result.status
            in (SensorVariantStatus.UNRESOLVED, SensorVariantStatus.INCONSISTENT)
            for key in result.candidate_sensor_keys
        }
        return tuple(key for key in self.sensor_keys if key in unresolved)

    @property
    def has_unresolved_variants(self) -> bool:
        """Return whether at least one variant still needs more evidence."""
        return any(
            result.status
            in (SensorVariantStatus.UNRESOLVED, SensorVariantStatus.INCONSISTENT)
            for result in self.variants
        )

    def result_for(self, sensor_key: str) -> ResolvedSensorVariant | None:
        """Return the variant result containing ``sensor_key``."""
        return next(
            (
                result
                for result in self.variants
                if sensor_key in result.variant_sensor_keys
            ),
            None,
        )


# Common CO8 input assignments. Availability still comes from each model's
# coil ranges; a missing selector simply leaves the variant unresolved.
_COMMON_SENSOR_INPUTS = {
    "sf2": 4,
    "rf2": 6,
    "vf2": 9,
    "vf3": 10,
    "vf4": 11,
    "fg1": 15,
    "fg2": 16,
}

# TROVIS 5573 and 5573-1 share the same logical role selectors.
_TROVIS_5573_MODELS = {
    ControllerModel.TROVIS_5573,
    ControllerModel.TROVIS_5573_1,
}

# The smaller 5573/5573-1/5575 family exposes FG1/FG2 through CL801/CL802.
_SMALL_TWO_CIRCUIT_MODELS = _TROVIS_5573_MODELS | {
    ControllerModel.TROVIS_5575,
}

# Multi-role inputs for which CO8 can at least distinguish sensor from binary
# mode. CO8 alone does not choose one logical role from these groups.
_MULTI_ROLE_INPUTS = {
    frozenset(("sf2", "rf2", "analog_input_voltage", "pulse_rate")): 3,
    frozenset(("sf3", "analog_input_voltage", "pulse_rate")): 17,
    frozenset(("sf3", "fg3", "pulse_rate")): 17,
    frozenset(("ae1", "fg1")): 15,
    frozenset(("ae2", "fg2")): 16,
    frozenset(("ae3", "fg3", "sf3", "pulse_rate")): 17,
    frozenset(
        (
            "sf3",
            "fg3",
            "analog_input_voltage",
            "analog_input_current",
            "pulse_rate",
        )
    ): 17,
}


def _input_number_for(
    model: ControllerModel,
    variant: SensorVariant,
) -> int | None:
    """Return a verified CO8 input number for one variant, when known."""
    if len(variant.sensor_keys) > 1:
        return _MULTI_ROLE_INPUTS.get(frozenset(variant.sensor_keys))

    sensor_key = variant.sensor_keys[0]
    if model in _SMALL_TWO_CIRCUIT_MODELS and sensor_key in {"fg1", "fg2"}:
        return 1 if sensor_key == "fg1" else 2
    return _COMMON_SENSOR_INPUTS.get(sensor_key)


def _input_mode(
    functions: Functions,
    input_number: int,
) -> tuple[bool | None, Evidence]:
    """Return one CO8 input mode and its diagnostic evidence."""
    field_name = f"input_{input_number:02d}_is_binary"
    try:
        value = functions.input_is_binary(input_number)
    except KeyError:
        value = None
    return value, ((field_name, value),)


def _resolved_by_selector(
    variant: SensorVariant,
    selected_sensor_key: str,
    reason: str,
    evidence: Evidence,
) -> ResolvedSensorVariant:
    """Build a resolved result selected by documented function coils."""
    return ResolvedSensorVariant(
        variant_sensor_keys=variant.sensor_keys,
        status=SensorVariantStatus.RESOLVED,
        selected_sensor_key=selected_sensor_key,
        candidate_sensor_keys=(selected_sensor_key,),
        reason=reason,
        evidence=evidence,
    )


def _resolve_5573_variant(
    model: ControllerModel,
    variant: SensorVariant,
    functions: Functions,
) -> ResolvedSensorVariant | None:
    """Resolve the documented 5573/5573-1 SF2/RF2 and VF2/VF3/VF4 roles."""
    if model not in _TROVIS_5573_MODELS:
        return None

    variant_keys = frozenset(variant.sensor_keys)

    if variant_keys == frozenset(("sf2", "rf2")):
        sf2_enabled = getattr(functions, "storage_sensor_2_enabled", None)
        evidence: Evidence = (("storage_sensor_2_enabled", sf2_enabled),)
        if sf2_enabled is True:
            return _resolved_by_selector(
                variant,
                "sf2",
                "FB02 selects storage tank sensor SF2",
                evidence,
            )
        if sf2_enabled is False:
            return _resolved_by_selector(
                variant,
                "rf2",
                "FB02 is inactive, selecting room sensor RF2",
                evidence,
            )
        return ResolvedSensorVariant(
            variant_sensor_keys=variant.sensor_keys,
            status=SensorVariantStatus.UNRESOLVED,
            selected_sensor_key=None,
            candidate_sensor_keys=variant.sensor_keys,
            reason="FB02 SF2 selector is not available",
            evidence=evidence,
        )

    if variant_keys == frozenset(("vf2", "vf3", "vf4")):
        vf2_enabled = getattr(functions, "flow_sensor_2_enabled", None)
        vf4_enabled = getattr(functions, "flow_sensor_4_enabled", None)
        evidence = (
            ("flow_sensor_2_enabled", vf2_enabled),
            ("flow_sensor_4_enabled", vf4_enabled),
        )
        if vf2_enabled is True:
            selected = "vf2"
        elif vf4_enabled is True:
            selected = "vf4"
        elif vf2_enabled is False and vf4_enabled is False:
            selected = "vf3"
        else:
            return ResolvedSensorVariant(
                variant_sensor_keys=variant.sensor_keys,
                status=SensorVariantStatus.UNRESOLVED,
                selected_sensor_key=None,
                candidate_sensor_keys=variant.sensor_keys,
                reason="VF2/VF4 selectors are not both available",
                evidence=evidence,
            )
        return _resolved_by_selector(
            variant,
            selected,
            f"VF2/VF4 function selectors resolve the input as {selected}",
            evidence,
        )

    return None


def _resolve_variant(
    model: ControllerModel,
    variant: SensorVariant,
    functions: Functions,
) -> ResolvedSensorVariant:
    """Resolve one model-defined sensor variant from documented selectors."""
    selected_5573_variant = _resolve_5573_variant(model, variant, functions)
    if selected_5573_variant is not None:
        return selected_5573_variant

    pulse_enabled = None
    pulse_evidence: Evidence = ()
    if "pulse_rate" in variant.sensor_keys:
        pulse_enabled = getattr(functions, "pulse_input_enabled", None)
        pulse_evidence = (("pulse_input_enabled", pulse_enabled),)
        if pulse_enabled is True:
            return _resolved_by_selector(
                variant,
                "pulse_rate",
                "FB10 enables flow or power limitation through pulse input",
                pulse_evidence,
            )

    input_number = _input_number_for(model, variant)
    if input_number is None:
        return ResolvedSensorVariant(
            variant_sensor_keys=variant.sensor_keys,
            status=SensorVariantStatus.UNRESOLVED,
            selected_sensor_key=None,
            candidate_sensor_keys=variant.sensor_keys,
            reason="No verified selector is implemented for this variant",
        )

    binary_mode, evidence = _input_mode(functions, input_number)
    evidence = pulse_evidence + evidence
    if binary_mode is True:
        return ResolvedSensorVariant(
            variant_sensor_keys=variant.sensor_keys,
            status=SensorVariantStatus.INACTIVE,
            selected_sensor_key=None,
            candidate_sensor_keys=(),
            reason=f"CO8 input {input_number} is configured as a binary input",
            evidence=evidence,
        )
    if binary_mode is None:
        return ResolvedSensorVariant(
            variant_sensor_keys=variant.sensor_keys,
            status=SensorVariantStatus.UNRESOLVED,
            selected_sensor_key=None,
            candidate_sensor_keys=variant.sensor_keys,
            reason=f"CO8 input {input_number} mode is not available",
            evidence=evidence,
        )
    if len(variant.sensor_keys) == 1:
        sensor_key = variant.sensor_keys[0]
        return ResolvedSensorVariant(
            variant_sensor_keys=variant.sensor_keys,
            status=SensorVariantStatus.RESOLVED,
            selected_sensor_key=sensor_key,
            candidate_sensor_keys=(sensor_key,),
            reason=f"CO8 input {input_number} is configured as a sensor input",
            evidence=evidence,
        )

    candidates = [
        key
        for key in variant.sensor_keys
        if key != "pulse_rate" or pulse_enabled is not False
    ]

    # CO1 -> F25 (CL2125) explicitly selects the buffer-storage bottom
    # sensor SF3. If it is inactive, SF3 is removed from the candidates.
    if "sf3" in candidates:
        sf3_enabled = getattr(functions, "buffer_storage_bottom_sensor_enabled", None)
        evidence += (("buffer_storage_bottom_sensor_enabled", sf3_enabled),)
        if sf3_enabled is True:
            candidates = [key for key in candidates if key in {"sf3", "pulse_rate"}]
        elif sf3_enabled is False:
            candidates.remove("sf3")

    # For the shared FG3/analog input, CL905 distinguishes the analog
    # function from the potentiometer view. It does not distinguish voltage
    # from current, so both analog candidates remain when enabled.
    analog_keys = {"analog_input_voltage", "analog_input_current"}
    if "fg3" in candidates and analog_keys.intersection(candidates):
        analog_enabled = getattr(functions, "analog_setpoint_correction_enabled", None)
        evidence += (("analog_setpoint_correction_enabled", analog_enabled),)
        if analog_enabled is True:
            candidates = [key for key in candidates if key in analog_keys]
        elif analog_enabled is False:
            candidates = [key for key in candidates if key not in analog_keys]

    if len(candidates) == 1:
        selected = candidates[0]
        return ResolvedSensorVariant(
            variant_sensor_keys=variant.sensor_keys,
            status=SensorVariantStatus.RESOLVED,
            selected_sensor_key=selected,
            candidate_sensor_keys=(selected,),
            reason=f"Configuration selectors resolve the input as {selected}",
            evidence=evidence,
        )
    if not candidates:
        return ResolvedSensorVariant(
            variant_sensor_keys=variant.sensor_keys,
            status=SensorVariantStatus.INCONSISTENT,
            selected_sensor_key=None,
            candidate_sensor_keys=(),
            reason="Configuration selectors exclude every documented sensor role",
            evidence=evidence,
        )
    return ResolvedSensorVariant(
        variant_sensor_keys=variant.sensor_keys,
        status=SensorVariantStatus.UNRESOLVED,
        selected_sensor_key=None,
        candidate_sensor_keys=tuple(candidates),
        reason=(
            f"CO8 input {input_number} confirms sensor mode, but the "
            "available selectors leave multiple logical roles"
        ),
        evidence=evidence,
    )


def resolve_sensor_variants(
    model: ModelDefinition,
    functions: Functions,
    parameters: Parameters,
) -> SensorVariantResolution:
    """Resolve documented variants without guessing from values or model quirks.

    ``parameters`` remains part of the stable resolver API. Only explicitly
    documented configuration selectors are evaluated; measurement values are
    never used to guess a logical role.
    """
    del parameters
    results = tuple(
        _resolve_variant(model.model, variant, functions)
        for variant in model.sensor_variants
    )
    return SensorVariantResolution(
        model=model.model,
        sensor_keys=model.sensor_keys,
        fixed_sensor_keys=tuple(
            key for key in model.sensor_keys if key in model.fixed_sensor_keys
        ),
        variants=results,
    )
