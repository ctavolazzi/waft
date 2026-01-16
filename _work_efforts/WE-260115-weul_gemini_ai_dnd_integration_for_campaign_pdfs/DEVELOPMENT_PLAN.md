# Development Plan: Gemini AI-DnD Integration

**Work Effort**: WE-260115-weul  
**Date**: 2026-01-15  
**Status**: In Progress

## Overview

Integrate the Gemini narrative engine from AI-DnD project into WAFT to enhance D&D campaign PDF generation with AI-powered storytelling.

## Architecture

```
AI-DnD Project
  └── gemini_narrative_engine.py
        │
        │ (copy & adapt)
        ↓
WAFT Project
  └── src/waft/campaign/
        ├── gemini_narrative_engine.py  (adapted)
        └── gemini_pdf_adapter.py        (new bridge)
              │
              │ (integration)
              ↓
      PDF Generator
        └── Enhanced campaign PDFs with AI narrative
```

## Implementation Steps

### Step 1: Copy and Adapt Gemini Engine

**Source**: `/Users/ctavolazzi/Code/active/AI-DnD/gemini_narrative_engine.py`  
**Target**: `src/waft/campaign/gemini_narrative_engine.py`

**Tasks**:
1. Copy the file to WAFT structure
2. Update imports to match WAFT conventions
3. Ensure environment variable handling works with WAFT's config
4. Test basic initialization

**Key Adaptations**:
- Update import paths
- Align with WAFT's logging system
- Ensure compatibility with WAFT's async patterns
- Add WAFT-specific error handling

### Step 2: Create PDF Integration Adapter

**New File**: `src/waft/campaign/gemini_pdf_adapter.py`

**Purpose**: Bridge between Gemini narrative engine and PDF generation

**Interface Design**:
```python
class GeminiPDFAdapter:
    """Adapter to integrate Gemini narrative engine with PDF generation"""
    
    async def enhance_campaign_narrative(
        self, 
        campaign_data: dict,
        context: NarrativeContext
    ) -> str:
        """Generate AI-enhanced narrative for campaign PDF"""
        
    async def enhance_character_description(
        self,
        character: dict,
        context: NarrativeContext
    ) -> str:
        """Generate AI-enhanced character description"""
        
    async def generate_story_chapter(
        self,
        chapter_data: dict,
        context: NarrativeContext
    ) -> str:
        """Generate AI-powered story chapter content"""
```

### Step 3: Integrate with PDF Generation

**Modified File**: `examples/generate_dnd_campaign_pdfs.py`

**Enhancements**:
- Add `--use-gemini` flag
- Integrate Gemini adapter into PDF generation workflow
- Enhance campaign content with AI-generated narrative
- Add fallback when Gemini unavailable

### Step 4: Testing

**New File**: `examples/test_gemini_campaign_pdf.py`

**Test Cases**:
1. Test Gemini engine initialization
2. Test narrative generation
3. Test PDF generation with Gemini enhancement
4. Test fallback when API unavailable
5. End-to-end campaign PDF generation

## Integration Points

### With Existing Systems

1. **PDF Generator** (`src/waft/evolution/pdf_generator.py`)
   - Add optional Gemini enhancement parameter
   - Integrate narrative content into PDF structure

2. **Campaign System** (`src/waft/campaign/`)
   - Use Gemini for dynamic narrative generation
   - Enhance campaign chapters with AI content

3. **Work Effort WE-260113-wfbu** (AI DM System)
   - Can leverage Gemini for DM narrative generation
   - Enhance story booklets with AI content

## Configuration

### Environment Variables
- `GEMINI_API_KEY` - Required for Gemini API access
- `GEMINI_MODEL` - Optional, defaults to `gemini-3-pro-preview`
- `GEMINI_THINKING_LEVEL` - Optional, defaults to `high`

### Dependencies
```python
# Add to requirements.txt or setup
google-genai  # Gemini API client
```

## Success Criteria

- ✅ Gemini engine successfully copied and adapted
- ✅ PDF adapter created and functional
- ✅ Campaign PDFs enhanced with AI narrative
- ✅ Fallback works when Gemini unavailable
- ✅ Sample PDFs generated successfully
- ✅ Documentation complete

## Next Steps

1. Copy `gemini_narrative_engine.py` from AI-DnD
2. Adapt for WAFT structure
3. Create PDF adapter
4. Integrate with existing PDF generation
5. Test and document
