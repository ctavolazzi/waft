"""
Pydantic schemas for Work Efforts API.

Defines request and response models for work effort management endpoints.
"""

from pydantic import BaseModel, Field


class WorkEffortCreateRequest(BaseModel):
    """Request model for creating a new work effort."""

    title: str = Field(..., min_length=1, max_length=200, description="Work effort title")
    description: str = Field(default="", max_length=10000, description="Work effort description")
    status: str = Field(default="active", description="Initial status (active, paused, completed)")
    tags: list[str] = Field(default_factory=list, max_items=20, description="Work effort tags")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "API Enhancement",
                "description": "Enhance the API with CRUD operations",
                "status": "active",
                "tags": ["api", "backend"],
            }
        }


class WorkEffortUpdateRequest(BaseModel):
    """Request model for full work effort update (PUT)."""

    title: str | None = Field(None, min_length=1, max_length=200, description="Work effort title")
    description: str | None = Field(None, max_length=10000, description="Work effort description")
    status: str | None = Field(None, description="Work effort status")
    tags: list[str] | None = Field(None, max_items=20, description="Work effort tags")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Updated Work Effort Title",
                "description": "Updated description",
                "status": "paused",
                "tags": ["updated", "tags"],
            }
        }


class WorkEffortPatchRequest(BaseModel):
    """Request model for partial work effort update (PATCH)."""

    title: str | None = Field(None, min_length=1, max_length=200, description="Work effort title")
    description: str | None = Field(None, max_length=10000, description="Work effort description")
    status: str | None = Field(None, description="Work effort status")
    tags: list[str] | None = Field(None, max_items=20, description="Work effort tags")

    class Config:
        json_schema_extra = {"example": {"status": "completed"}}


class WorkEffortResponse(BaseModel):
    """Response model for work effort data."""

    id: str
    title: str
    description: str | None = None
    status: str
    tags: list[str]
    created: str
    created_by: str | None = None
    last_updated: str
    path: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": "WE-260116-xxxx",
                "title": "API Enhancement",
                "description": "Enhance the API with CRUD operations",
                "status": "active",
                "tags": ["api", "backend"],
                "created": "2026-01-16T20:19:00",
                "created_by": "api",
                "last_updated": "2026-01-16T20:19:00",
                "path": "_work_efforts/WE-260116-xxxx_api_enhancement",
            }
        }


class WorkEffortListResponse(BaseModel):
    """Response model for paginated work effort list."""

    items: list[WorkEffortResponse]
    total: int
    limit: int
    offset: int
    has_more: bool

    class Config:
        json_schema_extra = {
            "example": {"items": [], "total": 0, "limit": 50, "offset": 0, "has_more": False}
        }
