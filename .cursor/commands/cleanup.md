# Cleanup

**Cleanup and maintenance - organize and clean up.**

Cleans up temporary files, organizes `_pyrite/active/` files, archives old checkpoints, and cleans up test files. Perfect for maintenance, organization, and keeping the project clean.

**Use when:** Need to organize, clean up temporary files, or perform maintenance.

---

## Purpose

This command provides:
- **Temporary File Cleanup**: Remove temporary files
- **File Organization**: Organize `_pyrite/active/` files
- **Archive Management**: Archive old checkpoints
- **Test File Cleanup**: Clean up test files
- **Project Maintenance**: General cleanup tasks

---

## Philosophy

1. **Safe**: Verify before deleting
2. **Selective**: Clean up specific areas
3. **Organized**: Organize files properly
4. **Traceable**: Document what was cleaned
5. **Reversible**: Support dry-run mode

---

## Execution Steps

### Cleanup 1.1: Identify Cleanup Targets
**Purpose**: Find what needs to be cleaned

**Steps**:
1. Find temporary files (`.tmp`, `.temp`, `*.swp`, etc.)
2. Check `_pyrite/active/` for old files
3. Find old checkpoint files
4. Identify test files to clean
5. Check for duplicate files

**Output**: List of cleanup targets

---

### Cleanup 1.2: Organize Active Files
**Purpose**: Organize `_pyrite/active/` directory

**Steps**:
1. Review files in `_pyrite/active/`
2. Identify files older than threshold (e.g., 30 days)
3. Move to `_pyrite/backlog/` or archive
4. Organize by date or category
5. Update indexes

**Output**: Organized active files

---

### Cleanup 1.3: Archive Old Checkpoints
**Purpose**: Archive old checkpoint files

**Steps**:
1. Find checkpoint files in `_work_efforts/`
2. Identify old checkpoints (e.g., >90 days)
3. Move to archive directory
4. Update indexes
5. Clean up old archives

**Output**: Archived checkpoints

---

### Cleanup 1.4: Remove Temporary Files
**Purpose**: Clean up temporary files

**Steps**:
1. Find temporary files
2. Verify they're safe to delete
3. Remove temporary files
4. Report what was removed

**Output**: Removed temporary files

---

### Cleanup 1.5: Clean Test Files
**Purpose**: Clean up test files

**Steps**:
1. Find test output files
2. Identify test artifacts
3. Remove test files (if safe)
4. Report cleanup

**Output**: Cleaned test files

---

## Execution Flow

```
Cleanup 1.1: Identify Cleanup Targets
  ↓
Cleanup 1.2: Organize Active Files
  ↓
Cleanup 1.3: Archive Old Checkpoints
  ↓
Cleanup 1.4: Remove Temporary Files
  ↓
Cleanup 1.5: Clean Test Files
  ↓
✅ Complete - Cleanup report displayed
```

---

## Output Format

### Console Output

The command displays cleanup summary:

```
🧹 Cleanup: Project Maintenance

Cleanup Targets Identified:
  - 5 temporary files
  - 12 old active files (>30 days)
  - 3 old checkpoints (>90 days)
  - 2 test output files

Active Files Organization:
  ✅ Moved 12 files to backlog
  ✅ Organized by date
  ✅ Updated indexes

Checkpoint Archiving:
  ✅ Archived 3 old checkpoints
  ✅ Updated indexes

Temporary File Cleanup:
  ✅ Removed 5 temporary files
    - .tmp/test_output.tmp
    - .temp/debug.log.temp
    - *.swp files (2)

Test File Cleanup:
  ✅ Removed 2 test output files

Summary:
  Files Organized: 12
  Files Archived: 3
  Files Removed: 7
  Space Freed: ~2.3 MB

⏱️  Cleanup complete: 3.5s
```

---

## What Gets Cleaned

### Temporary Files
- `.tmp` files
- `.temp` files
- `*.swp` files (vim swap files)
- `*.bak` files (backup files)
- `*~` files (editor backups)

### Active Files Organization
- Old files in `_pyrite/active/` (>30 days)
- Files moved to `_pyrite/backlog/`
- Files organized by date/category

### Old Checkpoints
- Checkpoint files >90 days old
- Moved to archive directory
- Old archives cleaned up

### Test Files
- Test output files
- Test artifacts
- Temporary test files

---

## Use Cases

### 1. Regular Maintenance
**Scenario**: Regular cleanup to keep project organized

**Example**:
```
User: "/cleanup"
```

**Output**: Project cleaned and organized

---

### 2. Organize Active Files
**Scenario**: Active directory is cluttered

**Example**:
```
User: "/cleanup --active"
```

**Output**: Active files organized

---

### 3. Archive Old Files
**Scenario**: Need to archive old checkpoints

**Example**:
```
User: "/cleanup --archive"
```

**Output**: Old files archived

---

### 4. Remove Temporary Files
**Scenario**: Temporary files accumulating

**Example**:
```
User: "/cleanup --temp"
```

**Output**: Temporary files removed

---

## Integration with Other Commands

- **`/status`**: Shows cleanup status (`/cleanup` performs cleanup)
- **`/sync`**: Syncs docs (`/cleanup` organizes files)
- **`/search`**: Finds files (`/cleanup` removes files)

---

## When to Use

**Use `/cleanup` when**:
- ✅ Need to organize files
- ✅ Temporary files accumulating
- ✅ Active directory cluttered
- ✅ Need maintenance
- ✅ Want to free up space

**Don't use `/cleanup` when**:
- ❌ Unsure about file safety (use `--dry-run` first)
- ❌ Need to keep all files (skip cleanup)
- ❌ Recent work might be affected (be careful)

---

## Technical Details

### Tools Used

**File System**:
- `find` - Find files to clean
- `rm` - Remove files (with verification)
- `mv` - Move files for organization
- File operations for archiving

**Safety Checks**:
- File age verification
- File type checking
- Backup before deletion (optional)
- Dry-run mode support

### Performance

- **Target Time**: < 10 seconds
- **Target Identification**: ~2 seconds
- **Organization**: ~3 seconds
- **Archiving**: ~2 seconds
- **Cleanup**: ~2 seconds
- **Reporting**: ~1 second

### Error Handling

- **File Errors**: Skip problematic files, continue
- **Permission Errors**: Show error, continue
- **Safety Checks**: Verify before deletion
- **Always Complete**: Always show what was cleaned

---

## Example Workflow

```
User: "/cleanup --dry-run"

AI: 🧹 Cleanup: Project Maintenance (Dry Run)

Would Clean:
  - 5 temporary files
  - 12 old active files
  - 3 old checkpoints

User: "/cleanup"

AI: 🧹 Cleanup: Project Maintenance

✅ Organized 12 active files
✅ Archived 3 checkpoints
✅ Removed 5 temporary files

Summary:
  Files Organized: 12
  Files Archived: 3
  Files Removed: 5
  Space Freed: ~2.1 MB

⏱️  Cleanup complete: 3.2s

User: [Project is now clean and organized]
```

---

## Advanced Features

### Dry Run Mode
Preview what would be cleaned:
```bash
/cleanup --dry-run    # Show what would be cleaned
```

### Focus Areas
Clean specific areas:
```bash
/cleanup --active     # Organize active files only
/cleanup --archive    # Archive old files only
/cleanup --temp       # Remove temporary files only
/cleanup --test       # Clean test files only
```

### Age Thresholds
Set age thresholds:
```bash
/cleanup --active-threshold 60    # Active files >60 days
/cleanup --checkpoint-threshold 180  # Checkpoints >180 days
```

### Verbose Mode
Get detailed output:
```bash
/cleanup --verbose    # Detailed cleanup information
```

---

## Safety Features

### Verification
- Always verify before deletion
- Show what will be deleted
- Support dry-run mode
- Backup option for important files

### Selective Cleanup
- Clean specific areas only
- Skip important files
- Preserve recent work
- Respect file age thresholds

### Reversibility
- Dry-run mode to preview
- Archive instead of delete (when possible)
- Log what was cleaned
- Support undo (if implemented)

---

## Best Practices

1. **Dry Run First**: Always use `--dry-run` first
2. **Review Carefully**: Review what will be cleaned
3. **Backup Important**: Backup important files before cleanup
4. **Regular Cleanup**: Run cleanup regularly
5. **Be Selective**: Clean specific areas when needed

---

## Output Location

Cleanup operations are performed in place. A summary is displayed in console.

For detailed cleanup log:
- Use `--verbose` flag for detailed output
- Review git status to see changes

---

**This command keeps the project clean and organized - essential for maintenance and organization.**
