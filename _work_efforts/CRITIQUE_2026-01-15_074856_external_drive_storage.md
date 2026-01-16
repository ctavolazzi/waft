# Adversarial Plan Critique

**Date**: 2026-01-15
**Time**: 07:48:56 PST
**Plan**: External Drive Storage System - Content-Aware Routing
**Critique Mode**: Bad Faith / Adversarial / Security-First

---

## Executive Summary

**CRITICAL Security Vulnerabilities**: 4
**HIGH Safety Issues**: 5
**MEDIUM Unexamined Assumptions**: 11
**LOW Overengineering**: 3
**Oversights**: 8
**Missed Obviousness**: 5

**Overall Assessment**: This plan has **CRITICAL security vulnerabilities** related to path validation, file permissions, and external drive access. Multiple unexamined assumptions about drive availability, filesystem behavior, and content classification could cause catastrophic failures. The plan lacks critical error handling, validation, and security considerations for external storage operations.

---

## 🔴 CRITICAL: Security Vulnerabilities

### 1. No Path Validation for External Drive Operations (CRITICAL)
**Issue**: Plan routes content to `/Volumes/Easystore/waft/{project_name}/` without validating:
- Path traversal in project_name
- Symlink attacks on external drive
- Absolute paths that escape intended directory
- Malicious directory names

**Attack Vector**:
- Malicious project_name: `project_name = "../../../etc/passwd"` → writes to system files
- Symlink on external drive: `/Volumes/Easystore/waft/` → symlink to `/etc/` → system compromise
- Path components with null bytes: `project_name = "waft\x00evil"` → filesystem corruption
- UNC paths on Windows: `\\?\C:\Windows\System32\` → system file access

**Impact**:
- Writing files outside intended directory
- System file corruption
- Potential root/system compromise
- Data exfiltration

**Severity**: CRITICAL

**Evidence**:
- Plan mentions `get_external_drive_base(project_name)` but no validation
- No mention of path sanitization
- Existing codebase has `_validate_path_in_project()` pattern (see `src/waft/karma.py:93`)
- No validation before `Path.resolve()` or after

**Fix Required**:
- Validate project_name before use (reject `..`, `/`, `\`, null bytes, control characters)
- Limit project_name length (max 255 characters)
- Sanitize project_name (alphanumeric + underscore + hyphen only)
- Validate resolved path is within `/Volumes/Easystore/waft/` AFTER `Path.resolve()`
- Check for symlinks before creating directories
- Reject UNC paths on Windows
- Use whitelist of allowed characters

**Code Fix**:
```python
def _validate_project_name(project_name: str) -> bool:
    """Validate project_name is safe for filesystem use."""
    if not project_name:
        return False
    if len(project_name) > 255:
        return False
    if any(c in project_name for c in ['..', '/', '\\', '\x00']):
        return False
    if any(ord(c) < 32 for c in project_name):
        return False
    if not project_name.replace('_', '').replace('-', '').isalnum():
        return False
    return True

def get_external_drive_base(project_name: Optional[str] = None) -> Optional[Path]:
    # CRITICAL: Validate project_name
    if project_name and not _validate_project_name(project_name):
        raise ValueError(f"Invalid project_name: {project_name}")
    
    # ... rest of implementation
    base_path = Path(f"/Volumes/Easystore/waft/{project_name}/")
    
    # CRITICAL: Validate resolved path
    resolved = base_path.resolve()
    expected_base = Path("/Volumes/Easystore/waft/").resolve()
    if not str(resolved).startswith(str(expected_base)):
        raise ValueError(f"Path traversal detected: {resolved}")
    
    # CRITICAL: Check for symlinks
    if resolved.is_symlink():
        raise ValueError(f"Symlink detected: {resolved}")
    
    return resolved
```

### 2. No File Permissions Set on External Drive Files (CRITICAL)
**Issue**: Plan creates files on external drive but doesn't set restrictive permissions.

**Attack Vector**:
- External drive files world-readable: Other users can read sensitive content
- External drive files world-writable: Other users can modify/delete content
- Registry files world-readable: Information disclosure

**Impact**:
- Sensitive content exposure (experiments, narratives, research data)
- Data tampering (malicious modification of content)
- Information disclosure (registry reveals storage locations)

**Severity**: CRITICAL

**Evidence**:
- Plan mentions creating directories/files but no permission setting
- Existing codebase sets permissions (see `src/waft/being.py:2036`, `src/waft/karma.py:213`)
- Registry file `_pyrite/.storage_registry.json` has no permission specification

**Fix Required**:
- Set restrictive file permissions: `0o600` (owner read/write only)
- Set restrictive directory permissions: `0o700` (owner read/write/execute only)
- Apply permissions after file creation in all storage operations
- Set permissions on registry file
- Handle permission errors gracefully (Windows compatibility)

**Code Fix**:
```python
def get_storage_path(...) -> Path:
    # ... create path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # CRITICAL: Set directory permissions
    try:
        output_path.parent.chmod(0o700)
    except (OSError, PermissionError):
        pass  # Ignore on Windows or if permissions can't be set
    
    return output_path

# After file write:
output_path.write_bytes(data)
# CRITICAL: Set file permissions
try:
    output_path.chmod(0o600)
except (OSError, PermissionError):
    pass  # Ignore on Windows
```

### 3. No Input Validation on Relative Paths (CRITICAL)
**Issue**: Plan accepts `relative_path: Path` in `get_storage_path()` without validation.

**Attack Vector**:
- Path traversal: `relative_path = Path("../../etc/passwd")` → escapes project
- Absolute paths: `relative_path = Path("/etc/passwd")` → writes to system
- Symlinks in path: `relative_path = Path("_experiments/../symlink")` → escapes via symlink
- Control characters: `relative_path = Path("_experiments/\x00evil")` → filesystem issues

**Impact**:
- Writing files outside project directory
- System file access
- Data exfiltration
- Filesystem corruption

**Severity**: CRITICAL

**Evidence**:
- Plan doesn't mention path validation
- Existing codebase has validation patterns (see `src/waft/karma.py:93`, `src/waft/ui/streamlit/work_efforts_integration.py:58`)
- No validation before or after path resolution

**Fix Required**:
- Validate relative_path before use (reject `..`, absolute paths, null bytes)
- Check resolved path is within intended directory AFTER `Path.resolve()`
- Reject symlinks in path components
- Sanitize path components
- Use whitelist of allowed directory patterns

**Code Fix**:
```python
def _validate_path_in_storage(relative_path: Path, base_path: Path) -> bool:
    """Validate path is within storage base directory."""
    try:
        # Reject absolute paths
        if relative_path.is_absolute():
            return False
        
        # Reject path traversal
        if '..' in relative_path.parts:
            return False
        
        # Resolve and check
        resolved = (base_path / relative_path).resolve()
        base_resolved = base_path.resolve()
        
        # Check path is within base
        return str(resolved).startswith(str(base_resolved))
    except (OSError, ValueError):
        return False

def get_storage_path(relative_path: Path, ...) -> Path:
    # CRITICAL: Validate path
    if not _validate_path_in_storage(relative_path, base_path):
        raise ValueError(f"Invalid path: {relative_path}")
    
    # ... rest of implementation
```

### 4. Storage Registry File World-Readable (CRITICAL)
**Issue**: Registry file `_pyrite/.storage_registry.json` has no permission specification.

**Attack Vector**:
- Registry file world-readable: Other users can see where all content is stored
- Registry file world-writable: Other users can modify registry, causing data loss
- Information disclosure: Registry reveals storage locations, content types, timestamps

**Impact**:
- Information disclosure (storage locations, content types)
- Data tampering (malicious registry modification)
- Privacy violation (content tracking exposed)

**Severity**: CRITICAL

**Evidence**:
- Plan mentions registry file but no permission setting
- Existing codebase sets permissions on similar files (see `src/waft/being.py:2036`)

**Fix Required**:
- Set restrictive file permissions: `0o600` (owner read/write only)
- Set restrictive directory permissions on `_pyrite/`: `0o700`
- Apply permissions after registry file creation
- Never store sensitive data in registry (sanitize before storage)

**Code Fix**:
```python
class StorageRegistry:
    def _save_registry(self):
        registry_file = self.project_path / "_pyrite" / ".storage_registry.json"
        registry_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(registry_file, 'w') as f:
            json.dump(self.registry, f, indent=2)
        
        # CRITICAL: Set restrictive permissions
        try:
            registry_file.chmod(0o600)
            registry_file.parent.chmod(0o700)
        except (OSError, PermissionError):
            pass  # Ignore on Windows
```

---

## 🔴 HIGH: Safety Issues

### 1. No Error Handling for Drive Disconnection During Write
**Issue**: Plan mentions "handle gracefully" but doesn't specify how.

**Impact**:
- Partial writes (corrupted files)
- Data loss (incomplete writes)
- No rollback mechanism
- Silent failures

**Severity**: HIGH

**Fix Required**:
- Use atomic writes (write to temp file, then rename)
- Check drive availability before write
- Retry mechanism with exponential backoff
- Rollback on failure
- Clear error messages

### 2. No Validation of External Drive Filesystem Type
**Issue**: Plan assumes external drive is writable but doesn't check filesystem type.

**Impact**:
- Read-only filesystems (NTFS on macOS, FAT32 limitations)
- Filesystem incompatibilities (case sensitivity, permissions)
- Write failures on unsupported filesystems

**Severity**: HIGH

**Fix Required**:
- Check filesystem type before use
- Validate write permissions
- Handle filesystem-specific limitations
- Provide clear error messages

### 3. No Concurrent Access Protection
**Issue**: Multiple processes could write to external drive simultaneously.

**Impact**:
- Race conditions (file corruption)
- Registry corruption (concurrent writes)
- Data loss (overwrites)

**Severity**: HIGH

**Fix Required**:
- File locking for registry writes
- Atomic operations for file creation
- Process coordination (lock files)
- Handle lock timeouts

### 4. No Size Limits on External Drive Operations
**Issue**: Plan doesn't limit size of content written to external drive.

**Impact**:
- Disk space exhaustion
- DoS attacks (extremely large files)
- System instability

**Severity**: HIGH

**Fix Required**:
- Check available disk space before write
- Set maximum file size limits
- Set maximum directory size limits
- Provide clear error messages when limits exceeded

### 5. No Validation of Content Classification Patterns
**Issue**: Content classification uses pattern matching but patterns aren't validated.

**Impact**:
- Misclassification (core content routed to external, augmented to local)
- Security bypass (malicious directory names match patterns)
- Data loss (wrong routing)

**Severity**: HIGH

**Fix Required**:
- Validate classification patterns (no regex injection)
- Whitelist approach (explicit allowed patterns)
- Test classification with edge cases
- Log classification decisions for audit

---

## ⚠️ MEDIUM: Unexamined Assumptions

### 1. Assumes External Drive Always Mounted at `/Volumes/Easystore`
**Issue**: Drive might be mounted at different location or with different name.

**Impact**: Drive detection fails, all content falls back to local

**Fix Required**: Check multiple possible mount points, use environment variable for custom path

### 2. Assumes External Drive is Writable
**Issue**: Drive might be read-only (NTFS on macOS, write-protected).

**Impact**: Write failures, silent fallback to local

**Fix Required**: Test write permissions before use, handle read-only gracefully

### 3. Assumes Project Name is Safe for Filesystem
**Issue**: Project name might contain special characters, spaces, etc.

**Impact**: Invalid directory names, filesystem errors

**Fix Required**: Sanitize project name, validate before use

### 4. Assumes External Drive Has Sufficient Space
**Issue**: Drive might be full or nearly full.

**Impact**: Write failures, data loss

**Fix Required**: Check available space before write, provide clear errors

### 5. Assumes Filesystem Supports Permissions
**Issue**: FAT32/exFAT don't support Unix permissions.

**Impact**: Permission setting fails silently, files remain world-readable

**Fix Required**: Check filesystem type, handle permission errors gracefully

### 6. Assumes Path Resolution is Atomic
**Issue**: Path resolution might change between check and use (drive unmounts).

**Impact**: Race conditions, write failures

**Fix Required**: Validate path immediately before use, handle errors

### 7. Assumes Registry File is Always Accessible
**Issue**: Registry file might be locked, corrupted, or inaccessible.

**Impact**: Registry operations fail, system loses track of content

**Fix Required**: Handle registry errors gracefully, provide fallback

### 8. Assumes Content Classification is Deterministic
**Issue**: Same path might be classified differently in different contexts.

**Impact**: Inconsistent routing, data loss

**Fix Required**: Make classification deterministic, test edge cases

### 9. Assumes External Drive Persists Across Sessions
**Issue**: Drive might be unmounted between sessions.

**Impact**: System loses track of content location

**Fix Required**: Validate drive availability on startup, update registry

### 10. Assumes No Symlinks in Project Structure
**Issue**: Project might contain symlinks that point outside project.

**Impact**: Content routed incorrectly, security issues

**Fix Required**: Check for symlinks, handle appropriately

### 11. Assumes Python Path Operations are Safe
**Issue**: Path operations might fail on edge cases (very long paths, special characters).

**Impact**: Runtime errors, data loss

**Fix Required**: Validate paths, handle edge cases, provide clear errors

---

## ⚠️ LOW: Overengineering

### 1. Storage Registry Might Be Overkill
**Issue**: Full registry system for simple path routing might be unnecessary.

**Impact**: Maintenance burden, potential bugs, complexity

**Fix Consideration**: Consider simpler approach (just route, don't track)

### 2. Content Classification System Too Complex
**Issue**: Pattern-based classification with extensibility might be over-engineered.

**Impact**: Maintenance burden, potential misclassification

**Fix Consideration**: Consider simpler whitelist/blacklist approach

### 3. Multiple Path Resolution Functions
**Issue**: `get_storage_path()` and `resolve_output_path()` might be redundant.

**Impact**: Confusion, maintenance burden

**Fix Consideration**: Consolidate into single function

---

## ⚠️ Oversights

### 1. No Error Handling for Directory Creation Failures
**Issue**: `mkdir(parents=True, exist_ok=True)` might fail.

**Impact**: Runtime errors, data loss

**Fix Required**: Add try/except, handle errors gracefully

### 2. No Cleanup for Failed Writes
**Issue**: Partial writes might leave corrupted files.

**Impact**: Data corruption, disk space waste

**Fix Required**: Use atomic writes, cleanup on failure

### 3. No Tests Mentioned
**Issue**: Plan doesn't mention testing strategy.

**Impact**: Untested code, potential bugs

**Fix Required**: Add unit tests, integration tests, security tests

### 4. No Documentation for Storage Registry
**Issue**: Registry format and usage not documented.

**Impact**: Confusion, misuse

**Fix Required**: Document registry format, usage, query functions

### 5. No Migration Strategy for Existing Content
**Issue**: Plan doesn't mention migrating existing content to external drive.

**Impact**: Content remains local, inconsistent storage

**Fix Required**: Add migration script, document migration process

### 6. No Monitoring/Logging Strategy
**Issue**: Plan doesn't mention logging storage operations.

**Impact**: Difficult to debug, no audit trail

**Fix Required**: Add logging for storage operations, errors, routing decisions

### 7. No Performance Considerations
**Issue**: Plan doesn't mention performance impact of drive detection.

**Impact**: Slow operations, poor user experience

**Fix Required**: Consider caching drive availability, optimize path resolution

### 8. No Rollback Mechanism
**Issue**: No way to undo routing decisions or migrate content back.

**Impact**: Data stuck on external drive, no recovery

**Fix Required**: Add rollback/migration tools

---

## ⚠️ Missed Obviousness

### 1. No Authentication/Authorization
**Issue**: No mention of who can access external drive content.

**Impact**: Unauthorized access, data exposure

**Fix Required**: Consider access control, authentication

### 2. No Backup Strategy
**Issue**: External drive might fail, no backup mentioned.

**Impact**: Data loss, no recovery

**Fix Required**: Document backup strategy, consider redundancy

### 3. No Encryption for Sensitive Content
**Issue**: Sensitive content (experiments, research) stored unencrypted on external drive.

**Impact**: Data exposure if drive lost/stolen

**Fix Required**: Consider encryption for sensitive content

### 4. No Rate Limiting
**Issue**: No limits on storage operations.

**Impact**: Resource exhaustion, DoS attacks

**Fix Required**: Add rate limiting, resource limits

### 5. No Input Size Limits
**Issue**: No limits on content size written to external drive.

**Impact**: Disk space exhaustion, DoS attacks

**Fix Required**: Add size limits, validate before write

---

## Additional Adversarial Findings

### Failure Modes
- **Drive Unmounts During Write**: Partial write, corrupted file, no recovery
- **Drive Fails**: All content on external drive lost, no backup
- **Registry Corruption**: System loses track of content, data orphaned
- **Path Resolution Race**: Drive unmounts between check and use, write fails
- **Permission Denied**: Filesystem doesn't support permissions, files world-readable

### Attack Vectors
- **Path Traversal**: Malicious project_name or relative_path escapes directory
- **Symlink Attacks**: Symlinks on external drive point to system files
- **Resource Exhaustion**: Extremely large files exhaust disk space
- **Registry Tampering**: Malicious modification of registry file
- **Classification Bypass**: Malicious directory names match core patterns

### Edge Cases
- **Empty External Drive**: Drive exists but is empty, write fails
- **Read-Only External Drive**: Drive is read-only, write fails
- **Very Long Paths**: Paths exceed filesystem limits, write fails
- **Concurrent Writes**: Multiple processes write simultaneously, corruption
- **Unicode Paths**: Paths with special characters, encoding issues

---

## Recommendations (Prioritized)

### Priority 1: CRITICAL - Fix Immediately
1. **Add Path Validation**: Validate all paths (project_name, relative_path) before use
2. **Set File Permissions**: Set restrictive permissions (0o600/0o700) on all files/directories
3. **Add Input Sanitization**: Sanitize all inputs (project_name, paths) before use
4. **Validate External Drive Paths**: Check resolved paths are within intended directory
5. **Set Registry Permissions**: Set restrictive permissions on registry file

### Priority 2: HIGH - Fix Before Implementation
6. **Add Error Handling**: Handle drive disconnection, write failures, permission errors
7. **Add Concurrent Access Protection**: File locking, atomic operations
8. **Add Size Limits**: Check disk space, limit file sizes
9. **Validate Filesystem Type**: Check filesystem supports required features
10. **Add Atomic Writes**: Use temp files, rename for atomicity

### Priority 3: MEDIUM - Fix During Implementation
11. **Add Tests**: Unit tests, integration tests, security tests
12. **Add Documentation**: Document registry format, usage, migration
13. **Add Logging**: Log storage operations, errors, routing decisions
14. **Handle Edge Cases**: Empty drive, read-only drive, long paths, Unicode
15. **Add Migration Strategy**: Script to migrate existing content

### Priority 4: LOW - Consider for Future
16. **Simplify Architecture**: Consider if registry is necessary
17. **Add Monitoring**: Monitor drive availability, storage usage
18. **Consider Encryption**: Encrypt sensitive content on external drive
19. **Add Backup Strategy**: Document backup approach
20. **Add Rollback Tools**: Tools to migrate content back to local

---

## Conclusion

This plan has **CRITICAL security vulnerabilities** that must be addressed before any implementation. Path validation, file permissions, and input sanitization are completely missing. These are not minor issues - they are **show-stoppers**.

Additionally, there are multiple unexamined assumptions about drive availability, filesystem behavior, and error handling that could cause catastrophic failures. The plan lacks critical error handling, validation, and security considerations.

**Recommendation**: Do not proceed with implementation until all CRITICAL and HIGH priority issues are addressed. The security vulnerabilities alone make this plan unsafe to implement as-is.

---

**This critique assumes the worst and looks for all the ways things could fail. Address these issues before implementation.**
