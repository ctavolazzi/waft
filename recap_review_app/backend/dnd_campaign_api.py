"""
DnD Campaign API Endpoints for FastAPI Backend.

Provides REST API for running the self-playing DnD campaign
and streaming state updates.
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from fastapi import BackgroundTasks, FastAPI, HTTPException
from pydantic import BaseModel

# Add project root to path
if Path("/workspace").exists():
    project_root = Path("/workspace")
else:
    project_root = Path(__file__).parent.parent.parent

sys.path.insert(0, str(project_root))

# Import campaign script
campaign_script_path = (
    project_root
    / "_work_efforts"
    / "WE-260115-8vvn_self_playing_dnd_campaign_tavern_to_final_boss"
    / "SELF_PLAYING_CAMPAIGN_ELECTRON.py"
)

# Global campaign state
campaign_state = {
    "status": "idle",  # idle, running, complete
    "message": "Ready to start...",
    "party": [],
    "current_scene": "",
    "encounters": [],
    "log": [],
    "victory": False,
    "started_at": None,
    "completed_at": None,
}

campaign_process = None
campaign_task = None


class CampaignStateResponse(BaseModel):
    """Response model for campaign state."""

    state: dict[str, Any]
    timestamp: str


async def run_campaign_background():
    """Run the campaign in the background and update state."""
    global campaign_state, campaign_process

    try:
        campaign_state["status"] = "running"
        campaign_state["message"] = "🎲 Campaign starting..."
        campaign_state["started_at"] = datetime.now().isoformat()

        # Import and run campaign
        import os
        import subprocess

        # Use API mode script (preferred)
        api_script_path = campaign_script_path.parent / "SELF_PLAYING_CAMPAIGN_API.py"

        if api_script_path.exists():
            campaign_dir = api_script_path.parent
            script_name = api_script_path.name
        else:
            # Fallback to Electron script
            campaign_dir = campaign_script_path.parent
            script_name = campaign_script_path.name

        # Run campaign script with API mode enabled
        # Note: API_URL is the backend URL, which the script uses to send updates
        process = subprocess.Popen(
            ["python3", script_name],
            cwd=str(campaign_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env={**os.environ, "ELECTRON_MODE": "1", "API_URL": "http://127.0.0.1:8000"},
        )

        campaign_process = process

        # Wait for process to complete
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            campaign_state["status"] = "complete"
            campaign_state["message"] = "🎉 Campaign complete!"
            campaign_state["victory"] = True
            campaign_state["completed_at"] = datetime.now().isoformat()
        else:
            campaign_state["status"] = "error"
            campaign_state["message"] = f"Error: {stderr}"

    except Exception as e:
        campaign_state["status"] = "error"
        campaign_state["message"] = f"Error: {str(e)}"
    finally:
        campaign_process = None


def register_dnd_campaign_routes(app: FastAPI):
    """Register DnD campaign API routes."""

    @app.post("/api/dnd-campaign/start")
    async def start_campaign(background_tasks: BackgroundTasks):
        """Start the self-playing DnD campaign."""
        global campaign_state, campaign_task

        if campaign_state["status"] == "running":
            raise HTTPException(status_code=400, detail="Campaign is already running")

        # Reset state
        campaign_state = {
            "status": "running",
            "message": "🎲 Starting campaign...",
            "party": [],
            "current_scene": "Initializing...",
            "encounters": [],
            "log": [],
            "victory": False,
            "started_at": datetime.now().isoformat(),
            "completed_at": None,
        }

        # Start campaign in background
        campaign_task = asyncio.create_task(run_campaign_background())

        return {"success": True, "message": "Campaign started", "state": campaign_state}

    @app.post("/api/dnd-campaign/stop")
    async def stop_campaign():
        """Stop the running campaign."""
        global campaign_state, campaign_process, campaign_task

        if campaign_state["status"] != "running":
            raise HTTPException(status_code=400, detail="No campaign is currently running")

        # Kill process if running
        if campaign_process:
            campaign_process.terminate()
            campaign_process = None

        # Cancel task
        if campaign_task:
            campaign_task.cancel()
            campaign_task = None

        campaign_state["status"] = "idle"
        campaign_state["message"] = "Campaign stopped"

        return {"success": True, "message": "Campaign stopped"}

    @app.get("/api/dnd-campaign/state", response_model=CampaignStateResponse)
    async def get_campaign_state():
        """Get current campaign state."""
        return CampaignStateResponse(state=campaign_state, timestamp=datetime.now().isoformat())

    @app.post("/api/dnd-campaign/update")
    async def update_campaign_state(update: dict[str, Any]):
        """Update campaign state (called by Python script)."""
        global campaign_state

        # Update state with provided data
        campaign_state.update(update)

        return {"success": True, "message": "State updated"}
