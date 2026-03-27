"""Pantheon Oracle Cycle UI and API routes."""

import json
import re
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel

from ...core.science.oracle import TheOracle
from ..dependencies import get_project_path

router = APIRouter()


class OracleCycleRunRequest(BaseModel):
    objective: str
    order_prompt: str = "Should we implement state machine plus atomic persistence before stage logic for this project?"
    risk_prompt: str = "Which risk should be controlled first: lock race, deterministic zip drift, or schema mismatch?"
    output_dir: str | None = None


def _decision_from_recommendation(text: str) -> str:
    if not text:
        return "UNKNOWN"
    upper = text.upper()
    for token in ["PROCEED", "HALT", "BRANCH", "REVISE", "INVESTIGATE", "UNKNOWN"]:
        if f"[{token}]" in upper:
            return token
    return "UNKNOWN"


def _extract_reasoning(response: dict) -> str:
    reflection = response.get("reflection", {})
    check = response.get("check", {})
    parts = []
    if isinstance(reflection, dict):
        summary = reflection.get("summary") or reflection.get("reflection_summary")
        if summary:
            parts.append(str(summary))
    if isinstance(check, dict):
        if check.get("decision"):
            parts.append(f"check_decision={check.get('decision')}")
        if check.get("confidence") is not None:
            parts.append(f"check_confidence={check.get('confidence')}")
    rec = response.get("recommendation")
    if rec:
        parts.append(str(rec))
    return " | ".join(parts)[:2500]


def _cycle_store(project_path: Path) -> Path:
    path = project_path / "_pantheon" / "oracle_cycle" / "runs"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _store_from_output_dir(project_path: Path, output_dir: str | None, create: bool) -> Path:
    if not output_dir:
        return _cycle_store(project_path)
    try:
        store = Path(output_dir).expanduser().resolve()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid output_dir: {str(e)}")
    if create:
        store.mkdir(parents=True, exist_ok=True)
    return store


@router.post("/pantheon/oracle-cycle/run")
async def run_oracle_cycle(request_body: OracleCycleRunRequest, request: Request):
    project_path = get_project_path(request)
    try:
        oracle = TheOracle(project_path=project_path)
        order = oracle.provide_guidance(question=request_body.order_prompt, show_thinking=False)
        risk = oracle.provide_guidance(question=request_body.risk_prompt, show_thinking=False)
    except Exception as e:
        fallback = {
            "recommendation": f"[HALT] Oracle unavailable, investigate runtime prerequisites. Error: {str(e)}",
            "reflection": {"summary": "Oracle runtime failed; fallback response emitted for trace continuity."},
            "check": {"decision": "halt", "confidence": 0.0},
            "timestamp": datetime.now().isoformat(),
        }
        order = fallback
        risk = fallback

    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    payload = {
        "run_id": run_id,
        "objective": request_body.objective,
        "generated_at": datetime.now().isoformat(),
        "order_decision": _decision_from_recommendation(order.get("recommendation", "")),
        "risk_decision": _decision_from_recommendation(risk.get("recommendation", "")),
        "timeline": [
            {
                "step": "order_prompt",
                "prompt": request_body.order_prompt,
                "recommendation": order.get("recommendation", ""),
                "decision": _decision_from_recommendation(order.get("recommendation", "")),
                "reasoning": _extract_reasoning(order),
                "timestamp": order.get("timestamp", ""),
            },
            {
                "step": "risk_prompt",
                "prompt": request_body.risk_prompt,
                "recommendation": risk.get("recommendation", ""),
                "decision": _decision_from_recommendation(risk.get("recommendation", "")),
                "reasoning": _extract_reasoning(risk),
                "timestamp": risk.get("timestamp", ""),
            },
        ],
    }
    store = _store_from_output_dir(project_path, request_body.output_dir, create=True)
    run_path = store / f"{run_id}.json"
    run_path.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")
    with (store / "index.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps({k: payload[k] for k in ["run_id", "objective", "generated_at", "order_decision", "risk_decision"]}) + "\n")
    return payload


@router.get("/pantheon/oracle-cycle/runs")
async def list_oracle_cycle_runs(request: Request, output_dir: str | None = None):
    store = _store_from_output_dir(get_project_path(request), output_dir, create=False)
    if output_dir and not store.exists():
        return []
    runs = []
    for file_path in sorted(store.glob("*.json"), reverse=True):
        try:
            payload = json.loads(file_path.read_text(encoding="utf-8"))
            runs.append(
                {
                    "run_id": payload.get("run_id"),
                    "objective": payload.get("objective"),
                    "generated_at": payload.get("generated_at"),
                    "order_decision": payload.get("order_decision"),
                    "risk_decision": payload.get("risk_decision"),
                }
            )
        except json.JSONDecodeError:
            continue
    return runs


@router.get("/pantheon/oracle-cycle/runs/{run_id}")
async def get_oracle_cycle_run(run_id: str, request: Request, output_dir: str | None = None):
    if not re.match(r"^[0-9_\\-]+$", run_id):
        raise HTTPException(status_code=400, detail="Invalid run id")
    store = _store_from_output_dir(get_project_path(request), output_dir, create=False)
    path = store / f"{run_id}.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Run not found")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Stored run file is invalid")


@router.get("/pantheon/oracle-cycle/ui")
async def pantheon_oracle_cycle_ui():
    ui_path = Path(__file__).resolve().parents[2] / "pantheon" / "ui" / "oracle_cycle.html"
    if not ui_path.exists():
        raise HTTPException(status_code=404, detail="UI not found")
    return FileResponse(ui_path)


@router.get("/pantheon/oracle-cycle/ui/app.mjs")
async def pantheon_oracle_cycle_ui_script():
    script_path = Path(__file__).resolve().parents[2] / "pantheon" / "ui" / "oracle_cycle_app.mjs"
    if not script_path.exists():
        raise HTTPException(status_code=404, detail="UI script not found")
    return FileResponse(script_path, media_type="application/javascript")


@router.get("/pantheon/oracle-cycle/ui/profile")
async def pantheon_oracle_profile_ui():
    ui_path = Path(__file__).resolve().parents[2] / "pantheon" / "ui" / "oracle_profile.html"
    if not ui_path.exists():
        raise HTTPException(status_code=404, detail="Profile UI not found")
    return FileResponse(ui_path)


@router.get("/pantheon/oracle-cycle/ui/profile/app.mjs")
async def pantheon_oracle_profile_ui_script():
    script_path = Path(__file__).resolve().parents[2] / "pantheon" / "ui" / "oracle_profile_app.mjs"
    if not script_path.exists():
        raise HTTPException(status_code=404, detail="Profile UI script not found")
    return FileResponse(script_path, media_type="application/javascript")
