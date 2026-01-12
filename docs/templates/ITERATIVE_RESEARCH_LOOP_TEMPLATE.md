# Iterative Research Loop Template

**Purpose**: Template for conducting iterative research with hypothesis-driven development, batching, and systematic validation.

**Use Case**: When exploring a feature, system, or concept through multiple iterations with systematic tracking.

---

## Research Session Structure

### Phase 1: Initial Setup

```markdown
# [Research Topic]: Iterative Research Session

**Date**: YYYY-MM-DD
**Time**: HH:MM - HH:MM [TIMEZONE]
**Duration**: ~X minutes
**Status**: 🔄 In Progress / ✅ Complete / ⚠️ Blocked

---

## Research Question

[Clear, testable research question]

**Primary Question**: [What are we trying to understand?]

**Secondary Questions**:
1. [Question 1]
2. [Question 2]
3. [Question 3]

---

## Hypothesis

**H₀ (Null Hypothesis)**: [What we expect NOT to be true]

**H₁ (Alternative Hypothesis)**: [What we expect to be true]

**Rationale**: [Why this hypothesis?]

**Confidence Level**: [0.0 - 1.0] (initial confidence)

---

## Objectives

1. [Objective 1: Specific, measurable]
2. [Objective 2: Specific, measurable]
3. [Objective 3: Specific, measurable]

---

## Initial State

**Baseline Measurements**:
- [Metric 1]: [Value]
- [Metric 2]: [Value]
- [Metric 3]: [Value]

**Current Understanding**:
- [What we know]
- [What we don't know]
- [Assumptions]

**Constraints**:
- [Constraint 1]
- [Constraint 2]
- [Constraint 3]
```

### Phase 2: Iteration Planning

```markdown
## Iteration Plan

### Iteration Strategy

**Approach**: [Single iteration / Batching / Parallel]

**Number of Iterations**: [N]

**Variation Strategy**: [How iterations differ]
- [Variation 1]
- [Variation 2]
- [Variation 3]

### Constraints

**Max Iterations**: [N] (if applicable)
- **Based on**: [Page count / File size / Time / Other]

**Max Pages**: [N] (if applicable)
- **Calculation**: [Formula]

**Max File Size**: [N MB] (if applicable)
- **Calculation**: [Formula]

### Success Criteria

**Must Have**:
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

**Nice to Have**:
- [ ] [Criterion 1]
- [ ] [Criterion 2]

**Failure Conditions**:
- [Condition 1]
- [Condition 2]
```

### Phase 3: Iteration Execution

```markdown
## Iteration Log

### Iteration 1: [Name/Description]

**Date**: YYYY-MM-DD HH:MM
**Duration**: ~X minutes

**Configuration**:
- [Parameter 1]: [Value]
- [Parameter 2]: [Value]
- [Parameter 3]: [Value]

**Actions Taken**:
1. [Action 1]
2. [Action 2]
3. [Action 3]

**Results**:
- [Result 1]: [Value/Observation]
- [Result 2]: [Value/Observation]
- [Result 3]: [Value/Observation]

**Findings**:
- [Finding 1]
- [Finding 2]
- [Finding 3]

**Issues Encountered**:
- [Issue 1]: [Resolution/Status]
- [Issue 2]: [Resolution/Status]

**Next Iteration Adjustments**:
- [Adjustment 1]
- [Adjustment 2]

---

### Iteration 2: [Name/Description]

[Same structure as Iteration 1]

---

### Iteration N: [Name/Description]

[Same structure as Iteration 1]
```

### Phase 4: Batching (If Applicable)

```markdown
## Batch Generation

**Batch Size**: [N] permutations

**Batch Configuration**:
- [Config 1]: [Value]
- [Config 2]: [Value]
- [Config 3]: [Value]

**Variation Strategy**:
- [How permutations vary]

**Constraints Applied**:
- Max Pages: [N]
- Max File Size: [N MB]
- Max Iterations: [N] (calculated)

**Batch Results**:
- Total Permutations Generated: [N]
- Total Items Created: [N]
- Average Metric: [Value]
- PDF Size: [N KB/MB]
- PDF Pages: [N]

**Collation**:
- [ ] All permutations collated
- [ ] Statistics calculated
- [ ] PDF generated
- [ ] HTML generated
- [ ] Auto-open working
```

### Phase 5: Analysis

```markdown
## Analysis

### Data Collected

**Quantitative Metrics**:
| Metric | Iteration 1 | Iteration 2 | ... | Iteration N | Average |
|--------|-------------|-------------|-----|------------|---------|
| [Metric 1] | [Value] | [Value] | ... | [Value] | [Avg] |
| [Metric 2] | [Value] | [Value] | ... | [Value] | [Avg] |
| [Metric 3] | [Value] | [Value] | ... | [Value] | [Avg] |

**Qualitative Observations**:
- [Observation 1]
- [Observation 2]
- [Observation 3]

### Patterns Identified

1. **Pattern 1**: [Description]
   - Evidence: [Evidence]
   - Confidence: [0.0 - 1.0]

2. **Pattern 2**: [Description]
   - Evidence: [Evidence]
   - Confidence: [0.0 - 1.0]

3. **Pattern 3**: [Description]
   - Evidence: [Evidence]
   - Confidence: [0.0 - 1.0]

### Findings

**Finding 1**: [Description]
- **Evidence**: [Evidence]
- **Confidence**: [0.0 - 1.0]
- **Implications**: [What this means]

**Finding 2**: [Description]
- **Evidence**: [Evidence]
- **Confidence**: [0.0 - 1.0]
- **Implications**: [What this means]

**Finding 3**: [Description]
- **Evidence**: [Evidence]
- **Confidence**: [0.0 - 1.0]
- **Implications**: [What this means]
```

### Phase 6: Conclusions

```markdown
## Conclusions

### Hypothesis Evaluation

**H₀ (Null Hypothesis)**: [Status: Accepted / Rejected / Inconclusive]
- **Reasoning**: [Why]

**H₁ (Alternative Hypothesis)**: [Status: Accepted / Rejected / Inconclusive]
- **Reasoning**: [Why]
- **Final Confidence**: [0.0 - 1.0] (updated from initial)

### Answers to Research Questions

**Primary Question**: [Answer]
- **Confidence**: [0.0 - 1.0]
- **Evidence**: [Evidence]

**Secondary Question 1**: [Answer]
- **Confidence**: [0.0 - 1.0]
- **Evidence**: [Evidence]

**Secondary Question 2**: [Answer]
- **Confidence**: [0.0 - 1.0]
- **Evidence**: [Evidence]

### Key Learnings

1. [Learning 1]
2. [Learning 2]
3. [Learning 3]

### Surprises

1. [Unexpected finding 1]
2. [Unexpected finding 2]

### Limitations

1. [Limitation 1]
2. [Limitation 2]
3. [Limitation 3]
```

### Phase 7: Deliverables

```markdown
## Deliverables

### Code/Implementation

- [ ] [File 1]: [Description]
- [ ] [File 2]: [Description]
- [ ] [File 3]: [Description]

### Documentation

- [ ] [Doc 1]: [Description]
- [ ] [Doc 2]: [Description]
- [ ] [Doc 3]: [Description]

### Generated Artifacts

- [ ] [Artifact 1]: [Description, location]
- [ ] [Artifact 2]: [Description, location]
- [ ] [Artifact 3]: [Description, location]

### Test Results

- [ ] [Test 1]: [Status, results]
- [ ] [Test 2]: [Status, results]
- [ ] [Test 3]: [Status, results]
```

### Phase 8: Next Steps

```markdown
## Next Steps

### Immediate Actions

1. [Action 1]: [Priority: High/Medium/Low]
2. [Action 2]: [Priority: High/Medium/Low]
3. [Action 3]: [Priority: High/Medium/Low]

### Future Research

1. [Research Question 1]
   - **Why**: [Reason]
   - **When**: [Timeline]

2. [Research Question 2]
   - **Why**: [Reason]
   - **When**: [Timeline]

### Recommendations

1. [Recommendation 1]
2. [Recommendation 2]
3. [Recommendation 3]
```

---

## Template Usage Guidelines

### When to Use This Template

- ✅ Exploring a new feature or system
- ✅ Testing multiple configurations
- ✅ Validating hypotheses
- ✅ Generating multiple variations
- ✅ Systematic research with iterations

### How to Use

1. **Copy template** to your research folder
2. **Fill in Phase 1** (Initial Setup) before starting
3. **Update Phase 3** (Iteration Log) as you work
4. **Complete Phase 4** (Batching) if applicable
5. **Fill in Phase 5** (Analysis) after iterations
6. **Complete Phase 6** (Conclusions) at the end
7. **Document Phase 7** (Deliverables) as you create them
8. **Plan Phase 8** (Next Steps) for future work

### Customization

**For Batching Research**:
- Emphasize Phase 4 (Batching)
- Include max iterations calculations
- Document variation strategies

**For Hypothesis Testing**:
- Emphasize Phase 1 (Hypothesis) and Phase 6 (Conclusions)
- Include statistical analysis
- Document confidence levels

**For Exploratory Research**:
- Emphasize Phase 3 (Iterations) and Phase 5 (Analysis)
- Include pattern identification
- Document surprises and learnings

---

## Example: Demo Batching Research

See `_work_efforts/FINAL_SUMMARY_2026-01-11_DEMO_BATCHING.md` for a complete example of this template in use.

---

**Template Version**: 1.0
**Last Updated**: 2026-01-11
**Maintained By**: WAFT Research Team
