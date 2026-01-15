# Sync

**Sync documentation across files - ensure consistency.**

Synchronizes documentation across multiple files, updating devlog with recent work, syncing work effort status, updating related documentation, and ensuring consistency across the project. Perfect for keeping documentation in sync after work sessions.

**Use when:** Documentation is out of sync, after work session, or need to ensure consistency.

---

## Purpose

This command provides:
- **Devlog Updates**: Update devlog with recent work
- **Work Effort Sync**: Sync work effort status across files
- **Documentation Consistency**: Ensure related docs are updated
- **Status Synchronization**: Keep status information current
- **Link Integrity**: Verify and update links

---

## Philosophy

1. **Consistency First**: Keep documentation consistent
2. **Automated**: Reduce manual sync work
3. **Comprehensive**: Update all related files
4. **Safe**: Verify before updating
5. **Traceable**: Document what was synced

---

## Execution Steps

### Sync 1.1: Identify Recent Work
**Purpose**: Find what needs to be synced

**Steps**:
1. Check recent devlog entries
2. Identify recent work efforts
3. Find modified documentation files
4. Check for unsynced changes

**Output**: List of items to sync

---

### Sync 1.2: Update Devlog
**Purpose**: Sync devlog with recent work

**Steps**:
1. Review recent work efforts
2. Check for missing devlog entries
3. Add entries for recent work
4. Update timestamps
5. Ensure proper formatting

**Output**: Updated devlog

---

### Sync 1.3: Sync Work Effort Status
**Purpose**: Keep work effort status current

**Steps**:
1. Check active work efforts
2. Update work effort status files
3. Sync ticket statuses
4. Update progress notes
5. Ensure consistency across files

**Output**: Synced work effort status

---

### Sync 1.4: Update Related Documentation
**Purpose**: Update related documentation files

**Steps**:
1. Find documentation files related to recent work
2. Update status information
3. Add links to new work
4. Update indexes
5. Ensure consistency

**Output**: Updated documentation

---

### Sync 1.5: Verify Link Integrity
**Purpose**: Check and fix broken links

**Steps**:
1. Check for broken links in documentation
2. Verify link targets exist
3. Fix broken links
4. Update link references
5. Report link status

**Output**: Link integrity report

---

## Execution Flow

```
Sync 1.1: Identify Recent Work
  ↓
Sync 1.2: Update Devlog
  ↓
Sync 1.3: Sync Work Effort Status
  ↓
Sync 1.4: Update Related Documentation
  ↓
Sync 1.5: Verify Link Integrity
  ↓
✅ Complete - Sync report displayed
```

---

## Output Format

### Console Output

The command provides sync summary:

```
🔄 Sync: Documentation Synchronization

Recent Work Identified:
  - 3 work efforts with updates
  - 5 devlog entries to add
  - 2 documentation files to update

Devlog Updates:
  ✅ Added 5 entries
  ✅ Updated timestamps
  ✅ Formatted correctly

Work Effort Sync:
  ✅ WE-260112-g0ih: Status synced
  ✅ WE-260112-dr0f: Progress updated
  ✅ WE-260112-jr7r: Tickets synced

Documentation Updates:
  ✅ Updated COMMAND_RECOMMENDATIONS.md
  ✅ Updated help.md
  ✅ Updated work effort indexes

Link Integrity:
  ✅ All links verified
  ✅ 0 broken links found

Files Updated:
  - _work_efforts/devlog.md
  - _work_efforts/WE-260112-g0ih_*/index.md
  - .cursor/commands/COMMAND_RECOMMENDATIONS.md
  - .cursor/commands/help.md

⏱️  Sync complete: 4.2s
```

---

## What Gets Synced

### Devlog Updates
- Recent work effort entries
- Recent ticket completions
- Recent file changes
- Recent decisions

### Work Effort Status
- Work effort status files
- Ticket statuses
- Progress notes
- Completion dates

### Related Documentation
- Command documentation
- Help files
- Index files
- README files

### Link Integrity
- Broken link detection
- Link target verification
- Link reference updates

---

## Use Cases

### 1. Post-Session Sync
**Scenario**: After work session, sync all documentation

**Example**:
```
User: "/sync"
```

**Output**: All documentation synced

---

### 2. Manual Sync Needed
**Scenario**: Documentation is out of sync, need to fix

**Example**:
```
User: "/sync"
```

**Output**: Documentation synchronized

---

### 3. Regular Maintenance
**Scenario**: Regular sync to keep docs current

**Example**:
```
User: "/sync"
```

**Output**: Documentation updated

---

## Integration with Other Commands

- **`/checkpoint`**: Creates checkpoint (`/sync` keeps docs in sync)
- **`/context`**: Provides context (`/sync` updates context docs)
- **`/status`**: Shows status (`/sync` updates status docs)
- **`/links`**: Creates links (`/sync` verifies link integrity)

---

## When to Use

**Use `/sync` when**:
- ✅ Documentation is out of sync
- ✅ After work session
- ✅ Need to ensure consistency
- ✅ Want to update all related docs
- ✅ Regular maintenance

**Don't use `/sync` when**:
- ❌ Need quick status (use `/status`)
- ❌ Need context (use `/context`)
- ❌ Need checkpoint (use `/checkpoint`)

---

## Technical Details

### Tools Used

**File System**:
- `find` - Find documentation files
- `grep` - Search for patterns
- File reading/writing operations

**MCP Servers** (if available):
- `mcp_work-efforts_list_work_efforts` - Work efforts
- `mcp_work-efforts_list_tickets` - Tickets
- `mcp_docs-maintainer_rebuild_indices` - Rebuild indexes

**Git Commands**:
- `git status` - Check for changes
- `git log --oneline -10` - Recent commits

### Performance

- **Target Time**: < 10 seconds
- **Work Identification**: ~2 seconds
- **Devlog Update**: ~2 seconds
- **Work Effort Sync**: ~2 seconds
- **Documentation Update**: ~2 seconds
- **Link Verification**: ~2 seconds

### Error Handling

- **File Errors**: Show "Unable to update" and continue
- **MCP Errors**: Fall back to file system operations
- **Link Errors**: Report broken links, continue
- **Always Complete**: Always show what was synced

---

## Example Workflow

```
User: "/sync"

AI: 🔄 Sync: Documentation Synchronization

Recent Work: 3 work efforts, 5 devlog entries
Devlog: ✅ Updated (5 entries added)
Work Efforts: ✅ Synced (3 updated)
Documentation: ✅ Updated (2 files)
Links: ✅ Verified (0 broken)

Files Updated: 6
⏱️  Sync complete: 4.1s

User: [Documentation is now in sync]
```

---

## Advanced Features

### Dry Run Mode
Preview what would be synced:
```bash
/sync --dry-run    # Show what would be synced
```

### Focus Areas
Sync specific areas:
```bash
/sync --devlog     # Devlog only
/sync --work       # Work efforts only
/sync --docs       # Documentation only
/sync --links      # Links only
```

### Verbose Mode
Get detailed output:
```bash
/sync --verbose    # Detailed sync information
```

---

## Best Practices

1. **Run Regularly**: Sync after work sessions
2. **Verify Before**: Check what will be synced
3. **Review Changes**: Review synced changes
4. **Fix Issues**: Address any sync issues
5. **Keep Consistent**: Maintain documentation consistency

---

## Output Location

Sync operations update files in place. A summary is displayed in console.

For detailed sync log:
- Use `--verbose` flag for detailed output
- Review git diff to see changes

---

**This command keeps documentation synchronized across the project - essential for maintaining consistency and accuracy.**
