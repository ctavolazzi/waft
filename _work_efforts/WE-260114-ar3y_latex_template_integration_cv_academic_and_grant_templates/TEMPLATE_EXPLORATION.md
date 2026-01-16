# LaTeX Template Exploration Report

**Date:** 2026-01-14
**Work Effort:** WE-260114-ar3y
**Status:** ✅ Complete

---

## Overview

Successfully cloned and explored six LaTeX template repositories for integration into WAFT's PDF template library system:

1. **TwentySecondsCurriculumVitae-LaTex** - Professional CV template
2. **latex-templates-insa-toulouse** - INSA Toulouse academic document templates
3. **f31-templates** - NIH F31 grant proposal templates
4. **DND-5e-LaTeX-Template** - D&D 5e roleplaying game document template
5. **eth-zurich-article-template** - ETH Zurich MIP chair article template
6. **ArthurDantas-CV** - Bilingual CV template (English/Portuguese)

---

## 1. TwentySecondsCurriculumVitae-LaTex

### Repository Info
- **URL:** https://github.com/KasparJohannesSchneider/TwentySecondsCurriculumVitae-LaTex
- **License:** MIT
- **Purpose:** One-page professional CV/resume template
- **Key Features:**
  - FontAwesome5 icon support
  - Multi-language support (English/German)
  - Sidebar profile section
  - Skills visualization (bar charts)
  - Clean, minimal design (KISS principle)

### Structure
```
TwentySecondsCurriculumVitae-LaTex/
├── twentysecondcv.cls          # Main LaTeX class file
├── Twenty-Seconds-Icons_cv.tex # Example CV file
├── Twenty-Seconds-Icons_cv.pdf # Example output
├── Makefile                    # Build automation
├── README.md                   # Comprehensive documentation
└── alice.jpeg                  # Sample profile picture
```

### Key Components

#### Class File: `twentysecondcv.cls`
- Custom LaTeX document class
- Options: `icon`, `en`, `de`, `no_aboutme`
- Profile sidebar with photo, contact info, skills
- Body section with sections and timeline items
- Color scheme: mainblue (#0E5484), sidecolor (#E7E7E7), etc.

#### Profile Commands
```latex
\profilepic{path}           # Profile picture
\cvname{name}               # Name
\cvjobtitle{title}          # Job title
\cvdate{date}               # Date of birth
\cvaddress{address}         # Address
\cvnumberphone{phone}       # Phone number
\cvmail{email}              # Email
\cvgithub{username}         # GitHub (requires icon option)
\cvlinkedin{url}            # LinkedIn (requires icon option)
\about{description}         # About me section
\skills{{skill1/level1},{skill2/level2}}  # Skills with bars (0-6 scale)
\skillstext{{skill1/level1}}              # Skills as text
\makeprofile                # Render profile sidebar
```

#### Body Commands
```latex
\section{name}              # Section header
\sectionicon{icon}{name}    # Section with icon
\begin{twenty}              # Timeline items (year, title, place, description)
  \twentyitem{year}{title}{place}{description}
\end{twenty}
\begin{twentyicon}          # Timeline with icons
  \twentyitemicon{icon}{year}{title}{place}{description}
\end{twentyicon}
```

### Dependencies
- ClearSans font
- TikZ (for graphics)
- xcolor
- textpos
- fontawesome5 (optional, for icons)
- marvosym
- parskip

### Build Requirements
- LaTeX installation
- Additional packages: ClearSans, fontenc, tikz, xcolor, textpos, ragged2e, etoolbox, ifmtarg, ifthen, pgffor, marvosym, parskip

### Design Philosophy
- **KISS (Keep It Simple, Stupid)**
- One-page only (designed for "twenty seconds" screening)
- Accomplished <X> by implementing <Y> which led to <Z> format for experiences

### Integration Notes
- ✅ Well-documented
- ✅ Clean class-based structure
- ✅ Easy to convert to Python/WeasyPrint template
- ✅ Icon support via FontAwesome5
- ⚠️ Requires LaTeX compilation (or conversion to HTML/CSS)

---

## 2. latex-templates-insa-toulouse

### Repository Info
- **URL:** https://github.com/ClubInfoInsaT/latex-templates-insa-toulouse
- **License:** GPLv2.0
- **Purpose:** Academic document templates for INSA Toulouse (French engineering school)
- **Language:** French
- **Key Features:**
  - Professional academic document structure
  - Cover page templates
  - Table of contents
  - Bibliography support
  - Custom page layouts

### Structure
```
latex-templates-insa-toulouse/
├── Templates/
│   ├── main.tex                    # Main document file
│   ├── contents.tex                # Main content file
│   ├── template/
│   │   ├── preambule.tex           # Preamble (don't modify)
│   │   ├── premiere_page.tex       # First page template
│   │   ├── page_garde.tex          # Cover page template
│   │   ├── table_des_matieres.tex  # Table of contents
│   │   ├── derniere_page.tex       # Last page template
│   │   └── assets/                 # Images and PDFs
│   └── contents/
│       ├── abstract.tex            # Abstract section
│       ├── remerciements.tex      # Acknowledgments
│       ├── biblio.tex              # Bibliography
│       ├── bibliography.bib        # BibTeX file
│       ├── annexes.tex             # Appendices
│       ├── figures.tex             # Figures list
│       ├── lexique.tex             # Glossary
│       └── confidentiel.tex        # Confidentiality notice
└── README.md
```

### Key Components

#### Main Document Structure
```latex
\documentclass[11pt]{article}
\input{template/preambule}

% Custom commands for document metadata
\newcommand{\titre}{Nom du document}
\newcommand{\imagecouverture}{example-image}
\newcommand{\firstcouverture}{...}  % First cover page content
\newcommand{\secondcouverture}{...}  % Second cover page content

\begin{document}
    \input{template/premiere_page}
    \input{template/page_garde}
    \input{contents/confidentiel}
    \input{contents/remerciements}
    \input{contents/abstract}
    \input{template/table_des_matieres}
    \input{contents}                 # Main content
    \input{contents/biblio}
    \input{contents/lexique}
    \input{contents/figures}
    \input{contents/annexes}
    \input{template/derniere_page}
\end{document}
```

### Features
- Modular structure (easy to include/exclude sections)
- Professional cover pages
- Table of contents
- Bibliography support (biblatex)
- Custom page templates
- French academic document standards

### Integration Notes
- ✅ Modular structure (easy to adapt)
- ✅ Well-organized file structure
- ⚠️ French language (may need translation)
- ⚠️ INSA-specific branding (may need customization)
- ✅ Can be adapted for general academic documents

---

## 3. f31-templates

### Repository Info
- **URL:** https://github.com/novasmedley/f31-templates
- **License:** (Not specified, check LICENSE file)
- **Purpose:** NIH F31 predoctoral fellowship grant proposal templates
- **Key Features:**
  - Complete F31 grant component templates
  - NIH formatting compliance
  - Multiple document sections
  - Example PDFs for reference

### Structure
```
f31-templates/
├── aims-and-research-strategy/
│   ├── f31-aims-strategy.tex       # Specific Aims & Research Strategy
│   ├── f31-aims-strategy.pdf       # Example output
│   ├── ieetrCustom.bst             # Custom bibliography style
│   ├── sample.bib                  # Sample bibliography
│   └── README.md                   # Tips and guidance
├── applicant-background-and-goals-for-fellowship-training/
│   ├── f31-applicant.tex
│   └── f31-applicant.pdf
├── description-of-institutional-environment-and-commitment-to-training/
│   ├── f31-environment.tex
│   └── f31-environment.pdf
├── protection-of-human-subjects/
│   ├── f31-human-subjects.tex
│   └── f31-human-subjects.pdf
├── relevance-to-public-health/
│   ├── f31-relevance.tex
│   └── f31-relevance.pdf
├── resource-sharing-plan/
│   ├── f31-share-plan.tex
│   └── f31-share-plan.pdf
├── respective-contributions/
│   ├── f31-contributions.tex
│   └── f31-contributions.pdf
├── selection-of-sponsor-and-institution/
│   ├── f31-selection.tex
│   └── f31-selection.pdf
├── training-in-responsible-conduct-of-research/
│   ├── f31-conduct.tex
│   └── f31-conduct.pdf
└── README.md                       # Comprehensive guide
```

### Key Components

#### Document Structure (Example: aims-and-research-strategy)
```latex
\documentclass[11pt]{article}
\usepackage{lipsum}  % Dummy text
\usepackage{xparse}
\usepackage{varwidth}
\usepackage{cite}
\usepackage{graphicx,url}
\usepackage[font=small,labelfont=bf]{caption}
\usepackage{amsmath}
\usepackage{geometry}
\geometry{margin=0.5in}  % NIH requirement: 0.5 inch margins
\usepackage{fontspec}
\setmainfont{Times New Roman}  % NIH requirement: Times New Roman
\setlength\parindent{0pt}
\setcounter{section}{3}
\renewcommand{\thesubsection}{\thesection.\alph{subsection}}
\pagenumbering{gobble}  % No page numbers

\begin{document}
\section*{Specific Aims [1 pg]}
% Content here...
\end{document}
```

### Grant Components
1. **Specific Aims & Research Strategy** (Most important - 90% of work)
2. **Applicant's Background and Goals for Fellowship Training**
3. **Description of Institutional Environment and Commitment to Training**
4. **Protection of Human Subjects** (if applicable)
5. **Relevance to Public Health**
6. **Resource Sharing Plan**
7. **Respective Contributions**
8. **Selection of Sponsor and Institution**
9. **Training in Responsible Conduct of Research**

### NIH Requirements
- **Margins:** 0.5 inches
- **Font:** Times New Roman (or Arial/Helvetica)
- **Font Size:** 11pt minimum
- **Page Limits:** Varies by section (e.g., Specific Aims: 1 page)
- **Line Spacing:** Single or double (varies by section)
- **Compilation:** LuaLaTeX (for Times New Roman via fontspec)

### Integration Notes
- ✅ Complete grant component templates
- ✅ NIH formatting compliance built-in
- ✅ Example PDFs for reference
- ✅ Comprehensive README with grant process guidance
- ⚠️ Very specific to NIH F31 grants
- ✅ Can be adapted for other grant formats

---

## Comparison & Integration Strategy

### Template Characteristics

| Feature | CV Template | INSA Template | F31 Template | D&D 5e Template | ETH Zurich Article | ArthurDantas-CV |
|---------|------------|---------------|--------------|-----------------|---------------------|------------------|
| **Type** | Resume/CV | Academic Document | Grant Proposal | RPG Source Material | Academic Article | Resume/CV |
| **Pages** | 1 page | Multi-page | Multi-page (varies) | Multi-page | Multi-page | Multi-page |
| **Language** | EN/DE | FR | EN | Multi (EN/FR/IT/ES/PT/RU/JA/DE) | EN | EN/PT |
| **Structure** | Class-based | Modular files | Section-based | Class/Package + Modular | Single file | Single file |
| **Icons** | FontAwesome5 | None | None | None | None | FontAwesome |
| **Complexity** | Medium | High | Medium | High | Low | Low |
| **Customization** | High | Medium | Low (NIH-specific) | High | Medium | High |
| **Special Features** | Skills bars | Cover pages | NIH compliance | Stat blocks, read-aloud | Theorem environments, line numbers | Bilingual, full-width |

### Integration Approach

#### 1. CV Template → WAFT Integration
**Strategy:** Convert LaTeX class to WeasyPrint HTML/CSS template

- Create `src/waft/templates/cv_twenty_seconds.py`
- Convert sidebar profile to HTML/CSS
- Convert skills bars to CSS progress bars
- Convert timeline items to HTML structure
- Support FontAwesome icons via CDN or local files
- Add multi-language support

**Commands to Create:**
- `/cv-generate` - Generate CV from YAML/JSON data
- `/cv-from-markdown` - Generate CV from markdown file

#### 2. INSA Template → WAFT Integration
**Strategy:** Extract modular structure, adapt for general academic use

- Create `src/waft/templates/academic_document.py` (enhanced version)
- Extract cover page templates
- Extract table of contents structure
- Support bibliography
- Make language-agnostic (remove French-specific content)

**Commands to Create:**
- `/academic-document` - Generate academic document
- `/thesis-template` - Generate thesis document

#### 3. F31 Template → WAFT Integration
**Strategy:** Create grant proposal template system

- Create `src/waft/templates/grant_proposal.py`
- Extract NIH formatting requirements
- Create modular grant sections
- Support multiple grant types (F31, R01, etc.)

**Commands to Create:**
- `/grant-proposal` - Generate grant proposal
- `/nih-f31` - Generate NIH F31 specific proposal

#### 4. D&D 5e Template → WAFT Integration
**Strategy:** Integrate LaTeX package/class, create Python wrapper for campaign document generation

- Create `src/waft/templates/dnd5e_latex.py` (LaTeX-based)
- Create `src/waft/templates/dnd5e_campaign.py` (WeasyPrint alternative)
- Extract monster stat block structure
- Extract read-aloud and sidebar environments
- Support D&D 5e color schemes
- Integrate with existing `dnd_scenario.py` template

**Commands to Create:**
- `/dnd-campaign-book` - Generate full campaign book with LaTeX
- `/dnd-adventure` - Generate adventure module
- `/dnd-monster-manual` - Generate monster collection
- `/dnd-stat-block` - Generate single monster stat block

#### 5. ETH Zurich Article Template → WAFT Integration
**Strategy:** Simple academic article template - enhance existing `academic_paper.py` or create LaTeX-based version

**Repository Info:**
- **URL:** https://github.com/moritzhoferer/article_template
- **License:** Not specified (public template)
- **Purpose:** Research article template for ETH Zurich MIP chair
- **Key Features:**
  - Standard article class with minimal customization
  - Theorem environments (definition, assumption, theorem, corollary, lemma, proposition)
  - Line numbering enabled by default
  - natbib bibliography (apalike style)
  - Custom table column types (fixed width, alignment)
  - Abstract structure with example format
  - JEL classification support (economics-specific)
  - Proof environment with custom styling

**Structure:**
```
eth-zurich-article-template/
├── main.tex          # Main document (single file)
├── references.bib    # Bibliography file
├── main.pdf          # Example output
├── README.md         # Brief documentation
└── .gitignore        # Standard LaTeX ignores
```

**Key Components:**

1. **Document Class:** Standard `article` class with options:
   - Font sizes: 10pt, 11pt, 12pt
   - Paper sizes: a4paper, a5paper
   - Optional: draft, twocolumn, fleqn, leqno, landscape

2. **Package Usage:**
   - `amssymb`, `amsmath`, `amsfonts` - Advanced math
   - `authblk` - Author/affiliation blocks
   - `geometry` - Page margins (2.54cm all sides)
   - `setspace` - Line spacing (onehalfspacing default)
   - `natbib` - Bibliography management
   - `hyperref` - Hyperlinks (black, breaklinks)
   - `ntheorem` - Theorem environments
   - `lineno` - Line numbering

3. **Theorem Environments:**
   - `definition`, `assumption`, `theorem`, `corollary`, `lemma`, `proposition`
   - All use `theoremstyle{break}` for line breaks
   - Custom `proof` environment with rule ending

4. **Table Column Types:**
   - `\C{width}`, `\L{width}`, `\R{width}` for fixed-width columns

5. **Abstract Structure:**
   - Example format with sections: Context, What we have, What we want, Task, Object, Findings, Conclusion, Perspectives
   - Keywords and JEL Classification fields

6. **Bibliography:**
   - Uses `apalike` style (economics standard)
   - natbib citation commands

**Comparison to WAFT's `academic_paper.py`:**
- WAFT uses **WeasyPrint/HTML** (not pure LaTeX)
- ETH template is **pure LaTeX** (requires pdflatex/lualatex)
- ETH template has theorem environments (WAFT doesn't)
- ETH template has line numbering (WAFT doesn't)
- ETH template is simpler, single-file structure
- ETH template is economics-focused (JEL classification)
- WAFT template is more general-purpose

**Integration Options:**

**Option A: Enhance Existing Template**
- Add theorem environments to `academic_paper.py` (WeasyPrint)
- Add line numbering support
- Add JEL classification field
- Keep WeasyPrint approach (no LaTeX compilation needed)

**Option B: Create LaTeX-Based Template**
- Create `src/waft/templates/eth_article_latex.py`
- Generate pure LaTeX files
- Require LaTeX installation for compilation
- More faithful to original template

**Option C: Hybrid Approach**
- Use WeasyPrint for main content
- Generate LaTeX for complex math/theorems
- Compile LaTeX snippets and embed as PDFs

**Recommended:** Option A - Enhance existing `academic_paper.py` with theorem environments and line numbering. This maintains WAFT's no-LaTeX-required philosophy while adding useful features.

**Commands to Create:**
- `/article-generate` - Generate academic article (enhanced version)
- `/article-with-theorems` - Generate article with theorem environments
- `/economics-article` - Generate economics article with JEL classification

#### 6. ArthurDantas-CV Template → WAFT Integration
**Strategy:** Simple single-file CV template - alternative to TwentySecondsCurriculumVitae-LaTex with full-width layout

**Repository Info:**
- **URL:** https://github.com/ArthurSilvaDantas/ArthurDantas-CV.git
- **License:** MIT
- **Purpose:** Personal CV template with bilingual support (English/Portuguese)
- **Key Features:**
  - Full-width layout (no sidebar)
  - Bilingual support (separate EN/PT files)
  - FontAwesome icons for contact info
  - Custom resume commands for structured sections
  - Clean, professional design
  - Multi-page capable (not limited to one page)

**Structure:**
```
ArthurDantas-CV/
├── en-main.tex          # English version
├── pt-main.tex           # Portuguese version
├── CV_ArthurSD (en).pdf # Example English output
├── CV_ArthurSD (pt).pdf  # Example Portuguese output
├── README.md             # Brief documentation
├── LICENSE               # MIT License
└── assets/               # Images and logos
    ├── capa-readme.png
    └── logo.svg
```

**Key Components:**

1. **Document Class:** Standard `article` class with letterpaper, 11pt
   - No custom class file (simpler than TwentySecondsCurriculumVitae-LaTex)
   - Uses standard LaTeX packages

2. **Package Usage:**
   - `fontawesome` - Icons for contact information
   - `hyperref` - Clickable links (hidelinks option)
   - `babel` - Multi-language support (english, portuguese)
   - `tabularx` - Flexible table layouts
   - `enumitem` - Custom list formatting
   - `fancyhdr` - Header/footer control (disabled)
   - `titlesec` - Section title formatting

3. **Custom Commands:**
   ```latex
   \resumeItem{text}                    # Bullet point item
   \resumeSubheading{title}{place}{role}{dates}  # Experience entry
   \resumeEducationHeading{institution}{location}{degree}{dates}  # Education entry
   \resumeProjectHeading{title}{link}   # Project entry
   \resumeOrganizationHeading{name}{location}{role}{dates}  # Organization entry
   \resumeSubHeadingListStart/End       # List environment wrappers
   \resumeItemListStart/End             # Item list wrappers
   ```

4. **Layout Features:**
   - Full-width design (no sidebar)
   - Centered header with name and contact info
   - Sections: Summary, Education, Skills, Experience, Projects
   - Custom section formatting with horizontal rules
   - Compact spacing for dense information

5. **Language Support:**
   - Separate files for each language (en-main.tex, pt-main.tex)
   - Uses babel package for language-specific formatting
   - Same structure, different content

**Known Issues:**
- ⚠️ `\sotag` command used but not defined (line 119 in both .tex files)
  - Used for interest tags: `\sotag{Software Engineering}`
  - Likely should be a custom command for styled tags/badges
  - Template will compile with error unless command is defined

**Dependencies:**
- Standard LaTeX packages (fontawesome, hyperref, babel, tabularx, enumitem, etc.)
- No special fonts required
- No custom class files

**Comparison to TwentySecondsCurriculumVitae-LaTex:**
- **Layout:** Full-width vs sidebar profile
- **Structure:** Single file vs class-based
- **Pages:** Multi-page capable vs one-page only
- **Complexity:** Simpler (no custom class) vs more complex (custom class)
- **Language:** Bilingual (EN/PT) vs bilingual (EN/DE)
- **Icons:** FontAwesome (same)
- **Skills:** Text list vs visual bars
- **Design Philosophy:** Professional full-width vs KISS one-page

**Integration Notes:**
- ✅ Simple structure (easier to convert than class-based templates)
- ✅ Full-width layout offers alternative to sidebar designs
- ✅ Multi-page capability (more flexible than one-page templates)
- ✅ Well-organized custom commands
- ⚠️ Missing `\sotag` command definition (needs to be added)
- ✅ MIT License (permissive)
- ✅ Good example of bilingual CV structure

**Integration Strategy:**
- Create `src/waft/templates/cv_arthurdantas.py` (WeasyPrint version)
- Convert custom commands to HTML/CSS equivalents
- Support bilingual output (EN/PT or configurable)
- Implement tag/badge system for interests (replacing `\sotag`)
- Full-width layout with centered header
- Support multi-page CVs

**Commands to Create:**
- `/cv-generate-arthurdantas` - Generate CV using ArthurDantas style
- `/cv-bilingual` - Generate bilingual CV (EN/PT)

### Common Patterns to Extract

1. **Modular Structure:** All templates use modular file inclusion
2. **Metadata Commands:** Custom LaTeX commands for document metadata
3. **Professional Typography:** Times New Roman, proper spacing
4. **Page Layouts:** Custom first/last pages, headers/footers
5. **Section Organization:** Clear section hierarchy

---

## Next Steps

### Ticket TKT-ar3y-001: ✅ COMPLETE
- [x] Clone all six repositories
- [x] Explore structure and documentation
- [x] Document findings
- [x] Added ETH Zurich article template (2026-01-14)
- [x] Added ArthurDantas-CV template (2026-01-14)

### Ticket TKT-ar3y-002: Integrate into Template Library
- [ ] Add templates to `src/waft/templates/`
- [ ] Register in template registry (WE-260112-q6gl)
- [ ] Create template metadata
- [ ] Add validation

### Ticket TKT-ar3y-003: Create CV Generator
- [ ] Convert CV template to WeasyPrint
- [ ] Create data schema (YAML/JSON)
- [ ] Implement `/cv-generate` command
- [ ] Add FontAwesome icon support
- [ ] Test with sample data

### Ticket TKT-ar3y-004: Create Academic Document Generators
- [ ] Extract INSA template structure
- [ ] Create general academic document template
- [ ] Implement cover page system
- [ ] Add bibliography support
- [ ] Enhance `academic_paper.py` with theorem environments (from ETH template)
- [ ] Add line numbering support (from ETH template)
- [ ] Add JEL classification field (from ETH template)
- [ ] Create `/academic-document` command

### Ticket TKT-ar3y-005: Create Grant Proposal Generators
- [ ] Extract F31 template structure
- [ ] Create grant proposal template
- [ ] Implement NIH formatting requirements
- [ ] Create modular grant sections
- [ ] Create `/grant-proposal` command

### Ticket TKT-ar3y-006: Document Template Usage
- [ ] Create usage documentation
- [ ] Add examples
- [ ] Document data schemas
- [ ] Create template gallery

---

## Files Created

- `templates_exploration/` - Cloned repositories
  - `TwentySecondsCurriculumVitae-LaTex/`
  - `latex-templates-insa-toulouse/`
  - `f31-templates/`
  - `DND-5e-LaTeX-Template/`
  - `eth-zurich-article-template/`
  - `ArthurDantas-CV/`
- `TEMPLATE_EXPLORATION.md` - This document

---

## References

- [TwentySecondsCurriculumVitae-LaTex](https://github.com/KasparJohannesSchneider/TwentySecondsCurriculumVitae-LaTex)
- [latex-templates-insa-toulouse](https://github.com/ClubInfoInsaT/latex-templates-insa-toulouse)
- [f31-templates](https://github.com/novasmedley/f31-templates)
- [DND-5e-LaTeX-Template](https://github.com/rpgtex/DND-5e-LaTeX-Template)
- [ETH Zurich Article Template](https://github.com/moritzhoferer/article_template)
- [ArthurDantas-CV](https://github.com/ArthurSilvaDantas/ArthurDantas-CV)
- [WAFT Template Library System (WE-260112-q6gl)](../WE-260112-q6gl_pdf_template_library_system/WE-260112-q6gl_index.md)
