# Empirica Python Version Compatibility Issue

**Date**: 2026-01-05
**Status**: ✅ FIXED
**Issue**: Empirica CLI requires Python 3.11+ but system has Python 3.10.0

---

## Problem

Empirica 1.2.3 fails to run on Python 3.10.0 with the following error:

```
ImportError: cannot import name 'UTC' from 'datetime'
```

**Root Cause**: Empirica uses `from datetime import UTC`, which was added in Python 3.11. Python 3.10's datetime module doesn't have `UTC`.

**MCP Server**: Also requires Python 3.11+ (all versions: 1.0.0, 1.0.1, 1.0.2, 1.0.3, 1.1.0, 1.2.0, 1.2.1)

---

## System Information

- **Python Version**: 3.10.0
- **Empirica Version**: 1.2.3
- **Project Requirement**: `>=3.10` (supports 3.10, 3.11, 3.12)

---

## Impact

- ✅ Empirica package installed successfully
- ❌ Empirica CLI cannot run on Python 3.10
- ⚠️ EmpiricaManager integration code is ready but CLI won't work
- ✅ Work documented in _pyrite structure instead

---

## Solutions

### Option 1: Upgrade Python (Recommended)

Upgrade to Python 3.11+ to use Empirica CLI:

```bash
# Check available Python versions
python3.11 --version  # If available
python3.12 --version  # If available

# Use Python 3.11+ for Empirica
python3.11 -m pip install empirica
python3.11 -m empirica session-create ...
```

### Option 2: Document Limitation

Keep current setup and document that:
- EmpiricaManager code works (Python 3.10+)
- Empirica CLI requires Python 3.11+
- Projects using Empirica CLI need Python 3.11+

### Option 3: Make Empirica Optional

Already done - Empirica is in dependencies but CLI usage is optional. The EmpiricaManager gracefully handles CLI not being available.

---

## Solution Implemented

**EmpiricaManager** now automatically detects and uses Python 3.12's empirica binary when available:

1. Checks for `/Library/Frameworks/Python.framework/Versions/3.12/bin/empirica`
2. Verifies it works by checking version output (must show Python 3.12 or 3.11)
3. Falls back to Python 3.11 if 3.12 not available
4. Falls back to system `empirica` command if versioned paths not found (with version verification)

**Result**: EmpiricaManager now works correctly even when system Python is 3.10, as long as Python 3.12 is installed.

---

## Current Status

- ✅ Empirica package installed (both Python 3.10 and 3.12)
- ✅ Empirica CLI working with Python 3.12
- ✅ EmpiricaManager updated to auto-detect Python 3.12
- ✅ Fix implemented and tested

---

## Next Steps

1. ✅ **COMPLETE**: EmpiricaManager auto-detects Python 3.12
2. ✅ **COMPLETE**: Tested and verified working
3. ⏳ **Optional**: Update documentation to note auto-detection feature

---

**Last Updated**: 2026-01-05
**Status**: ✅ **FIXED** - EmpiricaManager now auto-detects and uses Python 3.12 when available

