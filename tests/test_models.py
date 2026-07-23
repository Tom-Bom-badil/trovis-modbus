"""Tests for static TROVIS controller-model definitions."""

import pytest

from trovis_modbus.enums import ControllerModel
from trovis_modbus.models import (
    MODEL_DEFINITIONS,
    TROVIS_5573,
    TROVIS_5573_1,
    TROVIS_5575,
    TROVIS_5576,
    TROVIS_5578,
    TROVIS_5578_E,
    TROVIS_5579,
    ControllerModel as ModelsControllerModel,
    InputRole,
    get_model_definition,
    model_candidates_for_reported_model,
)
from trovis_modbus.models.definitions import (
    ControllerModel as DefinitionsControllerModel,
)


def test_controller_model_import_paths_share_the_canonical_enum() -> None:
    assert ModelsControllerModel is ControllerModel
    assert DefinitionsControllerModel is ControllerModel


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

        assert definition.input_for_measurement("fg1") is not None
        assert definition.input_for_measurement("fg2") is not None
        assert definition.input_for_measurement("ae1") is None
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
        "analog_input_current": 40042,
    }
    voltage = terminal_3.view_for_key("analog_input_voltage")
    current = terminal_3.view_for_key("analog_input_current")
    assert voltage is not None
    assert current is not None


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
        "analog_input_current": 40042,
    }


def test_5578_keeps_af2_ruef4_and_sf3_fg3_as_logical_alternatives() -> None:
    terminal_2 = TROVIS_5578.input_for_terminal(2)
    assert terminal_2 is not None
    assert {view.measurement_key for view in terminal_2.register_views} == {
        "af2",
        "ruef4",
    }
    af2 = terminal_2.view_for_key("af2")
    ruef4 = terminal_2.view_for_key("ruef4")
    assert af2 is not None
    assert ruef4 is not None

    terminal_17 = TROVIS_5578.input_for_terminal(17)
    assert terminal_17 is not None
    assert {view.measurement_key for view in terminal_17.register_views} == {
        "sf3",
        "fg3",
        "pulse_rate",
    }
    fg3 = terminal_17.view_for_key("fg3")
    assert fg3 is not None
    assert fg3.register == 40028


def test_5578_e_keeps_separate_ae_and_fg_measurements() -> None:
    terminal_2 = TROVIS_5578_E.input_for_terminal(2)
    assert terminal_2 is not None
    assert {view.measurement_key for view in terminal_2.register_views} == {
        "af2",
        "ruef4",
    }

    terminal_15 = TROVIS_5578_E.input_for_terminal(15)
    assert terminal_15 is not None
    assert {view.measurement_key for view in terminal_15.register_views} == {
        "ae1",
        "fg1",
    }

    terminal_16 = TROVIS_5578_E.input_for_terminal(16)
    assert terminal_16 is not None
    assert {view.measurement_key for view in terminal_16.register_views} == {
        "ae2",
        "fg2",
    }

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
        "ae3": 40028,
        "fg3": 40028,
        "pulse_rate": 40029,
    }


def test_5578_has_separate_additional_voltage_input() -> None:
    voltage_input = TROVIS_5578.input_for_terminal(23)
    assert voltage_input is not None
    assert voltage_input.paired_common == 24
    assert voltage_input.possible_roles == (InputRole.ANALOG_VOLTAGE,)
    assert voltage_input.register_views[0].measurement_key == "analog_input_voltage"
    assert voltage_input.register_views[0].register == 40042


def test_5579_terminal_17_contains_distinct_voltage_and_current_views() -> None:
    terminal_17 = TROVIS_5579.input_for_terminal(17)
    assert terminal_17 is not None
    assert terminal_17.paired_common == 18
    assert InputRole.ANALOG_CURRENT in terminal_17.possible_roles

    voltage = terminal_17.view_for_key("analog_input_voltage")
    current = terminal_17.view_for_key("analog_input_current")
    assert voltage is not None
    assert current is not None
    assert voltage.register == current.register == 40042
    assert voltage.roles == (InputRole.ANALOG_VOLTAGE,)
    assert current.roles == (InputRole.ANALOG_CURRENT,)


@pytest.mark.parametrize("definition", MODEL_DEFINITIONS.values())
def test_model_definitions_use_only_canonical_logical_sensor_names(definition) -> None:
    combined_keys = {
        "ae1_fg1",
        "ae2_fg2",
        "ae3_fg3",
        "af2_ruef4",
        "sf2_rf2",
        "sf3_fg3",
        "vf2_3_4",
    }
    assert not (set(definition.measurement_keys) & combined_keys)


@pytest.mark.parametrize("definition", MODEL_DEFINITIONS.values())
def test_all_register_views_match_existing_sensor_descriptor_keys(definition) -> None:
    existing_sensor_keys = {
        "af1",
        "af2",
        "ruef4",
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
        "ae1",
        "fg1",
        "ae2",
        "fg2",
        "ae3",
        "fg3",
        "pulse_rate",
        "analog_input_voltage",
        "analog_input_current",
    }
    assert set(definition.measurement_keys) <= existing_sensor_keys
