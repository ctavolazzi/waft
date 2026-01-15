---
name: Scint Core Implementation
overview: Replace the existing scint.py implementation with the user's ontological design for Scint detection, including ScintType enum, Scint dataclass, RealityAnchor ABC, and RegexScintDetector with exception-based detection.
todos:
  - id: "1"
    content: "Update imports: Add ABC and abstractmethod from abc module"
    status: completed
  - id: "2"
    content: Replace ScintType enum (ensure 4 types match specification)
    status: completed
  - id: "3"
    content: Replace Scint dataclass with frozen=True, __str__(), and get_stat_category()
    status: completed
  - id: "4"
    content: Replace RealityAnchor as ABC with abstract scan() method
    status: completed
  - id: "5"
    content: "Replace RegexScintDetector: instance-based with patterns dict keyed by ScintType"
    status: completed
  - id: "6"
    content: Implement detect_from_exception() as instance method (primary entry point)
    status: completed
  - id: "7"
    content: Implement _get_type_from_error() for exception classification
    status: completed
  - id: "8"
    content: Implement _calculate_severity() with base severity + difficulty boost
    status: completed
  - id: "9"
    content: Implement _get_correction_hint() with type-specific hints
    status: completed
  - id: "10"
    content: Add get_max_severity() static method helper
    status: completed

category: hopes
confidence: 0.43
constellation_date: 2026-01-14
---

# Scint Core Implementation Plan

## Objective

Replace the current `src/gym/rpg/scint.py` implementation with the ontological design that treats AI errors as "reality fractures" (Scints), implementing the core detection framework.

## Current State

- File exists at `src/gym/rpg/scint.py` with a different implementation
- Current implementation uses class-level patterns and classmethod for `detect_from_exception`
- Missing ABC for `RealityAnchor`
- Different severity calculation and pattern structure

## Implementation Steps

### 1. Replace Core Definitions

**File**: `src/gym/rpg/scint.py`

**Changes**:

- Keep the module docstring (philosophical foundation)
- Replace `ScintType` enum (ensure 4 types: SYNTAX_TEAR, LOGIC_FRACTURE, SAFETY_VOID, HALLUCINATION)
- Replace `Scint` dataclass with:
  - Frozen dataclass (immutable)
  - `__str__()` method for human-readable output
  - `get_stat_category()` method mapping to INT/WIS/CHA
- Replace `RealityAnchor` as abstract base class:
  - Import `ABC` and `abstractmethod` from `abc`
  - Make `scan()` abstract
- Replace `RegexScintDetector` implementation:
  - Instance-based (not classmethod)
  - Pattern dictionary keyed by `ScintType` (not string keys)
  - `scan()` method for text scanning
  - `detect_from_exception()` as primary instance method
  - `_get_type_from_error()` for exception classification
  - `_calculate_severity()` with base severity + difficulty boost
  - `_get_correction_hint()` with type-specific hints
  - `get_max_severity()` as static method

### 2. Key Implementation Details

**Pattern Structure**:

```python
self.patterns = {
    ScintType.SYNTAX_TEAR: [re.compile(...), ...],
    ScintType.LOGIC_FRACTURE: [re.compile(...), ...],
    ScintType.SAFETY_VOID: [re.compile(...), ...]
}
```

**Exception Classification** (`_get_type_from_error`):

- `json.JSONDecodeError` → `SYNTAX_TEAR`
- `KeyError`, `ValueError`, `TypeError` → `LOGIC_FRACTURE`
- Fallback: pattern matching on error message
- Default: `LOGIC_FRACTURE`

**Severity Calculation**:

- Base severities: SYNTAX_TEAR=0.3, LOGIC_FRACTURE=0.5, HALLUCINATION=0.6, SAFETY_VOID=0.9
- Difficulty boost: `(difficulty - 1) * 0.1`
- Capped at 1.0

**Correction Hints**:

- SYNTAX_TEAR: "Ensure output is valid JSON. Fix quotes, braces, and commas."
- LOGIC_FRACTURE: Schema violations or logic errors with specific guidance
- SAFETY_VOID: "Content violated safety constraints. Rephrase to be helpful and harmless."
- Default fallback hint

### 3. Dependencies

- `enum.Enum, auto` - Already imported
- `dataclasses.dataclass` - Already imported
- `typing.List, Optional, Pattern, Dict, Any` - Add `Any` if needed
- `re` - Already imported
- `json` - For `JSONDecodeError` detection
- `abc.ABC, abstractmethod` - **NEW** - Need to import

### 4. Testing Considerations

- Verify `Scint` is immutable (frozen dataclass)
- Test `get_stat_category()` returns correct stat (INT/WIS/CHA)
- Test `detect_from_exception()` with various exception types
- Test severity calculation with different difficulty levels
- Test pattern matching for each ScintType
- Verify `get_max_severity()` handles empty lists

### 5. Integration Points

- `game_master.py` will use `RegexScintDetector.detect_from_exception()` when exceptions occur
- `models.py` may reference Scint types for stat updates
- Future: StabilizationLoop will use Scints for correction

## Files to Modify

1. `src/gym/rpg/scint.py` - Complete replacement with new implementation

## Validation

- Import statements are correct
- All methods match the provided signature
- Pattern matching logic is correct
- Severity calculation matches specification
- Stat category mapping is correct (SYNTAX_TEAR→CHA, SAFETY_VOID→WIS, others→INT)

## Notes

- This is Step 1 of the Scint integration plan
- The implementation treats errors as ontological "reality fractures"
- Design aligns with Reflexion, Chain of Verification, and Constitutional AI research patterns
- Foundation for future StabilizationLoop implementation