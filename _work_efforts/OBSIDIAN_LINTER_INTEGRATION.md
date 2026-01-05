# Obsidian Linter Integration

**Created**: 2026-01-05
**Purpose**: Integrate pyrite's Obsidian linter into waft project

---

## Solution: Symlink to Pyrite Linter

Instead of copying the linter (which would create duplication and version drift), we created a **symlink** that points to the pyrite project's linter.

**Benefits**:
- ✅ Always uses latest version from pyrite
- ✅ Updates automatically when pyrite updates
- ✅ No code duplication
- ✅ Single source of truth

---

## Structure

```
waft/
├── tools/
│   ├── obsidian-linter/
│   │   ├── README.md              # Documentation
│   │   ├── waft-lint.sh           # Wrapper script
│   │   └── .gitkeep               # Ensures directory is tracked
│   └── obsidian-linter-pyrite ->  # Symlink to pyrite linter
│       /Users/ctavolazzi/Code/active/_pyrite/tools/obsidian-linter
```

---

## Usage

### Method 1: Wrapper Script (Recommended)

```bash
# Check for issues (read-only)
./tools/obsidian-linter/waft-lint.sh

# Preview fixes
./tools/obsidian-linter/waft-lint.sh --fix --dry-run

# Apply fixes
./tools/obsidian-linter/waft-lint.sh --fix

# Custom scope
./tools/obsidian-linter/waft-lint.sh --scope _pyrite
```

### Method 2: Direct Access

```bash
# Use the symlink directly
python3 tools/obsidian-linter-pyrite/lint.py --scope _work_efforts

# Or use full path
python3 /Users/ctavolazzi/Code/active/_pyrite/tools/obsidian-linter/lint.py --scope _work_efforts
```

### Method 3: Justfile Recipes (if Justfile exists)

```bash
# Lint Obsidian files
just lint-obsidian

# Fix Obsidian files
just fix-obsidian
```

---

## How It Works

1. **Symlink Creation**
   ```bash
   ln -sf /Users/ctavolazzi/Code/active/_pyrite/tools/obsidian-linter \
          tools/obsidian-linter-pyrite
   ```

2. **Wrapper Script**
   - Checks if pyrite linter exists
   - Sets default scope to `_work_efforts`
   - Passes all arguments to pyrite's linter
   - Provides helpful error messages

3. **Justfile Integration**
   - Added `lint-obsidian` recipe
   - Added `fix-obsidian` recipe
   - Gracefully handles if linter unavailable

---

## Verification

To verify the symlink is working:

```bash
# Check symlink
ls -la tools/obsidian-linter-pyrite

# Should show:
# obsidian-linter-pyrite -> /Users/ctavolazzi/Code/active/_pyrite/tools/obsidian-linter

# Test access
python3 tools/obsidian-linter-pyrite/lint.py --help
```

---

## If Symlink Breaks

If the pyrite project moves or the symlink breaks:

```bash
# Remove broken link
rm tools/obsidian-linter-pyrite

# Recreate symlink
ln -sf /Users/ctavolazzi/Code/active/_pyrite/tools/obsidian-linter \
       tools/obsidian-linter-pyrite

# Verify
ls -la tools/obsidian-linter-pyrite
```

---

## Integration Points

### Template System

The Justfile template now includes:
- `lint-obsidian` - Check Obsidian files
- `fix-obsidian` - Fix Obsidian files

### Project Startup Process

The Obsidian linter is now part of the quality checks in `PROJECT_STARTUP_PROCESS.md`:
- Phase 3: Documentation & Quality
- Step 3.3: Run Quality Checks

---

## Available Tools

The pyrite linter provides:

1. **lint.py** - Unified linter (runs all checks)
2. **check.py** - Linting checks
3. **validate.py** - Validation checks
4. **fix-all.py** - Auto-fix all issues
5. **fix-obsidian-links.py** - Fix Obsidian wikilinks
6. **fix-links.py** - Fix general links

All accessible via the symlink.

---

## Status

✅ **Integration Complete**
- Symlink created
- Wrapper script created
- Documentation created
- Justfile recipes added (in template)
- Ready for use

---

## Next Steps

1. **Test Integration**
   ```bash
   ./tools/obsidian-linter/waft-lint.sh
   ```

2. **Fix Issues** (if desired)
   ```bash
   ./tools/obsidian-linter/waft-lint.sh --fix
   ```

3. **Add to CI/CD** (future)
   - Run linter in CI pipeline
   - Fail on critical issues
   - Auto-fix on merge

---

**Note**: The symlink approach ensures we always use the latest version of the linter from pyrite, maintaining consistency across projects.

