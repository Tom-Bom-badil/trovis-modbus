"""Helpers for per-device Modbus read exclusions."""

from __future__ import annotations

from collections.abc import Iterable

MODBUS_ADDRESS_MIN = 0
MODBUS_ADDRESS_MAX = 0xFFFF

AddressRange = tuple[int, int]
AddressRanges = tuple[AddressRange, ...]


def normalize_excluded_addresses(addresses: Iterable[int]) -> frozenset[int]:
    """Return validated zero-based Modbus addresses."""
    normalized: set[int] = set()

    for address in addresses:
        if isinstance(address, bool) or not isinstance(address, int):
            raise ValueError("excluded Modbus addresses must be integers")
        if not MODBUS_ADDRESS_MIN <= address <= MODBUS_ADDRESS_MAX:
            raise ValueError(
                "excluded Modbus addresses must be in range "
                f"{MODBUS_ADDRESS_MIN}..{MODBUS_ADDRESS_MAX}"
            )
        normalized.add(address)

    return frozenset(normalized)


def ranges_excluding_addresses(
    ranges: AddressRanges,
    excluded_addresses: frozenset[int],
) -> AddressRanges:
    """Split inclusive readable ranges around excluded zero-based addresses."""
    if not excluded_addresses:
        return ranges

    excluded = sorted(excluded_addresses)
    result: list[AddressRange] = []

    for low, high in ranges:
        start = low

        for address in excluded:
            if address < start:
                continue
            if address > high:
                break

            if start < address:
                result.append((start, address - 1))
            start = address + 1

        if start <= high:
            result.append((start, high))

    return tuple(result)
