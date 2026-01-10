# Foundation Module Status

**Date:** 2026-01-10
**Status:** Documentation

---

## Overview

The Waft project currently has two foundation modules:
- `src/waft/foundation.py` (1088 lines) - **PRODUCTION**
- `src/waft/foundation_v2.py` (1059 lines) - **EXPERIMENTAL**

This document clarifies their status and usage.

---

## Current Usage

### foundation.py (PRODUCTION)
**Used by:**
- `src/waft/verify_foundation.py` - Foundation verification tests
- `src/waft/generate_artifacts.py` - Artifact generation

**Status:** Active production code

### foundation_v2.py (EXPERIMENTAL)
**Used by:**
- `scripts/generate_foundation_demo.py` - Demo script only

**Status:** Experimental/demonstration code

---

## Key Differences

### foundation.py Features
- RedactionStyle enum
- DocumentConfig dataclass (basic)
- ContentBlock ABC
- SectionHeader, TextBlock, KeyValueBlock, TableBlock
- DocumentEngine class
- `generate_specimen_d_audit()` function

### foundation_v2.py Enhancements
- All foundation.py features PLUS:
- FontFamily enum (NEW)
- FontConfig dataclass (NEW)
- Enhanced DocumentConfig with font support
- CoverPage support (NEW)
- MetadataRail support (NEW)
- RuleBlock support (NEW)
- Improved typography
- `generate_clinical_report_demo()` (vs `generate_specimen_d_audit()`)

---

## Recommendations

### Short-term (Current)
- **Keep both files** as-is to avoid breaking changes
- Document foundation_v2.py as experimental
- Continue using foundation.py for production

### Medium-term (Phase 2-3 Refactoring)
1. Evaluate if foundation_v2 features are needed in production
2. If yes:
   - Migrate `verify_foundation.py` to use foundation_v2
   - Migrate `generate_artifacts.py` to use foundation_v2
   - Add deprecation warning to foundation.py
   - Update all imports
3. If no:
   - Move foundation_v2.py to `scripts/` or `examples/`
   - Document as "advanced example"

### Long-term (Post-refactoring)
- Merge beneficial foundation_v2 features back into foundation.py
- Deprecate and remove foundation_v2.py
- Maintain single canonical implementation

---

## Migration Guide (Future)

If migrating from foundation.py → foundation_v2.py:

### Breaking Changes
- `DocumentConfig` now requires `font_config: FontConfig`
- Function renamed: `generate_specimen_d_audit()` → `generate_clinical_report_demo()`

### Migration Steps
1. Add font configuration:
   ```python
   from waft.foundation_v2 import FontConfig, FontFamily

   font_config = FontConfig(family=FontFamily.HELVETICA)
   ```

2. Update DocumentConfig:
   ```python
   # OLD
   config = DocumentConfig(title="Report")

   # NEW
   config = DocumentConfig(title="Report", font_config=font_config)
   ```

3. Update function calls:
   ```python
   # OLD
   generate_specimen_d_audit()

   # NEW
   generate_clinical_report_demo()
   ```

---

## Decision: Phase 1 Action

For Phase 1 refactoring, we are:
- ✅ Documenting the status (this file)
- ✅ Keeping both files unchanged
- ❌ NOT migrating or removing either file

This preserves stability while documenting technical debt for future resolution.
