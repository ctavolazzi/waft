# Empirica Dashboard Integration - Complete Guide

## Overview

The `waft empirica monitor` command provides real-time monitoring of epistemic state through Empirica's terminal-based dashboards. This document explains how to use it and how to prompt AI systems to leverage it.

## Quick Start

```bash
# Launch dashboard
waft empirica monitor --type tui

# Populate with data (triggers CASCADE workflow)
waft oracle "your question"
```

## How It Works

### Dashboard Types

1. **TUI Dashboard** (Recommended)
   - Full Textual-based terminal UI
   - Shows: Project context, active session, epistemic vectors, recent activity
   - Auto-refreshes every 1-5 seconds
   - Controls: `q` (quit), `r` (refresh), `c` (clear)

2. **Snapshot Monitor**
   - Curses-based
   - Monitors snapshot memory quality
   - Shows compression ratios, reliability scores

3. **CASCADE Monitor**
   - Curses-based, minimalist
   - Monitors PREFLIGHT → POSTFLIGHT workflow
   - Event-driven updates

### Data Sources

The dashboard displays data from:
- **`sessions` table**: Active sessions, duration
- **`reflexes` table**: CASCADE phase checkpoints (PREFLIGHT, INVESTIGATE, CHECK, ACT, POSTFLIGHT)
- **`epistemic_snapshots` table**: 13 epistemic vectors
- **`project_findings` table**: Discoveries logged
- **`project_unknowns` table**: Knowledge gaps logged

## Populating Dashboard Data

### Method 1: TheOracle (Automatic - Recommended)

**Command:**
```bash
waft oracle "your question"
```

**What it does:**
- Runs full CASCADE workflow: PREFLIGHT → INVESTIGATE → CHECK → ACT → POSTFLIGHT
- Creates reflexes for each phase
- Logs findings and unknowns
- Measures learning deltas
- All visible in dashboard

**AI Prompt:**
```
"Consult TheOracle about [topic]"
"Ask TheOracle for guidance on [question]"
```

### Method 2: /think Command (CURSOR)

**Command:**
```
/think
```

**What it does:**
- Initializes cognitive tools
- Creates PREFLIGHT checkpoint
- Sets up epistemic state
- Visible in dashboard

**AI Prompt:**
```
"Run /think to initialize cognitive tools"
"Start with /think to assess what we know"
```

### Method 3: /run-it Command (CURSOR)

**Command:**
```
/run-it
```

**What it does:**
- Comprehensive workflow orchestration
- Includes: /think, /check-assumptions, /verify, /reflect
- Creates multiple CASCADE checkpoints
- All visible in dashboard

**AI Prompt:**
```
"Use /run-it for comprehensive workflow"
"Run the full workflow with /run-it"
```

### Method 4: Manual Logging

**Commands:**
```bash
waft finding log "discovery" --impact 0.7
waft unknown log "knowledge gap"
waft check
waft assess
```

**AI Prompts:**
```
"Log this discovery: [finding]"
"Record that we don't know: [unknown]"
"Run a CHECK gate before proceeding"
```

## Prompting AI Systems

### Pattern 1: Epistemic-Aware Development

**Prompt:**
```
For this task, use an epistemic-aware approach:
1. Start with /think to assess current knowledge
2. Consult TheOracle if uncertainty is high
3. Log findings and unknowns as you work
4. Run CHECK gates before major changes
5. Monitor progress in the dashboard
```

**What AI should do:**
1. Execute `/think`
2. Run `waft oracle "question"` if needed
3. `waft finding log "discovery" --impact 0.7` during work
4. `waft unknown log "gap"` for knowledge gaps
5. `waft check` before risky operations
6. Launch `waft empirica monitor --type tui` to monitor

### Pattern 2: Learning-Focused Work

**Prompt:**
```
Focus on learning and tracking knowledge:
- Log every discovery as a finding
- Log every question as an unknown
- Use TheOracle for guidance when uncertain
- Show me the dashboard periodically to see what we're learning
```

**What AI should do:**
- Actively log findings: `waft finding log "X" --impact 0.7`
- Actively log unknowns: `waft unknown log "Y"`
- Consult TheOracle: `waft oracle "question"`
- Show dashboard: `waft empirica monitor --type tui`

### Pattern 3: Safety-First Development

**Prompt:**
```
Before making any changes, run CHECK gates:
- CHECK before code generation
- CHECK before refactoring
- CHECK before deleting files
- Show dashboard to see decision and confidence
- Only proceed if PROCEED, otherwise explain why not
```

**What AI should do:**
- `waft check --operation '{"type": "code_generation", "scope": "high"}'` before code gen
- `waft check --operation '{"type": "refactoring", "scope": "medium"}'` before refactoring
- `waft check --operation '{"type": "file_deletion", "scope": "high"}'` before deleting
- Show dashboard to display decision
- Only proceed if result is "PROCEED"

## Complete Workflow Example

**User Prompt:**
```
I want to add OAuth2 authentication. Use an epistemic-aware approach:
1. Consult TheOracle about best practices
2. Open the dashboard to monitor
3. As you implement, log discoveries and gaps
4. Run CHECK gates before major changes
5. Show me what we learned at the end
```

**AI Execution:**
```bash
# Step 1: Consult TheOracle (triggers full CASCADE)
waft oracle "What are the best practices for implementing OAuth2 authentication?"

# Step 2: Open dashboard (in background/separate terminal)
waft empirica monitor --type tui

# Step 3: During implementation, log findings
waft finding log "OAuth2 requires PKCE for mobile apps" --impact 0.8
waft finding log "Token refresh should use refresh_token grant" --impact 0.7
waft unknown log "How to handle token expiration in background jobs?"

# Step 4: Before major changes, run CHECK
waft check --operation '{"type": "code_generation", "scope": "high"}'

# Step 5: Show learning summary
waft assess --history
```

**Dashboard Shows:**
- PREFLIGHT/POSTFLIGHT from TheOracle
- All logged findings/unknowns with timestamps
- CHECK gate decisions
- Epistemic vectors and deltas
- Learning measurements

## Understanding Dashboard Messages

### "No reflexes yet"
- **Meaning**: No CASCADE workflow has run in this session
- **Solution**: Run `/think`, `waft oracle`, or `/run-it`
- **AI Prompt**: "The dashboard shows no reflexes. Please run /think to initialize."

### "No epistemic data yet"
- **Meaning**: No entries in `epistemic_snapshots` table
- **Solution**: Run CASCADE workflow (TheOracle or /think)
- **AI Prompt**: "The dashboard shows no epistemic data. Please consult TheOracle to trigger CASCADE."

### Recent Activity Shows Data
- **Good**: Dashboard is working and showing logged findings/unknowns
- **Timestamps**: Should show `HH:MM:SS` format (fixed in patches)
- **AI Prompt**: "Great! The dashboard is showing recent activity. Keep logging as we work."

## Integration Checklist

When starting new work, AI should:

- [ ] Run `/think` to initialize cognitive tools
- [ ] Consult TheOracle if uncertainty is high
- [ ] Launch dashboard: `waft empirica monitor --type tui`
- [ ] Log findings during work: `waft finding log "X" --impact 0.7`
- [ ] Log unknowns: `waft unknown log "Y"`
- [ ] Run CHECK gates before risky operations
- [ ] Show dashboard periodically to track progress

## Key Files

- **Usage Guide**: [EMPIRICA_DASHBOARD_USAGE.md](EMPIRICA_DASHBOARD_USAGE.md)
- **AI Prompts**: [AI_PROMPTS_EMPIRICA_DASHBOARD.md](AI_PROMPTS_EMPIRICA_DASHBOARD.md)
- **Quick Reference**: [EMPIRICA_DASHBOARD_QUICK_REFERENCE.md](EMPIRICA_DASHBOARD_QUICK_REFERENCE.md)
- **CASCADE Workflow**: [ORACLE_EMPIRICA_WORKFLOW.md](ORACLE_EMPIRICA_WORKFLOW.md)

## Summary

**To use the dashboard:**
1. Launch: `waft empirica monitor --type tui`
2. Populate: Use TheOracle (`waft oracle`), `/think`, or `/run-it`
3. Monitor: Watch epistemic state, activity, and learning in real-time

**To prompt AI:**
- "Use /think to initialize cognitive tools"
- "Consult TheOracle about [topic]"
- "Log this discovery: [finding]"
- "Run a CHECK gate before proceeding"
- "Open the dashboard to monitor our epistemic state"
