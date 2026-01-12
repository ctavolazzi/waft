# Status

**Quick, immediate status report - current state snapshot in seconds.**

Provides a fast, concise status check of the current project state. Focuses on essential information: git status, active work, recent changes, and quick health indicators. Designed for immediate awareness without comprehensive analysis.

**Use when:** Need a quick status check, want immediate awareness of current state, or need a fast snapshot before starting work.

---

## Purpose

This command provides:
- **Immediate Status**: Fast status check (< 5 seconds)
- **Essential Information**: Git, work efforts, recent activity
- **Quick Health Check**: Basic health indicators
- **Current State Snapshot**: What's happening right now
- **Minimal Output**: Concise, actionable information

---

## Philosophy

1. **Speed First**: Get status in seconds, not minutes
2. **Essentials Only**: Focus on what matters right now
3. **Actionable**: Information you can act on immediately
4. **No Analysis**: Just facts, no deep analysis
5. **Current State**: What's happening now, not history

---

## Execution Steps

### Status 1.1: Quick Git Check
**Purpose**: Get immediate git status

**Steps**:
1. Run `git status --short` for quick overview
2. Get current branch name
3. Count uncommitted files
4. Check commits ahead/behind (if applicable)

**Output**: Git status summary

---

### Status 1.2: Active Work Check
**Purpose**: See what's currently being worked on

**Steps**:
1. Check for active work efforts (via MCP or file system)
2. List active work effort names
3. Check for recent devlog entries
4. Identify current working directory context

**Output**: Active work summary

---

### Status 1.3: Recent Activity
**Purpose**: See what changed recently

**Steps**:
1. Check recent file modifications (last 5-10 files)
2. Check recent commits (last 3-5)
3. Check recent devlog entries (last 2-3)

**Output**: Recent activity summary

---

### Status 1.4: Quick Health Check
**Purpose**: Basic health indicators

**Steps**:
1. Check if project structure is valid (basic check)
2. Check for obvious issues (missing files, broken structure)
3. Quick dependency check (if applicable)

**Output**: Health status (✅ Good | ⚠️ Needs Attention | ❌ Issues)

---

## Execution Flow

```
Status 1.1: Quick Git Check
  ↓
Status 1.2: Active Work Check
  ↓
Status 1.3: Recent Activity
  ↓
Status 1.4: Quick Health Check
  ↓
✅ Complete - Status displayed
```

---

## Output Format

### Console Output

The command provides immediate status display:

```
📊 Status: Quick Project State

Git:
  Branch: main
  Uncommitted: 3 files (2 modified, 1 new)
  Status: ⚠️  Has uncommitted changes

Active Work:
  Work Efforts: 2 active
    - WE-260111-jpw1_dnd5e_ai_exploration_initiative
    - WE-260111-6ca4_ai-dnd-user_installation_exploration
  Current Directory: _work_efforts/WE-260111-jpw1_dnd5e_ai_exploration_initiative/

Recent Activity:
  Last Commit: 2 hours ago - "Created /deep-analyze command"
  Recent Files: 
    - .cursor/commands/deep-analyze.md (new)
    - .cursor/commands/status.md (new)
    - _work_efforts/devlog.md (modified)
  Devlog: Last entry 2 hours ago

Health:
  Structure: ✅ Valid
  Status: ✅ Good

⏱️  Status check: 2.3s
```

---

## What Gets Checked

### Git Status
- Current branch
- Uncommitted files count
- Staged vs unstaged
- Commits ahead/behind (if applicable)

### Active Work
- Active work efforts (names only)
- Current working directory
- Recent devlog activity

### Recent Activity
- Last 3-5 commits
- Last 5-10 modified files
- Last 2-3 devlog entries

### Health Indicators
- Project structure validity (basic)
- Obvious issues
- Dependency status (if quick to check)

---

## Use Cases

### 1. Quick Check Before Starting
**Scenario**: Starting work session, want quick status

**Example**:
```
User: "/status"
```

**Output**: Immediate status snapshot

---

### 2. Mid-Session Check
**Scenario**: Want to know current state without interrupting flow

**Example**:
```
User: "/status"
```

**Output**: Quick status update

---

### 3. Pre-Commit Check
**Scenario**: Want to see what's changed before committing

**Example**:
```
User: "/status"
```

**Output**: Git status and recent changes

---

### 4. Context Awareness
**Scenario**: Need to understand current context quickly

**Example**:
```
User: "/status"
```

**Output**: Current work and activity summary

---

## Integration with Other Commands

- **`/checkpoint`**: Comprehensive status (`/status` is quick snapshot)
- **`/waft-status`**: Detailed system status (`/status` is minimal)
- **`/spin-up`**: Orientation (`/status` is just current state)
- **`/verify`**: Verification (`/status` is just status check)
- **`/stats`**: Session statistics (`/status` is project state)

---

## When to Use

**Use `/status` when**:
- ✅ Need quick status check (< 5 seconds)
- ✅ Want immediate awareness
- ✅ Need current state snapshot
- ✅ Checking before starting work
- ✅ Want minimal output

**Don't use `/status` when**:
- ❌ Need comprehensive analysis (use `/checkpoint` or `/waft-status`)
- ❌ Need historical trends (use `/analyze`)
- ❌ Need detailed documentation (use `/waft-status --docs`)
- ❌ Need session statistics (use `/stats`)

---

## Technical Details

### Tools Used

**Git Commands**:
- `git status --short` - Quick git status
- `git branch --show-current` - Current branch
- `git log --oneline -5` - Recent commits

**File System**:
- `find` - Recent file modifications
- `ls -lt` - File timestamps

**MCP Servers** (if available):
- `mcp_work-efforts_list_work_efforts` - Active work efforts
- `mcp_filesystem_list_directory` - Directory contents

### Performance

- **Target Time**: < 5 seconds
- **Git Check**: ~1 second
- **Work Check**: ~1 second
- **Activity Check**: ~1 second
- **Health Check**: ~1 second

### Error Handling

- **Git Errors**: Show "Git unavailable" and continue
- **File Errors**: Show "Unable to check" and continue
- **MCP Errors**: Fall back to file system checks
- **Always Complete**: Always show what's available

---

## Example Workflow

```
User: "/status"

AI: 📊 Status: Quick Project State

Git:
  Branch: main
  Uncommitted: 3 files
  Status: ⚠️  Has uncommitted changes

Active Work:
  Work Efforts: 2 active
  Current: WE-260111-jpw1_dnd5e_ai_exploration_initiative

Recent Activity:
  Last Commit: 2 hours ago
  Recent Files: 3 modified

Health: ✅ Good

⏱️  Status check: 2.1s

User: [Sees status, decides next action]
```

---

## Advanced Features

### Focus Areas
Can focus on specific area:
```bash
/status --git          # Git status only
/status --work         # Work efforts only
/status --activity     # Recent activity only
/status --health       # Health check only
```

### Verbose Mode
Get more details:
```bash
/status --verbose      # More detailed output
```

### JSON Output
Get machine-readable output:
```bash
/status --json         # JSON format output
```

---

## Comparison with Related Commands

| Command | Speed | Detail | Use Case |
|---------|-------|--------|----------|
| `/status` | ⚡ Fast (< 5s) | Minimal | Quick check |
| `/checkpoint` | 🐢 Slow (~30s) | Comprehensive | Full snapshot |
| `/waft-status` | 🐢 Slow (~60s) | Very Detailed | System analysis |
| `/spin-up` | 🐢 Slow (~30s) | Detailed | Orientation |
| `/stats` | ⚡ Fast (< 5s) | Session stats | Session metrics |

---

## Best Practices

1. **Run Frequently**: Check status regularly during work
2. **Use Before Commits**: Check status before committing
3. **Use at Session Start**: Quick check when starting work
4. **Keep It Quick**: Don't add analysis, keep it fast
5. **Focus on Now**: Current state, not history

---

## Output Location

Status is displayed in console only. No files are created.

For persistent status:
- Use `/checkpoint` for checkpoint file
- Use `/waft-status --docs` for documentation

---

**This command provides immediate status awareness in seconds - perfect for quick checks and staying aware of current project state without interrupting workflow.**
