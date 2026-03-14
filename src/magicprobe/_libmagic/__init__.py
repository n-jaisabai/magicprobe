"""Internal libmagic integration package.

Exposes a single factory that returns a ready-to-use :class:`LibMagic`
instance.  Import from here rather than from the sub-modules directly.
"""
from ._wrapper import LibMagic

__all__ = ["LibMagic"]


def get_libmagic() -> LibMagic:
    """Return an initialised :class:`LibMagic` instance."""
    return LibMagic()
