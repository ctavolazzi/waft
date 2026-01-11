# Orchestrate

**Complete workflow orchestration: orientation, analysis, visualization, goal analysis, checkpoint, data gathering, hypothesis formation, verification, reflection, recap, and decision-making.**

Orchestrates a comprehensive workflow that combines orientation, repository analysis, visualization, goal analysis, checkpoint creation, systematic data gathering, hypothesis formation, verification, reflection, conversation recap, and strategic decision-making. Designed for starting new work with thorough understanding, systematic investigation, and informed planning.

**Use when:** Starting a new investigation, feature, or significant work that requires complete understanding, systematic data gathering, hypothesis-driven investigation, verification, reflection, and strategic decision-making.

---

## Purpose

This command provides:
- **Complete Orientation**: Full understanding of current state via `/spin-up`
- **Repository Analysis**: Strategic consideration of approach via `/consider`
- **Visual State Assessment**: Interactive visualization via `/visualize`
- **Goal Analysis**: Deep analysis of objectives via `/analyze`
- **Status Checkpoint**: Recovery point and documentation via `/checkpoint`
- **Systematic Data Gathering**: Comprehensive probe execution via `/execute`
- **Hypothesis Formation**: Structured hypothesis development
- **Evidence-Based Verification**: Traceable hypothesis validation via `/verify`
- **Reflective Learning**: Meta-cognitive review via `/reflect`
- **Conversation Documentation**: Complete session recap via `/recap`
- **Context Verification**: Assumption checking via `/proceed`
- **Strategic Decision-Making**: Calculated decisions via `/decide`

---

## Workflow Sequence

### Phase 1: Orientation

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

### Phase 2: Repository Analysis & Engineering Consideration

**Execute**: `/consider`

**Purpose**: Pause, analyze, and present options with recommendations

**Focus Areas**:
- Current repository state
- Whether to run full `/engineering` workflow
- Available paths forward
- Trade-offs and options
- Recommendations for approach

**Expected Output**:
- Situation analysis
- Options identified (including whether to do full engineering workflow)
- Trade-off evaluation
- Recommendations with reasoning
- Next steps

**Documentation**: Capture analysis and recommendations

---

### Phase 3: Visual State Assessment

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

### Phase 4: Goal Analysis

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

### Phase 5: Checkpoint Creation

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

### Phase 6: Data Gathering & Probe Execution

**Execute**: `/execute` with probe instructions

**Purpose**: Gather comprehensive data through systematic probes

**Probe Sequence**:

1. **Structural Probes**:
   - Project structure analysis
   - Architecture mapping
   - Dependency analysis
   - Pattern identification
   - Code organization review

2. **Functional Probes**:
   - Feature mapping
   - API exploration
   - Integration points
   - Testing coverage
   - Workflow analysis

3. **Data Probes**:
   - Git history analysis
   - Work effort review
   - Documentation review
   - Configuration analysis
   - Recent changes analysis

4. **System Probes**:
   - Environment verification
   - Dependency health
   - Build system status
   - Test suite status
   - Performance indicators

**Expected Output**:
- Comprehensive data collection
- Evidence gathered
- Assumptions tested
- Patterns identified
- Gaps discovered

**Documentation**: Document all probe findings in `_pyrite/active/YYYY-MM-DD_probes_*.md`

---

### Phase 7: Hypothesis Formation

**Purpose**: Form testable hypotheses based on probe findings

**Hypothesis Development**:

1. **Review Probe Findings**:
   - Consolidate all probe data
   - Identify patterns and anomalies
   - Note contradictions
   - Highlight key observations

2. **Formulate Hypotheses**:
   - Create clear, testable hypothesis statements
   - Identify supporting evidence
   - Note contradicting evidence
   - Define verification methods
   - Make predictions
   - Assess confidence level

**Hypothesis Format**:
```markdown
# Hypothesis: [Title]

**Date**: YYYY-MM-DD HH:MM:SS
**Status**: Initial | Refined | Verified | Rejected
**Confidence**: Low | Medium | High

## Statement
[Clear, testable hypothesis statement]

## Context
[Background information, why this hypothesis matters]

## Evidence Supporting
### Strong Evidence
- [Evidence 1 with source/reference]
- [Evidence 2 with source/reference]

### Moderate Evidence
- [Evidence 3 with source/reference]

### Weak Evidence
- [Evidence 4 with source/reference]

## Evidence Contradicting
- [Contradicting evidence 1 with source/reference]
- [Contradicting evidence 2 with source/reference]

## Verification Plan
### Method 1: [Method Name]
- **What**: [What to check]
- **How**: [How to verify]
- **Expected**: [What we expect to find]
- **Status**: [ ] Not Started | [ ] In Progress | [x] Complete

### Method 2: [Method Name]
- [Same structure]

## Predictions
### If Hypothesis is True
- [Prediction 1]: We expect to observe [specific observation]
- [Prediction 2]: We expect to find [specific finding]

### If Hypothesis is False
- [Prediction 1]: We expect to observe [different observation]
- [Prediction 2]: We expect to find [different finding]

## Confidence Assessment
**Current Confidence**: [Low | Medium | High]

**Reasoning**:
- [Why confidence is at this level]
- [What would increase confidence]
- [What would decrease confidence]

## Next Steps
1. [Next verification step]
2. [Next investigation]
3. [Next action]

## Related Documentation
- [Link to checkpoint]
- [Link to work effort]
- [Link to probe findings]
- [Link to analysis report]
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
   - Note discrepancies

2. **Test Predictions**:
   - Check if predictions hold
   - Document actual vs expected
   - Note discrepancies
   - Update confidence

3. **Evidence Review**:
   - Review supporting evidence
   - Review contradicting evidence
   - Assess evidence strength
   - Identify gaps

4. **Confidence Assessment**:
   - Update confidence level
   - Document reasoning
   - Note verification gaps
   - Update hypothesis status

**Expected Output**:
- Verification traces for each claim
- Evidence documentation
- Confidence assessment
- Updated hypothesis status

**Documentation**: Update hypothesis with verification results, create verification traces in `_pyrite/standards/verification/traces/`

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

### Phase 11: Context Verification & Proceeding

**Execute**: `/proceed`

**Purpose**: Verify context and assumptions before proceeding

**Proceed Steps**:
1. Context verification
2. Assumption checking
3. Ambiguity resolution
4. Flight check
5. Verified continuation

**Expected Output**:
- Verified understanding
- Assumptions checked
- Ambiguities resolved
- Ready to proceed

**Documentation**: Document verified context and assumptions

---

### Phase 12: Strategic Decision-Making

**Execute**: `/decide`

**Purpose**: Run mathematical decision matrix calculations

**Decision Process**:
1. Problem definition
2. Criteria development
3. Weighting
4. Scoring
5. Calculation
6. Analysis
7. Presentation

**Expected Output**:
- Decision matrix with calculations
- Recommendations
- Next steps
- Rationale

**Documentation**: Decision analysis saved, recommendations documented

---

## Complete Execution Sequence

```
1. /spin-up                    → Orientation
2. /consider                   → Repository analysis & engineering consideration
3. /visualize                  → Visual state assessment
4. /analyze                    → Goal analysis
5. /checkpoint                 → Status checkpoint
6. /execute [probes]           → Data gathering & probe execution
7. [Form hypothesis]            → Hypothesis formation
8. /verify                     → Hypothesis verification
9. /reflect                    → Reflection
10. /recap                     → Conversation recap
11. /proceed                   → Context verification
12. /decide                    → Decision-making
```

---

## Full Prompt Template

Use this complete prompt to execute the entire workflow:

```markdown
I need you to execute a comprehensive orchestration workflow to understand this repository,
analyze the current state, gather data, form hypotheses, verify them, reflect on the work,
recap the conversation, and make informed decisions. Please execute the following sequence:

**Phase 1: Orientation**
Execute `/spin-up` to get oriented to the codebase quickly. Capture:
- Environment status (date, disk, MCP health)
- Git status across repos
- Active work efforts
- Recent history
- Previous understanding

**Phase 2: Repository Analysis & Engineering Consideration**
Execute `/consider` to analyze the repository and consider whether to run full engineering workflow:
- Current repository state
- Available paths forward (including whether to do full `/engineering` workflow)
- Trade-offs and options
- Recommendations for approach

**Phase 3: Visual State Assessment**
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

**Phase 6: Data Gathering & Probe Execution**
Execute `/execute` with the following probe sequence:

1. **Structural Probes**:
   - Analyze project structure and organization
   - Map architecture and component relationships
   - Identify dependencies (internal and external)
   - Discover patterns and conventions
   - Review code organization

2. **Functional Probes**:
   - Map features and functionality
   - Explore API boundaries and interfaces
   - Identify integration points
   - Assess testing coverage
   - Analyze workflows

3. **Data Probes**:
   - Analyze git history and commit patterns
   - Review work efforts and progress
   - Examine documentation and decisions
   - Analyze configuration and setup
   - Review recent changes

4. **System Probes**:
   - Verify environment setup
   - Check dependency health
   - Assess build system status
   - Review test suite status
   - Check performance indicators

**Phase 7: Hypothesis Formation**
Based on probe findings, formulate testable hypotheses:
- Clear hypothesis statement
- Supporting evidence
- Contradicting evidence
- Verification plan
- Predictions
- Confidence level

Save hypothesis to: `_pyrite/hypothesis/YYYY-MM-DD_[hypothesis-name].md`

**Phase 8: Verification**
Execute `/verify` to verify the hypothesis:
- Verify each claim in the hypothesis
- Test predictions
- Review evidence (supporting and contradicting)
- Assess confidence level
- Update hypothesis with verification results

**Phase 9: Reflection**
Execute `/reflect` to write a journal entry:
- Reflect on what you're doing
- Document what you're thinking and learning
- Identify patterns you notice
- Note questions and uncertainties
- Meta-reflect on the process

**Phase 10: Recap**
Execute `/recap` to create a conversation summary:
- Summarize the entire conversation
- Extract key points and decisions
- Document accomplishments
- Track open questions
- Identify next steps

**Phase 11: Proceed**
Execute `/proceed` to verify context and assumptions:
- Verify understanding
- Check assumptions
- Resolve ambiguities
- Perform flight check
- Proceed with verified understanding

**Phase 12: Decide**
Execute `/decide` to make strategic decisions:
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

## Usage Examples

### Standard Orchestration
```
/orchestrate
```

Executes the complete workflow sequence automatically.

### Custom Focus Area
```
/orchestrate --focus "authentication system"
```

Focuses probes and hypothesis on specific area.

### Quick Orchestration (Skip Some Phases)
```
/orchestrate --quick
```

Runs essential phases only (spin-up, consider, analyze, execute, verify, decide).

---

## Integration with Other Commands

This command orchestrates:
- `/spin-up` - Orientation
- `/consider` - Repository analysis
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

**Use `/orchestrate` when**:
- ✅ Starting new investigation or feature
- ✅ Need systematic understanding
- ✅ Want to form and verify hypotheses
- ✅ Need comprehensive workflow
- ✅ Starting significant new work
- ✅ Want thorough analysis and planning
- ✅ Need strategic decision-making support

**Don't use `/orchestrate` when**:
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
8. **Use Tools Actively**: Leverage Empirica, _pyrite, MCPs, waft throughout

---

## Time Estimates

- **Phase 1** (spin-up): ~1-2 minutes
- **Phase 2** (consider): ~2-5 minutes
- **Phase 3** (visualize): ~1-2 minutes
- **Phase 4** (analyze): ~3-8 minutes
- **Phase 5** (checkpoint): ~1-2 minutes
- **Phase 6** (execute probes): ~5-15 minutes
- **Phase 7** (hypothesis): ~3-5 minutes
- **Phase 8** (verify): ~5-10 minutes
- **Phase 9** (reflect): ~2-3 minutes
- **Phase 10** (recap): ~2-3 minutes
- **Phase 11** (proceed): ~1-2 minutes
- **Phase 12** (decide): ~5-10 minutes

**Total**: ~30-60 minutes for complete orchestration

---

## Error Handling

If any phase fails:
- Document the failure
- Continue with remaining phases if possible
- Note what was skipped
- Provide summary of what completed vs. what failed
- Suggest remediation steps

---

**This command provides a complete workflow from orientation through hypothesis formation, verification, reflection, recap, and strategic decision-making - perfect for starting new work with thorough understanding and systematic approach.**

--- End Command ---
