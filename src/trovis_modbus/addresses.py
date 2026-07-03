"""Address helpers for TROVIS manufacturer references.

The manufacturer documents use:
- holding-register references like HR40102
- coil references like CL137

The Modbus protocol uses zero-based PDU addresses. The conversion is kept in
this module so component definitions can stay aligned with the maker docs.
"""

REGISTER_REFERENCE_BASE = 40001
REGISTER_REFERENCE_MAX = 49999


def register_address(hr_number: int) -> int:
    """Return the zero-based Modbus address for a TROVIS HR reference.

    Examples:
        HR40001 -> Modbus address 0, HR40002 -> Modbus address 1 ...
    """
    if hr_number < REGISTER_REFERENCE_BASE or hr_number > REGISTER_REFERENCE_MAX:
        raise ValueError(
            f"Expected TROVIS holding-register reference like 40102, got {hr_number}"
        )

    return hr_number - REGISTER_REFERENCE_BASE


def coil_address(cl_number: int) -> int:
    """Return the zero-based Modbus address for a TROVIS CL number.

    Examples:
        CL1 -> Modbus address 0, CL2 -> Modbus address 1 ...
    """
    if cl_number < 1:
        raise ValueError(f"Invalid TROVIS coil number: {cl_number}")

    return cl_number - 1


def hr_range(start_hr: int, end_hr: int) -> tuple[int, int]:
    """Create an inclusive readable register range from HR references."""
    if end_hr < start_hr:
        raise ValueError(f"Invalid TROVIS register range: {start_hr}..{end_hr}")

    return register_address(start_hr), register_address(end_hr)


def cl_range(start_cl: int, end_cl: int) -> tuple[int, int]:
    """Create an inclusive readable coil range from CL references."""
    if end_cl < start_cl:
        raise ValueError(f"Invalid TROVIS coil range: {start_cl}..{end_cl}")

    return coil_address(start_cl), coil_address(end_cl)
