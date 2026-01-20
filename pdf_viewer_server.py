#!/usr/bin/env python3
"""
PDF Viewer Server
Simple web server for browsing and viewing PDF files in a browser.
"""

import os
import sys
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, unquote
import json


class PDFViewerHandler(BaseHTTPRequestHandler):
    """HTTP handler for PDF viewer server."""
    
    def __init__(self, base_dir: Path, *args, **kwargs):
        self.base_dir = base_dir.resolve()
        super().__init__(*args, **kwargs)
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS preflight."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests."""
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == "/" or path == "/index.html":
            self._serve_html()
        elif path == "/api/pdfs":
            self._serve_pdf_list()
        elif path.startswith("/api/pdf/"):
            pdf_path = unquote(path.replace("/api/pdf/", ""))
            self._serve_pdf(pdf_path)
        else:
            self._send_404()
    
    def _serve_html(self):
        """Serve the PDF viewer HTML page."""
        html_path = Path(__file__).parent / "pdf_viewer.html"
        if html_path.exists():
            with open(html_path, "rb") as f:
                content = f.read()
            self._send_response(200, "text/html", content)
        else:
            self._send_404()
    
    def _serve_pdf_list(self):
        """Serve list of PDF files in the base directory."""
        pdfs = []
        
        # Search for PDFs recursively
        for pdf_file in self.base_dir.rglob("*.pdf"):
            try:
                # Get relative path from base directory
                rel_path = pdf_file.relative_to(self.base_dir)
                pdfs.append({
                    "name": pdf_file.name,
                    "path": str(rel_path),
                    "size": pdf_file.stat().st_size
                })
            except (ValueError, OSError):
                continue
        
        # Sort by name
        pdfs.sort(key=lambda x: x["name"].lower())
        
        self._send_json(pdfs)
    
    def _serve_pdf(self, pdf_path: str):
        """Serve a PDF file."""
        # Security: prevent directory traversal
        pdf_file = self.base_dir / pdf_path
        try:
            # Ensure the file is within base_dir
            pdf_file = pdf_file.resolve()
            if not str(pdf_file).startswith(str(self.base_dir.resolve())):
                self._send_404()
                return
            
            if not pdf_file.exists() or not pdf_file.is_file():
                self._send_404()
                return
            
            # Read and serve PDF
            with open(pdf_file, "rb") as f:
                content = f.read()
            
            self._send_response(200, "application/pdf", content)
        except (OSError, ValueError) as e:
            print(f"Error serving PDF {pdf_path}: {e}", file=sys.stderr)
            self._send_404()
    
    def _send_json(self, data):
        """Send JSON response."""
        json_str = json.dumps(data, indent=2)
        self._send_response(200, "application/json", json_str.encode())
    
    def _send_response(self, status: int, content_type: str, data: bytes):
        """Send HTTP response."""
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data)
    
    def _send_404(self):
        """Send 404 Not Found."""
        self.send_response(404)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"404 Not Found")
    
    def log_message(self, format, *args):
        """Override to use stderr instead of stdout."""
        print(f"[{self.address_string()}] {format % args}", file=sys.stderr)


def create_handler(base_dir: Path):
    """Create handler class with base_dir bound."""
    def handler(*args, **kwargs):
        return PDFViewerHandler(base_dir, *args, **kwargs)
    return handler


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="PDF Viewer Server")
    parser.add_argument(
        "--dir",
        type=str,
        default=".",
        help="Directory to serve PDFs from (default: current directory)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to serve on (default: 8000)"
    )
    parser.add_argument(
        "--host",
        type=str,
        default="localhost",
        help="Host to bind to (default: localhost)"
    )
    
    args = parser.parse_args()
    
    base_dir = Path(args.dir).resolve()
    if not base_dir.exists():
        print(f"Error: Directory does not exist: {base_dir}", file=sys.stderr)
        sys.exit(1)
    
    if not base_dir.is_dir():
        print(f"Error: Not a directory: {base_dir}", file=sys.stderr)
        sys.exit(1)
    
    handler = create_handler(base_dir)
    server = HTTPServer((args.host, args.port), handler)
    
    print(f"\n📄 PDF Viewer Server")
    print(f"📍 Serving at http://{args.host}:{args.port}")
    print(f"📁 PDF Directory: {base_dir}")
    print(f"\nPress Ctrl+C to stop\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down server...")
        server.shutdown()


if __name__ == "__main__":
    main()
