"""Integration tests — verify that libmagic loads and works on the current OS.

Designed to run inside a Docker container (see ``docker/``) where libmagic is
installed via the OS package manager.  Kept separate from the unit-test suite
so ``pytest tests/`` works without Docker.

The ``libmagic`` session fixture is provided by ``tests/integration/conftest.py``.
"""
from __future__ import annotations

import pytest

import magicprobe
from magicprobe import probe, probe_all
from tests.helpers import GIF_MAGIC, JPEG_MAGIC, PDF_MAGIC, PNG_BYTES, ZIP_BYTES


# ---------------------------------------------------------------------------
# Library loads correctly
# ---------------------------------------------------------------------------

def test_libmagic_loads(libmagic):
    """LibMagic initialises without raising."""
    assert libmagic is not None


# ---------------------------------------------------------------------------
# from_buffer — common MIME types
# ---------------------------------------------------------------------------

def test_detect_png_from_buffer(libmagic):
    assert libmagic.from_buffer(PNG_BYTES) == "image/png"


def test_detect_jpeg_from_buffer(libmagic):
    result = libmagic.from_buffer(JPEG_MAGIC)
    assert result == "image/jpeg"


def test_detect_gif_from_buffer(libmagic):
    result = libmagic.from_buffer(GIF_MAGIC)
    assert result == "image/gif"


def test_detect_zip_from_buffer(libmagic):
    result = libmagic.from_buffer(ZIP_BYTES)
    assert result is not None
    assert "zip" in result or "officedocument" in result


def test_detect_pdf_from_buffer(libmagic):
    result = libmagic.from_buffer(PDF_MAGIC)
    assert result == "application/pdf"


def test_unknown_bytes_returns_value(libmagic):
    """Truly random bytes should return *something* (not raise)."""
    result = libmagic.from_buffer(b"\xaa\xbb\xcc\xdd" * 1024)
    assert result is None or isinstance(result, str)


# ---------------------------------------------------------------------------
# from_file — round-trip via a real file path
# ---------------------------------------------------------------------------

def test_detect_png_from_file(libmagic, tmp_path):
    f = tmp_path / "sample.png"
    f.write_bytes(PNG_BYTES)
    assert libmagic.from_file(str(f)) == "image/png"


def test_detect_zip_from_file(libmagic, tmp_path):
    f = tmp_path / "sample.zip"
    f.write_bytes(ZIP_BYTES)
    result = libmagic.from_file(str(f))
    assert result is not None
    assert "zip" in result or "officedocument" in result


# ---------------------------------------------------------------------------
# Public high-level API
# ---------------------------------------------------------------------------

def test_probe_png(libmagic):
    result = probe(PNG_BYTES)
    assert result is not None
    assert result.mime_type == "image/png"


def test_probe_accepts_bytearray(libmagic):
    result = probe(bytearray(PNG_BYTES))
    assert result is not None
    assert result.mime_type == "image/png"


def test_probe_accepts_path(libmagic, tmp_path):
    f = tmp_path / "img.png"
    f.write_bytes(PNG_BYTES)
    result = probe(f)
    assert result is not None
    assert result.mime_type == "image/png"


def test_probe_all_returns_list(libmagic):
    results = probe_all(PNG_BYTES)
    assert isinstance(results, list)
    assert len(results) >= 1
    assert any(r.mime_type == "image/png" for r in results)


def test_probe_unknown_returns_none(libmagic):
    result = probe(b"\xaa\xbb\xcc\xdd" * 1024)
    assert result is None or result.mime_type


# ---------------------------------------------------------------------------
# Package sanity
# ---------------------------------------------------------------------------

def test_version_is_set():
    assert magicprobe.__version__
