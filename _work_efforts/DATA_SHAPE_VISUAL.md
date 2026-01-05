# Waft Data Shape: Visual Guide

**Quick Reference**: How data actually looks in waft

---

## 1. _pyrite/ Data Shape

### Structure
```
_pyrite/
├── active/     [Flat collection of files]
├── backlog/     [Flat collection of files]
└── standards/   [Flat collection of files]
```

### Shape: Array of File Names
```json
{
  "active": ["file1.md", "file2.txt"],
  "backlog": ["idea.md"],
  "standards": ["guidelines.md"]
}
```

### File Content Shape
```markdown
# Any markdown/text content
- No enforced structure
- User-defined format
- Free-form text
```

---

## 2. pyproject.toml Shape

### Structure
```toml
[project]                    ← Table (object)
  name = "string"           ← String field
  version = "string"         ← String field
  dependencies = [          ← Array field
    "package>=version"      ← String items
  ]
```

### Extracted Shape
```json
{
  "name": "waft",
  "version": "0.0.1"
}
```

---

## 3. uv.lock Shape

### Structure
```toml
version = 1                 ← Integer
[[package]]                 ← Array of objects
  name = "string"
  version = "string"
  source = { ... }          ← Nested object
  dependencies = [ ... ]    ← Array
```

### Shape: Array of Package Objects
```json
{
  "version": 1,
  "packages": [
    {
      "name": "package-name",
      "version": "1.2.3",
      "source": {...},
      "dependencies": [...]
    }
  ]
}
```

---

## 4. Work Effort Shape

### File Structure
```yaml
---                        ← YAML frontmatter (metadata object)
id: "WE-260104-bk5z"
title: "Title"
status: "completed"
created: "2026-01-05T..."
---                        ← End metadata

# Markdown content        ← Free-form text
## Section
Content...
```

### Extracted Shape
```json
{
  "metadata": {
    "id": "WE-260104-bk5z",
    "title": "Title",
    "status": "completed",
    "created": "2026-01-05T..."
  },
  "content": "# Markdown content..."
}
```

---

## 5. API Response Shapes

### Project Info
```json
{
  "project_path": "string",
  "project_name": "string",
  "version": "string",
  "pyrite_structure": {
    "valid": boolean,
    "folders": {
      "_pyrite/active": boolean,
      "_pyrite/backlog": boolean,
      "_pyrite/standards": boolean
    }
  },
  "uv_lock": boolean,
  "templates": {
    "justfile": boolean,
    "ci": boolean,
    "agents": boolean,
    "gitignore": boolean,
    "readme": boolean
  }
}
```

### Memory Structure
```json
{
  "active": ["string", "string"],
  "backlog": ["string"],
  "standards": ["string"]
}
```

---

## Data Type Matrix

| Location | Format | Shape | Schema | Example |
|----------|--------|-------|--------|---------|
| `_pyrite/*` | Markdown | Flat array of files | None | `["file.md"]` |
| `pyproject.toml` | TOML | Nested object | Defined | `{name: "project"}` |
| `uv.lock` | TOML | Array of objects | Defined | `{packages: [...]}` |
| Work Efforts | YAML+MD | Object+text | Partial | `{metadata: {}, content: ""}` |

---

## Current Data Shape (Waft Project)

```json
{
  "_pyrite": {
    "active": { "files": [".gitkeep"], "count": 1 },
    "backlog": { "files": [".gitkeep"], "count": 1 },
    "standards": { "files": [".gitkeep"], "count": 1 }
  },
  "pyproject.toml": {
    "size": 1672,
    "lines": 68,
    "has_dependencies": true
  },
  "uv.lock": {
    "size": 730740,
    "lines": 3980,
    "has_packages": true
  }
}
```

---

## Key Insights

1. **Mixed Formats**: TOML (structured) + Markdown (unstructured)
2. **Flat Collections**: `_pyrite/` folders are flat (no nesting)
3. **Nested Objects**: Configuration files use nested structures
4. **No Schema**: User files have no enforced structure
5. **Partial Schema**: Work efforts have YAML frontmatter only

---

**Shape**: Hierarchical files → Flat arrays → Nested objects → Free text

