"""Unit tests for executable type detectors."""

from tests.conftest import pad
from magicprobe.types.executable import ELF, PE, MachO, DEX, WASM


class TestELF:
    def test_match(self):
        assert ELF.match(pad(b"\x7fELF"))

    def test_no_match(self):
        assert not ELF.match(pad(b"\x7fELG"))


class TestPE:
    def test_match_exe(self):
        assert PE.match(pad(b"MZ"))

    def test_no_match(self):
        assert not PE.match(pad(b"NZ"))


class TestMachO:
    def test_match_32bit_le(self):
        assert MachO.match(pad(b"\xce\xfa\xed\xfe"))

    def test_match_64bit_le(self):
        assert MachO.match(pad(b"\xcf\xfa\xed\xfe"))

    def test_match_fat(self):
        assert MachO.match(pad(b"\xca\xfe\xba\xbe"))

    def test_no_match(self):
        assert not MachO.match(pad(b"\x00" * 4))


class TestDEX:
    def test_match_035(self):
        assert DEX.match(pad(b"dex\n035\x00"))

    def test_match_039(self):
        assert DEX.match(pad(b"dex\n039\x00"))

    def test_no_match(self):
        assert not DEX.match(pad(b"dex\nabc\x00"))


class TestWASM:
    def test_match(self):
        assert WASM.match(pad(b"\x00asm"))

    def test_no_match(self):
        assert not WASM.match(pad(b"\x01asm"))
