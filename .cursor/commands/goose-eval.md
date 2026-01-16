# Goose Eval

**Systematic evaluation and decision-making workflow for evaluating goose as an AI agent tool.**

Executes a complete 12-phase evaluation workflow: orientation → analysis → data gathering → hypothesis formation → verification → reflection → decision. Designed for reliable, repeatable evaluation of tools, technologies, or approaches.

**Use when:** You need to systematically evaluate a tool/technology, want structured decision-making, or need comprehensive evaluation with hypothesis testing and verification.

---

## Purpose

This command provides:
- **Systematic Evaluation**: Complete 12-phase workflow
- **Hypothesis-Driven**: Form and verify testable hypotheses
- **Evidence-Based**: Gather and assess evidence at each phase
- **Decision Support**: Structured decision matrix with recommendations
- **Documentation**: Complete paper trail of evaluation process
- **Reliable Execution**: Repeatable workflow with clear outputs

---

## Philosophy

1. **Systematic Over Ad-Hoc**: Follow structured phases, don't skip steps
2. **Evidence First**: Gather data before forming opinions
3. **Hypothesis-Driven**: Form testable hypotheses, then verify
4. **Document Everything**: Create paper trail at each phase
5. **Decision Support**: End with clear recommendation and reasoning

---

## Execution Phases

### Phase 1: Orientation (`/spin-up`)
**Purpose**: Get oriented to current state

**Actions**:
1. Check current date/time
2. Review git status
3. Check active work efforts (especially related work like OpenHands)
4. Review recent devlog entries
5. Check MCP server health
6. Identify current AI agent integration state

**Output**: Current state snapshot, active work context

**Files Created**: None (gathers context only)

---

### Phase 2: Repository Analysis (`/consider`)
**Purpose**: Analyze repository state and present options

**Focus Areas**:
- Current AI agent tool landscape in WAFT
- OpenHands integration status (if applicable)
- Available paths for evaluation
- Trade-offs between different approaches

**Output**: Analysis of options, recommendations for evaluation approach

**Files Created**: None (analysis only)

---

### Phase 3: Visual Assessment (`/visualize`)
**Purpose**: Create interactive dashboard of current state

**Visualizations**:
- Project structure
- Active work efforts
- Git status
- AI agent integration points
- System architecture

**Output**: Standalone HTML dashboard in browser

**Files Created**: `_work_efforts/visualizations/goose_eval_YYYY-MM-DD.html` (optional)

---

### Phase 4: Goal Analysis (`/analyze`)
**Purpose**: Analyze the goal of evaluating goose

**Analysis Areas**:
- Health of current AI agent integrations
- Gaps in current architecture
- Opportunities goose might address
- Risks of adding another tool

**Output**: Insights, opportunities, action planning

**Files Created**: None (analysis only)

---

### Phase 5: Checkpoint (`/checkpoint`)
**Purpose**: Create situation report

**Content**:
- Chat recap so far
- Current state snapshot
- Work progress summary
- Next steps identified

**Output**: Checkpoint file

**Files Created**: `_work_efforts/CHECKPOINT_YYYY-MM-DD_goose_evaluation.md`

---

### Phase 6: Data Gathering & Hypothesis Formation (`/execute`)
**Purpose**: Gather data and form testable hypothesis

**Probe Sequence**:

#### 6.1 Structural Probes
- Analyze goose repository structure (via web search/analysis)
- Map goose architecture and capabilities
- Identify goose's tool ecosystem
- Compare goose structure to WAFT's needs

#### 6.2 Functional Probes
- Map goose features and capabilities
- Explore goose's MCP integration (if any)
- Identify goose's execution model
- Assess goose's extensibility

#### 6.3 Comparative Probes
- Compare goose vs OpenHands SDK (if applicable)
- Compare goose vs WAFT's native agent capabilities
- Identify overlap and complementarity
- Assess integration complexity

#### 6.4 Hypothesis Formation
**Create hypothesis file**: `_pyrite/hypothesis/YYYY-MM-DD_goose_integration.md`

**Hypothesis Structure**:
- **Statement**: Clear, testable hypothesis about goose's fit
- **Evidence Supporting**: Why goose might be useful
- **Evidence Contradicting**: Why goose might not fit
- **Verification Plan**: How to test the hypothesis
- **Predictions**: What we expect if hypothesis is true/false
- **Confidence Level**: Initial assessment

**Output**: Structured hypothesis document

**Files Created**: `_pyrite/hypothesis/YYYY-MM-DD_goose_integration.md`

---

### Phase 7: Hypothesis Verification (`/verify`)
**Purpose**: Verify hypothesis claims with evidence

**Verification Steps**:
1. Verify goose capabilities claims
2. Test integration feasibility
3. Verify compatibility with WAFT architecture
4. Test predictions from hypothesis
5. Assess evidence strength

**Output**: Verification traces, updated hypothesis with confidence level

**Files Created**: Updates to hypothesis file with verification results

---

### Phase 8: Reflection (`/reflect`)
**Purpose**: Journal entry on the evaluation process

**Reflection Areas**:
- What we learned about goose
- How it compares to existing tools
- Patterns noticed in AI agent tool landscape
- Questions remaining
- Meta-reflection on evaluation process

**Output**: Journal entry

**Files Created**: Entry in `_pyrite/journal/ai-journal.md`

---

### Phase 9: Conversation Recap (`/recap`)
**Purpose**: Complete session summary

**Content**:
- Full conversation summary
- Key findings about goose
- Comparison insights
- Decision context
- Open questions

**Output**: Recap file

**Files Created**: `_work_efforts/SESSION_RECAP_YYYY-MM-DD_goose_evaluation.md`

---

### Phase 10: Decision Analysis (`/proceed` then `/decide`)
**Purpose**: Make structured decision about goose

#### 10.1 Context Verification (`/proceed`)
- Verify understanding of goose
- Check assumptions about WAFT needs
- Resolve ambiguities
- Flight check before decision

#### 10.2 Decision Matrix (`/decide`)
**Decision Problem**: "Should we integrate goose into WAFT?"

**Alternatives** (to be refined):
1. Integrate goose as primary agent execution engine
2. Integrate goose alongside OpenHands (complementary)
3. Evaluate goose but don't integrate yet
4. Don't use goose (stick with current approach)

**Criteria** (to be refined):
- Technical fit with WAFT architecture
- Feature overlap/complementarity with OpenHands
- Integration complexity
- Maintenance burden
- Community/ecosystem health
- Performance/benchmarks
- License compatibility
- Learning curve

**Process**:
1. Define alternatives clearly
2. Define evaluation criteria
3. Assign weights to criteria
4. Score each alternative on each criterion
5. Calculate weighted scores
6. Rank alternatives
7. Provide recommendations
8. Sensitivity analysis

**Output**: Decision matrix, rankings, recommendations with reasoning

**Files Created**: `_work_efforts/DECISION_YYYY-MM-DD_goose_integration.md`

---

### Phase 11: Next Steps (`/next`)
**Purpose**: Identify prioritized next actions

**Based On**:
- Decision results
- Hypothesis verification
- Current work state
- Dependencies

**Output**: Prioritized next steps with reasoning

**Files Created**: Updates to work effort or devlog

---

### Phase 12: Work Effort Update
**Purpose**: Update or create work effort for tracking

**Actions**:
1. Search `_work_efforts/` for existing goose-related work
2. If found: Update existing work effort with findings
3. If not found: Create new work effort (e.g., `WE-YYYYMMDD-goose_goose_ai_agent_evaluation`)
4. Update devlog with evaluation session

**Output**: Updated or created work effort

**Files Created**: Work effort file (if new) or updates to existing

---

## Execution Flow

```
Phase 1: Orientation → 
Phase 2: Repository Analysis → 
Phase 3: Visual Assessment → 
Phase 4: Goal Analysis → 
Phase 5: Checkpoint → 
Phase 6: Data Gathering & Hypothesis → 
Phase 7: Hypothesis Verification → 
Phase 8: Reflection → 
Phase 9: Conversation Recap → 
Phase 10: Decision Analysis → 
Phase 11: Next Steps → 
Phase 12: Work Effort Update
```

**Each phase builds on previous phases. Execute sequentially.**

---

## Key Research Areas

### Goose Capabilities
- What can goose do?
- How does it execute tasks?
- What tools does it support?
- MCP integration capabilities?
- Model support (LLM agnostic?)

### Comparison with OpenHands
- Feature overlap
- Complementary capabilities
- Integration complexity differences
- Performance differences
- Ecosystem differences

### WAFT Integration Points
- How would goose fit into WAFT architecture?
- Integration with existing agent systems
- Compatibility with WAFT's self-modification goals
- Alignment with WAFT's scientific mission

---

## Documentation Requirements

### Files Created During Evaluation

1. **Hypothesis File**: `_pyrite/hypothesis/YYYY-MM-DD_goose_integration.md`
   - Structured hypothesis with evidence
   - Verification plan
   - Predictions

2. **Checkpoint File**: `_work_efforts/CHECKPOINT_YYYY-MM-DD_goose_evaluation.md`
   - Situation report
   - Progress summary

3. **Recap File**: `_work_efforts/SESSION_RECAP_YYYY-MM-DD_goose_evaluation.md`
   - Complete session summary
   - Key findings

4. **Decision Analysis**: `_work_efforts/DECISION_YYYY-MM-DD_goose_integration.md`
   - Decision matrix
   - Calculations
   - Recommendations

5. **Devlog Update**: `_work_efforts/devlog.md`
   - Add entry for evaluation session

6. **Journal Entry**: `_pyrite/journal/ai-journal.md`
   - Reflection on evaluation process

7. **Work Effort**: `_work_efforts/WE-YYYYMMDD-goose_goose_ai_agent_evaluation/` (if new)
   - Complete work effort with findings

---

## Success Criteria

1. **Hypothesis Formed**: Clear, testable hypothesis about goose's fit
2. **Hypothesis Verified**: Evidence gathered and assessed
3. **Decision Made**: Structured decision with clear recommendation
4. **Next Steps Identified**: Prioritized action plan
5. **Documentation Complete**: All findings documented

---

## Usage Examples

### Basic Evaluation
```
/goose-eval
```

Executes all 12 phases sequentially for goose evaluation.

### Evaluation with Custom Target
```
/goose-eval evaluate langchain
```

Adapts workflow to evaluate langchain instead of goose (modify hypothesis and research areas).

### Partial Evaluation
```
/goose-eval phases 1-5
```

Executes only phases 1-5 (orientation through checkpoint).

---

## Integration with Other Commands

This command orchestrates multiple existing commands:
- `/spin-up` - Phase 1 orientation
- `/consider` - Phase 2 repository analysis
- `/visualize` - Phase 3 visual assessment
- `/analyze` - Phase 4 goal analysis
- `/checkpoint` - Phase 5 checkpoint
- `/execute` - Phase 6 data gathering
- `/verify` - Phase 7 hypothesis verification
- `/reflect` - Phase 8 reflection
- `/recap` - Phase 9 recap
- `/proceed` - Phase 10.1 context verification
- `/decide` - Phase 10.2 decision matrix
- `/next` - Phase 11 next steps

**This command coordinates these commands in the proper sequence.**

---

## Notes

- This is an evaluation, not an implementation plan
- Focus on understanding fit, not building integration yet
- Compare fairly with existing tools (e.g., OpenHands)
- Consider WAFT's unique needs (self-modification, evolution, scientific mission)
- Document everything for future reference
- Each phase should be completed before moving to next
- Can be adapted for evaluating other tools/technologies

---

## When to Use

**Use `/goose-eval` when**:
- ✅ Need systematic evaluation of a tool/technology
- ✅ Want hypothesis-driven approach
- ✅ Need structured decision-making
- ✅ Want complete documentation trail
- ✅ Evaluating AI agent tools or frameworks
- ✅ Need to compare multiple options

**Don't use `/goose-eval` when**:
- ❌ Quick decision needed (use `/decide` directly)
- ❌ Already have enough information
- ❌ Simple yes/no question
- ❌ Just need quick research (use `/execute` or web search)

---

## Customization

The workflow can be adapted for evaluating other tools by:
1. Changing research focus areas
2. Modifying hypothesis statement
3. Adjusting comparison targets
4. Updating decision criteria

**The 12-phase structure remains the same, but content adapts to evaluation target.**

---

**This command provides a reliable, repeatable workflow for systematic tool evaluation with hypothesis testing, verification, and structured decision-making.**

--- End Command ---
