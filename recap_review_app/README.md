# Recap and Review Full Stack Application

**Electron + FastAPI application for mindspace documentation and review PDF generation.**

This full stack application provides a local desktop application for capturing mindspace, generating review documents, and opening PDFs on your desktop.

---

## Architecture

### Backend: FastAPI
- **Location**: `backend/`
- **Purpose**: API server for mindspace capture and PDF generation
- **Port**: `8000` (default)
- **Features**:
  - REST API endpoints
  - Mindspace data gathering
  - PDF generation
  - File management

### Frontend: Electron
- **Location**: `frontend/`
- **Purpose**: Desktop application UI
- **Features**:
  - Mindspace capture interface
  - Review document display
  - PDF preview
  - Desktop integration

---

## Setup

### Prerequisites
- Python 3.9+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Setup

Following Electron tutorial structure:

```bash
cd frontend
npm install
```

**Verify Installation**:
```bash
node -v    # Should show Node.js version
npm -v     # Should show npm version
```

---

## Running

### Development Mode

**Terminal 1 - Backend**:
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm start
# or
npm run dev
```

The Electron app will open automatically!

### Production Build

**Build Frontend**:
```bash
cd frontend
npm run build
```

**Run Backend**:
```bash
cd backend
uvicorn main:app --port 8000
```

**Package Electron App**:
```bash
cd frontend
npm run package  # Package without installer
npm run dist      # Build with installer
```

**Using Electron Forge (Optional)**:
```bash
cd frontend
npm install --save-dev @electron-forge/cli
npx electron-forge import
npm run make      # Package
npm run publish   # Publish
```

---

## API Endpoints

### POST `/api/recap-and-review`
Generate mindspace review document and PDF.

**Request Body**:
```json
{
  "project_path": "/path/to/project",
  "output_path": null
}
```

**Response**:
```json
{
  "success": true,
  "markdown_file": "_work_efforts/MINDSPACE_REVIEW_2026-01-15_1200.md",
  "pdf_file": "_work_efforts/MINDSPACE_REVIEW_2026-01-15_1200.pdf",
  "mindspace_data": {...}
}
```

### GET `/api/health`
Health check endpoint.

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2026-01-15T12:00:00"
}
```

---

## Features

### Mindspace Capture
- Current state analysis
- Session statistics
- Active files tracking
- Git status
- Thoughts and observations
- Decisions documentation
- Work in progress
- Questions and unknowns
- Next steps
- Reflections

### PDF Generation
- Beautiful PDF formatting
- Professional styling
- Complete mindspace documentation
- Desktop opening integration

### Desktop Integration
- Native desktop application
- System tray integration (optional)
- Desktop notifications
- File system access

---

## Development

### Project Structure

```
recap_review_app/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── api/
│   │   └── routes.py        # API routes
│   ├── core/
│   │   └── recap_review.py  # Recap and review logic
│   ├── requirements.txt
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── main.js          # Electron main process
│   │   ├── preload.js       # Preload script
│   │   └── renderer/
│   │       ├── index.html   # UI HTML
│   │       ├── app.js        # UI logic
│   │       └── styles.css    # Styling
│   ├── package.json
│   └── README.md
└── README.md
```

---

## Docker Support

### Quick Start with Docker

```bash
# Start backend in Docker
docker-compose up -d backend

# Start frontend locally
cd frontend && npm start
```

See `DOCKER.md` for complete Docker documentation.

---

## Next Steps

1. ✅ Create application structure
2. ✅ Build FastAPI backend
3. ✅ Build Electron frontend
4. ✅ Integrate PDF generation
5. ✅ Dockerize backend
6. ⏳ Test complete workflow
7. ⏳ Package for distribution

---

**This application provides a complete local solution for mindspace documentation and review PDF generation.**
