# Adversarial Plan Critique: OriginPoint Probe Experimental System

**Date**: 2026-01-14 09:55:39 PST  
**Plan**: OriginPoint Probe Experimental System  
**Critique Mode**: Bad Faith / Adversarial  
**Security-First Analysis**: YES

---

## Executive Summary

**CRITICAL Security Vulnerabilities**: 4  
**HIGH Safety Issues**: 3  
**MEDIUM Unexamined Assumptions**: 12  
**LOW Overengineering**: 5  
**Oversights**: 8  
**Missed Obviousness**: 6

**Overall Assessment**: This plan has **CRITICAL security vulnerabilities** that must be addressed before implementation. The Probe system will handle file operations, state capture, and data collection without proper security measures defined. Multiple unexamined assumptions about integration and behavior could cause catastrophic failures. Significant architectural complexity adds unnecessary risk.

**Recommendation**: **DO NOT PROCEED** until all CRITICAL and HIGH priority issues are addressed. The security vulnerabilities alone make this plan unsafe to implement as-is.

---

## 🔴 CRITICAL: Security Vulnerabilities

### 1. No File Permission Security for Probe Storage (CRITICAL)

**Issue**: Plan specifies `_experiments/probe/` storage but doesn't mention file permissions.

**Attack Vector**: 
- Probe experiment data stored with default permissions (world-readable)
- Observation logs, hypotheses, reflections could be read by other users/processes
- Sensitive experiment data exposed

**Impact**: 
- Information disclosure (experiment results, Being states)
- Potential data leakage if storage is shared
- Privacy violation (Being observations and reflections)

**Severity**: CRITICAL

**Evidence**: 
- Existing Being system uses `0o600` for files, `0o700` for directories (see `src/waft/being.py:1964`)
- Scientific method tool's `StateCapture` doesn't set permissions (see `scientific_method_tool/state_capture.py:68`)
- Plan doesn't specify security measures for Probe storage

**Fix Required**:
- Set restrictive file permissions: `0o600` for files, `0o700` for directories
- Apply permissions after file creation in all Probe storage operations
- Validate storage path is within project (path traversal protection)
- Never store sensitive data (sanitize before storage)

**Code Fix**:
```python
# In ProbeBeing._save_experiment()
experiment_file = self.storage_path / f"probe_originpoint_{experiment_id}.json"
with open(experiment_file, "w") as f:
    json.dump(experiment_data, f, indent=2)
# CRITICAL: Set restrictive permissions
experiment_file.chmod(0o600)  # Owner read/write only
self.storage_path.chmod(0o700)  # Owner read/write/execute only
```

---

### 2. No Input Validation on probe_id/reality_id (CRITICAL)

**Issue**: Plan uses `probe_id` and `reality_id` in file paths without validation.

**Attack Vector**:
- Malicious `probe_id` with path traversal: `probe_id = "../../../etc/passwd"`
- Malicious `reality_id` with control characters: `reality_id = "reality\n../../secrets"`
- Extremely long IDs (DoS): `probe_id = "a" * 10000`
- IDs with null bytes: `probe_id = "probe\x00evil"`

**Impact**:
- Path traversal attacks (read/write files outside project)
- DoS attacks (resource exhaustion from long paths)
- File system corruption (null bytes in filenames)
- Log injection (newlines in IDs)

**Severity**: CRITICAL

**Evidence**:
- Existing Being system has `_validate_being_id()` method (see `src/waft/being.py:1949`)
- Plan doesn't mention validation for Probe IDs
- Scientific method tool doesn't validate experiment IDs

**Fix Required**:
- Validate all IDs before use in file paths
- Reject IDs with `..`, `/`, `\`, null bytes, control characters
- Limit ID length (e.g., max 255 characters)
- Sanitize IDs (alphanumeric + underscore + hyphen only)
- Validate path encoding (UTF-8, handle encoding errors)
- Use `Path.resolve()` and check it's within project root

**Code Fix**:
```python
def _validate_probe_id(self, probe_id: str) -> bool:
    """Validate probe_id is safe for file system use."""
    if not probe_id or len(probe_id) > 255:
        return False
    if any(char in probe_id for char in ['..', '/', '\\', '\x00']):
        return False
    if not probe_id.replace('_', '').replace('-', '').isalnum():
        return False
    return True
```

---

### 3. State Capture Can Read Sensitive Being Data (CRITICAL)

**Issue**: Plan uses `scientific_method_tool/state_capture.py` which captures Being state including skills, fitness, personality.

**Attack Vector**:
- State capture reads Being objects without sanitization
- Sensitive Being data (personality, memories) stored in experiment files
- State snapshots could contain sensitive information
- No access control on who can capture state

**Impact**:
- Information disclosure (Being internal state)
- Privacy violation (Being memories, personality)
- Data leakage if experiment files are shared

**Severity**: CRITICAL

**Evidence**:
- `StateCapture.capture_being_state()` captures full Being state (see `scientific_method_tool/state_capture.py:99`)
- No sanitization of sensitive fields
- Plan doesn't specify what data should be excluded

**Fix Required**:
- Sanitize Being state before capture (exclude sensitive fields)
- Define whitelist of safe fields to capture
- Never capture memories, lessons, or personal data
- Add access control for state capture operations
- Encrypt sensitive state data if storage is shared

**Code Fix**:
```python
def capture_being_state(self, being: Any) -> Dict[str, Any]:
    """Capture SAFE state of a Being (sanitized)."""
    return {
        "being_id": being.being_id,  # Safe
        "reality_id": being.reality_id,  # Safe
        "skills": being.skills,  # Safe (public)
        "fitness": being.fitness,  # Safe (public)
        # EXCLUDE: memories, lessons, personality details, soul_id
    }
```

---

### 4. No Validation of Reality Access (CRITICAL)

**Issue**: Plan assumes Probe can access any Reality without validation.

**Attack Vector**:
- Probe could access Reality it shouldn't have access to
- No validation that Probe belongs to Reality
- Cross-Reality data leakage

**Impact**:
- Unauthorized access to Reality data
- Data leakage between Realities
- Privacy violation

**Severity**: CRITICAL

**Evidence**:
- Plan doesn't specify Reality access control
- Existing Reality system may not have access control
- Probe could observe Beings in other Realities

**Fix Required**:
- Validate Probe has access to Reality before operations
- Check `probe.reality_id` matches `reality.reality_id`
- Add Reality access control checks
- Log unauthorized access attempts

---

## 🔴 HIGH: Safety Issues

### 1. No Error Handling for File I/O Operations

**Issue**: Plan doesn't specify error handling for Probe file operations.

**Impact**: Crashes on file system errors, data loss, corrupted state

**Severity**: HIGH

**Fix Required**:
- Add try/except blocks for all file I/O
- Handle `IOError`, `PermissionError`, `OSError`
- Validate file operations succeed
- Implement retry logic for transient failures
- Log errors for debugging

---

### 2. No Resource Limits on Observations/Experiments

**Issue**: Plan doesn't specify limits on observation history, experiments, or data collection.

**Impact**: 
- Memory exhaustion (unbounded observation_history)
- Disk space exhaustion (unbounded experiment records)
- DoS attacks (malicious Probe creating infinite observations)

**Severity**: HIGH

**Fix Required**:
- Limit observation_history size (e.g., last 1000 observations)
- Limit active hypotheses (e.g., max 10)
- Limit experiment records (e.g., archive old experiments)
- Add disk space checks before writes
- Implement data rotation/archival

---

### 3. No Validation of Scientific Method Tool Integration

**Issue**: Plan assumes `scientific_method_tool/` works correctly without validation.

**Impact**: 
- Integration failures if tool has bugs
- Data corruption if tool has issues
- Unexpected behavior if tool changes

**Severity**: HIGH

**Fix Required**:
- Validate scientific method tool is available
- Test integration before use
- Handle tool failures gracefully
- Add fallback if tool unavailable
- Version pin scientific method tool

---

## ⚠️ MEDIUM: Unexamined Assumptions

### A1: Assumes Reality System Supports Probe Observation

**Assumption**: Probe can observe Reality state, other Beings, environmental features.

**Issue**: 
- Reality system may not expose observation API
- Other Beings may not be observable
- Environmental features may not exist

**Risk**: MEDIUM

**Evidence Needed**: 
- Check Reality system API for observation methods
- Verify Being system exposes observable state
- Test observation capabilities

**Recommendation**: Validate Reality observation API before implementation.

---

### A2: Assumes Scientific Method Tool Handles Probe Data Correctly

**Assumption**: Scientific method tool can handle Probe-specific data structures.

**Issue**: 
- Tool may not support Probe data formats
- Tool may have size limits
- Tool may not handle Probe-specific variables

**Risk**: MEDIUM

**Evidence Needed**: 
- Test scientific method tool with Probe data
- Verify tool supports required features
- Check tool limitations

**Recommendation**: Test integration with sample Probe data before full implementation.

---

### A3: Assumes D&D Stats Enhance Personality Without Conflicts

**Assumption**: D&D stats enhance existing personality without conflicts.

**Issue**: 
- D&D stats may conflict with existing personality traits
- Stats may override personality instead of enhancing
- Stats may not map correctly to personality

**Risk**: MEDIUM

**Evidence Needed**: 
- Test D&D stat integration with personality system
- Verify enhancement vs. override behavior
- Check stat-to-personality mapping

**Recommendation**: Define clear enhancement rules, test with sample personalities.

---

### A4: Assumes Collaborative Piloting Interface Works

**Assumption**: Probe can suggest actions, AI can review and guide.

**Issue**: 
- Interface may not work as expected
- Communication protocol undefined
- Error handling for failed suggestions unclear

**Risk**: MEDIUM

**Evidence Needed**: 
- Design communication protocol
- Test suggestion/review cycle
- Handle edge cases (Probe suggests invalid action)

**Recommendation**: Design and test piloting interface before full implementation.

---

### A5: Assumes Hybrid Exploration Phases Work Correctly

**Assumption**: Exploration evolves from random → systematic → adaptive correctly.

**Issue**: 
- Phase transitions may not work
- Pattern recognition may fail
- Adaptive phase may not combine correctly

**Risk**: MEDIUM

**Evidence Needed**: 
- Test phase transition logic
- Verify pattern recognition works
- Test adaptive exploration

**Recommendation**: Implement and test each phase separately before combining.

---

### A6: Assumes Feedback Loops Function Correctly

**Assumption**: External/Internal pressure loops work as designed.

**Issue**: 
- Pressure detection may fail
- Response generation may be incorrect
- Feedback analysis may be wrong

**Risk**: MEDIUM

**Evidence Needed**: 
- Test pressure detection
- Verify response generation
- Test feedback analysis

**Recommendation**: Test each loop component separately before integration.

---

### A7: Assumes Probe Can Learn from Experiments

**Assumption**: Probe updates behavior based on experiment results.

**Issue**: 
- Learning algorithm undefined
- Update mechanism unclear
- Learning may not converge

**Risk**: MEDIUM

**Evidence Needed**: 
- Define learning algorithm
- Specify update mechanism
- Test learning convergence

**Recommendation**: Design learning algorithm before implementation.

---

### A8: Assumes Observation System Can Access Reality Data

**Assumption**: Observation system can observe Reality, Beings, environment.

**Issue**: 
- Reality may not expose observation API
- Beings may not be observable
- Environment may not have observable features

**Risk**: MEDIUM

**Evidence Needed**: 
- Check Reality observation API
- Verify Being observability
- Test environment observation

**Recommendation**: Validate observation capabilities before implementation.

---

### A9: Assumes Reflection System Can Analyze Feedback

**Assumption**: Reflection system can analyze feedback loops and cause-effect.

**Issue**: 
- Analysis algorithm undefined
- Cause-effect detection may fail
- Reflection may not produce useful insights

**Risk**: MEDIUM

**Evidence Needed**: 
- Define analysis algorithm
- Test cause-effect detection
- Verify reflection produces insights

**Recommendation**: Design analysis algorithm before implementation.

---

### A10: Assumes Probe Storage Path is Writable

**Assumption**: `_experiments/probe/` directory is writable.

**Issue**: 
- Directory may not exist
- Permissions may be wrong
- Disk may be full

**Risk**: MEDIUM

**Evidence Needed**: 
- Check directory exists and is writable
- Verify permissions
- Check disk space

**Recommendation**: Add directory creation and permission checks.

---

### A11: Assumes Probe Can Spawn into Reality

**Assumption**: Probe can be spawned into existing Reality.

**Issue**: 
- Reality may not support Probe spawning
- Spawning may require special permissions
- Spawning may fail

**Risk**: MEDIUM

**Evidence Needed**: 
- Check Reality spawning API
- Verify spawning permissions
- Test spawning process

**Recommendation**: Validate spawning process before implementation.

---

### A12: Assumes D&D Character Sheet Data is Safe

**Assumption**: D&D character sheet data doesn't contain sensitive information.

**Issue**: 
- Character data may contain sensitive info
- Stats may reveal internal state
- Character data may be used for attacks

**Risk**: MEDIUM

**Evidence Needed**: 
- Review character data structure
- Check for sensitive fields
- Validate character data

**Recommendation**: Sanitize character data before storage.

---

## ⚠️ LOW: Overengineering

### 1. Separate Probe System When Being Subclass Would Work

**Issue**: Plan creates separate ProbeBeing class when Being subclass would work.

**Impact**: 
- Code duplication
- Maintenance burden
- Integration complexity

**Severity**: LOW

**Consideration**: Could use Being subclass with Probe capabilities instead of separate system.

---

### 2. Too Many Components for Experimental System

**Issue**: Plan has 8 separate components for experimental system.

**Impact**: 
- Coordination complexity
- More points of failure
- Harder to test

**Severity**: LOW

**Consideration**: Could combine some components (e.g., observation + reflection).

---

### 3. Over-Complex Feedback Loop System

**Issue**: Separate components for pressure detection, response generation, feedback analysis.

**Impact**: 
- Unnecessary abstraction
- Harder to understand
- More code to maintain

**Severity**: LOW

**Consideration**: Could simplify to single FeedbackLoop class.

---

### 4. D&D Character Sheet May Be Unnecessary

**Issue**: D&D stats may not add value beyond existing personality system.

**Impact**: 
- Unnecessary complexity
- Maintenance burden
- Potential conflicts

**Severity**: LOW

**Consideration**: Could enhance personality directly without D&D stats.

---

### 5. Collaborative Piloting May Be Over-Engineered

**Issue**: Separate piloting interface may be unnecessary for experimental system.

**Impact**: 
- Unnecessary complexity
- More code to maintain
- Harder to test

**Severity**: LOW

**Consideration**: Could use simpler direct control for experimental system.

---

## ⚠️ Oversights

### 1. No Tests Mentioned

**Issue**: Plan doesn't mention testing strategy.

**Impact**: Untested code, potential bugs

**Severity**: MEDIUM

**Fix Required**: Add unit tests, integration tests, security tests.

---

### 2. No Error Recovery

**Issue**: Plan doesn't specify error recovery mechanisms.

**Impact**: Crashes on errors, data loss

**Severity**: MEDIUM

**Fix Required**: Add error recovery, state restoration, retry logic.

---

### 3. No Performance Considerations

**Issue**: Plan doesn't consider performance (observation frequency, experiment duration).

**Impact**: Slow system, resource exhaustion

**Severity**: MEDIUM

**Fix Required**: Add performance limits, optimization, monitoring.

---

### 4. No Documentation Plan

**Issue**: Plan mentions documentation but doesn't specify what or how.

**Impact**: Unclear usage, integration issues

**Severity**: LOW

**Fix Required**: Specify documentation requirements (API docs, usage guide, examples).

---

### 5. No Migration Plan

**Issue**: Plan doesn't specify how to migrate Probe data if system changes.

**Impact**: Data loss on system changes

**Severity**: LOW

**Fix Required**: Add migration strategy, versioning, backward compatibility.

---

### 6. No Cleanup/Archival Strategy

**Issue**: Plan doesn't specify how to clean up old experiments/observations.

**Impact**: Disk space exhaustion, performance degradation

**Severity**: MEDIUM

**Fix Required**: Add cleanup strategy, archival, data rotation.

---

### 7. No Monitoring/Logging

**Issue**: Plan doesn't specify monitoring or logging for Probe operations.

**Impact**: Hard to debug, no visibility into Probe behavior

**Severity**: MEDIUM

**Fix Required**: Add logging, monitoring, metrics.

---

### 8. No Rollback Plan

**Issue**: Plan doesn't specify how to rollback if Probe system fails.

**Impact**: No recovery if system breaks

**Severity**: MEDIUM

**Fix Required**: Add rollback strategy, state backup, recovery procedures.

---

## ⚠️ Missed Obviousness

### 1. No Authentication/Authorization

**Issue**: Plan doesn't specify who can create/control Probes.

**Impact**: Unauthorized Probe creation, system abuse

**Severity**: MEDIUM

**Fix Required**: Add authentication, authorization, access control.

---

### 2. No Rate Limiting

**Issue**: Plan doesn't limit Probe operation frequency.

**Impact**: DoS attacks, resource exhaustion

**Severity**: MEDIUM

**Fix Required**: Add rate limiting, operation throttling.

---

### 3. No Input Size Limits

**Issue**: Plan doesn't limit size of observations, hypotheses, experiments.

**Impact**: Memory exhaustion, DoS attacks

**Severity**: MEDIUM

**Fix Required**: Add size limits, validation, truncation.

---

### 4. No Validation of Probe Actions

**Issue**: Plan doesn't validate Probe-suggested actions before execution.

**Impact**: Invalid actions executed, system damage

**Severity**: HIGH

**Fix Required**: Add action validation, whitelist of allowed actions.

---

### 5. No Isolation Between Probes

**Issue**: Plan doesn't specify if multiple Probes are isolated.

**Impact**: Probe interference, data leakage

**Severity**: MEDIUM

**Fix Required**: Add Probe isolation, separate storage, access control.

---

### 6. No Versioning

**Issue**: Plan doesn't specify versioning for Probe system or data.

**Impact**: Breaking changes, data incompatibility

**Severity**: LOW

**Fix Required**: Add versioning, migration, backward compatibility.

---

## Additional Adversarial Findings

### Failure Modes

1. **Disk Full**: What happens if disk fills up during experiment? (No handling)
2. **Network Down**: What if external dependencies unavailable? (No fallback)
3. **Process Killed**: What if process killed mid-experiment? (No cleanup)
4. **System Under Load**: What if system is under heavy load? (No throttling)

### Attack Vectors

1. **Path Traversal**: Probe IDs with `../` could escape project directory
2. **Resource Exhaustion**: No limits on observations/experiments
3. **Data Injection**: Malicious data in observations could corrupt system
4. **State Manipulation**: Probe could manipulate its own state maliciously

### Edge Cases

1. **Empty Reality**: What if Reality has no Beings? (No handling)
2. **Invalid Observations**: What if observations are malformed? (No validation)
3. **Concurrent Probes**: What if multiple Probes run simultaneously? (Race conditions)
4. **Corrupted State**: What if Probe state is corrupted? (No recovery)

---

## Recommendations (Prioritized)

### Priority 1: CRITICAL - Fix Immediately

1. **Add File Permission Security**: Set `0o600` for files, `0o700` for directories
2. **Validate All IDs**: Add validation for probe_id, reality_id, experiment_id
3. **Sanitize State Capture**: Exclude sensitive data from state capture
4. **Add Reality Access Control**: Validate Probe has access to Reality

### Priority 2: HIGH - Fix Before Implementation

5. **Add Error Handling**: Handle all file I/O errors, network errors
6. **Add Resource Limits**: Limit observation history, experiments, data size
7. **Validate Scientific Method Integration**: Test integration before use
8. **Add Action Validation**: Validate Probe-suggested actions before execution

### Priority 3: MEDIUM - Fix During Implementation

9. **Add Tests**: Unit tests, integration tests, security tests
10. **Add Monitoring/Logging**: Log Probe operations, monitor behavior
11. **Add Cleanup Strategy**: Archive old experiments, rotate data
12. **Add Error Recovery**: State restoration, retry logic, rollback

### Priority 4: LOW - Consider for Future

13. **Simplify Architecture**: Consider if separate system is necessary
14. **Add Versioning**: Version Probe system and data
15. **Add Documentation**: API docs, usage guide, examples

---

## Conclusion

This plan has **CRITICAL security vulnerabilities** that must be addressed before any code is written. The Probe system will handle file operations, state capture, and data collection without proper security measures. These are not minor issues - they are **show-stoppers**.

Additionally, there are multiple unexamined assumptions that could cause catastrophic failures, significant overengineering that adds unnecessary risk, and obvious oversights that should have been caught.

**Recommendation**: **DO NOT PROCEED** with implementation until all CRITICAL and HIGH priority issues are addressed. The security vulnerabilities alone make this plan unsafe to implement as-is.

---

**This critique assumes the worst and looks for all the ways things could fail. Address these issues before implementation.**
