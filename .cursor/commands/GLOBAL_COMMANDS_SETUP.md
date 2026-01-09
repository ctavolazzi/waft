# Global Cursor Commands Setup

**Purpose**: Make Cursor commands available globally across all Cursor instances.

---

## How Cursor Commands Work

Cursor looks for commands in two locations:
1. **Project-specific**: `.cursor/commands/` in each project
2. **Global**: `~/.cursor/commands/` in your home directory

Commands in the global location are available in **all** Cursor instances, regardless of project.

---

## Quick Setup

### Option 1: Use Sync Script (Recommended)

```bash
# From waft project root
./scripts/sync-cursor-commands.sh
```

This script:
- Copies all commands from `.cursor/commands/` to `~/.cursor/commands/`
- Only updates changed files
- Shows what was synced

### Option 2: Manual Copy

```bash
# Copy all commands to global location
cp -r .cursor/commands/* ~/.cursor/commands/
```

### Option 3: Symlink (Advanced)

```bash
# Create symlinks (commands stay in project, but available globally)
mkdir -p ~/.cursor/commands
ln -s "$(pwd)/.cursor/commands/"* ~/.cursor/commands/
```

**Note**: Symlinks mean commands are tied to this project location. If you move/delete the project, commands break.

---

## Current Global Commands

After syncing, these commands are available globally:

### Core Workflow Commands
1. **`/phase1`** - Comprehensive data gathering & visualization
2. **`/analyze`** - Analysis, insights & action planning
3. **`/resume`** - Pick up where you left off
4. **`/continue`** - Reflect on current work and continue
5. **`/reflect`** - Write in AI journal (reflection)
6. **`/recap`** - Conversation recap and session summary
7. **`/audit`** - Audit conversation quality, completeness, and issues
8. **`/checkpoint`** - Situation report and status update
9. **`/verify`** - Verification with traceable evidence

### Analysis & Planning Commands
6. **`/consider`** - Analysis and recommendations
7. **`/decide`** - Decision matrix and evaluation
8. **`/explore`** - Deep exploration

### Project Management Commands
9. **`/orient`** - Project startup process
10. **`/spin-up`** - Quick orientation
11. **`/engineer`** - Complete workflow
12. **`/goal`** - Track larger goals, break into steps
13. **`/proceed`** - Verify context and assumptions before continuing
13. **`/next`** - Identify next step based on goals
14. **`/checkout`** - Branch checkout and context switching

### Utility Commands
13. **`/visualize`** - Generate visual dashboard
14. **`/stats`** - Project statistics
15. **`/analytics`** - Session analytics

### Documentation
16. **`/COMMAND_RECOMMENDATIONS`** - Command recommendations guide

---

## Keeping Commands Updated

### Option 1: Manual Sync (When Changed)

When you update a command in the project:
```bash
./scripts/sync-cursor-commands.sh
```

### Option 2: Auto-Sync on Commit (Git Hook)

Add a git hook to auto-sync on commit:

```bash
# Create post-commit hook
cat > .git/hooks/post-commit << 'EOF'
#!/bin/bash
# Auto-sync Cursor commands after commit
if [ -f scripts/sync-cursor-commands.sh ]; then
    ./scripts/sync-cursor-commands.sh > /dev/null 2>&1
fi
EOF

chmod +x .git/hooks/post-commit
```

### Option 3: Watch Script (Development)

For active development, watch for changes:

```bash
# Install fswatch if needed: brew install fswatch
fswatch -o .cursor/commands/ | while read; do
    ./scripts/sync-cursor-commands.sh
done
```

---

## Verification

Check that commands are global:

```bash
# List global commands
ls -1 ~/.cursor/commands/*.md

# Test in any Cursor instance
# Type "/" in chat and you should see your commands
```

---

## Project-Specific vs Global

**Global Commands** (`~/.cursor/commands/`):
- ✅ Available in all projects
- ✅ Shared across all Cursor instances
- ✅ Good for reusable workflows
- ⚠️ Need to sync when updated

**Project Commands** (`.cursor/commands/`):
- ✅ Project-specific workflows
- ✅ Version controlled with project
- ✅ Don't need syncing
- ⚠️ Only available in that project

**Best Practice**: 
- Put **reusable** commands in global location
- Put **project-specific** commands in project location
- Sync global commands when updated

---

## Troubleshooting

### Commands Not Appearing

1. **Check location**: `ls ~/.cursor/commands/`
2. **Check permissions**: Files should be readable
3. **Restart Cursor**: May need to restart for changes to take effect
4. **Check file format**: Must be `.md` files

### Commands Out of Date

1. **Run sync script**: `./scripts/sync-cursor-commands.sh`
2. **Check for conflicts**: Compare project vs global versions
3. **Manual update**: Copy specific file if needed

### Multiple Versions

If you have the same command in both locations:
- **Global takes precedence** (usually)
- Or Cursor may show both (check Cursor behavior)
- **Recommendation**: Keep global version as source of truth for reusable commands

---

## Maintenance

### Regular Sync

Sync commands periodically:
```bash
# Weekly sync
./scripts/sync-cursor-commands.sh
```

### Update Workflow

1. Edit command in project: `.cursor/commands/command.md`
2. Test locally
3. Sync to global: `./scripts/sync-cursor-commands.sh`
4. Commands now available everywhere

---

## Related Files

- **Sync Script**: `scripts/sync-cursor-commands.sh`
- **Project Commands**: `.cursor/commands/`
- **Global Commands**: `~/.cursor/commands/`

---

**Commands synced and ready for global use!** 🚀
