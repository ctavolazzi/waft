"""
ODD research notes endpoints.
"""

import json
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter()

PROJECT_ROOT = Path(__file__).resolve().parents[4]
NOTES_DIR = PROJECT_ROOT / "_realms" / "odd_realm" / "notes"
NOTES_PATH = NOTES_DIR / "odd_research_notes.json"


class OddNoteIn(BaseModel):
    title: str
    summary: str | None = None
    content: str | None = None
    tags: list[str] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)


def _load_notes() -> dict:
    if not NOTES_PATH.exists():
        NOTES_DIR.mkdir(parents=True, exist_ok=True)
        NOTES_PATH.write_text(json.dumps({"notes": []}, indent=2))
    try:
        data = json.loads(NOTES_PATH.read_text())
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=500, detail=f"Invalid notes JSON: {exc}") from exc
    if not isinstance(data, dict) or "notes" not in data:
        data = {"notes": []}
    return data


def _save_notes(data: dict) -> None:
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    NOTES_PATH.write_text(json.dumps(data, indent=2))


@router.get("/odd/notes")
async def list_notes():
    data = _load_notes()
    return {"notes": data.get("notes", [])}


@router.post("/odd/notes", status_code=status.HTTP_201_CREATED)
async def create_note(note: OddNoteIn):
    data = _load_notes()
    now = datetime.now()
    record = {
        "id": now.strftime("%Y%m%dT%H%M%S%f"),
        "title": note.title,
        "summary": note.summary or "",
        "content": note.content or "",
        "tags": note.tags,
        "sources": note.sources,
        "created_at": now.isoformat(),
    }
    data.setdefault("notes", []).insert(0, record)
    _save_notes(data)
    return record
