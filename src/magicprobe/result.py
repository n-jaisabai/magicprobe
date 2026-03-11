from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProbeResult:
    """Immutable result of a file-type probe operation."""

    name: str
    """Human-readable type name, e.g. ``"PNG"``."""

    mime_type: str
    """IANA MIME type string, e.g. ``"image/png"``."""

    extensions: tuple[str, ...]
    """Tuple of common file extensions, e.g. ``(".png",)``."""

    @property
    def extension(self) -> str | None:
        """Primary file extension, or ``None`` if unknown."""
        return self.extensions[0] if self.extensions else None

    def __repr__(self) -> str:
        return f"ProbeResult(name={self.name!r}, mime_type={self.mime_type!r})"
