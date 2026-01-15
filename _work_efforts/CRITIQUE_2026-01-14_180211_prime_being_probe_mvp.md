# Adversarial Plan Critique - Prime Being Probe MVP

**Date**: 2026-01-14
**Time**: 18:02:11 PST
**Plan**: Prime Being Probe MVP
**Critique Mode**: Bad Faith / Adversarial

---

## Executive Summary

**CRITICAL Security Vulnerabilities**: 2
**HIGH Safety Issues**: 3
**MEDIUM Unexamined Assumptions**: 7
**LOW Overengineering**: 2
**Oversights**: 5
**Missed Obviousness**: 3

**Overall Assessment**: This MVP plan has CRITICAL security vulnerabilities related to database probing and path validation. Multiple unexamined assumptions about personality types and database dependencies could cause failures. Several oversights in error handling and testing need addressing.

---

## 🔴 CRITICAL: Security Vulnerabilities

### 1. Database Connection String Injection (CRITICAL)
**Issue**: Plan mentions adding DatabaseProbe but doesn't specify how database connection strings are validated.
**Attack Vector**: If user-provided connection strings are used, SQL injection or connection to malicious databases possible
**Impact**: Data exfiltration, arbitrary database access, potential system compromise
**Severity**: CRITICAL
**Location**: Phase 3 - DatabaseProbe implementation
**Fix Required**: 
- Never accept user-provided connection strings without validation
- Whitelist allowed database types (SQLite only for MVP)
- Validate database file paths are within project directory
- Use parameterized queries if executing SQL
- Never probe databases outside project scope

### 2. Path Traversal in Database File Paths (CRITICAL)
**Issue**: DatabaseProbe will probe SQLite files, but no path validation mentioned
**Attack Vector**: Paths like `../../../etc/passwd` could escape project directory
**Impact**: Reading sensitive system files, potential data exfiltration
**Severity**: CRITICAL
**Location**: Phase 3 - DatabaseProbe.probe() method
**Fix Required**:
- Validate all database file paths
- Reject paths with `..` or absolute paths outside project
- Use `Path.resolve()` and check it's within project root
- Never probe databases outside `_prime_being_data/` or explicitly allowed directories

---

## 🔴 HIGH: Safety Issues

### 1. No Error Handling for Database Operations
**Issue**: Plan doesn't mention error handling for database connection failures, permission errors, or corrupted databases
**Impact**: Crashes on database errors, poor user experience, potential data loss
**Severity**: HIGH
**Location**: Phase 3 - DatabaseProbe implementation
**Fix Required**: 
- Wrap all database operations in try/except blocks
- Handle `sqlite3.OperationalError`, `sqlite3.DatabaseError`
- Handle permission errors gracefully
- Provide clear error messages

### 2. Missing Dependency Validation
**Issue**: Plan mentions "psycopg2/pymysql optional" but doesn't check if they're available before use
**Impact**: Runtime crashes if optional dependencies not installed
**Severity**: HIGH
**Location**: Phase 3 - DatabaseProbe implementation
**Fix Required**:
- Check for database driver availability before use
- Provide clear error messages if driver missing
- Gracefully degrade (SQLite only) if optional drivers unavailable
- Document required vs optional dependencies

### 3. No Input Validation on Hypothesis Predictions
**Issue**: Plan says "add testable predictions" but doesn't validate prediction format or content
**Impact**: Malformed predictions could break hypothesis verification, potential injection if predictions are executed
**Severity**: HIGH
**Location**: Phase 1 - Hypothesis formation
**Fix Required**:
- Validate prediction format (string, max length)
- Sanitize prediction content
- Never execute predictions as code
- Store predictions as data only

---

## ⚠️ MEDIUM: Unexamined Assumptions

### 1. Assumes Personality Types Exist in Being System
**Issue**: Plan lists personality types (`curious_explorer`, `cautious_observer`, etc.) but doesn't verify they exist in Being class
**Impact**: Runtime errors if personality types don't exist
**Severity**: MEDIUM
**Evidence Needed**: Check `src/waft/being.py` for available personality types
**Fix Required**: 
- Verify personality types exist before implementing mappings
- Use existing personality types or document new ones needed
- Add validation in `__init__` to reject invalid personality types

### 2. Assumes Scientific Method Tool Hypothesis Class Supports Verification
**Issue**: Plan says "store verification results in hypothesis objects" but doesn't verify Hypothesis class has verification fields
**Impact**: May need to extend Hypothesis class or create wrapper
**Severity**: MEDIUM
**Evidence Needed**: Check `scientific_method_tool` Hypothesis class structure
**Fix Required**:
- Check Hypothesis class for verification fields
- Extend or wrap if needed
- Document any modifications to Hypothesis class

### 3. Assumes Database Files Exist in Expected Locations
**Issue**: Plan doesn't specify where database files should be located or how to discover them
**Impact**: DatabaseProbe won't know what to probe
**Severity**: MEDIUM
**Fix Required**:
- Define database discovery strategy (scan directories, user-provided paths, etc.)
- Document expected database locations
- Add database discovery to probe target selection

### 4. Assumes SQLite is Always Available
**Issue**: Plan says "sqlite3 built-in" but doesn't verify it's available
**Impact**: Runtime errors if sqlite3 not available (rare but possible)
**Severity**: MEDIUM
**Fix Required**:
- Check for sqlite3 availability at import time
- Provide clear error if not available
- Document Python version requirements (sqlite3 in stdlib since 2.5)

### 5. Assumes Probe Results Have Consistent Structure
**Issue**: Plan says "analyze probe types, targets, and results" but doesn't verify ProbeResult structure is consistent
**Impact**: Code may break if ProbeResult structure varies by probe type
**Severity**: MEDIUM
**Evidence Needed**: Check ProbeResult dataclass structure
**Fix Required**:
- Verify ProbeResult structure is consistent
- Handle missing fields gracefully
- Document expected ProbeResult structure

### 6. Assumes Storage Path is Writable
**Issue**: Plan doesn't check if `_prime_being_data/` is writable before use
**Impact**: Crashes on read-only filesystems (containers, CI/CD)
**Severity**: MEDIUM
**Fix Required**:
- Check filesystem permissions before writing
- Provide read-only mode if filesystem not writable
- Handle permission errors gracefully

### 7. Assumes Hypothesis Verification Can Be Automated
**Issue**: Plan says "check if new observations confirm/refute hypotheses" but doesn't specify how to determine confirmation/refutation
**Impact**: Verification logic may be ambiguous or incorrect
**Severity**: MEDIUM
**Fix Required**:
- Define clear verification criteria
- Document how predictions are matched to observations
- Handle edge cases (partial matches, timing issues)

---

## ⚠️ LOW: Overengineering

### 1. Multiple Database Support for MVP
**Issue**: Plan mentions PostgreSQL and MySQL support but MVP only needs SQLite
**Impact**: Unnecessary complexity, more dependencies, more attack surface
**Severity**: LOW
**Fix Consideration**: Start with SQLite only, add other databases in v2

### 2. Complex Personality Mappings
**Issue**: Plan defines 4 personality types with different behaviors, but MVP could start with 2
**Impact**: More code to test and maintain
**Severity**: LOW
**Fix Consideration**: Start with 2 personality types (curious_explorer, cautious_observer), add others in v2

---

## ⚠️ Oversights

### 1. No Error Handling for Hypothesis Formation Failures
**Issue**: Plan doesn't mention what happens if hypothesis formation fails
**Impact**: Crashes on malformed observations or edge cases
**Severity**: MEDIUM
**Fix Required**: Add try/except blocks around hypothesis formation, handle failures gracefully

### 2. No Tests for Edge Cases
**Issue**: MVP tests are basic, no edge cases mentioned (empty observations, malformed data, etc.)
**Impact**: Bugs in edge cases, poor robustness
**Severity**: MEDIUM
**Fix Required**: Add tests for:
- Empty observation lists
- Malformed probe results
- Invalid personality types
- Database connection failures
- Hypothesis verification edge cases

### 3. Missing Cleanup for Database Connections
**Issue**: Plan doesn't mention closing database connections after probing
**Impact**: Connection leaks, resource exhaustion
**Severity**: MEDIUM
**Fix Required**: Use context managers for database connections, ensure cleanup

### 4. No Rate Limiting on Probes
**Issue**: Plan doesn't mention rate limiting for probe operations
**Impact**: Could overwhelm systems being probed, potential DoS
**Severity**: LOW
**Fix Consideration**: Add rate limiting, especially for HTTP probes

### 5. No Documentation for New Features
**Issue**: Plan doesn't mention updating documentation for new features
**Impact**: Users won't know how to use new features
**Severity**: LOW
**Fix Required**: Update PRIME_BEING_PROBE.md with new features, add examples

---

## ⚠️ Missed Obviousness

### 1. No Validation That Learning Actually Improves
**Issue**: Plan says "show adaptation actually improves behavior" but doesn't define what "improves" means
**Impact**: Unclear success criteria, may not actually verify learning works
**Severity**: MEDIUM
**Fix Required**: Define improvement metrics (success rate increase, hypothesis accuracy, etc.)

### 2. No Rollback Mechanism for Adaptations
**Issue**: Plan doesn't mention what happens if an adaptation makes things worse
**Impact**: System could degrade over time with bad adaptations
**Severity**: LOW
**Fix Consideration**: Add adaptation rollback or fitness-based selection

### 3. No Timeout for Database Probes
**Issue**: Plan doesn't mention timeouts for database operations
**Impact**: Database probes could hang indefinitely
**Severity**: MEDIUM
**Fix Required**: Add timeouts to all database operations (5-10 seconds for MVP)

---

## Additional Adversarial Findings

### Failure Modes
- **Database File Locked**: What if database is locked by another process? (No handling)
- **Network Database Unavailable**: What if PostgreSQL/MySQL database is down? (No fallback)
- **Hypothesis Verification Race**: What if multiple hypotheses verified simultaneously? (No locking)
- **Storage Path Full**: What if disk fills up during state save? (No handling)

### Attack Vectors
- **Database Path Traversal**: `../../../etc/passwd` in database path
- **SQL Injection**: If executing user-provided SQL queries
- **Resource Exhaustion**: No limits on number of probes or database connections
- **Information Disclosure**: Probe results may contain sensitive data

### Edge Cases
- **Empty Database**: What if database has no tables? (No handling)
- **Corrupted Database**: What if database file is corrupted? (No handling)
- **Concurrent Probes**: What if multiple probes run simultaneously? (No locking)
- **Invalid Personality**: What if personality_type is None or invalid? (No validation)

---

## Recommendations (Prioritized)

### Priority 1: CRITICAL - Fix Immediately
1. **Add Path Validation**: Validate all database file paths, reject traversal attempts
2. **Restrict Database Types**: SQLite only for MVP, no user-provided connection strings
3. **Add Input Sanitization**: Sanitize all inputs to DatabaseProbe

### Priority 2: HIGH - Fix Before Implementation
4. **Add Error Handling**: Wrap all database operations in try/except blocks
5. **Add Dependency Checks**: Check for sqlite3 availability, handle missing drivers
6. **Add Prediction Validation**: Validate hypothesis predictions, never execute as code

### Priority 3: MEDIUM - Fix During Implementation
7. **Verify Personality Types**: Check Being class for available personality types
8. **Verify Hypothesis Class**: Check Hypothesis class structure for verification support
9. **Add Database Discovery**: Define how to discover database files
10. **Add Timeouts**: Add timeouts to all database operations
11. **Add Edge Case Tests**: Test empty observations, malformed data, etc.
12. **Add Cleanup**: Ensure database connections are closed

### Priority 4: LOW - Consider for Future
13. **Simplify Database Support**: SQLite only for MVP
14. **Simplify Personality Types**: Start with 2 types, add more later
15. **Add Rate Limiting**: Prevent overwhelming probed systems
16. **Add Documentation**: Update docs with new features

---

## Conclusion

This MVP plan has **CRITICAL security vulnerabilities** related to database probing that must be addressed before implementation. Path traversal and connection string injection are serious risks. Additionally, multiple unexamined assumptions about personality types and database dependencies need validation.

**Recommendation**: Do not proceed with implementation until all CRITICAL and HIGH priority issues are addressed. The security vulnerabilities alone make this plan unsafe to implement as-is.

---

**This critique assumes the worst and looks for all the ways things could fail. Address these issues before implementation.**
