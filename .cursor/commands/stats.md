# Stats

**Show session statistics - files created, lines written, activity tracking.**

Displays comprehensive statistics about the current chat session, including files created, lines written, files modified, and other activity metrics. Useful for tracking productivity, understanding scope of work, and getting a quick overview of session activity.

**Use when:** You want to see what was accomplished in this session, track productivity, or get a summary of work done.

---

## Purpose

This command provides:
- **Session Statistics**: Files created, modified, deleted
- **Code Metrics**: Lines written, files changed
- **Activity Summary**: Commands run, work completed
- **Time Tracking**: Session duration (if available)
- **Productivity Metrics**: Files per hour, lines per file, etc.

---

## Philosophy

1. **Transparency**: Show what was actually done
2. **Metrics**: Quantify the work accomplished
3. **Useful**: Help understand scope and productivity
4. **Non-intrusive**: Lightweight, doesn't slow down work
5. **Session-focused**: Track current session, not all-time

---

## What Gets Tracked

### Files
- **Created**: New files added
- **Modified**: Existing files changed
- **Deleted**: Files removed
- **Total**: Sum of all file operations

### Code Metrics
- **Lines Written**: Total lines added
- **Lines Modified**: Lines changed in existing files
- **Lines Deleted**: Lines removed
- **Net Change**: Lines added - lines deleted

### Activity
- **Commands Executed**: Cursor commands run
- **Work Efforts**: Created or updated
- **Documentation**: Files documented
- **Tests**: Tests written or updated

### Time (if available)
- **Session Start**: When session began
- **Session Duration**: How long session has been active
- **Files per Hour**: Productivity metric

---

## Execution Steps

1. **Scan Workspace**
   - Check git status for modified files
   - Identify new files (untracked)
   - Check deleted files (if git tracked)

2. **Calculate Metrics**
   - Count lines in new files
   - Count lines changed (git diff)
   - Calculate net changes

3. **Gather Activity**
   - List commands executed (from chat history)
   - Check work efforts created/updated
   - Identify documentation changes

4. **Calculate Statistics**
   - Files per hour (if time available)
   - Average lines per file
   - Most active file types
   - Most changed files

5. **Display Results**
   - Formatted statistics table
   - Breakdown by category
   - Top files by changes
   - Summary metrics

---

## Output Format

### Summary Table

```
📊 Session Statistics

Files:
  Created:    5 files
  Modified:   8 files
  Deleted:    0 files
  Total:      13 operations

Code:
  Lines Written:    1,247 lines
  Lines Modified:     342 lines
  Lines Deleted:       12 lines
  Net Change:       1,577 lines

Activity:
  Commands Run:       3 commands
  Work Efforts:       1 created
  Documentation:      4 files updated

Top Files by Changes:
  1. visualizer.py        +687 lines
  2. decision_matrix.py   +439 lines
  3. phase1.md           +378 lines
  4. visualize.md         +278 lines
  5. decide.md            +267 lines

File Types:
  Python:     2 files  (+1,126 lines)
  Markdown:   3 files  (+923 lines)
  JSON:       0 files  (0 lines)

Productivity:
  Files/Hour:  2.5 files/hour
  Lines/Hour:  628 lines/hour
  Avg/File:    249 lines/file
```

### Detailed Breakdown

- **By Category**: Files grouped by type
- **By Activity**: Files grouped by operation (create/modify/delete)
- **Top Contributors**: Files with most changes
- **Time Analysis**: If session timing available

---

## Use Cases

### 1. Session Summary
**Scenario**: Want to see what was accomplished

**Example**:
```
User: "/stats"
```

**Output**: Complete session statistics

---

### 2. Productivity Check
**Scenario**: Want to track productivity

**Example**:
```
User: "/stats"
```

**Output**: Files/hour, lines/hour metrics

---

### 3. Scope Assessment
**Scenario**: Need to understand scope of work

**Example**:
```
User: "/stats"
```

**Output**: Detailed breakdown of all changes

---

### 4. Documentation
**Scenario**: Creating session report

**Example**:
```
User: "/stats"
```

**Output**: Statistics to include in report

---

## Options

### Basic Stats (Default)
```bash
/stats
```
- Shows summary statistics
- Files and lines counts
- Top files by changes

### Detailed Stats
```bash
/stats --detailed
```
- Full breakdown
- All files listed
- Time analysis
- Category breakdowns

### Export Stats
```bash
/stats --export
```
- Save statistics to file
- JSON format
- Save to `_pyrite/phase1/` or similar

---

## Statistics Calculated

### File Metrics
- Total files created
- Total files modified
- Total files deleted
- Files by type (Python, Markdown, etc.)
- Files by category (commands, core, tests, etc.)

### Code Metrics
- Total lines written
- Total lines modified
- Total lines deleted
- Net line change
- Average lines per file
- Largest file created
- Most changed file

### Activity Metrics
- Commands executed
- Work efforts created/updated
- Documentation files updated
- Tests written/updated

### Productivity Metrics
- Files per hour (if time available)
- Lines per hour (if time available)
- Average lines per file
- Most productive file type

---

## Integration with Other Commands

- **`/checkpoint`**: May include stats in checkpoint
- **`/phase1`**: Stats can be part of Phase 1 output
- **`/visualize`**: Stats can be visualized in dashboard
- **`/verify`**: Can verify stats accuracy

---

## When to Use

**Use `/stats` when**:
- ✅ Want to see session summary
- ✅ Need productivity metrics
- ✅ Creating session reports
- ✅ Understanding scope of work
- ✅ Tracking activity

**Don't use `/stats` when**:
- ❌ Need real-time file status (use `git status`)
- ❌ Need detailed file contents (use file readers)
- ❌ Need historical stats (this is session-only)

---

## Technical Details

### Data Sources

- **Git Status**: For modified/deleted files
- **File System**: For new files
- **Git Diff**: For line change counts
- **Chat History**: For commands executed (if available)
- **Work Efforts**: For work effort activity

### Calculations

- **Lines Written**: Sum of all lines in new files
- **Lines Modified**: Git diff additions
- **Lines Deleted**: Git diff deletions
- **Net Change**: Additions - deletions

### Accuracy

- **Git-based**: Uses git for accurate change tracking
- **Real-time**: Shows current state
- **Session-scoped**: Only current session, not all-time

---

## Example Output

```
📊 Session Statistics

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Files:
  ✅ Created:    5 files
  📝 Modified:   8 files
  🗑️  Deleted:    0 files
  ────────────────────────────────────────────────────────────────────────────────
  📦 Total:      13 file operations

Code:
  ➕ Lines Written:    1,247 lines
  🔄 Lines Modified:     342 lines
  ➖ Lines Deleted:       12 lines
  ────────────────────────────────────────────────────────────────────────────────
  📊 Net Change:       1,577 lines added

Activity:
  ⚡ Commands:           3 commands executed
  📋 Work Efforts:       1 created
  📚 Documentation:      4 files updated

Top Files by Changes:
  1. 📄 visualizer.py        +687 lines  (new)
  2. 📄 decision_matrix.py   +439 lines  (new)
  3. 📄 phase1.md           +378 lines  (new)
  4. 📄 visualize.md         +278 lines  (new)
  5. 📄 decide.md            +267 lines  (new)

File Types:
  🐍 Python:     2 files  (+1,126 lines)
  📝 Markdown:   3 files  (+923 lines)
  ⚙️  Config:     0 files  (0 lines)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 Tip: Use /checkpoint to save this session's work
```

---

## Advanced Features

### Session Timing
If session start time is available:
- Calculate session duration
- Files per hour
- Lines per hour
- Productivity trends

### Historical Comparison
Compare with previous sessions:
- Files vs last session
- Lines vs last session
- Productivity trends

### Export Options
- Save as JSON
- Save as Markdown
- Include in checkpoint
- Add to devlog

---

**This command helps you understand what was accomplished in the current session with quantified metrics.**
