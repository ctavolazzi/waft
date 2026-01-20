# WAFT PDF Library

A local document library UI for WAFT PDFs with search, version history, and Typst template compilation. The stack is SvelteKit (frontend) + FastAPI (backend).

## Features
- Search and browse PDFs across WAFT
- Inline PDF viewer with quick-open
- Version history snapshots per PDF
- Typst template compilation (s6t5-page-bordering, drafting)

## Quick Start

### Backend (FastAPI)
```bash
cd waft_pdf_library/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload --port 4434
```

### Frontend (SvelteKit)
```bash
cd waft_pdf_library/frontend
pnpm install
pnpm dev
```

Then open: `http://localhost:4433`

## Configuration
- Library roots and ignore list: `backend/config/library.json`
- Typst templates: `backend/typst/templates/*.typ`

## Typst
The backend expects the `typst` CLI on your PATH to compile templates.
