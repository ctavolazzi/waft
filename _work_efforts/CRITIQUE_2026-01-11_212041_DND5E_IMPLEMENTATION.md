# Adversarial Plan Critique: D&D 5e Physics Engine Implementation

**Date**: 2026-01-11
**Time**: 21:20:41
**Plan**: D&D 5e Physics Engine for WAFT Beings
**Critique Mode**: Bad Faith / Adversarial

---

## Executive Summary

**CRITICAL Security Vulnerabilities**: 0
**HIGH Safety Issues**: 2
**MEDIUM Unexamined Assumptions**: 7
**LOW Overengineering**: 2
**Oversights**: 5
**Missed Obviousness**: 3

**Overall Assessment**: This plan is relatively safe from a security perspective (no code execution, no file system access), but has several unexamined assumptions that could cause failures. The plan is well-structured but missing critical details about state persistence, error handling, and integration points.

---

## 🔴 HIGH: Safety Issues

### 1. No Input Validation on Ability Scores
**Issue**: The plan doesn't specify validation for ability scores. What happens if someone passes `strength: -5` or `strength: 999`?

**Attack Vector**: Malformed state data could cause:
- Integer overflow in calculations
- Negative modifiers breaking game logic
- Extremely high scores breaking balance

**Impact**: Game mechanics could break, calculations could produce invalid results

**Severity**: HIGH

**Fix Required**:
- Add validation: `if not (1 <= score <= 30): raise ValueError("Ability score must be 1-30")`
- Add bounds checking in all calculation functions
- Validate on character creation and state loading

### 2. No Error Handling for Dice Rolling Failures
**Issue**: The `d20` library could fail (malformed expressions, library errors). What happens then?

**Attack Vector**: 
- Malformed dice expressions: `"2d20xyz"` could crash
- Library import failures if `d20` not installed (even though it's in dependencies)
- Network issues if library tries to fetch updates

**Impact**: Unhandled exceptions could crash Being operations

**Severity**: HIGH

**Fix Required**:
- Wrap all `d20.roll()` calls in try/except
- Validate dice expressions before passing to library
- Provide fallback behavior (e.g., return 0, log error, continue)
- Check library availability at module import

---

## ⚠️ MEDIUM: Unexamined Assumptions

### 1. Assumes `d20` Library is Installed and Working
**Issue**: Plan assumes `d20>=1.0.0` is available, but what if:
- Installation failed silently?
- Version conflict?
- Library has bugs?
- Import fails?

**Impact**: Module import could fail, breaking entire D&D system

**Severity**: MEDIUM

**Fix Required**:
- Check library availability at module import
- Provide clear error message if missing
- Consider fallback dice implementation (though this defeats the purpose)

### 2. Assumes Being State Can Be Extended
**Issue**: Plan says "add optional `dnd5e_character` field" but doesn't check:
- Is Being class frozen/immutable?
- Are there serialization constraints?
- Will this break existing Being instances?
- Does state persistence handle new fields?

**Impact**: Integration could fail silently or break existing Beings

**Severity**: MEDIUM

**Fix Required**:
- Verify Being class can be extended
- Check state serialization/deserialization handles new fields
- Test backward compatibility (Beings without D&D stats)
- Add migration path for existing Beings

### 3. Assumes State Schema Can Be Modified
**Issue**: Plan mentions updating `{being_id}_state.json` but doesn't address:
- What if state file is locked?
- What if JSON is malformed?
- What if file doesn't exist?
- What if permissions are wrong?

**Impact**: State persistence could fail, losing D&D stats

**Severity**: MEDIUM

**Fix Required**:
- Add error handling for file I/O
- Validate JSON structure before writing
- Handle missing files gracefully
- Check file permissions

### 4. Assumes Integer Division Behavior
**Issue**: Modifier calculation uses `(score - 10) // 2`. Assumes:
- Python 3 integer division (floor division)
- Negative scores handled correctly (they're not - negative scores would produce wrong modifiers)
- No floating point issues

**Impact**: Calculations could be wrong for edge cases

**Severity**: MEDIUM

**Fix Required**:
- Document integer division behavior
- Test negative scores (should be rejected, not calculated)
- Verify floor division works as expected

### 5. Assumes Armor Types Are Validated
**Issue**: AC calculation uses `armor_type` string but doesn't validate:
- What if `armor_type = "invalid"`?
- What if `armor_type = None`?
- What if `armor_type = ""` (empty string)?

**Impact**: AC calculation could return wrong values or crash

**Severity**: MEDIUM

**Fix Required**:
- Validate armor_type against allowed values: `["none", "light", "medium", "heavy"]`
- Use Enum for armor types instead of strings
- Provide default behavior for invalid types

### 6. Assumes Level is Always Positive
**Issue**: Proficiency bonus calculation uses `level` but doesn't check:
- What if `level = 0`? (returns +1, which is wrong)
- What if `level = -5`? (returns +0, which is wrong)
- What if `level = 999`? (returns +251, which breaks game balance)

**Impact**: Proficiency bonus could be wrong, breaking game balance

**Severity**: MEDIUM

**Fix Required**:
- Validate level: `if not (1 <= level <= 20): raise ValueError("Level must be 1-20")`
- Cap proficiency bonus at +6 (level 17-20)
- Handle epic levels (>20) separately if needed

### 7. Assumes Properties Don't Have Side Effects
**Issue**: Plan uses `@property` decorators for derived values (modifiers, AC). Assumes:
- Properties are fast (no expensive calculations)
- Properties don't modify state
- Properties are idempotent

**Impact**: Performance issues if properties are expensive, state corruption if they modify state

**Severity**: MEDIUM

**Fix Required**:
- Document that properties are pure calculations
- Don't modify state in properties
- Consider caching if calculations become expensive

---

## ⚠️ LOW: Overengineering

### 1. Separate Module for Each Component
**Issue**: Plan creates 6 separate files (`stats.py`, `dice.py`, `character.py`, `adapter.py`, `combat.py`, `__init__.py`). For initial implementation, this might be overkill.

**Impact**: More files to maintain, more imports, more coordination

**Severity**: LOW

**Fix Consideration**: Could start with fewer files, combine related functionality. But this is actually good architecture - separation of concerns is valuable.

### 2. Adapter Pattern May Be Premature
**Issue**: The adapter pattern for 4-stat to 6-stat conversion is planned, but:
- Is it needed immediately?
- Do we have any 4-stat systems to adapt?
- Could this be added later?

**Impact**: Unnecessary complexity if not needed

**Severity**: LOW

**Fix Consideration**: Mark adapter as "future" or "optional" - implement only if needed. This is actually fine - the plan already marks some things as "future".

---

## ⚠️ Oversights

### 1. No Error Handling Strategy
**Issue**: Plan doesn't mention error handling approach:
- What happens if calculation fails?
- How are errors logged?
- Should errors be silent or raise exceptions?
- How do errors affect Being operations?

**Impact**: Unclear error behavior, potential crashes

**Severity**: MEDIUM

**Fix Required**:
- Define error handling strategy
- Add try/except blocks where needed
- Log errors appropriately
- Decide on error propagation (raise vs return None vs default values)

### 2. No Testing Strategy
**Issue**: Plan mentions "Testing Strategy" section but it's marked as "Future". No unit tests planned for initial implementation.

**Impact**: Untested code, potential bugs, no verification

**Severity**: MEDIUM

**Fix Required**:
- Write tests alongside implementation (TDD approach)
- Test all calculation functions
- Test edge cases (boundary conditions)
- Test integration with Being class

### 3. No Migration Path for Existing Beings
**Issue**: Plan doesn't address how to add D&D stats to existing Beings:
- Do they get default stats?
- Do they get stats based on existing attributes?
- Is migration automatic or manual?

**Impact**: Existing Beings might not have D&D stats, breaking compatibility

**Severity**: MEDIUM

**Fix Required**:
- Define migration strategy
- Create migration function
- Handle Beings without D&D stats gracefully
- Document migration process

### 4. No Performance Considerations
**Issue**: Plan doesn't mention performance:
- Are property calculations fast enough?
- Should modifiers be cached?
- What about large numbers of Beings?

**Impact**: Performance issues if calculations are expensive or called frequently

**Severity**: LOW

**Fix Consideration**: Profile if performance becomes an issue. For initial implementation, this is probably fine.

### 5. No Documentation Plan
**Issue**: Plan doesn't mention documentation:
- API documentation?
- Usage examples?
- Algorithm explanations?
- Integration guide?

**Impact**: Unclear how to use the module, poor developer experience

**Severity**: LOW

**Fix Required**:
- Add docstrings to all functions
- Create usage examples
- Document algorithm formulas
- Write integration guide

---

## ⚠️ Missed Obviousness

### 1. No Type Hints in Plan Examples
**Issue**: Code examples in plan don't show type hints, but project uses Python 3.10+ which supports modern type hints.

**Impact**: Less clear API, no IDE support, potential type errors

**Severity**: LOW

**Fix Required**: Add type hints to all function signatures in implementation

### 2. No Enum for Constants
**Issue**: Plan uses string literals for armor types (`"none"`, `"light"`, etc.) but doesn't mention using Enum.

**Impact**: Typos possible, no IDE autocomplete, harder to refactor

**Severity**: LOW

**Fix Required**: Use Enum for armor types, ability scores, etc.

### 3. No Validation of Dice Expressions
**Issue**: Plan uses `d20.roll(expression)` but doesn't validate expressions before passing to library.

**Impact**: Malformed expressions could crash or produce wrong results

**Severity**: MEDIUM

**Fix Required**: Validate dice expressions (regex or library validation) before rolling

---

## Additional Adversarial Findings

### Failure Modes
- **Library Import Failure**: If `d20` import fails, entire module breaks
- **State File Corruption**: If JSON is corrupted, D&D stats could be lost
- **Circular Dependencies**: If `character.py` imports `stats.py` and `stats.py` imports `character.py`, import fails
- **Memory Issues**: If many Beings have D&D stats, memory usage could be high

### Attack Vectors
- **Malformed State Data**: Attacker could craft malicious JSON with extreme values
- **Dice Expression Injection**: If expressions come from user input, could cause issues
- **State File Manipulation**: If state files are writable, could be tampered with

### Edge Cases
- **Level 0 Beings**: What if a Being has level 0? (shouldn't happen, but what if?)
- **Negative Ability Scores**: What if score is negative? (should be rejected)
- **Floating Point Scores**: What if score is 15.5? (should be integer)
- **Missing Equipment**: What if `equipped_weapon` is set but weapon doesn't exist?

### Integration Issues
- **Breaking Changes**: Adding D&D stats could break existing code that expects certain Being structure
- **State Schema Versioning**: How do we handle schema changes? Version the schema?
- **Backward Compatibility**: Existing Beings without D&D stats need to work

---

## Recommendations (Prioritized)

### Priority 1: HIGH - Fix Before Implementation
1. **Add Input Validation**: Validate all ability scores (1-30), levels (1-20), armor types
2. **Add Error Handling**: Wrap dice rolling in try/except, handle library failures
3. **Add Type Hints**: Use modern Python type hints throughout
4. **Use Enums**: Replace string literals with Enum for armor types, ability scores

### Priority 2: MEDIUM - Fix During Implementation
5. **Add Testing**: Write unit tests alongside implementation
6. **Add Error Handling Strategy**: Define how errors are handled (raise vs return None)
7. **Add Migration Path**: Handle existing Beings without D&D stats
8. **Add State Validation**: Validate JSON structure, handle missing files
9. **Add Documentation**: Docstrings, examples, integration guide

### Priority 3: LOW - Consider for Future
10. **Performance Optimization**: Profile if needed, add caching if expensive
11. **Adapter Pattern**: Implement only if 4-stat systems exist
12. **Comprehensive Combat**: Expand combat.py only if needed

---

## Conclusion

This plan is **relatively safe** from a security perspective - no code execution, no file system traversal, no network access. However, it has **several unexamined assumptions** that could cause failures:

1. **Input validation is missing** - ability scores, levels, armor types need validation
2. **Error handling is unclear** - no strategy for handling failures
3. **State integration is assumed** - need to verify Being class can be extended
4. **Testing is deferred** - should write tests alongside implementation

The plan is well-structured and follows good practices (separation of concerns, clear phases), but needs more detail on:
- Error handling
- Input validation
- State integration
- Testing strategy

**Recommendation**: Address HIGH priority items before implementation. The plan is solid but needs hardening around edge cases and error handling.

---

**This critique assumes the worst and looks for all the ways things could fail. Address these issues before implementation.**
