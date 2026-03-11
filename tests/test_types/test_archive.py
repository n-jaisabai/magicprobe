"""Unit tests for archive type detectors."""

from tests.conftest import pad
from magicprobe.types.archive import ZIP, GZIP, BZIP2, XZ, SevenZip, RAR, TAR, Zstandard, LZ4


class TestZIP:
    def test_local_file_header(self):
        assert ZIP.match(pad(b"PK\x03\x04"))

    def test_end_of_central_dir(self):
        assert ZIP.match(pad(b"PK\x05\x06"))

    def test_no_match(self):
        assert not ZIP.match(pad(b"\x00" * 4))


class TestGZIP:
    def test_match(self):
        assert GZIP.match(pad(b"\x1f\x8b"))

    def test_no_match(self):
        assert not GZIP.match(pad(b"\x1f\x9b"))


class TestBZIP2:
    def test_match(self):
        assert BZIP2.match(pad(b"BZh"))

    def test_no_match(self):
        assert not BZIP2.match(pad(b"BZi"))


class TestXZ:
    def test_match(self):
        assert XZ.match(pad(b"\xfd7zXZ\x00"))

    def test_no_match(self):
        assert not XZ.match(pad(b"\xfd7zXY\x00"))


class TestSevenZip:
    def test_match(self):
        assert SevenZip.match(pad(b"7z\xbc\xaf\x27\x1c"))

    def test_no_match(self):
        assert not SevenZip.match(pad(b"8z\xbc\xaf\x27\x1c"))


class TestRAR:
    def test_match_rar4(self):
        assert RAR.match(pad(b"Rar!\x1a\x07\x00"))

    def test_match_rar5(self):
        assert RAR.match(pad(b"Rar!\x1a\x07\x01\x00"))

    def test_no_match(self):
        assert not RAR.match(pad(b"Rar!\x1a\x08\x00"))


class TestTAR:
    def test_match_ustar(self):
        data = b"\x00" * 257 + b"ustar" + b"\x00" * 0
        assert TAR.match(data)

    def test_no_match_too_short(self):
        assert not TAR.match(b"\x00" * 100)


class TestZstandard:
    def test_match(self):
        assert Zstandard.match(pad(b"\x28\xb5\x2f\xfd"))

    def test_no_match(self):
        assert not Zstandard.match(pad(b"\x29\xb5\x2f\xfd"))


class TestLZ4:
    def test_match(self):
        assert LZ4.match(pad(b"\x04\x22\x4d\x18"))

    def test_no_match(self):
        assert not LZ4.match(pad(b"\x05\x22\x4d\x18"))
