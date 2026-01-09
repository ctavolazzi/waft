# Global Cursor Commands Setup

**Date**: 2026-01-07 19:46 PST  
**Work**: Make Cursor commands available globally  
**Status**: ✅ Complete

---

## Summary

Set up global Cursor commands system so all commands are available across all Cursor instances on the local machine. Created sync script and synced 8 commands to `~/.cursor/commands/`.

---

## What Was Done

### 1. Created Global Commands Directory ✅
- **Location**: `~/.cursor/commands/`
- **Status**: Created and ready

### 2. Created Sync Script ✅
- **Location**: `scripts/sync-cursor-commands.sh`
- **Features**:
  - Copies commands from project to global location
  - Only updates changed files
  - Shows sync status with colors
  - Counts synced/skipped files

### 3. Synced All Commands ✅
- **Commands Synced**: 8 total
  1. `verify.md`
  2. `checkpoint.md`
  3. `consider.md`
  4. `engineering.md`
  5. `explore.md`
  6. `orient.md`
  7. `spin-up.md`
  8. `COMMAND_RECOMMENDATIONS.md`

### 4. Created Documentation ✅
- **Setup Guide**: `.cursor/commands/GLOBAL_COMMANDS_SETUP.md`
- **Includes**: Setup instructions, maintenance, troubleshooting

---

## How It Works

### Cursor Command Locations

Cursor looks for commands in two places:
1. **Project-specific**: `.cursor/commands/` (per project)
2. **Global**: `~/.cursor/commands/` (all projects)

**Global commands are available in ALL Cursor instances**, regardless of which project you're in.

### Sync Process

```bash
# From waft project root
./scripts/sync-cursor-commands.sh
```

The script:
- Copies all `.md` files from `.cursor/commands/` to `~/.cursor/commands/`
- Only updates files that have changed
- Shows what was synced/skipped
- Provides colored output for clarity

---

## Usage

### Using Global Commands

1. **Open any Cursor instance** (any project)
2. **Type `/` in chat**
3. **See your commands** in the list
4. **Select command** to use it

### Updating Commands

When you update a command in the waft project:

```bash
# Sync updated commands to global
./scripts/sync-cursor-commands.sh
```

Commands are now updated globally!

---

## Files Created

1. **`scripts/sync-cursor-commands.sh`** - Sync script (executable)
2. **`.cursor/commands/GLOBAL_COMMANDS_SETUP.md`** - Setup documentation
3. **`~/.cursor/commands/`** - Global commands directory (8 files)

---

## Verification

✅ **Global commands directory exists**: `~/.cursor/commands/`  
✅ **8 commands synced**: All commands copied successfully  
✅ **Sync script works**: Tested and functional  
✅ **Documentation created**: Setup guide available

---

## Next Steps

1. **Test in another project**: Open a different project in Cursor and type `/` to see commands
2. **Update workflow**: When updating commands, run sync script
3. **Optional**: Set up git hook for auto-sync on commit (see GLOBAL_COMMANDS_SETUP.md)

---

## Maintenance

### Regular Sync

When you update commands in the waft project:
```bash
./scripts/sync-cursor-commands.sh
```

### Auto-Sync (Optional)

Add git hook for automatic syncing:
```bash
# See GLOBAL_COMMANDS_SETUP.md for details
```

---

**Status**: ✅ Complete - Commands are now global!
