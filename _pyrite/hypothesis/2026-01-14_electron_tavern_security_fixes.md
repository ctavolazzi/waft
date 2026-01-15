# Hypothesis: Electron Tavern Game Display Security Fixes

**Date**: 2026-01-14 20:22:22
**Status**: Initial
**Confidence**: High
**Related Work**: CRITIQUE_2026-01-14_202222_electron_tavern_game_display.md

---

## Statement

The Electron Tavern Game Display plan can be made secure and robust by applying existing codebase patterns for subprocess security, async state locking, and serialization, while adding missing validation and error handling.

---

## Context

A critique identified CRITICAL security vulnerabilities in the plan:
1. Command injection risk in launch script
2. Race conditions in game state management
3. Missing input validation
4. Missing error handling

The codebase already has established patterns for these concerns that can be applied.

---

## Evidence Supporting

### Strong Evidence
- **Subprocess Security Patterns Exist**: Work effort WE-260109-sec1 provides guidelines for safe subprocess usage, avoiding shell=True and using list arguments
- **Async Locking Patterns**: `src/waft/core/now_cycle.py` demonstrates `asyncio.Lock()` usage in FastAPI async endpoints
- **Serialization Method Exists**: `DnD5eCharacter.to_dict()` method exists and handles enum conversion
- **CORS Patterns**: `src/waft/api/main.py` shows CORS configuration for localhost origins

### Moderate Evidence
- **Port Checking**: No existing code checks port availability, but socket module can be used
- **Command Validation**: No existing code validates npm, but `which` command can check availability

---

## Evidence Contradicting

- **Computed Properties**: `DnD5eCharacter.to_dict()` doesn't include @property modifiers (str_modifier, AC, etc.) - needs enhancement
- **Error Handling**: Existing FastAPI endpoints have minimal error handling - need to add comprehensive try/except

---

## Verification Plan

### Method 1: Code Pattern Analysis
- **What**: Verify existing patterns can be applied
- **How**: Review codebase for subprocess, locking, and serialization patterns
- **Expected**: Patterns exist and are applicable
- **Status**: ✅ Complete

### Method 2: Port Availability Check
- **What**: Verify port 8765 is available
- **How**: Use socket.connect_ex() to test port
- **Expected**: Port is available (or provide fallback)
- **Status**: [ ] In Progress

### Method 3: npm Availability Check
- **What**: Verify npm command exists
- **How**: Use `which npm` command
- **Expected**: npm is available (or provide clear error)
- **Status**: [ ] In Progress

### Method 4: Serialization Test
- **What**: Test DnD5eCharacter serialization with computed properties
- **How**: Create test character, serialize, verify all fields
- **Expected**: Serialization works but needs computed properties added
- **Status**: [ ] Not Started

---

## Predictions

### If Hypothesis is True
- We can fix all CRITICAL issues using existing patterns
- Implementation will be secure and robust
- Code will follow established codebase conventions
- Fixes will be straightforward to implement

### If Hypothesis is False
- Existing patterns won't cover all security concerns
- Need to create new security mechanisms
- Implementation will require more custom code
- Fixes will be more complex

---

## Confidence Assessment

**Current Confidence**: High (0.85)

**Reasoning**:
- Strong evidence that patterns exist for most concerns
- Only minor gaps (computed properties, port checking) need to be addressed
- Codebase has established security practices (WE-260109-sec1)
- FastAPI async patterns are well-established

**What Would Increase Confidence**:
- Successful implementation of fixes
- Passing security tests
- Code review approval

**What Would Decrease Confidence**:
- Patterns don't work for this use case
- Additional security issues discovered
- Performance problems with locking

**Last Updated**: 2026-01-14 20:22:22

---

## Next Steps

1. Apply subprocess security patterns from WE-260109-sec1
2. Implement asyncio.Lock() for game state (pattern from NowCycleManager)
3. Enhance DnD5eCharacter serialization to include computed properties
4. Add port availability checking before server startup
5. Add npm command validation in launch script
6. Add comprehensive error handling to all endpoints
7. Add input validation with Pydantic models

---

## Related Documentation

- [Critique Report](_work_efforts/CRITIQUE_2026-01-14_202222_electron_tavern_game_display.md)
- [Assumptions Validation](_work_efforts/ASSUMPTIONS_VALIDATION_2026-01-14_202222_electron_tavern.md)
- [Subprocess Security Work Effort](_work_efforts/WE-260109-sec1_critical_security_portability/)

---

**Hypothesis Created**: 2026-01-14 20:22:22
**Last Updated**: 2026-01-14 20:22:22