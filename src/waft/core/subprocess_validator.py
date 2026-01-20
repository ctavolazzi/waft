"""
Centralized subprocess input validation.

Validates external input before passing it into subprocess calls.
"""

from ..utils import validate_package_name, validate_project_name


def validate_project_name_arg(name: str) -> str:
    is_valid, error = validate_project_name(name)
    if not is_valid:
        raise ValueError(error or "Invalid project name")
    return name


def validate_package_name_arg(package: str) -> str:
    is_valid, error = validate_package_name(package)
    if not is_valid:
        raise ValueError(error or "Invalid package name")
    return package


def validate_free_text(value: str, field_name: str = "text", max_length: int = 10000) -> str:
    if not value or not value.strip():
        raise ValueError(f"{field_name} cannot be empty")
    if len(value) > max_length:
        raise ValueError(f"{field_name} exceeds {max_length} characters")
    if "\x00" in value:
        raise ValueError(f"{field_name} contains invalid characters")
    if any(ord(c) < 32 and c not in ["\n", "\t", "\r"] for c in value):
        raise ValueError(f"{field_name} contains control characters")
    return value
