"""
WAFT Version Monitoring System

Epoch-based versioning with quarterly checkpoints.
Epoch: January 4, 2026 @ 4:19:05 PM (first commit)

Version Format: v{Years}.{Months}.{Days}.{Hour}.{Quarter}
"""

from .calculator import (
    EPOCH,
    EPOCH_COMMIT,
    EPOCH_ISO,
    Version,
    calculate_version,
    current_version,
    version_string,
    get_quarter_boundaries,
    time_until_next_quarter,
    format_countdown,
    days_since_epoch,
)

from .schema import (
    Checkpoint,
    VersionState,
    VersionManifest,
    VersionManager,
)

__all__ = [
    # Calculator
    "EPOCH",
    "EPOCH_COMMIT",
    "EPOCH_ISO",
    "Version",
    "calculate_version",
    "current_version",
    "version_string",
    "get_quarter_boundaries",
    "time_until_next_quarter",
    "format_countdown",
    "days_since_epoch",
    # Schema
    "Checkpoint",
    "VersionState",
    "VersionManifest",
    "VersionManager",
]
