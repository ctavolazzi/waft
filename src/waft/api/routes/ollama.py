"""
Ollama-compatible WAFT adapter routes.
"""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel, Field

from ...core.science.oracle import TheOracle
from ..dependencies import get_project_path

router = APIRouter()


class GenerateRequest(BaseModel):
    model: str = "waft-oracle:latest"
    prompt: str = Field(..., min_length=1)
    stream: bool = False
    options: dict[str, Any] | None = None


class ChatMessage(BaseModel):
    role: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)


class ChatRequest(BaseModel):
    model: str = "waft-oracle:latest"
    messages: list[ChatMessage] = Field(..., min_length=1)
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


def _history_path(project_path: Path) -> Path:
    return project_path / ".waft" / "ollama_runtime.jsonl"


def _append_history(project_path: Path, event: dict[str, Any]) -> None:
    path = _history_path(project_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=True) + "\n")


def _read_history(project_path: Path, limit: int) -> list[dict[str, Any]]:
    path = _history_path(project_path)
    if not path.exists():
        return []
    events = []
    lines = path.read_text(encoding="utf-8").splitlines()
    for line in reversed(lines):
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
        if len(events) >= limit:
            break
    events.reverse()
    return events


def _prompt_from_messages(messages: list[ChatMessage]) -> str:
    for message in reversed(messages):
        if message.role.lower() == "user":
            return message.content.strip()
    return messages[-1].content.strip()


@router.get("/tags")
async def list_tags():
    return {"models": _models()}


@router.get("/runtime-ui", response_class=HTMLResponse)
async def runtime_ui():
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>WAFT Ollama Runtime UI</title>
  <style>
    :root { color-scheme: dark; }
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 20px; background: #0f172a; color: #e2e8f0; }
    h1 { margin: 0 0 16px; font-size: 22px; }
    .row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
    .card { background: #111827; border: 1px solid #334155; border-radius: 10px; padding: 14px; }
    .diff-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
    label { display: block; margin-top: 8px; margin-bottom: 4px; font-size: 13px; color: #93c5fd; }
    input, textarea, button { width: 100%; box-sizing: border-box; border-radius: 8px; border: 1px solid #334155; background: #0b1220; color: #e2e8f0; padding: 8px; }
    textarea { min-height: 100px; resize: vertical; }
    button { margin-top: 10px; cursor: pointer; background: #1d4ed8; border-color: #2563eb; font-weight: 600; }
    button.secondary { background: #334155; border-color: #475569; }
    pre { white-space: pre-wrap; word-break: break-word; background: #020617; border: 1px solid #334155; border-radius: 8px; padding: 10px; min-height: 120px; }
    .full { margin-top: 16px; }
    .status { margin: 10px 0 0; font-size: 13px; color: #a7f3d0; }
    .hint { margin: 6px 0 0; font-size: 12px; color: #94a3b8; }
    .kpis { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; margin: 10px 0; }
    .kpi { background: #020617; border: 1px solid #334155; border-radius: 8px; padding: 8px; }
    .kpi .label { color: #94a3b8; font-size: 12px; }
    .kpi .value { color: #e2e8f0; font-size: 20px; font-weight: 700; }
    .added { border-color: #14532d; background: #052e16; }
  </style>
</head>
<body>
  <h1>WAFT Ollama Runtime UI</h1>
  <div class="hint">Use this page to send requests and verify persisted history from <code>.waft/ollama_runtime.jsonl</code>.</div>
  <button id="run-demo">Run Demo Flow</button>
  <div class="hint">Demo runs generate + chat with timestamped prompts, then refreshes history.</div>

  <div class="row">
    <section class="card">
      <h2>Generate</h2>
      <label for="gen-model">Model</label>
      <input id="gen-model" value="waft-echo:latest" />
      <label for="gen-prompt">Prompt</label>
      <textarea id="gen-prompt">show me that generate is working</textarea>
      <button id="gen-send">POST /api/generate</button>
      <pre id="gen-output"></pre>
    </section>

    <section class="card">
      <h2>Chat</h2>
      <label for="chat-model">Model</label>
      <input id="chat-model" value="waft-echo:latest" />
      <label for="chat-user">User message</label>
      <textarea id="chat-user">show me that chat is working</textarea>
      <button id="chat-send">POST /api/chat</button>
      <pre id="chat-output"></pre>
    </section>
  </div>

  <section class="card full">
    <h2>Persisted History</h2>
    <label for="history-limit">Limit</label>
    <input id="history-limit" type="number" min="1" max="500" value="20" />
    <button class="secondary" id="history-refresh">GET /api/history</button>
    <pre id="history-output"></pre>
  </section>

  <section class="card full">
    <h2>Visual Diff</h2>
    <div class="hint">Shows what changed between history before and after running Demo.</div>
    <div class="kpis">
      <div class="kpi"><div class="label">Before</div><div class="value" id="diff-before-count">0</div></div>
      <div class="kpi"><div class="label">After</div><div class="value" id="diff-after-count">0</div></div>
      <div class="kpi added"><div class="label">Added</div><div class="value" id="diff-added-count">0</div></div>
    </div>
    <div class="diff-grid">
      <div>
        <label>Before Snapshot</label>
        <pre id="diff-before-output"></pre>
      </div>
      <div>
        <label>After Snapshot</label>
        <pre id="diff-after-output"></pre>
      </div>
    </div>
    <label>Added Events</label>
    <pre id="diff-added-output"></pre>
  </section>

  <div class="status" id="status">Ready.</div>

  <script>
    const statusEl = document.getElementById("status");

    function setStatus(message, ok = true) {
      statusEl.textContent = message;
      statusEl.style.color = ok ? "#a7f3d0" : "#fca5a5";
    }

    async function postJson(url, payload, outputId) {
      try {
        setStatus("Request in progress...");
        const response = await fetch(url, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });
        const data = await response.json();
        document.getElementById(outputId).textContent = JSON.stringify(data, null, 2);
        if (!response.ok) {
          setStatus(`${url} failed with ${response.status}`, false);
          return;
        }
        setStatus(`${url} succeeded (${response.status})`);
      } catch (error) {
        document.getElementById(outputId).textContent = String(error);
        setStatus(`Request failed: ${error}`, false);
      }
    }

    function eventKey(event) {
      return [
        event.created_at || "",
        event.endpoint || "",
        event.model || "",
        JSON.stringify(event.request || {}),
        JSON.stringify(event.response || {})
      ].join("|");
    }

    function setDiff(beforeEvents, afterEvents) {
      const before = Array.isArray(beforeEvents) ? beforeEvents : [];
      const after = Array.isArray(afterEvents) ? afterEvents : [];
      const seenBefore = new Set(before.map(eventKey));
      const added = after.filter((event) => !seenBefore.has(eventKey(event)));

      document.getElementById("diff-before-count").textContent = String(before.length);
      document.getElementById("diff-after-count").textContent = String(after.length);
      document.getElementById("diff-added-count").textContent = String(added.length);

      document.getElementById("diff-before-output").textContent = JSON.stringify(before, null, 2);
      document.getElementById("diff-after-output").textContent = JSON.stringify(after, null, 2);
      document.getElementById("diff-added-output").textContent = JSON.stringify(added, null, 2);
    }

    async function fetchHistory(limit) {
      const response = await fetch(`/api/history?limit=${limit}`);
      const data = await response.json();
      if (!response.ok) {
        throw new Error(`/api/history failed with ${response.status}`);
      }
      return data;
    }

    async function refreshHistory() {
      const limit = Number(document.getElementById("history-limit").value || 20);
      try {
        setStatus("Loading history...");
        const data = await fetchHistory(limit);
        document.getElementById("history-output").textContent = JSON.stringify(data, null, 2);
        setStatus(`/api/history loaded (${(data.events || []).length} events)`);
      } catch (error) {
        document.getElementById("history-output").textContent = String(error);
        setStatus(`History load failed: ${error}`, false);
      }
    }

    document.getElementById("gen-send").addEventListener("click", async () => {
      const payload = {
        model: document.getElementById("gen-model").value.trim() || "waft-echo:latest",
        prompt: document.getElementById("gen-prompt").value,
        stream: false
      };
      await postJson("/api/generate", payload, "gen-output");
      await refreshHistory();
    });

    document.getElementById("chat-send").addEventListener("click", async () => {
      const payload = {
        model: document.getElementById("chat-model").value.trim() || "waft-echo:latest",
        messages: [{ role: "user", content: document.getElementById("chat-user").value }],
        stream: false
      };
      await postJson("/api/chat", payload, "chat-output");
      await refreshHistory();
    });

    async function runDemo() {
      const stamp = new Date().toISOString();
      const limit = Number(document.getElementById("history-limit").value || 20);
      let beforeData = { events: [] };
      let afterData = { events: [] };
      document.getElementById("gen-prompt").value = `demo generate ${stamp}`;
      document.getElementById("chat-user").value = `demo chat ${stamp}`;
      try {
        beforeData = await fetchHistory(limit);
      } catch (_error) {
        // Keep demo running even if baseline fetch fails.
      }
      await postJson("/api/generate", {
        model: document.getElementById("gen-model").value.trim() || "waft-echo:latest",
        prompt: document.getElementById("gen-prompt").value,
        stream: false
      }, "gen-output");
      await postJson("/api/chat", {
        model: document.getElementById("chat-model").value.trim() || "waft-echo:latest",
        messages: [{ role: "user", content: document.getElementById("chat-user").value }],
        stream: false
      }, "chat-output");
      try {
        afterData = await fetchHistory(limit);
        document.getElementById("history-output").textContent = JSON.stringify(afterData, null, 2);
      } catch (error) {
        document.getElementById("history-output").textContent = String(error);
      }
      setDiff(beforeData.events || [], afterData.events || []);
      setStatus("Demo flow completed. Check Visual Diff + Added Events.");
    }

    document.getElementById("run-demo").addEventListener("click", runDemo);
    document.getElementById("history-refresh").addEventListener("click", refreshHistory);
    refreshHistory();
  </script>
</body>
</html>
"""


@router.get("/history")
async def history(http_request: Request, limit: int = Query(default=50, ge=1, le=500)):
    project_path = get_project_path(http_request)
    return {"events": _read_history(project_path, limit)}


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

    _append_history(
        project_path,
        {
            "created_at": created_at,
            "endpoint": "/api/generate",
            "model": model,
            "stream": request.stream,
            "request": {"prompt": prompt},
            "response": {"text": response_text},
        },
    )

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


@router.post("/chat")
async def chat(request: ChatRequest, http_request: Request):
    if not request.messages:
        raise HTTPException(status_code=400, detail="messages must not be empty")

    prompt = _prompt_from_messages(request.messages)
    if not prompt:
        raise HTTPException(status_code=400, detail="messages must include non-empty content")

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
        "message": {"role": "assistant", "content": response_text},
        "done": True,
        "done_reason": "stop",
        "total_duration": 0,
        "load_duration": 0,
        "prompt_eval_count": len(prompt.split()),
        "prompt_eval_duration": 0,
        "eval_count": len(response_text.split()),
        "eval_duration": 0,
    }

    _append_history(
        project_path,
        {
            "created_at": created_at,
            "endpoint": "/api/chat",
            "model": model,
            "stream": request.stream,
            "request": {
                "messages": [message.model_dump() for message in request.messages],
                "prompt": prompt,
            },
            "response": {"text": response_text},
        },
    )

    if not request.stream:
        return payload

    first_chunk = {
        "model": model,
        "created_at": created_at,
        "message": {"role": "assistant", "content": response_text},
        "done": False,
    }
    done_chunk = {
        "model": model,
        "created_at": created_at,
        "message": {"role": "assistant", "content": ""},
        "done": True,
        "done_reason": "stop",
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
