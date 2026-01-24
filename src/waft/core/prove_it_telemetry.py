"""
Prove-it telemetry server.

Lightweight FastAPI app that logs run metrics to a JSONL evidence log.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field


class TelemetryRun(BaseModel):
    run_id: str
    source: str = "autoplay"
    started_at: str | None = None
    ended_at: str | None = None
    metrics: dict[str, Any] = Field(default_factory=dict)
    events: list[dict[str, Any]] = Field(default_factory=list)


def create_app(log_path: Path) -> FastAPI:
    app = FastAPI(title="Waft Telemetry", version="0.1")

    @app.get("/telemetry/health")
    def health():
        return {"ok": True}

    @app.post("/telemetry/run")
    def submit_run(payload: TelemetryRun):
        log_path.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "received_at": datetime.now(timezone.utc).isoformat(),
            **payload.model_dump(),
        }
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry) + "\n")
        return {"ok": True, "log_path": str(log_path)}

    return app
