---
name: Run-It Command Creation
overview: "Create a new `/run-it` slash command that orchestrates a comprehensive workflow sequence: consider → think → check-assumptions → deep-analyze → critique → status → hypothesis → prove-it → verify → proceed → reflect → checkpoint → decide → next → goal. This command provides a systematic, self-correcting approach that balances analysis with critique, verification with reflection, and planning with action."
todos:
  - id: create-command-file
    content: Create .cursor/commands/run-it.md with complete workflow documentation
    status: pending
  - id: document-workflow-sequence
    content: Document all 15 phases with execution steps, expected outputs, and integration points
    status: pending
  - id: add-philosophy-section
    content: Add philosophy section explaining self-correcting balance and design principles
    status: pending
  - id: document-deep-analyze-before-critique
    content: "Document the special consideration: deep-analyze before critique to prevent being too harsh"
    status: pending
  - id: add-error-handling
    content: Document error handling strategy for phase failures
    status: pending
  - id: add-time-estimates
    content: Include time estimates for each phase and total workflow
    status: pending
  - id: add-usage-examples
    content: Provide usage examples (standard, with focus, quick mode)
    status: pending
  - id: document-outputs
    content: Document what files/outputs each phase generates
    status: pending
  - id: add-integration-section
    content: Document how this differs from other orchestration commands
    status: pending
  - id: update-command-recommendations
    content: Update COMMAND_RECOMMENDATIONS.md to include /run-it command
    status: pending
---

# Run-It Command - Comprehensive Workflow Orchestration

## Overview

The `/run-it` command orchestrates a complete, systematic workflow that combines analysis, verification, critique, hypothesis formation, reflection, and decision-making. It's designed to be self-correcting - using deep analysis before critique to avoid being too harsh, and verification before proceeding to ensure accuracy.

## Command File Location

Create: `.cursor/commands/run-it.md`

## Workflow Sequence

The command executes these phases in order:

### Phase 1: Consider Options
**Command**: `/consider`
- Analyze current situation
- Identify available paths forward
- Evaluate trade-offs
- Present recommendations

### Phase 2: Initialize Cognitive Tools
**Command**: `/think`
- Initialize Empirica for epistemic tracking
- Activate Sequential Thinking MCP
- Load project context via bootstrap
- Create epistemic session
- Assess current cognitive state

### Phase 3: Check Assumptions
**Command**: `/check-assumptions`
- Extract assumptions from conversation
- Validate each assumption with evidence
- Categorize by risk level
- Document validation results

### Phase 4: Deep Analysis (Before Critique)
**Command**: `/deep-analyze`
- Perform comprehensive code analysis
- Extract algorithms and patterns
- Understand codebase deeply
- Document findings
- **Purpose**: Balance harsh critique with understanding

### Phase 5: Adversarial Critique
**Command**: `/critique`
- Security-first analysis
- Find unexamined assumptions
- Detect overengineering
- Catch oversights
- **Note**: Deep analysis done first prevents being too harsh

### Phase 6: Quick Status Check
**Command**: `/status`
- Fast status snapshot (< 5 seconds)
- Git status, active work, recent activity
- Quick health indicators

### Phase 7: Hypothesis Formation
**Command**: `/hypothesis`
- Form testable hypotheses based on findings
- Document evidence supporting/contradicting
- Create verification plan
- Save to `_pyrite/hypothesis/`

### Phase 8: Prove Scientific Method
**Command**: `/prove-it`
- Demonstrate scientific method tool works
- Run proof demonstrations
- Verify state capture (A & B)
- Verify data collection (C)
- Confirm file persistence

### Phase 9: Verify Everything
**Command**: `/verify`
- Verify all claims and assumptions
- Create traceable evidence
- Document verification traces
- Update hypothesis confidence

### Phase 10: Proceed with Verification
**Command**: `/proceed`
- Verify context and assumptions
- Check for ambiguity
- Perform flight check
- Proceed with verified understanding

### Phase 11: Final Reflection
**Command**: `/reflect`
- Write comprehensive journal entry
- Reflect on entire workflow
- Document learnings and insights
- Capture patterns and questions

### Phase 12: Create Checkpoint
**Command**: `/checkpoint`
- Create situation report
- Document current state
- Update devlog
- Sync work efforts

### Phase 13: Strategic Decision
**Command**: `/decide`
- Use decision matrix methodology
- Evaluate options quantitatively
- Calculate weighted scores
- Provide recommendations

### Phase 14: Identify Next Step
**Command**: `/next`
- Analyze goals and context
- Identify most important next action
- Prioritize based on goals

### Phase 15: Goal Management
**Command**: `/goal`
- Track larger objectives
- Break goals into steps
- Update progress
- Link to work efforts

## Key Design Principles

### 1. Self-Correcting Balance
- **Deep Analysis Before Critique**: Prevents being too harsh by understanding first
- **Verification Before Proceeding**: Ensures accuracy before action
- **Reflection After Work**: Captures learnings for future improvement

### 2. Comprehensive Coverage
- **Analysis**: Consider, think, deep-analyze
- **Verification**: Check-assumptions, verify, proceed
- **Critique**: Critique (balanced with deep-analyze)
- **Scientific Method**: Hypothesis, prove-it
- **Planning**: Status, checkpoint, decide, next, goal
- **Reflection**: Reflect

### 3. Evidence-Based
- All assumptions validated with evidence
- All hypotheses verified with traces
- All decisions supported by data

### 4. Systematic Flow
- Each phase builds on previous
- Outputs feed into next phase
- Complete cycle from consideration to goal

## Command Structure

The command file should include:

1. **Purpose Section**: What the command does and when to use it
2. **Philosophy Section**: Design principles and approach
3. **Workflow Sequence**: Detailed phase descriptions
4. **Execution Steps**: How to run each phase
5. **Integration Points**: How phases connect
6. **Output Format**: What gets generated
7. **Error Handling**: How to handle failures
8. **Time Estimates**: Expected duration
9. **Best Practices**: How to use effectively

## Special Considerations

### Deep-Analyze Before Critique
The command explicitly runs `/deep-analyze` before `/critique` to:
- Build understanding before finding problems
- Balance adversarial review with comprehension
- Prevent being too harsh on things not yet understood
- Create evidence base for critique

### Verification Throughout
Multiple verification points:
- `/check-assumptions` - Early assumption validation
- `/verify` - Comprehensive verification
- `/proceed` - Final verification before action

### Scientific Method Integration
- `/hypothesis` - Form testable hypotheses
- `/prove-it` - Demonstrate scientific method works
- Creates evidence-based approach

## Output Documentation

Each phase should document its outputs:

1. **Consider**: Analysis document in `_pyrite/active/`
2. **Think**: Empirica session ID, epistemic state
3. **Check-Assumptions**: Validation report with traces
4. **Deep-Analyze**: Analysis documents in work effort
5. **Critique**: Critique report in `_work_efforts/`
6. **Status**: Console output (no file)
7. **Hypothesis**: Hypothesis file in `_pyrite/hypothesis/`
8. **Prove-It**: Proof demonstration results
9. **Verify**: Verification traces in `_pyrite/standards/verification/`
10. **Proceed**: Verified context summary
11. **Reflect**: Journal entry in `_pyrite/journal/ai-journal.md`
12. **Checkpoint**: Checkpoint file in `_work_efforts/`
13. **Decide**: Decision matrix and recommendations
14. **Next**: Next step recommendation
15. **Goal**: Goal tracking updates

## Error Handling

If any phase fails:
- Document the failure
- Continue with remaining phases if possible
- Note what was skipped
- Provide summary of completed vs failed
- Suggest remediation steps

## Time Estimates

- Phase 1 (consider): ~2-5 minutes
- Phase 2 (think): ~1-2 minutes
- Phase 3 (check-assumptions): ~5-10 minutes
- Phase 4 (deep-analyze): ~30-120 seconds (if external repos) or skip
- Phase 5 (critique): ~5-10 minutes
- Phase 6 (status): ~2-5 seconds
- Phase 7 (hypothesis): ~3-5 minutes
- Phase 8 (prove-it): ~1-2 minutes
- Phase 9 (verify): ~5-10 minutes
- Phase 10 (proceed): ~1-2 minutes
- Phase 11 (reflect): ~2-3 minutes
- Phase 12 (checkpoint): ~1-2 minutes
- Phase 13 (decide): ~5-10 minutes
- Phase 14 (next): ~1 minute
- Phase 15 (goal): ~1-2 minutes

**Total**: ~35-70 minutes for complete workflow

## Usage Examples

### Standard Execution
```
/run-it
```

Executes all 15 phases in sequence.

### With Focus Area
```
/run-it --focus "authentication system"
```

Focuses analysis and hypothesis on specific area.

### Quick Mode (Skip Some Phases)
```
/run-it --quick
```

Runs essential phases only (consider, think, check-assumptions, verify, proceed, decide).

## Integration with Existing Commands

This command orchestrates:
- `/consider` - Options analysis
- `/think` - Cognitive initialization
- `/check-assumptions` - Assumption validation
- `/deep-analyze` - Code analysis
- `/critique` - Adversarial review
- `/status` - Quick status
- `/hypothesis` - Hypothesis formation
- `/prove-it` - Scientific method proof
- `/verify` - Comprehensive verification
- `/proceed` - Context verification
- `/reflect` - Reflection
- `/checkpoint` - Status checkpoint
- `/decide` - Decision-making
- `/next` - Next step identification
- `/goal` - Goal management

## Differences from Other Orchestration Commands

### vs `/orchestrate`
- `/run-it` includes: deep-analyze, critique, prove-it, status, next, goal
- `/orchestrate` focuses more on: spin-up, visualize, analyze, execute probes
- `/run-it` is more verification and critique focused
- `/run-it` includes scientific method demonstration

### vs `/comprehensive-orchestration`
- `/run-it` is the executable command version
- `/comprehensive-orchestration` is the prompt template
- `/run-it` adds: deep-analyze before critique, prove-it, status, next, goal

### vs `/hypothesis`
- `/run-it` includes hypothesis but also adds critique, prove-it, and goal management
- `/hypothesis` focuses on hypothesis formation workflow
- `/run-it` is more comprehensive end-to-end

## Implementation Details

### Command File Structure
```markdown
# Run-It

**Purpose**: Comprehensive workflow orchestration with self-correcting balance

**Use when**: Starting significant work, need systematic approach, want verification and critique

## Workflow Sequence
[15 phases documented]

## Execution
[How to run each phase]

## Philosophy
[Design principles]

## Output
[What gets generated]

## Integration
[How phases connect]
```

### Execution Logic
The command should:
1. Execute each phase in sequence
2. Use output from previous phase to inform next
3. Document findings at each phase
4. Handle errors gracefully
5. Provide progress updates
6. Generate summary at end

## Success Criteria

Command is successful when:
- All phases execute (or fail gracefully)
- All outputs documented
- Evidence traces created
- Hypothesis formed and verified
- Decision made with recommendations
- Next steps identified
- Goals tracked
- Reflection captured
- Checkpoint created