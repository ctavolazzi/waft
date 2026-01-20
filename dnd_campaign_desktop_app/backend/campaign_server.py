"""
D&D Campaign Desktop App - FastAPI Backend Server

Self-running, self-monitoring D&D campaign backend.
Wraps CampaignOrchestrator with FastAPI for Electron integration.
"""

import asyncio
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import uvicorn
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Add parent directory to path to import CampaignOrchestrator
sys.path.insert(
    0,
    str(
        Path(__file__).parent.parent.parent
        / "_work_efforts"
        / "WE-260113-wfbu_ai_dm_system_d_d_5e_campaign_orchestrator_with_story_booklet_generation"
        / "src"
    ),
)

try:
    from campaign_orchestrator import CampaignOrchestrator
    from campaign_state import CampaignSession, CampaignState, CampaignStatus, SessionStatus
except ImportError as e:
    print(f"Warning: Could not import CampaignOrchestrator: {e}")
    CampaignOrchestrator = None

# Import monitoring system
from monitoring import EventType, init_monitoring
from monitoring_api import router as monitoring_router

app = FastAPI(title="D&D Campaign Desktop App API")

# CORS for Electron
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Electron app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include monitoring router
app.include_router(monitoring_router)

# Global state
campaign_manager = None
project_path = Path.cwd()
active_campaigns: dict[str, dict[str, Any]] = {}
websocket_connections: list[WebSocket] = []


class CampaignCreateRequest(BaseModel):
    campaign_name: str
    scenario_file: str | None = None
    description: str = ""
    difficulty: str = "medium"


class CampaignStartRequest(BaseModel):
    campaign_id: str
    session_number: int | None = None


class DMDecisionRequest(BaseModel):
    campaign_id: str
    problem: str
    alternatives: list[str]
    criteria: dict[str, float]
    scores: dict[str, dict[str, float]]


class SelfMonitoringCampaign:
    """Wrapper around CampaignOrchestrator with self-monitoring."""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.orchestrator = None
        self.running = False
        self.metrics = {"turns_completed": 0, "errors": 0, "uptime": 0, "started_at": None}
        self._initialize_orchestrator()

    def _initialize_orchestrator(self):
        """Initialize CampaignOrchestrator."""
        if CampaignOrchestrator is None:
            raise RuntimeError("CampaignOrchestrator not available")
        self.orchestrator = CampaignOrchestrator(self.project_path)

    async def run_campaign(self, campaign_id: str):
        """Run campaign with self-monitoring."""
        self.running = True
        self.metrics["started_at"] = datetime.now().isoformat()

        try:
            # Start campaign session
            session = self.orchestrator.run_session(campaign_id)

            # Broadcast campaign start
            await self._broadcast_event(
                {
                    "type": "campaign_started",
                    "campaign_id": campaign_id,
                    "session_id": session.session_id,
                    "timestamp": datetime.now().isoformat(),
                }
            )

            # TODO: Run actual campaign loop here
            # For now, just mark as running

        except Exception as e:
            self.metrics["errors"] += 1
            await self._broadcast_event(
                {
                    "type": "campaign_error",
                    "campaign_id": campaign_id,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                }
            )
        finally:
            self.running = False

    async def _broadcast_event(self, event: dict[str, Any]):
        """Broadcast event to all WebSocket connections."""
        disconnected = []
        for ws in websocket_connections:
            try:
                await ws.send_json(event)
            except:
                disconnected.append(ws)

        # Remove disconnected connections
        for ws in disconnected:
            if ws in websocket_connections:
                websocket_connections.remove(ws)


# Initialize monitoring
monitoring = init_monitoring(project_path, component="backend")

# Initialize campaign manager
try:
    campaign_manager = SelfMonitoringCampaign(project_path)
    backend_start_time = (time.time() - monitoring.start_time) * 1000

    # Record first startup
    if monitoring.is_first_startup:
        monitoring.record_first_startup(
            backend_start_time=backend_start_time,
            health_check_passed=False,  # Will be updated after first health check
        )
        monitoring.record_event(EventType.BACKEND_START)
except Exception as e:
    print(f"Warning: Could not initialize campaign manager: {e}")
    if monitoring:
        monitoring.record_error("initialization_error", str(e))


@app.get("/api/health")
async def health():
    """Health check endpoint."""
    health_check_start = time.time()

    if campaign_manager is None:
        status = {
            "status": "unhealthy",
            "message": "Campaign manager not initialized",
            "orchestrator_available": CampaignOrchestrator is not None,
        }
        if monitoring:
            monitoring.record_metric(
                "health_check_duration", (time.time() - health_check_start) * 1000
            )
        return status

    health_check_passed = True
    status = {
        "status": "healthy",
        "running": campaign_manager.running,
        "metrics": campaign_manager.metrics,
        "orchestrator_available": CampaignOrchestrator is not None,
    }

    # Record health check metric
    if monitoring:
        duration_ms = (time.time() - health_check_start) * 1000
        monitoring.record_metric("health_check_duration", duration_ms)
        monitoring.record_event(EventType.HEALTH_CHECK, {"passed": health_check_passed})

        # Update startup data if first startup
        if monitoring.is_first_startup and monitoring.startup_data:
            monitoring.startup_data.health_check_passed = health_check_passed
            with open(monitoring.startup_data_file, "w") as f:
                from dataclasses import asdict

                json.dump(asdict(monitoring.startup_data), f, indent=2)

    return status


@app.get("/api/campaigns")
async def list_campaigns():
    """List all campaigns."""
    if campaign_manager is None or campaign_manager.orchestrator is None:
        raise HTTPException(status_code=503, detail="Campaign orchestrator not available")

    # TODO: Get campaigns from state manager
    return {"campaigns": list(active_campaigns.values()), "count": len(active_campaigns)}


@app.get("/api/campaigns/{campaign_id}")
async def get_campaign(campaign_id: str):
    """Get campaign details."""
    if campaign_manager is None or campaign_manager.orchestrator is None:
        raise HTTPException(status_code=503, detail="Campaign orchestrator not available")

    if campaign_id not in active_campaigns:
        raise HTTPException(status_code=404, detail="Campaign not found")

    return active_campaigns[campaign_id]


@app.post("/api/campaigns")
async def create_campaign(request: CampaignCreateRequest):
    """Create a new campaign."""
    if campaign_manager is None or campaign_manager.orchestrator is None:
        raise HTTPException(status_code=503, detail="Campaign orchestrator not available")

    try:
        campaign = campaign_manager.orchestrator.start_campaign(
            campaign_name=request.campaign_name,
            scenario_file=request.scenario_file,
            description=request.description,
            difficulty=request.difficulty,
        )

        active_campaigns[campaign.campaign_id] = {
            "campaign_id": campaign.campaign_id,
            "campaign_name": campaign.campaign_name,
            "status": campaign.status.value
            if hasattr(campaign.status, "value")
            else str(campaign.status),
            "created_at": campaign.created_at,
            "description": campaign.description,
        }

        # Record feature access
        if monitoring:
            monitoring.record_feature_access("campaign_create")
            monitoring.record_event(
                EventType.CAMPAIGN_CREATED,
                {"campaign_id": campaign.campaign_id, "campaign_name": campaign.campaign_name},
            )

        await campaign_manager._broadcast_event(
            {
                "type": "campaign_created",
                "campaign_id": campaign.campaign_id,
                "campaign_name": campaign.campaign_name,
                "timestamp": datetime.now().isoformat(),
            }
        )

        return campaign
    except Exception as e:
        if monitoring:
            monitoring.record_error("campaign_creation_error", str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/campaigns/{campaign_id}/start")
async def start_campaign(campaign_id: str):
    """Start running a campaign."""
    if campaign_manager is None or campaign_manager.orchestrator is None:
        raise HTTPException(status_code=503, detail="Campaign orchestrator not available")

    if campaign_id not in active_campaigns:
        raise HTTPException(status_code=404, detail="Campaign not found")

    # Run campaign in background
    asyncio.create_task(campaign_manager.run_campaign(campaign_id))

    return {"status": "started", "campaign_id": campaign_id, "message": "Campaign started"}


@app.get("/api/campaigns/stats")
async def get_stats():
    """Get campaign statistics."""
    if campaign_manager is None:
        return {"total_campaigns": 0, "active_campaigns": 0, "running_campaigns": 0, "metrics": {}}

    running = sum(1 for c in active_campaigns.values() if c.get("status") == "active")

    return {
        "total_campaigns": len(active_campaigns),
        "active_campaigns": running,
        "running_campaigns": 1 if campaign_manager.running else 0,
        "metrics": campaign_manager.metrics,
    }


@app.websocket("/ws/campaign")
async def campaign_websocket(websocket: WebSocket):
    """WebSocket for real-time campaign updates."""
    await websocket.accept()
    websocket_connections.append(websocket)

    try:
        # Send initial state
        await websocket.send_json(
            {
                "type": "connected",
                "timestamp": datetime.now().isoformat(),
                "active_campaigns": len(active_campaigns),
            }
        )

        # Keep connection alive
        while True:
            try:
                data = await websocket.receive_text()
                # Echo back (can add command handling here)
                await websocket.send_json(
                    {"type": "echo", "data": data, "timestamp": datetime.now().isoformat()}
                )
            except WebSocketDisconnect:
                break
    except WebSocketDisconnect:
        pass
    finally:
        if websocket in websocket_connections:
            websocket_connections.remove(websocket)


if __name__ == "__main__":
    # Get project path from environment or use current directory
    project_path = Path(os.getenv("WAFT_PROJECT_PATH", Path.cwd()))

    print("Starting D&D Campaign Desktop App Backend...")
    print(f"Project path: {project_path}")
    print(f"CampaignOrchestrator available: {CampaignOrchestrator is not None}")

    uvicorn.run("campaign_server:app", host="127.0.0.1", port=8000, reload=True, log_level="info")
