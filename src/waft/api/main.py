"""
FastAPI application for Waft Visualizer API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from .routes import state, git, work_efforts, empirica, decision


def create_app(project_path: Path, static_dir: Path | None = None) -> FastAPI:
    """
    Create and configure FastAPI application.

    Args:
        project_path: Path to the Waft project
        static_dir: Optional path to static files (SvelteKit build)

    Returns:
        Configured FastAPI app
    """
    app = FastAPI(
        title="Waft Visualizer API",
        description="API for Waft project visualization dashboard",
        version="0.1.0"
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Store project path in app state
    app.state.project_path = project_path

    # API routes
    app.include_router(state.router, prefix="/api", tags=["state"])
    app.include_router(git.router, prefix="/api", tags=["git"])
    app.include_router(work_efforts.router, prefix="/api", tags=["work-efforts"])
    app.include_router(empirica.router, prefix="/api", tags=["empirica"])
    app.include_router(decision.router, prefix="/api/decision", tags=["decision"])

    # Serve static files if provided (must be last route)
    if static_dir and static_dir.exists():
        # Mount static files, but don't override API routes
        app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")

    return app


# Create default app instance for direct uvicorn usage
# Usage: uvicorn src.waft.api.main:app --reload
app = create_app(project_path=Path.cwd())
