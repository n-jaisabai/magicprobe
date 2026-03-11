"""Unit tests for image type detectors."""

import pytest
from tests.conftest import pad
from magicprobe.types.image import PNG, JPEG, GIF, WEBP, BMP, TIFF, ICO, AVIF, HEIC


class TestPNG:
    def test_match(self):
        assert PNG.match(pad(b"\x89PNG\r\n\x1a\n"))

    def test_no_match(self):
        assert not PNG.match(pad(b"\x00" * 8))

    def test_mime(self):
        assert PNG.mime_type == "image/png"

    def test_extension(self):
        assert ".png" in PNG.extensions


class TestJPEG:
    def test_match(self):
        assert JPEG.match(pad(b"\xff\xd8\xff"))

    def test_no_match(self):
        assert not JPEG.match(pad(b"\x00\xd8\xff"))

    def test_mime(self):
        assert JPEG.mime_type == "image/jpeg"


class TestGIF:
    def test_gif87a(self):
        assert GIF.match(pad(b"GIF87a"))

    def test_gif89a(self):
        assert GIF.match(pad(b"GIF89a"))

    def test_no_match(self):
        assert not GIF.match(pad(b"GIF90a"))

    def test_mime(self):
        assert GIF.mime_type == "image/gif"


class TestWEBP:
    def test_match(self):
        data = b"RIFF\x00\x00\x00\x00WEBP" + b"\x00" * 252
        assert WEBP.match(data)

    def test_no_match_riff_wave(self):
        data = b"RIFF\x00\x00\x00\x00WAVE" + b"\x00" * 252
        assert not WEBP.match(data)

    def test_no_match_wrong_start(self):
        assert not WEBP.match(pad(b"\x00" * 12))


class TestBMP:
    def test_match(self):
        assert BMP.match(pad(b"BM"))

    def test_no_match(self):
        assert not BMP.match(pad(b"BA"))


class TestTIFF:
    def test_little_endian(self):
        assert TIFF.match(pad(b"II*\x00"))

    def test_big_endian(self):
        assert TIFF.match(pad(b"MM\x00*"))

    def test_no_match(self):
        assert not TIFF.match(pad(b"\x00" * 4))


class TestICO:
    def test_match(self):
        assert ICO.match(pad(b"\x00\x00\x01\x00"))

    def test_no_match(self):
        assert not ICO.match(pad(b"\x00\x00\x02\x00"))


class TestAVIF:
    def test_match(self):
        data = pad(b"\x00\x00\x00\x00ftypavif")
        assert AVIF.match(data)

    def test_match_avis(self):
        data = pad(b"\x00\x00\x00\x00ftypavis")
        assert AVIF.match(data)

    def test_no_match_heic(self):
        data = pad(b"\x00\x00\x00\x00ftypheic")
        assert not AVIF.match(data)


class TestHEIC:
    def test_match_heic(self):
        data = pad(b"\x00\x00\x00\x00ftypheic")
        assert HEIC.match(data)

    def test_match_mif1(self):
        data = pad(b"\x00\x00\x00\x00ftypmif1")
        assert HEIC.match(data)

    def test_no_match_avif(self):
        data = pad(b"\x00\x00\x00\x00ftypavif")
        assert not HEIC.match(data)
