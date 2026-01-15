---
name: Enhance Engineering Command with Scientific Method and Hypothesis Testing
overview: Transform the engineering command to heavily emphasize hypothesis testing using the scientific method and make Empirica usage central to the workflow. Add hypothesis formation, experimentation, observation, and validation throughout all phases.
todos:
  - id: add_scientific_method_framework
    content: Add scientific method framework section explaining hypothesis → experiment → observation → conclusion workflow
    status: pending
  - id: enhance_phase1_hypothesis
    content: Enhance Phase 1 (Spin-Up) with hypothesis formation about current state and Empirica session creation
    status: pending
    dependencies:
      - add_scientific_method_framework
  - id: transform_phase2_hypothesis
    content: Transform Phase 2 (Explore) into hypothesis-driven exploration with specific hypothesis examples for each area
    status: pending
    dependencies:
      - add_scientific_method_framework
  - id: enhance_phase3_planning_hypothesis
    content: Enhance Phase 3 (Draft Plan) with hypothesis formation about solution approach and plan completeness
    status: pending
    dependencies:
      - add_scientific_method_framework
  - id: enhance_phase4_critique_hypothesis
    content: Enhance Phase 4 (Critique Plan) with hypothesis testing for plan completeness, feasibility, and assumptions
    status: pending
    dependencies:
      - add_scientific_method_framework
  - id: enhance_phase5_finalize_hypothesis
    content: Enhance Phase 5 (Finalize Plan) with final hypothesis validation using Empirica assess and check commands
    status: pending
    dependencies:
      - add_scientific_method_framework
  - id: transform_phase6_hypothesis
    content: Transform Phase 6 (Begin) into hypothesis-driven implementation with testing workflow for each change
    status: pending
    dependencies:
      - add_scientific_method_framework
  - id: add_empirica_integration_section
    content: Add comprehensive Empirica integration section with command examples and usage patterns for each phase
    status: pending
  - id: add_hypothesis_checklist
    content: Add hypothesis testing checklist section with items for each phase
    status: pending
    dependencies:
      - add_scientific_method_framework
  - id: add_scientific_method_examples
    content: Add concrete examples of hypothesis testing workflow throughout the document
    status: pending
    dependencies:
      - add_scientific_method_framework
  - id: update_tool_usage_empirica
    content: Update Tool Usage section to emphasize Empirica as primary tool with mandatory checks and examples
    status: pending
    dependencies:
      - add_empirica_integration_section
  - id: update_notes_scientific_method
    content: Update Notes section to emphasize scientific method, hypothesis testing, and Empirica usage
    status: pending
    dependencies:
      - add_scientific_method_framework

category: hopes
confidence: 0.67
constellation_date: 2026-01-14
---

# Enhance Engineering Command with Scientific Method and Hypothesis Testing

## Overview

Transform `.cursor/commands/engineering.md` to integrate the scientific method throughout all phases, with heavy emphasis on hypothesis testing and Empirica usage for epistemic tracking.

## Key Changes

### 1. Add Scientific Method Framework

Add a new section explaining the scientific method workflow that will be used throughout:

```markdown
## Scientific Method Workflow

For every understanding, assumption, or approach:

1. **Hypothesis Formation**: State what you believe to be true
2. **Experiment Design**: Design a test to validate/invalidate
3. **Experiment Execution**: Run the test
4. **Observation**: Record what actually happened
5. **Conclusion**: Validate or invalidate hypothesis
6. **Iterate**: Refine hypothesis and repeat if needed
```

### 2. Enhance Phase 1: Spin-Up with Hypothesis Testing

**Add hypothesis formation step:**
- Form hypotheses about current state (e.g., "No uncommitted changes", "All MCPs healthy")
- Test each hypothesis
- Log results in Empirica

**Add Empirica integration:**
- Check if Empirica initialized (warn if not, but continue)
- Create session if available: `waft session create --ai-id waft --type engineering`
- Log initial hypotheses: `waft finding log "Hypothesis: X" --impact 0.5`
- Use `waft check` for safety gates before proceeding

### 3. Transform Phase 2: Explore into Hypothesis-Driven Exploration

**Restructure exploration around hypotheses:**

For each exploration area (structure, architecture, dependencies, etc.):

1. **Form Hypotheses**:
   - "The codebase uses X pattern for Y"
   - "Component A depends on Component B"
   - "This function handles X case"

2. **Design Experiments**:
   - Code search queries
   - File reading
   - Test execution
   - GitHub code search

3. **Execute Experiments**:
   - Run searches
   - Read code
   - Execute tests
   - Analyze results

4. **Observe & Log**:
   - Document findings in `_pyrite/active/`
   - Log validated hypotheses: `waft finding log "Validated: X" --impact 0.7`
   - Log invalidated hypotheses: `waft finding log "Invalidated: X, actual: Y" --impact 0.8`
   - Log unknowns: `waft unknown log "Need to test: X"`

5. **Form New Hypotheses**:
   - Based on observations, form new hypotheses
   - Continue iterating

**Add specific hypothesis examples for each exploration area:**
- Structure: "Project uses src/ layout", "Tests in tests/ directory"
- Architecture: "Uses MVC pattern", "Components communicate via events"
- Dependencies: "Uses X library for Y", "Internal modules follow Z pattern"
- Patterns: "Error handling uses X pattern", "Logging uses Y approach"

### 4. Enhance Phase 3: Draft Plan with Hypothesis-Driven Planning

**Add hypothesis formation for planning:**
- "This approach will solve the problem"
- "This task breakdown is complete"
- "This complexity estimate is accurate"

**Test planning hypotheses:**
- Review against exploration findings
- Check for missing dependencies
- Validate assumptions
- Use `waft check` for plan validation

**Log planning hypotheses:**
- `waft finding log "Planning hypothesis: X approach will work" --impact 0.6`
- `waft unknown log "Uncertain about: Y aspect"`

### 5. Enhance Phase 4: Critique Plan with Hypothesis Testing

**Add hypothesis testing for critique:**
- "This plan is complete" → Test: Check all requirements covered
- "This approach is feasible" → Test: Review complexity, dependencies
- "Assumptions are correct" → Test: Validate each assumption
- "Dependencies are accurate" → Test: Trace dependencies

**Log critique findings:**
- Validated hypotheses: `waft finding log "Validated: Plan is complete" --impact 0.7`
- Invalidated hypotheses: `waft finding log "Invalidated: Missing X requirement" --impact 0.8`

### 6. Enhance Phase 5: Finalize Plan with Final Hypothesis Validation

**Add final hypothesis checks:**
- "Plan is ready for implementation" → Test: Final review checklist
- "All tickets are properly scoped" → Test: Review each ticket
- "Dependencies are correct" → Test: Final dependency check

**Use Empirica for final validation:**
- `waft assess` - Check epistemic state
- `waft check` - Safety gate before implementation
- Log final state: `waft finding log "Plan finalized, epistemic state: X" --impact 0.8`

### 7. Transform Phase 6: Begin into Hypothesis-Driven Implementation

**Add hypothesis testing for each implementation step:**

For each ticket/change:

1. **Form Hypothesis**:
   - "This change will fix the bug"
   - "This function will work correctly"
   - "This integration will work"

2. **Design Test**:
   - Unit test
   - Integration test
   - Manual verification
   - Code review

3. **Implement & Test**:
   - Make change
   - Run tests
   - Verify behavior
   - Check `waft verify`

4. **Observe & Log**:
   - Document results
   - Log validated: `waft finding log "Validated: X works" --impact 0.7`
   - Log invalidated: `waft finding log "Invalidated: X, fixed with Y" --impact 0.8`
   - Log unknowns: `waft unknown log "Unexpected behavior: X"`

5. **Iterate**:
   - Refine approach if hypothesis invalidated
   - Form new hypotheses
   - Continue testing

**Add preflight/postflight assessments:**
- Preflight: `waft session bootstrap` or manual preflight assessment
- Postflight: Submit postflight assessment with learning summary

### 8. Add Comprehensive Empirica Integration Section

**New section: "Empirica Usage Throughout"**

For each phase, specify:
- Which Empirica commands to use
- When to use them
- What to log
- How to interpret results

**Commands to emphasize:**
- `waft session create` - Start of each phase
- `waft session bootstrap` - Load context
- `waft finding log` - Log validated hypotheses, discoveries
- `waft unknown log` - Log invalidated hypotheses, gaps
- `waft check` - Safety gates before major operations
- `waft assess` - Check epistemic state
- `waft goal` - Create goals with epistemic scope

**Add examples for each command usage**

### 9. Add Hypothesis Testing Checklist

**New section: "Hypothesis Testing Checklist"**

For each phase, checklist items like:
- [ ] Formed hypotheses about X
- [ ] Designed experiments to test hypotheses
- [ ] Executed experiments
- [ ] Observed and documented results
- [ ] Logged validated hypotheses in Empirica
- [ ] Logged invalidated hypotheses in Empirica
- [ ] Formed new hypotheses based on observations
- [ ] Iterated if needed

### 10. Update Tool Usage Section

**Enhance "Tool Usage Throughout" section:**

Add Empirica as first/primary tool with:
- Mandatory checks (warn if not initialized)
- Specific command examples
- Integration with hypothesis testing
- Epistemic state tracking

### 11. Add Scientific Method Examples

**Add concrete examples throughout:**

Example hypothesis testing workflow:
```markdown
**Example: Testing Architecture Hypothesis**

1. **Hypothesis**: "The codebase uses dependency injection pattern"
2. **Experiment**: Search for DI patterns, read core modules
3. **Observation**: Found X uses Y, but Z doesn't
4. **Conclusion**: Partially validated - some components use DI, others don't
5. **Log**: `waft finding log "Partially validated: DI used in X, not in Z" --impact 0.6`
6. **New Hypothesis**: "DI is used for testability in X module"
7. **Iterate**: Test new hypothesis
```

### 12. Update Notes Section

**Enhance notes to emphasize:**
- Scientific method is core to the workflow
- Hypothesis testing happens continuously
- Empirica is strongly encouraged (warn if not used)
- Every assumption should be tested
- Observations should be logged immediately

## Files to Modify

1. `.cursor/commands/engineering.md` - Main file to enhance
   - Add scientific method framework section
   - Enhance each phase with hypothesis testing
   - Add comprehensive Empirica integration
   - Add hypothesis testing checklist
   - Add examples throughout

## Implementation Details

### Scientific Method Integration Points

- **Phase 1**: Hypotheses about current state
- **Phase 2**: Hypotheses about codebase structure/behavior
- **Phase 3**: Hypotheses about solution approach
- **Phase 4**: Hypotheses about plan completeness/feasibility
- **Phase 5**: Hypotheses about plan readiness
- **Phase 6**: Hypotheses about implementation correctness

### Empirica Integration Points

- **Session Management**: Create session at start, bootstrap context
- **Finding Logging**: Log validated hypotheses, discoveries
- **Unknown Logging**: Log invalidated hypotheses, gaps
- **Safety Gates**: Use `waft check` before major operations
- **State Assessment**: Use `waft assess` to track epistemic health
- **Goal Management**: Create goals with epistemic scope
- **Preflight/Postflight**: Assess knowledge before/after work

### Hypothesis Testing Workflow

For each hypothesis:
1. Form hypothesis (document in `_pyrite/active/`)
2. Design experiment (specify test method)
3. Execute experiment (run test)
4. Observe results (document findings)
5. Log in Empirica (finding/unknown)
6. Form conclusions (validate/invalidate)
7. Iterate if needed (refine hypothesis)

## Success Criteria

- Every phase includes hypothesis formation and testing
- Empirica usage is strongly emphasized throughout
- Scientific method workflow is clearly explained
- Concrete examples are provided for each phase
- Hypothesis testing checklist is comprehensive
- Empirica integration is detailed and actionable