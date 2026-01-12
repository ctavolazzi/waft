# Banned Words System

**Created**: 2026-01-11
**Status**: Active
**Purpose**: Enforce word restrictions across the codebase

---

## Overview

The Banned Words System (`src/waft/core/banned_words.py`) provides tools to:
1. **Check** for banned words in code and documentation
2. **Replace** banned words with approved alternatives
3. **Enforce** word restrictions automatically

---

## Current Banned Words

| Word | Replacement | Reason |
|------|-------------|--------|
| `manifesto` | `report` | Banned by user request |

---

## Usage

### Command Line Tool

```bash
# Scan for banned words
python3 scripts/remove_banned_words.py

# The tool will:
# 1. Scan all files (*.py, *.md, *.txt, *.json, *.yaml, *.yml)
# 2. Report violations with line numbers and context
# 3. Ask for confirmation before replacing
# 4. Replace all instances
# 5. Verify replacements
```

### Python API

```python
from pathlib import Path
from src.waft.core.banned_words import BannedWordsSystem

# Initialize system
ban_system = BannedWordsSystem(project_path=Path("."))

# Add a banned word
ban_system.add_ban(
    word="example",
    replacement="sample",
    reason="User request",
    case_sensitive=False
)

# Check text
violations = ban_system.check_text("This is an example text.")
# Returns: [{"line": 1, "word": "example", "replacement": "sample", ...}]

# Scan file
violations = ban_system.scan_file(Path("file.py"))

# Scan directory
violations = ban_system.scan_directory(Path("."), patterns=["*.py", "*.md"])

# Replace in text
new_text = ban_system.replace_in_text("This is an example text.")
# Returns: "This is a sample text."

# Replace in file
modified = ban_system.replace_in_file(Path("file.py"))
# Returns: True if file was modified
```

---

## Implementation Details

### BannedWord Class

```python
@dataclass
class BannedWord:
    word: str              # Word to ban
    replacement: str       # Replacement word
    reason: str = ""       # Reason for ban
    case_sensitive: bool = False  # Whether ban is case-sensitive
```

### BannedWordsSystem Class

- **`add_ban()`**: Add a banned word
- **`check_text()`**: Check text for violations
- **`scan_file()`**: Scan a file for violations
- **`scan_directory()`**: Scan directory recursively
- **`replace_in_text()`**: Replace banned words in text
- **`replace_in_file()`**: Replace banned words in file
- **`get_banned_words()`**: Get list of all banned words
- **`get_replacements()`**: Get mapping of banned words to replacements

---

## File Exclusions

The scanner automatically excludes:
- `.git/` directories
- `__pycache__/` directories
- `node_modules/` directories
- `.venv/` directories

---

## Integration

The banned words system is integrated into:
- **Scripts**: `scripts/remove_banned_words.py` - Command-line tool
- **Core**: `src/waft/core/banned_words.py` - Python API

---

## Adding New Banned Words

1. **Via Python API**:
```python
ban_system = BannedWordsSystem(project_path)
ban_system.add_ban("word", "replacement", "reason")
```

2. **Via Code** (edit `src/waft/core/banned_words.py`):
```python
def _load_default_bans(self):
    self.banned_words = [
        BannedWord(word="manifesto", replacement="report", ...),
        BannedWord(word="new_word", replacement="new_replacement", ...),
    ]
```

---

## Verification

After adding a banned word, run:
```bash
python3 scripts/remove_banned_words.py
```

This will:
1. Scan the entire codebase
2. Report all violations
3. Allow you to replace them all at once

---

**Status**: System active, "manifesto" banned and removed from codebase
