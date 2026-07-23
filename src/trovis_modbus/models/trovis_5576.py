"""Static physical-input definition for the TROVIS 5576."""

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
_POTENTIOMETER_OR_BINARY = (
    InputRole.POTENTIOMETER,
    InputRole.BINARY_INPUT,
)

# EB 5576, firmware 2.28, figure 16. The connection diagram exposes terminals
# 1 to 17 as BE1 to BE17 and documents 15 sensor/FG assignments; terminals 7
# and 14 have no separate analog sensor label and are therefore retained as
# binary-only inputs. Terminal 17 is the documented SF3 and WMZ/demand channel.
# The wider model-specific current-input rules remain intentionally deferred to
# the later sensor-role inventory and resolver block.
TROVIS_5576 = ModelDefinition(
    model=ControllerModel.TROVIS_5576,
    heating_circuits=2,
    inputs=(
        physical_input(
            1,
            "AF1",
            "BE1",
            possible_roles=_RESISTANCE_OR_BINARY,
            register_views=(register_view("af1", 40010, InputRole.RESISTANCE_SENSOR),),
            paired_common=18,
        ),
        physical_input(
            2,
            "AF2",
            "BE2",
            possible_roles=_RESISTANCE_OR_BINARY,
            register_views=(register_view("af2", 40011, InputRole.RESISTANCE_SENSOR),),
            paired_common=18,
        ),
        physical_input(
            3,
            "SF1",
            "BE3",
            possible_roles=_RESISTANCE_OR_BINARY,
            register_views=(register_view("sf1", 40023, InputRole.RESISTANCE_SENSOR),),
            paired_common=18,
        ),
        physical_input(
            4,
            "SF2",
            "BE4",
            possible_roles=_RESISTANCE_OR_BINARY,
            register_views=(register_view("sf2", 40024, InputRole.RESISTANCE_SENSOR),),
            paired_common=18,
        ),
        physical_input(
            5,
            "RF1",
            "BE5",
            possible_roles=_RESISTANCE_OR_BINARY,
            register_views=(register_view("rf1", 40020, InputRole.RESISTANCE_SENSOR),),
            paired_common=18,
        ),
        physical_input(
            6,
            "RF2",
            "BE6",
            possible_roles=_RESISTANCE_OR_BINARY,
            register_views=(register_view("rf2", 40021, InputRole.RESISTANCE_SENSOR),),
            paired_common=18,
        ),
        physical_input(
            7,
            "BE7",
            possible_roles=(InputRole.BINARY_INPUT,),
            register_views=(),
            paired_common=18,
        ),
        physical_input(
            8,
            "VF1",
            "BE8",
            possible_roles=_RESISTANCE_OR_BINARY,
            register_views=(register_view("vf1", 40013, InputRole.RESISTANCE_SENSOR),),
            paired_common=18,
        ),
        physical_input(
            9,
            "VF2",
            "BE9",
            possible_roles=_RESISTANCE_OR_BINARY,
            register_views=(register_view("vf2", 40014, InputRole.RESISTANCE_SENSOR),),
            paired_common=18,
        ),
        physical_input(
            10,
            "VF3",
            "BE10",
            possible_roles=_RESISTANCE_OR_BINARY,
            register_views=(register_view("vf3", 40015, InputRole.RESISTANCE_SENSOR),),
            paired_common=18,
        ),
        physical_input(
            11,
            "VF4",
            "BE11",
            possible_roles=_RESISTANCE_OR_BINARY,
            register_views=(register_view("vf4", 40016, InputRole.RESISTANCE_SENSOR),),
            paired_common=18,
        ),
        physical_input(
            12,
            "RüF1",
            "BE12",
            possible_roles=_RESISTANCE_OR_BINARY,
            register_views=(
                register_view("ruef1", 40017, InputRole.RESISTANCE_SENSOR),
            ),
            paired_common=18,
        ),
        physical_input(
            13,
            "RüF2",
            "BE13",
            possible_roles=_RESISTANCE_OR_BINARY,
            register_views=(
                register_view("ruef2", 40018, InputRole.RESISTANCE_SENSOR),
            ),
            paired_common=18,
        ),
        physical_input(
            14,
            "BE14",
            possible_roles=(InputRole.BINARY_INPUT,),
            register_views=(),
            paired_common=18,
        ),
        physical_input(
            15,
            "FG1",
            "BE15",
            possible_roles=_POTENTIOMETER_OR_BINARY,
            register_views=(register_view("ae1_fg1", 40026, InputRole.POTENTIOMETER),),
            paired_common=18,
        ),
        physical_input(
            16,
            "FG2",
            "BE16",
            possible_roles=_POTENTIOMETER_OR_BINARY,
            register_views=(register_view("ae2_fg2", 40027, InputRole.POTENTIOMETER),),
            paired_common=18,
        ),
        physical_input(
            17,
            "SF3",
            "BE17",
            "WMZ/Bed (analog return terminal 19)",
            possible_roles=(
                InputRole.RESISTANCE_SENSOR,
                InputRole.BINARY_INPUT,
                InputRole.PULSE_INPUT,
                InputRole.ANALOG_VOLTAGE,
                InputRole.ANALOG_CURRENT,
            ),
            register_views=(
                register_view("sf3", 40025, InputRole.RESISTANCE_SENSOR),
                register_view("pulse_rate", 40029, InputRole.PULSE_INPUT),
                register_view(
                    "analog_input_voltage",
                    40042,
                    InputRole.ANALOG_VOLTAGE,
                    InputRole.ANALOG_CURRENT,
                ),
            ),
            paired_common=18,
        ),
    ),
)
