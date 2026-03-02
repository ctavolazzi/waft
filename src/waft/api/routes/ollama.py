"""
Ollama-compatible WAFT adapter routes.
"""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from ...core.science.oracle import TheOracle
from ..dependencies import get_project_path

router = APIRouter()


class GenerateRequest(BaseModel):
    model: str = "waft-oracle:latest"
    prompt: str = Field(..., min_length=1)
    stream: bool = False
    options: dict[str, Any] | None = None


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _models() -> list[dict[str, Any]]:
    names = [
        "waft-oracle:latest",
        "waft-storyteller:latest",
        "waft-pet:latest",
        "waft-echo:latest",
    ]
    modified_at = _now_iso()
    models = []
    for name in names:
        models.append(
            {
                "name": name,
                "model": name,
                "modified_at": modified_at,
                "size": 0,
                "digest": f"sha256:{hashlib.sha256(name.encode('utf-8')).hexdigest()}",
                "details": {
                    "format": "waft",
                    "family": "waft",
                    "families": ["waft"],
                    "parameter_size": "n/a",
                    "quantization_level": "n/a",
                },
            }
        )
    return models


def _oracle_generate(project_path: Path, prompt: str) -> str:
    try:
        guidance = TheOracle(project_path=project_path).provide_guidance(
            question=prompt, show_thinking=False
        )
        recommendation = guidance.get("recommendation", "").strip()
        if recommendation:
            return recommendation
    except Exception:
        pass
    return ""


@router.get("/tags")
async def list_tags():
    return {"models": _models()}


@router.post("/generate")
async def generate(request: GenerateRequest, http_request: Request):
    prompt = request.prompt.strip()
    if not prompt:
        raise HTTPException(status_code=400, detail="prompt must not be empty")

    project_path = get_project_path(http_request)
    model = request.model.strip() or "waft-oracle:latest"

    response_text = ""
    if model.startswith("waft-oracle"):
        response_text = _oracle_generate(project_path, prompt)

    if not response_text:
        response_text = f"[{model}] {prompt}"

    created_at = _now_iso()
    payload = {
        "model": model,
        "created_at": created_at,
        "response": response_text,
        "done": True,
        "done_reason": "stop",
        "context": [],
        "total_duration": 0,
        "load_duration": 0,
        "prompt_eval_count": len(prompt.split()),
        "prompt_eval_duration": 0,
        "eval_count": len(response_text.split()),
        "eval_duration": 0,
    }

    if not request.stream:
        return payload

    first_chunk = {
        "model": model,
        "created_at": created_at,
        "response": response_text,
        "done": False,
    }
    done_chunk = {
        "model": model,
        "created_at": created_at,
        "response": "",
        "done": True,
        "done_reason": "stop",
        "context": [],
        "total_duration": 0,
        "load_duration": 0,
        "prompt_eval_count": len(prompt.split()),
        "prompt_eval_duration": 0,
        "eval_count": len(response_text.split()),
        "eval_duration": 0,
    }

    def _stream():
        yield json.dumps(first_chunk) + "\n"
        yield json.dumps(done_chunk) + "\n"

    return StreamingResponse(_stream(), media_type="application/x-ndjson")
