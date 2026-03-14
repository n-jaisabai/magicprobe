"""Shared binary factories and byte constants for the test suite.

Functions prefixed with ``make_`` build minimal but valid binary blobs that
libmagic can classify.  Module-level constants are pre-built once and reused
across all test modules.
"""
from __future__ import annotations

import io
import struct
import zipfile
import zlib


# ---------------------------------------------------------------------------
# Padding helper
# ---------------------------------------------------------------------------

def pad(header: bytes, size: int = 4096) -> bytes:
    """Pad *header* with null bytes up to *size* bytes total."""
    return header + b"\x00" * max(0, size - len(header))


# ---------------------------------------------------------------------------
# Binary factories
# ---------------------------------------------------------------------------

def make_png() -> bytes:
    """Return a minimal valid 1×1 PNG that libmagic recognises."""
    sig = b"\x89PNG\r\n\x1a\n"

    def chunk(tag: bytes, data: bytes) -> bytes:
        crc = zlib.crc32(tag + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", crc)

    ihdr = chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0))
    idat = chunk(b"IDAT", zlib.compress(b"\x00\xFF\xFF\xFF"))
    iend = chunk(b"IEND", b"")
    return sig + ihdr + idat + iend


def make_zip() -> bytes:
    """Return a minimal valid ZIP archive that libmagic recognises."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("hello.txt", "hello")
    return buf.getvalue()


# ---------------------------------------------------------------------------
# Pre-built constants (built once at import time)
# ---------------------------------------------------------------------------

PNG_BYTES  = make_png()
ZIP_BYTES  = make_zip()
JPEG_MAGIC = pad(b"\xff\xd8\xff")   # minimal JPEG header
GIF_MAGIC  = pad(b"GIF89a")         # minimal GIF header
PDF_MAGIC  = pad(b"%PDF-1.4")       # minimal PDF header
