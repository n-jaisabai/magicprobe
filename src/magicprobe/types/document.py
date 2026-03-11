"""Document file-type definitions.

Covered formats: PDF, RTF, OLE2 (legacy Office), OOXML (DOCX/XLSX/PPTX), EPUB.

**Registration order matters for** ``probe()``: more specific ZIP-based formats
(EPUB, OOXML) are registered before the generic ZIP detector in
``archive.py``, so they win when ``probe()`` returns the first match.
"""

from ..registry import register
from .base import FileType


@register
class PDF(FileType):
    name = "PDF"
    mime_type = "application/pdf"
    extensions = [".pdf"]

    @classmethod
    def match(cls, data: bytes) -> bool:
        return data[:4] == b"%PDF"


@register
class RTF(FileType):
    name = "RTF"
    mime_type = "application/rtf"
    extensions = [".rtf"]

    @classmethod
    def match(cls, data: bytes) -> bool:
        return data[:5] == b"{\\rtf"


@register
class OLE2(FileType):
    """Microsoft OLE2 compound document (legacy .doc, .xls, .ppt, .msi …)."""

    name = "OLE2"
    mime_type = "application/x-ole-storage"
    extensions = [".doc", ".xls", ".ppt", ".msi"]

    @classmethod
    def match(cls, data: bytes) -> bool:
        return data[:8] == b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"


@register
class EPUB(FileType):
    """EPUB e-book — a ZIP file whose first entry is the uncompressed ``mimetype`` file."""

    name = "EPUB"
    mime_type = "application/epub+zip"
    extensions = [".epub"]

    @classmethod
    def match(cls, data: bytes) -> bool:
        # The spec requires "mimetype" as the first filename (offset 30) and
        # "application/epub+zip" as its uncompressed content immediately after.
        return (
            data[:4] == b"PK\x03\x04"
            and b"mimetype" in data[28:42]
            and b"application/epub+zip" in data
        )


@register
class OOXML(FileType):
    """Office Open XML — DOCX, XLSX, PPTX (ZIP containing ``[Content_Types].xml``)."""

    name = "OOXML"
    mime_type = "application/vnd.openxmlformats-officedocument"
    extensions = [".docx", ".xlsx", ".pptx"]

    @classmethod
    def match(cls, data: bytes) -> bool:
        # The first entry in the ZIP is always [Content_Types].xml for OOXML files.
        return data[:4] == b"PK\x03\x04" and b"[Content_Types].xml" in data
