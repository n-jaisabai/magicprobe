"""Video file-type definitions.

Covered formats: MP4, MOV, AVI, WEBM, MKV, FLV, WMV/ASF.

**Registration order:** WEBM (more specific EBML container) is registered
before the generic MKV detector.  MP4 and MOV share the ``ftyp`` atom but
use different brand codes.
"""

from ..registry import register
from .base import FileType


@register
class MP4(FileType):
    name = "MP4"
    mime_type = "video/mp4"
    extensions = [".mp4"]

    _BRANDS = {
        b"isom", b"iso2", b"iso3", b"iso4", b"iso5", b"iso6",
        b"avc1", b"mp41", b"mp42", b"mp71",
    }

    @classmethod
    def match(cls, data: bytes) -> bool:
        return data[4:8] == b"ftyp" and data[8:12] in cls._BRANDS


@register
class MOV(FileType):
    name = "MOV"
    mime_type = "video/quicktime"
    extensions = [".mov"]

    @classmethod
    def match(cls, data: bytes) -> bool:
        # ftyp box with QuickTime brand or bare moov/wide/mdat atoms
        return (data[4:8] == b"ftyp" and data[8:12] == b"qt  ") or data[4:8] in (
            b"moov",
            b"wide",
            b"mdat",
            b"free",
        )


@register
class AVI(FileType):
    name = "AVI"
    mime_type = "video/x-msvideo"
    extensions = [".avi"]

    @classmethod
    def match(cls, data: bytes) -> bool:
        return data[:4] == b"RIFF" and data[8:12] == b"AVI "


@register
class WEBM(FileType):
    """WebM video (EBML container with ``webm`` DocType)."""

    name = "WEBM"
    mime_type = "video/webm"
    extensions = [".webm"]

    @classmethod
    def match(cls, data: bytes) -> bool:
        return data[:4] == b"\x1a\x45\xdf\xa3" and b"webm" in data[:64]


@register
class MKV(FileType):
    """Matroska video (EBML container)."""

    name = "MKV"
    mime_type = "video/x-matroska"
    extensions = [".mkv", ".mka"]

    @classmethod
    def match(cls, data: bytes) -> bool:
        return data[:4] == b"\x1a\x45\xdf\xa3"


@register
class FLV(FileType):
    name = "FLV"
    mime_type = "video/x-flv"
    extensions = [".flv"]

    @classmethod
    def match(cls, data: bytes) -> bool:
        return data[:3] == b"FLV" and data[3:4] == b"\x01"


@register
class WMV(FileType):
    """Windows Media Video / Audio / ASF container."""

    name = "WMV"
    mime_type = "video/x-ms-wmv"
    extensions = [".wmv", ".wma", ".asf"]

    # ASF GUID: 30 26 B2 75 8E 66 CF 11 A6 D9 00 AA 00 62 CE 6C
    _MAGIC = b"\x30\x26\xb2\x75\x8e\x66\xcf\x11\xa6\xd9\x00\xaa\x00\x62\xce\x6c"

    @classmethod
    def match(cls, data: bytes) -> bool:
        return data[:16] == cls._MAGIC
