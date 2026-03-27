"""
Oracle API endpoints.

Exposes TheOracle to web clients via FastAPI.
"""

from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from ...karma import KarmaMerchant
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
    epistemic_phase: str | None = None
    knowledge_coverage: float | None = None
    uncertainty: float | None = None
    findings: list[dict[str, Any]] = []
    unknowns: list[dict[str, Any]] = []
    preflight: dict[str, Any] | None = None
    check: dict[str, Any] | None = None
    reflection: dict[str, Any] | None = None
    postflight: dict[str, Any] | None = None
    personality: dict[str, Any] | None = None
    timestamp: str


@router.post("/oracle/consult", response_model=OracleConsultResponse)
async def consult_oracle(request_body: OracleConsultRequest, http_request: Request):
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
            question=request_body.question, show_thinking=request_body.show_thinking
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
            timestamp=guidance.get("timestamp", ""),
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
            "personality": oracle.personality.data.get("name", "The Oracle"),
        }
    except Exception as e:
        return {"status": "error", "oracle_available": False, "error": str(e)}


@router.get("/oracle/profile")
async def oracle_profile(http_request: Request, soul_id: str | None = None):
    project_path = get_project_path(http_request)

    try:
        oracle = TheOracle(project_path=project_path)
        personality = oracle.get_personality_info()
        epistemic_state = oracle.get_epistemic_state()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Oracle profile failed: {str(e)}")

    reincarnation = {
        "soul_id": soul_id,
        "total_karma": 0.0,
        "lifetimes_count": 0,
        "last_incarnation": None,
        "memory_fragments_count": 0,
    }

    if soul_id:
        try:
            soul = KarmaMerchant(project_path=project_path).access_akasha(soul_id)
            reincarnation = {
                "soul_id": soul.get("soul_id", soul_id),
                "total_karma": soul.get("total_karma", 0.0),
                "lifetimes_count": len(soul.get("lifetimes", []) or []),
                "last_incarnation": soul.get("last_incarnation"),
                "memory_fragments_count": len(soul.get("memory_fragments", []) or []),
            }
        except Exception:
            pass

    return {
        "oracle": {
            "name": personality.get("name", "The Oracle"),
            "type": personality.get("type", "balanced"),
            "title": personality.get("title", "Epistemic Intelligence System"),
            "traits": personality.get("traits", {}),
            "communication_style": personality.get("communication_style", {}),
        },
        "epistemic": {
            "ready": epistemic_state.get("ready", False),
            "has_context": epistemic_state.get("has_context", False),
            "message": epistemic_state.get("message", ""),
            "findings_count": len(epistemic_state.get("findings", []) or []),
            "unknowns_count": len(epistemic_state.get("unknowns", []) or []),
            "goals_count": len(epistemic_state.get("goals", []) or []),
            "timestamp": epistemic_state.get("timestamp", ""),
        },
        "reincarnation": reincarnation,
    }
