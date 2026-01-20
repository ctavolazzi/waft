# /critique-and-revise - Critique and Revise Plan

**Critique a plan and automatically revise it based on valid criticisms.**

Combines adversarial critique analysis with automatic plan document revision. Unlike `/respond-to-critique` which fixes code files, this command revises the plan markdown document itself.

**Use when:** Have a plan that needs critique and automatic revision. Want to improve plans based on security analysis, assumption detection, and oversight identification.

---

## Purpose

This command provides:
- **Plan Critique**: Adversarial analysis of plan (like `/critique`)
- **Automatic Revision**: Updates plan markdown based on valid criticisms
- **Evidence-Based**: Validates criticisms before revising
- **Backup & Rollback**: Creates backups and enables rollback
- **Revision Reports**: Documents all changes made

---

## Philosophy

1. **Critique First**: Find all problems before fixing
2. **Validate Criticisms**: Only revise based on valid, evidence-backed criticisms
3. **Preserve Structure**: Maintain plan formatting and organization
4. **Safety First**: Always backup before revision
5. **Traceable**: Document all revisions with evidence

---

## Execution Steps

### Step 1: Locate Plan

**Purpose**: Find the plan to critique and revise

**Actions**:
1. Check for plan path argument: `/critique-and-revise plan:feature_name`
2. Check for file path: `/critique-and-revise file:~/.cursor/plans/plan.plan.md`
3. If no path, find most recent plan in:
   - `~/.cursor/plans/` (user-level plans)
   - `.cursor/plans/` (project-level plans)
4. Load plan markdown content
5. Parse plan structure (sections, todos, frontmatter)

**Output**: Plan content loaded and parsed

---

### Step 2: Generate Critique

**Purpose**: Analyze plan for problems

**Actions**:
1. Use existing critique system (`/critique` logic)
2. Analyze plan for:
   - Security vulnerabilities
   - Unexamined assumptions
   - Overengineering
   - Oversights
   - Missed obviousness
3. Generate critique document (temporary, for analysis)

**Output**: Critique document with criticisms

---

### Step 3: Validate Criticisms

**Purpose**: Determine which criticisms are valid for plan revision

**Actions**:
1. For each criticism, validate against plan content:
   - **VALID**: Issue exists in plan, needs revision
   - **INVALID**: Issue doesn't exist or already addressed
   - **PARTIALLY VALID**: Issue exists but different than described
   - **CANNOT VERIFY**: Need more context
2. Check if plan already addresses the issue
3. Verify criticism applies to plan (not just code)

**Output**: List of valid criticisms for revision

---

### Step 4: Revise Plan

**Purpose**: Update plan markdown based on valid criticisms

**Actions**:
For VALID and PARTIALLY VALID criticisms:

**CRITICAL Issues**:
- Add "Security Considerations" section
- Document security vulnerabilities
- Add security requirements to Implementation
- Add todos for critical security fixes

**HIGH Issues**:
- Add "Error Handling" section
- Add validation requirements
- Document safety measures
- Add error handling todos

**MEDIUM Issues**:
- Add "Assumptions" section
- Document unexamined assumptions
- Add "Testing Strategy" section
- Clarify dependencies

**LOW Issues**:
- Add "Architecture Notes" section
- Note overengineering concerns
- Suggest simplifications

**Revision Strategies**:
- Add missing sections
- Update existing sections with fixes
- Add todos for critical issues
- Document assumptions explicitly
- Add risk mitigations
- Clarify dependencies

**Output**: Revised plan content

---

### Step 5: Create Backup

**Purpose**: Preserve original plan before revision

**Actions**:
1. Create backup directory: `_hidden/.plan_revisions/backups/`
2. Copy original plan to backup with timestamp
3. Store backup metadata in revision history

**Output**: Backup created

---

### Step 6: Save Revised Plan

**Purpose**: Save revised plan

**Actions**:
1. If dry-run mode: Show diff, don't save
2. Otherwise:
   - Update existing plan file, OR
   - Create new file with `_revised` suffix (if specified)
3. Preserve frontmatter and structure
4. Update revision metadata

**Output**: Revised plan saved

---

### Step 7: Generate Revision Report

**Purpose**: Document all revisions made

**Actions**:
1. Create revision report with:
   - Original plan path
   - Revised plan path
   - Criticisms addressed
   - Sections added/modified
   - Todos added
   - Backup location
   - Evidence for each revision
2. Save to `_work_efforts/PLAN_REVISION_YYYY-MM-DD_HHMMSS.md`
3. Display summary in console

**Output**: Revision report generated

---

## Command Options

```
/critique-and-revise                    # Critique and revise most recent plan
/critique-and-revise plan:feature_name  # Critique and revise specific plan
/critique-and-revise file:path/to/plan.plan.md  # Use specific plan file
/critique-and-revise --dry-run          # Show revisions without applying
/critique-and-revise --severity CRITICAL # Only revise CRITICAL issues
/critique-and-revise --rollback         # Rollback last revision
```

---

## Integration

### With Critique System
- Uses `CritiqueParser` for parsing critiques
- Uses `CriticismValidator` for validation
- Reuses critique generation logic from `/critique`

### With Plan System
- Reads plans from `~/.cursor/plans/` or `.cursor/plans/`
- Parses plan markdown structure
- Updates plan using markdown manipulation
- Preserves plan structure and formatting

### With Backup System
- Creates backup before revision: `_hidden/.plan_revisions/backups/`
- Stores revision history: `_hidden/.plan_revisions/history.jsonl`
- Enables rollback: `/critique-and-revise --rollback`

---

## Revision Examples

### Example 1: Security Vulnerability

**Criticism**: "No path validation mentioned in plan"

**Plan Revision**:
```markdown
## Security Considerations

### Path Validation
- Validate all file paths before use
- Reject paths containing `..` (path traversal)
- Ensure paths are within project root
- Use `Path.resolve()` and validate against project root
```

### Example 2: Missing Assumption

**Criticism**: "Assumes Python 3.10+ without version check"

**Plan Revision**:
```markdown
## Assumptions

- Python 3.10+ is available
  - **Mitigation**: Add version check at startup
  - **Fallback**: Provide clear error message if version insufficient
```

### Example 3: Missing Error Handling

**Criticism**: "No error handling strategy mentioned"

**Plan Revision**:
```markdown
## Error Handling

- File I/O: Wrap in try/except, handle PermissionError, IOError
- Network: Handle connection errors, timeouts
- Validation: Provide clear error messages for invalid input
- Logging: Log errors with context for debugging
```

---

## Output Format

### Console Output

```
🔍 Critique and Revise Plan

📋 Plan: feature_documenter_demi-god_80a9480c.plan.md
🔍 Generating critique...
✅ Found 12 criticisms

🔍 Validating criticisms...
✅ Valid: 8
⚠️  Partially Valid: 2
❌ Invalid: 2

📝 Revising plan...
✅ Added: Security Considerations section
✅ Added: Assumptions section
✅ Updated: Implementation section
✅ Added: 3 todos

💾 Backup created: _hidden/.plan_revisions/backups/...
💾 Revised plan saved: ~/.cursor/plans/feature_documenter_demi-god_80a9480c.plan.md
📄 Report: _work_efforts/PLAN_REVISION_2026-01-19_102730.md
```

### Revision Report

```markdown
# Plan Revision Report

**Date**: 2026-01-19 10:27:30
**Original Plan**: feature_documenter_demi-god_80a9480c.plan.md
**Revised Plan**: feature_documenter_demi-god_80a9480c.plan.md
**Backup**: _hidden/.plan_revisions/backups/...

## Summary

**Total Criticisms**: 12
**Valid**: 8 (revised)
**Partially Valid**: 2 (revised with modifications)
**Invalid**: 2 (skipped)

## Revisions Made

### Security Considerations (Added)
- Path validation requirements
- Input sanitization
- Access control

### Assumptions (Added)
- Python 3.10+ requirement
- Filesystem writable assumption

### Implementation (Updated)
- Added error handling requirements
- Added validation steps

### Todos (Added)
- [ ] Add path validation
- [ ] Add version check
- [ ] Add error handling
```

---

## Safety Measures

1. **Backup Before Revision**: Always backup original plan
2. **Dry Run Mode**: Preview revisions without applying
3. **Severity Filtering**: Only revise specified severity levels
4. **Rollback Support**: Ability to undo revisions
5. **Revision History**: Track all revisions for audit

---

## When to Use

**Use `/critique-and-revise` when**:
- ✅ Have a plan that needs improvement
- ✅ Want automatic plan revision based on critique
- ✅ Need to add missing sections (Security, Assumptions, etc.)
- ✅ Want evidence-based plan improvements
- ✅ Need to document assumptions and risks

**Don't use `/critique-and-revise` when**:
- ❌ Haven't created a plan yet (create plan first)
- ❌ Want manual control over all revisions (use `/critique` + manual edit)
- ❌ Plan is already perfect (no need for critique)

---

## Related Commands

- **`/critique`**: Generate critique without revision
- **`/respond-to-critique`**: Fix code files based on critique
- **`/examine-plan`**: Deep adversarial examination
- **`/plan-evolve`**: Create comprehensive plan

---

**This command critiques plans and automatically revises them based on valid, evidence-backed criticisms - improving plans systematically.**

---

End Command ---
