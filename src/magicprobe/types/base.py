"""Base class for all file-type definitions."""

from __future__ import annotations

from abc import ABC, abstractmethod


class FileType(ABC):
    """Abstract base class for a file-type detector.

    To add a new file type, subclass ``FileType``, decorate it with
    :func:`~magicprobe.registry.register`, and set the three class
    attributes below.  See :ref:`contributing` for a full walk-through.

    Attributes:
        name:       Human-readable name, e.g. ``"PNG"``.
        mime_type:  IANA MIME type, e.g. ``"image/png"``.
        extensions: List of conventional extensions, e.g. ``[".png"]``.
                    Use ``[""]`` for formats without a fixed extension.
    """

    name: str
    mime_type: str
    extensions: list[str]

    @classmethod
    @abstractmethod
    def match(cls, data: bytes) -> bool:
        """Return ``True`` if *data* starts with this type's magic signature.

        Args:
            data: Up to 262 bytes read from the beginning of the file.
        """
        ...
