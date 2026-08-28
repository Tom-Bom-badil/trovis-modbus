"""Tests for COx-F12 control parameters and their hydronic capabilities."""

from __future__ import annotations

import pytest

from trovis_modbus import Trovis557x
from trovis_modbus.configurations import ControllerModel, get_configuration_definition


@pytest.mark.parametrize(
    ("model", "system_code", "index", "expected"),
    (
        (ControllerModel.TROVIS_5578, 61, 1, True),
        (ControllerModel.TROVIS_5578, 61, 2, True),
        (ControllerModel.TROVIS_5578, 61, 3, True),
        (ControllerModel.TROVIS_5578, 61, 4, False),
        (ControllerModel.TROVIS_5579, 51, 1, True),
        (ControllerModel.TROVIS_5579, 51, 2, True),
        (ControllerModel.TROVIS_5579, 51, 3, True),
        (ControllerModel.TROVIS_5579, 51, 4, False),
        # Project decision: include 5578-E systems 3.7 and 3.8 despite the
        # conflicting availability table/text in the current manual.
        (ControllerModel.TROVIS_5578_E, 37, 4, True),
        (ControllerModel.TROVIS_5578_E, 38, 4, True),
        (ControllerModel.TROVIS_5576, 71, 4, True),
        (ControllerModel.TROVIS_5576, 21, 4, False),
    ),
)
def test_control_parameter_capability(
    model: ControllerModel,
    system_code: int,
    index: int,
    expected: bool,
) -> None:
    """Gate COx-F12 control parameters by model, hydronics and technical Rk."""
    definition = get_configuration_definition(system_code)

    assert definition.supports_control_parameters(model, index) is expected


@pytest.mark.parametrize(
    ("model", "system_code", "index", "expected"),
    (
        (ControllerModel.TROVIS_5578, 61, 1, True),
        (ControllerModel.TROVIS_5578, 61, 2, True),
        (ControllerModel.TROVIS_5578, 61, 3, True),
        (ControllerModel.TROVIS_5579, 51, 1, True),
        (ControllerModel.TROVIS_5579, 51, 2, False),
        (ControllerModel.TROVIS_5579, 51, 3, False),
        (ControllerModel.TROVIS_5579, 210, 3, True),
        (ControllerModel.TROVIS_5575, 100, 2, True),
        (ControllerModel.TROVIS_5575, 101, 2, False),
        (ControllerModel.TROVIS_5578_E, 37, 4, True),
        (ControllerModel.TROVIS_5578_E, 38, 4, False),
        (ControllerModel.TROVIS_5579, 110, 4, True),
        (ControllerModel.TROVIS_5579, 112, 4, False),
    ),
)
def test_two_point_control_parameter_capability(
    model: ControllerModel,
    system_code: int,
    index: int,
    expected: bool,
) -> None:
    """Keep the F12=0 parameter set restricted to documented combinations."""
    definition = get_configuration_definition(system_code)

    assert definition.supports_two_point_control_parameters(model, index) is expected


def test_f12_control_parameter_addresses_and_metadata() -> None:
    """Keep the F12 parameter family aligned with manufacturer references."""
    device = Trovis557x(unit=None)  # type: ignore[arg-type]

    for circuit, base_register, f12_coil in (
        (device.rk1, 1064, 1035),
        (device.rk2, 1264, 1235),
        (device.rk3, 1464, 1435),
    ):
        expected_registers = {
            "control_parameter_kp": base_register,
            "control_parameter_tn": base_register + 1,
            "control_parameter_ty": base_register + 2,
            "control_parameter_tv": base_register + 3,
            "control_parameter_hysteresis": base_register + 4,
            "control_parameter_minimum_on_time": base_register + 5,
            "control_parameter_minimum_off_time": base_register + 6,
        }
        for field, address in expected_registers.items():
            descriptor = circuit.declared_fields[field]
            assert circuit._address(descriptor) == address
            assert descriptor.writable
            assert circuit.require_metadata_for(field).writable is True

        f12 = circuit.declared_fields["three_point_control_enabled"]
        assert circuit._address(f12) == f12_coil
        assert f12.writable

    rk4 = device.rk4
    for offset, field in enumerate(
        (
            "control_parameter_kp",
            "control_parameter_tn",
            "control_parameter_ty",
            "control_parameter_tv",
            "control_parameter_hysteresis",
            "control_parameter_minimum_on_time",
            "control_parameter_minimum_off_time",
        )
    ):
        descriptor = rk4.declared_fields[field]
        assert rk4._address(descriptor) == 1864 + offset
        assert descriptor.writable
        assert rk4.require_metadata_for(field).writable is True

    rk4_f12 = rk4.declared_fields["three_point_control_enabled"]
    assert rk4._address(rk4_f12) == 411
    assert rk4_f12.writable

    kp = device.rk1.require_metadata_for("control_parameter_kp")
    assert kp.number is not None
    assert kp.number.min_value == pytest.approx(0.1)
    assert kp.number.max_value == pytest.approx(50.0)

    ty = device.rk1.require_metadata_for("control_parameter_ty")
    assert ty.number is not None
    assert ty.number.min_value == 15
    assert ty.number.max_value == 240

    hysteresis = device.rk1.require_metadata_for("control_parameter_hysteresis")
    assert hysteresis.number is not None
    assert hysteresis.number.min_value == pytest.approx(1.0)
    assert hysteresis.number.max_value == pytest.approx(30.0)
    # Project-wide HA convention: writable temperature differences use a
    # conservative 1 K UI step even when the raw register resolves 0.1 K.
    assert hysteresis.number.step == 1
