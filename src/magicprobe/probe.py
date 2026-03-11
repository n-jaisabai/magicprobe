from __future__ import annotations

import os
from pathlib import Path
from typing import Union

from . import registry
from .result import ProbeResult

# How many bytes to read from the file — large enough for all known signatures.
_READ_SIZE = 262


def probe(source: Union[str, bytes, os.PathLike]) -> ProbeResult | None:
    """Detect the file type of *source*.

    Args:
        source: A file path (:class:`str`, :class:`pathlib.Path`) or raw
                :class:`bytes` / :class:`bytearray`.

    Returns:
        A :class:`~magicprobe.result.ProbeResult` for the *first* matching
        type, or ``None`` if the type is unknown.

    Example::

        import magicprobe

        result = magicprobe.probe("photo.jpg")
        print(result.name)       # JPEG
        print(result.mime_type)  # image/jpeg
    """
    data = _read(source)
    for file_type in registry.get_all():
        if file_type.match(data):
            return ProbeResult(
                name=file_type.name,
                mime_type=file_type.mime_type,
                extensions=tuple(file_type.extensions),
            )
    return None


def probe_all(source: Union[str, bytes, os.PathLike]) -> list[ProbeResult]:
    """Detect **all** matching file types for *source*.

    Some formats are container formats (e.g. DOCX is also a ZIP file).
    This function returns every type whose signature matches, ordered by
    registration priority (most specific first).

    Args:
        source: A file path or raw bytes.

    Returns:
        A list of :class:`~magicprobe.result.ProbeResult` objects (may be
        empty if the type is unknown).
    """
    data = _read(source)
    results: list[ProbeResult] = []
    for file_type in registry.get_all():
        if file_type.match(data):
            results.append(
                ProbeResult(
                    name=file_type.name,
                    mime_type=file_type.mime_type,
                    extensions=tuple(file_type.extensions),
                )
            )
    return results


def _read(source: Union[str, bytes, os.PathLike]) -> bytes:
    if isinstance(source, (bytes, bytearray)):
        return bytes(source)[:_READ_SIZE]
    path = Path(os.fspath(source))
    with path.open("rb") as fh:
        return fh.read(_READ_SIZE)
