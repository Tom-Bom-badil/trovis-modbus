"""Static physical-input definition for the TROVIS 5579."""

from ..enums import ControllerModel
from .definitions import (
    InputRole,
    ModelDefinition,
    physical_input,
    register_view,
)

_RESISTANCE_OR_BINARY = (
    InputRole.RESISTANCE_SENSOR,
    InputRole.BINARY_INPUT,
)

# EB 5579, firmware 2.48, figure 5-2. The connection diagram labels BE1 to
# BE17, while T 5500 lists 14 inputs as alternatively binary. The model keeps
# every electrically documented possibility; the later CO8 resolver decides
# which roles are actually selectable and configured.
TROVIS_5579 = ModelDefinition(
    model=ControllerModel.TROVIS_5579,
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
            "FG1",
            possible_roles=(InputRole.POTENTIOMETER, InputRole.BINARY_INPUT),
            register_views=(
                register_view(
                    "fg1",
                    40026,
                    InputRole.POTENTIOMETER,
                ),
            ),
            paired_common=18,
        ),
        physical_input(
            16,
            "FG2",
            possible_roles=(InputRole.POTENTIOMETER, InputRole.BINARY_INPUT),
            register_views=(
                register_view(
                    "fg2",
                    40027,
                    InputRole.POTENTIOMETER,
                ),
            ),
            paired_common=18,
        ),
        physical_input(
            17,
            "SF3",
            "FG3",
            "WMZ/Bed (return terminal 19)",
            possible_roles=(
                InputRole.RESISTANCE_SENSOR,
                InputRole.POTENTIOMETER,
                InputRole.PULSE_INPUT,
                InputRole.ANALOG_VOLTAGE,
                InputRole.ANALOG_CURRENT,
                InputRole.BINARY_INPUT,
            ),
            register_views=(
                register_view("sf3", 40025, InputRole.RESISTANCE_SENSOR),
                register_view(
                    "fg3",
                    40028,
                    InputRole.POTENTIOMETER,
                ),
                register_view("pulse_rate", 40029, InputRole.PULSE_INPUT),
                register_view(
                    "analog_input_voltage",
                    40042,
                    InputRole.ANALOG_VOLTAGE,
                ),
                register_view(
                    "analog_input_current",
                    40042,
                    InputRole.ANALOG_CURRENT,
                ),
            ),
            paired_common=18,
        ),
    ),
)
