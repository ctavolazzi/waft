# Hypothesis

**Comprehensive workflow: orientation, analysis, planning, and hypothesis formation.**

Orchestrates a complete workflow from orientation through data gathering, hypothesis formation, verification, reflection, and decision-making. Designed for starting new work with thorough understanding and systematic approach.

**Use when:** Starting a new investigation, feature, or significant work that requires deep understanding, systematic data gathering, hypothesis formation, and careful planning.

---

## Purpose

This command provides:
- **Complete Orientation**: Full understanding of current state
- **Systematic Analysis**: Deep analysis of repository and goals
- **Data Gathering**: Comprehensive probe execution
- **Hypothesis Formation**: Structured hypothesis development
- **Verification**: Evidence-based hypothesis validation
- **Reflection & Planning**: Meta-cognitive review and decision-making

---

## Workflow Sequence

### Phase 1: Orientation & Context Gathering

**Execute**: `/spin-up`

**Purpose**: Get oriented to the codebase quickly

**Expected Output**:
- Environment status (date, disk space, MCP health)
- Git status across repos
- Active work efforts
- Recent history from devlog
- Previous understanding state
- Recommended next step

**Documentation**: Note key findings for later reference

---

### Phase 2: Repository Analysis & Consideration

**Execute**: `/consider`

**Purpose**: Pause, analyze, and present options with recommendations

**Focus Areas**:
- Current repository state
- Available paths forward
- Trade-offs and options
- Recommendations for approach

**Expected Output**:
- Situation analysis
- Options identified
- Trade-off evaluation
- Recommendations with reasoning
- Next steps

**Documentation**: Capture analysis and recommendations

---

### Phase 3: Engineering Workflow (Reference)

**Note**: `/engineering` is a complete workflow. For this command, we reference it but focus on specific phases.

**Key Phases to Consider**:
- **Explore**: Deep understanding of structure and architecture
- **Draft Plan**: Initial planning based on understanding
- **Critique Plan**: Review and refine approach

**Documentation**: Reference engineering workflow patterns

---

### Phase 4: Visual State Assessment

**Execute**: `/visualize`

**Purpose**: Create interactive browser UI to visualize current state

**Expected Output**:
- Standalone HTML dashboard
- Visual representation of:
  - Project overview
  - Git status
  - Active work
  - Project structure
  - System status
- Auto-opens in browser

**Documentation**: Note visual insights and patterns observed

---

### Phase 5: Goal Analysis

**Execute**: `/analyze`

**Purpose**: Analyze the goal at hand, transform data into decisions

**If Phase 1 data exists**: Analyze it
**If not**: Run `/phase1` first, then analyze

**Expected Output**:
- Health analysis
- Issue identification
- Opportunity discovery
- Pattern analysis
- Insight generation
- Action planning with priorities

**Documentation**: Save analysis report, note key insights

---

### Phase 6: Checkpoint Creation

**Execute**: `/checkpoint`

**Purpose**: Create situation report and status update

**Expected Output**:
- Checkpoint file in `_work_efforts/`
- Chat recap
- Current state snapshot
- Work progress summary
- Next steps identified
- Devlog updated

**Documentation**: Checkpoint file created and linked

---

### Phase 7: Data Gathering & Hypothesis Formation

**Execute**: `/execute` with probe instructions

**Purpose**: Gather comprehensive data and form initial hypothesis

**Probe Sequence**:

1. **Structural Probes**:
   - Project structure analysis
   - Architecture mapping
   - Dependency analysis
   - Pattern identification

2. **Functional Probes**:
   - Feature mapping
   - API exploration
   - Integration points
   - Testing coverage

3. **Data Probes**:
   - Git history analysis
   - Work effort review
   - Documentation review
   - Configuration analysis

4. **Hypothesis Formation**:
   - Based on probe findings
   - Formulate testable hypothesis
   - Identify verification methods
   - Document hypothesis structure

**Hypothesis Format**:
```markdown
# Hypothesis: [Title]

**Date**: YYYY-MM-DD HH:MM:SS
**Status**: Initial | Refined | Verified | Rejected

## Statement
[Clear, testable hypothesis statement]

## Evidence Supporting
- [Evidence 1]
- [Evidence 2]
- [Evidence 3]

## Evidence Contradicting
- [Contradicting evidence 1]
- [Contradicting evidence 2]

## Verification Plan
1. [Verification method 1]
2. [Verification method 2]
3. [Verification method 3]

## Predictions
- If hypothesis is true, we expect: [prediction 1]
- If hypothesis is false, we expect: [prediction 2]

## Confidence Level
[Low | Medium | High] - [Reasoning]
```

**Documentation**: Save hypothesis to `_pyrite/hypothesis/YYYY-MM-DD_[hypothesis-name].md`

---

### Phase 8: Hypothesis Verification

**Execute**: `/verify`

**Purpose**: Lightweight diagnostic verification with traceable evidence

**Verification Steps**:
1. **Verify Hypothesis Claims**:
   - Check each claim in hypothesis
   - Gather evidence for each claim
   - Document verification traces

2. **Test Predictions**:
   - Check if predictions hold
   - Document actual vs expected
   - Note discrepancies

3. **Evidence Review**:
   - Review supporting evidence
   - Review contradicting evidence
   - Assess evidence strength

4. **Confidence Assessment**:
   - Update confidence level
   - Document reasoning
   - Note verification gaps

**Expected Output**:
- Verification traces for each claim
- Evidence documentation
- Confidence assessment
- Updated hypothesis status

**Documentation**: Update hypothesis with verification results, create verification traces

---

### Phase 9: Reflection

**Execute**: `/reflect`

**Purpose**: Induce AI to write in its journal - reflect on current work

**Reflection Areas**:
- What I'm doing
- What I'm thinking
- What I'm learning
- Patterns I notice
- Questions I have
- How I feel about this
- What I'd do differently
- Meta-reflection

**Expected Output**:
- Journal entry in `_pyrite/journal/ai-journal.md`
- Deep reflection on the process
- Insights and learnings
- Self-awareness observations

**Documentation**: Journal entry created

---

### Phase 10: Conversation Recap

**Execute**: `/recap`

**Purpose**: Conversation recap and session summary

**Expected Output**:
- Complete conversation summary
- Key points extraction
- Decision documentation
- Accomplishment tracking
- Question tracking
- Next steps

**Documentation**: Recap saved to `_work_efforts/SESSION_RECAP_YYYY-MM-DD.md`

---

### Phase 11: Proceed to Decision

**Execute**: `/proceed` then `/decide`

**Purpose**: Verify context and assumptions, then make calculated decision

**Proceed Steps**:
1. Context verification
2. Assumption checking
3. Ambiguity resolution
4. Flight check
5. Verified continuation

**Decide Steps**:
1. Problem definition
2. Criteria development
3. Weighting
4. Scoring
5. Calculation
6. Analysis
7. Presentation

**Expected Output**:
- Verified understanding
- Decision matrix with calculations
- Recommendations
- Next steps

**Documentation**: Decision analysis saved, recommendations documented

---

## Complete Execution Sequence

```
1. /spin-up                    → Orientation
2. /consider                   → Repository analysis
3. /visualize                  → Visual state assessment
4. /analyze                    → Goal analysis
5. /checkpoint                 → Status checkpoint
6. /execute [probes]           → Data gathering & hypothesis
7. /verify                     → Hypothesis verification
8. /reflect                    → Reflection
9. /recap                      → Conversation recap
10. /proceed                   → Context verification
11. /decide                    → Decision-making
```

---

## Full Prompt Template

Use this complete prompt to execute the entire workflow:

```markdown
I need you to execute a comprehensive workflow to understand this repository,
analyze the current state, gather data, form hypotheses, and make informed
decisions. Please execute the following sequence:

**Phase 1: Orientation**
Execute `/spin-up` to get oriented to the codebase quickly. Capture:
- Environment status (date, disk, MCP health)
- Git status across repos
- Active work efforts
- Recent history
- Previous understanding

**Phase 2: Repository Analysis**
Execute `/consider` to analyze the repository and present options:
- Current repository state
- Available paths forward
- Trade-offs and options
- Recommendations for approach

**Phase 3: Visual Assessment**
Execute `/visualize` to create an interactive dashboard showing:
- Project overview
- Git status
- Active work
- Project structure
- System status

**Phase 4: Goal Analysis**
Execute `/analyze` to analyze the goal at hand:
- If Phase 1 data exists, analyze it
- If not, run `/phase1` first, then analyze
- Generate insights and action plans

**Phase 5: Checkpoint**
Execute `/checkpoint` to create a situation report:
- Chat recap
- Current state snapshot
- Work progress
- Next steps

**Phase 6: Data Gathering & Hypothesis**
Execute `/execute` with the following probe sequence:

1. **Structural Probes**:
   - Analyze project structure and organization
   - Map architecture and component relationships
   - Identify dependencies (internal and external)
   - Discover patterns and conventions

2. **Functional Probes**:
   - Map features and functionality
   - Explore API boundaries and interfaces
   - Identify integration points
   - Assess testing coverage

3. **Data Probes**:
   - Analyze git history and commit patterns
   - Review work efforts and progress
   - Examine documentation and decisions
   - Analyze configuration and setup

4. **Hypothesis Formation**:
   Based on probe findings, formulate a testable hypothesis:
   - Clear hypothesis statement
   - Supporting evidence
   - Contradicting evidence
   - Verification plan
   - Predictions
   - Confidence level

   Save hypothesis to: `_pyrite/hypothesis/YYYY-MM-DD_[hypothesis-name].md`

**Phase 7: Verification**
Execute `/verify` to verify the hypothesis:
- Verify each claim in the hypothesis
- Test predictions
- Review evidence (supporting and contradicting)
- Assess confidence level
- Update hypothesis with verification results

**Phase 8: Reflection**
Execute `/reflect` to write a journal entry:
- Reflect on what you're doing
- Document what you're thinking and learning
- Identify patterns you notice
- Note questions and uncertainties
- Meta-reflect on the process

**Phase 9: Recap**
Execute `/recap` to create a conversation summary:
- Summarize the entire conversation
- Extract key points and decisions
- Document accomplishments
- Track open questions
- Identify next steps

**Phase 10: Proceed & Decide**
Execute `/proceed` to verify context and assumptions, then execute `/decide`:
- Verify understanding
- Check assumptions
- Resolve ambiguities
- Then use decision matrix to:
  - Define the decision problem
  - Identify alternatives
  - Define criteria
  - Assign weights
  - Score alternatives
  - Calculate and rank
  - Provide recommendations

**Documentation Requirements:**
- Document findings at each phase
- Create hypothesis file with proper structure
- Update checkpoint and devlog
- Save verification traces
- Create journal entry
- Generate recap document
- Document decision analysis

**Output Expectations:**
After completing all phases, provide:
1. Summary of all phases completed
2. Key findings from each phase
3. Hypothesis statement and verification status
4. Decision recommendations
5. Next steps with priorities
6. Links to all documentation created

Please proceed through all phases systematically, documenting as you go.
```

---

## Hypothesis File Structure

When creating hypothesis files, use this structure:

```markdown
# Hypothesis: [Clear Title]

**Date**: YYYY-MM-DD HH:MM:SS
**Status**: Initial | Refined | Verified | Rejected | Partially Verified
**Confidence**: Low | Medium | High
**Related Work**: [Links to work efforts, checkpoints, etc.]

---

## Statement

[One clear, testable hypothesis statement. Should be specific, measurable, and falsifiable.]

**Example**: "The authentication system uses JWT tokens stored in HTTP-only cookies, and the token refresh mechanism is implemented in the frontend JavaScript."

---

## Context

[Background information, why this hypothesis matters, what problem it addresses]

---

## Evidence Supporting

### Strong Evidence
- [Evidence 1 with source/reference]
- [Evidence 2 with source/reference]

### Moderate Evidence
- [Evidence 3 with source/reference]
- [Evidence 4 with source/reference]

### Weak Evidence
- [Evidence 5 with source/reference]

---

## Evidence Contradicting

- [Contradicting evidence 1 with source/reference]
- [Contradicting evidence 2 with source/reference]

---

## Verification Plan

### Method 1: [Method Name]
- **What**: [What to check]
- **How**: [How to verify]
- **Expected**: [What we expect to find]
- **Status**: [ ] Not Started | [ ] In Progress | [x] Complete

### Method 2: [Method Name]
- **What**: [What to check]
- **How**: [How to verify]
- **Expected**: [What we expect to find]
- **Status**: [ ] Not Started | [ ] In Progress | [x] Complete

---

## Predictions

### If Hypothesis is True
- [Prediction 1]: We expect to observe [specific observation]
- [Prediction 2]: We expect to find [specific finding]

### If Hypothesis is False
- [Prediction 1]: We expect to observe [different observation]
- [Prediction 2]: We expect to find [different finding]

---

## Verification Results

### Verification 1: [Method Name]
- **Date**: YYYY-MM-DD
- **Result**: [What was found]
- **Status**: ✅ Verified | ⚠️ Partial | ❌ Contradicted
- **Evidence**: [Link to verification trace]

### Verification 2: [Method Name]
- **Date**: YYYY-MM-DD
- **Result**: [What was found]
- **Status**: ✅ Verified | ⚠️ Partial | ❌ Contradicted
- **Evidence**: [Link to verification trace]

---

## Confidence Assessment

**Current Confidence**: [Low | Medium | High]

**Reasoning**:
- [Why confidence is at this level]
- [What would increase confidence]
- [What would decrease confidence]

**Last Updated**: YYYY-MM-DD HH:MM:SS

---

## Next Steps

1. [Next verification step]
2. [Next investigation]
3. [Next action]

---

## Related Documentation

- [Link to checkpoint]
- [Link to work effort]
- [Link to verification traces]
- [Link to analysis report]
- [Link to recap]

---

**Hypothesis Created**: YYYY-MM-DD HH:MM:SS
**Last Updated**: YYYY-MM-DD HH:MM:SS
```

---

## Usage Examples

### Standard Hypothesis Workflow
```
/hypothesis
```

Executes the complete workflow sequence automatically.

### Custom Hypothesis Focus
```
/hypothesis --focus "authentication system"
```

Focuses probes and hypothesis on specific area.

### Quick Hypothesis (Skip Some Phases)
```
/hypothesis --quick
```

Runs essential phases only (spin-up, consider, analyze, execute, verify, decide).

---

## Integration with Other Commands

This command orchestrates:
- `/spin-up` - Orientation
- `/consider` - Analysis
- `/visualize` - Visualization
- `/analyze` - Goal analysis
- `/checkpoint` - Status checkpoint
- `/execute` - Data gathering
- `/verify` - Hypothesis verification
- `/reflect` - Reflection
- `/recap` - Conversation recap
- `/proceed` - Context verification
- `/decide` - Decision-making

---

## When to Use

**Use `/hypothesis` when**:
- ✅ Starting new investigation or feature
- ✅ Need systematic understanding
- ✅ Want to form and verify hypotheses
- ✅ Need comprehensive workflow
- ✅ Starting significant new work
- ✅ Want thorough analysis and planning

**Don't use `/hypothesis` when**:
- ❌ Quick task or simple change
- ❌ Already have full understanding
- ❌ Just need one specific command
- ❌ Time-constrained (use individual commands)

---

## Output Summary

After completion, provides:
1. **Orientation Summary**: Current state understanding
2. **Analysis Results**: Repository and goal analysis
3. **Visual Dashboard**: Interactive state visualization
4. **Hypothesis Document**: Structured hypothesis with evidence
5. **Verification Traces**: Evidence for each claim
6. **Reflection Entry**: Journal entry with insights
7. **Conversation Recap**: Complete session summary
8. **Decision Analysis**: Calculated recommendations
9. **Next Steps**: Prioritized action plan

---

## Best Practices

1. **Document Everything**: Save findings at each phase
2. **Be Specific**: Clear, testable hypotheses
3. **Gather Evidence**: Support claims with evidence
4. **Verify Thoroughly**: Test predictions and claims
5. **Reflect Deeply**: Capture learnings and insights
6. **Decide Systematically**: Use decision matrix for choices
7. **Link Everything**: Connect related documentation

---

**This command provides a complete workflow from orientation through hypothesis formation, verification, reflection, and decision-making - perfect for starting new work with thorough understanding and systematic approach.**

--- End Command ---