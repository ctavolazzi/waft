#!/usr/bin/env python3
"""
🎮 Quest Guide Server

A standalone FastAPI server for the Quest Guide Implementation system.

Usage:
    python3 scripts/quest_server.py [--port 8001] [--host localhost]

This starts a web server that provides a REST API for managing quests,
checkpoints, and tests.
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Import quest routes
from waft.api.routes import quests


def create_quest_app(project_path: Path) -> FastAPI:
    """Create FastAPI app for quest system."""
    app = FastAPI(
        title="Quest Guide API",
        description="""
        🎮 Quest Guide Implementation API

        A gamified quest system for implementing the Meta-Cognitive Guide LLM System.

        Features:
        - 17 quests with checkpoints and tests
        - XP system and achievements
        - Progress tracking
        - RESTful API for all operations
        """,
        version="1.0.0",
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins for standalone server
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Store project path
    app.state.project_path = project_path

    # Include quest router
    app.include_router(quests.router)

    @app.get("/")
    async def root():
        """Root endpoint with API information."""
        return JSONResponse(
            {
                "name": "Quest Guide API",
                "version": "1.0.0",
                "description": "🎮 Quest-based implementation orchestrator",
                "endpoints": {
                    "status": "/api/quests/status",
                    "list_quests": "/api/quests",
                    "get_quest": "/api/quests/{quest_id}",
                    "start_quest": "POST /api/quests/{quest_id}/start",
                    "complete_quest": "POST /api/quests/{quest_id}/complete",
                    "check_checkpoint": "POST /api/quests/checkpoints/{checkpoint_id}/check",
                    "run_test": "POST /api/quests/tests/{test_id}/run",
                },
                "docs": "/docs",
                "openapi": "/openapi.json",
            }
        )

    return app


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Quest Guide Server")
    parser.add_argument(
        "--port", type=int, default=8001, help="Port to run server on (default: 8001)"
    )
    parser.add_argument(
        "--host", type=str, default="localhost", help="Host to bind to (default: localhost)"
    )
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload for development")

    args = parser.parse_args()

    project_path = Path.cwd()
    app = create_quest_app(project_path)

    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║   🎮 Quest Guide Server                                      ║
    ║                                                              ║
    ║   A gamified quest system for implementing the               ║
    ║   Meta-Cognitive Guide LLM System                           ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    print(f"📍 Project: {project_path.resolve()}")
    print(f"🌐 Server: http://{args.host}:{args.port}")
    print(f"📚 API Docs: http://{args.host}:{args.port}/docs")
    print(f"🎮 Quest Status: http://{args.host}:{args.port}/api/quests/status")
    print("\nPress Ctrl+C to stop\n")

    uvicorn.run(app, host=args.host, port=args.port, reload=args.reload)


if __name__ == "__main__":
    main()
