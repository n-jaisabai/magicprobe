"""Loads the libmagic shared library from the first working candidate path."""
from __future__ import annotations

import ctypes as _ct
import logging

from ._candidates import INSTALL_HINT, all_candidates

logger = logging.getLogger(__name__)


def load_lib() -> _ct.CDLL:
    """Try each candidate path in order and return the first that loads."""
    errors: list[OSError] = []

    for candidate in all_candidates():
        if not candidate:
            continue
        try:
            lib = _ct.CDLL(candidate)
            logger.debug("magicprobe: loaded libmagic from %r", candidate)
            return lib
        except OSError as exc:
            errors.append(exc)

    detail = "\n".join(str(e) for e in errors)
    raise ImportError(
        f"magicprobe: could not load libmagic.\n{INSTALL_HINT}\n\n{detail}"
    )
