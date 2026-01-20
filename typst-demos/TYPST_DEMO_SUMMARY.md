# Typst Demo Summary

**Created:** 2026-01-19
**Updated:** 2026-01-19
**Work Effort:** WE-260119-50hp

---

## Overview

This document summarizes the Typst package demos and full-stack web application created to demonstrate:

1. **s6t5-page-bordering** - Professional page borders with headers/footers
2. **drafting** - Margin notes and annotations for document review
3. **scaffolder** - Layout debugging borders for visual layout inspection
4. **codly** - Beautiful code blocks with syntax highlighting and annotations
5. **pinit** - Relative positioning by pins for annotations and arrows
6. **showybox** - Colorful customizable boxes for callouts and notes
7. **stack-pointer** - Program execution and call stack visualization

---

## PDFs Generated

| File | Package | Size | Location |
|------|---------|------|----------|
| `s6t5-page-bordering-demo.pdf` | s6t5-page-bordering v1.0.0 | 57.8 KB | `typst-demos/` |
| `drafting-demo.pdf` | drafting v0.2.2 | 40.3 KB | `typst-demos/` |
| `scaffolder-demo.pdf` | scaffolder v0.2.1 | 49.8 KB | `typst-demos/` |
| `codly-demo.pdf` | codly v1.3.0 | 190.7 KB | `typst-demos/` |
| `pinit-demo.pdf` | pinit v0.2.2 | 50.5 KB | `typst-demos/` |
| `showybox-demo.pdf` | showybox v2.0.4 | 38.7 KB | `typst-demos/` |
| `stack-pointer-demo.pdf` | stack-pointer v0.1.0 | 76 KB | `typst-demos/` |
| `combined-demo.pdf` | ALL 7 PACKAGES | 286 KB | `typst-demos/` |

---

## Package 1: s6t5-page-bordering

**URL:** https://typst.app/universe/package/s6t5-page-bordering

### Purpose
Creates professional bordered pages with customizable headers and footers. Ideal for:
- Business documents
- Technical specifications
- Legal documents
- Academic papers

### Usage

```typst
#import "@preview/s6t5-page-bordering:1.0.0": s6t5-page-bordering

#show: s6t5-page-bordering.with(
  margin: (left: 40pt, right: 40pt, top: 70pt, bottom: 70pt),
  expand: 15pt,
  space-top: 15pt,
  space-bottom: 15pt,
  stroke-header: none,
  stroke-footer: none,
  header: header,
  footer: footer,
)
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| `margin` | Dictionary with left, right, top, bottom values |
| `expand` | Border expansion beyond margin |
| `space-top` | Space between header and content |
| `space-bottom` | Space between content and footer |
| `stroke-header` | Stroke style for header border |
| `stroke-footer` | Stroke style for footer border |
| `header` | Custom header content |
| `footer` | Custom footer content |

---

## Package 2: drafting

**URL:** https://typst.app/universe/package/drafting

### Purpose
Provides margin notes and annotations for document review. Features:
- Left and right margin notes
- Inline annotations
- Automatic collision avoidance
- Multiple reviewer support
- Custom styling

### Usage

```typst
#import "@preview/drafting:0.2.2": *

#set page(margin: (left: 2.5cm, right: 4cm, top: 2cm, bottom: 2cm))
#set-page-properties(margin-right: 4cm)

#margin-note[This appears in the right margin]
#margin-note(side: left)[This appears in the left margin]
#inline-note[This is an inline annotation]
```

### Features

| Function | Description |
|----------|-------------|
| `margin-note` | Add notes to page margins |
| `inline-note` | Add inline annotations |
| `set-margin-note-defaults` | Customize default styling |
| `set-page-properties` | Configure page bounds |

---

## Package 3: scaffolder

**URL:** https://typst.app/universe/package/scaffolder

### Purpose
Shows borders around the main text area, header, and footer for debugging layout issues. Similar to LaTeX's `showframe` package.

### Usage

```typst
#import "@preview/scaffolder:0.2.1": scaffolding

#set page(background: scaffolding())
```

### Customization

```typst
// Red thin border
scaffolding(stroke: red + 0.5pt)

// Blue thick border  
scaffolding(stroke: blue + 1pt)

// Dashed green border
scaffolding(stroke: (paint: green, dash: "dashed"))
```

### Features

| Feature | Description |
|---------|-------------|
| Visual debugging | See exact content boundaries |
| Custom strokes | Color, width, dash patterns |
| Multi-column | Works with column layouts |
| Minimal setup | Single function call |

---

## Package 4: codly

**URL:** https://typst.app/universe/package/codly

### Purpose
Supercharges code blocks with line numbering, syntax highlighting, language icons, annotations, and much more. Essential for technical documentation.

### Setup

```typst
#import "@preview/codly:1.3.0": *
#import "@preview/codly-languages:0.1.1": *
#show: codly-init.with()
#codly(languages: codly-languages)
```

### Features

| Feature | Description |
|---------|-------------|
| Line numbers | Customizable numbering format |
| Syntax highlighting | Auto-detected by language |
| Language icons | Via codly-languages companion |
| Zebra striping | Alternating row colors |
| Highlights | Mark specific code sections |
| Annotations | Add explanations to lines |
| Smart indent | Wrapped line alignment |
| Skip lines | Show partial code with gaps |
| References | Link to lines and highlights |

### Customization

```typst
// Custom language styling
#codly(languages: (
  rust: (name: "Rust", icon: "🦀", color: rgb("#CE412B")),
  python: (name: "Python", icon: "🐍", color: rgb("#3776AB")),
))

// Disable line numbers
#codly(number-format: none)

// Disable zebra striping
#codly(zebra-fill: none)

// Add highlights
#codly(highlights: (
  (line: 1, start: 4, end: 7, fill: yellow),
))
```

---

## Package 5: pinit

**URL:** https://typst.app/universe/package/pinit

### Purpose
Relative positioning by pins - place invisible markers in text and draw arrows, highlights, and annotations between them. Essential for slides and educational materials.

### Setup

```typst
#import "@preview/pinit:0.2.2": *
```

### Basic Usage

```typst
A simple #pin(1)highlighted text#pin(2).
#pinit-highlight(1, 2)
#pinit-point-from(2)[It is simple.]
```

### Functions

| Function | Description |
|----------|-------------|
| `pin(name)` | Place invisible marker |
| `pinit-highlight(pin1, pin2)` | Highlight between pins |
| `pinit-arrow(start, end)` | Arrow between pins |
| `pinit-double-arrow(start, end)` | Bidirectional arrow |
| `pinit-point-to(pin, body)` | Arrow pointing to pin |
| `pinit-point-from(pin, body)` | Arrow from pin to content |
| `pinit-rect(pin1, pin2)` | Rectangle around pins |
| `pinit-line(start, end)` | Line between pins |
| `pinit-place(pin, body)` | Place content at pin |

---

## Package 6: showybox

**URL:** https://typst.app/universe/package/showybox

### Purpose
Creates colorful and customizable boxes for callouts, notes, warnings, tips, and highlighted content sections.

### Setup

```typst
#import "@preview/showybox:2.0.4": showybox
```

### Basic Usage

```typst
#showybox[Basic box content]

#showybox(
  title: "Note",
  [Box with a title]
)
```

### Custom Colors

```typst
#showybox(
  frame: (
    border-color: red.darken(50%),
    title-color: red.lighten(60%),
    body-color: red.lighten(80%)
  ),
  title: "Warning",
  [Custom colored box]
)
```

### Features

| Feature | Description |
|---------|-------------|
| Custom colors | Title, body, footer, border |
| Shadow effects | Configurable offset and color |
| Border styles | Solid, dashed, custom thickness |
| Rounded corners | Adjustable radius |
| Boxed titles | Floating title style |
| Multi-section | Automatic separators |
| Footer support | Bottom content area |
| Nestable | Boxes within boxes |

---

## Full-Stack Web Application

### Architecture

```
typst-webapp/
├── backend/           # FastAPI (Python)
│   ├── main.py
│   └── requirements.txt
├── frontend/          # SvelteKit (TypeScript)
│   ├── src/
│   │   ├── routes/
│   │   │   ├── +layout.svelte
│   │   │   └── +page.svelte
│   │   └── lib/
│   │       └── components/
│   │           ├── TemplateCard.svelte
│   │           ├── PdfViewer.svelte
│   │           └── CodeEditor.svelte
│   └── package.json
├── README.md
└── start.sh
```

### Backend API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/templates` | GET | List available templates |
| `/api/pdf/{name}` | GET | Get pre-compiled PDF |
| `/api/source/{name}` | GET | Get Typst source code |
| `/api/compile` | POST | Compile custom Typst code |
| `/health` | GET | Health check |

### Frontend Features

- **Template Cards**: Select from available Typst templates
- **Code Editor**: Edit Typst source with line numbers
- **PDF Viewer**: Inline preview with download option
- **Live Compile**: Compile edited code on demand
- **Dark Theme**: Modern UI with gradient accents

---

## Quick Start

### 1. View PDFs Directly

```bash
open typst-demos/s6t5-page-bordering-demo.pdf
open typst-demos/drafting-demo.pdf
```

### 2. Start Web Application

```bash
# Terminal 1 - Backend
cd typst-webapp/backend
pip install -r requirements.txt
python -m uvicorn main:app --port 8000

# Terminal 2 - Frontend
cd typst-webapp/frontend
npm install
npm run dev
```

Then open http://localhost:5173

### 3. Use the Startup Script

```bash
cd typst-webapp
./start.sh
```

---

## File Locations

```
/Users/ctavolazzi/Code/active/waft/
├── typst-demos/
│   ├── drafting-demo.typ          # Typst source
│   ├── drafting-demo.pdf          # Compiled PDF
│   ├── s6t5-page-bordering-demo.typ
│   ├── s6t5-page-bordering-demo.pdf
│   └── TYPST_DEMO_SUMMARY.md      # This file
└── typst-webapp/
    ├── backend/
    │   ├── main.py
    │   └── requirements.txt
    ├── frontend/
    │   ├── package.json
    │   ├── svelte.config.js
    │   ├── vite.config.ts
    │   └── src/
    │       ├── app.html
    │       ├── app.css
    │       ├── routes/
    │       │   ├── +layout.svelte
    │       │   └── +page.svelte
    │       └── lib/
    │           ├── index.ts
    │           └── components/
    │               ├── TemplateCard.svelte
    │               ├── PdfViewer.svelte
    │               └── CodeEditor.svelte
    ├── README.md
    └── start.sh
```

---

## Tech Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Document | Typst | Latest |
| Backend | FastAPI | ≥0.109.0 |
| Server | Uvicorn | ≥0.27.0 |
| Frontend | SvelteKit | 2.x |
| Build | Vite | 5.x |
| Language | TypeScript/Python | 5.x/3.10+ |

---

## Screenshots

The web application features:
- Dark theme with purple/orange gradient title
- Template cards with version badges
- Split-pane editor and PDF viewer
- Responsive design for mobile/desktop

---

## References

- [Typst Documentation](https://typst.app/docs)
- [s6t5-page-bordering Package](https://typst.app/universe/package/s6t5-page-bordering)
- [drafting Package](https://typst.app/universe/package/drafting)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [SvelteKit Documentation](https://kit.svelte.dev)
