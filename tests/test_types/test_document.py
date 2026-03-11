"""Unit tests for document type detectors."""

from tests.conftest import pad
from magicprobe.types.document import PDF, RTF, OLE2, EPUB, OOXML


class TestPDF:
    def test_match(self):
        assert PDF.match(pad(b"%PDF"))

    def test_no_match(self):
        assert not PDF.match(pad(b"%PDE"))


class TestRTF:
    def test_match(self):
        assert RTF.match(pad(b"{\\rtf"))

    def test_no_match(self):
        assert not RTF.match(pad(b"{\\rtg"))


class TestOLE2:
    def test_match(self):
        assert OLE2.match(pad(b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"))

    def test_no_match(self):
        assert not OLE2.match(pad(b"\x00" * 8))


class TestEPUB:
    def test_match(self):
        # Minimal fake EPUB: PK header, "mimetype" at offset 30, content follows
        header = b"PK\x03\x04" + b"\x00" * 26 + b"mimetype" + b"application/epub+zip" + b"\x00" * 100
        assert EPUB.match(header)

    def test_no_match_plain_zip(self):
        assert not EPUB.match(pad(b"PK\x03\x04"))

    def test_no_match_ooxml(self):
        data = b"PK\x03\x04" + b"\x00" * 27 + b"[Content_Types].xml" + b"\x00" * 100
        assert not EPUB.match(data)


class TestOOXML:
    def test_match(self):
        data = b"PK\x03\x04" + b"\x00" * 27 + b"[Content_Types].xml" + b"\x00" * 100
        assert OOXML.match(data)

    def test_no_match_plain_zip(self):
        assert not OOXML.match(pad(b"PK\x03\x04"))

    def test_no_match_epub(self):
        header = b"PK\x03\x04" + b"\x00" * 26 + b"mimetype" + b"application/epub+zip" + b"\x00" * 100
        assert not OOXML.match(header)
