# Development Workflow - Preventing Stale Installations

## Problem

When developing waft, code changes in `src/waft/` are not automatically reflected when running `waft` commands because the installed package at `/Users/ctavolazzi/.local/share/uv/tools/waft/` contains a **copy** of the code, not a link to the source.

## Solution: Editable Installs

Use `--editable` (or `-e`) mode when installing:

```bash
uv tool install --editable .
```

This creates a **link** to your source code instead of copying it, so changes are immediately reflected.

## Prevention Strategies

### 1. Always Use Editable Mode for Development

**Initial setup:**
```bash
cd /path/to/waft
uv sync
uv tool install --editable .
```

**If already installed without `--editable`:**
```bash
uv tool install --editable .
# or
./scripts/dev-reinstall.sh
```

### 2. Verification Script

Check if installation is editable:
```bash
./scripts/check-editable.sh
```

This will tell you if your installation is in editable mode.

### 3. Quick Reinstall Script

After making changes (if not using editable mode):
```bash
./scripts/dev-reinstall.sh
```

### 4. Documentation

- **CONTRIBUTING.md** - Updated with editable install instructions
- **README.md** - Added development mode section
- **This document** - Comprehensive workflow guide

## How to Tell if You Have the Problem

**Symptoms:**
- Code changes don't appear when running `waft` commands
- Error tracebacks show paths like `/Users/.../.local/share/uv/tools/waft/...`
- Changes work in source but not in installed package

**Check:**
```bash
./scripts/check-editable.sh
```

If it says "NOT installed in editable mode", run:
```bash
./scripts/dev-reinstall.sh
```

## Best Practices

1. **Always use `--editable` for development**
2. **Run `./scripts/check-editable.sh`** if you're unsure
3. **Reinstall after major refactoring** even with editable mode (sometimes needed)
4. **Document in CONTRIBUTING.md** so others know the workflow

## Files Created

- `scripts/dev-reinstall.sh` - Quick reinstall script
- `scripts/check-editable.sh` - Verification script
- `CONTRIBUTING.md` - Updated with workflow
- `README.md` - Updated with development mode section

