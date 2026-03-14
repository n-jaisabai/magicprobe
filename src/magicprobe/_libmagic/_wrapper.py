"""ctypes wrapper around the libmagic C API."""
from __future__ import annotations

import ctypes as _ct
import os
from typing import Optional

from ._loader import load_lib

# MIME type flag
_MAGIC_MIME_TYPE = 0x000010


def _setup_signatures(lib: _ct.CDLL) -> None:
    """Declare argtypes / restype for every libmagic function we use."""
    void_p = _ct.c_void_p
    char_p = _ct.c_char_p
    c_int  = _ct.c_int
    size_t = _ct.c_size_t

    lib.magic_open.argtypes     = [c_int];          lib.magic_open.restype     = void_p
    lib.magic_close.argtypes    = [void_p];          lib.magic_close.restype    = None
    lib.magic_load.argtypes     = [void_p, char_p];  lib.magic_load.restype     = c_int
    lib.magic_setflags.argtypes = [void_p, c_int];   lib.magic_setflags.restype = c_int
    lib.magic_buffer.argtypes   = [void_p, void_p, size_t]; lib.magic_buffer.restype = char_p
    lib.magic_file.argtypes     = [void_p, char_p];         lib.magic_file.restype   = char_p


def _decode_result(raw: Optional[bytes]) -> Optional[str]:
    """Decode a raw libmagic result to a clean MIME-type string, or ``None``."""
    if not raw:
        return None
    return raw.decode("utf-8", errors="ignore").split(";")[0].strip() or None


class LibMagic:
    """Thin ctypes wrapper around the libmagic C library."""

    def __init__(self) -> None:
        self._lib = load_lib()
        _setup_signatures(self._lib)

        self._handle = self._lib.magic_open(_MAGIC_MIME_TYPE)
        if not self._handle:
            raise OSError("magic_open() returned NULL")
        self._lib.magic_load(self._handle, None)

    def from_buffer(self, data: bytes) -> Optional[str]:
        """Return the MIME type of *data*, or ``None``."""
        buf = _ct.create_string_buffer(bytes(data), len(data))
        raw = self._lib.magic_buffer(self._handle, buf, _ct.c_size_t(len(data)))
        return _decode_result(raw)

    def from_file(self, path: str) -> Optional[str]:
        """Return the MIME type of the file at *path*, or ``None``."""
        raw = self._lib.magic_file(self._handle, _ct.c_char_p(os.fsencode(path)))
        return _decode_result(raw)

    def __del__(self) -> None:
        handle = getattr(self, "_handle", None)
        lib    = getattr(self, "_lib", None)
        if handle and lib:
            try:
                lib.magic_close(handle)
            except Exception:
                pass
        self._handle = None
