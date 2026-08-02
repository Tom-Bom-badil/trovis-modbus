"""Configuration functions and parameters used by TROVIS interpretation."""

from __future__ import annotations

from ..data_model import TrovisComponent, coil, integer

SENSOR_OR_BINARY_INPUT_NUMBERS = (1, 2, 3, 4, 5, 6, 9, 10, 11, 12, 13, 15, 16, 17)


def _sensor_binary_selector(cl_number: int, input_number: int):
    """Create a read-only CO8 selector for sensor or binary-input mode."""
    return coil(
        cl_number,
        writable=False,
        false_key="sensor_input",
        true_key="binary_input",
        false_label="Sensor input",
        true_label="Binary input",
        maker_key=f"FB{input_number:02d}_BE{input_number:02d}",
        maker_category="CON-FSR",
        description=(
            f"Input {input_number}: false selects sensor input, "
            "true selects binary input"
        ),
    )


def _function_selector(
    cl_number: int,
    *,
    maker_key: str,
    maker_category: str,
    description: str,
):
    """Create a read-only inactive/active function selector."""
    return coil(
        cl_number,
        writable=False,
        false_key="inactive",
        true_key="active",
        false_label="Inactive",
        true_label="Active",
        maker_key=maker_key,
        maker_category=maker_category,
        description=description,
    )


class Functions(TrovisComponent):
    """CO/F states needed to interpret configurable functions.

    The selectors use their common manufacturer CL addresses. The selected
    model ranges decide which declared fields are actually read.
    """

    input_01_is_binary = _sensor_binary_selector(801, 1)
    input_02_is_binary = _sensor_binary_selector(802, 2)
    input_03_is_binary = _sensor_binary_selector(803, 3)
    input_04_is_binary = _sensor_binary_selector(804, 4)
    input_05_is_binary = _sensor_binary_selector(805, 5)
    input_06_is_binary = _sensor_binary_selector(806, 6)
    input_09_is_binary = _sensor_binary_selector(809, 9)
    input_10_is_binary = _sensor_binary_selector(810, 10)
    input_11_is_binary = _sensor_binary_selector(811, 11)
    input_12_is_binary = _sensor_binary_selector(812, 12)
    input_13_is_binary = _sensor_binary_selector(813, 13)
    input_15_is_binary = _sensor_binary_selector(815, 15)
    input_16_is_binary = _sensor_binary_selector(816, 16)
    input_17_is_binary = _sensor_binary_selector(817, 17)

    pulse_input_enabled = _function_selector(
        139,
        maker_key="FB10_Leist_Beg",
        maker_category="CON-SON",
        description="Flow or power limitation through pulse input enabled",
    )

    heating_circuit_1_outdoor_sensor_enabled = _function_selector(
        1026,
        maker_key="FB02_AF1",
        maker_category="CON-AT",
        description="Outdoor sensor for Rk1 enabled",
    )

    heating_circuit_2_outdoor_sensor_enabled = _function_selector(
        1226,
        maker_key="FB02_AF2",
        maker_category="CON-AT",
        description="Outdoor sensor for Rk2 enabled",
    )

    heating_circuit_3_outdoor_sensor_enabled = _function_selector(
        1426,
        maker_key="FB02_AF2_Rk3",
        maker_category="CON-AT",
        description="Outdoor sensor for Rk3 enabled",
    )

    heating_circuit_1_four_point_characteristic_enabled = _function_selector(
        1035,
        maker_key="FB11_4P_HKL_Rk1",
        maker_category="CON-BTR",
        description="Four-point characteristic for Rk1 enabled",
    )

    heating_circuit_2_four_point_characteristic_enabled = _function_selector(
        1235,
        maker_key="FB11_4P_HKL_Rk2",
        maker_category="CON-BTR",
        description="Four-point characteristic for Rk2 enabled",
    )

    heating_circuit_3_four_point_characteristic_enabled = _function_selector(
        1435,
        maker_key="FB11_4P_HKL_Rk3",
        maker_category="CON-BTR",
        description="Four-point characteristic for Rk3 enabled",
    )

    storage_sensor_2_enabled = _function_selector(
        402,
        maker_key="FB02_SF2",
        maker_category="CON-WW",
        description="Storage tank sensor SF2 enabled",
    )

    flow_sensor_4_enabled_cl405 = _function_selector(
        405,
        maker_key="FB05_VF4",
        maker_category="CON-WW",
        description="Flow sensor VF4 enabled",
    )

    flow_sensor_2_enabled = _function_selector(
        907,
        maker_key="FB07_Anl_2x_VF2",
        maker_category="CON-SON",
        description="Flow sensor VF2 enabled",
    )

    flow_sensor_4_enabled_cl1829 = _function_selector(
        1829,
        maker_key="FB05_VF4",
        maker_category="CON-WW",
        description="Flow sensor VF4 enabled",
    )

    analog_setpoint_correction_enabled = _function_selector(
        905,
        maker_key="FB05_Sollw_Korr",
        maker_category="CON-SON",
        description="Setpoint correction through the general 0 to 10 V input",
    )

    buffer_tank_bottom_sensor_enabled = _function_selector(
        2125,
        maker_key="FB25_PS_Bodensen",
        maker_category="CON-SON",
        description="Buffer tank bottom sensor SF3 enabled",
    )

    def heating_circuit_uses_outdoor_sensor(self, index: int) -> bool | None:
        """Return whether Rk1 through Rk3 uses an outdoor sensor."""
        if not 1 <= index <= 3:
            raise ValueError("heating circuit index must be in range 1..3")

        field = f"heating_circuit_{index}_outdoor_sensor_enabled"
        if not self.is_field_readable(field):
            return None
        return getattr(self, field)

    def heating_circuit_uses_four_point_characteristic(
        self,
        index: int,
    ) -> bool | None:
        """Return whether Rk1 through Rk3 uses the four-point characteristic."""
        if not 1 <= index <= 3:
            raise ValueError("heating circuit index must be in range 1..3")

        field = f"heating_circuit_{index}_four_point_characteristic_enabled"
        if not self.is_field_readable(field):
            return None
        return getattr(self, field)

    def input_is_binary(self, input_number: int) -> bool | None:
        """Return the configured mode of one known CO8 input selector."""
        if input_number not in SENSOR_OR_BINARY_INPUT_NUMBERS:
            raise KeyError(f"no sensor/binary selector known for input {input_number}")
        return getattr(self, f"input_{input_number:02d}_is_binary")

    @property
    def readable_input_numbers(self) -> tuple[int, ...]:
        """Return CO8 input selectors present in the current model range."""
        return tuple(
            input_number
            for input_number in SENSOR_OR_BINARY_INPUT_NUMBERS
            if self.is_field_readable(f"input_{input_number:02d}_is_binary")
        )

    @property
    def flow_sensor_4_enabled(self) -> bool | None:
        """Return the logical VF4 selector from its documented CL views."""
        field_names = (
            "flow_sensor_4_enabled_cl405",
            "flow_sensor_4_enabled_cl1829",
        )
        values = tuple(
            getattr(self, field_name)
            for field_name in field_names
            if self.is_field_readable(field_name)
        )
        known_values = tuple(value for value in values if value is not None)
        if not known_values:
            return None
        return any(known_values)


def _validated_integer(
    value: int | None,
    minimum: int,
    maximum: int,
) -> int | None:
    """Return a documented integer value or ``None`` for invalid raw data."""
    if value is None or not minimum <= value <= maximum:
        return None
    return value


class Parameters(TrovisComponent):
    """PA and selection values needed by the sensor-variant resolver."""

    analog_input_selection = integer(
        42002,
        signed=False,
        min_value=1,
        max_value=7,
        digits=0,
        maker_key="AE_Auswahl",
        maker_category="ALG-BTR",
        description="Analog-input selection bit mask: AE1=1, AE2=2 and AE3=4",
    )

    storage_tank_charging_pump_sensor_input = integer(
        42003,
        signed=False,
        min_value=1,
        max_value=17,
        digits=0,
        maker_key="SLP_Sensor",
        maker_category="ALG-BTR",
        description="Input number assigned to the storage tank charging pump sensor",
    )

    @property
    def validated_analog_input_selection(self) -> int | None:
        """Return HR42002 only when it is inside its documented value range."""
        return _validated_integer(self.analog_input_selection, 1, 7)

    @property
    def validated_storage_tank_charging_pump_sensor_input(self) -> int | None:
        """Return HR42003 only when it is inside its documented value range."""
        return _validated_integer(
            self.storage_tank_charging_pump_sensor_input,
            1,
            17,
        )

    @property
    def selected_analog_inputs(self) -> tuple[int, ...]:
        """Return the AE input numbers selected by a valid HR42002 value."""
        selection = self.validated_analog_input_selection
        if selection is None:
            return ()
        return tuple(
            input_number
            for input_number, mask in ((1, 1), (2, 2), (3, 4))
            if selection & mask
        )
