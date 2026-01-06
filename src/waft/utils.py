"""
Utility functions - Helper functions for common operations.

These "little guys" help with repetitive tasks like path resolution,
file operations, formatting, and validation.
"""

from pathlib import Path
from typing import Optional


def resolve_project_path(path: Optional[str] = None) -> Path:
    """
    Resolve project path from optional string or default to current directory.

    Args:
        path: Optional path string. If None, uses current directory.

    Returns:
        Resolved Path object

    Raises:
        ValueError: If path doesn't exist or is not a directory
    """
    resolved = Path(path) if path else Path.cwd()

    # Validate path exists
    if not resolved.exists():
        raise ValueError(f"Path does not exist: {resolved}")

    # Validate path is a directory
    if not resolved.is_dir():
        raise ValueError(f"Path is not a directory: {resolved}")

    return resolved


def is_waft_project(path: Path) -> bool:
    """
    Check if a path is a Waft project (has _pyrite directory).

    Args:
        path: Path to check

    Returns:
        True if path is a Waft project, False otherwise
    """
    if not path.exists() or not path.is_dir():
        return False
    return (path / "_pyrite").exists()


def is_inside_waft_project(path: Path) -> tuple[bool, Optional[Path]]:
    """
    Check if a path is inside a Waft project.

    Args:
        path: Path to check

    Returns:
        Tuple of (is_inside, waft_project_path)
        - is_inside: True if path is inside a Waft project
        - waft_project_path: Path to the Waft project root, or None
    """
    current = path.resolve()

    # Walk up the directory tree looking for _pyrite
    for parent in [current] + list(current.parents):
        if is_waft_project(parent):
            return True, parent

    return False, None


def validate_project_name(name: str) -> tuple[bool, Optional[str]]:
    """
    Validate a project name.

    Args:
        name: Project name to validate

    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if name is valid
        - error_message: None if valid, error description if invalid
    """
    if not name:
        return False, "Project name cannot be empty"

    if len(name) > 100:
        return False, "Project name is too long (max 100 characters)"

    # Check for valid Python identifier (allowing hyphens and underscores)
    import re
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_-]*$', name):
        return False, "Project name must be a valid identifier (letters, numbers, hyphens, underscores only, starting with letter or underscore)"

    # Reserved names
    reserved = ['con', 'prn', 'aux', 'nul', 'com1', 'com2', 'com3', 'com4', 'com5', 'com6', 'com7', 'com8', 'com9', 'lpt1', 'lpt2', 'lpt3', 'lpt4', 'lpt5', 'lpt6', 'lpt7', 'lpt8', 'lpt9']
    if name.lower() in reserved:
        return False, f"Project name '{name}' is reserved"

    return True, None


def validate_package_name(package: str) -> tuple[bool, Optional[str]]:
    """
    Validate a package name for dependency addition.

    Args:
        package: Package name (may include version specifier)

    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if package name is valid
        - error_message: None if valid, error description if invalid
    """
    if not package:
        return False, "Package name cannot be empty"

    # Extract package name (before version specifiers)
    import re
    match = re.match(r'^([a-zA-Z0-9_-]+(?:\[[^\]]+\])?)', package)
    if not match:
        return False, "Invalid package name format"

    package_name = match.group(1)

    # Basic validation
    if len(package_name) > 200:
        return False, "Package name is too long"

    return True, None


def validate_waft_project(project_path: Path) -> tuple[bool, Optional[str]]:
    """
    Validate that a path is a Waft project.

    Args:
        project_path: Path to check

    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if valid Waft project
        - error_message: None if valid, error description if invalid
    """
    if not project_path.exists():
        return False, f"Path does not exist: {project_path}"

    if not project_path.is_dir():
        return False, f"Path is not a directory: {project_path}"

    pyrite_path = project_path / "_pyrite"
    if not pyrite_path.exists():
        return False, "Not a Waft project: _pyrite directory not found"

    pyproject_path = project_path / "pyproject.toml"
    if not pyproject_path.exists():
        return False, "Not a Python project: pyproject.toml not found"

    return True, None


def parse_toml_field(file_path: Path, field: str) -> Optional[str]:
    """
    Parse a simple field from a TOML file using regex.

    This is a lightweight alternative to full TOML parsing for simple cases.
    For complex TOML, use a proper TOML library.

    Args:
        file_path: Path to TOML file
        field: Field name to extract (e.g., "name", "version")

    Returns:
        Field value as string, or None if not found
    """
    if not file_path.exists():
        return None

    try:
        content = file_path.read_text()
        import re

        # Pattern: field = "value" or field = 'value'
        pattern = rf'{field}\s*=\s*["\']([^"\']+)["\']'
        match = re.search(pattern, content)
        if match:
            return match.group(1)
        return None
    except Exception:
        return None


def safe_read_file(file_path: Path, default: str = "") -> str:
    """
    Safely read a file, returning default if it doesn't exist or can't be read.

    Args:
        file_path: Path to file
        default: Default value to return on error

    Returns:
        File contents as string, or default if error
    """
    try:
        if file_path.exists() and file_path.is_file():
            return file_path.read_text()
        return default
    except Exception:
        return default


def safe_write_file(file_path: Path, content: str, create_dirs: bool = True) -> bool:
    """
    Safely write a file, creating directories if needed.

    Args:
        file_path: Path to file
        content: Content to write
        create_dirs: If True, create parent directories

    Returns:
        True if successful, False otherwise
    """
    try:
        if create_dirs:
            file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        return True
    except Exception:
        return False


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted string (e.g., "1.5 KB", "3.2 MB")
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def format_relative_path(path: Path, base: Path) -> str:
    """
    Format a path relative to a base path.

    Args:
        path: Path to format
        base: Base path

    Returns:
        Relative path string, or absolute if not relative
    """
    try:
        return str(path.relative_to(base))
    except ValueError:
        return str(path.resolve())


def ensure_directory(path: Path) -> None:
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        path: Directory path
    """
    path.mkdir(parents=True, exist_ok=True)


def get_file_metadata(file_path: Path) -> dict:
    """
    Get metadata about a file.

    Args:
        file_path: Path to file

    Returns:
        Dictionary with metadata:
        - exists: bool
        - size: int (bytes)
        - extension: str
        - name: str
        - modified: float (timestamp) or None
    """
    from datetime import datetime

    metadata = {
        "exists": file_path.exists(),
        "size": 0,
        "extension": file_path.suffix,
        "name": file_path.name,
        "modified": None,
    }

    if file_path.exists() and file_path.is_file():
        stat = file_path.stat()
        metadata["size"] = stat.st_size
        metadata["modified"] = stat.st_mtime

    return metadata


def filter_files_by_extension(files: list[Path], extension: str) -> list[Path]:
    """
    Filter a list of files by extension.

    Args:
        files: List of file paths
        extension: Extension to filter by (with or without leading dot)

    Returns:
        Filtered list of files
    """
    ext = extension if extension.startswith(".") else f".{extension}"
    return [f for f in files if f.suffix == ext]


def find_files_recursive(directory: Path, pattern: str = "*", exclude_dirs: Optional[list[str]] = None) -> list[Path]:
    """
    Find files recursively in a directory.

    Args:
        directory: Directory to search
        pattern: Glob pattern (default: "*")
        exclude_dirs: List of directory names to exclude (e.g., [".git", "__pycache__"])

    Returns:
        List of matching file paths
    """
    if not directory.exists():
        return []

    exclude_dirs = exclude_dirs or []
    files = []

    for item in directory.rglob(pattern):
        if item.is_file():
            # Check if any parent directory is excluded
            should_exclude = False
            for parent in item.parents:
                if parent.name in exclude_dirs:
                    should_exclude = True
                    break
            if not should_exclude:
                files.append(item)

    return files

