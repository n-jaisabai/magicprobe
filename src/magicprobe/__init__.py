"""magicprobe — Detect file types by magic bytes."""

from .probe import probe, probe_all
from .result import ProbeResult
from . import types as _types  # noqa: F401 — ensure all type modules are imported & registered

__version__ = "0.1.0"
__all__ = ["probe", "probe_all", "ProbeResult"]
