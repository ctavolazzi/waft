---
id: TKT-75vp-002
parent: WE-260113-75vp
title: "Document HannaCLIEngine JSON game file schema and structure"
status: completed
created: 2026-01-13T08:26:24.193Z
completed: 2026-01-13T09:00:00.000Z
created_by: ctavolazzi
assigned_to: null
---

# TKT-75vp-002: Document HannaCLIEngine JSON game file schema and structure

## Metadata
- **Created**: Tuesday, January 13, 2026 at 12:26:24 AM PST
- **Completed**: Tuesday, January 13, 2026 at 1:00:00 AM PST
- **Parent Work Effort**: WE-260113-75vp
- **Author**: ctavolazzi

## Description
Document the complete JSON game file schema and structure used by HannaCLIEngine, including all field definitions, data types, and example structures.

## Acceptance Criteria
- [x] Top-level game file structure documented
- [x] Sequence structure documented with all fields
- [x] Choice structure documented with all types
- [x] Container system documented
- [x] Example JSON structures provided
- [x] Schema documented in architecture analysis document

## Files Changed
- `HANNA_CLI_ENGINE_ARCHITECTURE_ANALYSIS.md` - JSON schema section (lines 39-128)

## Implementation Notes

### Schema Documentation Location
The complete JSON schema is documented in `HANNA_CLI_ENGINE_ARCHITECTURE_ANALYSIS.md` under the "JSON Game File Structure" section.

### Documented Components

1. **Top-Level Structure**:
   - `gameTitle` (string) - Game title
   - `gameAuthor` (string) - Author name
   - `gameDesc` (string) - Game description
   - `startSq` (string) - Starting sequence ID
   - `gameContainers` (array of strings) - Container names
   - `sequences` (array) - Sequence objects

2. **Sequence Structure**:
   - `sqId` (string) - Unique sequence identifier
   - `sqType` (string) - "ordinary" or "end"
   - `mainText` (string) - Primary narrative text
   - `secondaryText` (string) - Secondary prompt text
   - `choices` (array) - Choice objects

3. **Choice Structure**:
   - `choiceLetter` (string) - Choice identifier (A, B, C, D)
   - `choiceType` (string) - "set" or "conditional"
   - `choiceText` (string) - Display text for choice
   - `outcomeText` (string) - Text shown after choice
   - `choiceCondition` (object, optional) - Conditional display logic
     - `container` (string) - Container to check
     - `value` (string) - Value that must exist
   - `containerAdd` (object, optional) - Container modification
     - `container` (string) - Container to modify
     - `value` (string) - Value to add
   - `nextSq` (string) - Next sequence ID

4. **Container System**:
   - Named collections of string values
   - Initialized as empty vectors
   - Values added via `containerAdd` in choices
   - Used for conditional choice display

### Example Structures
Complete example JSON structures are provided in the architecture analysis document, including:
- Full game file example
- Sequence examples
- Choice examples (set and conditional types)
- Container usage examples

### Source Code References
Schema derived from C++ source code:
- `HannaCLIEngine.h` - `loadGameFile()` method (lines 60-117)
- `game.cpp` - Processing logic

## Commits
- (work in progress, not yet committed)
