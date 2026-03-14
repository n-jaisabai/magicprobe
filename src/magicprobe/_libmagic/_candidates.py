"""Platform-specific libmagic library discovery.

Each ``_candidates_*`` function yields candidate paths / names for its
platform.  ``all_candidates()`` is the single entry-point used by the loader.
"""
from __future__ import annotations

import glob
import os
import sys
from ctypes.util import find_library
from typing import Iterator, Optional

INSTALL_HINT = (
    "  macOS  : brew install libmagic\n"
    "  Debian : apt install libmagic1\n"
    "  Fedora : dnf install file-libs\n"
    "  Windows: pip install python-magic-bin"
)


def _candidates_linux() -> Iterator[str]:
    yield "libmagic.so.1"                                  # resolved via ld.so cache
    yield "/usr/lib/x86_64-linux-gnu/libmagic.so.1"        # Debian/Ubuntu amd64
    yield "/usr/lib/aarch64-linux-gnu/libmagic.so.1"       # Debian/Ubuntu arm64
    yield "/usr/lib/arm-linux-gnueabihf/libmagic.so.1"     # Debian/Ubuntu armhf
    yield "/usr/lib64/libmagic.so.1"                       # RHEL/Fedora/CentOS
    yield "/usr/lib/libmagic.so.1"                         # generic
    yield "/usr/lib/libmagic.so"                           # Alpine / musl
    yield "/usr/local/lib/libmagic.so"                     # FreeBSD/OpenBSD
    yield "/nix/var/nix/profiles/default/lib/libmagic.so"  # Nix


def _candidates_macos() -> Iterator[str]:
    dirs = [
        "/opt/homebrew/lib",  # Homebrew (Apple silicon)
        "/opt/local/lib",     # MacPorts
        "/usr/local/lib",     # Homebrew (Intel)
        *glob.glob("/usr/local/Cellar/libmagic/*/lib"),  # versioned Cellar paths
    ]
    for d in dirs:
        yield os.path.join(d, "libmagic.dylib")


def _candidates_windows() -> Iterator[Optional[str]]:
    # GnuWin32, Cygwin, MSYS2, vcpkg variants
    prefixes = ("libmagic", "magic1", "magic-1", "cygmagic-1", "libmagic-1", "msys-magic-1")
    for prefix in prefixes:
        yield f"./{prefix}.dll"    # current directory (find_library skips it)
        yield find_library(prefix)  # searches PATH / registry


_PLATFORM_CANDIDATES = {
    "linux":  _candidates_linux,
    "darwin": _candidates_macos,
    "win32":  _candidates_windows,
    "cygwin": _candidates_windows,
    "sunos5": _candidates_linux,
}


def all_candidates() -> Iterator[Optional[str]]:
    """Yield every library candidate to try, starting with the generic lookup."""
    yield find_library("magic")  # works on most systems when ldconfig is configured

    platform_func = _PLATFORM_CANDIDATES.get(sys.platform)
    if platform_func is None:
        raise ImportError(f"magicprobe: unsupported platform: {sys.platform}")
    yield from platform_func()
