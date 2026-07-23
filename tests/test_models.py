"""Tests for static TROVIS controller-model definitions."""

import pytest

from trovis_modbus.models import (
    MODEL_DEFINITIONS,
    TROVIS_5573,
    TROVIS_5573_1,
    TROVIS_5575,
    TROVIS_5576,
    TROVIS_5578,
    TROVIS_5578_E,
    TROVIS_5579,
    ControllerModel,
    InputRole,
    get_model_definition,
    model_candidates_for_reported_model,
)


@pytest.mark.parametrize(
    ("definition", "expected_heating_circuits", "expected_input_count"),
    (
        (TROVIS_5573, 2, 11),
        (TROVIS_5573_1, 2, 11),
        (TROVIS_5575, 2, 10),
        (TROVIS_5576, 2, 17),
        (TROVIS_5578, 3, 18),
        (TROVIS_5578_E, 3, 17),
        (TROVIS_5579, 3, 17),
    ),
)
def test_model_definitions_have_unique_inputs(
    definition, expected_heating_circuits, expected_input_count
) -> None:
    assert definition.heating_circuits == expected_heating_circuits
    assert len(definition.inputs) == expected_input_count
    assert len({item.terminal for item in definition.inputs}) == expected_input_count
    assert (
        len({item.conflict_group for item in definition.inputs}) == expected_input_count
    )


def test_registry_contains_all_supported_model_designations() -> None:
    assert set(MODEL_DEFINITIONS) == set(ControllerModel)
    assert get_model_definition("5573-1") is TROVIS_5573_1
    assert get_model_definition("5578-E") is TROVIS_5578_E


@pytest.mark.parametrize(
    ("reported_model", "expected_definition"),
    (
        (5573, TROVIS_5573),
        (55731, TROVIS_5573_1),
        (5575, TROVIS_5575),
        (5576, TROVIS_5576),
        (5578, TROVIS_5578),
        (55781, TROVIS_5578_E),
        (5579, TROVIS_5579),
    ),
)
def test_reported_model_values_resolve_exactly(
    reported_model, expected_definition
) -> None:
    assert model_candidates_for_reported_model(reported_model) == (expected_definition,)


def test_unknown_reported_model_has_no_candidates() -> None:
    assert model_candidates_for_reported_model(9999) == ()


def test_5573_family_uses_documented_reduced_sensor_matrix() -> None:
    for definition in (TROVIS_5573, TROVIS_5573_1):
        terminal_3 = definition.input_for_terminal(3)
        assert terminal_3 is not None
        assert terminal_3.paired_common == 12
        assert {view.measurement_key for view in terminal_3.register_views} == {
            "sf2",
            "rf2",
        }

        terminal_8 = definition.input_for_terminal(8)
        assert terminal_8 is not None
        assert {view.measurement_key for view in terminal_8.register_views} == {
            "vf2",
            "vf3",
            "vf4",
        }

        assert definition.input_for_measurement("af2") is None
        assert definition.input_for_measurement("sf3") is None


def test_5575_terminal_3_is_one_multi_purpose_input() -> None:
    terminal_3 = TROVIS_5575.input_for_terminal(3)
    assert terminal_3 is not None
    assert terminal_3.paired_common == 12
    assert set(terminal_3.possible_roles) == {
        InputRole.RESISTANCE_SENSOR,
        InputRole.ANALOG_VOLTAGE,
        InputRole.ANALOG_CURRENT,
        InputRole.PULSE_INPUT,
    }
    assert {
        view.measurement_key: view.register for view in terminal_3.register_views
    } == {
        "sf2": 40024,
        "rf2": 40021,
        "pulse_rate": 40029,
        "analog_input_voltage": 40042,
    }


def test_5576_keeps_binary_only_terminals_and_terminal_17_conflict() -> None:
    for terminal in (7, 14):
        binary_input = TROVIS_5576.input_for_terminal(terminal)
        assert binary_input is not None
        assert binary_input.possible_roles == (InputRole.BINARY_INPUT,)
        assert binary_input.register_views == ()

    terminal_17 = TROVIS_5576.input_for_terminal(17)
    assert terminal_17 is not None
    assert terminal_17.paired_common == 18
    assert set(terminal_17.possible_roles) == {
        InputRole.RESISTANCE_SENSOR,
        InputRole.BINARY_INPUT,
        InputRole.PULSE_INPUT,
        InputRole.ANALOG_VOLTAGE,
        InputRole.ANALOG_CURRENT,
    }
    assert {
        view.measurement_key: view.register for view in terminal_17.register_views
    } == {
        "sf3": 40025,
        "pulse_rate": 40029,
        "analog_input_voltage": 40042,
    }


def test_5578_e_terminal_17_keeps_one_physical_conflict_group() -> None:
    terminal_17 = TROVIS_5578_E.input_for_terminal(17)
    assert terminal_17 is not None
    assert terminal_17.paired_common == 18
    assert set(terminal_17.possible_roles) == {
        InputRole.ANALOG_VOLTAGE,
        InputRole.POTENTIOMETER,
        InputRole.RESISTANCE_SENSOR,
        InputRole.PULSE_INPUT,
        InputRole.BINARY_INPUT,
    }
    assert {
        view.measurement_key: view.register for view in terminal_17.register_views
    } == {
        "sf3": 40025,
        "ae3_fg3": 40028,
        "pulse_rate": 40029,
    }


def test_5578_has_separate_additional_voltage_input() -> None:
    voltage_input = TROVIS_5578.input_for_terminal(23)
    assert voltage_input is not None
    assert voltage_input.paired_common == 24
    assert voltage_input.possible_roles == (InputRole.ANALOG_VOLTAGE,)
    assert voltage_input.register_views[0].measurement_key == "analog_input_voltage"
    assert voltage_input.register_views[0].register == 40042


def test_5579_terminal_17_contains_voltage_and_current_roles() -> None:
    terminal_17 = TROVIS_5579.input_for_terminal(17)
    assert terminal_17 is not None
    assert terminal_17.paired_common == 18
    assert InputRole.ANALOG_CURRENT in terminal_17.possible_roles

    analog_view = terminal_17.view_for_key("analog_input_voltage")
    assert analog_view is not None
    assert analog_view.register == 40042
    assert analog_view.roles == (InputRole.ANALOG_VOLTAGE,)


@pytest.mark.parametrize("definition", MODEL_DEFINITIONS.values())
def test_all_register_views_match_existing_sensor_descriptor_keys(definition) -> None:
    # This list mirrors subsystems/sensors.py without importing the component
    # framework. It protects the static model block from inventing new runtime
    # sensor descriptors before the later resolver/profile work.
    existing_sensor_keys = {
        "af1",
        "af2",
        "vf1",
        "vf2",
        "vf3",
        "vf4",
        "ruef1",
        "ruef2",
        "ruef3",
        "rf1",
        "rf2",
        "rf3",
        "sf1",
        "sf2",
        "sf3",
        "ae1_fg1",
        "ae2_fg2",
        "ae3_fg3",
        "pulse_rate",
        "analog_input_voltage",
    }
    assert {
        view.measurement_key
        for input_definition in definition.inputs
        for view in input_definition.register_views
    } <= existing_sensor_keys
