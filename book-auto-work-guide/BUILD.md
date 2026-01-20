# Building the Auto-Work Guide

This document explains how to build both the HTML and PDF versions of the Auto-Work guide.

## Two Formats Available

### 1. HTML Book (Shiroa)

The interactive HTML book with all 22 chapters:

```bash
cd book-auto-work-guide
shiroa serve
```

Then open http://localhost:25520 in your browser.

**Features:**
- Interactive navigation
- Search functionality
- Responsive design
- All 22 chapters included

### 2. PDF Document

The complete PDF with all 22 chapters:

```bash
cd book-auto-work-guide
typst compile src/book-complete-pdf.typ output.pdf
```

**Features:**
- Print-ready format
- All 22 chapters included
- Professional formatting
- Table of contents
- Page numbers

## File Structure

```
book-auto-work-guide/
├── src/
│   ├── book.typ              # Shiroa HTML book config
│   ├── book-complete-pdf.typ # Complete PDF source (all chapters)
│   └── chapters/             # 22 chapter files
│       ├── 01-introduction.typ
│       ├── 02-what-is-auto-work.typ
│       └── ... (20 more chapters)
├── output.pdf                # Generated PDF
└── README.md                 # Quick start guide
```

## Rebuilding

### Rebuild HTML

```bash
shiroa build
shiroa serve
```

### Rebuild PDF

```bash
typst compile src/book-complete-pdf.typ output.pdf
```

## Notes

- The HTML version uses the shiroa template (interactive book)
- The PDF version uses standard Typst (print-ready)
- Both include all 22 chapters
- Screenshot placeholders are marked with `*[Screenshot Placeholder: ...]*`
- See `SCREENSHOT_GUIDE.md` for adding screenshots
