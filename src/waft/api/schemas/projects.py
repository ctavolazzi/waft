"""
Pydantic schemas for Projects API.

Defines request and response models for project management endpoints.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class ProjectCreateRequest(BaseModel):
    """Request model for creating a new project."""
    title: str = Field(..., min_length=1, max_length=200, description="Project title")
    description: str = Field(default="", max_length=10000, description="Project description")
    tags: List[str] = Field(default_factory=list, max_items=20, description="Project tags")
    status: str = Field(default="planning", description="Initial project status")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "My New Project",
                "description": "A project for managing long-term work",
                "tags": ["development", "api"],
                "status": "planning"
            }
        }


class ProjectUpdateRequest(BaseModel):
    """Request model for full project update (PUT)."""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Project title")
    description: Optional[str] = Field(None, max_length=10000, description="Project description")
    tags: Optional[List[str]] = Field(None, max_items=20, description="Project tags")
    status: Optional[str] = Field(None, description="Project status")
    progress_percent: Optional[float] = Field(None, ge=0.0, le=100.0, description="Progress percentage")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Updated Project Title",
                "description": "Updated description",
                "tags": ["updated", "tags"],
                "status": "active",
                "progress_percent": 50.0
            }
        }


class ProjectPatchRequest(BaseModel):
    """Request model for partial project update (PATCH)."""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Project title")
    description: Optional[str] = Field(None, max_length=10000, description="Project description")
    tags: Optional[List[str]] = Field(None, max_items=20, description="Project tags")
    status: Optional[str] = Field(None, description="Project status")
    progress_percent: Optional[float] = Field(None, ge=0.0, le=100.0, description="Progress percentage")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "active"
            }
        }


class ProjectResponse(BaseModel):
    """Response model for project data."""
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
        json_schema_extra = {
            "example": {
                "project_id": "proj_20260116_201900",
                "title": "My Project",
                "description": "Project description",
                "status": "active",
                "progress_percent": 25.5,
                "tags": ["development", "api"],
                "milestones": [],
                "created_at": "2026-01-16T20:19:00",
                "updated_at": "2026-01-16T20:19:00",
                "related_work_efforts": ["WE-260116-xxxx"]
            }
        }
