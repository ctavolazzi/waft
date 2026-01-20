#!/usr/bin/env python3
"""
Live Reloading Development Server for Research Simulation

Starts the research simulation server with live reloading enabled.
Watches for changes in:
- research_simulation_server.py
- WAFT evolution modules
- LaTeX generator modules
- Research tools

Usage:
    python3 scripts/dev_research_server.py
    # Or with custom port:
    python3 scripts/dev_research_server.py --port 8001
"""

import argparse
import sys
import time
import webbrowser
from pathlib import Path


def main():
    """Start development server with live reloading."""
    parser = argparse.ArgumentParser(
        description="Start research simulation server with live reloading"
    )
    parser.add_argument("--port", type=int, default=8001, help="Port to run on (default: 8001)")
    parser.add_argument(
        "--host", type=str, default="0.0.0.0", help="Host to bind to (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--no-browser", action="store_true", help="Don't open browser automatically"
    )
    args = parser.parse_args()

    project_root = Path(__file__).parent.parent

    print("🔬 Starting Research Simulation Server (Development Mode)")
    print(f"📍 Server will be available at http://localhost:{args.port}")
    print("🔄 Live reloading enabled - server will restart on code changes")
    print("\nWatching for changes in:")
    print("  - scripts/research_simulation_server.py")
    print("  - src/waft/evolution/")
    print("  - src/waft/evolution/latex_generator.py (when created)")
    print("  - src/waft/evolution/pdf_research_tool.py")
    print("\nPress Ctrl+C to stop\n")

    if not args.no_browser:
        # Wait a moment for server to start
        time.sleep(2)
        webbrowser.open(f"http://localhost:{args.port}")

    # Import uvicorn and run with reload
    try:
        import uvicorn

        # Files to watch for changes
        watch_files = [
            str(project_root / "scripts" / "research_simulation_server.py"),
            str(project_root / "src" / "waft" / "evolution"),
        ]

        # Start server with reload enabled
        uvicorn.run(
            "research_simulation_server:app",
            host=args.host,
            port=args.port,
            reload=True,
            reload_dirs=[
                str(project_root / "scripts"),
                str(project_root / "src" / "waft" / "evolution"),
            ],
            reload_includes=["*.py"],
            log_level="info",
        )
    except ImportError:
        print("❌ Error: uvicorn not installed")
        print("   Install with: pip install uvicorn[standard]")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down server...")
        sys.exit(0)


if __name__ == "__main__":
    main()
