"""Pytest fixtures for the integration test suite."""
from __future__ import annotations

import pytest

from magicprobe._libmagic import get_libmagic


@pytest.fixture(scope="session")
def libmagic():
    """Return a live LibMagic instance; skip the whole session if unavailable."""
    try:
        return get_libmagic()
    except ImportError as exc:
        pytest.skip(f"libmagic not available on this system: {exc}")
