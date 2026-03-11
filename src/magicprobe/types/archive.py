"""Archive / compression file-type definitions.

Covered formats: ZIP, GZIP, BZIP2, XZ, 7-Zip, RAR (v4 & v5), TAR, Zstandard, LZ4.

ZIP is registered *after* the more specific ZIP-based document types
(EPUB, OOXML) so that ``probe()`` returns the precise format first.
"""

from ..registry import register
from .base import FileType


@register
class ZIP(FileType):
    name = "ZIP"
    mime_type = "application/zip"
    extensions = [".zip"]

    @classmethod
    def match(cls, data: bytes) -> bool:
        # Local file header, empty archive, or spanned archive signatures
        return data[:4] in (b"PK\x03\x04", b"PK\x05\x06", b"PK\x07\x08")


@register
class GZIP(FileType):
    name = "GZIP"
    mime_type = "application/gzip"
    extensions = [".gz"]

    @classmethod
    def match(cls, data: bytes) -> bool:
        return data[:2] == b"\x1f\x8b"


@register
class BZIP2(FileType):
    name = "BZIP2"
    mime_type = "application/x-bzip2"
    extensions = [".bz2"]

    @classmethod
    def match(cls, data: bytes) -> bool:
        return data[:2] == b"BZ" and data[2:3] == b"h"


@register
class XZ(FileType):
    name = "XZ"
    mime_type = "application/x-xz"
    extensions = [".xz"]

    @classmethod
    def match(cls, data: bytes) -> bool:
        return data[:6] == b"\xfd7zXZ\x00"


@register
class SevenZip(FileType):
    name = "7-Zip"
    mime_type = "application/x-7z-compressed"
    extensions = [".7z"]

    @classmethod
    def match(cls, data: bytes) -> bool:
        return data[:6] == b"7z\xbc\xaf\x27\x1c"


@register
class RAR(FileType):
    name = "RAR"
    mime_type = "application/x-rar-compressed"
    extensions = [".rar"]

    @classmethod
    def match(cls, data: bytes) -> bool:
        # RAR 4.x: Rar!\x1a\x07\x00  |  RAR 5.x: Rar!\x1a\x07\x01\x00
        return data[:7] == b"Rar!\x1a\x07\x00" or data[:8] == b"Rar!\x1a\x07\x01\x00"


@register
class TAR(FileType):
    """POSIX ustar tape archive."""

    name = "TAR"
    mime_type = "application/x-tar"
    extensions = [".tar"]

    @classmethod
    def match(cls, data: bytes) -> bool:
        # ustar magic field at offset 257 (POSIX) — "ustar" with or without space
        return len(data) >= 262 and data[257:262] in (b"ustar", b"ustar")


@register
class Zstandard(FileType):
    name = "Zstandard"
    mime_type = "application/zstd"
    extensions = [".zst"]

    @classmethod
    def match(cls, data: bytes) -> bool:
        return data[:4] == b"\x28\xb5\x2f\xfd"


@register
class LZ4(FileType):
    name = "LZ4"
    mime_type = "application/x-lz4"
    extensions = [".lz4"]

    @classmethod
    def match(cls, data: bytes) -> bool:
        return data[:4] == b"\x04\x22\x4d\x18"
