#!/usr/bin/env python3
"""
Mission Control & Village API Server

FastAPI backend that serves real data from Mission Control and The Village systems.
"""

import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional
import json

# Add project root to path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.waft.pantheon import MissionControl, TheVillage

app = FastAPI(title="Mission Control & Village API")

# CORS middleware for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize systems
mission_control = MissionControl(project_path=project_root)
village = TheVillage(project_path=project_root)


@app.get("/")
async def root():
    """API root."""
    return {
        "name": "Mission Control & Village API",
        "version": "1.0.0",
        "endpoints": {
            "mission_control": "/api/mission-control",
            "village": "/api/village",
            "mission_status": "/api/mission-control/mission/{mission_id}",
            "gathering": "/api/village/gathering/{gathering_id}"
        }
    }


@app.get("/api/mission-control")
async def get_mission_control_summary():
    """Get Mission Control summary and all mission statuses."""
    try:
        summary = mission_control.get_control_summary()
        all_status = mission_control.get_all_status()
        
        # Load mission names from Military Brass
        from src.waft.pantheon import MilitaryBrass
        brass = MilitaryBrass(project_path=project_root)
        
        # Enhance status with mission names
        enhanced_missions = []
        for status in all_status:
            mission = brass.get_mission(status['mission_id'])
            if mission:
                status['name'] = mission.name
                status['objective'] = mission.objective
            enhanced_missions.append(status)
        
        return {
            "missions_monitored": summary["missions_monitored"],
            "active_commands": summary["active_commands"],
            "active_alerts": summary["active_alerts"],
            "mission_statuses": summary.get("mission_statuses", {}),
            "missions": enhanced_missions,
            "last_update": summary["last_update"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/mission-control/mission/{mission_id}")
async def get_mission_status(mission_id: str):
    """Get detailed status for a specific mission."""
    try:
        status = mission_control.get_status(mission_id)
        if not status:
            raise HTTPException(status_code=404, detail="Mission not found")
        
        # Load mission details from Military Brass
        from src.waft.pantheon import MilitaryBrass
        brass = MilitaryBrass(project_path=project_root)
        mission = brass.get_mission(mission_id)
        
        if mission:
            status['name'] = mission.name
            status['objective'] = mission.objective
            status['classification'] = mission.classification
            status['success_criteria'] = mission.success_criteria
            status['briefing'] = mission.briefing
        
        return status
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/mission-control/command")
async def issue_mission_command(command_data: Dict[str, Any]):
    """Issue a command to a mission."""
    try:
        mission_id = command_data.get("mission_id")
        command = command_data.get("command")
        parameters = command_data.get("parameters", {})
        
        if not mission_id or not command:
            raise HTTPException(status_code=400, detail="mission_id and command required")
        
        result = mission_control.issue_command(
            mission_id=mission_id,
            command=command,
            parameters=parameters
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/village")
async def get_village_summary():
    """Get Village summary and all active gatherings."""
    try:
        summary = village.get_village_summary()
        
        # Load all active gatherings
        import json
        registry = json.loads(village.registry_file.read_text(encoding="utf-8"))
        
        active_gatherings = []
        for gathering_id in registry.get("active_gatherings", []):
            gathering_file = village.gatherings_path / f"{gathering_id}.json"
            if gathering_file.exists():
                gathering_data = json.loads(gathering_file.read_text(encoding="utf-8"))
                if gathering_data.get("status") == "active":
                    active_gatherings.append(gathering_data)
        
        return {
            "active_gatherings": summary["active_gatherings"],
            "total_connections": summary["total_connections"],
            "shared_quests": summary["shared_quests"],
            "collective_wisdom_count": summary["collective_wisdom_count"],
            "gatherings": active_gatherings,
            "last_update": summary["last_update"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/village/gathering/{gathering_id}")
async def get_gathering_details(gathering_id: str):
    """Get detailed information for a specific gathering."""
    try:
        gathering_file = village.gatherings_path / f"{gathering_id}.json"
        
        if not gathering_file.exists():
            raise HTTPException(status_code=404, detail="Gathering not found")
        
        gathering_data = json.loads(gathering_file.read_text(encoding="utf-8"))
        return gathering_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/village/gathering")
async def create_gathering(gathering_data: Dict[str, Any]):
    """Create a new gathering."""
    try:
        topic = gathering_data.get("topic")
        description = gathering_data.get("description", "")
        participants = gathering_data.get("participants", [])
        
        if not topic:
            raise HTTPException(status_code=400, detail="topic required")
        
        result = village.create_gathering(
            topic=topic,
            description=description,
            participants=participants
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/village/insight")
async def add_insight(insight_data: Dict[str, Any]):
    """Add an insight to a gathering."""
    try:
        gathering_id = insight_data.get("gathering_id")
        insight = insight_data.get("insight")
        contributor = insight_data.get("contributor")
        
        if not gathering_id or not insight:
            raise HTTPException(status_code=400, detail="gathering_id and insight required")
        
        result = village.add_insight(
            gathering_id=gathering_id,
            insight=insight,
            contributor=contributor
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    print("\n🚀 Starting Mission Control & Village API Server...")
    print("📡 API available at: http://localhost:8000")
    print("📚 API docs at: http://localhost:8000/docs\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
