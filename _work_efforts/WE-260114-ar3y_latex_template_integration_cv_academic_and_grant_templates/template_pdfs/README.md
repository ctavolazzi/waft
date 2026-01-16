# Template PDF Gallery

**Generated:** 2026-01-14
**Purpose:** Showcase PDF outputs from all LaTeX templates being integrated into WAFT

## PDF Collection

### 1. ETH Zurich Article Template
- **File:** `eth-zurich-article-template.pdf`
- **Source:** https://github.com/moritzhoferer/article_template
- **Type:** Academic article template
- **Features:** Simple structure, theorem environments, line numbering, natbib bibliography

### 2. Twenty Seconds CV Template
- **File:** `twenty-seconds-cv-template.pdf`
- **Source:** https://github.com/KasparJohannesSchneider/TwentySecondsCurriculumVitae-LaTex
- **Type:** Professional CV/Resume
- **Features:** One-page layout, sidebar profile, FontAwesome icons, skills visualization

### 3. NIH F31 Grant Proposal Templates (9 sections)
- **Files:** `f31-*-*.pdf`
- **Source:** https://github.com/novasmedley/f31-templates
- **Type:** Grant proposal sections
- **Sections:**
  1. `f31-aims-and-research-strategy-f31-aims-strategy.pdf` - Aims and Research Strategy
  2. `f31-applicant-background-and-goals-for-fellowship-training-f31-applicant.pdf` - Applicant Background
  3. `f31-description-of-institutional-environment-and-commitment-to-training-f31-environment.pdf` - Institutional Environment
  4. `f31-protection-of-human-subjects-f31-human-subjects.pdf` - Human Subjects Protection
  5. `f31-relevance-to-public-health-f31-relevance.pdf` - Public Health Relevance
  6. `f31-resource-sharing-plan-f31-share-plan.pdf` - Resource Sharing Plan
  7. `f31-respective-contributions-f31-contributions.pdf` - Respective Contributions
  8. `f31-selection-of-sponsor-and-institution-f31-selection.pdf` - Sponsor Selection
  9. `f31-training-in-responsible-conduct-of-research-f31-conduct.pdf` - Responsible Conduct of Research

### 4. INSA Toulouse Template Pages
- **Files:** `insa-toulouse-*.pdf`
- **Source:** https://github.com/ClubInfoInsaT/latex-templates-insa-toulouse
- **Type:** Academic document template pages
- **Pages:**
  - `insa-toulouse-first-page.pdf` - Cover page template
  - `insa-toulouse-page.pdf` - Standard page template
  - `insa-toulouse-last-page.pdf` - Last page template

### 5. WAFT Generated Samples
- **Files:**
  - `waft-academic-paper-sample.pdf` - Academic paper sample
  - `waft-dnd-scenario-sample.pdf` - D&D scenario sample
- **Source:** Generated using WAFT's template system
- **Type:** WeasyPrint-based PDFs
- **Features:** Demonstrates WAFT's PDF generation without LaTeX installation

## Notes

- **LaTeX Compilation:** Most templates require LaTeX (pdflatex/lualatex) to compile from source
- **WAFT Approach:** Uses WeasyPrint for PDF generation (no LaTeX required)
- **Template Status:** All templates are being analyzed for integration into WAFT's template library system

## Missing Templates

- **D&D 5e LaTeX Template:** No example PDF found in repository (requires compilation from source)
  - ✅ **WAFT Alternative:** `waft-dnd-scenario-sample.pdf` demonstrates D&D-style output
- **INSA Toulouse Full Document:** Only page templates available (full document requires compilation)

## Next Steps

1. Install LaTeX distribution to compile remaining templates
2. Generate sample PDFs from D&D 5e template
3. Compile full INSA Toulouse document
4. Create WAFT equivalents using WeasyPrint for all templates
