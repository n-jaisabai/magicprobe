"""Unit tests for video type detectors."""

from tests.conftest import pad
from magicprobe.types.video import MP4, MOV, AVI, WEBM, MKV, FLV, WMV


class TestMP4:
    def test_match_isom(self):
        data = pad(b"\x00\x00\x00\x00ftypisom")
        assert MP4.match(data)

    def test_match_avc1(self):
        data = pad(b"\x00\x00\x00\x00ftypavc1")
        assert MP4.match(data)

    def test_no_match_mov(self):
        data = pad(b"\x00\x00\x00\x00ftypqt  ")
        assert not MP4.match(data)


class TestMOV:
    def test_match_ftyp_qt(self):
        data = pad(b"\x00\x00\x00\x00ftypqt  ")
        assert MOV.match(data)

    def test_match_moov_atom(self):
        data = pad(b"\x00\x00\x00\x00moov")
        assert MOV.match(data)

    def test_no_match_mp4(self):
        data = pad(b"\x00\x00\x00\x00ftypisom")
        assert not MOV.match(data)


class TestAVI:
    def test_match(self):
        data = b"RIFF\x00\x00\x00\x00AVI " + b"\x00" * 252
        assert AVI.match(data)

    def test_no_match_wave(self):
        data = b"RIFF\x00\x00\x00\x00WAVE" + b"\x00" * 252
        assert not AVI.match(data)


class TestWEBM:
    def test_match(self):
        data = b"\x1a\x45\xdf\xa3" + b"\x00" * 10 + b"webm" + b"\x00" * 248
        assert WEBM.match(data)

    def test_no_match_no_webm_string(self):
        # EBML magic but no "webm" DocType in first 64 bytes
        data = b"\x1a\x45\xdf\xa3" + b"\x00" * 258
        assert not WEBM.match(data)


class TestMKV:
    def test_match(self):
        assert MKV.match(pad(b"\x1a\x45\xdf\xa3"))

    def test_no_match(self):
        assert not MKV.match(pad(b"\x1b\x45\xdf\xa3"))


class TestFLV:
    def test_match(self):
        assert FLV.match(pad(b"FLV\x01"))

    def test_no_match_wrong_version(self):
        assert not FLV.match(pad(b"FLV\x02"))


class TestWMV:
    def test_match(self):
        magic = b"\x30\x26\xb2\x75\x8e\x66\xcf\x11\xa6\xd9\x00\xaa\x00\x62\xce\x6c"
        assert WMV.match(pad(magic))

    def test_no_match(self):
        assert not WMV.match(pad(b"\x00" * 16))
