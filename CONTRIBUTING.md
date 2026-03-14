# Contributing to magicprobe

Thank you for your interest in contributing!

---

## How it works

magicprobe is a thin `ctypes` wrapper around the system **libmagic** C library.
The main modules are:

| Module          | Purpose |
|-----------------|---------|
| `libmagic_c.py` | Loads libmagic via `ctypes` and exposes `from_buffer()` / `from_file()` |
| `probe.py`      | Public `probe()` and `probe_all()` functions |
| `result.py`     | `ProbeResult` dataclass |
| `__main__.py`   | CLI entry point |

---

## Development setup

```bash
git clone https://github.com/n7gj/magicprobe
cd magicprobe
pip install -e ".[dev]"
```

You also need the system libmagic library:

```bash
# macOS
brew install libmagic

# Debian / Ubuntu
apt install libmagic1
```

---

## Running the tests

```bash
pytest

# With coverage
pytest --cov
```

Tests that require a working libmagic installation are marked with
`@needs_libmagic` and are automatically skipped when the library is absent.

---

## Making a change

1. Fork the repository and create a feature branch.
2. Make your changes.
3. Add or update tests in `tests/` to cover the change.
4. Run `pytest` and confirm all tests pass.
5. Open a pull request.

---

## Pull request checklist

- [ ] All existing tests pass.
- [ ] New behaviour is covered by at least one test.
- [ ] No new runtime dependencies are introduced.
- [ ] Code follows the style guide below.

---

## Code style

- Python 3.10+ syntax.
- No external runtime dependencies — only the stdlib and the system libmagic C library.
- Public functions and classes must have docstrings.
- Line length ≤ 100 characters.
- Linting: `ruff check src/ tests/`

---

## Questions?

Open a [GitHub issue](https://github.com/n7gj/magicprobe/issues).
