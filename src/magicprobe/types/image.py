"""Image file-type definitions.

Covered formats: PNG, JPEG, GIF, WEBP, BMP, TIFF, ICO, AVIF, HEIC.
"""

from ..registry import register
from .base import FileType


@register
class PNG(FileType):
    name = "PNG"
    mime_type = "image/png"
    extensions = [".png"]

    @classmethod
    def match(cls, data: bytes) -> bool:
        return data[:8] == b"\x89PNG\r\n\x1a\n"


@register
class JPEG(FileType):
    name = "JPEG"
    mime_type = "image/jpeg"
    extensions = [".jpg", ".jpeg"]

    @classmethod
    def match(cls, data: bytes) -> bool:
        return data[:3] == b"\xff\xd8\xff"


@register
class GIF(FileType):
    name = "GIF"
    mime_type = "image/gif"
    extensions = [".gif"]

    @classmethod
    def match(cls, data: bytes) -> bool:
        return data[:6] in (b"GIF87a", b"GIF89a")


@register
class WEBP(FileType):
    name = "WEBP"
    mime_type = "image/webp"
    extensions = [".webp"]

    @classmethod
    def match(cls, data: bytes) -> bool:
        return data[:4] == b"RIFF" and data[8:12] == b"WEBP"


@register
class BMP(FileType):
    name = "BMP"
    mime_type = "image/bmp"
    extensions = [".bmp"]

    @classmethod
    def match(cls, data: bytes) -> bool:
        return data[:2] == b"BM"


@register
class TIFF(FileType):
    name = "TIFF"
    mime_type = "image/tiff"
    extensions = [".tif", ".tiff"]

    @classmethod
    def match(cls, data: bytes) -> bool:
        # Little-endian ("II") or big-endian ("MM") byte order mark
        return data[:4] in (b"II*\x00", b"MM\x00*")


@register
class ICO(FileType):
    name = "ICO"
    mime_type = "image/x-icon"
    extensions = [".ico"]

    @classmethod
    def match(cls, data: bytes) -> bool:
        return data[:4] == b"\x00\x00\x01\x00"


@register
class AVIF(FileType):
    name = "AVIF"
    mime_type = "image/avif"
    extensions = [".avif"]

    _BRANDS = {b"avif", b"avis"}

    @classmethod
    def match(cls, data: bytes) -> bool:
        return data[4:8] == b"ftyp" and data[8:12] in cls._BRANDS


@register
class HEIC(FileType):
    name = "HEIC"
    mime_type = "image/heic"
    extensions = [".heic", ".heif"]

    _BRANDS = {b"heic", b"heix", b"hevc", b"hevx", b"heim", b"heis", b"hevm", b"hevs", b"mif1", b"msf1"}

    @classmethod
    def match(cls, data: bytes) -> bool:
        return data[4:8] == b"ftyp" and data[8:12] in cls._BRANDS
