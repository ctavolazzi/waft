#!/usr/bin/env python3
"""Quick test script for waft web server."""

from pathlib import Path
from src.waft.web import serve

if __name__ == "__main__":
    project_path = Path("_experiments/test_project_001")
    if not project_path.exists():
        project_path = Path(".")

    print(f"Starting server for: {project_path.resolve()}")
    serve(project_path, port=8000)

