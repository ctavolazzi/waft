---
id: WE-260109-sec1
title: "Critical Security & Portability Fixes"
status: open
priority: CRITICAL
created: 2026-01-09T00:00:00.000Z
created_by: claude_audit
last_updated: 2026-01-09T00:00:00.000Z
branch: claude/explore-waft-UugBV
repository: waft
---

# WE-260109-sec1: Critical Security & Portability Fixes

## Metadata
- **Created**: Thursday, January 9, 2026
- **Author**: Claude Audit System
- **Repository**: waft
- **Branch**: claude/explore-waft-UugBV
- **Priority**: CRITICAL

## Objective

Fix critical security vulnerabilities and portability issues discovered during comprehensive codebase audit. These issues prevent the project from working on different machines and expose potential security risks.

## Audit Context

Comprehensive audit of all 49 Python files (12,731 LOC) revealed:
- Hardcoded absolute paths breaking portability
- Command injection risks in subprocess calls
- 546 lines of legacy dead code
- Missing input validation on critical paths

## Tickets

| ID | Title | Status | Priority |
|----|-------|--------|----------|
| TKT-sec1-001 | Fix hardcoded absolute path in .empirica/config.yaml | open | CRITICAL |
| TKT-sec1-002 | Add comprehensive input validation to subprocess calls | open | CRITICAL |
| TKT-sec1-003 | Delete legacy web.py (546 lines dead code) | open | HIGH |
| TKT-sec1-004 | Add security tests for input validation | open | HIGH |
| TKT-sec1-005 | Audit and fix all subprocess.run() calls (21 files) | open | HIGH |

## Impact Assessment

**Current Risk**: HIGH
- Project breaks on any machine except developer's Mac
- Potential command injection in user-facing commands
- Dead code creates confusion and maintenance burden

**Post-Fix Risk**: LOW
- Portable across all platforms
- Input validation prevents injection attacks
- Clean codebase

## Success Criteria

- [ ] Project works on Linux, Mac, Windows
- [ ] All subprocess calls have input validation
- [ ] No dead code remains
- [ ] Security tests pass
- [ ] `waft verify` passes on all platforms

## Related

- Audit Report: Created 2026-01-09
- Security: big_bad_wolf.py (existing security test suite)
- Architecture: Subprocess usage across 21 files

## Notes

This work effort addresses the most critical findings from the comprehensive audit. These issues must be fixed before any feature work continues, as they represent fundamental flaws in portability and security.
