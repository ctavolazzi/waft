# Waft Framework: Data Traversal Guide

**Created**: 2026-01-04
**Purpose**: Document how to traverse and navigate waft's data structures

---

## Overview

Waft's file-based data model can be traversed through multiple methods:
1. **Programmatic API** - Using `MemoryManager` and `SubstrateManager`
2. **Direct File System** - Standard Python `pathlib` operations
3. **CLI Commands** - `waft info` and `waft serve`
4. **Web Dashboard** - HTTP API endpoints

---

## Current Traversal Methods

### 1. MemoryManager API

#### List Files by Category

```python
from pathlib import Path
from waft.core.memory import MemoryManager

project_path = Path(".")
memory = MemoryManager(project_path)

# Get all files in active/
active_files = memory.get_active_files()
# Returns: [Path('_pyrite/active/file1.md'), Path('_pyrite/active/file2.txt'), ...]

# Get all files in backlog/
backlog_files = memory.get_backlog_files()
# Returns: [Path('_pyrite/backlog/idea1.md'), ...]

# Get all files in standards/
standards_files = memory.get_standards_files()
# Returns: [Path('_pyrite/standards/coding-standards.md'), ...]
```

#### Verify Structure

```python
status = memory.verify_structure()
# Returns: {
#     "valid": True/False,
#     "folders": {
#         "_pyrite/active": True/False,
#         "_pyrite/backlog": True/False,
#         "_pyrite/standards": True/False
#     }
# }
```

### 2. SubstrateManager API

#### Get Project Information

```python
from waft.core.substrate import SubstrateManager

substrate = SubstrateManager()
info = substrate.get_project_info(project_path)
# Returns: {"name": "my-project", "version": "0.1.0"}
```

#### Check Lock File

```python
has_lock = substrate.verify_lock(project_path)
# Returns: True/False
```

### 3. Direct File System Traversal

#### Using pathlib (Recommended)

```python
from pathlib import Path

project_path = Path(".")
pyrite_path = project_path / "_pyrite"

# List all files recursively
all_files = list(pyrite_path.rglob("*"))
# Returns: [Path('_pyrite/active/.gitkeep'), Path('_pyrite/active/file1.md'), ...]

# List only markdown files
md_files = list(pyrite_path.rglob("*.md"))
# Returns: [Path('_pyrite/active/file1.md'), ...]

# List only files (exclude directories)
files_only = [f for f in pyrite_path.rglob("*") if f.is_file()]
```

#### Using os.walk (Alternative)

```python
import os
from pathlib import Path

pyrite_path = Path("_pyrite")
for root, dirs, files in os.walk(pyrite_path):
    for file in files:
        file_path = Path(root) / file
        print(file_path)
```

### 4. CLI Traversal

#### `waft info` Command

```bash
waft info
# Shows:
# - Project path
# - Project name and version
# - _pyrite structure status
# - uv.lock status
# - Templates present
```

#### `waft serve` Web Dashboard

```bash
waft serve --port 8000
# Access at http://localhost:8000
# Provides:
# - Visual project overview
# - File listings
# - JSON API endpoints
```

### 5. Web API Endpoints

#### GET `/api/info`

```bash
curl http://localhost:8000/api/info
```

Returns:
```json
{
  "project_path": "/path/to/project",
  "project_name": "my-project",
  "version": "0.1.0",
  "pyrite_structure": {
    "valid": true,
    "folders": {
      "_pyrite/active": true,
      "_pyrite/backlog": true,
      "_pyrite/standards": true
    }
  },
  "uv_lock": true,
  "templates": {
    "justfile": true,
    "ci": true,
    "agents": false,
    "gitignore": true,
    "readme": true
  }
}
```

#### GET `/api/structure`

```bash
curl http://localhost:8000/api/structure
```

Returns:
```json
{
  "active": ["file1.md", "file2.txt"],
  "backlog": ["idea1.md"],
  "standards": ["coding-standards.md"]
}
```

---

## Traversal Patterns

### Pattern 1: Iterate All Files

```python
from pathlib import Path
from waft.core.memory import MemoryManager

memory = MemoryManager(Path("."))

# Get all files across all categories
all_files = (
    memory.get_active_files() +
    memory.get_backlog_files() +
    memory.get_standards_files()
)

for file_path in all_files:
    print(f"File: {file_path.name}")
    content = file_path.read_text()
    # Process content...
```

### Pattern 2: Search by Content

```python
from pathlib import Path

def search_pyrite_content(query: str, project_path: Path) -> list[Path]:
    """Search for query string in all _pyrite files."""
    pyrite_path = project_path / "_pyrite"
    matches = []

    for file_path in pyrite_path.rglob("*.md"):
        if file_path.is_file() and file_path.name != ".gitkeep":
            content = file_path.read_text()
            if query.lower() in content.lower():
                matches.append(file_path)

    return matches

# Usage
results = search_pyrite_content("TODO", Path("."))
```

### Pattern 3: Filter by Extension

```python
from pathlib import Path
from waft.core.memory import MemoryManager

memory = MemoryManager(Path("."))

def get_markdown_files(memory: MemoryManager) -> list[Path]:
    """Get all markdown files from _pyrite."""
    all_files = (
        memory.get_active_files() +
        memory.get_backlog_files() +
        memory.get_standards_files()
    )
    return [f for f in all_files if f.suffix == ".md"]

md_files = get_markdown_files(memory)
```

### Pattern 4: Group by Category

```python
from pathlib import Path
from waft.core.memory import MemoryManager

memory = MemoryManager(Path("."))

structure = {
    "active": memory.get_active_files(),
    "backlog": memory.get_backlog_files(),
    "standards": memory.get_standards_files(),
}

for category, files in structure.items():
    print(f"{category}: {len(files)} files")
    for file in files:
        print(f"  - {file.name}")
```

### Pattern 5: Read and Process Content

```python
from pathlib import Path
from waft.core.memory import MemoryManager

memory = MemoryManager(Path("."))

def process_file(file_path: Path) -> dict:
    """Read and extract metadata from a file."""
    content = file_path.read_text()
    return {
        "path": str(file_path),
        "name": file_path.name,
        "size": len(content),
        "lines": len(content.splitlines()),
        "preview": content[:100] + "..." if len(content) > 100 else content,
    }

# Process all active files
for file_path in memory.get_active_files():
    info = process_file(file_path)
    print(f"{info['name']}: {info['lines']} lines")
```

---

## Advanced Traversal

### Recursive Directory Walk

```python
from pathlib import Path

def walk_pyrite(project_path: Path) -> dict:
    """Recursively walk _pyrite structure."""
    pyrite_path = project_path / "_pyrite"
    structure = {}

    for item in pyrite_path.rglob("*"):
        if item.is_file():
            rel_path = item.relative_to(pyrite_path)
            parts = rel_path.parts
            category = parts[0] if parts else "root"

            if category not in structure:
                structure[category] = []

            structure[category].append({
                "path": str(rel_path),
                "name": item.name,
                "size": item.stat().st_size,
            })

    return structure
```

### Search with Metadata

```python
from pathlib import Path
from datetime import datetime

def get_file_metadata(file_path: Path) -> dict:
    """Get comprehensive file metadata."""
    stat = file_path.stat()
    return {
        "path": str(file_path),
        "name": file_path.name,
        "size": stat.st_size,
        "modified": datetime.fromtimestamp(stat.st_mtime),
        "created": datetime.fromtimestamp(stat.st_ctime),
        "extension": file_path.suffix,
    }

# Get metadata for all files
memory = MemoryManager(Path("."))
all_files = (
    memory.get_active_files() +
    memory.get_backlog_files() +
    memory.get_standards_files()
)

metadata = [get_file_metadata(f) for f in all_files]
```

### Filter and Sort

```python
from pathlib import Path
from waft.core.memory import MemoryManager

memory = MemoryManager(Path("."))

# Get all markdown files, sorted by modification time
all_files = (
    memory.get_active_files() +
    memory.get_backlog_files() +
    memory.get_standards_files()
)

md_files = [f for f in all_files if f.suffix == ".md"]
md_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)

# Most recently modified first
for file in md_files:
    print(file.name)
```

---

## Traversal Limitations

### Current Limitations

1. **No recursive subdirectories**: `MemoryManager` only lists files directly in `active/`, `backlog/`, `standards/` - not subdirectories
2. **No content indexing**: No built-in search across file contents
3. **No filtering**: No built-in methods to filter by extension, date, size, etc.
4. **No metadata extraction**: No automatic parsing of frontmatter or structured data

### Workarounds

- Use `pathlib.Path.rglob()` for recursive traversal
- Implement custom search functions (see patterns above)
- Use external tools (grep, ripgrep) for content search
- Parse files manually for structured data

---

## Future Enhancements

### Potential Additions

1. **Recursive traversal methods**:
   ```python
   memory.get_all_files(recursive=True)
   memory.get_files_by_extension(".md")
   ```

2. **Content search**:
   ```python
   memory.search_content("TODO")
   memory.search_regex(r"\[.*\]")
   ```

3. **Metadata extraction**:
   ```python
   memory.get_file_metadata(file_path)
   memory.get_all_metadata()
   ```

4. **Filtering and sorting**:
   ```python
   memory.get_files(filter_by={"extension": ".md", "min_size": 100})
   memory.get_files(sort_by="modified", reverse=True)
   ```

---

## Examples

### Example 1: List All Project Files

```python
from pathlib import Path
from waft.core.memory import MemoryManager

memory = MemoryManager(Path("."))

print("Active Files:")
for f in memory.get_active_files():
    print(f"  - {f.name}")

print("\nBacklog Files:")
for f in memory.get_backlog_files():
    print(f"  - {f.name}")

print("\nStandards Files:")
for f in memory.get_standards_files():
    print(f"  - {f.name}")
```

### Example 2: Find All TODOs

```python
from pathlib import Path

def find_todos(project_path: Path) -> list[dict]:
    """Find all TODO comments in _pyrite files."""
    pyrite_path = project_path / "_pyrite"
    todos = []

    for file_path in pyrite_path.rglob("*.md"):
        if file_path.is_file():
            content = file_path.read_text()
            lines = content.splitlines()

            for line_num, line in enumerate(lines, 1):
                if "TODO" in line.upper() or "FIXME" in line.upper():
                    todos.append({
                        "file": str(file_path.relative_to(project_path)),
                        "line": line_num,
                        "content": line.strip(),
                    })

    return todos

# Usage
todos = find_todos(Path("."))
for todo in todos:
    print(f"{todo['file']}:{todo['line']} - {todo['content']}")
```

### Example 3: Generate File Index

```python
from pathlib import Path
from waft.core.memory import MemoryManager
from datetime import datetime

def generate_index(project_path: Path) -> str:
    """Generate a markdown index of all _pyrite files."""
    memory = MemoryManager(project_path)

    index_lines = ["# _pyrite File Index\n", f"Generated: {datetime.now()}\n\n"]

    categories = {
        "Active": memory.get_active_files(),
        "Backlog": memory.get_backlog_files(),
        "Standards": memory.get_standards_files(),
    }

    for category, files in categories.items():
        index_lines.append(f"## {category} ({len(files)} files)\n\n")
        for file in sorted(files):
            rel_path = file.relative_to(project_path)
            index_lines.append(f"- [{file.name}]({rel_path})\n")
        index_lines.append("\n")

    return "".join(index_lines)

# Usage
index = generate_index(Path("."))
print(index)
```

---

## Summary

**Current Traversal Methods:**
- ✅ List files by category (`get_active_files()`, etc.)
- ✅ Verify structure (`verify_structure()`)
- ✅ Get project info (`get_project_info()`)
- ✅ Direct file system access (`pathlib`)

**Common Patterns:**
- Iterate all files across categories
- Search content with custom functions
- Filter by extension or other criteria
- Group files by category
- Extract metadata manually

**Best Practices:**
- Use `MemoryManager` API for structured access
- Use `pathlib.Path.rglob()` for recursive traversal
- Implement custom search/filter functions as needed
- Combine API methods with direct file operations for flexibility

