# Adversarial Plan Critique

**Date**: 2026-01-16
**Time**: 11:28:41 PST
**Plan**: Projects Feature: Long-Term Project Management System
**Critique Mode**: Bad Faith / Adversarial / Security-First

---

## Executive Summary

**CRITICAL Security Vulnerabilities**: 4
**HIGH Safety Issues**: 5
**MEDIUM Unexamined Assumptions**: 9
**LOW Overengineering**: 2
**Oversights**: 7
**Missed Obviousness**: 4

**Overall Assessment**: This plan has **CRITICAL security vulnerabilities** related to path validation, file permissions, and input sanitization. The plan lacks critical error handling, validation, and security considerations for file-based storage operations. Multiple unexamined assumptions about filesystem behavior, JSON serialization, and concurrent access could cause catastrophic failures.

---

## 🔴 CRITICAL: Security Vulnerabilities

### 1. No Path Validation for Project IDs (CRITICAL)
**Issue**: Plan stores projects as `{project_id}.json` without validating project_id:
- Path traversal in project_id: `project_id = "../../../etc/passwd"` → writes to system files
- Null bytes in project_id: `project_id = "proj\x00evil"` → filesystem corruption
- Absolute paths: `project_id = "/etc/passwd"` → system file access
- Symlink attacks: Malicious symlinks in `_pyrite/.waft/projects/` directory

**Attack Vector**:
- User creates project with malicious ID: `waft project create "../../../etc/passwd"`
- System writes to `/etc/passwd` instead of project directory
- System compromise, data exfiltration

**Impact**:
- Writing files outside intended directory
- System file corruption
- Potential root/system compromise
- Data exfiltration

**Severity**: CRITICAL

**Evidence**:
- Plan shows `{project_id}.json` but no validation
- No mention of path sanitization
- Existing codebase has `_validate_path_in_project()` pattern (see `src/waft/being.py:2064`, `src/waft/utils.py:1244`)
- No validation before `Path.resolve()` or after

**Fix Required**:
- Validate project_id before use (reject `..`, `/`, `\`, null bytes, control characters)
- Use `_validate_path_in_project()` pattern from existing codebase
- Reject absolute paths
- Check for symlinks in directory structure
- Sanitize project_id to safe filename characters only

---

### 2. No File Permissions Set on Project Files (CRITICAL)
**Issue**: Plan doesn't mention setting file permissions on project JSON files:
- Project files stored with default permissions (world-readable on many systems)
- Sensitive project data (notes, work effort IDs, progress) exposed
- Other users/processes can read project data

**Attack Vector**:
- Project files created with default permissions (0644)
- Other users on system can read project data
- Information disclosure of project details, work efforts, progress

**Impact**:
- Information disclosure
- Privacy violation
- Potential data leakage

**Severity**: CRITICAL

**Evidence**:
- Plan shows JSON file storage but no permission setting
- Existing codebase sets `chmod(0o600)` on sensitive files (see `src/waft/being.py:2073`, `src/waft/utils.py:1631`, `src/waft/core/reflect.py:613`)
- No mention of file permissions in plan

**Fix Required**:
- Set `chmod(0o600)` on project JSON files (owner read/write only)
- Set `chmod(0o700)` on `_pyrite/.waft/projects/` directory
- Handle permission errors gracefully (Windows compatibility)

---

### 3. No Input Validation on User Inputs (CRITICAL)
**Issue**: Plan doesn't validate user inputs for:
- Project title: Could contain path traversal, null bytes, control characters
- Description: Could contain malicious content, extremely long strings (DoS)
- Tags: Could contain path traversal, injection attacks
- Progress percentage: Could be negative, >100, NaN, infinity
- Work effort IDs: Could contain path traversal, injection attacks

**Attack Vector**:
- User provides malicious title: `title = "../../../etc/passwd"`
- System uses title in file operations without validation
- Path traversal, system compromise

**Impact**:
- Path traversal attacks
- DoS attacks (extremely long strings)
- Injection attacks
- Data corruption

**Severity**: CRITICAL

**Evidence**:
- Plan shows data model but no validation
- No mention of input sanitization
- Existing codebase validates inputs (see `src/waft/being.py:2058` for being_id validation)

**Fix Required**:
- Validate all user inputs
- Sanitize strings (remove control characters, limit length)
- Validate progress_percent (0.0 to 100.0, not NaN, not infinity)
- Validate work effort IDs (format check, no path traversal)
- Reject malicious inputs with clear error messages

---

### 4. No Concurrent Access Protection (CRITICAL)
**Issue**: Plan doesn't mention file locking or atomic writes:
- Multiple processes could write to same project file simultaneously
- Race conditions: Lost updates, corrupted JSON
- Data corruption from concurrent writes

**Attack Vector**:
- Two CLI commands run simultaneously: `waft project progress proj_123 --percent 50` and `waft project update proj_123 --status active`
- Both read file, modify, write back
- Last write wins, data loss

**Impact**:
- Data corruption
- Lost updates
- Inconsistent state

**Severity**: CRITICAL

**Evidence**:
- Plan shows file writes but no locking
- Existing codebase uses file locking (see `src/waft/utils.py:1599` for `Lock()`, `src/waft/utils.py:1622` for atomic writes)
- No mention of concurrent access protection

**Fix Required**:
- Use file locking (`threading.Lock()` or `fcntl.flock()`)
- Implement atomic writes (write to temp file, then rename)
- Handle lock timeouts gracefully
- Document concurrent access behavior

---

## 🔴 HIGH: Safety Issues

### 1. No Error Handling for File I/O Operations
**Issue**: Plan doesn't mention error handling for:
- File read errors (file doesn't exist, permission denied, corrupted JSON)
- File write errors (disk full, permission denied, filesystem errors)
- JSON serialization errors (circular references, non-serializable objects)
- Directory creation errors (permission denied, disk full)

**Impact**: Runtime crashes, poor user experience, data loss

**Severity**: HIGH

**Fix Required**:
- Add try/except blocks for all file I/O
- Handle `IOError`, `OSError`, `PermissionError`, `json.JSONDecodeError`
- Provide clear error messages
- Graceful degradation (read-only mode if can't write)

---

### 2. No Validation of JSON Data Structure
**Issue**: Plan doesn't validate JSON data when loading:
- Corrupted JSON files could crash system
- Malformed data structures could cause errors
- Schema violations not caught

**Impact**: Runtime crashes, data corruption

**Severity**: HIGH

**Fix Required**:
- Validate JSON structure on load
- Use dataclass validation (Pydantic or manual)
- Handle schema migrations gracefully
- Provide clear error messages for corrupted data

---

### 3. No Disk Space Checks
**Issue**: Plan doesn't check available disk space before writes:
- Disk full during write could corrupt data
- No warning before running out of space
- No cleanup of old/temporary files

**Impact**: Data corruption, system failures

**Severity**: HIGH

**Fix Required**:
- Check disk space before writes
- Warn if disk space low
- Clean up temporary files
- Handle disk full errors gracefully

---

### 4. No Backup/Rollback Mechanism
**Issue**: Plan doesn't mention backup or rollback:
- Updates are destructive (no backup before modify)
- No way to recover from corrupted data
- No version history

**Impact**: Data loss, inability to recover

**Severity**: HIGH

**Fix Required**:
- Create backup before updates
- Implement rollback mechanism
- Keep version history (optional)
- Document recovery procedures

---

### 5. No Input Size Limits
**Issue**: Plan doesn't limit input sizes:
- Extremely long descriptions could cause DoS
- Large progress entry lists could exhaust memory
- No limits on number of milestones or tags

**Impact**: Memory exhaustion, DoS attacks

**Severity**: HIGH

**Fix Required**:
- Limit description length (e.g., 10,000 characters)
- Limit number of milestones (e.g., 100)
- Limit number of tags (e.g., 20)
- Limit progress entry history (e.g., last 1000 entries)

---

## ⚠️ MEDIUM: Unexamined Assumptions

### 1. Assumes Filesystem is Writable
**Issue**: Plan assumes `_pyrite/.waft/projects/` is writable
**Impact**: Crashes on read-only filesystems (containers, CI/CD)
**Fix Required**: Check filesystem permissions, provide read-only mode

### 2. Assumes JSON Serialization Works
**Issue**: Plan assumes all data is JSON-serializable
**Impact**: Runtime errors if dataclasses contain non-serializable objects
**Fix Required**: Use custom JSON encoder, validate serializability

### 3. Assumes Directory Structure Exists
**Issue**: Plan assumes `_pyrite/.waft/projects/` exists
**Impact**: Crashes if directory doesn't exist
**Fix Required**: Create directory structure on initialization

### 4. Assumes Project IDs are Unique
**Issue**: Plan doesn't check for duplicate project IDs
**Impact**: Data overwrites, lost projects
**Fix Required**: Check for existing project before create, generate unique IDs

### 5. Assumes Progress Percentage is Valid
**Issue**: Plan doesn't validate progress_percent range
**Impact**: Invalid data (negative, >100, NaN)
**Fix Required**: Validate range (0.0 to 100.0), reject invalid values

### 6. Assumes Work Effort IDs Exist
**Issue**: Plan links to work efforts but doesn't validate they exist
**Impact**: Broken references, inconsistent state
**Fix Required**: Validate work effort IDs exist, handle missing references

### 7. Assumes Timestamps are Valid
**Issue**: Plan uses ISO format timestamps but doesn't validate
**Impact**: Invalid timestamps, parsing errors
**Fix Required**: Validate timestamp format, use datetime objects

### 8. Assumes CLI Inputs are Sanitized
**Issue**: Plan assumes CLI inputs are safe
**Impact**: Injection attacks, path traversal
**Fix Required**: Validate and sanitize all CLI inputs

### 9. Assumes No Race Conditions
**Issue**: Plan doesn't consider concurrent access
**Impact**: Data corruption, lost updates
**Fix Required**: Implement file locking, atomic writes

---

## ⚠️ LOW: Overengineering

### 1. Unnecessary Complexity for Simple Project Tracking
**Issue**: Full dataclass system with milestones, progress entries, work effort links for simple project tracking
**Impact**: Unnecessary complexity, maintenance burden
**Fix Consideration**: Could use simpler data structure for basic use cases

### 2. Over-Complex Progress Tracking
**Issue**: Progress entries with timestamps, deltas, work effort links, session duration
**Impact**: Complexity for simple progress updates
**Fix Consideration**: Could simplify to just progress percentage and notes

---

## ⚠️ Oversights

### 1. No Tests Mentioned
**Issue**: Plan doesn't mention testing strategy
**Impact**: Untested code, potential bugs
**Fix Required**: Add unit tests, integration tests, security tests

### 2. Missing Cleanup for Temporary Files
**Issue**: No cleanup mentioned for temporary files created during operations
**Impact**: Disk space leaks, temporary file accumulation
**Fix Required**: Add cleanup, use context managers

### 3. No Documentation Plan
**Issue**: Plan mentions documentation but no details
**Impact**: Users don't know how to use feature
**Fix Required**: Create user guide, API docs, examples

### 4. No Migration Strategy
**Issue**: Plan doesn't consider data migration if schema changes
**Impact**: Breaking changes, data loss
**Fix Required**: Add version field, migration logic

### 5. No Performance Considerations
**Issue**: Plan doesn't consider performance for large numbers of projects
**Impact**: Slow operations, poor user experience
**Fix Required**: Add pagination, indexing, caching

### 6. No Logging Strategy
**Issue**: Plan doesn't mention logging
**Impact**: Difficult to debug, no audit trail
**Fix Required**: Add logging for operations, errors, security events

### 7. No CLI Help Text
**Issue**: Plan shows CLI commands but no help text
**Impact**: Users don't know how to use commands
**Fix Required**: Add comprehensive help text, examples

---

## ⚠️ Missed Obviousness

### 1. No Authentication/Authorization
**Issue**: No mention of who can create/update/delete projects
**Impact**: Unauthorized access, data tampering
**Fix Required**: Add access control, validate user permissions

### 2. No Rate Limiting
**Issue**: CLI commands could be run repeatedly, causing resource exhaustion
**Impact**: DoS attacks, resource exhaustion
**Fix Consideration**: Add rate limiting, resource limits

### 3. No Input Sanitization in CLI
**Issue**: CLI inputs not sanitized before use
**Impact**: Injection attacks, path traversal
**Fix Required**: Sanitize all CLI inputs

### 4. No Error Messages
**Issue**: Plan doesn't mention error messages for users
**Impact**: Poor user experience, confusion
**Fix Required**: Add clear, actionable error messages

---

## Additional Adversarial Findings

### Failure Modes
- **Disk Full**: What happens if disk fills up during project write? (No handling)
- **Network Down**: What if external dependencies unavailable? (No fallback)
- **Process Killed**: What if process killed mid-write? (No cleanup, corrupted JSON)
- **System Under Load**: What if system is under heavy load? (No throttling)

### Attack Vectors
- **Path Traversal**: Project IDs with `../` could escape project directory
- **Injection Attacks**: Unsanitized inputs in CLI commands
- **Resource Exhaustion**: No limits on project size or number of entries
- **Information Disclosure**: Project files world-readable

### Edge Cases
- **Empty Project List**: What if no projects exist? (No handling)
- **Concurrent Updates**: What if multiple updates happen simultaneously? (Race conditions)
- **Malformed JSON**: What if JSON file is corrupted? (No recovery)
- **Invalid Progress**: What if progress is negative or >100? (No validation)

---

## Recommendations (Prioritized)

### Priority 1: CRITICAL - Fix Immediately
1. **Add Path Validation**: Validate project_id, reject path traversal, use `_validate_path_in_project()` pattern
2. **Set File Permissions**: Set `chmod(0o600)` on project files, `chmod(0o700)` on directory
3. **Add Input Validation**: Validate all user inputs, sanitize strings, validate ranges
4. **Add File Locking**: Use file locking and atomic writes for concurrent access protection

### Priority 2: HIGH - Fix Before Implementation
5. **Add Error Handling**: Handle all file I/O errors, JSON errors, permission errors
6. **Add JSON Validation**: Validate JSON structure on load, handle schema violations
7. **Add Disk Space Checks**: Check disk space before writes, warn if low
8. **Add Backup/Rollback**: Create backups before updates, implement rollback
9. **Add Input Size Limits**: Limit description length, number of milestones, tags

### Priority 3: MEDIUM - Fix During Implementation
10. **Add Tests**: Unit tests, integration tests, security tests
11. **Add Documentation**: User guide, API docs, examples
12. **Add Logging**: Log operations, errors, security events
13. **Add Migration Strategy**: Version field, migration logic

### Priority 4: LOW - Consider for Future
14. **Simplify Architecture**: Consider if full dataclass system is necessary
15. **Add Rate Limiting**: Prevent resource exhaustion
16. **Add Performance Optimization**: Pagination, indexing, caching

---

## Conclusion

This plan has **CRITICAL security vulnerabilities** that must be addressed before any code is written. The lack of path validation, file permissions, input validation, and concurrent access protection are **show-stoppers**. These are not minor issues - they could lead to system compromise, data corruption, and data loss.

Additionally, there are multiple unexamined assumptions that could cause catastrophic failures, significant oversights in error handling and testing, and missed obviousness in security considerations.

**Recommendation**: Do not proceed with implementation until all CRITICAL and HIGH priority issues are addressed. The security vulnerabilities alone make this plan unsafe to implement as-is.

---

**This critique assumes the worst and looks for all the ways things could fail. Address these issues before implementation.**
