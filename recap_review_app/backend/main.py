"""
FastAPI Backend for Recap and Review Application.

Provides REST API endpoints for mindspace capture and PDF generation.
"""

import sys
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Add project root to path
# In Docker, workspace is mounted at /workspace
# Locally, use parent directory
if Path("/workspace").exists():
    project_root = Path("/workspace")
else:
    project_root = Path(__file__).parent.parent.parent

# Add to Python path
sys.path.insert(0, str(project_root))

# Verify src directory exists
src_path = project_root / "src"
if not src_path.exists():
    raise ImportError(
        f"WAFT src directory not found at {src_path}. Is workspace mounted correctly?"
    )

from src.waft.core.recap_and_review import RecapAndReviewManager

from .dnd_campaign_api import register_dnd_campaign_routes

app = FastAPI(
    title="Recap and Review API",
    description="API for mindspace documentation and review PDF generation",
    version="1.0.0",
)

# Register DnD campaign routes
register_dnd_campaign_routes(app)

# CORS middleware for Electron frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to Electron app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RecapAndReviewRequest(BaseModel):
    """Request model for recap and review."""

    project_path: str | None = None
    output_path: str | None = None


class RecapAndReviewResponse(BaseModel):
    """Response model for recap and review."""

    success: bool
    markdown_file: str | None = None
    pdf_file: str | None = None
    mindspace_data: dict[str, Any] | None = None
    error: str | None = None


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "recap-and-review-api", "version": "1.0.0"}


@app.post("/api/recap-and-review", response_model=RecapAndReviewResponse)
async def recap_and_review(request: RecapAndReviewRequest):
    """
    Generate mindspace review document and PDF.

    Args:
        request: Recap and review request with project path

    Returns:
        Recap and review response with file paths and data
    """
    try:
        # Resolve project path
        if request.project_path:
            project_path = Path(request.project_path)
        else:
            # Default to workspace (Docker) or project root (local)
            if Path("/workspace").exists():
                project_path = Path("/workspace")
            else:
                project_path = project_root

        if not project_path.exists():
            raise HTTPException(
                status_code=400, detail=f"Project path does not exist: {project_path}"
            )

        # Initialize manager
        manager = RecapAndReviewManager(project_path)

        # Run recap and review
        result = manager.run_recap_and_review(output_path=request.output_path)

        return RecapAndReviewResponse(
            success=result["success"],
            markdown_file=result.get("markdown_file"),
            pdf_file=result.get("pdf_file"),
            mindspace_data=result.get("mindspace_data"),
        )

    except Exception as e:
        return RecapAndReviewResponse(success=False, error=str(e))


@app.get("/api/project-info")
async def get_project_info(project_path: str | None = None):
    """
    Get project information.

    Args:
        project_path: Optional project path

    Returns:
        Project information
    """
    try:
        if project_path:
            path = Path(project_path)
        else:
            path = project_root

        if not path.exists():
            raise HTTPException(status_code=400, detail=f"Project path does not exist: {path}")

        return {
            "project_path": str(path),
            "exists": path.exists(),
            "is_directory": path.is_dir(),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
