# Phase 1

**Comprehensive data gathering and visualization - complete project overview.**

Runs a full data collection phase in logical order, gathering all relevant information about the current project state, then generates and opens an interactive visual dashboard. This is your "first phase" command for getting complete insight into what's happening.

**Use when:** You need a comprehensive overview, want to understand the full current state, or need to start a new session with complete context.

---

## Purpose

This command provides:
- **Comprehensive Data Gathering**: Collects all relevant project information
- **Logical Execution Order**: Runs checks in the right sequence
- **Complete State Snapshot**: Full picture of project status
- **Visual Dashboard**: Interactive browser visualization
- **Session Starter**: Perfect for beginning work or handoffs

---

## Philosophy

1. **Complete First**: Gather everything before analyzing
2. **Logical Order**: Run checks in dependency order
3. **Visual Insight**: End with interactive visualization
4. **Comprehensive**: Leave no stone unturned
5. **Fast**: Efficient execution, parallel where possible

---

## Execution Phases

### Phase 1.1: Environment Verification
**Purpose**: Verify basic environment is ready

**Steps**:
1. Check date/time accuracy
2. Verify working directory
3. Check Python version
4. Verify disk space (if available)

**Output**: Environment status

---

### Phase 1.2: Project Discovery
**Purpose**: Identify and validate project

**Steps**:
1. Detect if we're in a waft project
2. Resolve project path
3. Verify project structure exists
4. Check project configuration (pyproject.toml)

**Output**: Project identification and validation

---

### Phase 1.3: Git Status Analysis
**Purpose**: Understand version control state

**Steps**:
1. Check if git is initialized
2. Get current branch
3. Analyze uncommitted changes
4. Check commits ahead/behind
5. Get recent commit history
6. Analyze file changes (added, modified, deleted, untracked)

**Output**: Complete git status breakdown

---

### Phase 1.4: Project Health Check
**Purpose**: Assess project integrity and status

**Steps**:
1. Run `waft verify` (structure validation)
2. Check _pyrite structure validity
3. Verify uv.lock exists
4. Get gamification stats (integrity, level, insight)
5. Check template status

**Output**: Project health assessment

---

### Phase 1.5: Work Effort Discovery
**Purpose**: Identify active and recent work

**Steps**:
1. List active work efforts
2. Get recent work effort activity
3. Read recent devlog entries
4. Check for pending todos (if applicable)

**Output**: Work effort status

---

### Phase 1.6: Memory Layer Analysis
**Purpose**: Understand _pyrite structure

**Steps**:
1. List files in active/
2. List files in backlog/
3. List files in standards/
4. Count files by category
5. Identify recent activity

**Output**: Memory layer status

---

### Phase 1.7: Integration Status
**Purpose**: Check external integrations

**Steps**:
1. Check Empirica initialization status
2. Verify GitHub remote (if applicable)
3. Check dependency status
4. Verify template files exist

**Output**: Integration health

---

### Phase 1.8: Visualization Generation
**Purpose**: Create interactive dashboard

**Steps**:
1. Gather all collected data
2. Save raw state data as JSON
3. Generate HTML dashboard
4. Save both files to `_pyrite/phase1/` folder
5. Open in browser automatically
6. Display file paths

**Output**: Interactive visual dashboard + raw data JSON

---

## Execution Flow

```
Phase 1.1: Environment Verification
  ↓
Phase 1.2: Project Discovery
  ↓
Phase 1.3: Git Status Analysis
  ↓
Phase 1.4: Project Health Check
  ↓
Phase 1.5: Work Effort Discovery
  ↓
Phase 1.6: Memory Layer Analysis
  ↓
Phase 1.7: Integration Status
  ↓
Phase 1.8: Visualization Generation
  ↓
✅ Complete - Dashboard opened in browser
```

---

## What Gets Collected

### Environment
- Date/time
- Working directory
- Python version
- Platform information
- Disk space (if available)

### Project
- Project name and version
- Project path
- Project structure validity
- Configuration status

### Git
- Repository initialization status
- Current branch
- Uncommitted files (detailed breakdown)
- Commits ahead/behind
- Recent commit history (last 5)
- File change statistics

### Health
- _pyrite structure validity
- uv.lock status
- Integrity percentage
- Current level
- Insight progress
- Template status

### Work
- Active work efforts
- Recent work effort activity
- Recent devlog entries
- Pending items

### Memory
- Active files (count and list)
- Backlog files (count and list)
- Standards files (count and list)
- Recent activity

### Integrations
- Empirica status
- GitHub remote status
- Dependency status
- Template status

---

## Output Format

### Console Output

The command provides progress updates as it runs:

```
🌊 Phase 1: Comprehensive Data Gathering & Visualization

Phase 1.1: Environment Verification
  ✓ Date/time: 2026-01-07 20:25:35 PST
  ✓ Working directory: /Users/ctavolazzi/Code/active/waft
  ✓ Python: 3.10.0
  ✓ Platform: darwin

Phase 1.2: Project Discovery
  ✓ Waft project detected
  ✓ Project path: /Users/ctavolazzi/Code/active/waft
  ✓ Project name: waft
  ✓ Version: 0.0.2

Phase 1.3: Git Status Analysis
  ✓ Git initialized
  ✓ Branch: main
  ✓ Uncommitted files: 54
  ✓ Commits ahead: 4
  ✓ Recent commits: 5 found

Phase 1.4: Project Health Check
  ✓ _pyrite structure: Valid
  ✓ uv.lock: Exists
  ✓ Integrity: 100.0%
  ✓ Level: 1
  ✓ Insight: 0/100

Phase 1.5: Work Effort Discovery
  ✓ Active work efforts: 0
  ✓ Recent devlog entries: 5 found

Phase 1.6: Memory Layer Analysis
  ✓ Active files: 12
  ✓ Backlog files: 0
  ✓ Standards files: 3

Phase 1.7: Integration Status
  ✓ Empirica: Initialized
  ✓ GitHub: Configured
  ✓ Templates: All present

Phase 1.8: Visualization Generation
  📊 Gathering all data...
  ✓ State data saved: phase1-2026-01-07-202535.json
  📄 Generating HTML dashboard...
  ✓ Dashboard created: phase1-2026-01-07-202535.html
  🌐 Opening in browser...
  ✓ Dashboard opened

✅ Phase 1 Complete - All data gathered and visualized
   📁 Output folder: _pyrite/phase1/
   📄 Dashboard: phase1-2026-01-07-202535.html
   📊 Data: phase1-2026-01-07-202535.json
```

### Visual Dashboard

The final step opens an interactive HTML dashboard showing:
- All collected data in organized cards
- Interactive elements (expandable sections)
- Visual indicators (progress bars, status badges)
- Color-coded status
- Complete project overview

---

## Use Cases

### 1. Session Start
**Scenario**: Beginning a new work session

**Example**:
```
User: "/phase1"
```

**Output**: Complete overview, then visual dashboard

---

### 2. Handoff Preparation
**Scenario**: Preparing to hand off work

**Example**:
```
User: "/phase1"
```

**Output**: Complete state snapshot with visualization

---

### 3. Status Check
**Scenario**: Need comprehensive status check

**Example**:
```
User: "/phase1"
```

**Output**: Full status with visual dashboard

---

### 4. Problem Investigation
**Scenario**: Investigating an issue, need full context

**Example**:
```
User: "/phase1"
```

**Output**: Complete state analysis with visualization

---

### 5. Documentation
**Scenario**: Creating documentation snapshot

**Example**:
```
User: "/phase1"
```

**Output**: Complete data + visual dashboard (can be archived)

---

## Integration with Other Commands

- **`/spin-up`**: Quick orientation (Phase 1 is comprehensive version)
- **`/visualize`**: Just visualization (Phase 1 includes full gathering)
- **`/verify`**: Verification checks (Phase 1 includes verification)
- **`/checkpoint`**: Status snapshot (Phase 1 is visual version)
- **`/orient`**: Project orientation (Phase 1 is faster, visual version)

---

## When to Use

**Use `/phase1` when**:
- ✅ Starting a new work session
- ✅ Need comprehensive overview
- ✅ Preparing for handoff
- ✅ Investigating issues
- ✅ Want complete state snapshot
- ✅ Need visual insight into everything

**Don't use `/phase1` when**:
- ❌ Need quick one-liner status (use `/status`)
- ❌ Just want visualization (use `/visualize`)
- ❌ Need deep exploration (use `/explore`)
- ❌ Just need git status (use `git status`)

---

## Technical Details

### Execution Order

The phases run sequentially because:
- **Phase 1.1** (Environment) must succeed before project operations
- **Phase 1.2** (Project) must identify project before other checks
- **Phase 1.3-1.7** can run in parallel but sequential is clearer
- **Phase 1.8** (Visualization) needs all previous data

### Performance

- **Total Time**: ~2-5 seconds (depending on git operations)
- **Parallel Operations**: Some checks can run in parallel
- **Caching**: Results cached during execution for visualization

### Error Handling

- **Graceful Degradation**: Continues if individual checks fail
- **Error Reporting**: Shows which checks failed
- **Partial Results**: Visualization shows available data even if some checks fail

---

## Example Workflow

```
User: "/phase1"

AI: [Runs all 8 phases sequentially]

AI: ✅ Phase 1 Complete
    - Environment: ✓ Ready
    - Project: ✓ waft v0.0.2
    - Git: 54 uncommitted, 4 ahead
    - Health: 100% integrity, Level 1
    - Work: 0 active efforts
    - Memory: 12 active files
    - Integrations: ✓ All working
    - Dashboard: Opened in browser

User: [Reviews dashboard in browser]
```

---

## Advanced Features

### Custom Phases
Can skip phases if needed:
```bash
/phase1 --skip-git
/phase1 --skip-work-efforts
```

### Export Options
- ✅ Data automatically saved as JSON in `_pyrite/phase1/`
- ✅ HTML dashboard saved in `_pyrite/phase1/`
- All outputs organized by timestamp in dedicated folder

### Verbose Mode
- Show detailed output for each phase
- Display raw data
- Show execution times

---

**This command gives you a complete, comprehensive overview of your project state with visual insight - perfect for starting work or understanding current status.**
