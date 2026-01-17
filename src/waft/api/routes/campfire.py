"""
Campfire API routes - Story sharing and management.
"""

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, List
from pathlib import Path

router = APIRouter()


def get_project_path(request: Request) -> Path:
    """Get project path from app state."""
    if hasattr(request.app.state, 'project_path'):
        return request.app.state.project_path
    return Path.cwd()


class StoryInput(BaseModel):
    """Input model for creating a story."""
    story: str
    title: Optional[str] = None
    style: str = "premium"
    narrative_style: str = "medium"
    structure: str = "linear"
    include_oracle: bool = True


class StoryResponse(BaseModel):
    """Response model for story operations."""
    success: bool
    story: dict
    pdf_path: str
    oracle_insights: Optional[dict] = None


@router.post("/campfire/stories", response_model=StoryResponse)
async def create_story(
    story_input: StoryInput,
    request: Request
):
    """
    Gather around the campfire to tell a story.

    Creates a new story using TheCampfire, orchestrating
    TheOracle, Storyteller, and TavernKeeper.
    """
    from ...core.campfire import TheCampfire

    project_path = get_project_path(request)

    try:
        campfire = TheCampfire(project_path)
        result = campfire.gather_around_the_campfire(
            story_input=story_input.story,
            title=story_input.title,
            style=story_input.style,
            narrative_style=story_input.narrative_style,
            structure=story_input.structure,
            include_oracle=story_input.include_oracle,
            save_story=True
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/campfire/stories")
async def list_stories(
    request: Request,
    limit: Optional[int] = None
):
    """
    Get all stories from the campfire.

    Returns list of story metadata, sorted by creation date (newest first).
    """
    from ...core.campfire import TheCampfire

    project_path = get_project_path(request)

    try:
        campfire = TheCampfire(project_path)
        stories = campfire.get_stories(limit=limit)
        return {"stories": stories, "count": len(stories)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/campfire/stories/{story_id}")
async def get_story(
    story_id: str,
    request: Request
):
    """
    Get a specific story by ID.

    Returns story metadata including PDF path and Oracle insights.
    """
    from ...core.campfire import TheCampfire

    project_path = get_project_path(request)

    try:
        campfire = TheCampfire(project_path)
        story = campfire.get_story(story_id)

        if not story:
            raise HTTPException(status_code=404, detail="Story not found")

        return story
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/campfire/stories/{story_id}/content")
async def get_story_content(
    story_id: str,
    request: Request
):
    """
    Get the full content of a story.

    Returns the markdown content of the story.
    """
    from ...core.campfire import TheCampfire

    project_path = get_project_path(request)

    try:
        campfire = TheCampfire(project_path)
        content = campfire.get_story_content(story_id)

        if not content:
            raise HTTPException(status_code=404, detail="Story content not found")

        return {"content": content}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
