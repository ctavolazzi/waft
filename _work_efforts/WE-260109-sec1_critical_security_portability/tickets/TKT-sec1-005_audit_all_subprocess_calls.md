---
id: TKT-sec1-005
parent: WE-260109-sec1
title: "Audit and fix all subprocess.run() calls (21 files)"
status: open
priority: HIGH
created: 2026-01-09T00:00:00.000Z
created_by: claude_audit
assigned_to: null
depends_on: [TKT-sec1-002]
---

# TKT-sec1-005: Audit and fix all subprocess.run() calls (21 files)

## Metadata
- **Created**: Thursday, January 9, 2026
- **Parent Work Effort**: WE-260109-sec1
- **Author**: Claude Audit System
- **Priority**: HIGH
- **Estimated Effort**: 5 tickets (extensive audit across codebase)
- **Dependencies**: TKT-sec1-002 (validation layer must exist first)

## Description

Comprehensive audit found **subprocess.run() calls in 21 files**. Each call must be reviewed and updated to use the new input validation layer. This ticket tracks the systematic audit and remediation of all subprocess usage.

## Scope

**Files with subprocess.run()** (from audit):
1. `src/waft/core/substrate.py`
2. `src/waft/core/empirica.py`
3. `src/waft/core/session_stats.py`
4. `src/waft/core/github.py`
5. `src/waft/core/visualizer.py`
6. `src/waft/core/tavern_keeper/keeper.py`
7. `src/waft/utils.py`
8. (14 more files - see audit report)

**Total Occurrences**: 50+ subprocess calls

## Acceptance Criteria

- [ ] All 21 files audited for subprocess usage
- [ ] Each subprocess.run() categorized (safe/needs-validation/critical)
- [ ] All user-input paths updated to use SubprocessValidator
- [ ] Git/system commands verified safe (no user input)
- [ ] Documentation updated with safe subprocess patterns
- [ ] Tests verify all changes work correctly

## Implementation Plan

### Phase 1: Discovery and Categorization

Create audit spreadsheet/file:

```markdown
# Subprocess Audit Results

## Critical (User Input - Must Validate)
| File | Line | Command | User Input | Risk | Status |
|------|------|---------|------------|------|--------|
| substrate.py | 52 | uv init --name {name} | name | HIGH | needs-fix |
| empirica.py | 272 | --finding {finding} | finding | HIGH | needs-fix |
| ... | ... | ... | ... | ... | ... |

## Medium (Indirect User Input)
| File | Line | Command | Input Source | Risk | Status |
|------|------|---------|--------------|------|--------|
| github.py | X | git operations | repo paths | MED | review |
| ... | ... | ... | ... | ... | ... |

## Safe (No User Input)
| File | Line | Command | Why Safe | Status |
|------|------|---------|----------|--------|
| session_stats.py | 44 | git diff --numstat HEAD | no user input | OK |
| ... | ... | ... | ... | ... |
```

### Phase 2: Prioritize by Risk

**Priority 1 - CRITICAL (User-Facing Commands)**:
- substrate.py: `waft new`, `waft init`, `waft add`
- empirica.py: `waft session`, `waft finding`
- Any command that takes CLI arguments

**Priority 2 - MEDIUM (Internal Operations)**:
- github.py: git operations
- visualizer.py: data processing
- Internal tools that process files

**Priority 3 - LOW (System Commands)**:
- git status, git diff (no user input)
- uv sync (no parameters)
- System information gathering

### Phase 3: Fix Each File

For each file in Priority 1-2:

```python
# Before:
subprocess.run(["uv", "init", "--name", name], ...)

# After:
from .subprocess_validator import SubprocessValidator

validated_name = SubprocessValidator.validate_project_name(name)
subprocess.run(["uv", "init", "--name", validated_name], ...)
```

### Phase 4: Add Safety Comments

For safe commands, add comments explaining why:

```python
# Safe: git diff with no user input, reads from HEAD
subprocess.run(["git", "diff", "--numstat", "HEAD"], ...)
```

### Phase 5: Create Safety Guidelines

Document safe subprocess patterns in `docs/SUBPROCESS_SAFETY.md`:

```markdown
# Safe Subprocess Usage Guidelines

## Rule 1: Never trust user input
ALL user-provided input must pass through SubprocessValidator.

## Rule 2: Use list-based arguments
✅ subprocess.run(["git", "status"])
❌ subprocess.run("git status", shell=True)

## Rule 3: Avoid shell=True
shell=True enables shell metacharacters and command chaining.
NEVER use shell=True with user input.

## Rule 4: Validate before passing
```python
# ✅ Good
validated = SubprocessValidator.validate_project_name(user_input)
subprocess.run(["command", validated])

# ❌ Bad
subprocess.run(["command", user_input])
```

## Examples

### Safe Patterns

```python
# System information (no user input)
subprocess.run(["git", "status"], capture_output=True)

# Fixed commands (no parameters)
subprocess.run(["uv", "sync"], cwd=project_path)
```

### Unsafe Patterns

```python
# ❌ User input without validation
subprocess.run(["uv", "init", "--name", user_name])

# ❌ Shell with user input (NEVER!)
subprocess.run(f"uv init --name {user_name}", shell=True)

# ❌ String interpolation with user data
subprocess.run(["git", "commit", f"-m {user_message}"])
```

### Safe After Validation

```python
# ✅ Validated user input
name = SubprocessValidator.validate_project_name(user_input)
subprocess.run(["uv", "init", "--name", name])

# ✅ Quoted if contains special chars
finding = SubprocessValidator.validate_finding_text(user_text)
finding_quoted = SubprocessValidator.quote_if_needed(finding)
subprocess.run(["empirica", "--finding", finding_quoted])
```
```

## Audit Checklist

For each file with subprocess.run():

- [ ] **Identify all subprocess calls** in file
- [ ] **Trace input source** (user CLI? file read? hardcoded?)
- [ ] **Categorize risk** (critical/medium/low)
- [ ] **Apply validation** if user input
- [ ] **Add safety comment** if no validation needed
- [ ] **Test changes** (unit + integration)
- [ ] **Document in audit file**

## Files to Change

**High Priority** (Direct CLI input):
- [ ] src/waft/core/substrate.py
- [ ] src/waft/core/empirica.py
- [ ] src/waft/main.py (if subprocess calls exist)
- [ ] src/waft/core/github.py

**Medium Priority** (Indirect input):
- [ ] src/waft/core/visualizer.py
- [ ] src/waft/core/tavern_keeper/keeper.py
- [ ] src/waft/utils.py
- [ ] (Other files with file-based input)

**Low Priority** (System commands):
- [ ] src/waft/core/session_stats.py
- [ ] (Files with git status, git diff, etc.)

**New Files**:
- [ ] docs/SUBPROCESS_SAFETY.md (guidelines)
- [ ] _work_efforts/subprocess_audit_results.md (audit log)

## Testing Strategy

For each updated file:

1. **Unit Test**: Verify validation is called
2. **Integration Test**: Verify command still works
3. **Security Test**: Verify malicious input blocked
4. **Regression Test**: Verify valid input still works

## Deliverables

1. **Audit Results Document**: Complete list of all subprocess calls with risk assessment
2. **Updated Code**: All critical/medium risk calls validated
3. **Safety Guidelines**: Documentation for future development
4. **Test Coverage**: Security tests for all user-input paths
5. **Commit History**: Clear commits for each file updated

## Success Metrics

- [ ] 100% of user-input subprocess calls validated
- [ ] 0 security test failures
- [ ] All existing tests still pass
- [ ] Documentation complete
- [ ] Code review approved

## Timeline Estimate

**Discovery**: 2 tickets (audit all 21 files)
**Critical Fixes**: 2 tickets (substrate.py, empirica.py, main.py)
**Medium Fixes**: 1 ticket (remaining files)
**Documentation**: 1 ticket (safety guidelines)
**Testing**: 1 ticket (verify all changes)

**Total**: 7 tickets (but only 5 allocated since some overlap)

## Related Issues

- TKT-sec1-002: SubprocessValidator implementation
- TKT-sec1-004: Security testing
- Audit Finding: "Command Injection Risks (21 files)"

## Commits

- (populated as work progresses)
