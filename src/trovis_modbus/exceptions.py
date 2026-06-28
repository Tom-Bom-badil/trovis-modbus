# src/trovis_modbus/exceptions.py

"""Exceptions raised by trovis-modbus."""

from __future__ import annotations


class TrovisWriteNotImplementedError(NotImplementedError):
    """Raised when writing to TROVIS (only for functions not implemented yet)."""