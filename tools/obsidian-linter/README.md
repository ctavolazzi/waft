# Obsidian Linter Integration

This directory contains a **symlink** to the pyrite project's Obsidian linter.

**Source**: `/Users/ctavolazzi/Code/active/_pyrite/tools/obsidian-linter/`
**Symlink**: `tools/obsidian-linter-pyrite` → pyrite's linter

---

## Usage

### Direct Access

```bash
# Run the linter from pyrite
python3 tools/obsidian-linter-pyrite/lint.py --scope _work_efforts

# Or use the wrapper script
./tools/obsidian-linter/waft-lint.sh --scope _work_efforts
```

### Via Wrapper Script

```bash
# Check for issues (read-only)
./tools/obsidian-linter/waft-lint.sh

# Preview fixes
./tools/obsidian-linter/waft-lint.sh --fix --dry-run

# Apply fixes
./tools/obsidian-linter/waft-lint.sh --fix
```

---

## How It Works

The linter is **not copied** - it's linked from the pyrite project. This means:
- ✅ Always uses the latest version from pyrite
- ✅ Updates automatically when pyrite updates
- ✅ No duplication of code
- ✅ Single source of truth

**Note**: If the pyrite project moves or the symlink breaks, you'll need to recreate it:
```bash
ln -sf /Users/ctavolazzi/Code/active/_pyrite/tools/obsidian-linter tools/obsidian-linter-pyrite
```

---

## Available Tools

The pyrite linter includes:

- `lint.py` - Unified linter (runs all checks)
- `check.py` - Linting checks
- `validate.py` - Validation checks
- `fix-all.py` - Auto-fix all issues
- `fix-obsidian-links.py` - Fix Obsidian wikilinks
- `fix-links.py` - Fix general links

---

## Integration with Waft

This linter is used to maintain quality of markdown documentation in:
- `_work_efforts/` - Work effort documentation
- `_pyrite/` - Project memory files
- Any other markdown files in the project

---

## Updating

The linter updates automatically when pyrite is updated. To verify the link:

```bash
ls -la tools/obsidian-linter-pyrite
# Should show: obsidian-linter-pyrite -> /Users/ctavolazzi/Code/active/_pyrite/tools/obsidian-linter
```

If the link is broken, recreate it:
```bash
rm tools/obsidian-linter-pyrite  # Remove broken link
ln -sf /Users/ctavolazzi/Code/active/_pyrite/tools/obsidian-linter tools/obsidian-linter-pyrite
```

