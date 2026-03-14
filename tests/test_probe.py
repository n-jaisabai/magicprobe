"""High-level tests for the public ``probe`` / ``probe_all`` API."""

from __future__ import annotations

import pytest

import magicprobe
from magicprobe import probe, probe_all, ProbeResult
from tests.conftest import needs_libmagic
from tests.helpers import GIF_MAGIC, JPEG_MAGIC, PNG_BYTES, ZIP_BYTES, pad


# ---------------------------------------------------------------------------
# probe() — basic contract
# ---------------------------------------------------------------------------


@needs_libmagic
def test_probe_accepts_bytearray():
    result = probe(bytearray(PNG_BYTES))
    assert result is not None
    assert result.mime_type == "image/png"


@needs_libmagic
def test_probe_accepts_path_object(tmp_path):
    f = tmp_path / "sample.png"
    f.write_bytes(PNG_BYTES)
    result = probe(f)
    assert result is not None
    assert result.mime_type == "image/png"


@needs_libmagic
def test_probe_accepts_str_path(tmp_path):
    f = tmp_path / "sample.gif"
    f.write_bytes(pad(b"GIF89a"))
    result = probe(str(f))
    assert result is not None
    assert result.mime_type == "image/gif"


# ---------------------------------------------------------------------------
# ProbeResult — properties
# ---------------------------------------------------------------------------


@needs_libmagic
def test_probe_result_is_frozen():
    result = probe(PNG_BYTES)
    assert result is not None
    with pytest.raises((AttributeError, TypeError)):
        result.name = "other"  # type: ignore[misc]


@needs_libmagic
def test_probe_result_extension_is_none():
    result = probe(PNG_BYTES)
    assert result is not None
    assert result.extension is None


@needs_libmagic
def test_probe_result_repr():
    result = probe(pad(b"\xff\xd8\xff"))
    assert result is not None
    assert "image/jpeg" in repr(result)


# ---------------------------------------------------------------------------
# probe_all() — list return
# ---------------------------------------------------------------------------


@needs_libmagic
def test_probe_all_returns_list():
    results = probe_all(PNG_BYTES)
    assert isinstance(results, list)
    assert len(results) >= 1


@needs_libmagic
def test_probe_all_png_mime():
    results = probe_all(PNG_BYTES)
    mimes = [r.mime_type for r in results]
    assert "image/png" in mimes


@needs_libmagic
def test_probe_all_unknown_returns_list():
    results = probe_all(pad(b"\xaa\xbb\xcc\xdd"))
    assert isinstance(results, list)


@needs_libmagic
def test_probe_all_zip_detected():
    results = probe_all(ZIP_BYTES)
    assert len(results) >= 1
    assert any("zip" in r.mime_type or "officedocument" in r.mime_type for r in results)


# ---------------------------------------------------------------------------
# Version sanity (always runs)
# ---------------------------------------------------------------------------


def test_version_exists():
    assert magicprobe.__version__

