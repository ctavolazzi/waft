# Objective Testing Strategy: Testing Assumptions Without Bias

**Created**: 2026-01-04
**Purpose**: How to test assumptions objectively and avoid confirmation bias

---

## The Problem with Biased Testing

**Confirmation Bias:** We tend to write tests that confirm what we want to be true, not what actually is true.

**Example of Biased Test:**
```python
def test_create_structure():
    memory = MemoryManager(Path("/tmp/test"))
    memory.create_structure()
    assert (Path("/tmp/test/_pyrite/active")).exists()  # ✅ Passes - confirms what we want
```

**Problem:** This only tests the happy path. It doesn't test:
- What if filesystem is read-only?
- What if path doesn't exist?
- What if permissions are wrong?
- What if disk is full?

---

## Principles of Objective Testing

### 1. Test Failure Cases First

**Bias:** We test success, assume failure is handled
**Objective:** Test failure explicitly

**Example:**
```python
def test_create_structure_fails_on_readonly_filesystem():
    """Test that create_structure() fails gracefully when filesystem is read-only."""
    # This is hard to test, but we can test the error handling
    memory = MemoryManager(Path("/readonly/path"))
    # Mock or use actual read-only path
    with pytest.raises(PermissionError):
        memory.create_structure()
```

### 2. Test Edge Cases, Not Just Happy Paths

**Bias:** We test normal usage
**Objective:** Test boundaries and edge cases

**Example:**
```python
# Biased: Only tests normal case
def test_get_project_info():
    info = substrate.get_project_info(Path("."))
    assert "name" in info

# Objective: Tests edge cases
def test_get_project_info_missing_file():
    """Test when pyproject.toml doesn't exist."""
    info = substrate.get_project_info(Path("/nonexistent"))
    assert info == {}

def test_get_project_info_invalid_toml():
    """Test when pyproject.toml is malformed."""
    # Create temp file with invalid TOML
    with tempfile.TemporaryDirectory() as tmpdir:
        invalid_toml = Path(tmpdir) / "pyproject.toml"
        invalid_toml.write_text("this is not valid toml [unclosed")
        info = substrate.get_project_info(Path(tmpdir))
        # Should handle gracefully, not crash
        assert isinstance(info, dict)
```

### 3. Use Property-Based Testing

**Bias:** We test specific examples
**Objective:** Test properties that should always hold

**Example with Hypothesis:**
```python
from hypothesis import given, strategies as st

@given(st.text(min_size=1, max_size=100))
def test_parse_toml_field_handles_any_string(project_name):
    """Test that parse_toml_field handles any valid project name."""
    # Create temp TOML with random name
    with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
        f.write(f'name = "{project_name}"\n')
        f.flush()
        result = parse_toml_field(Path(f.name), "name")
        assert result == project_name
```

### 4. Test Invariants

**Bias:** We test outputs match expectations
**Objective:** Test that invariants always hold

**Example:**
```python
def test_verify_structure_invariants():
    """Test that verify_structure() always returns consistent structure."""
    memory = MemoryManager(Path("."))
    result = memory.verify_structure()

    # Invariants that should always hold:
    assert isinstance(result, dict)
    assert "valid" in result
    assert "folders" in result
    assert isinstance(result["valid"], bool)
    assert isinstance(result["folders"], dict)
    assert len(result["folders"]) == 3  # Always 3 folders
    assert all(isinstance(v, bool) for v in result["folders"].values())
```

### 5. Test Error Messages, Not Just Exceptions

**Bias:** We test that exceptions are raised
**Objective:** Test that error messages are helpful

**Example:**
```python
def test_uv_not_found_error_message():
    """Test that error message is helpful when uv is missing."""
    # Mock subprocess to raise FileNotFoundError
    with patch('subprocess.run', side_effect=FileNotFoundError):
        with pytest.raises(SystemExit) as exc_info:
            substrate.init_project("test", Path("/tmp"))
        # Error message should tell user what to do
        assert "uv" in str(exc_info.value).lower()
        assert "install" in str(exc_info.value).lower()
```

### 6. Use Mocks to Control Environment

**Bias:** We test in ideal conditions
**Objective:** Test in controlled, varied conditions

**Example:**
```python
@patch('subprocess.run')
def test_sync_handles_uv_failure(mock_run):
    """Test that sync() handles uv failures gracefully."""
    # Simulate uv failure
    mock_run.side_effect = subprocess.CalledProcessError(1, "uv", "error")

    substrate = SubstrateManager()
    result = substrate.sync(Path("/tmp/test"))

    # Should return False, not crash
    assert result is False
```

### 7. Test State Transitions

**Bias:** We test final state
**Objective:** Test all state transitions

**Example:**
```python
def test_memory_manager_state_transitions():
    """Test all possible state transitions."""
    memory = MemoryManager(Path("/tmp/test"))

    # State 1: No _pyrite
    assert not memory.pyrite_path.exists()
    status1 = memory.verify_structure()
    assert status1["valid"] is False

    # Transition: Create structure
    memory.create_structure()

    # State 2: _pyrite exists
    assert memory.pyrite_path.exists()
    status2 = memory.verify_structure()
    assert status2["valid"] is True

    # Transition: Remove a folder
    (memory.pyrite_path / "active").rmdir()

    # State 3: Invalid structure
    status3 = memory.verify_structure()
    assert status3["valid"] is False
    assert status3["folders"]["_pyrite/active"] is False
```

---

## Testing Framework for Waft

### 1. Unit Tests (Isolated, Fast)

**Purpose:** Test individual functions in isolation
**Tools:** `pytest`, `unittest.mock`

**Example Structure:**
```python
# tests/test_memory.py
def test_create_structure_creates_all_folders():
    """Test that create_structure() creates all required folders."""
    with tempfile.TemporaryDirectory() as tmpdir:
        memory = MemoryManager(Path(tmpdir))
        memory.create_structure()

        # Verify all folders exist
        for folder in MemoryManager.REQUIRED_FOLDERS:
            assert (memory.pyrite_path / folder).exists()
            assert (memory.pyrite_path / folder).is_dir()
```

### 2. Integration Tests (Real Dependencies)

**Purpose:** Test components working together
**Tools:** `pytest`, real file system

**Example:**
```python
# tests/test_integration.py
def test_new_command_creates_complete_project():
    """Test that 'waft new' creates a complete, valid project."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "test_project"

        # Run command
        from waft.main import new
        new("test_project", path=str(tmpdir))

        # Verify complete structure
        assert (project_path / "pyproject.toml").exists()
        assert (project_path / "_pyrite" / "active").exists()
        assert (project_path / "Justfile").exists()

        # Verify it's a valid Waft project
        memory = MemoryManager(project_path)
        assert memory.verify_structure()["valid"] is True
```

### 3. Property-Based Tests (Random Inputs)

**Purpose:** Test with varied inputs automatically
**Tools:** `hypothesis`

**Example:**
```python
from hypothesis import given, strategies as st

@given(
    st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=('L', 'N', '_', '-')))
)
def test_project_name_handling(name):
    """Test that any valid project name works."""
    # Test that we can parse it back
    toml_content = f'name = "{name}"\nversion = "0.1.0"'
    with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
        f.write(toml_content)
        f.flush()
        result = parse_toml_field(Path(f.name), "name")
        assert result == name
```

### 4. Error Injection Tests (Force Failures)

**Purpose:** Test error handling paths
**Tools:** `pytest`, `unittest.mock`

**Example:**
```python
@patch('pathlib.Path.mkdir')
def test_create_structure_handles_permission_error(mock_mkdir):
    """Test that create_structure() handles permission errors."""
    mock_mkdir.side_effect = PermissionError("Permission denied")

    memory = MemoryManager(Path("/tmp/test"))

    # Should raise or handle gracefully
    with pytest.raises(PermissionError):
        memory.create_structure()
```

### 5. Fuzz Testing (Random Malformed Input)

**Purpose:** Test with invalid/corrupted data
**Tools:** `hypothesis`, custom fuzzers

**Example:**
```python
@given(st.binary(min_size=0, max_size=1000))
def test_parse_toml_field_handles_binary_data(data):
    """Test that parse_toml_field() handles binary data gracefully."""
    with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
        f.write(data)
        f.flush()
        # Should not crash, should return None or handle gracefully
        result = parse_toml_field(Path(f.name), "name")
        assert result is None or isinstance(result, str)
```

---

## Specific Tests for Waft Assumptions

### Assumption 1: `uv` command exists

**Objective Test:**
```python
def test_uv_missing_handles_gracefully():
    """Test that missing uv command is handled gracefully."""
    with patch('subprocess.run', side_effect=FileNotFoundError):
        substrate = SubstrateManager()
        result = substrate.init_project("test", Path("/tmp"))
        # Should return False, not crash
        assert result is False

def test_uv_command_works():
    """Test that uv command actually works (integration test)."""
    # This requires uv to be installed
    substrate = SubstrateManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        result = substrate.init_project("test", Path(tmpdir))
        assert result is True
        assert (Path(tmpdir) / "test" / "pyproject.toml").exists()
```

### Assumption 2: File system is writable

**Objective Test:**
```python
@patch('pathlib.Path.mkdir')
def test_create_structure_handles_readonly_filesystem(mock_mkdir):
    """Test that create_structure() handles read-only filesystem."""
    mock_mkdir.side_effect = PermissionError("Read-only filesystem")

    memory = MemoryManager(Path("/readonly"))
    with pytest.raises(PermissionError):
        memory.create_structure()

def test_create_structure_handles_disk_full():
    """Test that create_structure() handles disk full scenario."""
    with patch('pathlib.Path.mkdir', side_effect=OSError(28, "No space left on device")):
        memory = MemoryManager(Path("/tmp"))
        with pytest.raises(OSError):
            memory.create_structure()
```

### Assumption 3: TOML parsing with regex

**Objective Test:**
```python
def test_parse_toml_field_handles_complex_toml():
    """Test that parse_toml_field() handles complex TOML."""
    complex_toml = """
    name = "project"
    version = "0.1.0"
    description = "A project with 'quotes' and \"double quotes\"
    [tool.something]
    nested = { value = "test" }
    """
    with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
        f.write(complex_toml)
        f.flush()
        # Should still extract name correctly
        result = parse_toml_field(Path(f.name), "name")
        assert result == "project"

def test_parse_toml_field_handles_multiline_strings():
    """Test that parse_toml_field() handles multiline strings."""
    multiline_toml = '''
    name = """
    multi
    line
    name
    """
    '''
    with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
        f.write(multiline_toml)
        f.flush()
        # Regex might fail here - this test will reveal the assumption
        result = parse_toml_field(Path(f.name), "name")
        # If this fails, we know our assumption is wrong
```

### Assumption 4: Subprocess error handling

**Objective Test:**
```python
def test_subprocess_error_handling_variations():
    """Test that we handle different subprocess error formats."""
    error_variations = [
        ("already initialized", True),
        ("already exists", True),
        ("permission denied", False),
        ("", False),  # Empty error
    ]

    for error_msg, should_succeed in error_variations:
        with patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, "uv", error_msg)):
            substrate = SubstrateManager()
            result = substrate.init_project("test", Path("/tmp"))
            assert result is should_succeed, f"Failed for error: {error_msg}"
```

---

## Testing Checklist for Each Assumption

For each assumption, test:

- [ ] **Happy path** - Does it work in ideal conditions?
- [ ] **Failure case** - What happens when it fails?
- [ ] **Edge cases** - Boundaries, empty inputs, max inputs
- [ ] **Error messages** - Are they helpful?
- [ ] **State transitions** - All possible states
- [ ] **Invariants** - Properties that always hold
- [ ] **Integration** - Works with real dependencies
- [ ] **Performance** - Doesn't hang or use too much memory

---

## Tools for Objective Testing

### 1. pytest
- Fixtures for setup/teardown
- Parametrized tests for multiple inputs
- Markers for test categories

### 2. hypothesis
- Property-based testing
- Generates test cases automatically
- Finds edge cases we wouldn't think of

### 3. unittest.mock
- Mock external dependencies
- Control test environment
- Test error conditions

### 4. coverage
- Measure what we're actually testing
- Find untested code paths
- Ensure we test error handling

---

## The Testing Strategy

### Phase 1: Test Critical Assumptions (High Risk)
1. `uv` command exists and works
2. File system operations
3. TOML parsing edge cases
4. Error handling

### Phase 2: Test All Assumptions
1. Document all assumptions
2. Write tests for each
3. Run tests in CI

### Phase 3: Continuous Testing
1. Run tests on every change
2. Add tests for new assumptions
3. Update tests when assumptions change

---

## Example Test Structure

```
tests/
├── conftest.py           # Shared fixtures
├── test_memory.py        # MemoryManager tests
├── test_substrate.py     # SubstrateManager tests
├── test_templates.py     # TemplateWriter tests
├── test_main.py          # CLI command tests
├── test_utils.py         # Utility function tests
├── test_integration.py   # Integration tests
└── test_properties.py    # Property-based tests
```

---

## Key Principle

**Test what could go wrong, not just what should go right.**

Every assumption is a potential failure point. Test it.

