# magicprobe

A Python library that detects file types by delegating to the system
[libmagic](https://www.darwinsys.com/file/) C library via `ctypes`.
No third-party Python packages are required.

```python
import magicprobe

result = magicprobe.probe("photo.jpg")
if result:
    print(result.mime_type)  # image/jpeg
```

## Requirements

- Python 3.10+
- The **libmagic** shared library installed on the system:

```bash
# macOS
brew install libmagic

# Debian / Ubuntu
apt install libmagic1
```

## Installation

```bash
pip install magicprobe
```

## Usage

### Detect the type of a file

```python
import magicprobe

# From a file path (str or pathlib.Path)
result = magicprobe.probe("archive.zip")

# From raw bytes
with open("file.bin", "rb") as f:
    result = magicprobe.probe(f.read())

if result:
    print(result.name)       # "application/zip"
    print(result.mime_type)  # "application/zip"
else:
    print("Unknown file type")
```

### Detect all matching types

`probe_all()` returns every MIME type libmagic reports for the source,
ordered from most to least specific:

```python
results = magicprobe.probe_all("document.docx")
for r in results:
    print(r.mime_type)
```

### Command-line interface

```bash
magicprobe image.png
# image.png: image/png (image/png)  [—]

magicprobe file1 file2 file3
```

## API reference

### `magicprobe.probe(source) → ProbeResult | None`

Detect the file type of `source`.

- `source` — a file path (`str` or `pathlib.Path`) or raw `bytes` / `bytearray`.
- Returns the first matching `ProbeResult`, or `None` if libmagic cannot identify the type.

### `magicprobe.probe_all(source) → list[ProbeResult]`

Same as `probe()` but returns all matching `ProbeResult` objects.
Returns an empty list if the type is unknown.

### `ProbeResult`

| Attribute    | Type              | Description |
|--------------|-------------------|-------------|
| `name`       | `str`             | MIME type string returned by libmagic, e.g. `"image/png"` |
| `mime_type`  | `str`             | IANA MIME type, e.g. `"image/png"` |
| `extensions` | `tuple[str, ...]` | File extensions (empty tuple in the current release) |
| `extension`  | `str \| None`     | Primary extension, or `None` (property) |

## Project structure

```
src/magicprobe/
├── __init__.py      — public API (probe, probe_all, ProbeResult)
├── probe.py         — probe() / probe_all() implementation
├── result.py        — ProbeResult dataclass
├── libmagic_c.py    — ctypes wrapper for the system libmagic library
└── __main__.py      — CLI entry point
```

## Contributing

Contributions are welcome.  
See [CONTRIBUTING.md](CONTRIBUTING.md) for setup instructions and guidelines.

## License

[MIT](LICENSE)
