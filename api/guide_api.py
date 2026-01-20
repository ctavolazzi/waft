#!/usr/bin/env python3
"""
TheGuide REST API

A FastAPI-based REST API for TheGuide meta-cognitive guidance system.

Features:
- Create guidance sessions
- Query session status
- Get "Why?" explanations
- Stream real-time guidance progress
- Browse session history
- FVCU score analytics

Usage:
    # Start the API server
    uvicorn api.guide_api:app --reload --port 8000

    # Or run directly
    python api/guide_api.py
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from pathlib import Path
import uvicorn
import asyncio
import json
import os
from datetime import datetime

# Add src to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from waft.pantheon import TheGuide, Protocol, EvaluationScores
except ImportError:
    # Fallback to direct import
    import importlib.util
    guide_path = Path(__file__).parent.parent / "src" / "waft" / "pantheon" / "guide.py"
    spec = importlib.util.spec_from_file_location("guide", guide_path)
    guide_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(guide_module)
    TheGuide = guide_module.TheGuide
    Protocol = guide_module.Protocol
    EvaluationScores = guide_module.EvaluationScores

# ============================================================================
# FastAPI App
# ============================================================================

app = FastAPI(
    title="TheGuide API",
    description="Meta-Cognitive Guidance System REST API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Global guide instance (will be configured on startup)
guide_instance: Optional[TheGuide] = None
active_sessions: Dict[str, Dict[str, Any]] = {}

# ============================================================================
# Request/Response Models
# ============================================================================

class GuidanceRequest(BaseModel):
    """Request to start a new guidance session."""
    problem_statement: str = Field(..., description="The problem to solve")
    max_iterations: int = Field(10, ge=1, le=50, description="Maximum iterations")
    quality_threshold: float = Field(0.8, ge=0.0, le=1.0, description="Quality threshold")
    use_partial_context: bool = Field(True, description="Use partial context optimization")
    test_time_scaling: int = Field(1, ge=1, le=10, description="Test-time scaling samples")
    enable_self_rewarding: bool = Field(False, description="Enable self-rewarding")
    enable_self_correction: bool = Field(False, description="Enable self-correction")

class GuidanceResponse(BaseModel):
    """Response from a guidance session."""
    session_id: str
    final_answer: str
    quality_score: float
    iteration_count: int
    created: str
    completed: str

class SessionStatus(BaseModel):
    """Current status of a guidance session."""
    session_id: str
    status: str  # "pending", "running", "completed", "failed"
    current_iteration: Optional[int] = None
    quality_score: Optional[float] = None
    message: str = ""

class FVCUScores(BaseModel):
    """FVCU+Faithfulness scores."""
    factuality: float
    validity: float
    coherence: float
    utility: float
    faithfulness: float
    overall: float

class SessionListItem(BaseModel):
    """Summary of a guidance session."""
    session_id: str
    problem_summary: str
    quality_score: float
    iteration_count: int
    created: str
    completed: Optional[str] = None

# ============================================================================
# Mock LLM for Demo
# ============================================================================

class DemoLLM:
    """Demo LLM that generates realistic responses."""

    def __init__(self, model="demo", api_key=None, base_url=None):
        self.model = model
        self.call_count = 0

    def complete(self, prompt: str) -> str:
        """Generate demo responses based on prompt."""
        self.call_count += 1

        if "meta-cognitive guide" in prompt.lower():
            if "first instruction" in prompt.lower():
                return "Let's start by breaking down the problem into its core components and identifying what we need to understand first."
            else:
                return "Now, let's dive deeper into the specific implementation details and address the gaps we identified."

        elif "follow the instruction" in prompt.lower():
            return """I'll approach this systematically:

1. First, let me identify the key requirements
2. Then, I'll analyze the available approaches
3. Next, I'll evaluate the trade-offs
4. Finally, I'll recommend a solution

Let me work through each step carefully..."""

        elif "meta-cognitive evaluator" in prompt.lower():
            return """{
  "factuality": 0.90,
  "validity": 0.85,
  "coherence": 0.88,
  "utility": 0.92,
  "faithfulness": 0.90,
  "overall": 0.89,
  "rationale": "Strong systematic approach with clear reasoning steps.",
  "strengths": ["Clear structure", "Methodical approach"],
  "weaknesses": ["Could include more specific examples"],
  "recommendations": ["Add concrete examples in next iteration"],
  "should_continue": true,
  "planning_detected": false,
  "unfaithful_reasoning_detected": false
}"""

        elif "final answer" in prompt.lower():
            return """Based on the systematic analysis, here's the recommended solution:

1. Use approach X because it provides the best trade-off between simplicity and effectiveness
2. Implement components A, B, and C in that order
3. Test incrementally at each step
4. Monitor for edge cases and iterate as needed

This solution addresses the core requirements while maintaining flexibility for future changes."""

        return f"Response to prompt (call #{self.call_count})"

# ============================================================================
# Startup/Shutdown
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize TheGuide on startup."""
    global guide_instance

    project_path = Path(__file__).parent.parent

    # Check if we have real API key
    api_key = os.getenv("LLM_API_KEY")
    model = os.getenv("LLM_MODEL", "anthropic/claude-sonnet-4-5-20250929")

    if api_key:
        # Use real LLMs
        try:
            from openhands.sdk import LLM
            client_llm = LLM(model=model, api_key=api_key)
            guide_llm_config = {"model": model, "api_key": api_key}
            print(f"✅ Using real LLMs: {model}")
        except ImportError:
            # Fallback to demo LLM
            client_llm = DemoLLM()
            guide_llm_config = {"model": "demo"}
            print("⚠️  OpenHands SDK not available, using demo LLM")
    else:
        # Use demo LLM
        client_llm = DemoLLM()
        guide_llm_config = {"model": "demo"}
        print("ℹ️  No API key found, using demo LLM")

    guide_instance = TheGuide(
        project_path=project_path,
        client_llm=client_llm,
        guide_llm_config=guide_llm_config
    )

    print(f"🚀 TheGuide API started!")
    print(f"   Project: {project_path}")
    print(f"   Storage: {guide_instance.guide_path}")
    print(f"   Docs: http://localhost:8000/docs")

# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/")
async def root():
    """API root - health check."""
    return {
        "service": "TheGuide API",
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs",
        "endpoints": {
            "create_session": "POST /sessions",
            "get_session": "GET /sessions/{session_id}",
            "list_sessions": "GET /sessions",
            "explain_session": "GET /sessions/{session_id}/explain",
            "get_scores": "GET /sessions/{session_id}/scores",
            "analytics": "GET /analytics"
        }
    }

@app.post("/sessions", response_model=GuidanceResponse)
async def create_session(
    request: GuidanceRequest,
    background_tasks: BackgroundTasks
):
    """
    Create a new guidance session.

    The session will run asynchronously in the background.
    Use GET /sessions/{session_id} to check status.
    """
    if not guide_instance:
        raise HTTPException(status_code=500, detail="TheGuide not initialized")

    # Generate session ID
    session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # Mark as pending
    active_sessions[session_id] = {
        "status": "pending",
        "request": request.model_dump(),
        "created": datetime.now().isoformat()
    }

    # Run in background
    async def run_guidance():
        try:
            active_sessions[session_id]["status"] = "running"

            # Create a new guide instance with requested settings
            guide = TheGuide(
                project_path=guide_instance.project_path,
                client_llm=guide_instance.client_llm,
                guide_llm_config=guide_instance.guide_llm_config,
                enable_self_rewarding=request.enable_self_rewarding,
                enable_self_correction=request.enable_self_correction
            )

            # Run guidance loop
            answer, protocol = guide.solve(
                problem_statement=request.problem_statement,
                max_iterations=request.max_iterations,
                quality_threshold=request.quality_threshold,
                use_partial_context=request.use_partial_context,
                test_time_scaling=request.test_time_scaling
            )

            active_sessions[session_id]["status"] = "completed"
            active_sessions[session_id]["protocol"] = protocol
            active_sessions[session_id]["answer"] = answer

        except Exception as e:
            active_sessions[session_id]["status"] = "failed"
            active_sessions[session_id]["error"] = str(e)

    background_tasks.add_task(run_guidance)

    return GuidanceResponse(
        session_id=session_id,
        final_answer="Processing in background...",
        quality_score=0.0,
        iteration_count=0,
        created=active_sessions[session_id]["created"],
        completed=""
    )

@app.get("/sessions/{session_id}/status", response_model=SessionStatus)
async def get_session_status(session_id: str):
    """Get the current status of a guidance session."""
    if session_id in active_sessions:
        session = active_sessions[session_id]
        return SessionStatus(
            session_id=session_id,
            status=session["status"],
            current_iteration=None,
            quality_score=None,
            message=f"Session is {session['status']}"
        )

    # Check if completed and in storage
    protocol = guide_instance.get_protocol(session_id)
    if protocol:
        return SessionStatus(
            session_id=session_id,
            status="completed",
            current_iteration=protocol.iteration_count,
            quality_score=protocol.quality_score,
            message="Session completed"
        )

    raise HTTPException(status_code=404, detail=f"Session {session_id} not found")

@app.get("/sessions/{session_id}")
async def get_session(session_id: str):
    """Get full details of a guidance session."""
    protocol = guide_instance.get_protocol(session_id)

    if not protocol:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")

    return protocol.model_dump()

@app.get("/sessions", response_model=List[SessionListItem])
async def list_sessions(limit: int = 10):
    """List recent guidance sessions."""
    recent = guide_instance.get_recent_sessions(limit=limit)

    return [
        SessionListItem(
            session_id=s["session_id"],
            problem_summary=s.get("problem_summary", ""),
            quality_score=s.get("quality_score", 0.0),
            iteration_count=s.get("iterations", 0),
            created=s.get("created", ""),
            completed=s.get("completed")
        )
        for s in recent
    ]

@app.get("/sessions/{session_id}/explain")
async def explain_session(session_id: str):
    """Get a 'Why?' explanation for a session."""
    explanation = guide_instance.explain(session_id)

    if explanation.startswith("Session"):
        raise HTTPException(status_code=404, detail=explanation)

    return {"session_id": session_id, "explanation": explanation}

@app.get("/sessions/{session_id}/scores", response_model=List[FVCUScores])
async def get_session_scores(session_id: str):
    """Get FVCU+Faithfulness scores for all iterations."""
    protocol = guide_instance.get_protocol(session_id)

    if not protocol:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")

    return [
        FVCUScores(**eval_data["scores"])
        for eval_data in protocol.evaluations
    ]

@app.get("/analytics")
async def get_analytics():
    """Get analytics across all sessions."""
    summary = guide_instance.get_session_summary()
    recent = guide_instance.get_recent_sessions(limit=100)

    # Calculate average scores
    avg_quality = 0.0
    avg_iterations = 0.0
    if recent:
        avg_quality = sum(s.get("quality_score", 0.0) for s in recent) / len(recent)
        avg_iterations = sum(s.get("iterations", 0) for s in recent) / len(recent)

    return {
        "total_sessions": summary["total_sessions"],
        "average_quality_score": avg_quality,
        "average_iterations": avg_iterations,
        "last_updated": summary["last_updated"],
        "recent_sessions": len(recent)
    }

@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a guidance session."""
    session_file = guide_instance.guide_path / "sessions" / f"{session_id}.json"
    protocol_file = guide_instance.guide_path / "protocols" / f"{session_id}.json"

    deleted = False

    if session_file.exists():
        session_file.unlink()
        deleted = True

    if protocol_file.exists():
        protocol_file.unlink()
        deleted = True

    if not deleted:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")

    return {"status": "deleted", "session_id": session_id}

# ============================================================================
# Run Server
# ============================================================================

if __name__ == "__main__":
    uvicorn.run(
        "guide_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
