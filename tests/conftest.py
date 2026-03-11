"""Shared test helpers."""

from __future__ import annotations


def pad(header: bytes, size: int = 262) -> bytes:
    """Pad *header* with null bytes to *size* bytes total."""
    return header + b"\x00" * max(0, size - len(header))
