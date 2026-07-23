"""Static physical-input definition for the TROVIS 5578-E."""

from .definitions import (
    ControllerModel,
    InputRole,
    ModelDefinition,
    physical_input,
    register_view,
)

_RESISTANCE_OR_BINARY = (
    InputRole.RESISTANCE_SENSOR,
    InputRole.BINARY_INPUT,
)
_ANALOG_POTENTIOMETER_OR_BINARY = (
    InputRole.ANALOG_VOLTAGE,
    InputRole.POTENTIOMETER,
    InputRole.BINARY_INPUT,
)

# EB 5578-E, firmware 3.10.xx, figure 3. TROVIS I/O expansion modules and
# their additional heating circuits Hk11 to Hk13 are intentionally excluded.
TROVIS_5578_E = ModelDefinition(
    model=ControllerModel.TROVIS_5578_E,
    heating_circuits=3,
    inputs=(
        physical_input(
            1,
            "AF1",
            possible_roles=_RESISTANCE_OR_BINARY,
            register_views=(register_view("af1", 40010, InputRole.RESISTANCE_SENSOR),),
            paired_common=18,
        ),
        physical_input(
            2,
            "AF2",
            "RüF4",
            possible_roles=_RESISTANCE_OR_BINARY,
            register_views=(register_view("af2", 40011, InputRole.RESISTANCE_SENSOR),),
            paired_common=18,
        ),
        physical_input(
            3,
            "SF1",
            possible_roles=_RESISTANCE_OR_BINARY,
            register_views=(register_view("sf1", 40023, InputRole.RESISTANCE_SENSOR),),
            paired_common=18,
        ),
        physical_input(
            4,
            "SF2",
            possible_roles=_RESISTANCE_OR_BINARY,
            register_views=(register_view("sf2", 40024, InputRole.RESISTANCE_SENSOR),),
            paired_common=18,
        ),
        physical_input(
            5,
            "RF1",
            possible_roles=_RESISTANCE_OR_BINARY,
            register_views=(register_view("rf1", 40020, InputRole.RESISTANCE_SENSOR),),
            paired_common=18,
        ),
        physical_input(
            6,
            "RF2",
            possible_roles=_RESISTANCE_OR_BINARY,
            register_views=(register_view("rf2", 40021, InputRole.RESISTANCE_SENSOR),),
            paired_common=18,
        ),
        physical_input(
            7,
            "RF3",
            possible_roles=_RESISTANCE_OR_BINARY,
            register_views=(register_view("rf3", 40022, InputRole.RESISTANCE_SENSOR),),
            paired_common=18,
        ),
        physical_input(
            8,
            "VF1",
            possible_roles=_RESISTANCE_OR_BINARY,
            register_views=(register_view("vf1", 40013, InputRole.RESISTANCE_SENSOR),),
            paired_common=18,
        ),
        physical_input(
            9,
            "VF2",
            possible_roles=_RESISTANCE_OR_BINARY,
            register_views=(register_view("vf2", 40014, InputRole.RESISTANCE_SENSOR),),
            paired_common=18,
        ),
        physical_input(
            10,
            "VF3",
            possible_roles=_RESISTANCE_OR_BINARY,
            register_views=(register_view("vf3", 40015, InputRole.RESISTANCE_SENSOR),),
            paired_common=18,
        ),
        physical_input(
            11,
            "VF4",
            possible_roles=_RESISTANCE_OR_BINARY,
            register_views=(register_view("vf4", 40016, InputRole.RESISTANCE_SENSOR),),
            paired_common=18,
        ),
        physical_input(
            12,
            "RüF1",
            possible_roles=_RESISTANCE_OR_BINARY,
            register_views=(
                register_view("ruef1", 40017, InputRole.RESISTANCE_SENSOR),
            ),
            paired_common=18,
        ),
        physical_input(
            13,
            "RüF2",
            possible_roles=_RESISTANCE_OR_BINARY,
            register_views=(
                register_view("ruef2", 40018, InputRole.RESISTANCE_SENSOR),
            ),
            paired_common=18,
        ),
        physical_input(
            14,
            "RüF3",
            possible_roles=_RESISTANCE_OR_BINARY,
            register_views=(
                register_view("ruef3", 40019, InputRole.RESISTANCE_SENSOR),
            ),
            paired_common=18,
        ),
        physical_input(
            15,
            "AE1",
            "FG1",
            possible_roles=_ANALOG_POTENTIOMETER_OR_BINARY,
            register_views=(
                register_view(
                    "ae1_fg1",
                    40026,
                    InputRole.ANALOG_VOLTAGE,
                    InputRole.POTENTIOMETER,
                ),
            ),
            paired_common=18,
        ),
        physical_input(
            16,
            "AE2",
            "FG2",
            possible_roles=_ANALOG_POTENTIOMETER_OR_BINARY,
            register_views=(
                register_view(
                    "ae2_fg2",
                    40027,
                    InputRole.ANALOG_VOLTAGE,
                    InputRole.POTENTIOMETER,
                ),
            ),
            paired_common=18,
        ),
        physical_input(
            17,
            "AE3",
            "FG3",
            "SF3",
            possible_roles=(
                InputRole.ANALOG_VOLTAGE,
                InputRole.POTENTIOMETER,
                InputRole.RESISTANCE_SENSOR,
                InputRole.PULSE_INPUT,
                InputRole.BINARY_INPUT,
            ),
            register_views=(
                register_view("sf3", 40025, InputRole.RESISTANCE_SENSOR),
                register_view(
                    "ae3_fg3",
                    40028,
                    InputRole.ANALOG_VOLTAGE,
                    InputRole.POTENTIOMETER,
                ),
                register_view("pulse_rate", 40029, InputRole.PULSE_INPUT),
            ),
            paired_common=18,
        ),
    ),
)
