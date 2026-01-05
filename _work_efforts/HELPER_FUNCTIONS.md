# Waft Framework: Helper Functions

**Created**: 2026-01-04
**Purpose**: Document utility functions and helper methods

---

## Overview

Waft includes a `utils.py` module with helper functions ("little guys") that simplify common operations throughout the codebase. These utilities reduce code duplication and provide consistent behavior.

---

## Available Helper Functions

### Path Utilities

#### `resolve_project_path(path: Optional[str] = None) -> Path`
Resolve project path from optional string or default to current directory.

**Usage:**
```python
from waft.utils import resolve_project_path

# Default to current directory
project_path = resolve_project_path()

# Use provided path
project_path = resolve_project_path("/path/to/project")
```

**Replaces:** `Path(path) if path else Path.cwd()` (used 7+ times)

---

#### `validate_waft_project(project_path: Path) -> tuple[bool, Optional[str]]`
Validate that a path is a Waft project.

**Returns:**
- `(True, None)` if valid
- `(False, error_message)` if invalid

**Usage:**
```python
from waft.utils import validate_waft_project

is_valid, error = validate_waft_project(project_path)
if not is_valid:
    print(f"Error: {error}")
```

**Checks:**
- Path exists and is a directory
- `_pyrite/` directory exists
- `pyproject.toml` exists

---

### File Utilities

#### `parse_toml_field(file_path: Path, field: str) -> Optional[str]`
Parse a simple field from a TOML file using regex.

**Usage:**
```python
from waft.utils import parse_toml_field

name = parse_toml_field(Path("pyproject.toml"), "name")
version = parse_toml_field(Path("pyproject.toml"), "version")
```

**Note:** For complex TOML parsing, use a proper TOML library. This is for simple cases.

---

#### `safe_read_file(file_path: Path, default: str = "") -> str`
Safely read a file, returning default if it doesn't exist or can't be read.

**Usage:**
```python
from waft.utils import safe_read_file

content = safe_read_file(Path("config.txt"), default="")
```

---

#### `safe_write_file(file_path: Path, content: str, create_dirs: bool = True) -> bool`
Safely write a file, creating directories if needed.

**Usage:**
```python
from waft.utils import safe_write_file

success = safe_write_file(Path("output/file.txt"), "content")
if not success:
    print("Failed to write file")
```

---

#### `get_file_metadata(file_path: Path) -> dict`
Get metadata about a file.

**Returns:**
```python
{
    "exists": bool,
    "size": int,  # bytes
    "extension": str,
    "name": str,
    "modified": float  # timestamp or None
}
```

**Usage:**
```python
from waft.utils import get_file_metadata

meta = get_file_metadata(Path("file.txt"))
print(f"Size: {meta['size']} bytes")
```

---

### Formatting Utilities

#### `format_file_size(size_bytes: int) -> str`
Format file size in human-readable format.

**Usage:**
```python
from waft.utils import format_file_size

print(format_file_size(1024))      # "1.0 KB"
print(format_file_size(1048576))   # "1.0 MB"
```

---

#### `format_relative_path(path: Path, base: Path) -> str`
Format a path relative to a base path.

**Usage:**
```python
from waft.utils import format_relative_path

rel = format_relative_path(Path("/a/b/c"), Path("/a"))
# Returns: "b/c"
```

---

### Directory Utilities

#### `ensure_directory(path: Path) -> None`
Ensure a directory exists, creating it if necessary.

**Usage:**
```python
from waft.utils import ensure_directory

ensure_directory(Path("output/subdir"))
```

---

### File Search Utilities

#### `filter_files_by_extension(files: list[Path], extension: str) -> list[Path]`
Filter a list of files by extension.

**Usage:**
```python
from waft.utils import filter_files_by_extension

all_files = [Path("a.txt"), Path("b.md"), Path("c.txt")]
txt_files = filter_files_by_extension(all_files, ".txt")
# Returns: [Path("a.txt"), Path("c.txt")]
```

---

#### `find_files_recursive(directory: Path, pattern: str = "*", exclude_dirs: Optional[list[str]] = None) -> list[Path]`
Find files recursively in a directory.

**Usage:**
```python
from waft.utils import find_files_recursive

# Find all markdown files
md_files = find_files_recursive(Path("."), "*.md")

# Exclude certain directories
files = find_files_recursive(
    Path("."),
    exclude_dirs=[".git", "__pycache__", ".venv"]
)
```

---

## Integration Examples

### Before (Repetitive)
```python
# In main.py
project_path = Path(path) if path else Path.cwd()

# In another command
project_path = Path(path) if path else Path.cwd()

# In substrate.py
content = pyproject_path.read_text()
import re
name_match = re.search(r'name\s*=\s*["\']([^"\']+)["\']', content)
```

### After (Using Helpers)
```python
# In main.py
from .utils import resolve_project_path, parse_toml_field

project_path = resolve_project_path(path)

# In substrate.py
from ..utils import parse_toml_field

name = parse_toml_field(pyproject_path, "name")
```

---

## Benefits

1. **Reduced Duplication**: Common patterns extracted to single functions
2. **Consistency**: Same behavior across all commands
3. **Maintainability**: Fix bugs in one place
4. **Readability**: Clear function names express intent
5. **Testability**: Utilities can be tested independently

---

## Usage in Codebase

### Commands Using Helpers

- ✅ `waft verify` - Uses `resolve_project_path()`
- ✅ `waft info` - Uses `resolve_project_path()`
- ✅ `waft serve` - Uses `resolve_project_path()` and `validate_waft_project()`

### Managers Using Helpers

- ✅ `SubstrateManager.get_project_info()` - Uses `parse_toml_field()`

---

## Future Enhancements

Potential additions:
- `format_duration(seconds: float) -> str` - Human-readable durations
- `parse_markdown_frontmatter(content: str) -> dict` - Extract YAML frontmatter
- `validate_python_version(version: str) -> bool` - Validate Python version strings
- `slugify(text: str) -> str` - Convert text to URL-safe slug
- `truncate_text(text: str, max_length: int) -> str` - Truncate with ellipsis

---

## Summary

The `utils.py` module provides **12 helper functions** covering:
- ✅ Path resolution and validation
- ✅ File operations (read, write, metadata)
- ✅ TOML parsing (simple cases)
- ✅ Formatting (file sizes, paths)
- ✅ File searching and filtering

These utilities reduce code duplication by **7+ occurrences** of common patterns and make the codebase more maintainable.

