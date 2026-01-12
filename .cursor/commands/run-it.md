# Run-It

**Comprehensive workflow orchestration with self-correcting balance: consider → think → check-assumptions → deep-analyze → critique → status → hypothesis → prove-it → verify → proceed → reflect → checkpoint → decide → next → goal.**

Orchestrates a complete, systematic workflow that combines analysis, verification, critique, hypothesis formation, reflection, and decision-making. Designed to be self-correcting - using deep analysis before critique to avoid being too harsh, and verification before proceeding to ensure accuracy.

**Use when:** Starting significant work, need systematic approach, want comprehensive verification and critique, or need evidence-based decision-making with full workflow coverage.

---

## Purpose

This command provides:
- **Systematic Analysis**: Consider options, initialize cognitive tools, check assumptions
- **Balanced Critique**: Deep analysis before adversarial critique to prevent being too harsh
- **Scientific Method**: Hypothesis formation and proof demonstration
- **Comprehensive Verification**: Multiple verification points throughout workflow
- **Evidence-Based Decisions**: Quantitative decision-making with traceable evidence
- **Complete Documentation**: Reflection, checkpoint, and goal tracking
- **Self-Correcting**: Each phase balances and corrects the previous

---

## Philosophy

### 1. Self-Correcting Balance

The workflow is designed to prevent common pitfalls:

- **Deep Analysis Before Critique**: Running `/deep-analyze` before `/critique` ensures understanding before finding problems. This prevents being too harsh on things not yet understood and creates an evidence base for critique.

- **Verification Before Proceeding**: Multiple verification points (`/check-assumptions`, `/verify`, `/proceed`) ensure accuracy before taking action. This prevents proceeding on unverified assumptions.

- **Reflection After Work**: Final reflection captures learnings for future improvement, creating a feedback loop.

### 2. Comprehensive Coverage

The workflow covers all aspects of systematic work:

- **Analysis**: Consider options, think deeply, analyze codebase
- **Verification**: Check assumptions, verify claims, proceed with confidence
- **Critique**: Adversarial review balanced with understanding
- **Scientific Method**: Hypothesis formation and proof
- **Planning**: Status checks, checkpoints, decisions, next steps, goals
- **Reflection**: Meta-cognitive review and learning capture

### 3. Evidence-Based Approach

Every phase produces evidence:

- Assumptions validated with traces
- Hypotheses verified with evidence
- Decisions supported by data
- All findings documented and traceable

### 4. Systematic Flow

Each phase builds on the previous:

- Outputs from one phase inform the next
- Evidence accumulates throughout
- Understanding deepens progressively
- Complete cycle from consideration to goal

---

## Workflow Sequence

The command executes 15 phases in order:

### Phase 1: Consider Options

**Command**: `/consider`

**Purpose**: Analyze current situation and identify available paths forward

**Execution**:
1. Assess current state
2. Identify options and alternatives
3. Evaluate trade-offs (pros/cons, effort, risk)
4. Form recommendations with reasoning
5. Present findings

**Expected Output**:
- Situation analysis document
- Options identified with trade-offs
- Recommendations with reasoning
- Next steps

**Documentation**: Analysis document saved to `_pyrite/active/YYYY-MM-DD_consideration_*.md`

**Time Estimate**: ~2-5 minutes

---

### Phase 2: Initialize Cognitive Tools

**Command**: `/think`

**Purpose**: Activate all thinking and cognitive enhancement tools

**Execution**:
1. Verify environment (date, Python version, git, MCP servers)
2. Initialize Empirica (project init, session create)
3. Project bootstrap (load compressed context ~800 tokens)
4. Initialize Sequential Thinking MCP
5. Activate Work Efforts system
6. Assess current cognitive state

**Expected Output**:
- Empirica session ID
- Epistemic state summary
- Project context loaded
- Cognitive tools ready status

**Documentation**: Session ID and epistemic state recorded

**Time Estimate**: ~1-2 minutes

---

### Phase 3: Check Assumptions

**Command**: `/check-assumptions`

**Purpose**: Identify and validate all assumptions with evidence

**Execution**:
1. Extract assumptions from conversation history
2. Categorize by type (code, dependency, data, system, behavioral)
3. Prioritize by risk level (critical, high, medium, low)
4. Gather validation evidence from multiple sources:
   - Code analysis
   - File system checks
   - Test results
   - Git history
   - Empirica/Oracle
   - Documentation
   - Runtime checks
5. Validate each assumption (proven/disproven/partial/insufficient)
6. Generate validation report with evidence traces

**Expected Output**:
- Assumption validation report
- Evidence traces for each assumption
- Risk assessment
- Recommendations based on validation

**Documentation**: 
- Validation report with traces
- Evidence saved to `_pyrite/standards/verification/traces/`

**Time Estimate**: ~5-10 minutes

---

### Phase 4: Deep Analysis (Before Critique)

**Command**: `/deep-analyze`

**Purpose**: Perform comprehensive code analysis to build understanding before critique

**Special Note**: This phase runs BEFORE critique to:
- Build understanding before finding problems
- Balance adversarial review with comprehension
- Prevent being too harsh on things not yet understood
- Create evidence base for critique

**Execution**:
1. Repository discovery (if external repos specified)
2. Code search and discovery (semantic and exact)
3. Source file reading
4. Algorithm extraction
5. Pattern recognition
6. Data structure analysis
7. Integration opportunity identification
8. Documentation generation

**Expected Output**:
- Comprehensive analysis documents
- Algorithm reference
- Pattern catalog
- Data structure documentation
- Integration guide

**Documentation**: Analysis documents saved to work effort directory or `_pyrite/active/`

**Time Estimate**: ~30-120 seconds (if external repos) or skip if analyzing current codebase

**Note**: If analyzing current codebase, this phase may be skipped or simplified since we already have understanding from previous phases.

---

### Phase 5: Adversarial Critique

**Command**: `/critique`

**Purpose**: Security-first adversarial review assuming worst-case scenarios

**Special Note**: Deep analysis done first prevents being too harsh. The critique is informed by understanding from Phase 4.

**Execution**:
1. Locate plan or current work to critique
2. Security-first analysis (CRITICAL priority):
   - File system security
   - Code execution security
   - Data security
   - Network security
   - Dependency security
   - Access control
   - Input validation
3. Unexamined assumptions analysis
4. Overengineering detection
5. Oversight detection
6. Missed obviousness detection
7. Generate critique report

**Expected Output**:
- Critique report with security vulnerabilities (CRITICAL first)
- Assumption issues
- Overengineering findings
- Oversights identified
- Prioritized recommendations

**Documentation**: Critique report saved to `_work_efforts/CRITIQUE_YYYY-MM-DD_HHMMSS.md`

**Time Estimate**: ~5-10 minutes

---

### Phase 6: Quick Status Check

**Command**: `/status`

**Purpose**: Fast status snapshot for immediate awareness

**Execution**:
1. Quick git check (status --short, branch, uncommitted count)
2. Active work check (work efforts, current directory)
3. Recent activity (last commits, modified files, devlog entries)
4. Quick health check (structure validity, obvious issues)

**Expected Output**:
- Console status display (< 5 seconds)
- Git status summary
- Active work summary
- Recent activity summary
- Health status

**Documentation**: Console output only (no file created)

**Time Estimate**: ~2-5 seconds

---

### Phase 7: Hypothesis Formation

**Command**: `/hypothesis`

**Purpose**: Form testable hypotheses based on findings from previous phases

**Execution**:
1. Review findings from previous phases (consider, check-assumptions, deep-analyze, critique)
2. Formulate testable hypothesis statements
3. Identify supporting evidence
4. Note contradicting evidence
5. Define verification plan
6. Make predictions (if true vs if false)
7. Assess confidence level
8. Save hypothesis document

**Expected Output**:
- Structured hypothesis document
- Evidence supporting/contradicting
- Verification plan
- Predictions
- Confidence assessment

**Documentation**: Hypothesis saved to `_pyrite/hypothesis/YYYY-MM-DD_[hypothesis-name].md`

**Time Estimate**: ~3-5 minutes

---

### Phase 8: Prove Scientific Method

**Command**: `/prove-it`

**Purpose**: Demonstrate that the scientific method tool is fully functional

**Execution**:
1. Run simple proof demonstration
2. Run real D&D experiment proof (if applicable)
3. Show all captured states (A & B)
4. Show collected data (C)
5. Display analysis results
6. Verify file persistence

**Expected Output**:
- Proof demonstration results
- State capture verification (A & B)
- Data collection verification (C)
- File persistence confirmation

**Documentation**: Proof results displayed (experiment files saved to `scientific_method_tool/experiments/`)

**Time Estimate**: ~1-2 minutes

---

### Phase 9: Verify Everything

**Command**: `/verify`

**Purpose**: Comprehensive verification of all claims and assumptions

**Execution**:
1. Identify verifiable claims from conversation
2. Select relevant verification checks:
   - Environment verification
   - Project state verification
   - Tool availability verification
   - File/directory verification
   - Configuration verification
   - Dependency verification
   - Work effort verification
   - GitHub state verification
3. Run verification methods
4. Document traces with evidence
5. Update hypothesis confidence based on verification

**Expected Output**:
- Verification summary table
- Detailed verification results
- Evidence traces for each check
- Updated hypothesis confidence

**Documentation**: Verification traces saved to `_pyrite/standards/verification/traces/YYYY-MM-DD_verify-XXXX_*.md`

**Time Estimate**: ~5-10 minutes

---

### Phase 10: Proceed with Verification

**Command**: `/proceed`

**Purpose**: Final verification of context and assumptions before proceeding

**Execution**:
1. Context gathering (current work state, related files, project structure)
2. Assumption identification (find unverified assumptions)
3. Ambiguity detection (find unclear points)
4. Flight check (verify everything ready)
5. Clarifying questions (if critical)
6. Verified proceeding (continue with verified understanding)

**Expected Output**:
- Context summary
- Assumptions identified
- Ambiguities detected
- Flight check status
- Verified understanding

**Documentation**: Verified context documented

**Time Estimate**: ~1-2 minutes

---

### Phase 11: Final Reflection

**Command**: `/reflect`

**Purpose**: Comprehensive reflection on entire workflow

**Execution**:
1. Check for journal (create if missing)
2. Gather context (current work, recent activity, thoughts, learnings)
3. Write reflective journal entry covering:
   - What I'm doing
   - What I'm thinking
   - What I'm learning
   - Patterns I notice
   - Questions I have
   - How I feel about this
   - What I'd do differently
   - Meta-reflection
4. Save journal entry

**Expected Output**:
- Comprehensive journal entry
- Deep reflection on workflow
- Insights and learnings captured
- Patterns recognized

**Documentation**: Journal entry saved to `_pyrite/journal/ai-journal.md`

**Time Estimate**: ~2-3 minutes

---

### Phase 12: Create Checkpoint

**Command**: `/checkpoint`

**Purpose**: Create situation report and recovery point

**Execution**:
1. Get current state (date, directory, git status, project status)
2. Recap conversation (summary, decisions, questions, tasks)
3. Create checkpoint file
4. Update devlog
5. Update work efforts (if applicable)

**Expected Output**:
- Checkpoint file with complete state snapshot
- Devlog entry
- Work effort updates

**Documentation**: Checkpoint saved to `_work_efforts/CHECKPOINT_YYYY-MM-DD_[TOPIC].md`

**Time Estimate**: ~1-2 minutes

---

### Phase 13: Strategic Decision

**Command**: `/decide`

**Purpose**: Quantitative decision-making using decision matrix

**Execution**:
1. Problem definition (understand decision, context, constraints)
2. Criteria development (define evaluation criteria, categorize)
3. Weighting (assign weights to criteria, ensure sum to 1.0)
4. Scoring (score each alternative on each criterion)
5. Calculation (perform WSM/AHP/WPM/BWM calculations)
6. Analysis (rank alternatives, sensitivity analysis)
7. Presentation (show matrix, calculations, recommendations)

**Expected Output**:
- Decision matrix table
- Calculation details
- Sensitivity analysis
- Recommendations with reasoning

**Documentation**: Decision analysis saved (recommendations documented)

**Time Estimate**: ~5-10 minutes

---

### Phase 14: Identify Next Step

**Command**: `/next`

**Purpose**: Identify most important next action based on goals and context

**Execution**:
1. Analyze active goals (goals with pending steps)
2. Analyze work in progress (current tasks, files)
3. Analyze context (recent activity, blockers, dependencies)
4. Analyze priorities (goal importance, step dependencies, urgency)
5. Identify next step with reasoning

**Expected Output**:
- Next step recommendation
- Priority level
- Reasoning
- Estimated time
- Dependencies

**Documentation**: Next step displayed (may update goal tracking)

**Time Estimate**: ~1 minute

---

### Phase 15: Goal Management

**Command**: `/goal`

**Purpose**: Track larger objectives and break into actionable steps

**Execution**:
1. Review current goals
2. Update goal progress (if applicable)
3. Create new goal (if needed)
4. Break goals into steps
5. Link to work efforts
6. Update goal tracking

**Expected Output**:
- Goal status summary
- Progress updates
- Step breakdown
- Next actions

**Documentation**: Goal tracking updated (goals saved to goal system)

**Time Estimate**: ~1-2 minutes

---

## Complete Execution Sequence

```
1. /consider                    → Analyze options
2. /think                       → Initialize cognitive tools
3. /check-assumptions           → Validate assumptions
4. /deep-analyze                → Deep code analysis (before critique)
5. /critique                    → Adversarial review
6. /status                      → Quick status check
7. /hypothesis                  → Form hypotheses
8. /prove-it                    → Prove scientific method
9. /verify                      → Verify everything
10. /proceed                    → Final verification
11. /reflect                    → Final reflection
12. /checkpoint                 → Create checkpoint
13. /decide                     → Strategic decision
14. /next                       → Identify next step
15. /goal                       → Goal management
```

---

## Special Considerations

### Deep-Analyze Before Critique

The command explicitly runs `/deep-analyze` before `/critique` to:

- **Build Understanding First**: Deep analysis creates comprehension before finding problems
- **Balance Adversarial Review**: Understanding prevents critique from being too harsh
- **Evidence-Based Critique**: Analysis provides evidence base for critique
- **Prevent Premature Judgment**: Understanding context prevents unfair criticism

**Implementation**: If analyzing current codebase (not external repos), Phase 4 may be simplified or skipped since understanding already exists from previous phases. The key is ensuring understanding exists before critique.

### Verification Throughout

Multiple verification points ensure accuracy:

- **Early Verification** (`/check-assumptions`): Validates assumptions before proceeding
- **Comprehensive Verification** (`/verify`): Verifies all claims with traceable evidence
- **Final Verification** (`/proceed`): Last check before taking action

This triple-verification approach ensures nothing proceeds on unverified assumptions.

### Scientific Method Integration

The workflow includes scientific method demonstration:

- **Hypothesis Formation** (`/hypothesis`): Creates testable hypotheses
- **Proof Demonstration** (`/prove-it`): Shows scientific method works
- **Evidence-Based**: All conclusions supported by evidence

This creates a rigorous, evidence-based approach to work.

---

## Output Documentation

Each phase generates specific outputs:

1. **Consider**: Analysis document in `_pyrite/active/YYYY-MM-DD_consideration_*.md`
2. **Think**: Empirica session ID, epistemic state (no file, console output)
3. **Check-Assumptions**: Validation report with traces in `_pyrite/standards/verification/traces/`
4. **Deep-Analyze**: Analysis documents in work effort directory or `_pyrite/active/`
5. **Critique**: Critique report in `_work_efforts/CRITIQUE_YYYY-MM-DD_HHMMSS.md`
6. **Status**: Console output only (no file)
7. **Hypothesis**: Hypothesis file in `_pyrite/hypothesis/YYYY-MM-DD_[hypothesis-name].md`
8. **Prove-It**: Proof results (experiment files in `scientific_method_tool/experiments/`)
9. **Verify**: Verification traces in `_pyrite/standards/verification/traces/YYYY-MM-DD_verify-XXXX_*.md`
10. **Proceed**: Verified context summary (console output)
11. **Reflect**: Journal entry in `_pyrite/journal/ai-journal.md`
12. **Checkpoint**: Checkpoint file in `_work_efforts/CHECKPOINT_YYYY-MM-DD_[TOPIC].md`
13. **Decide**: Decision matrix and recommendations (console output + optional file)
14. **Next**: Next step recommendation (console output)
15. **Goal**: Goal tracking updates (goal system)

---

## Error Handling

If any phase fails:

1. **Document the Failure**:
   - Note which phase failed
   - Document error message
   - Capture context at time of failure

2. **Continue if Possible**:
   - Skip failed phase if not critical
   - Continue with remaining phases
   - Note what was skipped

3. **Provide Summary**:
   - List completed phases
   - List failed phases
   - Note partial completions

4. **Suggest Remediation**:
   - Provide steps to fix failure
   - Suggest alternative approaches
   - Recommend when to retry

**Graceful Degradation**: The command should continue with available phases even if some fail. Critical phases (like `/think` for Empirica) may cause subsequent phases to skip, but non-critical failures shouldn't stop the entire workflow.

---

## Time Estimates

**Per Phase**:
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

**Note**: Time varies based on:
- Complexity of codebase
- Number of assumptions to validate
- Depth of analysis needed
- Number of alternatives in decision
- Amount of existing documentation

---

## Usage Examples

### Standard Execution
```
/run-it
```

Executes all 15 phases in sequence. Use when:
- Starting significant new work
- Need comprehensive systematic approach
- Want full verification and critique
- Need evidence-based decision-making

### With Focus Area
```
/run-it --focus "authentication system"
```

Focuses analysis and hypothesis on specific area. Use when:
- Working on specific feature/system
- Need targeted analysis
- Want focused critique

### Quick Mode (Skip Some Phases)
```
/run-it --quick
```

Runs essential phases only:
- `/consider` - Options analysis
- `/think` - Cognitive initialization
- `/check-assumptions` - Assumption validation
- `/verify` - Comprehensive verification
- `/proceed` - Final verification
- `/decide` - Decision-making

Use when:
- Time-constrained
- Need faster workflow
- Some phases not applicable

### Custom Phase Selection
```
/run-it --phases "consider,think,check-assumptions,verify,decide"
```

Runs only specified phases. Use when:
- Want custom workflow
- Need specific phases only
- Skipping non-applicable phases

---

## Integration with Other Commands

This command orchestrates:
- `/consider` - Options analysis and recommendations
- `/think` - Cognitive tool initialization
- `/check-assumptions` - Assumption validation with evidence
- `/deep-analyze` - Comprehensive code analysis
- `/critique` - Adversarial security-first review
- `/status` - Quick status snapshot
- `/hypothesis` - Hypothesis formation workflow
- `/prove-it` - Scientific method demonstration
- `/verify` - Comprehensive verification with traces
- `/proceed` - Context verification before action
- `/reflect` - Reflective journal writing
- `/checkpoint` - Situation report creation
- `/decide` - Quantitative decision-making
- `/next` - Next step identification
- `/goal` - Goal tracking and management

---

## Differences from Other Orchestration Commands

### vs `/orchestrate`

**`/run-it` includes**:
- Deep-analyze before critique (balanced critique)
- Prove-it (scientific method demonstration)
- Status (quick status check)
- Next (next step identification)
- Goal (goal management)

**`/orchestrate` focuses on**:
- Spin-up (orientation)
- Visualize (interactive dashboard)
- Analyze (goal analysis)
- Execute probes (data gathering)

**Key Difference**: `/run-it` is more verification and critique focused, while `/orchestrate` is more exploration and visualization focused.

### vs `/comprehensive-orchestration`

**`/run-it`**:
- Executable command version
- 15 phases in specific sequence
- Includes deep-analyze before critique
- Includes prove-it, status, next, goal

**`/comprehensive-orchestration`**:
- Prompt template
- Reference document
- Can be customized

**Key Difference**: `/run-it` is the concrete implementation, `/comprehensive-orchestration` is the template.

### vs `/hypothesis`

**`/run-it` includes**:
- Hypothesis formation
- Plus critique, prove-it, goal management
- More comprehensive end-to-end

**`/hypothesis` focuses on**:
- Hypothesis formation workflow
- Orientation through decision-making
- Hypothesis-specific phases

**Key Difference**: `/run-it` is broader workflow, `/hypothesis` is hypothesis-focused.

---

## Best Practices

1. **Use for Significant Work**: This is a comprehensive workflow - use for major initiatives, not quick tasks

2. **Allow Time**: Full workflow takes 35-70 minutes - plan accordingly

3. **Review Outputs**: Each phase generates documentation - review as you go

4. **Customize as Needed**: Use `--quick` or `--phases` to customize workflow

5. **Trust the Process**: The self-correcting balance (deep-analyze before critique) is intentional - trust it

6. **Document Everything**: All phases create documentation - use it for future reference

7. **Verify Before Acting**: Multiple verification points ensure accuracy - don't skip them

8. **Reflect Deeply**: Final reflection captures learnings - take time for it

9. **Make Decisions Systematically**: Use decision matrix for important choices

10. **Track Goals**: Link work to larger objectives via goal management

---

## When to Use

**Use `/run-it` when**:
- ✅ Starting significant new work or feature
- ✅ Need comprehensive systematic approach
- ✅ Want verification and critique before proceeding
- ✅ Need evidence-based decision-making
- ✅ Want full workflow coverage
- ✅ Starting major investigation or analysis
- ✅ Need balanced critique (understanding before criticism)
- ✅ Want scientific method rigor

**Don't use `/run-it` when**:
- ❌ Quick task or simple change
- ❌ Already have full understanding
- ❌ Time-constrained (use `/run-it --quick`)
- ❌ Just need one specific command
- ❌ Routine maintenance work

---

## Output Summary

After completion, provides:

1. **Analysis Complete**: Options considered, assumptions validated, codebase understood
2. **Critique Balanced**: Adversarial review informed by deep understanding
3. **Hypothesis Formed**: Testable hypotheses with evidence
4. **Scientific Method Proven**: Tool functionality demonstrated
5. **Everything Verified**: All claims verified with traceable evidence
6. **Context Verified**: Final verification before proceeding
7. **Reflection Captured**: Comprehensive journal entry with learnings
8. **Checkpoint Created**: Complete state snapshot for recovery
9. **Decision Made**: Quantitative decision with recommendations
10. **Next Step Identified**: Prioritized next action
11. **Goals Tracked**: Larger objectives linked to work

---

## Command Dependencies

The command requires:
- All individual commands (`/consider`, `/think`, etc.) to be available
- Empirica CLI (for `/think` phase)
- MCP servers (sequential-thinking, work-efforts) for some phases
- Git repository (for some verification checks)
- Scientific method tool (for `/prove-it` phase)

If dependencies are missing:
- Document which phases are skipped
- Continue with available phases
- Provide guidance on installing missing dependencies

---

## Example Workflow

```
User: "/run-it"

AI: [Executes Phase 1: /consider]
AI: [Executes Phase 2: /think]
AI: [Executes Phase 3: /check-assumptions]
AI: [Executes Phase 4: /deep-analyze]
AI: [Executes Phase 5: /critique]
AI: [Executes Phase 6: /status]
AI: [Executes Phase 7: /hypothesis]
AI: [Executes Phase 8: /prove-it]
AI: [Executes Phase 9: /verify]
AI: [Executes Phase 10: /proceed]
AI: [Executes Phase 11: /reflect]
AI: [Executes Phase 12: /checkpoint]
AI: [Executes Phase 13: /decide]
AI: [Executes Phase 14: /next]
AI: [Executes Phase 15: /goal]

AI: ✅ Run-It Complete
    - Phases completed: 15/15
    - Assumptions validated: 8
    - Hypotheses formed: 2
    - Decisions made: 1
    - Next step identified
    - Goals tracked
    
    📁 All outputs documented
    🎯 Next: [Based on /next recommendation]
```

---

**This command provides a complete, self-correcting workflow from consideration through goal management - perfect for starting significant work with systematic verification, balanced critique, and evidence-based decision-making.**

--- End Command ---
