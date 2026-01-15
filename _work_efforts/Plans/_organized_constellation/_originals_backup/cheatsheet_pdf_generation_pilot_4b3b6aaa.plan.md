---
name: Cheatsheet PDF Generation Pilot
overview: Generate professional PDFs from selected GitHub cheatsheet repositories using WAFT's PDF generation tools. Start with 2-3 repositories as a pilot to establish the workflow.
todos:
  - id: clone_repos
    content: Clone or access the 3 selected cheatsheet repositories and examine their structure
    status: pending
  - id: extract_content
    content: Extract main cheatsheet content from each repository, handling different formats (markdown, YAML)
    status: pending
  - id: create_script
    content: Create script to generate PDFs using WAFT PDF generation tools
    status: pending
  - id: generate_pdfs
    content: Generate PDFs for each cheatsheet with appropriate WAFT style presets
    status: pending
  - id: organize_output
    content: Organize generated PDFs in _work_efforts/cheatsheet_pdfs/ with documentation
    status: pending
  - id: create_work_effort
    content: Create work effort to track progress and document findings
    status: pending
---

# Cheatsheet PDF Generation Pilot

## Objective
Generate professional PDFs from GitHub cheatsheet repositories using WAFT's PDF generation capabilities. This pilot will establish a reusable workflow for converting cheatsheet content into well-formatted PDF documents.

## Selected Repositories (Pilot)

1. **gto76/python-cheatsheet** (38k stars)
   - Comprehensive Python cheatsheet
   - Single markdown file format
   - Well-structured content

2. **tldr-pages/tldr** (60k stars)
   - Collaborative command-line cheatsheets
   - Multiple markdown files per command
   - Good for testing multi-file aggregation

3. **cheat/cheat** (13k stars)
   - Interactive command-line cheatsheet tool
   - YAML-based format
   - Different structure to test flexibility

## Implementation Plan

### Phase 1: Repository Setup
1. Clone selected repositories to temporary directory
2. Examine repository structure and content format
3. Identify main content files (README.md, main cheatsheet files)
4. Document file structure and format for each repository

### Phase 2: Content Extraction
1. Extract main cheatsheet content from each repository
2. Parse markdown/YAML content appropriately
3. Normalize content format for PDF generation
4. Handle code blocks, tables, and special formatting

### Phase 3: PDF Generation
1. Use WAFT's PDF generation system (`src/waft/pdf.py` or `src/waft/evolution/pdf_generator.py`)
2. Apply appropriate style preset (e.g., "clinical_standard" or "premium")
3. Generate individual PDFs for each cheatsheet
4. Optionally create a combined binder with all cheatsheets

### Phase 4: Output Organization
1. Create output directory structure: `_work_efforts/cheatsheet_pdfs/`
2. Organize PDFs by repository name
3. Generate index/README documenting the generated PDFs
4. Create comparison document showing different styles

## Technical Approach

### PDF Generation Method
Use `PDF.from_markdown()` or `PDF.from_content()` from `src/waft/pdf.py`:
- Simple markdown-to-PDF conversion
- Style presets available: "clinical_standard", "premium", "professional"
- Automatic handling of code blocks, tables, headers

### Content Processing
- Read repository files using standard file I/O
- Parse markdown with Python's markdown library (if needed)
- Extract and clean content for PDF generation
- Preserve code formatting and structure

### Output Structure
```
_work_efforts/cheatsheet_pdfs/
├── python-cheatsheet/
│   ├── python-cheatsheet.pdf
│   └── README.md
├── tldr/
│   ├── tldr-commands.pdf
│   └── README.md
├── cheat/
│   ├── cheat-sheets.pdf
│   └── README.md
└── index.md
```

## Files to Create/Modify

1. **Script**: `scripts/generate_cheatsheet_pdfs.py`
   - Clone repositories (or read from local path)
   - Extract content
   - Generate PDFs using WAFT tools
   - Organize output

2. **Output Directory**: `_work_efforts/cheatsheet_pdfs/`
   - Store generated PDFs
   - Include README with generation details

3. **Work Effort**: `_work_efforts/WE-260113-xxxx_cheatsheet_pdf_generation_pilot/`
   - Track progress
   - Document findings
   - Record lessons learned

## Success Criteria

- [ ] Successfully clone/access 3 cheatsheet repositories
- [ ] Extract and parse content from each repository
- [ ] Generate professional PDFs using WAFT tools
- [ ] PDFs are well-formatted with proper code blocks and tables
- [ ] Output is organized and documented
- [ ] Workflow is documented for future use

## Next Steps (Post-Pilot)

- Expand to more repositories
- Create automated pipeline for new cheatsheets
- Build cheatsheet collection/binder system
- Integrate with WAFT documentation system