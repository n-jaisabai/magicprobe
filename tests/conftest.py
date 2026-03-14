"""Shared pytest configuration and marks.

Binary helpers and byte constants live in ``tests.helpers`` to keep this
file focused on pytest-specific concerns.
"""
from __future__ import annotations

import pytest

from magicprobe.probe import _libmagic_c

# re-export for backwards compatibility
from tests.helpers import pad as pad  # noqa: PLC0414

__all__ = ["pad", "needs_libmagic"]

needs_libmagic = pytest.mark.skipif(
    _libmagic_c is None,
    reason="system libmagic not installed — run: brew install libmagic",
)
