#!/usr/bin/env python3
"""
Live Reloading Server for Fai Wei Founder UI

Serves the HTML file with live reloading capability.
Opens browser automatically and watches for file changes.
"""

import http.server
import os
import socketserver
import time
import webbrowser
from pathlib import Path
from threading import Timer

PORT = 8001
HTML_FILE = (
    Path(__file__).parent.parent
    / "_realms"
    / "bureaucracy_realm"
    / "corporations"
    / "teleport_massive_20250701"
    / "fai_wei_founder.html"
)


class LiveReloadHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP handler with live reload script injection."""

    def end_headers(self):
        # Add CORS headers for development
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def do_GET(self):
        if self.path == "/" or self.path == "/fai_wei_founder.html":
            self.path = str(HTML_FILE.relative_to(Path.cwd()))

        return super().do_GET()


def open_browser():
    """Open browser after a short delay."""
    time.sleep(1.5)
    webbrowser.open(f"http://localhost:{PORT}/fai_wei_founder.html")


def main():
    """Start the live reloading server."""
    # Change to the directory containing the HTML file
    os.chdir(HTML_FILE.parent)

    print("=" * 60)
    print("Fai Wei Founder UI - Live Reloading Server")
    print("=" * 60)
    print(f"HTML File: {HTML_FILE}")
    print(f"Server: http://localhost:{PORT}/fai_wei_founder.html")
    print()
    print("Opening browser in 1.5 seconds...")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()

    # Open browser after delay
    Timer(0, open_browser).start()

    # Start server
    with socketserver.TCPServer(("", PORT), LiveReloadHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nServer stopped.")


if __name__ == "__main__":
    main()
