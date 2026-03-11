"""High-level tests for the public ``probe`` / ``probe_all`` API."""

from __future__ import annotations

import pytest

import magicprobe
from magicprobe import probe, probe_all, ProbeResult
from tests.conftest import pad


# ---------------------------------------------------------------------------
# probe() — basic contract
# ---------------------------------------------------------------------------


def test_probe_returns_none_for_unknown_bytes():
    assert probe(pad(b"\x00\x01\x02\x03")) is None


def test_probe_accepts_bytearray():
    data = bytearray(b"\x89PNG\r\n\x1a\n") + bytearray(254)
    result = probe(data)
    assert result is not None
    assert result.name == "PNG"


def test_probe_accepts_path_object(tmp_path):
    f = tmp_path / "sample.png"
    f.write_bytes(pad(b"\x89PNG\r\n\x1a\n"))
    result = probe(f)
    assert result is not None
    assert result.name == "PNG"


def test_probe_accepts_str_path(tmp_path):
    f = tmp_path / "sample.gif"
    f.write_bytes(pad(b"GIF89a"))
    result = probe(str(f))
    assert result is not None
    assert result.name == "GIF"


# ---------------------------------------------------------------------------
# ProbeResult — properties
# ---------------------------------------------------------------------------


def test_probe_result_is_frozen():
    result = probe(pad(b"\x89PNG\r\n\x1a\n"))
    with pytest.raises((AttributeError, TypeError)):
        result.name = "other"  # type: ignore[misc]


def test_probe_result_extension_property():
    result = probe(pad(b"\x89PNG\r\n\x1a\n"))
    assert result is not None
    assert result.extension == ".png"


def test_probe_result_repr():
    result = probe(pad(b"\xff\xd8\xff"))
    assert result is not None
    assert "JPEG" in repr(result)
    assert "image/jpeg" in repr(result)


# ---------------------------------------------------------------------------
# probe_all() — multiple matches
# ---------------------------------------------------------------------------


def test_probe_all_returns_list():
    results = probe_all(pad(b"\x89PNG\r\n\x1a\n"))
    assert isinstance(results, list)
    assert len(results) >= 1


def test_probe_all_png_single_match():
    results = probe_all(pad(b"\x89PNG\r\n\x1a\n"))
    names = [r.name for r in results]
    assert "PNG" in names


def test_probe_all_empty_for_unknown():
    results = probe_all(pad(b"\xaa\xbb\xcc\xdd"))
    assert results == []


def test_probe_all_ooxml_also_matches_zip():
    # A minimal fake OOXML signature: PK header + [Content_Types].xml marker
    fake_ooxml = b"PK\x03\x04" + b"\x00" * 27 + b"[Content_Types].xml" + b"\x00" * 100
    results = probe_all(fake_ooxml)
    names = [r.name for r in results]
    assert "OOXML" in names
    assert "ZIP" in names  # OOXML is a ZIP — both should match


# ---------------------------------------------------------------------------
# Version sanity
# ---------------------------------------------------------------------------


def test_version_exists():
    assert magicprobe.__version__
