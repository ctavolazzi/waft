# Field Guide Booklet - Coordination Notes

**Date:** 2026-01-11  
**Issue:** Two different implementations using different systems

## The Problem

We have two implementations:

1. **Local (Cursor)**: Uses `templates/field_guide.py` (WeasyPrint/HTML) - **PRODUCTION SYSTEM**
2. **Cloud (Claude)**: Uses `foundation_v2.py` (FPDF2/DocumentEngine) - **EXPERIMENTAL SYSTEM**

## System Comparison

### Template System (Production - What I Used)
- **File**: `src/waft/templates/field_guide.py`
- **Technology**: WeasyPrint + HTML + Jinja2
- **Status**: ✅ Production, already working
- **Used by**: `generate_template_showcase.py`, other examples
- **Pros**: Flexible HTML layouts, CSS styling, proven to work
- **Cons**: Requires HTML knowledge

### Foundation V2 System (Experimental - What Claude Used)
- **File**: `src/waft/foundation_v2.py`
- **Technology**: FPDF2 + DocumentEngine blocks
- **Status**: ⚠️ Experimental (per docs/FOUNDATION_STATUS.md)
- **Used by**: `scripts/generate_foundation_demo.py` only
- **Pros**: Programmatic API, type-safe blocks
- **Cons**: Experimental, may not be production-ready

## Decision: Use Template System

**Recommendation**: Use the **template system** (`templates/field_guide.py`) because:
1. It's the production system
2. It's already working and tested
3. It's what other examples use
4. The HTML approach is more flexible for complex layouts

## Action Plan

1. ✅ Keep my implementation using template system
2. ✅ Incorporate Claude's good content ideas
3. ✅ Add Claude's `field_guide()` preset to foundation_v2 for future use (if needed)
4. ✅ Document which system to use going forward

## Content Comparison

Both implementations have similar content structure:
- Level 1: Layman's guide
- Level 2: Professional guide  
- Level 3: ML AI Scientist guide

**My version**: Complete HTML content, uses binder system to combine
**Claude's version**: Block-based API, incomplete (needs PDF merging)

## Going Forward

**For this feature**: Use template system (production)
**For future features**: Check which system is appropriate
**Coordination**: Always check branch status and recent commits before starting work
