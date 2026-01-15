---
name: Complete Cycle Master Command
overview: Create a new `/complete-cycle` command that orchestrates all major workflows (onboard, explore, check-assumptions, hypothesis, critique, journal, analyze, engineering, evolve, improve, version-bake, run-it, etc.) into a single comprehensive workflow, then execute it step by step.
todos:
  - id: create-command-file
    content: Create `.cursor/commands/complete-cycle.md` with full command structure, workflow sequence, and execution steps
    status: pending
  - id: document-phases
    content: Document all 17 phases organized into 6 logical groups (Orientation, Analysis, Engineering, Quality, Evolution, Planning)
    status: pending
  - id: add-configuration
    content: Add configuration options (--quick, --focus, --skip, --phases) for flexible execution
    status: pending
  - id: update-documentation
    content: Update COMMAND_RECOMMENDATIONS.md and help.md to include new command
    status: pending
  - id: test-structure
    content: Review command file structure and verify logical flow of phases
    status: pending
  - id: execute-step-by-step
    content: Execute /complete-cycle step by step, documenting progress as each phase completes
    status: pending

category: hopes
confidence: 1.00
constellation_date: 2026-01-14
---

# Complete Cycle Master Command Implementation Plan

## Overview

Create a new `/complete-cycle` command that orchestrates all major workflows into a single comprehensive master workflow. This command will execute the complete development cycle from onboarding through quality assurance and evolution.

## Command Name

**`/complete-cycle`** - Complete development cycle from orientation to evolution

**Aliases**: `/master-workflow`, `/full-cycle`, `/deep-dive`

## Workflow Sequence

The command will execute phases in this logical order:

### Phase 1: Orientation & Setup

1. **`/onboard`** - Standard repository onboarding (proceed → spin-up → analyze → phase1 → prepare → recap)
2. **`/explore`** - Deep codebase exploration (structure, architecture, patterns, dependencies)

### Phase 2: Analysis & Planning

3. **`/check-assumptions`** - Validate all assumptions with evidence
4. **`/hypothesis`** - Form testable hypotheses based on findings
5. **`/critique`** - Adversarial security-first review
6. **`/comprehensive-orchestration`** - Full orchestration workflow (spin-up → consider → engineering → visualize → analyze → goal → checkpoint → execute → hypothesis → verify → reflect → recap → proceed → decide)
7. **`/analyze`** - Data analysis, insights, and action planning

### Phase 3: Engineering & Implementation

8. **`/engineering`** - Complete engineering workflow (spin-up → explore → draft plan → critique plan → finalize plan → begin)

### Phase 4: Quality Assurance

9. **`/improve`** - Identify and prioritize improvements
10. **`/version-bake`** - Complete quality workflow (reflect → run-it → improve → check-assumptions → verify → hypothesis → prove-it)
11. **`/run-it`** - Comprehensive workflow orchestration (15 phases)
12. **`/prove-it`** - Prove scientific method tool works

### Phase 5: Evolution & Reflection

13. **`/evolve`** - Spawn Being from Source and run complete version-bake workflow
14. **`/journal`** - AI journal system hub (view, search, reflect)

### Phase 6: Planning & Tracking

15. **`/next`** - Identify next step based on goals
16. **`/goal`** - Track larger goals and break into steps
17. **`/checkpoint`** - Create situation report and status update

## Implementation Steps

### Step 1: Create Command File

- **File**: `.cursor/commands/complete-cycle.md`
- **Structure**: Follow existing command template
- **Sections**: Purpose, Philosophy, Workflow Sequence, Execution Steps, Output Format, Integration, When to Use

### Step 2: Define Execution Logic

- **Sequential Execution**: Execute phases in order
- **Error Handling**: Continue with remaining phases if one fails
- **Progress Tracking**: Show progress for each phase
- **Documentation**: Save outputs from each phase

### Step 3: Organize Phase Groups

- **Group 1**: Orientation (onboard, explore)
- **Group 2**: Analysis (check-assumptions, hypothesis, critique, comprehensive-orchestration, analyze)
- **Group 3**: Engineering (engineering)
- **Group 4**: Quality (improve, version-bake, run-it, prove-it)
- **Group 5**: Evolution (evolve, journal)
- **Group 6**: Planning (next, goal, checkpoint)

### Step 4: Add Configuration Options

- **`--quick`**: Skip non-essential phases
- **`--focus <area>`**: Focus on specific area (orientation, analysis, engineering, quality, evolution, planning)
- **`--skip <phases>`**: Skip specific phases
- **`--phases <list>`**: Run only specified phases

### Step 5: Document Integration

- Document how this command relates to individual commands
- Note when to use vs. individual commands
- Add to help system
- Update command recommendations

### Step 6: Test Command

- Review command file structure
- Verify phase sequence makes sense
- Check for logical flow
- Ensure error handling is appropriate

## Command Structure

```markdown
# Complete Cycle

**Complete development cycle from orientation to evolution.**

Orchestrates all major workflows into a single comprehensive master workflow: onboard → explore → check-assumptions → hypothesis → critique → comprehensive-orchestration → analyze → engineering → improve → version-bake → run-it → prove-it → evolve → journal → next → goal → checkpoint.

**Use when:** Starting major new work, need complete systematic approach, want full cycle from onboarding through quality assurance and evolution.

---

## Purpose

This command provides:
- **Complete Orientation**: Full onboarding and exploration
- **Comprehensive Analysis**: Assumption validation, hypothesis formation, critique, orchestration
- **Full Engineering**: Complete engineering workflow
- **Quality Assurance**: Improvements, version-bake, run-it, proof
- **Evolution**: Being evolution from Source
- **Reflection**: Journal and learning capture
- **Planning**: Next steps, goals, checkpoints

---

## Workflow Sequence

[17 phases organized into 6 groups]

---

## Execution Steps

[Detailed execution for each phase]

---

## Output Documentation

[All outputs from each phase documented]

---

## Integration

[How this relates to individual commands]

---

## When to Use

**Use `/complete-cycle` when:**
- ✅ Starting major new initiative
- ✅ Need complete systematic approach
- ✅ Want full cycle from start to finish
- ✅ Need comprehensive quality assurance
- ✅ Want Being evolution tracking

**Don't use `/complete-cycle` when:**
- ❌ Quick task or simple change
- ❌ Already have full understanding
- ❌ Time-constrained (use individual commands)
- ❌ Just need one specific workflow
```

## Files to Create/Modify

1. **Create**: `.cursor/commands/complete-cycle.md` - New command file
2. **Update**: `.cursor/commands/COMMAND_RECOMMENDATIONS.md` - Add new command
3. **Update**: `.cursor/commands/help.md` - Add to help system (if applicable)

## Execution Plan

After creating the command:

1. Review the command structure
2. Execute `/complete-cycle` step by step
3. Document progress as each phase completes
4. Handle any errors gracefully
5. Provide summary at completion

## Time Estimates

**Per Phase Group**:

- Orientation: ~10-15 minutes
- Analysis: ~60-90 minutes
- Engineering: ~45-80 minutes
- Quality: ~60-110 minutes
- Evolution: ~60-115 minutes
- Planning: ~5-10 minutes

**Total**: ~240-420 minutes (4-7 hours) for complete cycle

**Note**: Can use `--quick` or `--focus` to reduce time

## Success Criteria

- ✅ Command file created with proper structure
- ✅ All 17 phases documented and sequenced
- ✅ Error handling defined
- ✅ Integration documented
- ✅ Command ready for execution
- ✅ Can execute step by step as requested