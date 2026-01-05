# Empirica Enhanced Integration

**Created**: 2026-01-04
**Purpose**: Enhanced integration based on full Empirica 1.2.3 feature set

---

## What We Learned from Empirica README

### Key Features We Should Support

1. **✅ Project Bootstrap** - Critical for session continuity (~800 tokens)
2. **✅ Finding/Unknown Logging** - Track discoveries and gaps
3. **✅ CHECK Gates** - Safety gates (PROCEED/HALT/BRANCH/REVISE)
4. **✅ Goal Management** - Create goals with epistemic scope
5. **✅ State Assessment** - Assess current epistemic state
6. **⏳ Sentinel Safety Gates** - Full workflow orchestration (future)
7. **⏳ Multi-Agent Coordination** - agent-spawn, agent-aggregate (future)
8. **⏳ Trajectory Projection** - trajectory-project (future)
9. **⏳ Drift Detection** - check-drift (future)
10. **⏳ Persona System** - persona-list, persona-find (future)

---

## Enhanced EmpiricaManager

### New Methods Added

```python
from waft.core.empirica import EmpiricaManager

empirica = EmpiricaManager(project_path)

# 1. Project Bootstrap - Load compressed context (~800 tokens)
context = empirica.project_bootstrap()
# Returns: {"epistemic_state": {...}, "goals": [...], "findings": [...], "unknowns": [...]}

# 2. Log Findings - Track discoveries
empirica.log_finding("Discovered X", impact=0.7)

# 3. Log Unknowns - Track knowledge gaps
empirica.log_unknown("Need to investigate Y")

# 4. CHECK Gate - Assess if safe to proceed
gate_result = empirica.check_submit(operation={"type": "code_generation", "scope": "high"})
# Returns: "PROCEED" | "HALT" | "BRANCH" | "REVISE"

# 5. Create Goals - With epistemic scope
empirica.create_goal(
    session_id="abc-123",
    objective="Implement OAuth2",
    scope={"breadth": 0.6, "duration": 0.4},
    success_criteria=["Auth works", "Tests pass"],
    estimated_complexity=0.65
)

# 6. Assess State - Current epistemic health
state = empirica.assess_state(session_id="abc-123", include_history=True)
```

---

## Integration Points

### 1. Session Continuity (Project Bootstrap)

**When:** At the start of each Waft session
**What:** Load compressed project context

```python
# In waft commands that need context
empirica = EmpiricaManager(project_path)
context = empirica.project_bootstrap()

if context:
    console.print(f"[dim]📊 Epistemic State: know={context.get('epistemic_state', {}).get('know', 0):.0%}[/dim]")
    console.print(f"[dim]🎯 Active Goals: {len(context.get('goals', []))}[/dim]")
    console.print(f"[dim]💡 Recent Findings: {len(context.get('findings', []))}[/dim]")
    console.print(f"[dim]❓ Open Unknowns: {len(context.get('unknowns', []))}[/dim]")
```

### 2. Safety Gates (CHECK)

**When:** Before risky operations (code generation, file deletion, etc.)
**What:** Assess if safe to proceed

```python
# Before generating code
gate = empirica.check_submit(operation={
    "type": "code_generation",
    "scope": "high",
    "description": "Generating authentication module"
})

if gate == "HALT":
    console.print("[red]⚠️  Operation requires human approval[/red]")
    raise typer.Exit(1)
elif gate == "BRANCH":
    console.print("[yellow]⚠️  Need to investigate before proceeding[/yellow]")
    # Spawn investigation
elif gate == "REVISE":
    console.print("[yellow]⚠️  Approach needs revision[/yellow]")
    # Revise approach
```

### 3. Finding/Unknown Logging

**When:** During work, as discoveries are made
**What:** Track what we learn and what we don't know

```python
# When discovering something important
empirica.log_finding("Auth uses JWT with 15min expiry", impact=0.8)

# When encountering uncertainty
empirica.log_unknown("Token rotation mechanism unclear")
```

### 4. Goal Management

**When:** Starting new work items
**What:** Create goals with epistemic scope

```python
# When starting a new feature
session_id = empirica.create_session(ai_id="waft", session_type="development")
empirica.create_goal(
    session_id=session_id,
    objective="Refactor authentication module",
    scope={"breadth": 0.7, "duration": 0.5},
    success_criteria=["Tests pass", "No regressions"],
    estimated_complexity=0.6
)
```

---

## Future Enhancements

### CLI Commands to Add

```bash
# Session management
waft session create [--ai-id ID] [--type TYPE]
waft session bootstrap  # Load project context
waft session status     # Show current state

# Epistemic tracking
waft finding log "discovery" [--impact 0.7]
waft unknown log "gap"
waft check [--operation JSON]  # Safety gate

# Goals
waft goal create "objective" [--scope JSON] [--criteria LIST]

# Assessment
waft assess [--session-id ID] [--history]
```

### Integration with _pyrite

- Store session IDs in `_pyrite/active/`
- Link epistemic assessments to work items
- Track learning over time in `_pyrite/standards/`

---

## Benefits

1. **Session Continuity** - Resume work with compressed context (~800 tokens vs 200k)
2. **Safety** - CHECK gates prevent risky operations
3. **Transparency** - Track what we know and don't know
4. **Measurable Learning** - Quantified knowledge growth
5. **Goal Alignment** - Goals with epistemic scope

---

## Status

✅ **Enhanced EmpiricaManager created**
- Added 6 new methods
- Supports project-bootstrap, finding/unknown logging, CHECK gates, goals, state assessment
- Ready for integration into Waft commands

⏳ **Next Steps**
- Add CLI commands to expose these features
- Integrate project-bootstrap into command workflow
- Add CHECK gates before risky operations
- Document usage patterns

