# Typst Demo Web App

A full-stack web application demonstrating Typst packages with FastAPI backend and SvelteKit frontend.

## Features

- **PDF Preview**: View pre-compiled Typst documents
- **Live Editor**: Edit Typst source code in the browser
- **Compile on Demand**: Compile custom Typst code to PDF
- **Modern UI**: Beautiful dark theme with responsive design

## Packages Demonstrated

### 1. s6t5-page-bordering
Professional page borders with headers and footers for business documents.
- [Package URL](https://typst.app/universe/package/s6t5-page-bordering)

### 2. drafting
Margin notes and annotations for document review.
- [Package URL](https://typst.app/universe/package/drafting)

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- Typst CLI (`brew install typst` or [install guide](https://typst.app))

### Backend (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Backend runs at: http://localhost:8000

### Frontend (SvelteKit)

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: http://localhost:5173

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/templates` | GET | List available templates |
| `/api/pdf/{name}` | GET | Get pre-compiled PDF |
| `/api/source/{name}` | GET | Get Typst source code |
| `/api/compile` | POST | Compile custom Typst code |
| `/health` | GET | Health check |

## Project Structure

```
typst-webapp/
├── backend/
│   ├── main.py           # FastAPI application
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── routes/       # SvelteKit pages
│   │   └── lib/          # Components
│   └── package.json      # Node dependencies
└── README.md
```

## Development

### Adding New Templates

1. Create a `.typ` file in `typst-demos/`
2. Compile to PDF: `typst compile your-template.typ`
3. Add template info to `TEMPLATES` dict in `backend/main.py`

## Tech Stack

- **Backend**: FastAPI, Python, Uvicorn
- **Frontend**: SvelteKit, TypeScript, Vite
- **Document**: Typst
