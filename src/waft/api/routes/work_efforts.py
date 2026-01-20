"""
Work efforts API endpoints.
"""

from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status

from ...api.dependencies import get_project_path, require_auth
from ...api.schemas.work_efforts import (
    WorkEffortCreateRequest,
    WorkEffortListResponse,
    WorkEffortPatchRequest,
    WorkEffortResponse,
    WorkEffortUpdateRequest,
)
from ...api.services.work_effort_service import WorkEffortService

router = APIRouter()


@router.get("/work-efforts", response_model=WorkEffortListResponse)
async def get_work_efforts(
    request: Request,
    status: str | None = Query(None, description="Filter by status"),
    tags: str | None = Query(None, description="Comma-separated tags to filter by"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of results"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
):
    """
    Get list of work efforts with filtering and pagination.

    Supports filtering by status and tags, with pagination support.
    """
    project_path: Path = get_project_path(request)
    service = WorkEffortService(project_path)

    try:
        # Parse tags if provided
        tag_list = [t.strip() for t in tags.split(",")] if tags else None

        work_efforts, total = service.list_work_efforts(
            status=status, tags=tag_list, limit=limit, offset=offset
        )

        # Convert to response models
        items = [
            WorkEffortResponse(
                id=we.get("id", ""),
                title=we.get("title", ""),
                description=we.get("description", ""),
                status=we.get("status", "active"),
                tags=we.get("tags", []),
                created=we.get("created", ""),
                created_by=we.get("created_by"),
                last_updated=we.get("last_updated", ""),
                path=we.get("path", ""),
            )
            for we in work_efforts
        ]

        return WorkEffortListResponse(
            items=items, total=total, limit=limit, offset=offset, has_more=offset + limit < total
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/work-efforts/{work_effort_id}", response_model=WorkEffortResponse)
async def get_work_effort(work_effort_id: str, request: Request):
    """
    Get a specific work effort by ID.

    Work effort ID format: WE-YYMMDD-xxxx
    """
    project_path: Path = get_project_path(request)
    service = WorkEffortService(project_path)

    try:
        work_effort = service.get_work_effort(work_effort_id)
        if not work_effort:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Work effort not found: {work_effort_id}",
            )

        return WorkEffortResponse(
            id=work_effort.get("id", ""),
            title=work_effort.get("title", ""),
            description=work_effort.get("description", ""),
            status=work_effort.get("status", "active"),
            tags=work_effort.get("tags", []),
            created=work_effort.get("created", ""),
            created_by=work_effort.get("created_by"),
            last_updated=work_effort.get("last_updated", ""),
            path=work_effort.get("path", ""),
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post(
    "/work-efforts",
    response_model=WorkEffortResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new work effort",
    response_description="The created work effort with generated ID",
    responses={
        201: {"description": "Work effort created successfully"},
        401: {"description": "Authentication required"},
        422: {"description": "Validation error - invalid input data"},
    },
    operation_id="create_work_effort",
)
async def create_work_effort(
    request: Request, work_effort_data: WorkEffortCreateRequest, token: str = Depends(require_auth)
):
    """
    Create a new work effort.

    Requires authentication via Bearer token.

    Creates a new work effort with the provided title, description, status, and tags.
    The work effort ID is automatically generated in the format `WE-YYMMDD-xxxx` where:
    - `YYMMDD` is the current date
    - `xxxx` is a random 4-character alphanumeric suffix

    Creates the directory structure:
    - `_work_efforts/WE-YYMMDD-xxxx_slug/`
    - `WE-YYMMDD-xxxx_index.md` with YAML frontmatter
    - `tickets/` subdirectory

    **Request Body:**
    - `title` (required): Work effort title (1-200 characters)
    - `description` (optional): Work effort description (max 10,000 characters)
    - `status` (optional): Initial status - "active", "paused", or "completed" (default: "active")
    - `tags` (optional): List of tags (max 20 tags)

    **Response:**
    Returns the created work effort with all fields including generated ID, timestamps, and path.
    """
    project_path: Path = get_project_path(request)
    service = WorkEffortService(project_path)

    try:
        # Validate status
        valid_statuses = ["active", "paused", "completed"]
        if work_effort_data.status not in valid_statuses:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Invalid status: {work_effort_data.status}. Must be one of: {valid_statuses}",
            )

        # Create work effort
        work_effort = service.create_work_effort(
            title=work_effort_data.title,
            description=work_effort_data.description,
            status=work_effort_data.status,
            tags=work_effort_data.tags,
        )

        return WorkEffortResponse(
            id=work_effort["id"],
            title=work_effort["title"],
            description=work_effort.get("description", ""),
            status=work_effort["status"],
            tags=work_effort.get("tags", []),
            created=work_effort["created"],
            created_by=work_effort.get("created_by"),
            last_updated=work_effort["last_updated"],
            path=work_effort["path"],
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/work-efforts/{work_effort_id}", response_model=WorkEffortResponse)
async def update_work_effort(
    work_effort_id: str,
    request: Request,
    work_effort_data: WorkEffortUpdateRequest,
    token: str = Depends(require_auth),
):
    """
    Update a work effort (full update).

    Requires authentication. All provided fields will replace existing values.
    """
    project_path: Path = get_project_path(request)
    service = WorkEffortService(project_path)

    try:
        # Validate work effort exists
        existing = service.get_work_effort(work_effort_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Work effort not found: {work_effort_id}",
            )

        # Build updates dict (only include provided fields)
        updates = {}
        if work_effort_data.title is not None:
            updates["title"] = work_effort_data.title
        if work_effort_data.description is not None:
            updates["description"] = work_effort_data.description
        if work_effort_data.status is not None:
            valid_statuses = ["active", "paused", "completed"]
            if work_effort_data.status not in valid_statuses:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Invalid status: {work_effort_data.status}",
                )
            updates["status"] = work_effort_data.status
        if work_effort_data.tags is not None:
            updates["tags"] = work_effort_data.tags

        # Update work effort
        updated = service.update_work_effort(work_effort_id, updates)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Work effort not found: {work_effort_id}",
            )

        return WorkEffortResponse(
            id=updated.get("id", ""),
            title=updated.get("title", ""),
            description=updated.get("description", ""),
            status=updated.get("status", "active"),
            tags=updated.get("tags", []),
            created=updated.get("created", ""),
            created_by=updated.get("created_by"),
            last_updated=updated.get("last_updated", ""),
            path=updated.get("path", ""),
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch("/work-efforts/{work_effort_id}", response_model=WorkEffortResponse)
async def patch_work_effort(
    work_effort_id: str,
    request: Request,
    work_effort_data: WorkEffortPatchRequest,
    token: str = Depends(require_auth),
):
    """
    Partially update a work effort.

    Requires authentication. Only provided fields will be updated.
    """
    project_path: Path = get_project_path(request)
    service = WorkEffortService(project_path)

    try:
        # Validate work effort exists
        existing = service.get_work_effort(work_effort_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Work effort not found: {work_effort_id}",
            )

        # Build updates dict (only include provided fields)
        updates = {}
        if work_effort_data.title is not None:
            updates["title"] = work_effort_data.title
        if work_effort_data.description is not None:
            updates["description"] = work_effort_data.description
        if work_effort_data.status is not None:
            valid_statuses = ["active", "paused", "completed"]
            if work_effort_data.status not in valid_statuses:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Invalid status: {work_effort_data.status}",
                )
            updates["status"] = work_effort_data.status
        if work_effort_data.tags is not None:
            updates["tags"] = work_effort_data.tags

        # Update work effort
        updated = service.update_work_effort(work_effort_id, updates)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Work effort not found: {work_effort_id}",
            )

        return WorkEffortResponse(
            id=updated.get("id", ""),
            title=updated.get("title", ""),
            description=updated.get("description", ""),
            status=updated.get("status", "active"),
            tags=updated.get("tags", []),
            created=updated.get("created", ""),
            created_by=updated.get("created_by"),
            last_updated=updated.get("last_updated", ""),
            path=updated.get("path", ""),
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/work-efforts/{work_effort_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_work_effort(
    work_effort_id: str, request: Request, token: str = Depends(require_auth)
):
    """
    Delete a work effort.

    Requires authentication. This is a destructive operation that removes
    the entire work effort directory structure.
    """
    project_path: Path = get_project_path(request)
    service = WorkEffortService(project_path)

    try:
        # Check if work effort exists
        existing = service.get_work_effort(work_effort_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Work effort not found: {work_effort_id}",
            )

        # Delete work effort
        deleted = service.delete_work_effort(work_effort_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Work effort not found: {work_effort_id}",
            )

        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
