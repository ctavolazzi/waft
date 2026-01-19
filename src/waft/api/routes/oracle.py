"""
Oracle API endpoints.

Exposes TheOracle to web clients via FastAPI.
"""

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, Dict, Any
from pathlib import Path

from ...core.science.oracle import TheOracle
from ..dependencies import get_project_path

router = APIRouter()


class OracleConsultRequest(BaseModel):
    """Request model for Oracle consultation."""
    question: str
    show_thinking: bool = False


class OracleConsultResponse(BaseModel):
    """Response model for Oracle consultation."""
    question: str
    recommendation: str
    insights: list[str] = []
    epistemic_phase: Optional[str] = None
    knowledge_coverage: Optional[float] = None
    uncertainty: Optional[float] = None
    findings: list[Dict[str, Any]] = []
    unknowns: list[Dict[str, Any]] = []
    preflight: Optional[Dict[str, Any]] = None
    check: Optional[Dict[str, Any]] = None
    reflection: Optional[Dict[str, Any]] = None
    postflight: Optional[Dict[str, Any]] = None
    personality: Optional[Dict[str, Any]] = None
    timestamp: str


@router.post("/oracle/consult", response_model=OracleConsultResponse)
async def consult_oracle(
    request_body: OracleConsultRequest,
    http_request: Request
):
    """
    Consult TheOracle with a question.
    
    Args:
        request_body: OracleConsultRequest with question and optional show_thinking flag
        http_request: FastAPI Request object (for project path)
    
    Returns:
        OracleConsultResponse with guidance, insights, and epistemic state
    
    Raises:
        HTTPException: If Oracle consultation fails
    """
    project_path = get_project_path(http_request)
    
    try:
        oracle = TheOracle(project_path=project_path)
        
        # Get guidance from Oracle
        guidance = oracle.provide_guidance(
            question=request_body.question,
            show_thinking=request_body.show_thinking
        )
        
        # Extract insights (findings)
        insights = [f.get("insight", "") for f in guidance.get("findings", []) if f.get("insight")]
        
        # Build response
        response = OracleConsultResponse(
            question=guidance.get("question", request_body.question),
            recommendation=guidance.get("recommendation", ""),
            insights=insights,
            epistemic_phase=guidance.get("epistemic_phase"),
            knowledge_coverage=guidance.get("knowledge_coverage"),
            uncertainty=guidance.get("uncertainty"),
            findings=guidance.get("findings", []),
            unknowns=guidance.get("unknowns", []),
            preflight=guidance.get("preflight"),
            check=guidance.get("check"),
            reflection=guidance.get("reflection"),
            postflight=guidance.get("postflight"),
            personality=guidance.get("personality"),
            timestamp=guidance.get("timestamp", "")
        )
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Oracle consultation failed: {str(e)}")


@router.get("/oracle/health")
async def oracle_health(http_request: Request):
    """
    Health check endpoint for Oracle.
    
    Returns:
        Health status with Oracle availability
    """
    project_path = get_project_path(http_request)
    
    try:
        oracle = TheOracle(project_path=project_path)
        state = oracle.get_epistemic_state()
        
        return {
            "status": "ok",
            "oracle_available": True,
            "epistemic_state": state is not None,
            "personality": oracle.personality.data.get("name", "The Oracle")
        }
    except Exception as e:
        return {
            "status": "error",
            "oracle_available": False,
            "error": str(e)
        }
