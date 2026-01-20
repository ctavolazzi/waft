#!/usr/bin/env python3
"""
Generate PDF Documentation for /status Command
===============================================

Creates a professional PDF document about the /status Cursor command.
"""

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.evolution.pdf_generator import PDFGenerator


def create_status_command_content() -> str:
    """Create markdown content for /status command PDF."""

    content = """# /status Command Documentation

**Quick, Immediate Status Report - Current State Snapshot in Seconds**

---

## Overview

The `/status` command provides a fast, concise status check of the current project state. It focuses on essential information: git status, active work, recent changes, and quick health indicators. Designed for immediate awareness without comprehensive analysis.

**Execution Time**: < 5 seconds
**Output**: Console display only (no files created)
**Purpose**: Quick status awareness without interrupting workflow

---

## Philosophy

1. **Speed First**: Get status in seconds, not minutes
2. **Essentials Only**: Focus on what matters right now
3. **Actionable**: Information you can act on immediately
4. **No Analysis**: Just facts, no deep analysis
5. **Current State**: What's happening now, not history

---

## What Gets Checked

### Git Status
- Current branch name
- Uncommitted files count (staged vs unstaged)
- Commits ahead/behind remote (if applicable)
- Quick overview via `git status --short`

### Active Work
- Active work efforts (names only)
- Current working directory context
- Recent devlog activity

### Recent Activity
- Last 3-5 commits
- Last 5-10 modified files
- Last 2-3 devlog entries

### Health Indicators
- Project structure validity (basic check)
- Obvious issues detection
- Dependency status (if quick to check)

---

## Execution Phases

### Status 1.1: Quick Git Check
**Purpose**: Get immediate git status

**Actions**:
1. Run `git status --short` for quick overview
2. Get current branch name
3. Count uncommitted files
4. Check commits ahead/behind (if applicable)

**Output**: Git status summary

---

### Status 1.2: Active Work Check
**Purpose**: See what's currently being worked on

**Actions**:
1. Check for active work efforts (via MCP or file system)
2. List active work effort names
3. Check for recent devlog entries
4. Identify current working directory context

**Output**: Active work summary

---

### Status 1.3: Recent Activity
**Purpose**: See what changed recently

**Actions**:
1. Check recent file modifications (last 5-10 files)
2. Check recent commits (last 3-5)
3. Check recent devlog entries (last 2-3)

**Output**: Recent activity summary

---

### Status 1.4: Quick Health Check
**Purpose**: Basic health indicators

**Actions**:
1. Check if project structure is valid (basic check)
2. Check for obvious issues (missing files, broken structure)
3. Quick dependency check (if applicable)

**Output**: Health status (✅ Good | ⚠️ Needs Attention | ❌ Issues)

---

## Example Output

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

## Command Options

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

## Command Creation

**Created**: 2026-01-11
**Status**: ✅ Active
**Location**: `.cursor/commands/status.md`
**Global**: Available in all Cursor instances via `~/.cursor/commands/`

---

**This command provides immediate status awareness in seconds - perfect for quick checks and staying aware of current project state without interrupting workflow.**

---

## Quick Reference

**Basic Usage**:
```
/status
```

**Focused Checks**:
```
/status --git
/status --work
/status --activity
/status --health
```

**Output Formats**:
```
/status --verbose
/status --json
```

**Execution Flow**:
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

*Document generated: {timestamp}*
"""

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return content.replace("{timestamp}", timestamp)


def main():
    """Generate PDF documentation for /status command."""
    print("📄 Generating PDF Documentation for /status Command...")
    print()

    # Create content
    print("📝 Creating content...")
    content = create_status_command_content()
    print("✓ Content created")
    print()

    # Generate PDF
    print("🎨 Generating PDF with clinical_standard style...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path("_work_efforts/showcase_documents")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"Status_Command_Documentation_{timestamp}.pdf"

    PDFGenerator.from_content(
        content=content,
        title="/status Command Documentation",
        style="clinical_standard",
        output_path=output_path,
    ).save(str(output_path), open_pdf=False)

    print()
    print("=" * 60)
    print("✅ PDF Generated Successfully!")
    print("=" * 60)
    print(f"📄 Output: {output_path}")
    print("📊 Style: clinical_standard")
    print()

    # Count pages
    try:
        from pypdf import PdfReader

        reader = PdfReader(str(output_path))
        page_count = len(reader.pages)
        print(f"📑 Pages: {page_count}")
    except Exception:
        pass

    print()
    print("💡 Tip: Use `/status` in Cursor to get quick project status!")

    return output_path


if __name__ == "__main__":
    main()
