# Waft Data Storage: Quick Reference

**Location**: All data stored in project directory
**Format**: Plain text files (no database)
**Model**: Decentralized, file-based

---

## Storage Map

```
my_project/
├── _pyrite/              ← PRIMARY DATA STORAGE
│   ├── active/           ← Current work files
│   │   ├── .gitkeep
│   │   └── *.md, *.txt   ← User files
│   ├── backlog/          ← Future work files
│   │   ├── .gitkeep
│   │   └── *.md, *.txt   ← User files
│   └── standards/        ← Standards files
│       ├── .gitkeep
│       └── *.md, *.txt   ← User files
│
├── pyproject.toml        ← PROJECT CONFIG
│   └── name, version, dependencies
│
├── uv.lock              ← DEPENDENCY LOCK
│   └── Locked versions (read-only)
│
└── _work_efforts/       ← FRAMEWORK INTERNAL (optional)
    └── Work tracking (Johnny Decimal)
```

---

## Data Types

| Data Type | Location | Format | Managed By |
|-----------|----------|--------|------------|
| **Project Knowledge** | `_pyrite/` | Markdown/Text | User |
| **Project Config** | `pyproject.toml` | TOML | `uv` / User |
| **Dependencies** | `uv.lock` | TOML | `uv` |
| **Work Tracking** | `_work_efforts/` | Markdown | Framework |

---

## How Data is Stored

### 1. _pyrite/ (Memory Layer)
- **Purpose**: Project knowledge organization
- **Storage**: Regular files in folders
- **Format**: Any text format (typically `.md`)
- **Access**: Direct file system or `MemoryManager` API
- **Size**: 12KB (structure only, user files add to this)

### 2. pyproject.toml (Configuration)
- **Purpose**: Project metadata and dependencies
- **Storage**: Single TOML file
- **Format**: TOML
- **Access**: `SubstrateManager` API or direct editing
- **Size**: ~4KB

### 3. uv.lock (Dependencies)
- **Purpose**: Locked dependency versions
- **Storage**: Single TOML file (generated)
- **Format**: TOML (read-only for users)
- **Access**: `uv sync` command
- **Size**: ~716KB (depends on dependencies)

### 4. _work_efforts/ (Framework)
- **Purpose**: Development work tracking
- **Storage**: Markdown files with YAML frontmatter
- **Format**: Markdown + YAML
- **Access**: Work effort MCP tools
- **Size**: ~116KB (documentation and tracking)

---

## Storage Characteristics

✅ **Decentralized**: Each project is self-contained
✅ **File-based**: No database, just files
✅ **Git-friendly**: All data can be version controlled
✅ **Human-readable**: Plain text formats
✅ **Portable**: Copy directory = copy all data
✅ **Simple**: No complex storage layer

⚠️ **No indexing**: Files not searchable
⚠️ **No querying**: No SQL or query language
⚠️ **No transactions**: No atomic operations
⚠️ **No relationships**: No linking between files

---

## Access Patterns

### Read Data
```python
# Project info
substrate = SubstrateManager()
info = substrate.get_project_info(path)

# Memory structure
memory = MemoryManager(path)
files = memory.get_active_files()
```

### Write Data
```python
# Create structure
memory.create_structure()

# Add files (user does directly)
# touch _pyrite/active/my-file.md
```

### Query Data
```python
# List files
active = memory.get_active_files()
backlog = memory.get_backlog_files()
standards = memory.get_standards_files()

# Check structure
status = memory.verify_structure()
```

---

## Current Storage Stats

- **`_pyrite/`**: 12KB (structure)
- **`_work_efforts/`**: 116KB (documentation)
- **`uv.lock`**: 716KB (dependencies)
- **`pyproject.toml`**: 4KB (config)

**Total**: ~848KB (excluding user files in `_pyrite/`)

---

## Philosophy

**"Files Over Databases"**

- Data lives with the project
- No external dependencies
- Maximum portability
- Minimum complexity
- Git-friendly by design

