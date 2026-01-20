"""
Projects API endpoints.
"""

import re
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel

from ...api.dependencies import require_auth
from ...api.schemas.projects import (
    ProjectCreateRequest,
    ProjectPatchRequest,
    ProjectResponse,
    ProjectUpdateRequest,
)
from ...core.projects import ProjectManager, ProjectStatus

router = APIRouter()


class StatsResponse(BaseModel):
    """Statistics response model."""

    total_projects: int
    active_projects: int
    avg_progress: float
    total_milestones: int


@router.get("/projects", response_model=list[ProjectResponse])
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
                related_work_efforts=p.related_work_efforts,
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
            related_work_efforts=project.related_work_efforts,
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
            total_milestones=total_milestones,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    request: Request, project_data: ProjectCreateRequest, token: str = Depends(require_auth)
):
    """
    Create a new project.

    Requires authentication.
    """
    project_path: Path = request.app.state.project_path
    manager = ProjectManager(project_path)

    try:
        # Convert status string to enum
        status_enum = ProjectStatus.PLANNING
        if project_data.status:
            try:
                status_enum = ProjectStatus(project_data.status.lower())
            except ValueError:
                # Return 422 directly without raising HTTPException (which gets caught)
                from datetime import datetime

                from fastapi.responses import JSONResponse

                from ...api.responses import ErrorCodes, ErrorResponse

                error_response = ErrorResponse(
                    error=ErrorCodes.VALIDATION_ERROR,
                    message=f"Invalid status: {project_data.status}. Must be one of: {[s.value for s in ProjectStatus]}",
                    timestamp=datetime.now().isoformat(),
                )
                return JSONResponse(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    content=error_response.model_dump(),
                )

        # Create project
        project = manager.create_project(
            title=project_data.title,
            description=project_data.description,
            tags=project_data.tags,
            status=status_enum,
        )

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
            related_work_efforts=project.related_work_efforts,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put(
    "/projects/{project_id}",
    response_model=ProjectResponse,
    summary="Update a project (full update)",
    response_description="The updated project",
    responses={
        200: {"description": "Project updated successfully"},
        401: {"description": "Authentication required"},
        404: {"description": "Project not found"},
        422: {"description": "Validation error"},
    },
    operation_id="update_project",
)
async def update_project(
    project_id: str,
    request: Request,
    project_data: ProjectUpdateRequest,
    token: str = Depends(require_auth),
):
    """
    Update a project (full update).

    Requires authentication via Bearer token.

    Updates all provided fields of the project. Fields not provided will be set to None
    (use PATCH for partial updates).

    **Path Parameters:**
    - `project_id`: The project ID to update

    **Request Body:**
    All fields are optional:
    - `title`: Project title
    - `description`: Project description
    - `tags`: List of tags
    - `status`: Project status
    - `progress_percent`: Progress percentage (0.0-100.0)

    **Response:**
    Returns the updated project with new timestamps.
    """
    project_path: Path = request.app.state.project_path
    manager = ProjectManager(project_path)

    try:
        # Get existing project
        project = manager.get_project(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Project not found: {project_id}"
            )

        # Update fields
        if project_data.title is not None:
            project.title = project_data.title
        if project_data.description is not None:
            project.description = project_data.description
        if project_data.tags is not None:
            project.tags = project_data.tags
        if project_data.status is not None:
            try:
                project.status = ProjectStatus(project_data.status.lower())
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Invalid status: {project_data.status}",
                )
        if project_data.progress_percent is not None:
            project.progress_percent = project_data.progress_percent

        # Save updated project
        manager.update_project(project)

        # Reload to get updated timestamps
        updated_project = manager.get_project(project_id)

        return ProjectResponse(
            project_id=updated_project.project_id,
            title=updated_project.title,
            description=updated_project.description,
            status=updated_project.status.value,
            progress_percent=updated_project.progress_percent,
            tags=updated_project.tags,
            milestones=[m.to_dict() for m in updated_project.milestones],
            created_at=updated_project.created_at,
            updated_at=updated_project.updated_at,
            related_work_efforts=updated_project.related_work_efforts,
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch("/projects/{project_id}", response_model=ProjectResponse)
async def patch_project(
    project_id: str,
    request: Request,
    project_data: ProjectPatchRequest,
    token: str = Depends(require_auth),
):
    """
    Partially update a project.

    Requires authentication. Only provided fields will be updated.
    """
    project_path: Path = request.app.state.project_path
    manager = ProjectManager(project_path)

    try:
        # Get existing project
        project = manager.get_project(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Project not found: {project_id}"
            )

        # Update only provided fields
        if project_data.title is not None:
            project.title = project_data.title
        if project_data.description is not None:
            project.description = project_data.description
        if project_data.tags is not None:
            project.tags = project_data.tags
        if project_data.status is not None:
            try:
                project.status = ProjectStatus(project_data.status.lower())
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Invalid status: {project_data.status}",
                )
        if project_data.progress_percent is not None:
            project.progress_percent = project_data.progress_percent

        # Save updated project
        manager.update_project(project)

        # Reload to get updated timestamps
        updated_project = manager.get_project(project_id)

        return ProjectResponse(
            project_id=updated_project.project_id,
            title=updated_project.title,
            description=updated_project.description,
            status=updated_project.status.value,
            progress_percent=updated_project.progress_percent,
            tags=updated_project.tags,
            milestones=[m.to_dict() for m in updated_project.milestones],
            created_at=updated_project.created_at,
            updated_at=updated_project.updated_at,
            related_work_efforts=updated_project.related_work_efforts,
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: str, request: Request, token: str = Depends(require_auth)):
    """
    Delete a project.

    Requires authentication.
    """
    project_path: Path = request.app.state.project_path
    manager = ProjectManager(project_path)

    try:
        # Check if project exists
        project = manager.get_project(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Project not found: {project_id}"
            )

        # Delete project
        deleted = manager.delete_project(project_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Project not found: {project_id}"
            )

        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def _validate_work_effort_id(work_effort_id: str) -> bool:
    """Validate work effort ID format: WE-YYMMDD-xxxx"""
    pattern = r"^WE-\d{6}-[a-z0-9]{4}$"
    return bool(re.match(pattern, work_effort_id))


@router.post(
    "/projects/{project_id}/work-efforts/{work_effort_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def link_work_effort(
    project_id: str, work_effort_id: str, request: Request, token: str = Depends(require_auth)
):
    """
    Link a work effort to a project.

    Requires authentication.
    """
    project_path: Path = request.app.state.project_path
    manager = ProjectManager(project_path)

    try:
        # Validate work effort ID format
        if not _validate_work_effort_id(work_effort_id):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Invalid work effort ID format: {work_effort_id}. Expected format: WE-YYMMDD-xxxx",
            )

        # Get project
        project = manager.get_project(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Project not found: {project_id}"
            )

        # Add work effort if not already linked
        if work_effort_id not in project.related_work_efforts:
            project.related_work_efforts.append(work_effort_id)
            manager.update_project(project)

        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete(
    "/projects/{project_id}/work-efforts/{work_effort_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def unlink_work_effort(
    project_id: str, work_effort_id: str, request: Request, token: str = Depends(require_auth)
):
    """
    Unlink a work effort from a project.

    Requires authentication.
    """
    project_path: Path = request.app.state.project_path
    manager = ProjectManager(project_path)

    try:
        # Validate work effort ID format
        if not _validate_work_effort_id(work_effort_id):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Invalid work effort ID format: {work_effort_id}. Expected format: WE-YYMMDD-xxxx",
            )

        # Get project
        project = manager.get_project(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Project not found: {project_id}"
            )

        # Remove work effort if linked
        if work_effort_id in project.related_work_efforts:
            project.related_work_efforts.remove(work_effort_id)
            manager.update_project(project)

        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
