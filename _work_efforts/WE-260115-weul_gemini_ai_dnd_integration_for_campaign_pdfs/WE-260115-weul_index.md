---
id: WE-260115-weul
title: "Gemini AI-DnD Integration for D&D Campaign PDFs"
status: active
created: 2026-01-15T00:01:41.000Z
created_by: ctavolazzi
last_updated: 2026-01-15T00:01:41.000Z
branch: feature/WE-260115-weul-gemini-ai-dnd-integration
repository: waft
---

# WE-260115-weul: Gemini AI-DnD Integration for D&D Campaign PDFs

## Metadata
- **Created**: Thursday, January 15, 2026 at 12:01:41 AM PST
- **Author**: ctavolazzi
- **Repository**: waft
- **Branch**: feature/WE-260115-weul-gemini-ai-dnd-integration

## Objective
Integrate the Gemini API narrative engine from the AI-DnD project (`/Users/ctavolazzi/Code/active/AI-DnD`) into WAFT to enhance D&D campaign PDF generation with AI-powered narrative content. This will enable rich, dynamic storytelling in campaign PDFs using Gemini's narrative generation capabilities.

## Context
- **Source Project**: `/Users/ctavolazzi/Code/active/AI-DnD`
- **Key Files**:
  - `gemini_narrative_engine.py` - Main Gemini narrative engine
  - `gemini_enhanced_character_generator.py` - Character generation with Gemini
- **Target Integration**: WAFT's D&D campaign PDF generation system
- **Related Work Efforts**:
  - `WE-260112-jqkn` - D&D Campaign PDF Evolution
  - `WE-260113-wfbu` - AI DM System (can be enhanced with Gemini)

## Goals
1. ✅ Copy/adapt Gemini narrative engine from AI-DnD to WAFT
2. ⏳ Create adapter/bridge to connect Gemini engine with PDF generation
3. ⏳ Enhance campaign PDFs with AI-generated narrative content
4. ⏳ Test integration and verify PDF quality improvements
5. ⏳ Document integration and usage patterns

## Progress
- 1/15/2026: Work effort created. Starting integration planning.

## Implementation Plan

### Phase 1: Copy and Adapt Gemini Engine
- [x] Copy `gemini_narrative_engine.py` from AI-DnD to WAFT
- [x] Adapt imports and dependencies for WAFT structure
- [x] Ensure API key configuration works with WAFT's env system
- [x] Add graceful fallback when Gemini unavailable

### Phase 2: Create Integration Adapter
- [ ] Create adapter module to bridge Gemini engine with PDF generator
- [ ] Design interface for narrative content generation
- [ ] Integrate with existing campaign PDF generation workflow
- [ ] Handle fallback when Gemini unavailable

### Phase 3: Enhance PDF Generation
- [ ] Add AI-generated narrative sections to campaign PDFs
- [ ] Enhance character descriptions with Gemini
- [ ] Generate dynamic story content for campaign chapters
- [ ] Add NPC behavior and dialogue generation

### Phase 4: Testing and Documentation
- [ ] Test complete workflow end-to-end
- [ ] Generate sample campaign PDFs with Gemini enhancement
- [ ] Document integration patterns and usage
- [ ] Update related work efforts

## Files to Create/Modify

### New Files
- ✅ `src/waft/campaign/gemini_narrative_engine.py` - Adapted Gemini engine
- ✅ `src/waft/campaign/gemini_pdf_adapter.py` - Bridge between Gemini and PDF generation
- ✅ `src/waft/campaign/__init__.py` - Module initialization
- ✅ `examples/test_gemini_campaign_pdf.py` - Test script

### Modified Files
- `src/waft/evolution/pdf_generator.py` - Add Gemini integration option
- `examples/generate_dnd_campaign_pdfs.py` - Add Gemini enhancement option

## Dependencies
- Google Gemini API (`google-genai` package)
- Existing WAFT PDF generation system
- Campaign state management (from WE-260113-wfbu)

## Related
- Source: `/Users/ctavolazzi/Code/active/AI-DnD/gemini_narrative_engine.py`
- Related Work Efforts:
  - `WE-260112-jqkn` - D&D Campaign PDF Evolution
  - `WE-260113-wfbu` - AI DM System
- PDF Generator: `src/waft/evolution/pdf_generator.py`
