# Empirica Dashboard - Quick Reference

## Launch Dashboard
```bash
waft empirica monitor --type tui  # Recommended: Full TUI dashboard
```

## Populate Dashboard Data

### Automatic (Recommended)
```bash
waft oracle "your question"  # Triggers full CASCADE: PREFLIGHT → POSTFLIGHT
```

### Manual
```bash
waft finding log "discovery" --impact 0.7  # Log finding
waft unknown log "knowledge gap"            # Log unknown
waft check                                  # Decision gate
```

## AI Prompts

### To Launch Dashboard
- "Open the Empirica dashboard"
- "Show me the epistemic state dashboard"
- "Launch the TUI monitor"

### To Populate Data
- "Consult TheOracle about [topic]" → Full CASCADE
- "Run /think" → PREFLIGHT checkpoint
- "Use /run-it" → Full CASCADE workflow
- "Log this discovery: [finding]" → Activity entry
- "Run a CHECK gate" → Decision point

### Complete Workflow Prompt
```
"Before we start, run /think to assess what we know. 
Then consult TheOracle about the best approach. 
Open the dashboard to monitor our epistemic state as we work."
```

## What Dashboard Shows

- **Project Context**: Name, database, git repo
- **Current Activity**: Session, duration, CASCADE phase
- **Epistemic Vectors**: 13 vectors with deltas
- **Recent Activity**: Findings and unknowns with timestamps

## Dashboard Controls

- `q` - Quit
- `r` - Refresh
- `c` - Clear errors

## Troubleshooting

**"No reflexes yet"** → Run `/think` or `waft oracle`  
**"No epistemic data yet"** → Run CASCADE workflow  
**Dashboard won't launch** → Check `empirica --version` and `textual` installation
