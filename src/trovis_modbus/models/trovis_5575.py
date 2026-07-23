"""Static physical-input definition for the TROVIS 5575."""

from ..enums import ControllerModel
from .definitions import (
    InputRole,
    ModelDefinition,
    physical_input,
    register_view,
)

_BINARY_OR_POTENTIOMETER = (
    InputRole.BINARY_INPUT,
    InputRole.POTENTIOMETER,
)

# EB 5575, firmware 2.48, figures 5-2 to 5-4. Terminal 3 is the documented
# multi-purpose SF2/RF2 and WMZ/demand input. A 20-mA signal uses the documented
# 50-ohm resistor between terminals 3 and 13. The detailed electrical role is
# resolved later from functions and parameters.
TROVIS_5575 = ModelDefinition(
    model=ControllerModel.TROVIS_5575,
    heating_circuits=2,
    inputs=(
        physical_input(
            1,
            "AF1",
            possible_roles=(InputRole.RESISTANCE_SENSOR,),
            register_views=(register_view("af1", 40010, InputRole.RESISTANCE_SENSOR),),
            paired_common=12,
        ),
        physical_input(
            2,
            "SF1",
            possible_roles=(InputRole.RESISTANCE_SENSOR,),
            register_views=(register_view("sf1", 40023, InputRole.RESISTANCE_SENSOR),),
            paired_common=12,
        ),
        physical_input(
            3,
            "SF2",
            "RF2",
            "WMZ/Bed (analog return terminal 13)",
            possible_roles=(
                InputRole.RESISTANCE_SENSOR,
                InputRole.ANALOG_VOLTAGE,
                InputRole.ANALOG_CURRENT,
                InputRole.PULSE_INPUT,
            ),
            register_views=(
                register_view("sf2", 40024, InputRole.RESISTANCE_SENSOR),
                register_view("rf2", 40021, InputRole.RESISTANCE_SENSOR),
                register_view("pulse_rate", 40029, InputRole.PULSE_INPUT),
                register_view(
                    "analog_input_voltage",
                    40042,
                    InputRole.ANALOG_VOLTAGE,
                    InputRole.ANALOG_CURRENT,
                ),
            ),
            paired_common=12,
        ),
        physical_input(
            4,
            "RüF2",
            possible_roles=(InputRole.RESISTANCE_SENSOR,),
            register_views=(
                register_view("ruef2", 40018, InputRole.RESISTANCE_SENSOR),
            ),
            paired_common=12,
        ),
        physical_input(
            5,
            "RF1",
            possible_roles=(InputRole.RESISTANCE_SENSOR,),
            register_views=(register_view("rf1", 40020, InputRole.RESISTANCE_SENSOR),),
            paired_common=12,
        ),
        physical_input(
            6,
            "RüF1",
            possible_roles=(InputRole.RESISTANCE_SENSOR,),
            register_views=(
                register_view("ruef1", 40017, InputRole.RESISTANCE_SENSOR),
            ),
            paired_common=12,
        ),
        physical_input(
            7,
            "VF1",
            possible_roles=(InputRole.RESISTANCE_SENSOR,),
            register_views=(register_view("vf1", 40013, InputRole.RESISTANCE_SENSOR),),
            paired_common=12,
        ),
        physical_input(
            8,
            "VF2",
            "VF3",
            "VF4",
            possible_roles=(InputRole.RESISTANCE_SENSOR,),
            register_views=(
                register_view("vf2", 40014, InputRole.RESISTANCE_SENSOR),
                register_view("vf3", 40015, InputRole.RESISTANCE_SENSOR),
                register_view("vf4", 40016, InputRole.RESISTANCE_SENSOR),
            ),
            paired_common=12,
        ),
        physical_input(
            9,
            "BE1",
            "FG1",
            possible_roles=_BINARY_OR_POTENTIOMETER,
            register_views=(register_view("ae1_fg1", 40026, InputRole.POTENTIOMETER),),
            paired_common=12,
        ),
        physical_input(
            10,
            "BE2",
            "FG2",
            possible_roles=_BINARY_OR_POTENTIOMETER,
            register_views=(register_view("ae2_fg2", 40027, InputRole.POTENTIOMETER),),
            paired_common=12,
        ),
    ),
)
