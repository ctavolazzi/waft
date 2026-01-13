# Python Version Setup for Waft

## Overview

Waft requires **Python 3.12+** for full functionality, particularly for Empirica integration. This document explains how to ensure you're using the correct Python version.

## Current Setup

- **Required Python Version**: 3.12+
- **Current Python**: 3.12.0 (at `/Library/Frameworks/Python.framework/Versions/3.12/bin/python3`)
- **Empirica**: Installed and configured for Python 3.12
- **Version Pinning**: `.python-version` file in project root

## Verification

Run the verification script to check your setup:

```bash
python3 scripts/verify_python_version.py
```

This will check:
- ✅ Python version (must be 3.12+)
- ✅ Empirica installation and Python version
- ✅ Empirica project initialization

## Version Management

### Using `.python-version` File

The project includes a `.python-version` file that specifies Python 3.12. This file is recognized by:
- **pyenv** (if installed): Automatically switches to Python 3.12
- **IDE tools**: Many IDEs respect this file
- **Documentation**: Serves as a reference for the required version

### Manual Verification

Check your Python version:
```bash
python3 --version  # Should show Python 3.12.0 or higher
which python3      # Should point to Python 3.12
```

### Empirica Command

Empirica is installed for Python 3.12 at:
```
/Library/Frameworks/Python.framework/Versions/3.12/bin/empirica
```

The `EmpiricaManager` class automatically detects and uses this path.

## Troubleshooting

### If Python version is wrong:

1. **Check available Python versions:**
   ```bash
   python3.12 --version
   python3.11 --version
   ```

2. **Use Python 3.12 explicitly:**
   ```bash
   /Library/Frameworks/Python.framework/Versions/3.12/bin/python3 --version
   ```

3. **Update PATH (temporary):**
   ```bash
   export PATH="/Library/Frameworks/Python.framework/Versions/3.12/bin:$PATH"
   ```

### If Empirica is not found:

1. **Install Empirica for Python 3.12:**
   ```bash
   /Library/Frameworks/Python.framework/Versions/3.12/bin/pip3 install empirica
   ```

2. **Verify installation:**
   ```bash
   /Library/Frameworks/Python.framework/Versions/3.12/bin/empirica --version
   ```

### If Empirica is not initialized:

1. **Initialize Empirica in the project:**
   ```bash
   /Library/Frameworks/Python.framework/Versions/3.12/bin/empirica project-init
   ```

   Note: This requires git to be initialized first.

## Project Configuration

### pyproject.toml

The project specifies:
```toml
requires-python = ">=3.10"
```

However, **Empirica requires Python 3.11+**, so we use Python 3.12 for consistency.

### EmpiricaManager

The `EmpiricaManager` class (in `src/waft/core/empirica.py`) automatically:
1. Detects Python 3.12's empirica binary
2. Falls back to Python 3.11 if 3.12 not available
3. Verifies the Python version before using it

## Best Practices

1. **Always verify Python version** before running Waft commands
2. **Use the verification script** when setting up a new environment
3. **Check `.python-version`** is present in the project root
4. **Use Python 3.12 explicitly** in scripts if needed:
   ```bash
   /Library/Frameworks/Python.framework/Versions/3.12/bin/python3 script.py
   ```

## Status

✅ **Current Status (2026-01-13)**:
- Python 3.12.0 installed and configured
- Empirica 1.2.3 installed for Python 3.12
- Empirica initialized in project
- `.python-version` file created
- Verification script available

---

**Last Updated**: 2026-01-13
