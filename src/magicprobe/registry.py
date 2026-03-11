"""Global file-type registry.

Every :class:`~magicprobe.types.base.FileType` subclass decorated with
:func:`register` is stored here.  The registry is populated at import time
when the ``magicprobe.types`` sub-package is loaded.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .types.base import FileType

_registry: list[type[FileType]] = []


def register(cls: type[FileType]) -> type[FileType]:
    """Class decorator — add *cls* to the global type registry.

    Usage::

        from magicprobe.registry import register
        from magicprobe.types.base import FileType

        @register
        class MyType(FileType):
            ...
    """
    _registry.append(cls)
    return cls


def get_all() -> list[type[FileType]]:
    """Return a snapshot of all registered :class:`FileType` classes."""
    return list(_registry)
