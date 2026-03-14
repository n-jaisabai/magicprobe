from __future__ import annotations

import os
from pathlib import Path
from typing import Union

from .result import ProbeResult

try:
    from ._libmagic import get_libmagic
    _libmagic_c = get_libmagic()
except Exception:
    _libmagic_c = None

_READ_SIZE = 4096


def _detect(source: Union[str, bytes, os.PathLike]) -> str | None:
    """Return the MIME type string from libmagic for *source*, or None."""
    if _libmagic_c is None:
        return None
    try:
        if not isinstance(source, (bytes, bytearray)):
            return _libmagic_c.from_file(os.fspath(source))
        data = bytes(source)[:_READ_SIZE]
        return _libmagic_c.from_buffer(data)
    except Exception:
        return None


def probe(source: Union[str, bytes, os.PathLike]) -> ProbeResult | None:
    """Detect the file type of *source*. Returns the first match, or ``None``."""
    mime = _detect(source)
    if mime:
        return ProbeResult(name=mime, mime_type=mime, extensions=())
    return None


def probe_all(source: Union[str, bytes, os.PathLike]) -> list[ProbeResult]:
    """Detect all matching file types for *source*. Returns an empty list if unknown."""
    mime = _detect(source)
    if mime:
        return [ProbeResult(name=mime, mime_type=mime, extensions=())]
    return []
