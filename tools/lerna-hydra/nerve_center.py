"""Nerve Center — FastAPI server for Lerna Hydra.

Agent loop, SSE broadcast, file CRUD API, control endpoints.
The brain relay between llama-server and the browser dashboard.
PocketBase persistence for sessions and transmissions.
"""
import asyncio
import json
import logging
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from sandbox_manager import SandboxManager
from agent_protocol import (
    parse_actions, validate_action, build_messages, build_system_prompt,
)
from pocketbase_client import PocketBaseClient

logger = logging.getLogger("lerna-hydra")

# Policy document — the app reads this at runtime for startup procedure reference
STARTUP_PROCEDURE_PATH = Path(__file__).resolve().parent.parent.parent / "_policies" / "STARTUP_PROCEDURE.md"

# ---------------------------------------------------------------------------
# SSE Broadcast
# ---------------------------------------------------------------------------

_clients: list[asyncio.Queue] = []


async def broadcast(event_type: str, data: dict):
    """Send an SSE event to all connected clients."""
    msg = f"event: {event_type}\ndata: {json.dumps(data)}\n\n"
    for q in list(_clients):
        try:
            q.put_nowait(msg)
        except asyncio.QueueFull:
            pass


# ---------------------------------------------------------------------------
# Agent Loop State
# ---------------------------------------------------------------------------

class AgentState:
    """Mutable state for the agent loop."""
    def __init__(self, sandbox: SandboxManager, llama_url: str, pb_url: str = "http://127.0.0.1:8090"):
        self.sandbox = sandbox
        self.llama_url = llama_url
        self.pb = PocketBaseClient(pb_url)
        self.pb_session_id: str | None = None
        self.history: list[dict[str, str]] = []
        self.step_count = 0
        self.running = False
        self.task: asyncio.Task | None = None
        self.system_prompt_override: str | None = None
        self.first_task_done = False

    async def register_session(self):
        """Store session info in PocketBase on first load."""
        session_data = {
            "sandbox_path": str(self.sandbox.root),
            "llama_url": self.llama_url,
            "model_name": "gemma-4-E4B-Q4_K_M",
            "started_at": datetime.now(timezone.utc).isoformat(),
            "status": "running",
            "step_count": 0,
        }
        record = await self.pb.create_session(session_data)
        if record:
            self.pb_session_id = record.get("id")
            await broadcast("action_result", {
                "ok": True, "tool": "pocketbase",
                "detail": f"Session registered: {self.pb_session_id}",
            })
        else:
            await broadcast("action_result", {
                "ok": False, "tool": "pocketbase",
                "detail": "PocketBase not available — running without persistence",
            })

    async def store_transmission(self, step: int, observation: str,
                                  thoughts: str, response: str,
                                  actions: list, results: list):
        """Store one loop iteration in PocketBase."""
        if not self.pb_session_id:
            return
        await self.pb.create_transmission({
            "session_id": self.pb_session_id,
            "step": step,
            "prompt": observation[:2000],
            "thoughts": thoughts[:4000],
            "response": response[:4000],
            "actions": json.dumps(actions)[:2000],
            "results": json.dumps(results)[:2000],
        })

    async def observe(self) -> str:
        """Build an observation string from the sandbox state."""
        try:
            tree = self.sandbox.list_files(".")
        except Exception:
            tree = []
        lines = ["Current sandbox contents:"]
        for entry in tree:
            icon = "📁" if entry["type"] == "dir" else "📄"
            lines.append(f"  {icon} {entry['name']}")
        if self.step_count == 0 and not self.first_task_done:
            lines.append(FIRST_TASK_PROMPT)
            self.first_task_done = True
        return "\n".join(lines)


# The agent's first task: clone CopilotKit for exploration
FIRST_TASK_PROMPT = """
This is your first turn. Your mission has two phases:

PHASE 1 — IMMEDIATE:
The CopilotKit repository (https://github.com/CopilotKit/CopilotKit) has already been
cloned into the 'copilotkit' subdirectory of your sandbox. Start by exploring it:
1. List the copilotkit/ directory to understand its structure
2. Read its README.md and package.json
3. Identify the key packages and architecture

PHASE 2 — BUILD:
Create an index.html that serves as a beautiful interactive map of CopilotKit's
architecture. Use the FogSift design system. Show:
- Package structure and dependencies
- Key components and what they do
- How it connects AI to React apps
- Your analysis of the architecture

Update index.html iteratively as you learn more. The user is watching in real-time.
"""

    def get_file_tree(self) -> list[dict[str, Any]]:
        try:
            return self.sandbox.list_files(".")
        except Exception:
            return []


agent_state: AgentState | None = None


# ---------------------------------------------------------------------------
# Agent Loop
# ---------------------------------------------------------------------------

async def agent_loop():
    """Main agent loop: observe → prompt → stream → parse → execute → repeat."""
    state = agent_state
    if not state:
        return

    state.running = True
    await broadcast("loop_status", {"status": "running", "step": 0})

    # Register session in PocketBase on first start
    await state.register_session()

    try:
        while state.running:
            state.step_count += 1
            step = state.step_count
            await broadcast("loop_status", {"status": "running", "step": step})

            # 1. Observe
            observation = await state.observe()
            file_tree = state.get_file_tree()
            await broadcast("file_tree", {"files": file_tree})

            # 2. Build messages
            messages = build_messages(state.history, observation, file_tree)

            # 3. Stream from model — capture both reasoning and content
            full_response = ""
            full_reasoning = ""
            try:
                async with httpx.AsyncClient(timeout=None) as client:
                    payload = {
                        "model": "gemma-4",
                        "messages": messages,
                        "stream": True,
                        "temperature": 0.7,
                        "max_tokens": 4096,
                    }
                    async with client.stream(
                        "POST",
                        f"{state.llama_url}/v1/chat/completions",
                        json=payload,
                    ) as response:
                        async for line in response.aiter_lines():
                            if not line.startswith("data: "):
                                continue
                            if line == "data: [DONE]":
                                break
                            try:
                                chunk = json.loads(line[6:])
                                delta = chunk["choices"][0].get("delta", {})

                                reasoning = delta.get("reasoning_content", "")
                                content = delta.get("content", "")

                                if reasoning:
                                    await broadcast("reasoning", {"token": reasoning})
                                    full_reasoning += reasoning
                                if content:
                                    await broadcast("content", {"token": content})
                                    full_response += content
                            except (json.JSONDecodeError, KeyError, IndexError):
                                continue

            except httpx.ConnectError:
                await broadcast("error", {
                    "message": f"Cannot connect to llama-server at {state.llama_url}. Is it running?"
                })
                state.running = False
                break
            except Exception as e:
                await broadcast("error", {"message": f"Model error: {e}"})
                state.running = False
                break

            # 4. Parse actions
            actions = parse_actions(full_response)

            # 5. Execute actions
            results = []
            for action in actions:
                await broadcast("action_request", action)
                try:
                    validate_action(action)
                    result = _execute_action(state.sandbox, action)
                    result["ok"] = True
                    results.append(result)
                except Exception as e:
                    result = {"ok": False, "tool": action.get("tool"), "error": str(e)}
                    results.append(result)
                await broadcast("action_result", result)

            # Broadcast updated file tree after mutations
            if actions:
                await broadcast("file_tree", {"files": state.get_file_tree()})

            # 6. Store transmission in PocketBase
            await state.store_transmission(
                step=step,
                observation=observation,
                thoughts=full_reasoning,
                response=full_response,
                actions=actions,
                results=results,
            )

            # 7. Update history
            state.history.append({"role": "assistant", "content": full_response})
            if results:
                result_text = "Action results:\n" + json.dumps(results, indent=2)
                state.history.append({"role": "user", "content": result_text})

            # Brief pause between steps
            await asyncio.sleep(1)

    except asyncio.CancelledError:
        pass
    finally:
        state.running = False
        # Update session status in PocketBase
        if state.pb_session_id:
            await state.pb.update_session(state.pb_session_id, {
                "status": "stopped",
                "step_count": state.step_count,
            })
        await broadcast("loop_status", {"status": "stopped", "step": state.step_count})


def _execute_action(sandbox: SandboxManager, action: dict) -> dict:
    """Execute a single validated action against the sandbox."""
    tool = action["tool"]
    path = action.get("path", ".")

    if tool == "list_files":
        entries = sandbox.list_files(path)
        return {"tool": tool, "path": path, "entries": entries}
    elif tool == "read_file":
        content = sandbox.read_file(path)
        return {"tool": tool, "path": path, "content": content[:4000]}  # Cap for context
    elif tool == "write_file":
        content = action.get("content", "")
        return sandbox.write_file(path, content)
    elif tool == "delete_file":
        return sandbox.delete_file(path)
    else:
        raise ValueError(f"Unknown tool: {tool}")


# ---------------------------------------------------------------------------
# FastAPI App
# ---------------------------------------------------------------------------

def create_app(
    sandbox_dir: Path,
    llama_url: str = "http://127.0.0.1:8080",
    pb_url: str = "http://127.0.0.1:8090",
) -> FastAPI:
    """Create the FastAPI application."""
    global agent_state

    app = FastAPI(title="Lerna Hydra Nerve Center")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    sandbox = SandboxManager(sandbox_dir)
    agent_state = AgentState(sandbox, llama_url, pb_url)

    # --- SSE endpoint ---
    @app.get("/api/sse")
    async def sse_stream():
        q: asyncio.Queue = asyncio.Queue(maxsize=256)
        _clients.append(q)

        async def generate():
            try:
                # Send initial file tree
                tree = agent_state.get_file_tree()
                yield f"event: file_tree\ndata: {json.dumps({'files': tree})}\n\n"
                yield f"event: loop_status\ndata: {json.dumps({'status': 'stopped' if not agent_state.running else 'running', 'step': agent_state.step_count})}\n\n"

                while True:
                    msg = await q.get()
                    yield msg
            except asyncio.CancelledError:
                pass
            finally:
                if q in _clients:
                    _clients.remove(q)

        return StreamingResponse(generate(), media_type="text/event-stream")

    # --- Control endpoints ---
    @app.post("/api/control/start")
    async def control_start():
        if agent_state.running:
            return JSONResponse({"ok": False, "message": "Already running"})
        agent_state.task = asyncio.create_task(agent_loop())
        return JSONResponse({"ok": True, "message": "Agent loop started"})

    @app.post("/api/control/stop")
    async def control_stop():
        if agent_state.task and not agent_state.task.done():
            agent_state.running = False
            agent_state.task.cancel()
        return JSONResponse({"ok": True, "message": "Agent loop stopped"})

    @app.post("/api/control/reset")
    async def control_reset():
        if agent_state.running:
            agent_state.running = False
            if agent_state.task:
                agent_state.task.cancel()
        agent_state.history.clear()
        agent_state.step_count = 0
        # Re-seed index.html
        sandbox.write_file("index.html", _SEED_HTML)
        await broadcast("file_tree", {"files": agent_state.get_file_tree()})
        await broadcast("loop_status", {"status": "stopped", "step": 0})
        return JSONResponse({"ok": True, "message": "Reset complete"})

    @app.post("/api/control/prompt")
    async def control_prompt(request: Request):
        body = await request.json()
        agent_state.system_prompt_override = body.get("prompt")
        return JSONResponse({"ok": True})

    # --- File CRUD API ---
    @app.get("/api/sandbox/tree")
    async def sandbox_tree():
        return JSONResponse({"files": agent_state.get_file_tree()})

    @app.get("/api/sandbox/read")
    async def sandbox_read(path: str = "."):
        try:
            content = sandbox.read_file(path)
            return JSONResponse({"ok": True, "content": content})
        except (FileNotFoundError, ValueError) as e:
            return JSONResponse({"ok": False, "error": str(e)}, status_code=400)

    # --- Startup Procedure (policy document) ---
    @app.get("/api/startup-procedure")
    async def startup_procedure():
        if STARTUP_PROCEDURE_PATH.exists():
            return JSONResponse({
                "ok": True,
                "path": str(STARTUP_PROCEDURE_PATH),
                "content": STARTUP_PROCEDURE_PATH.read_text(),
            })
        return JSONResponse({"ok": False, "error": "Startup procedure not found"}, status_code=404)

    # --- Dashboard ---
    dashboard_path = Path(__file__).parent / "dashboard.html"

    @app.get("/", response_class=HTMLResponse)
    async def serve_dashboard():
        if dashboard_path.exists():
            return HTMLResponse(dashboard_path.read_text())
        return HTMLResponse("<h1>Dashboard not found</h1>")

    # --- Sandbox static files (for iframe preview) ---
    app.mount("/sandbox", StaticFiles(directory=str(sandbox_dir)), name="sandbox")

    return app


# Seed HTML for fresh/reset sandbox
_SEED_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Lerna Hydra Sandbox</title>
<style>
  body {
    background: #f5f0e6;
    color: #4a2c2a;
    font-family: 'Courier New', monospace;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100vh;
    margin: 0;
  }
  .waiting {
    text-align: center;
    border: 3px solid #4a2c2a;
    padding: 40px;
    box-shadow: 4px 4px 0 #e07b3c;
  }
  h1 { color: #e07b3c; margin: 0 0 10px; }
  p { color: #7a6b5d; }
</style>
</head>
<body>
<div class="waiting">
  <h1>🐉 LERNA HYDRA</h1>
  <p>Waiting for the agent to begin exploring...</p>
</div>
</body>
</html>
"""
