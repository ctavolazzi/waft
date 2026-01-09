---
id: TKT-sec1-002
parent: WE-260109-sec1
title: "Add comprehensive input validation to subprocess calls"
status: open
priority: CRITICAL
created: 2026-01-09T00:00:00.000Z
created_by: claude_audit
assigned_to: null
---

# TKT-sec1-002: Add comprehensive input validation to subprocess calls

## Metadata
- **Created**: Thursday, January 9, 2026
- **Parent Work Effort**: WE-260109-sec1
- **Author**: Claude Audit System
- **Priority**: CRITICAL
- **Estimated Effort**: 3 tickets (moderate complexity)

## Description

Multiple subprocess calls across 21 files pass user-controlled input without comprehensive validation. While list-based arguments mitigate some risks, edge cases and shell metacharacters could still cause issues.

## Problem Examples

### substrate.py:52 - Project name to uv
```python
subprocess.run(["uv", "init", "--name", name, "--no-readme"], ...)
```

**Risk**: If `name` contains special chars or spaces, could cause unexpected behavior.

### empirica.py:272 - User findings to subprocess
```python
subprocess.run([...] + ["--finding", finding, "--impact", str(impact)], ...)
```

**Risk**: `finding` is user-provided text, needs validation.

### session_stats.py:44-50 - Git commands
```python
subprocess.run(["git", "diff", "--numstat", "HEAD"], ...)
```

**Risk**: Currently safe, but relies on implicit trust of git safety.

## Current Mitigation

**Partial Protection**:
- ✅ Uses list-based arguments (not shell=True)
- ✅ Some validation exists (utils.py:75 for project names)
- ⚠️ Not comprehensive across all call sites
- ❌ No centralized validation layer

## Acceptance Criteria

- [ ] All subprocess calls validated through centralized layer
- [ ] Allowlist validation for project/package names
- [ ] Use `shlex.quote()` for any string interpolation
- [ ] Security tests cover injection attempts
- [ ] Documentation on safe subprocess usage

## Implementation Plan

### Step 1: Create Validation Layer
Create `src/waft/core/subprocess_validator.py`:

```python
"""
Centralized subprocess input validation.
Prevents command injection and validates all external input.
"""

import re
import shlex
from typing import List, Optional

class SubprocessValidator:
    """Validates inputs before passing to subprocess calls."""

    # Allowlists
    PROJECT_NAME_PATTERN = re.compile(r'^[a-zA-Z0-9_-]+$')
    PACKAGE_NAME_PATTERN = re.compile(r'^[a-zA-Z0-9_\-\.]+$')

    @classmethod
    def validate_project_name(cls, name: str) -> str:
        """Validate and sanitize project name."""
        if not name or len(name) > 100:
            raise ValueError("Invalid project name length")
        if not cls.PROJECT_NAME_PATTERN.match(name):
            raise ValueError("Project name contains invalid characters")
        return name

    @classmethod
    def validate_package_name(cls, name: str) -> str:
        """Validate and sanitize package name."""
        if not name or len(name) > 200:
            raise ValueError("Invalid package name length")
        if not cls.PACKAGE_NAME_PATTERN.match(name):
            raise ValueError("Package name contains invalid characters")
        return name

    @classmethod
    def quote_if_needed(cls, value: str) -> str:
        """Quote string if it contains special characters."""
        return shlex.quote(value)

    @classmethod
    def validate_finding_text(cls, text: str, max_length: int = 10000) -> str:
        """Validate user-provided finding text."""
        if not text:
            raise ValueError("Finding text cannot be empty")
        if len(text) > max_length:
            raise ValueError(f"Finding text exceeds {max_length} characters")
        # Remove null bytes and other dangerous chars
        text = text.replace('\0', '')
        return text
```

### Step 2: Update All Subprocess Calls

Update each file to use validator:

**substrate.py**:
```python
from .subprocess_validator import SubprocessValidator

def init_project(self, name: str):
    validated_name = SubprocessValidator.validate_project_name(name)
    subprocess.run(["uv", "init", "--name", validated_name, ...])
```

**empirica.py**:
```python
from .subprocess_validator import SubprocessValidator

def log_finding(self, finding: str, impact: int):
    validated_finding = SubprocessValidator.validate_finding_text(finding)
    subprocess.run([...] + ["--finding", validated_finding, ...])
```

### Step 3: Add Security Tests

Extend `big_bad_wolf.py` or create `tests/test_subprocess_security.py`:

```python
def test_command_injection_attempts():
    """Test that command injection is blocked."""
    injection_attempts = [
        "project; rm -rf /",
        "project`whoami`",
        "project$(ls)",
        "project & echo hacked",
        "project\nrm -rf /",
    ]

    for malicious_input in injection_attempts:
        with pytest.raises(ValueError):
            SubprocessValidator.validate_project_name(malicious_input)
```

## Files to Change

**Core**:
- `src/waft/core/subprocess_validator.py` (NEW)
- `src/waft/core/substrate.py` (update subprocess calls)
- `src/waft/core/empirica.py` (update subprocess calls)
- `src/waft/utils.py` (migrate validation logic)

**Tests**:
- `tests/test_subprocess_security.py` (NEW)
- `big_bad_wolf.py` (extend with subprocess tests)

**Files with subprocess.run()** (21 total - audit each):
- substrate.py
- empirica.py
- session_stats.py
- github.py
- (17 more - see audit report)

## Testing Strategy

1. **Unit Tests**: Test validator in isolation
2. **Integration Tests**: Test actual subprocess calls with validated input
3. **Security Tests**: Attempt injection attacks (should be blocked)
4. **Regression Tests**: Ensure valid inputs still work

## Related Issues

- Audit Finding: "Command Injection Risks (CRITICAL)"
- Files affected: 21 files with subprocess.run()
- Existing security test: big_bad_wolf.py (decision engine attacks)

## Commits

- (populated as work progresses)
