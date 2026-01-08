"""
Web server for Waft dashboard.

Simple HTTP server to view project information and structure.
"""

import json
import os
import sys
import time
import threading
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from .core.memory import MemoryManager
from .core.substrate import SubstrateManager




class WaftHandler(BaseHTTPRequestHandler):
    """HTTP request handler for Waft web dashboard."""

    def __init__(self, project_path: Path, dev_mode: bool = False, *args, **kwargs):
        self.project_path = project_path
        self.dev_mode = dev_mode
        self.memory = MemoryManager(project_path)
        self.substrate = SubstrateManager(project_path)
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == "/" or path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(self._get_dashboard_html().encode())
        elif path == "/api/info":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(self._get_project_info(), indent=2).encode())
        elif path == "/api/structure":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(self._get_structure_info(), indent=2).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    def _get_project_info(self) -> dict:
        """Get project information as JSON."""
        project_info = self.substrate.get_project_info()
        pyrite_status = self.memory.verify_structure()
        lock_exists = self.substrate.verify_lock()

        # Check templates
        justfile_exists = (self.project_path / "Justfile").exists()
        ci_exists = (self.project_path / ".github" / "workflows" / "ci.yml").exists()
        agents_exists = (self.project_path / "src" / "agents.py").exists()
        gitignore_exists = (self.project_path / ".gitignore").exists()
        readme_exists = (self.project_path / "README.md").exists()

        return {
            "project_path": str(self.project_path.resolve()),
            "project_name": project_info.get("name", "Unknown"),
            "version": project_info.get("version", "Unknown"),
            "pyrite_structure": {
                "valid": pyrite_status["valid"],
                "folders": pyrite_status["folders"],
            },
            "uv_lock": lock_exists,
            "templates": {
                "justfile": justfile_exists,
                "ci": ci_exists,
                "agents": agents_exists,
                "gitignore": gitignore_exists,
                "readme": readme_exists,
            },
        }

    def _get_structure_info(self) -> dict:
        """Get _pyrite structure information."""
        active_files = [str(f.name) for f in self.memory.get_active_files()]
        backlog_files = [str(f.name) for f in self.memory.get_backlog_files()]
        standards_files = [str(f.name) for f in self.memory.get_standards_files()]

        return {
            "active": active_files,
            "backlog": backlog_files,
            "standards": standards_files,
        }

    def _get_dashboard_html(self) -> str:
        """Generate dashboard HTML."""
        info = self._get_project_info()
        structure = self._get_structure_info()
        dev_mode = getattr(self, 'dev_mode', False)

        # Status badges
        pyrite_status = "✅ Valid" if info["pyrite_structure"]["valid"] else "❌ Invalid"
        lock_status = "✅ Exists" if info["uv_lock"] else "⚠️ Missing"

        templates_list = []
        if info["templates"]["justfile"]:
            templates_list.append("Justfile")
        if info["templates"]["ci"]:
            templates_list.append("CI")
        if info["templates"]["agents"]:
            templates_list.append("agents.py")
        if info["templates"]["gitignore"]:
            templates_list.append(".gitignore")
        if info["templates"]["readme"]:
            templates_list.append("README.md")

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Waft Dashboard - {info['project_name']}</title>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            padding: 20px;
            color: #e0e0e0;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .header {{
            background: #1e1e2e;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            border: 1px solid #2d2d3e;
        }}
        .header h1 {{
            color: #7c9eff;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        .header .subtitle {{
            color: #a0a0a0;
            font-size: 1.1em;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        .card {{
            background: #1e1e2e;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            border: 1px solid #2d2d3e;
        }}
        .card h2 {{
            color: #e0e0e0;
            margin-bottom: 15px;
            font-size: 1.5em;
            border-bottom: 2px solid #7c9eff;
            padding-bottom: 10px;
        }}
        .info-item {{
            margin: 10px 0;
            padding: 10px;
            background: #252538;
            border-radius: 6px;
            border: 1px solid #2d2d3e;
        }}
        .info-label {{
            font-weight: 600;
            color: #b0b0b0;
            margin-bottom: 5px;
        }}
        .info-value {{
            color: #e0e0e0;
            font-size: 1.1em;
        }}
        .status {{
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
        }}
        .status.valid {{
            background: #1e4d2e;
            color: #7dd87d;
        }}
        .status.invalid {{
            background: #4d1e1e;
            color: #ff7d7d;
        }}
        .status.missing {{
            background: #4d3d1e;
            color: #ffd87d;
        }}
        .file-list {{
            list-style: none;
            margin-top: 10px;
        }}
        .file-list li {{
            padding: 8px;
            margin: 5px 0;
            background: #252538;
            border-radius: 4px;
            border-left: 3px solid #7c9eff;
            color: #e0e0e0;
        }}
        .empty {{
            color: #707070;
            font-style: italic;
        }}
        .footer {{
            text-align: center;
            color: #a0a0a0;
            margin-top: 30px;
            opacity: 0.9;
        }}
        .navbar {{
            background: #1e1e2e;
            border-radius: 12px;
            padding: 15px 30px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            border: 1px solid #2d2d3e;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .navbar-brand {{
            font-size: 1.5em;
            font-weight: 700;
            color: #7c9eff;
            text-decoration: none;
        }}
        .navbar-links {{
            display: flex;
            gap: 20px;
            align-items: center;
        }}
        .navbar-link {{
            color: #e0e0e0;
            text-decoration: none;
            padding: 8px 16px;
            border-radius: 6px;
            transition: background 0.2s;
        }}
        .navbar-link:hover {{
            background: #252538;
        }}
        .navbar-link.active {{
            background: #252538;
            color: #7c9eff;
        }}
        .dev-badge {{
            background: #1e4d2e;
            color: #7dd87d;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 600;
        }}
        .navbar-button {{
            background: #7c9eff;
            color: #1e1e2e;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.9em;
            font-weight: 600;
            transition: background 0.2s;
        }}
        .navbar-button:hover {{
            background: #6b8eff;
        }}
        .navbar-button:active {{
            background: #5a7dff;
        }}
        .navbar-button.secondary {{
            background: #252538;
            color: #e0e0e0;
            border: 1px solid #2d2d3e;
        }}
        .navbar-button.secondary:hover {{
            background: #2d2d3e;
        }}
        @media (max-width: 768px) {{
            .navbar {{
                flex-direction: column;
                gap: 15px;
            }}
            .navbar-links {{
                flex-wrap: wrap;
                justify-content: center;
            }}
            .navbar-link {{
                font-size: 0.9em;
                padding: 6px 12px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <nav class="navbar" x-data="{{ openHelp: false }}">
            <a href="/" class="navbar-brand">🌊 Waft</a>
            <div class="navbar-links">
                <a href="/" class="navbar-link active">Dashboard</a>
                <a href="/api/info" class="navbar-link" target="_blank">API Info</a>
                <a href="/api/structure" class="navbar-link" target="_blank">Structure</a>
                <button class="navbar-button secondary" @click="openHelp = !openHelp">ℹ️ Help</button>
                <button class="navbar-button" onclick="location.reload()">🔄 Refresh</button>
                {f'<span class="dev-badge">DEV MODE</span>' if dev_mode else ''}
            </div>
            <!-- Help dropdown (Alpine.js powered) -->
            <div x-show="openHelp"
                 x-transition
                 @click.away="openHelp = false"
                 style="position: absolute; top: 100%; right: 30px; margin-top: 10px; background: #1e1e2e; border: 1px solid #2d2d3e; border-radius: 8px; padding: 15px; min-width: 250px; z-index: 1000; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                <h3 style="color: #7c9eff; margin-bottom: 10px;">Waft Dashboard</h3>
                <p style="color: #e0e0e0; margin: 5px 0;"><strong>Project:</strong> {info['project_name']}</p>
                <p style="color: #e0e0e0; margin: 5px 0;"><strong>Version:</strong> {info['version']}</p>
                {f'<p style="color: #7dd87d; margin-top: 10px;">✓ Live reloading enabled</p>' if dev_mode else ''}
            </div>
        </nav>
        <div class="header">
            <h1>🌊 Waft Dashboard</h1>
            <div class="subtitle">Project: {info['project_name']} v{info['version']}</div>
        </div>

        <div class="grid">
            <div class="card">
                <h2>Project Information</h2>
                <div class="info-item">
                    <div class="info-label">Project Path</div>
                    <div class="info-value">{info['project_path']}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Project Name</div>
                    <div class="info-value">{info['project_name']}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Version</div>
                    <div class="info-value">{info['version']}</div>
                </div>
            </div>

            <div class="card">
                <h2>Structure Status</h2>
                <div class="info-item">
                    <div class="info-label">_pyrite Structure</div>
                    <div class="info-value">
                        <span class="status {'valid' if info['pyrite_structure']['valid'] else 'invalid'}">
                            {pyrite_status}
                        </span>
                    </div>
                </div>
                <div class="info-item">
                    <div class="info-label">uv.lock</div>
                    <div class="info-value">
                        <span class="status {'valid' if info['uv_lock'] else 'missing'}">
                            {lock_status}
                        </span>
                    </div>
                </div>
            </div>

            <div class="card">
                <h2>Templates</h2>
                <ul class="file-list">
                    {''.join(f'<li>✅ {t}</li>' for t in templates_list) if templates_list else '<li class="empty">No templates found</li>'}
                </ul>
            </div>

            <div class="card">
                <h2>_pyrite/active</h2>
                <ul class="file-list">
                    {''.join(f'<li>📄 {f}</li>' for f in structure['active']) if structure['active'] else '<li class="empty">No files</li>'}
                </ul>
            </div>

            <div class="card">
                <h2>_pyrite/backlog</h2>
                <ul class="file-list">
                    {''.join(f'<li>📄 {f}</li>' for f in structure['backlog']) if structure['backlog'] else '<li class="empty">No files</li>'}
                </ul>
            </div>

            <div class="card">
                <h2>_pyrite/standards</h2>
                <ul class="file-list">
                    {''.join(f'<li>📄 {f}</li>' for f in structure['standards']) if structure['standards'] else '<li class="empty">No files</li>'}
                </ul>
            </div>
        </div>

        <div class="footer">
            <p>Waft - Ambient Meta-Framework for Python</p>
            <p>Refresh page to update information</p>
        </div>
    </div>

    <script>
        // No automatic reloading - use the refresh button when needed
        // This prevents constant reloading issues
    </script>
</body>
</html>"""

    def log_message(self, format, *args):
        """Suppress default logging."""
        pass


def create_handler(project_path: Path, dev_mode: bool = False):
    """Create a handler factory for the project path."""

    def handler(*args, **kwargs):
        return WaftHandler(project_path, dev_mode, *args, **kwargs)

    return handler


def _watch_files(project_path: Path, dev_mode: bool):
    """Watch for file changes and notify clients via SSE (no server restart needed)."""
    if not dev_mode:
        return

    # Get the path to the waft package
    waft_package_path = Path(__file__).parent.parent
    files_to_watch = [
        waft_package_path / "web.py",
        waft_package_path / "main.py",
    ]

    # Try to use watchdog if available
    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler

        class ReloadHandler(FileSystemEventHandler):
            def __init__(self, files_to_watch):
                self.files_to_watch = {str(f.resolve()) for f in files_to_watch}
                self.last_modified = {}

            def on_modified(self, event):
                if event.is_directory:
                    return
                file_path = Path(event.src_path).resolve()
                file_path_str = str(file_path)
                if file_path_str in self.files_to_watch:
                    try:
                        current_mtime = file_path.stat().st_mtime
                        # Debounce: only reload if file actually changed
                        if file_path_str not in self.last_modified or self.last_modified[file_path_str] != current_mtime:
                            self.last_modified[file_path_str] = current_mtime
                            print(f"\n🔄 File changed: {file_path.name}")
                            print("   Notifying clients to reload...")
                            _notify_clients()
                    except (OSError, FileNotFoundError):
                        # File might have been deleted or moved
                        pass

        event_handler = ReloadHandler(files_to_watch)
        observer = Observer()
        # Watch the waft package directory
        observer.schedule(event_handler, str(waft_package_path), recursive=False)
        observer.start()
        return observer

    except ImportError:
        # Fallback to simple polling if watchdog not available
        print("⚠️  Install 'watchdog' for better file watching: uv sync --extra dev")
        print("   Using simple polling (checks every 2 seconds)...")

        def poll_files():
            last_modified = {}
            while True:
                time.sleep(2)
                for file_path in files_to_watch:
                    if file_path.exists():
                        try:
                            current_mtime = file_path.stat().st_mtime
                            file_path_str = str(file_path.resolve())
                            if file_path_str not in last_modified or last_modified[file_path_str] != current_mtime:
                                last_modified[file_path_str] = current_mtime
                                print(f"\n🔄 File changed: {file_path.name}")
                                print("   Notifying clients to reload...")
                                _notify_clients()
                        except (OSError, FileNotFoundError):
                            pass

        thread = threading.Thread(target=poll_files, daemon=True)
        thread.start()
        return None


def serve(project_path: Path, port: int = 8000, host: str = "localhost", dev: bool = False):
    """Start the web server."""
    if dev:
        print(f"\n🌊 Waft Dashboard (Development Mode)")
        print(f"🔄 Live reloading enabled - browser will auto-refresh on changes")
    else:
        print(f"\n🌊 Waft Dashboard")
    print(f"📍 Serving at http://{host}:{port}")
    print(f"📁 Project: {project_path.resolve()}")
    print(f"\nPress Ctrl+C to stop\n")

    handler = create_handler(project_path, dev_mode=dev)
    server = HTTPServer((host, port), handler)

    # Start file watcher in dev mode (no server restart needed)
    observer = _watch_files(project_path, dev)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down server...")
        if observer:
            observer.stop()
            observer.join()
        server.shutdown()

