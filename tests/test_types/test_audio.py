"""Unit tests for audio type detectors."""

from tests.conftest import pad
from magicprobe.types.audio import MP3, WAV, FLAC, OPUS, OGG, M4A, AIFF


class TestMP3:
    def test_match_id3(self):
        assert MP3.match(pad(b"ID3"))

    def test_match_sync_fb(self):
        assert MP3.match(pad(b"\xff\xfb"))

    def test_match_sync_f3(self):
        assert MP3.match(pad(b"\xff\xf3"))

    def test_no_match(self):
        assert not MP3.match(pad(b"\x00" * 4))


class TestWAV:
    def test_match(self):
        data = b"RIFF\x00\x00\x00\x00WAVE" + b"\x00" * 252
        assert WAV.match(data)

    def test_no_match_webp(self):
        data = b"RIFF\x00\x00\x00\x00WEBP" + b"\x00" * 252
        assert not WAV.match(data)


class TestFLAC:
    def test_match(self):
        assert FLAC.match(pad(b"fLaC"))

    def test_no_match(self):
        assert not FLAC.match(pad(b"fLaD"))


class TestOPUS:
    def test_match(self):
        # OggS page containing OpusHead in the first 64 bytes
        data = b"OggS" + b"\x00" * 22 + b"OpusHead" + b"\x00" * 228
        assert OPUS.match(data)

    def test_no_match_plain_ogg(self):
        # OggS page without OpusHead
        data = b"OggS" + b"\x00" * 258
        assert not OPUS.match(data)


class TestOGG:
    def test_match(self):
        assert OGG.match(pad(b"OggS"))

    def test_no_match(self):
        assert not OGG.match(pad(b"OggT"))


class TestM4A:
    def test_match_m4a(self):
        data = pad(b"\x00\x00\x00\x00ftypM4A ")
        assert M4A.match(data)

    def test_match_m4b(self):
        data = pad(b"\x00\x00\x00\x00ftypM4B ")
        assert M4A.match(data)

    def test_no_match_mp4(self):
        data = pad(b"\x00\x00\x00\x00ftypisom")
        assert not M4A.match(data)


class TestAIFF:
    def test_match_aiff(self):
        data = b"FORM\x00\x00\x00\x00AIFF" + b"\x00" * 252
        assert AIFF.match(data)

    def test_match_aifc(self):
        data = b"FORM\x00\x00\x00\x00AIFC" + b"\x00" * 252
        assert AIFF.match(data)

    def test_no_match_wave(self):
        data = b"FORM\x00\x00\x00\x00WAVE" + b"\x00" * 252
        assert not AIFF.match(data)
