"""waft.record: the Logbook, a hash-chained, content-addressed record of a run.

Every claim a run makes is a record. Each record carries the hash of the one before it, stored outputs are
named by their own SHA-256, and `verify` re-derives all of it. The last record's hash (the head) is the one
string to publish: a run that verifies against a head published elsewhere has not been edited since.

Vendored, unchanged, from the FogSift system (ctavolazzi/_workbench, fogsift-system/, commit
a26696601375, copied 2026-11-14):

    custody.py        the Logbook and the Python verifier (standard library only)
    schemas.py        the record schemas and the small validator that applies them
    schemas/*.json    the same schemas, exported for verifiers in other languages
    node/verify.mjs   a second verifier written from CUSTODY.md alone; it shares no code with custody.py
    CUSTODY.md        the specification both verifiers implement

Keep these files identical to their source so they can be re-synced; WAFT-specific code lives in waft.lab.
"""

from .custody import (
    ExecResult,
    Logbook,
    LogbookError,
    VerifyReport,
    canon,
    dec,
    plainify,
    rule_r1,
    sha256,
    verify,
)
from .schemas import all_schemas, validate

__all__ = [
    "ExecResult",
    "Logbook",
    "LogbookError",
    "VerifyReport",
    "all_schemas",
    "canon",
    "dec",
    "plainify",
    "rule_r1",
    "sha256",
    "validate",
    "verify",
]
