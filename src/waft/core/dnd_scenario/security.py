"""
Security utilities for DnD Scenario system.

Provides path validation, input validation, and security checks.
"""

import re
from pathlib import Path

# Constants for validation
EXPERIMENT_ID_PATTERN = re.compile(r"^[a-zA-Z0-9_-]+$")
MAX_EXPERIMENT_ID_LENGTH = 64
MIN_ITERATION = 1
MAX_ITERATION = 10000


def validate_realm_path(realm_path: Path, expected_base: Path) -> bool:
    """
    Validate realm_path is safe and within expected base.

    CRITICAL: Security validation to prevent path traversal attacks.
    Uses the same pattern as RealmColonizationSystem._validate_realm_path()

    Args:
        realm_path: Path to validate
        expected_base: Expected base directory

    Returns:
        True if valid, False otherwise
    """
    try:
        resolved = realm_path.resolve()
        base_resolved = expected_base.resolve()

        # Must be within base
        if not str(resolved).startswith(str(base_resolved)):
            return False

        # Check for symlinks
        if resolved.is_symlink():
            return False

        # Check path components for traversal
        for part in realm_path.parts:
            if part == "..":
                return False

        # Check for null bytes
        if "\x00" in str(realm_path):
            return False

        return True
    except (OSError, ValueError):
        return False


def validate_experiment_id(experiment_id: str) -> tuple[bool, str | None]:
    """
    Validate experiment ID format.

    Args:
        experiment_id: Experiment ID to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(experiment_id, str):
        return False, "Experiment ID must be a string"

    if len(experiment_id) == 0:
        return False, "Experiment ID cannot be empty"

    if len(experiment_id) > MAX_EXPERIMENT_ID_LENGTH:
        return (
            False,
            f"Experiment ID exceeds maximum length of {MAX_EXPERIMENT_ID_LENGTH} characters",
        )

    if not EXPERIMENT_ID_PATTERN.match(experiment_id):
        return (
            False,
            "Experiment ID can only contain alphanumeric characters, underscores, and hyphens",
        )

    return True, None


def sanitize_experiment_id(experiment_id: str) -> str:
    """
    Sanitize experiment ID to safe format.

    Args:
        experiment_id: Experiment ID to sanitize

    Returns:
        Sanitized experiment ID
    """
    # Remove any invalid characters
    sanitized = re.sub(r"[^a-zA-Z0-9_-]", "", experiment_id)

    # Truncate to max length
    if len(sanitized) > MAX_EXPERIMENT_ID_LENGTH:
        sanitized = sanitized[:MAX_EXPERIMENT_ID_LENGTH]

    return sanitized


def validate_iteration(iteration: int) -> tuple[bool, str | None]:
    """
    Validate iteration number.

    Args:
        iteration: Iteration number to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(iteration, int):
        return False, "Iteration must be an integer"

    if iteration < MIN_ITERATION:
        return False, f"Iteration must be at least {MIN_ITERATION}"

    if iteration > MAX_ITERATION:
        return False, f"Iteration cannot exceed {MAX_ITERATION}"

    return True, None
