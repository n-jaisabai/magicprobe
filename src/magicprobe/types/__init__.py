"""File-type definitions sub-package.

Importing this package registers all built-in types with the global registry
in the order listed below.  **Order matters** — for ``probe()`` the first
registered type whose ``match()`` returns ``True`` wins.  More specific
types (e.g. EPUB, OOXML) are imported before the generic types they build on
(e.g. ZIP).
"""

from . import image, document, archive, audio, video, executable

__all__ = ["image", "document", "archive", "audio", "video", "executable"]
