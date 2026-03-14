"""
Interactive Demo Pages - showcases every WAFT API feature.
"""

from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

DEMO_HTML = Path(__file__).parent / "demo_page.html"
NARRATIVE_HTML = Path(__file__).parent / "narrative_page.html"


@router.get("/demo", response_class=HTMLResponse, include_in_schema=False)
async def demo_page():
    """Serve the interactive demo page."""
    return HTMLResponse(content=DEMO_HTML.read_text(encoding="utf-8"))


@router.get("/demo/narrative", response_class=HTMLResponse, include_in_schema=False)
async def narrative_page():
    """Serve the narrative cycle page."""
    return HTMLResponse(content=NARRATIVE_HTML.read_text(encoding="utf-8"))
