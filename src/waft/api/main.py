"""
FastAPI application for Waft Visualizer API.
"""

import logging
import os
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

from .responses import ErrorCodes, ErrorResponse
from .routes import (
    auth,
    being,
    campfire,
    cartographer,
    cyoa,
    dashboard_5050,
    decision,
    empirica,
    evolve_ui_monitor,
    git,
    gym,
    health,
    oracle,
    odd_notes,
    ollama,
    pet,
    projects,
    protocel,
    quests,
    state,
    storyteller,
    work_efforts,
)

logger = logging.getLogger(__name__)


def _static_file_response(static_dir: Path, full_path: str):
    """Serve a built visualizer asset or the SPA fallback page."""
    static_root = static_dir.resolve()
    requested = (static_root / full_path).resolve() if full_path else static_root

    if not str(requested).startswith(str(static_root)):
        raise HTTPException(status_code=404, detail="Static asset not found")

    if requested.is_dir():
        index_file = requested / "index.html"
        if index_file.exists():
            return FileResponse(str(index_file))

    if requested.exists() and requested.is_file():
        return FileResponse(str(requested))

    if Path(full_path).suffix:
        raise HTTPException(status_code=404, detail="Static asset not found")

    for fallback_name in ("200.html", "index.html"):
        fallback_file = static_root / fallback_name
        if fallback_file.exists():
            return FileResponse(str(fallback_file))

    raise HTTPException(status_code=404, detail="Static fallback not found")


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
        title="WAFT API",
        description="""
        WAFT (Wave Agent Framework & Tools) REST API.

        Provides comprehensive project management, work effort tracking, and system visualization
        capabilities through a RESTful interface.

        ## Features

        - **Projects**: Long-term project management with milestones and progress tracking
        - **Work Efforts**: File-based work effort system with YAML frontmatter
        - **Authentication**: Token-based authentication for write operations
        - **Visualization**: Project state, git status, and analytics

        ## Authentication

        Write operations (POST, PUT, PATCH, DELETE) require authentication via Bearer token.
        Read operations (GET) are publicly accessible.

        Get your token via `/api/auth/handshake` endpoint.
        """,
        version="0.1.0",
        contact={
            "name": "WAFT Team",
            "url": "https://github.com/ctavolazzi/waft",
        },
        license_info={
            "name": "MIT",
        },
        openapi_tags=[
            {
                "name": "projects",
                "description": (
                    "Project management operations. Create, read, update, and delete "
                    "long-term projects."
                ),
            },
            {
                "name": "work-efforts",
                "description": (
                    "Work effort management. Track work efforts with file-based storage "
                    "and YAML frontmatter."
                ),
            },
            {
                "name": "auth",
                "description": "Authentication endpoints for API access.",
            },
            {
                "name": "state",
                "description": "Project state and visualization data.",
            },
            {
                "name": "health",
                "description": "Health check and system status endpoints.",
            },
            {
                "name": "quests",
                "description": (
                    "Quest Guide Implementation system. Gamified quest-based "
                    "development orchestrator."
                ),
            },
        ],
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",  # Default Vite port
            "http://localhost:3000",  # React dev server
            "http://localhost:8781",  # Custom SvelteKit port
            "http://127.0.0.1:8781",  # IPv4 localhost
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Store project path in app state
    app.state.project_path = project_path

    # Exception handlers
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Handle HTTP exceptions with standard error response."""
        error_code = ErrorCodes.BAD_REQUEST
        if exc.status_code == 404:
            error_code = ErrorCodes.NOT_FOUND
        elif exc.status_code == 409:
            error_code = ErrorCodes.CONFLICT
        elif exc.status_code == 401:
            error_code = ErrorCodes.UNAUTHORIZED
        elif exc.status_code >= 500:
            error_code = ErrorCodes.INTERNAL_ERROR

        error_response = ErrorResponse(
            error=error_code,
            message=exc.detail if isinstance(exc.detail, str) else "An error occurred",
            detail=exc.detail if isinstance(exc.detail, dict) else None,
            timestamp=datetime.now().isoformat(),
        )
        return JSONResponse(status_code=exc.status_code, content=error_response.model_dump())

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle Pydantic validation errors."""
        errors = {}
        for error in exc.errors():
            field = ".".join(str(loc) for loc in error["loc"] if loc != "body")
            if field not in errors:
                errors[field] = []
            errors[field].append(error["msg"])

        error_response = ErrorResponse(
            error=ErrorCodes.VALIDATION_ERROR,
            message="Request validation failed",
            detail=errors,
            timestamp=datetime.now().isoformat(),
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=error_response.model_dump()
        )

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        """Handle ValueError exceptions."""
        logger.warning(f"ValueError in {request.url.path}: {exc}")
        error_response = ErrorResponse(
            error=ErrorCodes.BAD_REQUEST, message=str(exc), timestamp=datetime.now().isoformat()
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content=error_response.model_dump()
        )

    @app.exception_handler(FileNotFoundError)
    async def file_not_found_handler(request: Request, exc: FileNotFoundError):
        """Handle FileNotFoundError exceptions."""
        logger.warning(f"FileNotFoundError in {request.url.path}: {exc}")
        error_response = ErrorResponse(
            error=ErrorCodes.NOT_FOUND,
            message="Resource not found",
            detail={"path": str(exc)},
            timestamp=datetime.now().isoformat(),
        )
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content=error_response.model_dump()
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle all other exceptions."""
        logger.error(f"Unhandled exception in {request.url.path}: {exc}", exc_info=True)
        error_response = ErrorResponse(
            error=ErrorCodes.INTERNAL_ERROR,
            message="An internal server error occurred",
            timestamp=datetime.now().isoformat(),
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=error_response.model_dump()
        )

    # API routes
    app.include_router(state.router, prefix="/api", tags=["state"])
    app.include_router(git.router, prefix="/api", tags=["git"])
    app.include_router(work_efforts.router, prefix="/api", tags=["work-efforts"])
    app.include_router(empirica.router, prefix="/api", tags=["empirica"])
    app.include_router(decision.router, prefix="/api/decision", tags=["decision"])
    app.include_router(gym.router, prefix="/api", tags=["gym"])
    app.include_router(being.router, prefix="/api/being", tags=["being"])
    app.include_router(pet.router, prefix="/api/pet", tags=["pet"])
    app.include_router(campfire.router, prefix="/api", tags=["campfire"])
    app.include_router(protocel.router, prefix="/api/protocel", tags=["protocel"])
    app.include_router(cartographer.router, prefix="/api", tags=["cartographer"])
    app.include_router(projects.router, prefix="/api", tags=["projects"])
    app.include_router(health.router, prefix="/api", tags=["health"])
    app.include_router(auth.router, prefix="/api", tags=["auth"])
    app.include_router(quests.router, tags=["quests"])
    app.include_router(oracle.router, prefix="/api", tags=["oracle"])
    app.include_router(ollama.router, prefix="/api", tags=["ollama"])
    app.include_router(odd_notes.router, prefix="/api", tags=["odd"])
    app.include_router(evolve_ui_monitor.router, prefix="/api", tags=["evolve-ui"])
    app.include_router(dashboard_5050.router, prefix="/api", tags=["dashboard-5050"])
    app.include_router(cyoa.router, prefix="/api", tags=["cyoa"])
    app.include_router(storyteller.router, prefix="/api", tags=["storyteller"])

    # Serve built visualizer assets if provided (must be last route).
    if static_dir and static_dir.exists():

        @app.api_route("/{full_path:path}", methods=["GET", "HEAD"], include_in_schema=False)
        async def serve_visualizer(full_path: str):
            return _static_file_response(static_dir, full_path)

    return app


# Create default app instance for direct uvicorn usage
# Usage: uvicorn src.waft.api.main:app --reload
app = create_app(project_path=Path(os.getenv("WAFT_PROJECT_PATH", str(Path.cwd()))))
