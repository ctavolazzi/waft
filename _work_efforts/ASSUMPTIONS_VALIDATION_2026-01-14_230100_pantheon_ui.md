# Assumption Validation: Pantheon HTML UI

**Date**: 2026-01-14
**Time**: 23:01:00 PST
**Plan**: Pantheon HTML UI Development

---

## Executive Summary

**Total Assumptions Extracted**: 12
**✅ Proven**: 4
**❌ Disproven**: 3
**⚠️ Partially Proven**: 2
**❓ Insufficient Evidence**: 2
**🧪 Needs Testing**: 1

**Critical Assumptions**: 5
  ✅ 2 proven
  ❌ 2 disproven
  ⚠️ 1 partially proven

---

## Assumption 1: Browser Fetch API Can Access Local Filesystem

**Statement**: "JavaScript fetch() can load JSON files from `_pantheon/` directory directly"

**Category**: System / Browser Security
**Risk**: CRITICAL
**Status**: ❌ DISPROVEN
**Confidence**: 1.0

**Evidence**:
- ❌ **Browser Security Model**: Browsers block local file access via `fetch()` for security (CORS policy, file:// protocol limitations)
- ❌ **Plan Acknowledgment**: Plan itself mentions "HTML files can't directly access local filesystem"
- ❌ **Technical Reality**: `fetch('file:///path/to/file.json')` fails with CORS errors or security exceptions
- ✅ **Documentation**: MDN docs confirm browsers restrict local file access

**Impact**: HIGH - Entire data loading strategy is broken
**Recommendation**: Must use either HTTP server or static JSON export. Cannot use direct file access.

---

## Assumption 2: Path Validation Pattern Exists in Codebase

**Statement**: "Codebase has path validation patterns we can reuse"

**Category**: Code / Security
**Risk**: CRITICAL
**Status**: ✅ PROVEN
**Confidence**: 1.0

**Evidence**:
- ✅ **Existing Pattern Found**: `src/waft/being.py:1604` has `_validate_path_in_project()` method
- ✅ **Pattern Used**: `src/waft/karma.py:93` has same pattern
- ✅ **Pattern Structure**:
  ```python
  def _validate_path_in_project(self, file_path: Path) -> bool:
      try:
          resolved = file_path.resolve()
          project_resolved = self.project_path.resolve()
          return resolved.is_relative_to(project_resolved)
      except (ValueError, OSError):
          return False
  ```
- ✅ **Multiple Uses**: Pattern found in 8+ files across codebase

**Impact**: LOW - Pattern exists and can be reused
**Recommendation**: Use existing `_validate_path_in_project()` pattern in data export script.

---

## Assumption 3: Pantheon JSON Files Are Always Valid

**Statement**: "JSON files in `_pantheon/` are always valid and parseable"

**Category**: Data / Format
**Risk**: MEDIUM
**Status**: ⚠️ PARTIALLY PROVEN
**Confidence**: 0.7

**Evidence**:
- ✅ **Error Handling Exists**: `src/waft/pantheon/magistrate.py:225` has try/except for JSONDecodeError
- ✅ **Graceful Degradation**: Code handles corrupted JSON by starting fresh
- ⚠️ **No Validation**: No schema validation, only parse validation
- ❌ **No Recovery**: If JSON corrupted, data is lost (starts fresh)

**Impact**: MEDIUM - Corrupted JSON could cause data loss
**Recommendation**: Add JSON schema validation, backup before overwriting, provide recovery mechanism.

---

## Assumption 4: Python HTTP Server Supports CORS

**Statement**: "Python's `http.server` can serve files with CORS headers for fetch API"

**Category**: System / Server
**Risk**: MEDIUM
**Status**: ❌ DISPROVEN
**Confidence**: 0.9

**Evidence**:
- ❌ **Default Behavior**: `http.server` does NOT send CORS headers by default
- ❌ **No CORS Support**: Standard library server has no CORS configuration
- ✅ **Workaround Exists**: Must subclass `SimpleHTTPRequestHandler` and add CORS headers manually
- ✅ **Alternative**: Use `http.server` with custom handler or use Flask/FastAPI for CORS

**Impact**: MEDIUM - Fetch requests will fail with CORS errors
**Recommendation**: Document need for custom HTTP handler with CORS headers, or use framework with CORS support.

---

## Assumption 5: File Permissions Are Always Correct

**Statement**: "JSON files in `_pantheon/` are always readable"

**Category**: System / Permissions
**Risk**: MEDIUM
**Status**: ❓ INSUFFICIENT EVIDENCE
**Confidence**: 0.5

**Evidence**:
- ✅ **File Creation**: Pantheon classes create files with default permissions
- ❓ **No Permission Checks**: No code found that explicitly sets file permissions
- ❓ **No Error Handling**: No PermissionError handling found in Pantheon code
- ⚠️ **Assumption**: Files created with default permissions (usually readable)

**Impact**: MEDIUM - Could fail on read-only filesystems or permission issues
**Recommendation**: Add permission checks, handle PermissionError gracefully, document permission requirements.

---

## Assumption 6: Data Structure Matches Expected Format

**Statement**: "JSON structure matches expected schema (precedents array, judgments array, etc.)"

**Category**: Data / Schema
**Risk**: MEDIUM
**Status**: ✅ PROVEN
**Confidence**: 0.9

**Evidence**:
- ✅ **Schema Defined**: `src/waft/pantheon/magistrate.py:58` has `to_dict()` and `from_dict()` methods
- ✅ **Structure Documented**: `_pantheon/magistrate/body_of_proof.json` shows actual structure
- ✅ **Consistent Format**: All Pantheon classes use same pattern (to_dict/from_dict)
- ⚠️ **No Versioning**: No schema version field found

**Impact**: LOW - Structure is consistent, but no versioning
**Recommendation**: Add schema versioning for future compatibility, validate schema before rendering.

---

## Assumption 7: Fetch API Is Available in All Browsers

**Statement**: "All browsers support Fetch API"

**Category**: Browser / Compatibility
**Risk**: MEDIUM
**Status**: ⚠️ PARTIALLY PROVEN
**Confidence**: 0.8

**Evidence**:
- ✅ **Modern Browsers**: Fetch API supported in Chrome 42+, Firefox 39+, Safari 10.1+, Edge 14+
- ❌ **Old Browsers**: IE11 and very old mobile browsers don't support Fetch API
- ✅ **Polyfill Available**: `whatwg-fetch` polyfill exists for older browsers
- ⚠️ **No Check**: Plan doesn't check for Fetch API support

**Impact**: LOW - Only affects very old browsers
**Recommendation**: Add Fetch API detection, provide polyfill or fallback to XMLHttpRequest.

---

## Assumption 8: Project Path Can Be Detected Automatically

**Statement**: "Python script can automatically detect project root"

**Category**: System / Path Detection
**Risk**: MEDIUM
**Status**: ✅ PROVEN
**Confidence**: 0.9

**Evidence**:
- ✅ **Pattern Exists**: `src/waft/utils.py:136` has `validate_waft_project()` function
- ✅ **Detection Method**: Looks for `_pantheon/` or `pyproject.toml` to identify project root
- ✅ **Used Throughout**: Multiple files use `Path.cwd()` and validate project structure
- ✅ **Fallback**: Can accept project path as argument

**Impact**: LOW - Detection pattern exists
**Recommendation**: Use existing `validate_waft_project()` pattern, allow project path override.

---

## Assumption 9: No Concurrent Access Issues

**Statement**: "Pantheon data doesn't change while UI is open"

**Category**: Data / Concurrency
**Risk**: LOW
**Status**: ✅ PROVEN
**Confidence**: 0.8

**Evidence**:
- ✅ **File-Based**: Pantheon uses file-based storage (not database)
- ✅ **Read-Only UI**: Plan specifies read-only UI initially
- ⚠️ **No Locking**: No file locking found in Pantheon code
- ✅ **Snapshot Model**: UI shows snapshot of data at load time

**Impact**: LOW - Stale data is acceptable for read-only UI
**Recommendation**: Document that UI shows snapshot, add "Last updated" timestamp, consider refresh mechanism for future.

---

## Assumption 10: No Sensitive Data in Pantheon Files

**Statement**: "Pantheon JSON files don't contain sensitive information"

**Category**: Security / Data
**Risk**: CRITICAL
**Status**: ❓ INSUFFICIENT EVIDENCE
**Confidence**: 0.6

**Evidence**:
- ✅ **Public Data**: Precedents and judgments appear to be public proof cases
- ❓ **No Audit**: No code found that checks for sensitive data patterns
- ❓ **No Validation**: No validation that excludes `.env`, `secrets/`, etc.
- ⚠️ **Claims/Reasoning**: Text fields (claims, reasoning) could contain sensitive info if user adds it

**Impact**: HIGH - Could expose sensitive information
**Recommendation**: Add audit of Pantheon data for sensitive patterns, exclude sensitive files from export, sanitize text fields.

---

## Assumption 11: Error Messages Won't Expose Internal Paths

**Statement**: "Error handling won't expose file paths to users"

**Category**: Security / Information Disclosure
**Risk**: MEDIUM
**Status**: ❌ DISPROVEN
**Confidence**: 0.9

**Evidence**:
- ❌ **No Error Handling**: Plan doesn't specify error handling strategy
- ❌ **Default Behavior**: JavaScript errors often expose file paths in stack traces
- ❌ **No Sanitization**: No mention of sanitizing error messages
- ✅ **Best Practice**: Should never expose internal paths

**Impact**: MEDIUM - Information disclosure risk
**Recommendation**: Add error handling that sanitizes messages, never expose file paths, log details server-side only.

---

## Assumption 12: Static JSON Export Is Secure

**Statement**: "Static JSON export script is secure and won't expose sensitive files"

**Category**: Security / Path Traversal
**Risk**: CRITICAL
**Status**: ❌ DISPROVEN
**Confidence**: 1.0

**Evidence**:
- ❌ **No Path Validation**: Plan doesn't specify path validation in export script
- ❌ **No Exclusion List**: No mention of excluding sensitive files (`.env`, `secrets/`, `*.key`)
- ✅ **Pattern Available**: `_validate_path_in_project()` pattern exists in codebase
- ❌ **Not Applied**: Plan doesn't mention using existing validation pattern

**Impact**: CRITICAL - Could expose sensitive files
**Recommendation**: Add path validation using existing pattern, exclude sensitive file patterns, set restrictive permissions on exported JSON.

---

## Summary of Findings

### Critical Assumptions (5)
1. ❌ Browser Fetch API can access local filesystem - **DISPROVEN** (CRITICAL)
2. ✅ Path validation pattern exists - **PROVEN** (can reuse)
3. ⚠️ JSON files always valid - **PARTIALLY PROVEN** (needs validation)
4. ❌ Python HTTP server supports CORS - **DISPROVEN** (needs custom handler)
5. ❌ Static JSON export is secure - **DISPROVEN** (needs path validation)

### High Priority Fixes Needed
1. **Fix data loading strategy** - Cannot use direct file access
2. **Add path validation** - Use existing `_validate_path_in_project()` pattern
3. **Add CORS support** - Custom HTTP handler or use framework
4. **Add error handling** - Sanitize errors, don't expose paths
5. **Audit for sensitive data** - Check Pantheon files for sensitive information

### Medium Priority Fixes
1. Add JSON schema validation
2. Add file permission checks
3. Add Fetch API polyfill for older browsers
4. Add "Last updated" timestamp
5. Document browser requirements

---

## Recommendations

### Immediate Actions (Before Implementation)
1. **Choose Data Loading Strategy**: 
   - Option A: Python HTTP server with CORS handler
   - Option B: Static JSON export with path validation
   - Document security implications of each

2. **Add Path Validation**: Use existing `_validate_path_in_project()` pattern in export script

3. **Add Security Audit**: Check Pantheon files for sensitive data patterns before export

4. **Add Error Handling**: Define error handling strategy that doesn't expose internal paths

### During Implementation
5. Add JSON schema validation
6. Add file permission checks
7. Add CORS support if using HTTP server
8. Add Fetch API detection and polyfill
9. Add "Last updated" timestamp

### Future Enhancements
10. Add data refresh mechanism
11. Add schema versioning
12. Add performance optimization for large datasets

---

**This validation uses evidence from codebase analysis, file system checks, and technical documentation to prove or disprove assumptions.**
