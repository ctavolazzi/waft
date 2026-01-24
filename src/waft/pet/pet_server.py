"""
Standalone FastAPI server for the WAFT Pet System.
"""

from pathlib import Path

from fastapi import FastAPI

from waft.api.routes import pet as pet_routes


def create_app(project_path: Path | None = None) -> FastAPI:
    app = FastAPI(title="WAFT Pet Server", version="0.1.0")
    app.state.project_path = Path(project_path or Path.cwd())
    app.include_router(pet_routes.router, prefix="/pet", tags=["pet"])
    return app


app = create_app()
