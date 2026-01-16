#!/usr/bin/env python3
"""
Projects Dashboard Server

Serves a web dashboard that displays real WAFT projects data.
"""

import json
import sys
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from waft.core.projects import ProjectManager, ProjectStatus


class ProjectsDashboardHandler(BaseHTTPRequestHandler):
    """HTTP handler for Projects Dashboard."""

    def __init__(self, project_path: Path, *args, **kwargs):
        self.project_path = project_path
        self.manager = ProjectManager(project_path)
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == "/" or path == "/index.html":
            self._serve_dashboard()
        elif path == "/api/projects":
            self._serve_projects_api()
        elif path == "/api/stats":
            self._serve_stats_api()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    def _serve_dashboard(self):
        """Serve the HTML dashboard."""
        dashboard_path = Path(__file__).parent / "projects_dashboard.html"
        if dashboard_path.exists():
            with open(dashboard_path, 'r', encoding='utf-8') as f:
                html = f.read()

            # Replace mock data loading with API call
            html = html.replace(
                '// Mock data - in real implementation, parse from CLI output or API',
                '// Load from API'
            )
            html = html.replace(
                'projects = [',
                'const response = await fetch("/api/projects");\n                projects = await response.json();\n                /* Mock fallback: */ projects = projects.length > 0 ? projects : ['
            )
            html = html.replace(
                '];',
                '];'
            )

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Dashboard file not found")

    def _serve_projects_api(self):
        """Serve projects as JSON."""
        try:
            projects = self.manager.list_projects()
            projects_data = [self._project_to_dict(p) for p in projects]

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(projects_data, indent=2).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))

    def _serve_stats_api(self):
        """Serve statistics as JSON."""
        try:
            projects = self.manager.list_projects()
            total = len(projects)
            active = len([p for p in projects if p.status == ProjectStatus.ACTIVE])
            avg_progress = sum(p.progress_percent for p in projects) / total if total > 0 else 0.0
            total_milestones = sum(len(p.milestones) for p in projects)

            stats = {
                "total_projects": total,
                "active_projects": active,
                "avg_progress": round(avg_progress, 1),
                "total_milestones": total_milestones
            }

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(stats, indent=2).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))

    def _project_to_dict(self, project):
        """Convert Project to dictionary for JSON."""
        return {
            "project_id": project.project_id,
            "title": project.title,
            "description": project.description,
            "status": project.status.value,
            "progress_percent": project.progress_percent,
            "tags": project.tags,
            "milestones": [
                {
                    "milestone_id": m.milestone_id,
                    "title": m.title,
                    "description": m.description,
                    "target_date": m.target_date,
                    "completed": m.completed,
                    "completed_at": m.completed_at
                }
                for m in project.milestones
            ],
            "created_at": project.created_at,
            "updated_at": project.updated_at,
            "related_work_efforts": project.related_work_efforts
        }

    def log_message(self, format, *args):
        """Suppress default logging."""
        pass


def create_handler(project_path: Path):
    """Create handler with project path."""
    def handler(*args, **kwargs):
        return ProjectsDashboardHandler(project_path, *args, **kwargs)
    return handler


def serve(project_path: Path = None, port: int = 8080, host: str = "localhost"):
    """Start the dashboard server."""
    if project_path is None:
        project_path = Path.cwd()
    else:
        project_path = Path(project_path)

    print(f"\n🌊 WAFT Projects Dashboard")
    print(f"📍 Serving at http://{host}:{port}")
    print(f"📁 Project: {project_path.resolve()}")
    print(f"\nPress Ctrl+C to stop\n")

    handler = create_handler(project_path)
    server = HTTPServer((host, port), handler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down server...")
        server.shutdown()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="WAFT Projects Dashboard Server")
    parser.add_argument("--path", "-p", type=str, help="Project path (default: current)")
    parser.add_argument("--port", type=int, default=8080, help="Port to serve on (default: 8080)")
    parser.add_argument("--host", type=str, default="localhost", help="Host to bind to (default: localhost)")

    args = parser.parse_args()

    project_path = Path(args.path) if args.path else Path.cwd()
    serve(project_path, args.port, args.host)
