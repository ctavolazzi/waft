# Audit

**Audit the conversation - analyze quality, completeness, issues, and improvements.**

Analyzes the current conversation for quality, completeness, potential issues, missing information, and provides recommendations for improvement. Perfect for reviewing conversation health, identifying gaps, and ensuring effective communication.

**Use when:** Want to review conversation quality, identify issues, check for missing information, or get recommendations for improvement.

---

## Purpose

This command provides:
- **Quality Analysis**: Assess conversation clarity, coherence, and effectiveness
- **Completeness Check**: Identify missing information or unclear requests
- **Issue Detection**: Find potential problems, inconsistencies, or misunderstandings
- **Best Practices Review**: Check adherence to coding standards and best practices
- **Recommendations**: Actionable suggestions for improvement

---

## Philosophy

1. **Objective Analysis**: Unbiased assessment of conversation quality
2. **Actionable Insights**: Specific, actionable recommendations
3. **Comprehensive Review**: Check multiple dimensions of conversation health
4. **Constructive Feedback**: Focus on improvement, not criticism
5. **Context-Aware**: Consider project context and goals

---

## Execution Steps

### Step 1: Conversation Analysis
**Purpose**: Analyze the conversation for quality and completeness

**Actions**:
1. Review entire conversation history
2. Assess clarity of requests and responses
3. Check for missing information or context
4. Identify unclear or ambiguous statements
5. Evaluate coherence and flow
6. Check for inconsistencies or contradictions

**Output**: Structured analysis of conversation quality

---

### Step 2: Issue Detection
**Purpose**: Identify potential problems or issues

**Actions**:
1. Detect misunderstandings or miscommunications
2. Find incomplete or vague requests
3. Identify missing context or assumptions
4. Check for conflicting information
5. Find areas where clarification is needed
6. Detect potential errors or oversights

**Output**: List of identified issues with severity levels

---

### Step 3: Best Practices Review
**Purpose**: Check adherence to standards and best practices

**Actions**:
1. Review coding style adherence
2. Check documentation quality
3. Evaluate test coverage (if applicable)
4. Review error handling
5. Check security considerations
6. Assess maintainability

**Output**: Best practices assessment

---

### Step 4: Recommendations Generation
**Purpose**: Provide actionable recommendations

**Actions**:
1. Generate specific improvement suggestions
2. Prioritize recommendations by impact
3. Provide actionable next steps
4. Suggest clarifications needed
5. Recommend follow-up actions

**Output**: Prioritized list of recommendations

---

### Step 5: Audit Report Generation
**Purpose**: Create comprehensive audit report

**Actions**:
1. Generate markdown document with sections:
   - **Executive Summary**: Overall assessment
   - **Quality Analysis**: Conversation quality metrics
   - **Completeness Check**: Missing information identified
   - **Issues Found**: Problems detected with severity
   - **Best Practices**: Adherence assessment
   - **Recommendations**: Prioritized suggestions
   - **Next Steps**: Actionable follow-ups
2. Save to `_work_efforts/` directory
3. Use timestamped filename: `AUDIT_YYYY-MM-DD_HHMMSS.md`

**Output**: Complete audit report

---

### Step 6: Summary Display
**Purpose**: Show audit summary in console

**Actions**:
1. Display key findings from audit
2. Show issue count and severity
3. Highlight top recommendations
4. Provide file location

**Output**: Console summary

---

## What Gets Audited

### Conversation Quality
- Clarity of communication
- Coherence and flow
- Completeness of information
- Precision of requests
- Response quality

### Information Completeness
- Missing context
- Unclear requirements
- Ambiguous statements
- Assumptions made
- Gaps in understanding

### Issues Detected
- Misunderstandings
- Inconsistencies
- Potential errors
- Missing validations
- Security concerns

### Best Practices
- Code quality
- Documentation
- Testing
- Error handling
- Security

### Recommendations
- Immediate actions
- Improvements needed
- Clarifications required
- Follow-up tasks
- Best practice suggestions

---

## Output Format

### Console Output

```
🔍 Audit: Conversation Analysis

Overall Quality: ⭐⭐⭐⭐ (4/5)
Completeness: ⭐⭐⭐ (3/5)
Issues Found: 2 (1 high, 1 medium)
Recommendations: 5

Key Findings:
- ✅ Clear communication throughout
- ⚠️ Missing context in 2 requests
- ⚠️ 1 potential misunderstanding identified

Top Recommendations:
1. Clarify requirements for feature X
2. Add validation for edge case Y
3. Document decision Z

📄 Audit saved: _work_efforts/AUDIT_2026-01-09_000912.md
```

### Audit Report

The document includes:

```markdown
# Conversation Audit

**Date**: 2026-01-09
**Time**: 00:09:12
**Session Duration**: ~45 minutes

---

## Executive Summary

**Overall Quality**: ⭐⭐⭐⭐ (4/5)
**Completeness**: ⭐⭐⭐ (3/5)
**Issues Found**: 2 (1 high, 1 medium)
**Recommendations**: 5

### Key Findings
- Clear communication throughout conversation
- Missing context in 2 user requests
- 1 potential misunderstanding identified
- Good adherence to coding standards

---

## Quality Analysis

### Communication Quality
- **Clarity**: ⭐⭐⭐⭐ (4/5) - Clear and precise
- **Coherence**: ⭐⭐⭐⭐⭐ (5/5) - Well-structured
- **Completeness**: ⭐⭐⭐ (3/5) - Some gaps identified

### Request Quality
- **Specificity**: ⭐⭐⭐⭐ (4/5) - Generally specific
- **Context**: ⭐⭐⭐ (3/5) - Some missing context
- **Actionability**: ⭐⭐⭐⭐ (4/5) - Clear actions

---

## Completeness Check

### Missing Information
1. **Feature X Requirements**
   - Missing: Specific use case details
   - Impact: Medium
   - Recommendation: Request clarification

2. **Edge Case Y**
   - Missing: Handling for edge case
   - Impact: High
   - Recommendation: Add validation

### Unclear Statements
1. "Create an audit command" - Clarified during conversation
2. "Make it work like recap" - Understood from context

---

## Issues Found

### High Severity
1. **Missing Validation**
   - Issue: No validation for edge case Y
   - Location: Feature X implementation
   - Impact: Potential runtime error
   - Recommendation: Add input validation

### Medium Severity
1. **Incomplete Context**
   - Issue: Missing use case details for Feature X
   - Impact: May implement incorrectly
   - Recommendation: Request clarification

---

## Best Practices Review

### Code Quality
- ✅ Follows coding style guide
- ✅ Proper error handling
- ⚠️ Missing type hints in 2 functions
- ✅ Good documentation

### Security
- ✅ No security issues detected
- ✅ Proper input validation (mostly)
- ⚠️ One edge case needs validation

### Maintainability
- ✅ Clear code structure
- ✅ Good naming conventions
- ✅ Appropriate abstractions

---

## Recommendations

### Priority 1 (Immediate)
1. **Add Validation for Edge Case Y**
   - Action: Add input validation
   - Impact: High - Prevents potential errors
   - Effort: Low

2. **Clarify Feature X Requirements**
   - Action: Request use case details
   - Impact: Medium - Ensures correct implementation
   - Effort: Low

### Priority 2 (Important)
3. **Add Type Hints**
   - Action: Add type hints to 2 functions
   - Impact: Medium - Improves code quality
   - Effort: Low

4. **Document Decision Z**
   - Action: Add decision documentation
   - Impact: Medium - Improves maintainability
   - Effort: Low

### Priority 3 (Nice to Have)
5. **Improve Error Messages**
   - Action: Make error messages more descriptive
   - Impact: Low - Better debugging experience
   - Effort: Medium

---

## Next Steps

1. Address Priority 1 recommendations
2. Request clarification for Feature X
3. Add validation for edge case Y
4. Continue with implementation
5. Review audit findings in next session

---

## Notes

- Conversation was generally clear and productive
- Most issues are minor and easily addressed
- Good adherence to project standards
- Recommendations are actionable and prioritized
```

---

## Use Cases

### 1. Mid-Conversation Review
**Scenario**: Want to check conversation quality mid-session

**Example**:
```
User: "/audit"
```

**Output**: Complete audit with recommendations

---

### 2. Issue Detection
**Scenario**: Suspect there might be misunderstandings or issues

**Example**:
```
User: "/audit"
```

**Output**: Issues identified with severity levels

---

### 3. Quality Check
**Scenario**: Want to ensure conversation is on track

**Example**:
```
User: "/audit"
```

**Output**: Quality metrics and recommendations

---

### 4. Pre-Completion Review
**Scenario**: Before finishing work, audit the conversation

**Example**:
```
User: "/audit"
```

**Output**: Comprehensive review before completion

---

## Integration with Other Commands

- **`/recap`**: Conversation summary (`/audit` is quality analysis)
- **`/checkpoint`**: Status snapshot (`/audit` is conversation health)
- **`/verify`**: Technical verification (`/audit` is communication quality)
- **`/consider`**: Decision support (`/audit` is conversation review)

---

## When to Use

**Use `/audit` when**:
- ✅ Want to review conversation quality
- ✅ Need to identify issues or gaps
- ✅ Want recommendations for improvement
- ✅ Checking for missing information
- ✅ Reviewing before completion
- ✅ Mid-session quality check

**Don't use `/audit` when**:
- ❌ Need quick status (use `/checkpoint`)
- ❌ Need conversation summary (use `/recap`)
- ❌ Need technical verification (use `/verify`)
- ❌ Need decision support (use `/consider`)

---

## Technical Details

### Data Sources

Audit analyzes:
- Current conversation history
- Request clarity and completeness
- Response quality and accuracy
- Code quality (if applicable)
- Documentation quality
- Best practices adherence

### Output Location

- **Default**: `_work_efforts/AUDIT_YYYY-MM-DD_HHMMSS.md`
- **Custom**: Can specify output path if needed

### Format

- **Markdown**: Easy to read and edit
- **Structured**: Clear sections for easy scanning
- **Timestamped**: Unique filename per audit
- **Actionable**: Prioritized recommendations

---

## Example Workflow

```
User: [Works on implementing feature]
User: [Makes requests]
User: "/audit"

AI: [Analyzes conversation]
AI: [Generates audit report]
AI: [Displays summary]

AI: 🔍 Audit Complete
    📄 Saved: _work_efforts/AUDIT_2026-01-09_000912.md
    ⚠️ Issues: 2 found (1 high, 1 medium)
    💡 Recommendations: 5 prioritized
    ⭐ Quality: 4/5

User: [Reviews audit findings]
User: [Addresses recommendations]
```

---

**This command provides objective analysis of conversation quality - perfect for identifying issues, gaps, and opportunities for improvement.**

---

End Command ---
