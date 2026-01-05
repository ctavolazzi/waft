# Waft Framework: Data Shape and Structure

**Created**: 2026-01-04
**Purpose**: Visualize and document the actual shape/structure of data in waft

---

## Data Shape Overview

Waft data has a **hierarchical, file-based structure** with **no rigid schema**. Data is organized in directories and files, with different formats for different purposes.

---

## 1. _pyrite/ Structure (Memory Layer)

### Directory Shape
```
_pyrite/
├── active/          ← Flat file collection
│   ├── .gitkeep    ← Metadata file
│   └── *.md        ← User content files
├── backlog/        ← Flat file collection
│   ├── .gitkeep
│   └── *.md
└── standards/      ← Flat file collection
    ├── .gitkeep
    └── *.md
```

### Data Shape Characteristics
- **Structure**: Flat directory (no nesting)
- **Format**: Plain text files (typically Markdown)
- **Schema**: None (user-defined content)
- **Organization**: File-based (one concept per file)

### Example Data Shape

#### Empty State
```json
{
  "active": [],
  "backlog": [],
  "standards": []
}
```

#### With Content
```json
{
  "active": [
    "current-task.md",
    "work-in-progress.txt"
  ],
  "backlog": [
    "future-feature.md",
    "ideas.md"
  ],
  "standards": [
    "coding-standards.md",
    "project-guidelines.md"
  ]
}
```

### File Content Shape

#### Example: `_pyrite/active/test.md`
```markdown
# Test file
```

**Shape**:
- **Type**: Plain text
- **Format**: Markdown (convention, not enforced)
- **Structure**: Free-form
- **Size**: Variable (user-defined)

---

## 2. pyproject.toml Structure (Configuration)

### Data Shape
```toml
[project]
name = "string"              ← String value
version = "string"           ← String value
description = "string"       ← String value
requires-python = "string"   ← String constraint
dependencies = [             ← Array of strings
    "package>=version",
]
```

### Actual Example
```toml
[project]
name = "test-project-001"
version = "0.1.0"
description = "Add your description here"
requires-python = ">=3.10"
dependencies = []
```

### Shape Characteristics
- **Format**: TOML (structured)
- **Schema**: Defined by Python packaging standards
- **Structure**: Nested key-value pairs
- **Types**: Strings, arrays, tables

### Extracted Shape (via API)
```json
{
  "name": "test-project-001",
  "version": "0.1.0"
}
```

---

## 3. uv.lock Structure (Dependencies)

### Data Shape
```toml
version = 1                  ← Integer
revision = 1                 ← Integer
requires-python = "string"   ← String

[[package]]                  ← Array of package objects
name = "string"
version = "string"
source = { ... }             ← Nested object
dependencies = [ ... ]       ← Array
```

### Actual Example (excerpt)
```toml
version = 1
revision = 1
requires-python = ">=3.10"

[[package]]
name = "aiohappyeyeballs"
version = "2.6.1"
source = { registry = "https://pypi.org/simple" }
dependencies = []
```

### Shape Characteristics
- **Format**: TOML (complex nested structure)
- **Schema**: Defined by `uv` lock file format
- **Structure**: Array of package objects
- **Size**: Large (716KB for waft project)
- **Read-only**: Generated, not edited

---

## 4. Work Efforts Structure (_work_efforts/)

### Directory Shape
```
_work_efforts/
├── devlog.md                           ← Flat markdown
├── WE-YYYYMMDD-xxxx_index.md          ← YAML frontmatter + Markdown
└── WE-YYYYMMDD-xxxx_work_name/
    ├── WE-YYYYMMDD-xxxx_index.md      ← YAML frontmatter + Markdown
    └── tickets/
        └── TKT-xxxx-NNN_ticket.md     ← YAML frontmatter + Markdown
```

### Work Effort Index Shape

#### File Structure
```yaml
---                                    ← YAML frontmatter (metadata)
id: WE-260104-bk5z
title: "Development Environment Setup"
status: completed
created: 2026-01-05T07:55:51.589Z
created_by: ctavolazzi
last_updated: 2026-01-05T07:56:21.460Z
branch: feature/WE-260104-bk5z-...
repository: waft
---                                    ← End frontmatter

# Markdown content (free-form)
## Objective
...

## Tickets
| ID | Title | Status |
...
```

#### Extracted Shape
```json
{
  "id": "WE-260104-bk5z",
  "title": "Development Environment Setup",
  "status": "completed",
  "created": "2026-01-05T07:55:51.589Z",
  "created_by": "ctavolazzi",
  "last_updated": "2026-01-05T07:56:21.460Z",
  "branch": "feature/WE-260104-bk5z-...",
  "repository": "waft",
  "content": "# Markdown content..."
}
```

### Ticket Shape

#### File Structure
```yaml
---
id: TKT-bk5z-001
parent: WE-260104-bk5z
title: "Fix crewai dependency..."
status: completed
created: 2026-01-05T07:55:51.694Z
created_by: ctavolazzi
assigned_to: null
---

# Markdown content
## Description
...
```

#### Extracted Shape
```json
{
  "id": "TKT-bk5z-001",
  "parent": "WE-260104-bk5z",
  "title": "Fix crewai dependency...",
  "status": "completed",
  "created": "2026-01-05T07:55:51.694Z",
  "created_by": "ctavolazzi",
  "assigned_to": null,
  "content": "# Markdown content..."
}
```

### Devlog Shape

#### File Structure
```markdown
# Development Log

---

## 2026-01-04 - Title

**Work Effort:** WE-xxxx-xxxx

### Summary
...

### Completed Tasks
1. **Task name**
   - Details
...
```

**Shape**:
- **Format**: Pure Markdown (no frontmatter)
- **Structure**: Date-based sections
- **Schema**: None (free-form)
- **Organization**: Chronological

---

## 5. API Response Shapes

### Project Info Shape (`waft info` / API)
```json
{
  "project_path": "/absolute/path/to/project",
  "project_name": "waft",
  "version": "0.0.1",
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
    "agents": true,
    "gitignore": true,
    "readme": true
  }
}
```

### Memory Structure Shape (`/api/structure`)
```json
{
  "active": [
    "test.md",
    "current-work.md"
  ],
  "backlog": [
    "future-idea.md"
  ],
  "standards": [
    "coding-standards.md"
  ]
}
```

### Verification Shape (`waft verify`)
```json
{
  "valid": true,
  "folders": {
    "_pyrite/active": true,
    "_pyrite/backlog": true,
    "_pyrite/standards": true
  }
}
```

---

## Data Type Summary

| Data Type | Format | Schema | Structure | Example |
|-----------|--------|--------|-----------|---------|
| **_pyrite files** | Markdown/Text | None | Flat files | `# Title\nContent` |
| **pyproject.toml** | TOML | Defined | Nested KV | `name = "project"` |
| **uv.lock** | TOML | Defined | Array of objects | `[[package]]` |
| **Work Efforts** | YAML+MD | Partial | Frontmatter+MD | `---\nid: WE-...` |
| **Devlog** | Markdown | None | Sections | `## Date - Title` |

---

## Data Relationships

### Implicit Relationships
```
Project Root
  ├── _pyrite/          ← Independent (user-managed)
  ├── pyproject.toml    ← Referenced by SubstrateManager
  ├── uv.lock           ← Generated from pyproject.toml
  └── _work_efforts/    ← Independent (framework internal)
```

### No Explicit Relationships
- ❌ No foreign keys
- ❌ No references between files
- ❌ No linking system
- ❌ No graph structure

### Implicit Connections
- Files in same directory = related by location
- Work effort → Tickets (via `parent` field in frontmatter)
- Project → Dependencies (via `pyproject.toml`)

---

## Data Size Characteristics

### Typical Sizes
- **`.gitkeep` files**: ~50 bytes
- **`pyproject.toml`**: ~1-5 KB
- **`uv.lock`**: 100KB - 1MB (depends on dependencies)
- **`_pyrite/` files**: Variable (user content)
- **Work effort files**: 1-5 KB each

### Current Waft Project
- `_pyrite/`: 12 KB (structure only)
- `_work_efforts/`: 116 KB (documentation)
- `uv.lock`: 716 KB (dependencies)
- `pyproject.toml`: 4 KB

---

## Data Access Patterns

### Read Pattern
```python
# 1. Check if exists
path.exists()

# 2. Read content
content = path.read_text()

# 3. Parse (if structured)
# - TOML: regex or library
# - YAML: frontmatter parsing
# - Markdown: as-is
```

### Write Pattern
```python
# 1. Create directory
path.mkdir(parents=True, exist_ok=True)

# 2. Write content
path.write_text(content)

# 3. No validation (user responsibility)
```

---

## Data Shape Visualization

### Hierarchical View
```
Project
│
├── Configuration (Structured)
│   ├── pyproject.toml        [TOML: Nested KV]
│   └── uv.lock               [TOML: Array of Objects]
│
├── Memory (Unstructured)
│   └── _pyrite/
│       ├── active/           [Flat: Text Files]
│       ├── backlog/          [Flat: Text Files]
│       └── standards/        [Flat: Text Files]
│
└── Framework (Semi-structured)
    └── _work_efforts/
        ├── devlog.md         [Markdown: Sections]
        └── WE-*/             [YAML+MD: Frontmatter+Content]
            └── tickets/      [YAML+MD: Frontmatter+Content]
```

### Data Flow Shape
```
User Action
    ↓
File System Operation
    ↓
Read/Write Plain Text
    ↓
Parse (if needed)
    ↓
Return Data Structure
```

---

## Schema Comparison

### Structured Data (pyproject.toml, uv.lock)
- **Schema**: Defined (Python packaging standards)
- **Validation**: By `uv` tool
- **Types**: Enforced
- **Structure**: Rigid

### Semi-structured Data (Work Efforts)
- **Schema**: Partial (YAML frontmatter)
- **Validation**: None
- **Types**: Some (in frontmatter)
- **Structure**: Flexible (Markdown content)

### Unstructured Data (_pyrite/)
- **Schema**: None
- **Validation**: None
- **Types**: None
- **Structure**: Free-form

---

## Summary

### Data Shape Philosophy
- **Mixed Structure**: Some structured (TOML), some unstructured (Markdown)
- **File-Based**: All data is files, no binary formats
- **Hierarchical**: Directory-based organization
- **Flexible**: User-defined content in `_pyrite/`
- **Standard**: Standard formats (TOML, Markdown, YAML)

### Key Characteristics
1. **No Database**: Everything is files
2. **No Schema Enforcement**: Flexible organization
3. **Human-Readable**: All text formats
4. **Git-Friendly**: All version-controllable
5. **Portable**: Self-contained structure

---

**Last Updated**: 2026-01-04

