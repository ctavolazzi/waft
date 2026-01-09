---
id: TKT-sec1-001
parent: WE-260109-sec1
title: "Fix hardcoded absolute path in .empirica/config.yaml"
status: open
priority: CRITICAL
created: 2026-01-09T00:00:00.000Z
created_by: claude_audit
assigned_to: null
---

# TKT-sec1-001: Fix hardcoded absolute path in .empirica/config.yaml

## Metadata
- **Created**: Thursday, January 9, 2026
- **Parent Work Effort**: WE-260109-sec1
- **Author**: Claude Audit System
- **Priority**: CRITICAL
- **Estimated Effort**: 1 ticket (simple config fix)

## Description

The file `.empirica/config.yaml` contains a hardcoded absolute path that breaks portability:

```yaml
root: /Users/ctavolazzi/Code/active/waft/.empirica
```

This causes the project to fail on any machine except the developer's Mac. The path must be made relative or use environment variables.

## Problem Impact

**Severity**: CRITICAL ❌
- Project completely broken on Linux/Windows
- Breaks on any Mac without matching directory structure
- Committed to git, affects all users
- Violates basic portability principles

## Root Cause

Configuration file uses developer's personal absolute path instead of:
1. Relative paths (`.empirica/`)
2. Environment variables (`$EMPIRICA_ROOT`)
3. Runtime detection

## Acceptance Criteria

- [ ] `.empirica/config.yaml` uses relative paths or env vars
- [ ] Config works on Linux, Mac, Windows
- [ ] No hardcoded absolute paths remain in any config
- [ ] Tests pass on multiple platforms
- [ ] Documentation updated if env vars required

## Implementation Options

### Option 1: Relative Paths (Recommended)
```yaml
root: .empirica
paths:
  sessions: sessions/sessions.db
  identity: identity/
  # etc.
```

### Option 2: Environment Variables
```yaml
root: ${EMPIRICA_ROOT:-.empirica}  # Default to .empirica if not set
```

### Option 3: Runtime Detection
- Detect project root at runtime
- Build absolute path dynamically
- Never commit absolute paths

## Files to Change

- `.empirica/config.yaml` - Primary fix
- `src/waft/core/empirica.py` (lines 46-61) - May need path resolution updates
- Tests - Verify portability

## Testing Strategy

1. **Local Testing**: Remove `.empirica/` and recreate with new config
2. **Cross-Platform**: Test on Linux container
3. **Fresh Clone**: Clone repo in different location, verify works
4. **CI**: Ensure GitHub Actions passes (already runs on ubuntu-latest)

## Related Issues

- Audit Finding: "Hardcoded Python Version Detection" in empirica.py:46-61
- Also uses absolute paths to Python frameworks on Mac

## Commits

- (populated as work progresses)
