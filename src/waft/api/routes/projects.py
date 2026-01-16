"""
Projects API endpoints.
"""

from fastapi import APIRouter, Request, HTTPException
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel

from ...core.projects import ProjectManager, ProjectStatus, Project, Milestone, ProgressEntry

router = APIRouter()


class ProjectResponse(BaseModel):
    """Project response model."""
    project_id: str
    title: str
    description: str
    status: str
    progress_percent: float
    tags: List[str]
    milestones: List[dict]
    created_at: str
    updated_at: str
    related_work_efforts: List[str]

    class Config:
        from_attributes = True


class StatsResponse(BaseModel):
    """Statistics response model."""
    total_projects: int
    active_projects: int
    avg_progress: float
    total_milestones: int


@router.get("/projects", response_model=List[ProjectResponse])
async def get_projects(request: Request):
    """
    Get all projects.

    Returns list of all projects with optional filtering.
    """
    project_path: Path = request.app.state.project_path
    manager = ProjectManager(project_path)

    try:
        projects = manager.list_projects()
        return [
            ProjectResponse(
                project_id=p.project_id,
                title=p.title,
                description=p.description,
                status=p.status.value,
                progress_percent=p.progress_percent,
                tags=p.tags,
                milestones=[m.to_dict() for m in p.milestones],
                created_at=p.created_at,
                updated_at=p.updated_at,
                related_work_efforts=p.related_work_efforts
            )
            for p in projects
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str, request: Request):
    """
    Get a specific project by ID.
    """
    project_path: Path = request.app.state.project_path
    manager = ProjectManager(project_path)

    try:
        project = manager.get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail=f"Project not found: {project_id}")

        return ProjectResponse(
            project_id=project.project_id,
            title=project.title,
            description=project.description,
            status=project.status.value,
            progress_percent=project.progress_percent,
            tags=project.tags,
            milestones=[m.to_dict() for m in project.milestones],
            created_at=project.created_at,
            updated_at=project.updated_at,
            related_work_efforts=project.related_work_efforts
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/projects/stats", response_model=StatsResponse)
async def get_projects_stats(request: Request):
    """
    Get projects statistics.
    """
    project_path: Path = request.app.state.project_path
    manager = ProjectManager(project_path)

    try:
        projects = manager.list_projects()
        total = len(projects)
        active = len([p for p in projects if p.status == ProjectStatus.ACTIVE])
        avg_progress = sum(p.progress_percent for p in projects) / total if total > 0 else 0.0
        total_milestones = sum(len(p.milestones) for p in projects)

        return StatsResponse(
            total_projects=total,
            active_projects=active,
            avg_progress=round(avg_progress, 1),
            total_milestones=total_milestones
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
