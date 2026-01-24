# Typst Publication Template

This is a reusable template system for creating professional publications with Typst.

## Structure

```
typst_template/
├── main_template.typ          # Master orchestration file
├── functions.typ               # Shared custom functions (callouts, metrics, etc.)
├── cover_template.typ          # Cover page template
├── final_page_template.typ    # Final page/colophon template
└── sections/                   # Individual section files
    ├── 00_title_page.typ
    ├── 01_abstract.typ
    ├── 02_executive_summary.typ
    └── ...
```

## Features

### Custom Functions
- `callout(type, title, body)` - 5 styled callout boxes
  - Types: info, warning, danger, success, note
- `evidence(location, content)` - Special callout for code verification
- `metric(label, value, unit)` - Styled metric display

### Styling
- Professional typography (New Computer Modern)
- Code blocks with syntax highlighting
- Heading hierarchy with branded colors
- Figure/table auto-styling
- Link formatting

### Auto-Generated Content
- Table of Contents (depth 2)
- List of Figures
- List of Tables  
- List of Code Listings

### Page Numbering
- Roman numerals (i, ii, iii...) for front matter
- Arabic numerals (1, 2, 3...) for main body
- Custom headers with title + page number
- Custom footers with author + date

## Usage

### 1. Copy template to your project
```bash
cp -r typst_template/ my_project/
cd my_project
```

### 2. Edit configuration in main_template.typ
```typst
#set document(
  title: "Your Title",
  author: "Your Name",
  date: datetime(year: 2026, month: 1, day: 24),
  keywords: ("keyword1", "keyword2"),
)
```

### 3. Write your sections
Edit files in `sections/` directory. Each section auto-imports `functions.typ`.

### 4. Compile
```bash
# Full document
typst compile main_template.typ output.pdf

# Single section (for testing)
typst compile sections/40_your_section.typ section_output.pdf
```

### 5. Individual section PDFs
```bash
# Compile each section separately
for section in sections/*.typ; do
  name=$(basename "$section" .typ)
  typst compile "$section" "section_pdfs/${name}.pdf"
done
```

## Customization

### Colors
Edit color scheme in `main_template.typ`:
```typst
// Primary: rgb("#1976d2") - blue
// Success: rgb("#4caf50") - green
// Warning: rgb("#f57c00") - orange
// Danger: rgb("#d32f2f") - red
```

### Fonts
Change in global settings:
```typst
#set text(
  font: "Your Font",
  size: 11pt,
)
```

### Callout Types
Add new types in `functions.typ`:
```typst
let colors = (
  info: (bg: rgb("#e3f2fd"), border: rgb("#1976d2")),
  custom: (bg: rgb("#..."), border: rgb("#...")),
)
```

## File Naming Convention

Sections use hexadecimal prefixes for ordering:
- `00-0F` - Front matter
- `10-9F` - Main body chapters
- `A0-BF` - Conclusions
- `C0-DF` - Appendices
- `D0-FF` - Back matter (references, glossary, index)

## Notes

- All sections must `#import "../functions.typ": callout, evidence, metric`
- Cover and final pages are standalone (don't use section template)
- Use `#pagebreak()` sparingly - headings auto-break
- Images go in `images/` directory
- Keep sections modular for easy recompilation
