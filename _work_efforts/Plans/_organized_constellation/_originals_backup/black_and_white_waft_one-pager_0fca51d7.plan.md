---
name: Black and White WAFT One-Pager
overview: Create a beautiful black and white one-pager about WAFT for first-time viewers, addressing all critique findings with proper error handling, validation, and using existing TwoPageGenerator infrastructure.
todos:
  - id: "1"
    content: Create enhanced script with grayscale ColorGene configuration
    status: completed
  - id: "2"
    content: Add comprehensive error handling (WeasyPrint, file I/O, PDF generation)
    status: completed
  - id: "3"
    content: Add output validation (file existence, page count, structure, size)
    status: completed
  - id: "4"
    content: Add input validation (content, paths, styling parameters)
    status: completed
  - id: "5"
    content: Add edge case handling (empty content, very long/short content, special characters)
    status: completed
  - id: "6"
    content: Add CLI interface with argparse (--output, --content, --verbose, --validate-only)
    status: completed
  - id: "7"
    content: Add logging and observability (INFO, WARNING, ERROR, DEBUG levels)
    status: completed
  - id: "8"
    content: Add cross-platform support (detect platform, use webbrowser module)
    status: completed
  - id: "9"
    content: Design beautiful grayscale template (typography hierarchy, spacing, borders)
    status: completed
  - id: "10"
    content: Add metadata and versioning (timestamp, script version, genome ID in footer)
    status: completed
---

# Black and White WAFT One-Pager Implementation Plan

## Objective

Create a beautiful, printer-friendly black and white one-pager introducing WAFT to first-time viewers. The document must be exactly 2 pages, use only grayscale colors (black, white, grays), and include comprehensive error handling and validation.

## Context Analysis

### Existing Infrastructure

- **TwoPageGenerator** (`src/waft/evolution/two_page_generator.py`): Handles 2-page constraint enforcement with adaptive content selection
- **ColorGene** (`src/waft/evolution/styling_genome.py`): Manages color schemes - can be configured for grayscale
- **ChatDistiller**: Extracts ideas from content
- **StylingGenomeRegistry**: Manages styling genomes
- **Existing script** (`examples/generate_waft_intro_one_pager.py`): Creates colored intro one-pager - can be adapted

### Critique Findings (Must Address)

1. **HIGH**: No error handling for PDF generation failures
2. **HIGH**: No validation of output quality
3. **MEDIUM**: Assumes WeasyPrint installed
4. **MEDIUM**: Assumes filesystem writable
5. **MEDIUM**: No input validation
6. **MEDIUM**: No edge case handling
7. **LOW**: Missing CLI interface
8. **LOW**: No logging/observability

## Implementation Approach

### Option Selected: Modify Existing Script with Enhancements

**Rationale**:

- Reuses proven TwoPageGenerator infrastructure
- Leverages existing content distillation
- Faster implementation
- Addresses all critique findings

## Implementation Steps

### Step 1: Create Enhanced Script with Error Handling

**File**: `examples/generate_waft_intro_one_pager_bw.py`

**Key Features**:

1. **Dependency Checking**: Verify WeasyPrint, pypdf, jinja2 at startup
2. **Error Handling**: Wrap all operations in try/except with graceful degradation
3. **Input Validation**: Validate content, paths, styling parameters
4. **Output Validation**: Verify PDF exists, is readable, has correct page count
5. **Logging**: Add structured logging for debugging
6. **Cleanup**: Guaranteed temp file cleanup using context managers

**Grayscale ColorGene Configuration**:

```python
color=ColorGene(
    text="#000000",        # Pure black text
    background="#FFFFFF",  # Pure white background
    heading="#000000",     # Black headings
    accent="#333333",      # Dark gray for accents (not pure black for subtlety)
    code_bg="#f5f5f5",    # Light gray for code blocks
    code_text="#000000",   # Black code text
    border="#000000",      # Black borders
)
```

### Step 2: Add Comprehensive Error Handling

**Pattern**: Use context managers and try/except blocks

**Error Handling Points**:

1. **WeasyPrint Import**: Check availability, provide clear error if missing
2. **PDF Generation**: Handle font errors, memory errors, rendering failures
3. **File I/O**: Handle permission errors, disk full, network filesystem issues
4. **Directory Creation**: Handle permission errors gracefully
5. **Temp File Cleanup**: Use `tempfile.TemporaryDirectory` context manager
6. **Page Counting**: Handle PDF reading errors

**Fallback Strategy**:

- If PDF generation fails: Generate HTML output instead
- If WeasyPrint missing: Provide installation instructions
- If filesystem read-only: Skip registry writes, continue with generation

### Step 3: Add Output Validation

**Validation Checks**:

1. **File Existence**: Verify PDF file created and is readable
2. **Page Count**: Validate exactly 2 pages (not 1, not 3+)
3. **File Size**: Check not empty, not suspiciously small (< 10KB)
4. **PDF Structure**: Use pypdf to verify PDF is not corrupted
5. **Content Verification**: Optional - extract text to verify content present

**Validation Report**: Print validation results to console

### Step 4: Add Input Validation

**Validation Points**:

1. **Content**: Check not empty, reasonable length (100-5000 words)
2. **Output Path**: Validate path is writable, parent directory exists
3. **Styling Parameters**: Validate font sizes in reasonable ranges (8-24pt)
4. **Margin Values**: Validate margins are positive and reasonable (5-50mm)

### Step 5: Add Edge Case Handling

**Edge Cases to Handle**:

1. **Empty Content**: Error with helpful message
2. **Very Long Content**: Use adaptive selection (already in TwoPageGenerator)
3. **Very Short Content**: Warn if content might not fill 2 pages
4. **Special Characters**: Ensure UTF-8 encoding throughout
5. **Concurrent Execution**: Handle file locking if multiple instances run

### Step 6: Add CLI Interface

**Using argparse**:

- `--output`: Custom output path (default: `_work_efforts/one_pagers/WAFT_Intro_BW_[timestamp].pdf`)
- `--content`: Optional custom content file (default: use built-in WAFT explanation)
- `--verbose`: Enable verbose logging
- `--validate-only`: Only validate, don't generate
- `--help`: Show usage

**Make Executable**: Add `#!/usr/bin/env python3` shebang

### Step 7: Add Logging and Observability

**Logging Levels**:

- **INFO**: Normal operations (generation start, completion)
- **WARNING**: Non-fatal issues (fallbacks used, assumptions made)
- **ERROR**: Failures (with context for debugging)
- **DEBUG**: Detailed operations (only with --verbose)

**Log Format**: Structured with timestamps, operation context

### Step 8: Add Cross-Platform Support

**Platform Detection**:

- Detect macOS/Linux/Windows
- Use `webbrowser` module for opening PDF (cross-platform)
- Make PDF opening optional (flag)

### Step 9: Create Beautiful Grayscale Design

**Design Principles**:

1. **Typography Hierarchy**: Use font sizes and weights, not colors
2. **Spacing**: Generous whitespace for elegance
3. **Borders**: Black borders for structure (not colored)
4. **Shading**: Use grayscale gradients (light gray to dark gray) for depth
5. **Visual Elements**: Boxes, dividers, tables with black borders

**Template Enhancements**:

- Remove all color references from template
- Use grayscale palette: #000000, #333333, #666666, #999999, #CCCCCC, #F5F5F5, #FFFFFF
- Ensure high contrast for readability
- Use typography for visual interest (bold, italic, sizes)

### Step 10: Add Metadata and Versioning

**PDF Metadata**:

- Add generation timestamp to footer
- Add script version
- Add generator genome ID (for lineage tracking)
- Add "Black & White Edition" label

## File Structure

### New Files

- `examples/generate_waft_intro_one_pager_bw.py`: Main script with all enhancements

### Modified Files

- None (standalone script)

### Output Files

- `_work_efforts/one_pagers/WAFT_Intro_BW_[timestamp].pdf`: Generated PDF
- `_work_efforts/one_pagers/WAFT_Intro_BW_[timestamp].html`: HTML version (for debugging)

## Testing Strategy

### Unit Tests (Future)

- Test dependency checking
- Test error handling paths
- Test validation functions
- Test grayscale color conversion

### Manual Testing

1. **Happy Path**: Generate with default settings
2. **Missing Dependencies**: Test with WeasyPrint uninstalled
3. **Read-Only Filesystem**: Test with read-only directory
4. **Invalid Input**: Test with empty content, invalid paths
5. **Edge Cases**: Very long content, very short content

## Success Criteria

1. ✅ Generates exactly 2-page PDF
2. ✅ Uses only black, white, and grays
3. ✅ Beautiful, elegant design suitable for first-time viewers
4. ✅ Handles all error cases gracefully
5. ✅ Validates output quality
6. ✅ Provides clear error messages
7. ✅ Works cross-platform
8. ✅ Includes CLI interface
9. ✅ Logs operations appropriately
10. ✅ Cleans up temporary files

## Risk Mitigation

### Risk 1: Content Doesn't Fit in 2 Pages

**Mitigation**: TwoPageGenerator already handles this with adaptive selection

### Risk 2: WeasyPrint Fails

**Mitigation**: Fallback to HTML output, clear error message

### Risk 3: Filesystem Issues

**Mitigation**: Check permissions, provide helpful error messages

### Risk 4: Design Not Beautiful

**Mitigation**: Iterate on design, test with sample output, get feedback

## Dependencies

- **Required**: weasyprint, pypdf, jinja2 (already in project)
- **Python**: 3.10+ (check at startup)
- **System**: Fonts available for WeasyPrint (handle gracefully if missing)

## Timeline Estimate

- **Step 1-3** (Core script + error handling): 2 hours
- **Step 4-5** (Validation + edge cases): 1 hour
- **Step 6-7** (CLI + logging): 1 hour
- **Step 8** (Cross-platform): 30 minutes
- **Step 9** (Design refinement): 1-2 hours
- **Step 10** (Metadata): 30 minutes
- **Testing**: 1 hour

**Total**: ~6-7 hours

## Next Steps After Implementation

1. Test on multiple platforms
2. Get user feedback on design
3. Refine based on feedback
4. Consider adding to main CLI (`waft one-pager --bw`)
5. Document usage in README