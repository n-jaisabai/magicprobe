"""magicprobe — Detect file types by magic bytes."""

from .probe import probe, probe_all
from .result import ProbeResult

__version__ = "0.1.0"
__all__ = ["probe", "probe_all", "ProbeResult"]
