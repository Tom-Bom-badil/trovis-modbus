"""Static physical-input definition for the TROVIS 5573."""

from .definitions import (
    ControllerModel,
    InputRole,
    ModelDefinition,
    physical_input,
    register_view,
)

_BINARY_OR_POTENTIOMETER = (
    InputRole.BINARY_INPUT,
    InputRole.POTENTIOMETER,
)

# EB 5573, firmware 3.09.xx, figures 4 and 5. The first eight terminals are
# resistance-sensor inputs. Some terminals have several firmware labels whose
# meaning depends on the selected hydronic configuration. Terminals 9 and 10
# are the two additional BE/FG inputs. Terminal 11 is the shared 0-to-10-V
# input/output channel; input and output operation are mutually exclusive.
TROVIS_5573 = ModelDefinition(
    model=ControllerModel.TROVIS_5573,
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
            possible_roles=(InputRole.RESISTANCE_SENSOR,),
            register_views=(
                register_view("sf2", 40024, InputRole.RESISTANCE_SENSOR),
                register_view("rf2", 40021, InputRole.RESISTANCE_SENSOR),
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
        physical_input(
            11,
            "0...10 V in/out",
            possible_roles=(InputRole.ANALOG_VOLTAGE,),
            register_views=(
                register_view(
                    "analog_input_voltage",
                    40042,
                    InputRole.ANALOG_VOLTAGE,
                ),
            ),
            paired_common=12,
        ),
    ),
)
