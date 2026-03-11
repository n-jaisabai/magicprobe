"""Audio file-type definitions.

Covered formats: MP3, WAV, FLAC, OGG, OPUS, M4A, AIFF.

**Registration order:** OPUS (more specific OGG container) is registered
before the generic OGG detector so that ``probe()`` returns "OPUS" for
Opus-encoded Ogg streams.
"""

from ..registry import register
from .base import FileType


@register
class MP3(FileType):
    name = "MP3"
    mime_type = "audio/mpeg"
    extensions = [".mp3"]

    @classmethod
    def match(cls, data: bytes) -> bool:
        # ID3 tag header OR raw MPEG sync word (various layer / bitrate combos)
        return data[:3] == b"ID3" or data[:2] in (b"\xff\xfb", b"\xff\xf3", b"\xff\xf2")


@register
class WAV(FileType):
    name = "WAV"
    mime_type = "audio/wav"
    extensions = [".wav"]

    @classmethod
    def match(cls, data: bytes) -> bool:
        return data[:4] == b"RIFF" and data[8:12] == b"WAVE"


@register
class FLAC(FileType):
    name = "FLAC"
    mime_type = "audio/flac"
    extensions = [".flac"]

    @classmethod
    def match(cls, data: bytes) -> bool:
        return data[:4] == b"fLaC"


@register
class OPUS(FileType):
    """Opus audio encapsulated in an Ogg container."""

    name = "OPUS"
    mime_type = "audio/opus"
    extensions = [".opus"]

    @classmethod
    def match(cls, data: bytes) -> bool:
        # OggS capture pattern + OpusHead magic in the first page
        return data[:4] == b"OggS" and b"OpusHead" in data[:64]


@register
class OGG(FileType):
    name = "OGG"
    mime_type = "audio/ogg"
    extensions = [".ogg", ".oga"]

    @classmethod
    def match(cls, data: bytes) -> bool:
        return data[:4] == b"OggS"


@register
class M4A(FileType):
    name = "M4A"
    mime_type = "audio/mp4"
    extensions = [".m4a", ".m4b"]

    _BRANDS = {b"M4A ", b"M4B ", b"M4P "}

    @classmethod
    def match(cls, data: bytes) -> bool:
        return data[4:8] == b"ftyp" and data[8:12] in cls._BRANDS


@register
class AIFF(FileType):
    name = "AIFF"
    mime_type = "audio/aiff"
    extensions = [".aiff", ".aif"]

    @classmethod
    def match(cls, data: bytes) -> bool:
        return data[:4] == b"FORM" and data[8:12] in (b"AIFF", b"AIFC")
