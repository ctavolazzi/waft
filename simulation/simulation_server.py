"""
Simulation Server - Web server for Thoth Realm Simulator

Provides real-time web interface for viewing simulation.
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import time
import os

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from thoth_realm_simulator import ThothRealmSimulator, SimulationState


app = FastAPI(title="Thoth Realm Simulator")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global simulation instances
simulations: Dict[str, ThothRealmSimulator] = {}
active_connections: List[WebSocket] = []
refresh_connections: List[WebSocket] = []

# File watching for auto-refresh
html_file_path = Path(__file__).parent / "simulation_viewer.html"
html_file_mtime = html_file_path.stat().st_mtime if html_file_path.exists() else 0
html_path = html_file_path  # Alias for consistency


@app.get("/")
async def get_index():
    """Serve main HTML page."""
    html_file = Path(__file__).parent / "simulation_viewer.html"
    if html_file.exists():
        return FileResponse(html_file)
    return HTMLResponse("Simulation viewer not found")


@app.get("/favicon.ico")
async def get_favicon():
    """Serve favicon - return empty response to suppress 404 errors."""
    from fastapi.responses import Response
    # Return 200 with empty content instead of 204 to avoid browser warnings
    return Response(content=b"", media_type="image/x-icon", status_code=200)


@app.get("/pantheon")
async def get_pantheon():
    """Serve pantheon page - redirect to pantheon HTML if exists, otherwise 404."""
    project_path = Path(__file__).parent.parent
    pantheon_file = project_path / "scripts" / "pantheon_web.html"
    
    if pantheon_file.exists():
        return FileResponse(pantheon_file)
    
    # Fallback: return a simple redirect message
    return HTMLResponse("""
    <html>
        <head><title>Pantheon</title></head>
        <body style="background: #0a0a0a; color: #00ff00; font-family: monospace; padding: 20px;">
            <h1>🏛️ The Pantheon</h1>
            <p>Pantheon page not found. Run: <code>waft pantheon</code> to generate it.</p>
            <p><a href="/" style="color: #00ffff;">← Back to Thoth Realm Simulator</a></p>
        </body>
    </html>
    """)


@app.post("/api/simulation/create")
async def create_simulation(request: Request):
    """Create a new simulation."""
    try:
        body = await request.json()
        num_realms = body.get('num_realms', 1)
        prime_directives = body.get('prime_directives', None)
        
        project_path = Path(__file__).parent.parent
        
        if num_realms < 1 or num_realms > 10:
            raise HTTPException(status_code=400, detail="num_realms must be between 1 and 10")
        
        if prime_directives is None:
            prime_directives = [
                "Build a system that evolves",
                "Create tools that become aware",
                "Achieve self-improvement",
                "Learn through experience"
            ]
        
        sim = ThothRealmSimulator(project_path=project_path)
        sim.state = SimulationState.INITIALIZING
        
        # Create Realms
        for i in range(num_realms):
            directive = prime_directives[i % len(prime_directives)]
            try:
                sim.create_realm(directive)
            except Exception as e:
                sim._add_event(
                    event_type="error",
                    message=f"Error creating realm: {e}"
                )
        
        simulations[sim.simulation_id] = sim
        
        return {
            "simulation_id": sim.simulation_id,
            "state": sim.get_state()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/simulation/{simulation_id}/start")
async def start_simulation(simulation_id: str, request: Request):
    """Start running simulation."""
    try:
        body = await request.json()
        batch_size = body.get('batch_size', 1)
    except:
        batch_size = 1
    
    sim = simulations.get(simulation_id)
    if not sim:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    if batch_size < 1 or batch_size > 1000:
        raise HTTPException(status_code=400, detail="batch_size must be between 1 and 1000")
    
    sim.state = SimulationState.RUNNING
    
    # Run simulation in background (only if not already running)
    if not hasattr(sim, '_running_task') or sim._running_task.done():
        sim._running_task = asyncio.create_task(run_simulation_loop(sim, batch_size))
    
    return {"status": "started", "simulation_id": simulation_id}


async def run_simulation_loop(sim: ThothRealmSimulator, batch_size: int):
    """Run simulation loop."""
    try:
        while sim.state == SimulationState.RUNNING:
            # Run batch of cycles
            for _ in range(batch_size):
                try:
                    await sim.run_cycle()
                except Exception as e:
                    sim._add_event(
                        event_type="error",
                        message=f"Error in cycle: {e}"
                    )
                await asyncio.sleep(0.01)  # Small delay between cycles
            
            # Broadcast state to all connected clients
            try:
                await broadcast_state(sim)
            except Exception as e:
                print(f"Error broadcasting state: {e}")
            
            await asyncio.sleep(0.5)  # 0.5 second between batches
    except Exception as e:
        sim.state = SimulationState.ERROR
        sim._add_event(
            event_type="error",
            message=f"Simulation loop error: {e}"
        )


async def broadcast_state(sim: ThothRealmSimulator):
    """Broadcast simulation state to all connected clients."""
    state = sim.get_state()
    message = json.dumps({
        "type": "state_update",
        "simulation_id": sim.simulation_id,
        "data": state
    })
    
    disconnected = []
    for connection in active_connections:
        try:
            await connection.send_text(message)
        except:
            disconnected.append(connection)
    
    # Remove disconnected clients
    for conn in disconnected:
        active_connections.remove(conn)


@app.get("/api/simulation/{simulation_id}/state")
async def get_simulation_state(simulation_id: str):
    """Get current simulation state."""
    sim = simulations.get(simulation_id)
    if not sim:
        return {"error": "Simulation not found"}
    
    return sim.get_state()


@app.get("/api/simulations/list")
async def list_simulations():
    """List all past simulations."""
    project_path = Path(__file__).parent.parent
    simulations_dir = project_path / "_simulations"
    
    if not simulations_dir.exists():
        return {"simulations": []}
    
    simulation_list = []
    for sim_dir in sorted(simulations_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
        if not sim_dir.is_dir():
            continue
        
        metadata_file = sim_dir / "metadata.json"
        if metadata_file.exists():
            try:
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                    simulation_list.append(metadata)
            except:
                # If metadata is corrupted, create basic entry
                simulation_list.append({
                    "simulation_id": sim_dir.name,
                    "created_at": datetime.fromtimestamp(sim_dir.stat().st_mtime).isoformat(),
                    "state": "unknown",
                    "cycle": 0,
                    "realms_count": 0,
                    "beings_count": 0,
                    "tools_count": 0,
                    "prime_directives": [],
                    "metrics": {}
                })
    
    return {"simulations": simulation_list}


@app.post("/api/simulation/{simulation_id}/load")
async def load_simulation(simulation_id: str):
    """Load an existing simulation."""
    project_path = Path(__file__).parent.parent
    
    # Check if already loaded
    if simulation_id in simulations:
        return {
            "simulation_id": simulation_id,
            "state": simulations[simulation_id].get_state(),
            "message": "Simulation already loaded"
        }
    
    # Load from disk
    sim = ThothRealmSimulator(project_path=project_path, simulation_id=simulation_id)
    
    # Try to load latest snapshot
    simulations_dir = project_path / "_simulations" / simulation_id
    if simulations_dir.exists():
        snapshot_files = sorted(simulations_dir.glob("snapshot_*.json"), reverse=True)
        if snapshot_files:
            try:
                with open(snapshot_files[0], 'r') as f:
                    snapshot_data = json.load(f)
                    # Restore state from snapshot
                    sim.cycle = snapshot_data.get("cycle", 0)
                    sim.metrics = snapshot_data.get("metrics", sim.metrics)
                    # Note: Realms, beings, tools would need full restoration logic
                    # For now, just load metadata
            except Exception as e:
                return {"error": f"Failed to load snapshot: {e}"}
    
    simulations[simulation_id] = sim
    
    return {
        "simulation_id": simulation_id,
        "state": sim.get_state()
    }


@app.post("/api/simulation/{simulation_id}/pause")
async def pause_simulation(simulation_id: str):
    """Pause simulation."""
    sim = simulations.get(simulation_id)
    if not sim:
        return {"error": "Simulation not found"}
    
    sim.state = SimulationState.PAUSED
    return {"status": "paused"}


@app.post("/api/simulation/{simulation_id}/resume")
async def resume_simulation(simulation_id: str, request: Request):
    """Resume simulation."""
    try:
        body = await request.json()
        batch_size = body.get('batch_size', 1)
    except:
        batch_size = 1
    
    sim = simulations.get(simulation_id)
    if not sim:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    if batch_size < 1 or batch_size > 1000:
        raise HTTPException(status_code=400, detail="batch_size must be between 1 and 1000")
    
    sim.state = SimulationState.RUNNING
    if not hasattr(sim, '_running_task') or sim._running_task.done():
        sim._running_task = asyncio.create_task(run_simulation_loop(sim, batch_size))
    return {"status": "resumed"}


@app.websocket("/ws/{simulation_id}")
async def websocket_endpoint(websocket: WebSocket, simulation_id: str):
    """WebSocket endpoint for real-time updates."""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        # Send initial state
        sim = simulations.get(simulation_id)
        if sim:
            state = sim.get_state()
            await websocket.send_json({
                "type": "state_update",
                "simulation_id": simulation_id,
                "data": state
            })
        
        # Keep connection alive
        while True:
            await websocket.receive_text()
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        active_connections.remove(websocket)


@app.websocket("/ws/refresh")
async def refresh_websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for auto-refresh on file changes."""
    await websocket.accept()
    refresh_connections.append(websocket)
    
    try:
        # Keep connection alive and watch for file changes
        while True:
            # Check if HTML file changed
            global html_file_mtime
            if html_file_path.exists():
                current_mtime = html_file_path.stat().st_mtime
                if current_mtime > html_file_mtime:
                    html_file_mtime = current_mtime
                    await websocket.send_json({
                        "type": "refresh",
                        "message": "File changed, refreshing..."
                    })
            
            await asyncio.sleep(1)  # Check every second
    except WebSocketDisconnect:
        if websocket in refresh_connections:
            refresh_connections.remove(websocket)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
