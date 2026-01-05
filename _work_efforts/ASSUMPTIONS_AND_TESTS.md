# Assumptions and Tests: The Honest Assessment

**Created**: 2026-01-04
**Purpose**: Identify what we assume and whether we test it

---

## Do We Have Tests?

**NO. We have ZERO tests.**

**Evidence:**
- ❌ No `tests/` directory
- ❌ No `test_*.py` files (except `test_server.py` which is not a test)
- ❌ `pytest` is in dev dependencies but unused
- ❌ We've mentioned tests 20+ times but never written them

**What We Have:**
- ✅ Manual testing (EXPERIMENTAL_FINDINGS.md)
- ✅ `pytest` installed but not used
- ✅ Test projects in `_experiments/` (manual validation)

---

## Are We Aware of Our Assumptions?

**PARTIALLY. We have assumptions but they're not documented or tested.**

---

## Our Assumptions (Identified from Code)

### 1. External Dependencies

**Assumption:** `uv` command exists and is available
**Location:** `SubstrateManager` - all methods call `uv`
**Risk:** HIGH - Framework won't work without `uv`
**Tested:** ❌ NO
**Code:**
```python
subprocess.run(["uv", "init", ...])  # Assumes uv exists
```

**Assumption:** `uv` command works correctly
**Location:** All `SubstrateManager` methods
**Risk:** HIGH - If `uv` fails, framework fails
**Tested:** ❌ NO

---

### 2. File System Assumptions

**Assumption:** Project paths are valid and writable
**Location:** `MemoryManager.create_structure()`, all file operations
**Risk:** MEDIUM - Could fail on read-only filesystems
**Tested:** ❌ NO
**Code:**
```python
self.project_path.mkdir(parents=True, exist_ok=True)  # Assumes writable
```

**Assumption:** File system operations will succeed
**Location:** All file I/O operations
**Risk:** MEDIUM - Disk full, permissions, etc.
**Tested:** ❌ NO

**Assumption:** Directories can be created with `mkdir(parents=True)`
**Location:** `MemoryManager`, `TemplateWriter`
**Risk:** LOW - Standard Python, but edge cases exist
**Tested:** ❌ NO

---

### 3. Project Structure Assumptions

**Assumption:** `_pyrite/` structure is exactly 3 folders (active, backlog, standards)
**Location:** `MemoryManager.REQUIRED_FOLDERS`
**Risk:** LOW - Hardcoded, but what if user wants more?
**Tested:** ❌ NO
**Code:**
```python
REQUIRED_FOLDERS = ["active", "backlog", "standards"]  # Assumes exactly 3
```

**Assumption:** `.gitkeep` files should be ignored when listing files
**Location:** All `get_*_files()` methods
**Risk:** LOW - Design decision, but what if user wants to see them?
**Tested:** ❌ NO
**Code:**
```python
if f.name != ".gitkeep"  # Assumes we always ignore .gitkeep
```

**Assumption:** `pyproject.toml` exists or can be created
**Location:** `SubstrateManager.init_project()`, `get_project_info()`
**Risk:** MEDIUM - Core functionality depends on this
**Tested:** ❌ NO

---

### 4. Data Format Assumptions

**Assumption:** TOML parsing with regex is sufficient
**Location:** `SubstrateManager.get_project_info()`, `parse_toml_field()`
**Risk:** MEDIUM - Regex can break on complex TOML
**Tested:** ❌ NO
**Code:**
```python
re.search(r'name\s*=\s*["\']([^"\']+)["\']', content)  # Assumes simple TOML
```

**Assumption:** `pyproject.toml` has simple format (no multiline strings, etc.)
**Location:** `parse_toml_field()`
**Risk:** MEDIUM - Complex TOML will break
**Tested:** ❌ NO

**Assumption:** File content is text (not binary)
**Location:** All `read_text()` calls
**Risk:** LOW - We control file creation, but user files could be binary
**Tested:** ❌ NO

---

### 5. Path Assumptions

**Assumption:** Paths are valid Python `Path` objects
**Location:** All path operations
**Risk:** LOW - Type hints help, but runtime could pass wrong type
**Tested:** ❌ NO

**Assumption:** Paths are relative to project root or absolute
**Location:** All path operations
**Risk:** LOW - Standard usage, but edge cases exist
**Tested:** ❌ NO

---

### 6. Subprocess Assumptions

**Assumption:** `subprocess.run()` will work
**Location:** All `SubstrateManager` methods
**Risk:** LOW - Standard library, but could fail
**Tested:** ❌ NO

**Assumption:** `uv` commands return expected output
**Location:** `SubstrateManager` methods
**Risk:** MEDIUM - If `uv` changes, we break
**Tested:** ❌ NO

**Assumption:** Error handling for subprocess is correct
**Location:** `SubstrateManager.init_project()`
**Risk:** MEDIUM - We catch some errors, but miss others
**Tested:** ❌ NO
**Code:**
```python
except subprocess.CalledProcessError as e:
    if "already initialized" in e.stderr.lower():  # Assumes error message format
        return True
```

---

### 7. Template Assumptions

**Assumption:** Templates won't overwrite existing files
**Location:** `TemplateWriter` - all `write_*()` methods check `exists()`
**Risk:** LOW - We check, but what if file is created between check and write?
**Tested:** ❌ NO
**Code:**
```python
if justfile_path.exists():
    return  # Assumes no race condition
```

**Assumption:** Template content is correct
**Location:** All template methods
**Risk:** LOW - We control templates, but typos possible
**Tested:** ❌ NO

---

### 8. Web Server Assumptions

**Assumption:** Port is available
**Location:** `waft serve`
**Risk:** MEDIUM - Could fail if port in use
**Tested:** ❌ NO (we catch OSError but don't test it)

**Assumption:** HTTP server works correctly
**Location:** `web.py`
**Risk:** LOW - Standard library, but edge cases exist
**Tested:** ❌ NO

---

## Critical Assumptions (High Risk, No Tests)

1. **`uv` command exists** - Framework won't work without it
2. **File system is writable** - Core functionality depends on this
3. **TOML parsing with regex** - Could break on complex TOML
4. **Subprocess error handling** - Assumes specific error message formats

---

## What We Should Test

### High Priority Tests

1. **External Dependencies**
   - Test that `uv` is available
   - Test graceful failure when `uv` is missing
   - Mock `uv` commands for testing

2. **File System Operations**
   - Test with read-only filesystem
   - Test with invalid paths
   - Test with insufficient permissions
   - Test with full disk (if possible)

3. **Project Structure**
   - Test `create_structure()` creates correct folders
   - Test `verify_structure()` with various states
   - Test file listing methods

4. **TOML Parsing**
   - Test with simple TOML
   - Test with complex TOML (multiline, arrays, etc.)
   - Test with invalid TOML
   - Test edge cases

5. **Subprocess Handling**
   - Test success cases
   - Test failure cases
   - Test error message parsing
   - Test timeout scenarios

6. **Template Generation**
   - Test all templates are created
   - Test existing files aren't overwritten
   - Test template content is correct

---

## The Gap

**We Have:**
- ✅ Code that works (manually tested)
- ✅ Assumptions embedded in code
- ✅ `pytest` installed
- ✅ Manual test results

**We Don't Have:**
- ❌ Automated tests
- ❌ Documented assumptions
- ❌ Tests that verify assumptions
- ❌ Confidence in edge cases

**The Problem:**
- We assume things will work
- We don't verify those assumptions
- We don't know what will break
- We can't refactor safely

---

## What We Need

### 1. Document Assumptions
- List all assumptions
- Rate risk level
- Document expected behavior

### 2. Write Tests
- Test happy paths
- Test error cases
- Test edge cases
- Test assumptions

### 3. Test Infrastructure
- Set up `tests/` directory
- Create fixtures
- Mock external dependencies
- Run tests in CI

---

## The Honest Answer

**Do we have tests?** NO.

**Are we aware of assumptions?** PARTIALLY - we have them but don't document or test them.

**What should we do?**
1. Document all assumptions (this doc is a start)
2. Write tests for critical assumptions
3. Set up test infrastructure
4. Run tests automatically

**Priority:** HIGH - We're building on assumptions we haven't verified.

