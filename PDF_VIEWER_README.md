# PDF Viewer Browser UI

A simple, standalone browser-based PDF viewer with file browser interface.

## Features

- 📁 **File Browser**: Sidebar listing all PDFs in the directory
- 📄 **PDF Viewer**: Full-featured PDF viewer using PDF.js
- 🎯 **Navigation**: Previous/Next page buttons
- 🔍 **Zoom Controls**: Zoom in, zoom out, fit to width
- ⌨️ **Keyboard Shortcuts**: Arrow keys for navigation, +/- for zoom
- 🎨 **Dark Theme**: Modern dark UI

## Usage

### Start the Server

```bash
# Serve PDFs from current directory on port 8000
python3 pdf_viewer_server.py

# Serve from a specific directory
python3 pdf_viewer_server.py --dir /path/to/pdfs

# Use a custom port
python3 pdf_viewer_server.py --port 8080

# Bind to all interfaces (accessible from network)
python3 pdf_viewer_server.py --host 0.0.0.0
```

### Access the Viewer

Open your browser and navigate to:
```
http://localhost:8000
```

## Controls

### Mouse
- Click on a PDF in the sidebar to open it
- Use toolbar buttons for navigation and zoom

### Keyboard
- `←` / `→` : Previous/Next page
- `+` / `-` : Zoom in/out
- `Fit Width` button: Auto-fit PDF to window width

## API Endpoints

- `GET /` - Main HTML viewer interface
- `GET /api/pdfs` - List all PDF files (JSON)
- `GET /api/pdf/<path>` - Serve a PDF file

## Example

```bash
# Start server in project root
cd /Users/ctavolazzi/Code/active/waft
python3 pdf_viewer_server.py --port 8000

# Open browser to http://localhost:8000
# Browse and view any PDFs in the directory tree
```

## Requirements

- Python 3.6+
- Standard library only (no external dependencies)
- Modern web browser with JavaScript enabled

## Files

- `pdf_viewer.html` - Frontend HTML/CSS/JavaScript
- `pdf_viewer_server.py` - Python HTTP server
- `PDF_VIEWER_README.md` - This file

## Security Notes

- The server prevents directory traversal attacks
- Only serves files within the specified base directory
- PDFs are served with proper MIME types
- CORS headers allow cross-origin access (for development)
