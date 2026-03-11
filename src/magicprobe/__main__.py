"""Command-line interface for magicprobe.

Usage::

    magicprobe <file> [<file> ...]
    python -m magicprobe <file> [<file> ...]
"""

from __future__ import annotations

import sys

from .probe import probe


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: magicprobe <file> [<file> ...]", file=sys.stderr)
        sys.exit(1)

    exit_code = 0
    for path in sys.argv[1:]:
        result = probe(path)
        if result:
            exts = ", ".join(result.extensions) if result.extensions else "—"
            print(f"{path}: {result.name} ({result.mime_type})  [{exts}]")
        else:
            print(f"{path}: unknown")
            exit_code = 1

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
