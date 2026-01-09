# Rampup

**Progressive project orientation sequence - build understanding incrementally through phases.**

Executes the standard ramp-up workflow: proceed to spin-up and analyze the project, proceed through phase1, then prepare to move on to phase2, recap upon completion. Builds understanding progressively from initial orientation through comprehensive analysis.

**Use when:** Starting work on a new repository, need progressive orientation, want incremental understanding through phases.

---

## Purpose

Provides: progressive project orientation, incremental understanding, multi-phase discovery, systematic ramp-up, comprehensive setup.

---

## What It Does

Executes this sequence:
1. `/proceed` - Verify context and assumptions
2. `/spin-up` - Quick project orientation
3. `/analyze` - Initial project analysis
4. `/phase1` - Comprehensive data gathering
5. `/prepare` - Prepare for next phase (phase2)
6. `/recap` - Session summary

**Optional Parameters:**
- `with [command]` - Execute additional command during ramp-up (e.g., `/rampup with /policy86`)
- `on [branch]` - Switch to branch before ramp-up (e.g., `/rampup on feature/new-feature`)

---

## Execution Flow

```
/proceed → /spin-up → /analyze → /phase1 → /prepare phase2 → /recap
```

Each step:
- Verifies context before proceeding
- Gathers information incrementally
- Builds understanding progressively
- Documents findings
- Prepares for next steps

---

## Philosophy

1. **Progressive Discovery**: Build understanding incrementally (phase1 → phase2)
2. **Systematic Sequence**: Ordered steps, not ad-hoc exploration
3. **Context Verification**: Check assumptions before proceeding
4. **Incremental Understanding**: Each phase builds on previous
5. **Completion Tracking**: Ends with recap/summary

---

## Usage Examples

### Basic Ramp-up
```
/rampup
```

### Ramp-up with Additional Command
```
/rampup with /policy86
/rampup with /consider
/rampup with /explore
```

### Ramp-up on Specific Branch
```
/rampup on thenewfeaturebranch
/rampup on feature/auth-system
/rampup on main
```

### Ramp-up with Command and Branch
```
/rampup with /policy86 on feature/new-feature
```

### Natural Language (AI Recognizes)
```
proceed to spin-up and analyze the project. proceed through phase1 and then prepare to move on to phase2. recap upon completion
```

---

## Integration

This command encapsulates the standard phrase:
"proceed to spin-up and analyze the project. proceed through phase1 and then prepare to move on to phase2. recap upon completion"

**Usage Patterns:**
- `/rampup` - Basic ramp-up sequence
- `/rampup with [command]` - Ramp-up with additional command (e.g., `/rampup with /policy86`)
- `/rampup on [branch]` - Ramp-up on specific branch (e.g., `/rampup on feature/new-feature`)
- `/rampup with [command] on [branch]` - Combined parameters

**Natural Language:**
- Type the natural language phrase - AI will recognize and execute it
- Can include parameters: "rampup with policy86 on thenewfeaturebranch"

---

## When to Use

**Use `/rampup` when**:
- ✅ Starting work on new repository
- ✅ Need progressive orientation through phases
- ✅ Want incremental understanding
- ✅ Need systematic ramp-up sequence
- ✅ Want multi-phase discovery process
- ✅ Starting work on a new branch (use `on [branch]`)
- ✅ Need to apply policy/process during orientation (use `with [command]`)

**Don't use `/rampup` when**:
- ❌ Already familiar with project (use individual commands)
- ❌ Need custom sequence (use individual commands)
- ❌ Need single command (use command directly)
- ❌ Quick check only (use `/spin-up` or `/status`)

---

## Related Commands

- `/onboard` - Alternative name for same sequence (deprecated in favor of `/rampup`)
- `/spin-up` - Quick orientation (first step of rampup)
- `/analyze` - Project analysis (part of rampup)
- `/phase1` - Comprehensive data gathering (part of rampup)
- `/prepare` - Prepare for next phase (part of rampup)
- `/recap` - Session summary (final step of rampup)

---

**This command provides progressive project orientation through incremental phases - use it when starting work on a new repo to build understanding systematically.**
