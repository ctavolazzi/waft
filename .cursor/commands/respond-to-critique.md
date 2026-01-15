# Respond to Critique

**Automatically validate criticisms from critique documents and apply appropriate fixes.**

Reads critique documents, validates each criticism with evidence, determines validity, and applies fixes automatically for CRITICAL/HIGH issues or suggests fixes for MEDIUM/LOW issues.

**Use when:** After running `/critique` on a plan, want to automatically validate and fix the issues found. Need evidence-based validation of criticisms before making changes.

---

## Purpose

This command provides:
- **Critique Parsing**: Extracts structured data from critique markdown documents
- **Evidence-Based Validation**: Validates each criticism using code analysis, file checks, and tests
- **Automatic Fixes**: Applies fixes for CRITICAL/HIGH validated issues
- **Fix Suggestions**: Suggests fixes for MEDIUM/LOW issues
- **Comprehensive Reports**: Generates detailed response reports with evidence
- **Safety Measures**: Backups, dry-run mode, rollback capability

---

## Philosophy

1. **Evidence Over Assumptions**: Prove or disprove criticisms with evidence
2. **Safety First**: Backup before fixes, verify after fixes, enable rollback
3. **Automatic When Safe**: Auto-fix CRITICAL/HIGH issues, suggest MEDIUM/LOW
4. **Traceable**: Every validation and fix has evidence and documentation
5. **Reversible**: All fixes can be rolled back if needed

---

## Execution Steps

### Step 1: Locate Critique Document
**Purpose**: Find the critique to respond to

**Actions**:
1. Check for path argument: `/respond-to-critique path:_work_efforts/CRITIQUE_*.md`
2. If no path, find most recent critique in `_work_efforts/CRITIQUE_*.md`
3. Parse critique markdown to extract structured data
4. Display critique summary (total criticisms by severity)

**Output**: Critique document loaded and parsed

---

### Step 2: Extract Criticisms
**Purpose**: Extract individual criticisms with severity levels

**Actions**:
1. Parse critique sections:
   - 🔴 CRITICAL Security Vulnerabilities
   - 🔴 HIGH Safety Issues
   - ⚠️ MEDIUM Unexamined Assumptions
   - ⚠️ LOW Overengineering
   - Oversights
   - Missed Obviousness
2. Extract for each criticism:
   - Issue description
   - Severity level
   - Attack vector/impact
   - Recommended fix
   - Code location (if specified)
   - Fix code (if provided)

**Output**: List of structured criticisms

---

### Step 3: Validate Each Criticism
**Purpose**: Collect evidence to prove or disprove each criticism

**Actions**:
For each criticism:
1. **Code Analysis**:
   - Read relevant source files
   - Check if vulnerability exists
   - Verify current implementation
   - Test edge cases
2. **File System Checks**:
   - Check file permissions
   - Verify path validation
   - Test path traversal scenarios
   - Check for sensitive files
3. **Security Testing**:
   - Test attack vectors
   - Verify fixes work
   - Check for regressions
4. **Evidence Collection**:
   - Gather code snippets
   - File system state
   - Test results
   - Documentation references

**Output**: Validation result for each criticism (VALID, INVALID, PARTIALLY VALID, CANNOT VERIFY)

---

### Step 4: Categorize Findings
**Purpose**: Determine validity status for each criticism

**Actions**:
For each criticism:
- ✅ **VALID**: Evidence confirms the issue exists
- ❌ **INVALID**: Evidence disproves the issue
- ⚠️ **PARTIALLY VALID**: Issue exists but different than described
- ❓ **CANNOT VERIFY**: Insufficient evidence to determine

**Output**: Categorized validation results

---

### Step 5: Apply Fixes
**Purpose**: Fix validated issues based on severity

**Actions**:
For VALID and PARTIALLY VALID criticisms:

**CRITICAL Issues** (automatic fix):
- Create backup of files to be modified
- Apply security fixes immediately
- Set file permissions
- Add path validation
- Fix command injection vulnerabilities
- Add access control
- Verify fix works

**HIGH Issues** (automatic fix with confirmation):
- Create backup
- Add error handling
- Implement validation
- Add migration rollback
- Fix concurrent access issues
- Verify fix works

**MEDIUM Issues** (suggest fixes):
- Update plan with fixes
- Create TODO items
- Document required changes
- Suggest implementation approach

**LOW Issues** (document only):
- Note in response report
- Suggest for future consideration

**Output**: Fix results (applied, suggested, documented)

---

### Step 6: Generate Response Report
**Purpose**: Create comprehensive report of validation and fixes

**Actions**:
1. Create response report with:
   - Executive summary (total criticisms, validation results, fixes applied)
   - CRITICAL issues (fixed)
   - HIGH issues (fixed)
   - MEDIUM issues (suggested)
   - LOW issues (documented)
   - Invalid criticisms (disproven with evidence)
   - Partially valid (fixed with modifications)
   - Cannot verify (manual review required)
   - Files modified
   - Tests added
   - Next steps
2. Save to `_work_efforts/RESPONSE_YYYY-MM-DD_HHMMSS.md`
3. Display summary in console

**Output**: Comprehensive response report

---

## Command Options

```bash
/respond-to-critique                    # Use most recent critique
/respond-to-critique path:...            # Use specific critique file
/respond-to-critique --dry-run           # Show what would be fixed (no changes)
/respond-to-critique --auto-fix          # Auto-fix without confirmation prompts
/respond-to-critique --severity CRITICAL # Only fix CRITICAL issues
/respond-to-critique --validate-only     # Only validate, don't apply fixes
/respond-to-critique --rollback          # Rollback last set of fixes
```

---

## Integration with Other Commands

- **`/critique`**: Generates critiques that this command responds to
- **`/check-assumptions`**: Uses assumption validation for unexamined assumptions
- **`/verify`**: Uses verification methods for evidence collection
- **`/reflect`**: Logs reflection on fixes applied

---

## Safety Measures

### Before Applying Fixes
1. **Backup**: Create backup of all files to be modified in `_hidden/.critique_fix_backups/`
2. **Dry Run**: Use `--dry-run` to preview changes without applying
3. **Confirmation**: Ask for confirmation on CRITICAL fixes (unless `--auto-fix`)
4. **Testing**: Run tests after fixes to verify no regressions

### Fix Validation
1. **Verify Fix**: Test that fix actually resolves the issue
2. **No Regressions**: Ensure fix doesn't break existing functionality
3. **Documentation**: Update docs if fix changes behavior

### Rollback
1. **Backup Location**: Backups stored in `_hidden/.critique_fix_backups/YYYY-MM-DD_HHMMSS/`
2. **Rollback Command**: `/respond-to-critique --rollback` to undo last fixes
3. **Fix Log**: All fixes logged in `_hidden/.critique_fix_backups/fix_log.jsonl`

---

## Response Report Format

The response report includes:

```markdown
# Critique Response Report

**Date**: 2026-01-14
**Critique**: CRITIQUE_2026-01-14_103507_ai_journal_overhaul.md
**Status**: Complete

## Executive Summary

**Total Criticisms**: 29
**✅ Valid**: 18 (fixed automatically)
**❌ Invalid**: 3 (disproven with evidence)
**⚠️ Partially Valid**: 5 (fixed with modifications)
**❓ Cannot Verify**: 3 (requires manual review)

**Fixes Applied**: 23
**Fixes Suggested**: 5
**Manual Review Required**: 3

## CRITICAL Issues (Fixed)

### 1. Path Traversal Vulnerability
**Status**: ✅ VALID - FIXED
**Evidence**: Code analysis confirmed missing path validation
**Fix Applied**: Added `_validate_path_in_project()` method
**Files Modified**: `src/waft/core/reflect.py`
**Verification**: Path traversal test passed

[... more sections ...]
```

---

## Usage Examples

### Basic Usage
```
/respond-to-critique
```
Uses most recent critique, validates all criticisms, applies fixes for CRITICAL/HIGH issues.

### Specific Critique
```
/respond-to-critique path:_work_efforts/CRITIQUE_2026-01-14_103507.md
```
Responds to specific critique file.

### Dry Run
```
/respond-to-critique --dry-run
```
Shows what would be fixed without making changes.

### Validate Only
```
/respond-to-critique --validate-only
```
Only validates criticisms, doesn't apply fixes.

### Rollback
```
/respond-to-critique --rollback
```
Undoes the last set of fixes applied.

---

## When to Use

**Use `/respond-to-critique` when**:
- ✅ Just ran `/critique` and want to fix issues automatically
- ✅ Need evidence-based validation of criticisms
- ✅ Want to apply security fixes automatically
- ✅ Need comprehensive report of what was fixed and why
- ✅ Want to ensure fixes are reversible

**Don't use `/respond-to-critique` when**:
- ❌ Haven't run `/critique` yet (run critique first)
- ❌ Want manual control over all fixes (use validate-only mode)
- ❌ Fixes require complex refactoring (manual review needed)

---

## Fix Categories

### Security Fixes (CRITICAL)
- File permissions: `chmod(0o600)` on files, `chmod(0o700)` on directories
- Path validation: Add path traversal protection
- Input sanitization: Sanitize user inputs
- Access control: Add authorization checks
- Command injection: Fix `subprocess.run(shell=True)` → use list args

### Safety Fixes (HIGH)
- Error handling: Add try/except blocks
- Input validation: Validate all inputs
- Migration rollback: Add backup/rollback mechanisms
- Concurrent access: Add file locking or atomic writes

### Plan Updates (MEDIUM)
- Assumption documentation: Document assumptions
- Testing strategy: Add test requirements
- Documentation: Add missing docs
- Performance: Add performance considerations

---

**This command automatically validates and fixes issues found in critiques, making security fixes and improvements with evidence-based validation.**
