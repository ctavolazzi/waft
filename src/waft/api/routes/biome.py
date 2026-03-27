"""
Biome bridge endpoints for visualizer polling/SSE.
"""

from datetime import datetime, timezone

from fastapi import APIRouter

router = APIRouter()


@router.get("/biome")
async def biome_snapshot():
    """
    Lightweight biome payload used by the visualizer bridge.
    """
    now = datetime.now(timezone.utc).timestamp()
    return {
        "tick": int(now * 10),
        "time": now,
        "events": [],
    }
