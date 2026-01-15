# Report

**Generate comprehensive executive report on work completed during session.**

Creates a detailed, executive-style report summarizing all work, analysis, decisions, accomplishments, and outcomes from the current session. Perfect for documenting major initiatives, presenting progress, or creating handoff documentation.

**Use when:** End of significant work session, need executive summary, preparing handoff, or documenting major initiative completion.

---

## Purpose

This command provides:
- **Executive Summary**: High-level overview of work completed
- **Comprehensive Analysis**: All analysis, decisions, and findings
- **Accomplishment Tracking**: Completed work with evidence
- **Progress Documentation**: Status against plans and goals
- **Evidence-Based**: All claims supported by traces and documentation
- **Professional Format**: Executive-ready report format

---

## Philosophy

1. **Complete Picture**: Capture everything that happened
2. **Evidence-Based**: Every claim supported by documentation
3. **Executive-Ready**: Format suitable for stakeholders
4. **Traceable**: Links to all supporting documentation
5. **Actionable**: Clear next steps and recommendations

---

## Execution Steps

### Step 1: Gather Session Data
**Purpose**: Collect all relevant information from the session

**Actions**:
1. Review conversation history
2. Identify all checkpoints created
3. Find all critiques generated
4. Locate hypotheses formed
5. Check verification traces
6. Review work effort updates
7. Identify files created/modified
8. Check devlog entries
9. Review any analysis documents
10. Find decision matrices

**Output**: Complete dataset of session activity

---

### Step 2: Analyze Work Against Plan
**Purpose**: Compare actual work to planned work

**Actions**:
1. Identify original plan or goal
2. Map completed work to plan phases
3. Identify deviations or pivots
4. Note unplanned accomplishments
5. Assess completion percentage
6. Identify remaining work

**Output**: Progress analysis against plan

---

### Step 3: Generate Executive Report
**Purpose**: Create comprehensive report document

**Actions**:
1. Create markdown document with sections:
   - **Executive Summary**: One-page overview
   - **Objectives**: What was planned
   - **Approach**: How work was executed
   - **Analysis & Findings**: Key discoveries
   - **Decisions Made**: Important choices
   - **Accomplishments**: Completed work
   - **Evidence & Traces**: Supporting documentation
   - **Progress Status**: Against plan/goals
   - **Risks & Mitigations**: Issues identified
   - **Next Steps**: Recommended actions
   - **Recommendations**: Strategic guidance
2. Save to `_work_efforts/` directory
3. Use timestamped filename: `REPORT_YYYY-MM-DD_[TOPIC].md`
4. Generate PDF version (if brief system available)

**Output**: Complete executive report

---

### Step 4: Display Summary
**Purpose**: Show report summary in console

**Actions**:
1. Display executive summary
2. Show key metrics
3. Highlight accomplishments
4. Present next steps
5. Provide file location

**Output**: Console summary

---

## What Gets Captured

### Executive Summary
- One-page overview
- Key accomplishments
- Status summary
- Critical decisions
- Next steps

### Objectives
- Original goals/plans
- Success criteria
- Expected outcomes

### Approach
- Methodology used
- Tools employed
- Workflow executed
- Phases completed

### Analysis & Findings
- Key discoveries
- Patterns identified
- Insights gained
- Problems solved
- Opportunities found

### Decisions Made
- Important choices
- Rationale
- Alternatives considered
- Impact assessment

### Accomplishments
- Completed tasks
- Features implemented
- Documentation created
- Tests written
- Problems solved

### Evidence & Traces
- Checkpoints created
- Critiques generated
- Hypotheses formed
- Verification traces
- Analysis documents
- Decision matrices

### Progress Status
- Completion percentage
- Phases completed
- Remaining work
- Timeline status
- Goal achievement

### Risks & Mitigations
- Issues identified
- Risks discovered
- Mitigation strategies
- Blockers encountered

### Next Steps
- Immediate actions
- Recommended work
- Dependencies
- Priorities

### Recommendations
- Strategic guidance
- Best practices
- Lessons learned
- Future considerations

---

## Output Format

### Console Output

```
📊 Executive Report Generated

Report: Local-RAG Self-Evolution Integration
Date: 2026-01-13
Duration: ~2 hours

Executive Summary:
✅ Phase 1: Local-RAG Core - Complete
✅ Phase 2: Knowledge Ingestion - In Progress
⏸️ Phase 3: Agent Integration - Pending

Key Accomplishments:
- Created RAG engine wrapper
- Implemented file-based vector store
- Ingested WAFT source code
- Created agent query interface

Decisions Made:
- Selected FAISS for vector storage
- Chose sentence-transformers for embeddings
- Prioritized code ingestion first

Next Steps:
1. Complete knowledge ingestion pipeline
2. Integrate with BaseAgent.observe()
3. Test query interface

📄 Report saved: _work_efforts/REPORT_2026-01-13_local-rag-integration.md
📄 PDF saved: _work_efforts/reports/REPORT_2026-01-13_local-rag-integration.pdf
```

### Report Document Structure

```markdown
# Executive Report: [Topic/Initiative]

**Date**: YYYY-MM-DD
**Session Duration**: ~X hours
**Status**: ✅ Complete | 🚧 In Progress | ⏸️ Paused

---

## Executive Summary

[One-page overview covering:
- What was accomplished
- Key decisions made
- Current status
- Next steps]

---

## Objectives

### Original Goals
- [Goal 1]
- [Goal 2]

### Success Criteria
- [Criterion 1]
- [Criterion 2]

---

## Approach

### Methodology
[How work was executed]

### Tools & Technologies
- [Tool 1]
- [Tool 2]

### Workflow Phases
1. [Phase 1] - ✅ Complete
2. [Phase 2] - 🚧 In Progress
3. [Phase 3] - ⏸️ Pending

---

## Analysis & Findings

### Key Discoveries
- [Discovery 1 with evidence]
- [Discovery 2 with evidence]

### Patterns Identified
- [Pattern 1]
- [Pattern 2]

### Insights Gained
- [Insight 1]
- [Insight 2]

---

## Decisions Made

### Decision 1: [Title]
- **Context**: [Why decision was needed]
- **Options Considered**: [Alternatives]
- **Decision**: [What was chosen]
- **Rationale**: [Why]
- **Impact**: [Consequences]

---

## Accomplishments

### Completed Tasks
✅ [Task 1] - [Evidence link]
✅ [Task 2] - [Evidence link]

### Features Implemented
✅ [Feature 1] - [Evidence link]
✅ [Feature 2] - [Evidence link]

### Documentation Created
📄 [Doc 1] - [Link]
📄 [Doc 2] - [Link]

---

## Evidence & Traces

### Checkpoints
- [Checkpoint 1] - [Link]
- [Checkpoint 2] - [Link]

### Critiques
- [Critique 1] - [Link]
- [Critique 2] - [Link]

### Hypotheses
- [Hypothesis 1] - [Link]
- [Hypothesis 2] - [Link]

### Verification Traces
- [Trace 1] - [Link]
- [Trace 2] - [Link]

### Analysis Documents
- [Analysis 1] - [Link]
- [Analysis 2] - [Link]

---

## Progress Status

### Completion Overview
- **Overall Progress**: X% complete
- **Phases Completed**: X/Y
- **Tasks Completed**: X/Y

### Phase Breakdown
1. **Phase 1**: ✅ Complete (100%)
2. **Phase 2**: 🚧 In Progress (60%)
3. **Phase 3**: ⏸️ Pending (0%)

### Goal Achievement
- [Goal 1]: ✅ Achieved
- [Goal 2]: 🚧 In Progress

---

## Risks & Mitigations

### Issues Identified
- [Issue 1] - [Mitigation strategy]
- [Issue 2] - [Mitigation strategy]

### Blockers
- [Blocker 1] - [Resolution plan]

---

## Next Steps

### Immediate Actions (Next Session)
1. [Action 1] - [Priority]
2. [Action 2] - [Priority]

### Recommended Work
- [Work item 1]
- [Work item 2]

### Dependencies
- [Dependency 1]
- [Dependency 2]

---

## Recommendations

### Strategic Guidance
- [Recommendation 1]
- [Recommendation 2]

### Best Practices
- [Practice 1]
- [Practice 2]

### Lessons Learned
- [Lesson 1]
- [Lesson 2]

---

## Appendices

### Related Documentation
- [Doc 1] - [Link]
- [Doc 2] - [Link]

### Work Efforts
- [Work Effort 1] - [Link]
- [Work Effort 2] - [Link]

---

**Report Generated**: YYYY-MM-DD HH:MM:SS
**Generated By**: AI Assistant
```

---

## Use Cases

### 1. End of Major Initiative
**Scenario**: Completed significant work, need executive summary

**Example**:
```
User: "/report"
```

**Output**: Comprehensive report on initiative

---

### 2. Handoff Preparation
**Scenario**: Preparing to hand off work to team/stakeholder

**Example**:
```
User: "/report"
```

**Output**: Executive-ready report for handoff

---

### 3. Progress Documentation
**Scenario**: Need to document progress against plan

**Example**:
```
User: "/report"
```

**Output**: Progress report with evidence

---

### 4. Stakeholder Update
**Scenario**: Need to update stakeholders on work

**Example**:
```
User: "/report"
```

**Output**: Executive summary suitable for stakeholders

---

## Integration with Other Commands

- **`/checkpoint`**: Status snapshot (report is comprehensive summary)
- **`/recap`**: Conversation summary (report is work-focused)
- **`/verify`**: Verification (report includes verification traces)
- **`/critique`**: Critique (report includes critique findings)
- **`/hypothesis`**: Hypothesis (report includes hypotheses formed)

---

## When to Use

**Use `/report` when**:
- ✅ End of major work session
- ✅ Completed significant initiative
- ✅ Need executive summary
- ✅ Preparing handoff
- ✅ Documenting progress
- ✅ Stakeholder update needed
- ✅ Need comprehensive documentation

**Don't use `/report` when**:
- ❌ Quick status needed (use `/checkpoint`)
- ❌ Conversation summary needed (use `/recap`)
- ❌ Mid-session (use at end)

---

## Technical Details

### Data Sources

Report analyzes:
- Conversation history
- Checkpoints created
- Critiques generated
- Hypotheses formed
- Verification traces
- Work effort updates
- Files created/modified
- Devlog entries
- Analysis documents
- Decision matrices

### Output Location

- **Markdown**: `_work_efforts/REPORT_YYYY-MM-DD_[TOPIC].md`
- **PDF**: `_work_efforts/reports/REPORT_YYYY-MM-DD_[TOPIC].pdf` (if brief system available)

### Format

- **Markdown**: Structured, comprehensive
- **PDF**: Executive-ready (if generated)
- **Timestamped**: Unique filename per session
- **Evidence-Based**: All claims supported

---

## Example Workflow

```
User: [Completes Local-RAG integration work]
User: [Runs /run-it workflow]
User: "/report"

AI: [Gathers session data]
AI: [Analyzes work against plan]
AI: [Generates executive report]
AI: [Creates PDF version]
AI: [Displays summary]

AI: 📊 Executive Report Complete
    📄 Markdown: _work_efforts/REPORT_2026-01-13_local-rag-integration.md
    📄 PDF: _work_efforts/reports/REPORT_2026-01-13_local-rag-integration.pdf
    ✅ Accomplishments: 15 documented
    ✅ Evidence: 8 traces linked
    ✅ Progress: 60% complete
    🎯 Next: Complete Phase 2 ingestion
```

---

**This command creates a comprehensive, executive-ready report perfect for documenting major work, preparing handoffs, and presenting progress to stakeholders.**

--- End Command ---
