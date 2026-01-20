# AI Prompts for Empirica Dashboard

Quick reference for prompting AI systems (like Claude, GPT, etc.) to use the Empirica dashboard and trigger CASCADE workflows.

## Quick Reference

### Launch Dashboard
```
"Open the Empirica dashboard to monitor epistemic state"
"Show me the current epistemic state using the dashboard"
"Launch the TUI dashboard"
```

### Trigger CASCADE Workflow
```
"Consult TheOracle about [topic]" - Full CASCADE
"Run /think to initialize cognitive tools" - PREFLIGHT
"Use /run-it for comprehensive workflow" - Full CASCADE
```

### Log Findings/Unknowns
```
"Log this discovery: [finding]"
"Record that we don't know: [unknown]"
"Track this knowledge gap"
```

### Decision Gates
```
"Check if it's safe to proceed with [operation]"
"Run a safety gate check"
"Assess if we should continue"
```

## Detailed Prompts

### Starting New Work

**Prompt:**
```
Before we start working on [task], please:
1. Run /think to initialize cognitive tools and assess what we know
2. Consult TheOracle about the best approach: "What's the best way to [task]?"
3. Open the Empirica dashboard so I can monitor our epistemic state
4. As you work, log any discoveries as findings and knowledge gaps as unknowns
```

**What AI should do:**
1. Execute `/think` command (creates PREFLIGHT)
2. Run `waft oracle "What's the best way to [task]?"` (full CASCADE)
3. Launch `waft empirica monitor --type tui` (in background or separate terminal)
4. During work: `waft finding log "discovery" --impact 0.7`
5. During work: `waft unknown log "knowledge gap"`

### During Development

**Prompt:**
```
As you implement [feature], please:
- Log discoveries as findings with impact scores
- Log knowledge gaps as unknowns
- Run CHECK gates before risky operations
- Keep the dashboard open to track epistemic state
```

**What AI should do:**
- `waft finding log "discovery" --impact 0.7` for each discovery
- `waft unknown log "gap"` for each knowledge gap
- `waft check --operation '{"type": "code_generation", "scope": "high"}'` before risky ops
- Dashboard shows all logged items in real-time

### Before Major Decisions

**Prompt:**
```
Before we decide on [decision], please:
1. Run a CHECK gate to assess if it's safe to proceed
2. Show me the dashboard so I can see the decision and confidence level
3. If PROCEED, continue. If HALT/BRANCH/REVISE, explain why and what to do
```

**What AI should do:**
1. `waft check --operation '{"type": "[operation_type]", "scope": "[scope]"}'`
2. `waft empirica monitor --type tui` (or show output)
3. Interpret decision and act accordingly

### After Completing Work

**Prompt:**
```
Now that we've completed [task], please:
1. Run POSTFLIGHT to measure what we learned
2. Show me the epistemic deltas in the dashboard
3. Summarize the learning (knowledge increase, uncertainty decrease)
```

**What AI should do:**
1. POSTFLIGHT is typically automatic via TheOracle
2. `waft empirica monitor --type tui` to show deltas
3. Explain learning measurements

### Debugging Issues

**Prompt:**
```
We have a bug: [description]. Please:
1. Use /think to assess what we know about this issue
2. Investigate and log findings as you discover them
3. Log unknowns for things we need to investigate
4. Keep the dashboard open to track our investigation
```

**What AI should do:**
1. `/think` (PREFLIGHT)
2. Investigate bug
3. `waft finding log "root cause: X" --impact 0.9`
4. `waft unknown log "why does it happen in production?"`
5. Dashboard shows investigation progress

## Integration Patterns

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

### Pattern 2: Learning-Focused Work

**Prompt:**
```
Focus on learning and tracking knowledge:
- Log every discovery as a finding
- Log every question as an unknown
- Use TheOracle for guidance when uncertain
- Show me the dashboard periodically to see what we're learning
```

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

## Command Reference for AI

### Dashboard Commands
```bash
waft empirica monitor --type tui         # Launch TUI dashboard
waft empirica monitor --type snapshot    # Launch snapshot monitor
waft empirica monitor --type cascade     # Launch CASCADE monitor
waft empirica monitor --session-id ID    # Monitor specific session
```

### CASCADE Workflow Commands
```bash
waft oracle "question"                   # Full CASCADE (PREFLIGHT → POSTFLIGHT)
waft session create                      # Create session (if needed)
waft assess                             # Show epistemic assessment
waft check                              # Decision gate
```

### Logging Commands
```bash
waft finding log "discovery" --impact 0.7    # Log finding
waft unknown log "knowledge gap"              # Log unknown
```

## Example Full Workflow

**User prompt:**
```
I want to add OAuth2 authentication. Use an epistemic-aware approach:
1. Consult TheOracle about best practices
2. Open the dashboard to monitor
3. As you implement, log discoveries and gaps
4. Run CHECK gates before major changes
```

**AI execution:**
```bash
# Step 1: Consult TheOracle (triggers CASCADE)
waft oracle "What are the best practices for implementing OAuth2 authentication?"

# Step 2: Open dashboard (in background/separate terminal)
waft empirica monitor --type tui

# Step 3: During implementation, log findings
waft finding log "OAuth2 requires PKCE for mobile apps" --impact 0.8
waft finding log "Token refresh should use refresh_token grant" --impact 0.7
waft unknown log "How to handle token expiration in background jobs?"

# Step 4: Before major changes, run CHECK
waft check --operation '{"type": "code_generation", "scope": "high"}'

# Dashboard shows:
# - PREFLIGHT/POSTFLIGHT from TheOracle
# - All logged findings/unknowns
# - CHECK gate decisions
# - Epistemic vectors and deltas
```

## Key Points for AI Systems

1. **Dashboard is read-only monitoring** - It shows data but doesn't create it
2. **CASCADE workflows create the data** - Use TheOracle, /think, or /run-it
3. **Logging populates activity** - Use `waft finding log` and `waft unknown log`
4. **CHECK gates create decision points** - Use `waft check` before risky operations
5. **Dashboard auto-refreshes** - Press `r` to manually refresh if needed

## Troubleshooting Prompts

**If dashboard shows "No reflexes yet":**
```
"The dashboard shows no reflexes. Please run /think to initialize cognitive tools 
and create a PREFLIGHT checkpoint."
```

**If dashboard shows "No epistemic data yet":**
```
"The dashboard shows no epistemic data. Please consult TheOracle about something 
to trigger the CASCADE workflow and populate epistemic vectors."
```

**If dashboard shows errors:**
```
"The dashboard is showing errors. Please check if Empirica is properly installed 
and if textual is available in the system Python."
```
