# Contributing to magicprobe

Thank you for your interest in contributing!  
The most common contribution is **adding support for a new file type** — and it intentionally takes very little code.

---

## Adding a new file type

### 1  Find the magic bytes

Every binary file format has a unique byte sequence (called a "magic number") at the start of the file.  
Good references:
- [Gary Kessler's File Signature Table](https://www.garykessler.net/library/file_sigs.html)
- [Wikipedia – List of file signatures](https://en.wikipedia.org/wiki/List_of_file_signatures)
- The official format specification

### 2  Choose the right module

Add your type to an **existing** module in `src/magicprobe/types/` or create a new one:

| Module          | File types |
|-----------------|------------|
| `image.py`      | Raster & vector images |
| `document.py`   | Text documents, office formats |
| `archive.py`    | Archives, compressed files |
| `audio.py`      | Audio formats |
| `video.py`      | Video formats |
| `executable.py` | Binaries, bytecode |

If your type does not fit any category, create a new module (e.g. `font.py`) and add an import to `src/magicprobe/types/__init__.py`.

### 3  Write the class

Copy this template and fill it in:

```python
from ..registry import register
from .base import FileType

@register                          # ← required: registers the type automatically
class MyFormat(FileType):
    name = "MyFormat"              # human-readable name shown in ProbeResult
    mime_type = "application/x-myformat"   # IANA MIME type
    extensions = [".myfmt"]        # list of common extensions; use [""] if none

    @classmethod
    def match(cls, data: bytes) -> bool:
        # `data` is the first 262 bytes of the file.
        # Return True if the signature matches.
        return data[:4] == b"\xAB\xCD\xEF\x00"
```

**Tips:**
- Keep `match()` fast — avoid loops or regex when a simple slice comparison works.
- If your format builds on another (e.g. it is a ZIP), register it **before** the
  generic base type so `probe()` returns the specific result first.  
  Adjust the import order in `src/magicprobe/types/__init__.py` if needed.
- Use a `_BRANDS` or `_MAGIC` class-level set/bytes constant instead of inline literals
  when there are multiple valid signatures — it keeps `match()` readable.

### 4  Add tests

Create or update the corresponding test file in `tests/test_types/`.  
Each type needs at minimum:

```python
from tests.conftest import pad
from magicprobe.types.mymodule import MyFormat

class TestMyFormat:
    def test_match(self):
        assert MyFormat.match(pad(b"\xAB\xCD\xEF\x00"))

    def test_no_match(self):
        assert not MyFormat.match(pad(b"\x00" * 4))

    def test_mime(self):
        assert MyFormat.mime_type == "application/x-myformat"
```

`pad(header)` zero-pads the header to 262 bytes so you don't need to construct a full valid file.

### 5  Run the tests

```bash
# Install in editable mode with dev extras
pip install -e ".[dev]"

# Run all tests
pytest

# Or with coverage
pytest --cov
```

All existing tests must continue to pass.

---

## Pull request checklist

- [ ] Magic bytes are sourced from an official specification or trusted reference (add a comment with the URL).
- [ ] `@register` decorator is present on the class.
- [ ] `name`, `mime_type`, and `extensions` are set correctly.
- [ ] `match()` returns `False` for a zero-filled 262-byte buffer.
- [ ] At least one positive and one negative test case are included.
- [ ] `pytest` passes with no errors.

---

## Development setup

```bash
git clone https://github.com/yourusername/magicprobe
cd magicprobe
pip install -e ".[dev]"
pytest
```

---

## Code style

- Python 3.10+ syntax.
- No external runtime dependencies.
- Public symbols should have docstrings.
- Line length ≤ 100 characters.

---

## Questions?

Open a [GitHub issue](https://github.com/yourusername/magicprobe/issues) — we're happy to help!
