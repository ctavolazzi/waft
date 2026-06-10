"""
API routes for the SelfExplorer agent.

Exposes start/stop/status/journal/flight-log endpoints so the
dashboard_5050 browser panel can observe the agent in real time.
"""

import asyncio
import logging
from pathlib import Path

from fastapi import APIRouter, Request
from pydantic import BaseModel

from ...core.agent.self_explorer import SelfExplorerAgent, create_self_explorer

logger = logging.getLogger(__name__)
router = APIRouter()

# Module-level singleton — one explorer per server process
_agent: SelfExplorerAgent | None = None
_task: asyncio.Task | None = None


class StartRequest(BaseModel):
    max_steps: int = 20
    model: str = "gemma-4"
    base_url: str = "http://localhost:8080/v1"


class NudgeRequest(BaseModel):
    message: str


@router.post("/self-explorer/start")
async def start_explorer(req: StartRequest, request: Request):
    """Start the SelfExplorer agent OODA loop in background."""
    global _agent, _task

    if _agent and _agent._running:
        return {"status": "already_running", **_agent.get_status()}

    project_path = request.app.state.project_path
    _agent = create_self_explorer(
        project_path=project_path,
        model=req.model,
        base_url=req.base_url,
        max_steps=req.max_steps,
    )

    _task = asyncio.create_task(_agent.run(max_steps=req.max_steps))
    return {"status": "started", **_agent.get_status()}


@router.post("/self-explorer/stop")
async def stop_explorer():
    """Stop the agent after current step."""
    if _agent is None:
        return {"status": "not_running"}
    _agent.stop()
    return {"status": "stopping", **_agent.get_status()}


@router.get("/self-explorer/status")
async def get_status():
    """Current agent state."""
    if _agent is None:
        return {"status": "not_initialized", "running": False}
    return _agent.get_status()


@router.get("/self-explorer/journal")
async def get_journal(limit: int = 50, offset: int = 0):
    """Full journal (thoughts, musings, reflections)."""
    if _agent is None:
        return {"entries": [], "total": 0}
    entries = _agent.state.journal
    total = len(entries)
    sliced = entries[offset : offset + limit]
    return {"entries": sliced, "total": total, "offset": offset}


@router.get("/self-explorer/flight-log")
async def get_flight_log(limit: int = 50):
    """Flight recorder events."""
    if _agent is None:
        return {"events": [], "total": 0}
    events = [
        {
            "timestamp": e.timestamp.isoformat(),
            "event_type": e.event_type.value,
            "genome_id": e.genome_id[:16],
            "payload": e.payload,
        }
        for e in _agent.flight_recorder[-limit:]
    ]
    return {"events": events, "total": len(_agent.flight_recorder)}


@router.post("/self-explorer/nudge")
async def nudge_explorer(req: NudgeRequest):
    """Send a message to the agent's inbox."""
    if _agent is None:
        return {"status": "not_initialized"}
    from ...core.agent.state import Message, MessageRole

    _agent.state.inbox.append(
        Message(role=MessageRole.USER, content=req.message)
    )
    return {"status": "nudged", "inbox_size": len(_agent.state.inbox)}
