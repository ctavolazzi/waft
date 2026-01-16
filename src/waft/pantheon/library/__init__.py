"""
Library Realm
=============

The Library Realm is a bounded space where the Librarian God presides
and the Scribe writes all Pantheon records.

Following "as above, so below" principles:
- As above: Celestial library organizing all knowledge
- So below: File-based system cataloging all Pantheon records
"""

from .librarian import Librarian
from .scribe import Scribe
from .record_catalog import RecordCatalog, RecordEntry

__all__ = [
    "Librarian",
    "Scribe",
    "RecordCatalog",
    "RecordEntry",
]
