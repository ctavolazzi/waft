# Empirica Dashboard Usage Guide

## Overview

The `waft empirica monitor` command launches Empirica's terminal-based dashboard for real-time monitoring of epistemic state, CASCADE workflows, and project activity.

## Quick Start

```bash
# Launch TUI dashboard (recommended)
waft empirica monitor --type tui

# Launch snapshot monitor (curses-based)
waft empirica monitor --type snapshot

# Launch CASCADE monitor (curses-based, minimalist)
waft empirica monitor --type cascade

# Monitor specific session
waft empirica monitor --session-id abc-123

# Specify project path
waft empirica monitor --path /path/to/project
```

## What the Dashboard Shows

### 1. Project Context
- Project name
- Database path
- Git repository path

### 2. Current Activity
- Active session ID and AI identifier
- Session duration
- Current CASCADE phase (PREFLIGHT, INVESTIGATE, CHECK, ACT, POSTFLIGHT)
- Time spent in current phase

### 3. Epistemic Vectors
- 13 epistemic vectors (engagement, know, do, context, clarity, coherence, signal, density, state, change, completion, impact, uncertainty)
- Vector deltas (changes between latest and previous)

### 4. Recent Activity
- Recent findings (discoveries logged)
- Recent unknowns (knowledge gaps logged)
- Timestamps for each event

## Populating the Dashboard with Data

The dashboard shows data from Empirica's CASCADE workflow. To populate it, you need to trigger CASCADE phases.

### Method 1: Use TheOracle (Automatic CASCADE)

**TheOracle automatically runs the full CASCADE workflow:**

```bash
# Ask TheOracle a question - triggers PREFLIGHT → INVESTIGATE → CHECK → ACT → POSTFLIGHT
waft oracle "How should I structure my authentication system?"

# TheOracle will:
# 1. PREFLIGHT: Assess current knowledge
# 2. INVESTIGATE: Reflect on past experiences, log findings/unknowns
# 3. CHECK: Decision gate (PROCEED/HALT/BRANCH/REVISE)
# 4. ACT: Generate recommendation
# 5. POSTFLIGHT: Measure learning deltas
```

**What gets created:**
- Reflexes in `reflexes` table (PREFLIGHT, INVESTIGATE, CHECK, ACT, POSTFLIGHT)
- Epistemic vectors stored
- Findings and unknowns logged
- All visible in dashboard

### Method 2: Use /think Command (CURSOR)

**The `/think` command initializes cognitive tools and creates reflexes:**

```
/think
```

**What gets created:**
- Empirica session (if not exists)
- PREFLIGHT checkpoint
- Epistemic state initialization
- Visible in dashboard

### Method 3: Manual Empirica Commands

**Run CASCADE phases manually:**

```bash
# Create session
waft session create --ai-id claude-code --type development

# PREFLIGHT: Assess current state
waft assess

# Log findings (creates activity)
waft finding log "Discovered X" --impact 0.7

# Log unknowns (creates activity)
waft unknown log "Need to investigate Y"

# CHECK: Decision gate
waft check --operation '{"type": "code_generation", "scope": "high"}'

# POSTFLIGHT: Measure learning (after completing work)
# This is typically done automatically by TheOracle
```

### Method 4: Use /run-it Command (CURSOR)

**The `/run-it` command runs a comprehensive workflow that includes Empirica:**

```
/run-it
```

**What gets created:**
- `/think` phase creates PREFLIGHT
- `/check-assumptions` logs findings/unknowns
- `/verify` logs verification results
- `/reflect` creates POSTFLIGHT
- All visible in dashboard

## Prompting AI Systems to Use the Dashboard

### For Monitoring Current State

**Prompt:**
```
"Show me the current epistemic state using the Empirica dashboard"
"Launch the Empirica TUI dashboard to monitor project activity"
"Open the dashboard to see what we know and don't know"
```

**Command:**
```bash
waft empirica monitor --type tui
```

### For Triggering CASCADE Workflow

**Prompt:**
```
"Consult TheOracle about [topic]" - Triggers full CASCADE
"Run /think to initialize cognitive tools" - Creates PREFLIGHT
"Use /run-it for comprehensive workflow" - Runs full CASCADE cycle
```

**Commands:**
```bash
waft oracle "your question here"
# Or use CURSOR commands: /think, /run-it
```

### For Logging Findings/Unknowns

**Prompt:**
```
"Log this discovery: [finding]"
"Record that we don't know: [unknown]"
"Track this knowledge gap"
```

**Commands:**
```bash
waft finding log "your discovery" --impact 0.7
waft unknown log "what you don't know"
```

### For Decision Gates

**Prompt:**
```
"Check if it's safe to proceed with [operation]"
"Run a safety gate check"
"Assess if we should continue"
```

**Command:**
```bash
waft check --operation '{"type": "code_generation", "scope": "high"}'
```

## Integration with AI Workflows

### Example: Starting New Work

**Prompt to AI:**
```
"Before we start, run /think to initialize cognitive tools and assess what we know. 
Then consult TheOracle about the best approach. Monitor progress in the dashboard."
```

**What happens:**
1. `/think` creates PREFLIGHT checkpoint
2. `waft oracle` runs full CASCADE workflow
3. Dashboard shows all phases and epistemic state
4. You can monitor in real-time

### Example: During Development

**Prompt to AI:**
```
"As you work, log findings and unknowns to Empirica. 
Keep the dashboard open to track epistemic state."
```

**What happens:**
- AI logs discoveries: `waft finding log "discovery" --impact 0.7`
- AI logs gaps: `waft unknown log "gap"`
- Dashboard updates in real-time (press `r` to refresh)
- Recent activity shows all logged items

### Example: Before Major Decisions

**Prompt to AI:**
```
"Before making this decision, run a CHECK gate and show me the dashboard."
```

**What happens:**
1. `waft check` creates CHECK checkpoint
2. Dashboard shows decision (PROCEED/HALT/BRANCH/REVISE)
3. You can see confidence level and reasoning

### Example: After Completing Work

**Prompt to AI:**
```
"Now that we're done, run POSTFLIGHT to measure what we learned. 
Show me the epistemic deltas in the dashboard."
```

**What happens:**
1. POSTFLIGHT calculates learning deltas
2. Dashboard shows knowledge increase, uncertainty decrease
3. Epistemic vectors panel shows changes

## Dashboard Controls

### TUI Dashboard
- `q` - Quit
- `r` - Refresh (updates data)
- `c` - Clear errors
- Arrow keys - Navigate (if multiple panels)
- `^p` - Open palette (Textual command palette)

### Snapshot Monitor
- `q` - Quit
- `r` - Refresh
- `f` - Full view
- `e` - Export data
- `d` - Details

### CASCADE Monitor
- `q` - Quit
- Auto-refreshes (event-driven)

## Understanding Dashboard Data

### "No reflexes yet"
- **Meaning**: No CASCADE workflow has run in this session yet
- **Solution**: Run `/think`, `waft oracle`, or `/run-it` to create reflexes

### "No epistemic data yet"
- **Meaning**: No entries in `epistemic_snapshots` table
- **Solution**: Run PREFLIGHT/POSTFLIGHT workflows (via TheOracle or `/think`)

### Recent Activity Shows "N/A" Timestamps
- **Fixed**: Dashboard now correctly uses `created_timestamp` column
- **If still showing N/A**: Data might be from before the fix, or timestamps are NULL

## Best Practices

### 1. Start with /think
Always initialize cognitive tools before major work:
```
/think
```

### 2. Use TheOracle for Guidance
Consult TheOracle for epistemic-aware guidance:
```bash
waft oracle "your question"
```

### 3. Log as You Work
Have AI log findings and unknowns during development:
```bash
waft finding log "discovery" --impact 0.7
waft unknown log "knowledge gap"
```

### 4. Monitor in Real-Time
Keep dashboard open in separate terminal:
```bash
waft empirica monitor --type tui
# Press 'r' to refresh periodically
```

### 5. Check Before Major Operations
Run CHECK gates before risky operations:
```bash
waft check --operation '{"type": "code_generation", "scope": "high"}'
```

## Troubleshooting

### Dashboard Shows Errors
- **Timezone errors**: Fixed in patches (should not appear)
- **Timestamp errors**: Fixed in patches (should not appear)
- **Column errors**: Fixed in patches (should not appear)

### No Data Showing
- **Check session**: `waft session status`
- **Create session**: `waft session create`
- **Run CASCADE**: Use `/think` or `waft oracle`

### Dashboard Won't Launch
- **Check Empirica**: `empirica --version`
- **Check textual**: Should be installed in system Python
- **Check dependencies**: `waft empirica monitor --help` should work

## Integration Examples

### Example 1: Starting a New Feature

**User prompt:**
```
"I want to add user authentication. First, consult TheOracle about the best approach, 
then open the dashboard to monitor our epistemic state as we work."
```

**AI should:**
1. Run `waft oracle "What's the best approach for user authentication?"`
2. Launch `waft empirica monitor --type tui` in background/separate terminal
3. As work progresses, log findings: `waft finding log "OAuth2 uses PKCE" --impact 0.8`
4. Log unknowns: `waft unknown log "Token refresh flow details"`

### Example 2: Debugging an Issue

**User prompt:**
```
"We have a bug. Use /think to assess what we know, then investigate and log findings. 
Keep the dashboard open to track our learning."
```

**AI should:**
1. Run `/think` (creates PREFLIGHT)
2. Investigate the bug
3. Log findings: `waft finding log "Bug is in authentication middleware" --impact 0.9`
4. Log unknowns: `waft unknown log "Why does it fail in production?"`
5. Dashboard shows all logged items

### Example 3: Making a Decision

**User prompt:**
```
"Should we refactor this code? Run a CHECK gate first, then show me the dashboard."
```

**AI should:**
1. Run `waft check --operation '{"type": "refactoring", "scope": "medium"}'`
2. Launch dashboard: `waft empirica monitor --type tui`
3. Dashboard shows decision (PROCEED/HALT/BRANCH/REVISE) and confidence

## Summary

**To populate dashboard:**
- Use `/think` - Creates PREFLIGHT
- Use `waft oracle` - Runs full CASCADE (PREFLIGHT → POSTFLIGHT)
- Use `/run-it` - Comprehensive workflow with CASCADE
- Manually log: `waft finding log`, `waft unknown log`, `waft check`

**To monitor:**
- `waft empirica monitor --type tui` - Full dashboard
- `waft empirica monitor --type snapshot` - Memory quality monitor
- `waft empirica monitor --type cascade` - CASCADE workflow monitor

**Key prompts for AI:**
- "Use /think to initialize cognitive tools"
- "Consult TheOracle about [topic]"
- "Log this discovery: [finding]"
- "Run a CHECK gate before proceeding"
- "Show me the epistemic dashboard"
