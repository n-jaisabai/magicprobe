# magicprobe

A zero-dependency Python library that detects file types by inspecting **magic bytes** — the binary signatures at the start of every file.

```python
import magicprobe

result = magicprobe.probe("photo.jpg")
print(result.name)       # JPEG
print(result.mime_type)  # image/jpeg
print(result.extension)  # .jpg
```

## Features

- **Zero dependencies** — pure Python 3.10+
- **Fast** — reads only the first 262 bytes of each file
- **Extensible** — adding a new file type takes ~10 lines; see [CONTRIBUTING.md](CONTRIBUTING.md)
- **Type-safe** — fully typed, ships with `py.typed`
- **CLI included** — `magicprobe <file>` works out of the box

## Installation

```bash
pip install magicprobe
```

## Usage

### Detect a single file type

```python
import magicprobe

# From a file path (str or pathlib.Path)
result = magicprobe.probe("archive.zip")

# From raw bytes
with open("file.bin", "rb") as f:
    result = magicprobe.probe(f.read())

if result:
    print(result.name)        # "ZIP"
    print(result.mime_type)   # "application/zip"
    print(result.extensions)  # (".zip",)
    print(result.extension)   # ".zip"  ← primary extension shortcut
else:
    print("Unknown file type")
```

### Detect all matching types

Some formats are containers (e.g. a DOCX file is also a ZIP file).
`probe_all()` returns every matching type, ordered from most specific to least specific:

```python
results = magicprobe.probe_all("document.docx")
for r in results:
    print(r.name)  # OOXML, then ZIP
```

### Command-line interface

```bash
# One file
magicprobe image.png
# image.png: PNG (image/png)  [.png]

# Multiple files
magicprobe * 
```

## Supported types

| Category   | Types |
|------------|-------|
| Image      | PNG, JPEG, GIF, WEBP, BMP, TIFF, ICO, AVIF, HEIC |
| Document   | PDF, RTF, OLE2 (doc/xls/ppt), OOXML (docx/xlsx/pptx), EPUB |
| Archive    | ZIP, GZIP, BZIP2, XZ, 7-Zip, RAR, TAR, Zstandard, LZ4 |
| Audio      | MP3, WAV, FLAC, OGG, OPUS, M4A, AIFF |
| Video      | MP4, MOV, AVI, WEBM, MKV, FLV, WMV/ASF |
| Executable | ELF, PE (exe/dll), Mach-O, DEX (Android), WASM |

**Want to add a new type?**  
See [CONTRIBUTING.md](CONTRIBUTING.md) — it takes about 10 lines of code and a test.

## API reference

### `magicprobe.probe(source) → ProbeResult | None`

Detect the file type of `source` (file path or `bytes`).  
Returns the **first** matching `ProbeResult`, or `None` if unknown.

### `magicprobe.probe_all(source) → list[ProbeResult]`

Returns **all** matching `ProbeResult` objects (useful for container formats).

### `ProbeResult`

| Attribute    | Type            | Description |
|--------------|-----------------|-------------|
| `name`       | `str`           | Human-readable name, e.g. `"PNG"` |
| `mime_type`  | `str`           | IANA MIME type, e.g. `"image/png"` |
| `extensions` | `tuple[str, …]` | File extensions, e.g. `(".png",)` |
| `extension`  | `str \| None`   | Primary extension (property) |

## Project structure

```
src/magicprobe/
├── __init__.py       ← public API
├── probe.py          ← probe() / probe_all()
├── result.py         ← ProbeResult dataclass
├── registry.py       ← @register decorator & get_all()
├── __main__.py       ← CLI entry point
└── types/
    ├── base.py       ← FileType ABC
    ├── image.py
    ├── document.py
    ├── archive.py
    ├── audio.py
    ├── video.py
    └── executable.py
```

## Contributing

Contributions are welcome!  
Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a PR.

## License

[MIT](LICENSE)
