# Waft Framework: Database System

**Answer**: **Waft does NOT use a database system.**

---

## No Database Architecture

Waft is **completely file-based** with **zero database dependencies**. There is:

- ❌ **No SQL database** (no SQLite, PostgreSQL, MySQL, etc.)
- ❌ **No NoSQL database** (no MongoDB, Redis, etc.)
- ❌ **No key-value store** (no Redis, etcd, etc.)
- ❌ **No document store** (no CouchDB, etc.)
- ❌ **No graph database** (no Neo4j, etc.)
- ❌ **No in-memory cache** (no Redis, Memcached, etc.)
- ❌ **No centralized data store**

---

## What Waft Uses Instead

### File-Based Storage

Waft uses **plain text files** organized in a directory structure:

```
project/
├── _pyrite/           ← File-based "memory"
│   ├── active/        ← Regular files (.md, .txt, etc.)
│   ├── backlog/       ← Regular files
│   └── standards/     ← Regular files
├── pyproject.toml     ← TOML configuration file
└── uv.lock            ← TOML lock file
```

### Storage Mechanism

1. **File System**: Standard OS file system
2. **Plain Text**: Markdown, TOML, text files
3. **Direct Access**: Standard file I/O operations
4. **No Abstraction**: No database layer

---

## Why No Database?

### Design Philosophy

Waft follows a **"files over databases"** philosophy:

1. **Simplicity**: No database setup, configuration, or maintenance
2. **Portability**: Entire project (including data) is self-contained
3. **Git-Friendly**: All data can be version controlled
4. **Human-Readable**: Plain text files are easy to inspect/edit
5. **No Dependencies**: No database server required
6. **Decentralized**: Each project is independent

### Trade-offs

**Advantages**:
- ✅ Zero setup overhead
- ✅ Maximum portability
- ✅ Git-friendly by design
- ✅ Human-readable data
- ✅ No external dependencies

**Limitations**:
- ⚠️ No query language (SQL, etc.)
- ⚠️ No indexing (must scan files)
- ⚠️ No transactions (no atomic operations)
- ⚠️ No relationships (no foreign keys, etc.)
- ⚠️ Limited scalability (file system limits)

---

## Data Access Pattern

### Instead of Database Queries

**Database Approach** (NOT used):
```sql
SELECT * FROM active_files WHERE project_id = 1;
```

**Waft Approach** (actual):
```python
# Direct file system access
memory = MemoryManager(project_path)
files = memory.get_active_files()  # Returns list of Path objects
```

### Instead of Database Tables

**Database Approach** (NOT used):
```sql
CREATE TABLE projects (
    id INTEGER PRIMARY KEY,
    name TEXT,
    version TEXT
);
```

**Waft Approach** (actual):
```toml
# pyproject.toml (plain file)
[project]
name = "my-project"
version = "0.1.0"
```

---

## Code Evidence

### No Database Imports

Searching the codebase shows **zero database-related code**:

```bash
# No database imports found
grep -r "sqlite\|postgres\|mysql\|mongodb\|redis\|database" src/waft
# Result: No matches
```

### File-Based Operations

All data operations use standard file I/O:

```python
# From memory.py
gitkeep.write_text("# This file ensures...")  # Direct file write
content = pyproject_path.read_text()          # Direct file read
lock_file.exists()                            # Direct file check
```

---

## Comparison

| Feature | Database System | Waft (File-Based) |
|---------|----------------|-------------------|
| **Storage** | Database server | File system |
| **Format** | Binary/Structured | Plain text |
| **Query** | SQL/Query language | File system operations |
| **Indexing** | Automatic | None |
| **Transactions** | Yes | No |
| **Relationships** | Foreign keys | None |
| **Setup** | Complex | None |
| **Portability** | Requires DB server | Self-contained |
| **Version Control** | Difficult | Native (git) |
| **Human Readable** | No | Yes |

---

## Future Database Options

If a database were to be added in the future, options might include:

### Lightweight Options
- **SQLite**: Embedded, file-based, no server
- **TinyDB**: Pure Python, JSON-based
- **PickleDB**: Simple key-value store

### Why Not Now?
- **Philosophy**: Files align with waft's "ambient" philosophy
- **Simplicity**: No database complexity needed yet
- **Portability**: Files are more portable than databases
- **Git Integration**: Files work better with version control

---

## Summary

**Database System**: **None**

**Storage System**: **File-based**

- Files in `_pyrite/` directories
- TOML configuration files
- Plain text formats
- Standard file system operations

**Philosophy**: **"Files Over Databases"**

- Maximum simplicity
- Maximum portability
- Git-friendly by design
- Human-readable data
- Zero external dependencies

---

**Last Updated**: 2026-01-04

