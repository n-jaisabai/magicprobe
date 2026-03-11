"""Executable / binary file-type definitions.

Covered formats: ELF, PE (Windows), Mach-O (macOS), DEX (Android), WASM.
"""

from ..registry import register
from .base import FileType


@register
class ELF(FileType):
    """Executable and Linkable Format (Linux/Unix)."""

    name = "ELF"
    mime_type = "application/x-elf"
    extensions = [""]  # No single conventional extension (.so, .o, no ext, …)

    @classmethod
    def match(cls, data: bytes) -> bool:
        return data[:4] == b"\x7fELF"


@register
class PE(FileType):
    """Portable Executable (Windows .exe / .dll / .sys)."""

    name = "PE"
    mime_type = "application/x-dosexec"
    extensions = [".exe", ".dll", ".sys"]

    @classmethod
    def match(cls, data: bytes) -> bool:
        return data[:2] == b"MZ"


@register
class MachO(FileType):
    """Mach-O binary (macOS / iOS)."""

    name = "Mach-O"
    mime_type = "application/x-mach-binary"
    extensions = [""]

    _MAGICS = {
        b"\xce\xfa\xed\xfe",  # 32-bit little-endian
        b"\xcf\xfa\xed\xfe",  # 64-bit little-endian
        b"\xfe\xed\xfa\xce",  # 32-bit big-endian
        b"\xfe\xed\xfa\xcf",  # 64-bit big-endian
        b"\xca\xfe\xba\xbe",  # Universal (fat) binary
    }

    @classmethod
    def match(cls, data: bytes) -> bool:
        return data[:4] in cls._MAGICS


@register
class DEX(FileType):
    """Android Dalvik Executable."""

    name = "DEX"
    mime_type = "application/x-dex"
    extensions = [".dex"]

    @classmethod
    def match(cls, data: bytes) -> bool:
        # Magic: "dex\n" followed by version string ("035\0" … "039\0")
        return data[:4] == b"dex\n" and data[4:7].isdigit()


@register
class WASM(FileType):
    """WebAssembly binary module."""

    name = "WASM"
    mime_type = "application/wasm"
    extensions = [".wasm"]

    @classmethod
    def match(cls, data: bytes) -> bool:
        return data[:4] == b"\x00asm"
