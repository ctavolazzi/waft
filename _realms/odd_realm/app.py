"""
ODD Realm - FastAPI Live Server
Ontological Determinism Department Web Interface
Port: 6666
"""

import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

# Get the directory where this script lives
BASE_DIR = Path(__file__).parent.resolve()

app = FastAPI(
    title="ODD - Ontological Determinism Department",
    description="Reality Stability Monitoring Interface",
    version="0.1.0"
)

# Mount static directories
app.mount("/assets", StaticFiles(directory=BASE_DIR / "assets"), name="assets")
app.mount("/output", StaticFiles(directory=BASE_DIR / "output"), name="output")
app.mount("/beings", StaticFiles(directory=BASE_DIR / "beings"), name="beings")

# Serve the main index.html
@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main ODD interface"""
    index_path = BASE_DIR / "index.html"
    return FileResponse(index_path)

# Serve gallery.html
@app.get("/gallery", response_class=HTMLResponse)
@app.get("/gallery.html", response_class=HTMLResponse)
async def gallery():
    """Serve the asset gallery"""
    gallery_path = BASE_DIR / "gallery.html"
    return FileResponse(gallery_path)

# API endpoint for reality stability (can be extended)
@app.get("/api/stability")
async def get_stability():
    """Get current reality stability index"""
    import random
    return {
        "stability": round(0.7 + random.random() * 0.29, 2),
        "status": "MONITORED",
        "department": "ODD"
    }

# Health check
@app.get("/api/health")
async def health():
    return {"status": "operational", "realm": "odd"}

if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║         O.D.D. - Ontological Determinism Department       ║
    ║                   Reality Interface v0.1                  ║
    ╚═══════════════════════════════════════════════════════════╝
    
    🜏 Server starting on http://localhost:6660
    🜏 Say hello to yourself.
    """)
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=6660,
        reload=True,
        reload_dirs=[str(BASE_DIR)]
    )
