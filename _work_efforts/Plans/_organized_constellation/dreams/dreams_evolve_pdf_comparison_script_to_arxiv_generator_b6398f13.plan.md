---
name: Evolve PDF Comparison Script to ArXiv Generator
overview: Transform the comparison script from generating 3 comparison PDFs to generating a single ArXiv-ready academic paper PDF using the existing academic paper template, with automatic metadata extraction from markdown.
todos: []

category: dreams
confidence: 0.53
constellation_date: 2026-01-14
---

# Evolve PDF Comparison Script to ArXiv-Ready Generator

## Objective

Transform `examples/generate_all_pdfs_comparison.py` from a comparison tool (generates 3 PDFs) into an ArXiv-ready academic paper generator that produces a single publication-quality PDF similar to `world_models.pdf`.

## Current State

- Script generates 3 PDFs using ReportLab, WeasyPrint, and Jinja2+WeasyPrint for comparison
- Uses basic markdown-to-PDF conversion
- Outputs to `_temp_pdf_samples/` directory
- No academic formatting or metadata extraction

## Target State

- Single ArXiv-ready PDF using the academic paper template
- Automatic metadata extraction (title, abstract, authors, affiliations, references)
- Two-column academic layout matching ArXiv standards
- Professional typography (Times New Roman, proper spacing)
- Output similar to `world_models.pdf` format

## Implementation Plan

### 1. Refactor Script Structure

**File**: `examples/generate_all_pdfs_comparison.py`

- Remove the 3-way comparison logic
- Replace with single ArXiv PDF generation path
- Use `src/waft/templates/academic_paper.py` as the generation engine
- Keep markdown input file support

### 2. Add Metadata Extraction

**New Function**: `extract_arxiv_metadata(md_content: str) -> dict`

Extract from markdown frontmatter or structured format:

- **Title**: First `# Title` or frontmatter `title:`
- **Abstract**: Section starting with `## Abstract` or frontmatter `abstract:`
- **Authors**: Frontmatter `authors:` (list or comma-separated)
- **Affiliations**: Frontmatter `affiliations:` (list)
- **Email**: Frontmatter `email:`
- **References**: Section starting with `## References` or `## References` list
- **Year**: Current year (default) or frontmatter `year:`

**Pattern Matching**:

```python
# Look for frontmatter (YAML-style)
# Or structured markdown sections
# Or extract from first H1, Abstract section, etc.
```

### 3. Content Processing

**Function**: `process_markdown_content(md_content: str, metadata: dict) -> str`

- Convert markdown to HTML using `markdown` library with extensions
- Remove frontmatter/metadata sections from content
- Remove Abstract section (will be in template)
- Remove References section (will be in template)
- Preserve code blocks, tables, lists, formatting
- Handle HTML-in-markdown gracefully (use golden_triangle if needed)

### 4. Integrate Academic Paper Template

**Function**: `generate_arxiv_pdf(md_file: Path, output_path: Path) -> Path`

- Import `generate_academic_paper` from `src.waft.templates.academic_paper`
- Extract metadata from markdown
- Process content (remove metadata sections)
- Convert markdown content to HTML
- Call `generate_academic_paper()` with:
  - title
  - content (HTML)
  - abstract
  - authors (list of dicts with 'name' key)
  - affiliations (list of strings)
  - email
  - conference="arXiv"
  - year
  - references (list of strings)

### 5. Update Main Function

**Changes to `main()`**:

- Single PDF generation instead of 3
- Output path: `world_models.pdf` (or configurable)
- Better error handling
- Progress messages
- File size reporting
- Optional: Open PDF after generation

### 6. Handle Edge Cases

- Missing abstract: Extract first paragraph or generate placeholder
- Missing authors: Use default or extract from markdown
- No references: Empty list (template handles gracefully)
- HTML in markdown: Use golden_triangle conversion if needed
- Large documents: Ensure proper page breaks

### 7. Output Location

- Default: `world_models.pdf` in project root (matching user's example)
- Or: `_temp_pdf_samples/[filename]_arxiv.pdf`
- Make configurable via command-line argument

## Files to Modify

1. **`examples/generate_all_pdfs_comparison.py`**

   - Complete rewrite to use academic paper template
   - Add metadata extraction functions
   - Add content processing functions
   - Update main() function

## Files to Reference (No Changes)

1. **`src/waft/templates/academic_paper.py`**

   - Already has `generate_academic_paper()` function
   - Two-column layout, ArXiv formatting
   - Handles all academic paper requirements

2. **`_science/reports/waft_arxiv_paper.md`**

   - Example of ArXiv paper structure
   - Shows metadata format

3. **`world_models.pdf`**

   - Target output format reference

## Testing

1. Test with `_temp_pdf_samples/session_recap_2026-01-12.md`
2. Test with `_temp_pdf_samples/dnd_preflight_world_models.md` (has structured format)
3. Test with minimal markdown (no metadata)
4. Verify output matches ArXiv standards:

   - Two-column layout
   - Proper typography
   - Abstract section
   - References section
   - Page numbers
   - Conference header

## Success Criteria

- ✅ Single ArXiv-ready PDF generated
- ✅ Metadata extracted correctly from markdown
- ✅ Two-column academic layout
- ✅ Professional typography (Times New Roman, proper spacing)
- ✅ Abstract, authors, references properly formatted
- ✅ Output similar to `world_models.pdf` format
- ✅ Ready for ArXiv submission

## Implementation Notes

- Keep script simple and focused
- Reuse existing academic paper template (don't duplicate)
- Handle missing metadata gracefully (use defaults)
- Support both frontmatter and section-based metadata extraction
- Ensure HTML conversion preserves formatting