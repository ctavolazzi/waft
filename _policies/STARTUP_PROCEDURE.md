# Lerna Hydra — Startup Procedure

**Policy document:** Referenced by `tools/lerna-hydra/README.md` and consumed by the app at runtime.
**Last updated:** 2026-04-05

---

## Overview

Lerna Hydra is a self-exploring AI system. A local LLM (Gemma-4 via llama.cpp) autonomously explores a sandboxed copy of a codebase, performs file operations, and builds a live-updating `index.html` — all visible in real-time through a browser dashboard. Session data is persisted in PocketBase.

The startup procedure is designed so that a developer can **fork the repo and run two commands** to have the full stack running in their browser.

---

## Prerequisites

| Dependency | Required | How to get it |
|-----------|----------|---------------|
| Python 3.12+ | Yes | `brew install python@3.12` or system Python |
| Git | Yes | `brew install git` or Xcode CLI tools |
| pip packages: `fastapi`, `uvicorn`, `httpx` | Yes | `make setup` installs these |
| llama.cpp `llama-server` binary | For full mode | Build from `llama.cpp/` or set `LLAMA_BIN` |
| GGUF model file (Gemma-4 Q4_K_M) | For full mode | Set `MODEL_PATH` env var |
| PocketBase | Auto-downloaded | `launch.py` downloads v0.22.8 on first run |
| Internet connection | First run only | For PocketBase download + CopilotKit clone |

---

## Startup Sequence

The launcher (`launch.py`) executes these steps in order. Each step is independently skippable via flags.

### Step 1 — Create Sandbox

```
Method: git worktree (default) or git clone --depth 1 (--clone flag)
Location: /tmp/lerna-hydra-{uuid}/
Contents: Full copy of the waft repository
```

The sandbox is a **disposable, independent copy** of the repo. The agent can read, write, and delete any file inside it. The real repo is never touched.

**Fallback:** If worktree fails (detached HEAD, branch collision), automatically falls back to shallow clone.

### Step 2 — Seed Sandbox

```
Creates: index.html (FogSift-styled "Waiting for Hydra..." page)
Purpose: Gives the iframe preview something to render before the agent starts
```

### Step 3 — Clone CopilotKit (first-task material)

```
Repository: https://github.com/CopilotKit/CopilotKit.git
Location: {sandbox}/copilotkit/
Method: git clone --depth 1 (shallow, ~60s)
Skip: --no-copilotkit flag
```

CopilotKit is cloned into the sandbox so the agent has something interesting to explore on its first run. The agent's first-task prompt instructs it to analyze CopilotKit's architecture and build a visual map in `index.html`.

### Step 4 — Start PocketBase (persistence layer)

```
Port: 8090 (configurable via --pb-port)
Binary: Auto-downloaded to tools/lerna-hydra/.data/pocketbase
Data: tools/lerna-hydra/.data/pb_data/
Skip: --no-pocketbase flag
```

**Collections created via migration:**

| Collection | Fields | Purpose |
|-----------|--------|---------|
| `sessions` | `sandbox_path`, `llama_url`, `model_name`, `started_at`, `status`, `step_count` | One record per agent run |
| `transmissions` | `session_id`, `step`, `prompt`, `thoughts`, `response`, `actions`, `results` | One record per agent loop iteration |

On agent start, a session record is created. Each loop iteration stores a transmission. On stop, the session status is updated.

**Admin UI:** `http://localhost:8090/_/` — browse sessions and transmissions.

### Step 5 — Start llama-server (the brain)

```
Port: 8080 (configurable via --llama-port)
Binary: ~/Code/llama.cpp/build/bin/llama-server (configurable via LLAMA_BIN)
Model: ~/google_gemma-4-E4B-it-Q4_K_M.gguf (configurable via MODEL_PATH)
API: OpenAI-compatible /v1/chat/completions with SSE streaming
Skip: --no-llama flag (assumes already running)
Health check: GET /health — retries 15 times with 2s delay
```

### Step 6 — Start Nerve Center (the relay)

```
Port: 3000 (configurable via --port)
Framework: FastAPI + uvicorn
Role: Agent loop orchestrator, SSE broadcaster, file CRUD API, static file server
```

**Endpoints:**

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/` | Dashboard HTML |
| GET | `/api/sse` | Server-Sent Events stream (all real-time data) |
| POST | `/api/control/start` | Begin agent loop |
| POST | `/api/control/stop` | Cancel agent loop |
| POST | `/api/control/reset` | Restore sandbox, clear history |
| POST | `/api/control/prompt` | Update system prompt at runtime |
| GET | `/api/sandbox/tree` | Current file tree JSON |
| GET | `/api/sandbox/read?path=X` | Read a sandbox file |
| GET | `/sandbox/*` | Static files from sandbox (iframe preview) |

### Step 7 — Open Browser

```
URL: http://localhost:3000
Delay: 2 seconds (lets server bind first)
Skip: --no-browser flag
```

---

## Agent Loop Protocol

Once the user clicks **Start** in the dashboard, the agent loop runs:

```
┌─────────────────────────────────────────────────────────┐
│  LOOP (repeats until Stop or error)                      │
│                                                          │
│  1. OBSERVE  — list sandbox files, build context         │
│  2. PROMPT   — system prompt + history + observation     │
│  3. STREAM   — POST to llama-server, stream tokens       │
│       ├─ reasoning_content → broadcast to dashboard      │
│       └─ content → broadcast to dashboard                │
│  4. PARSE    — extract :::action JSON blocks             │
│  5. EXECUTE  — run file operations in sandbox            │
│       └─ broadcast results + updated file tree           │
│  6. PERSIST  — store transmission in PocketBase          │
│  7. HISTORY  — append to conversation, loop              │
│                                                          │
│  Sleep 1s between iterations                             │
└─────────────────────────────────────────────────────────┘
```

### Action Protocol

The model emits file operations as `:::action` fenced JSON:

```
I'll read the README first.

:::action
{"tool": "read_file", "path": "copilotkit/README.md"}
:::
```

**Available tools:**

| Tool | Parameters | Returns |
|------|-----------|---------|
| `list_files` | `path` (relative dir) | Array of `{name, type, size}` |
| `read_file` | `path` (relative file) | File content (capped at 4000 chars) |
| `write_file` | `path`, `content` | `{ok, path, bytes}` |
| `delete_file` | `path` | `{ok, path}` |

**Safety:** All paths are resolved and checked against the sandbox root. Path traversal (`..`), absolute paths, and symlink escapes are blocked. Per-file limit: 1MB. Total sandbox limit: 50MB.

### SSE Event Types

| Event | Data | When |
|-------|------|------|
| `reasoning` | `{"token": "..."}` | Each reasoning delta from model |
| `content` | `{"token": "..."}` | Each content delta from model |
| `action_request` | `{"tool": "...", "path": "..."}` | Action parsed from response |
| `action_result` | `{"ok": bool, "tool": "...", ...}` | After action execution |
| `file_tree` | `{"files": [...]}` | After file mutations + on connect |
| `loop_status` | `{"status": "...", "step": N}` | On state changes |
| `error` | `{"message": "..."}` | On errors |

---

## First Task

On the first agent loop iteration, the observation includes a special prompt instructing the agent to:

1. **Explore CopilotKit** — list directories, read README.md and package.json
2. **Analyze the architecture** — identify packages, dependencies, key components
3. **Build index.html** — create a FogSift-styled interactive map of CopilotKit's architecture
4. **Iterate** — update the page as it learns more

The user watches this happen in real-time via the dashboard's four panels (reasoning, response, file tree, iframe preview).

---

## Configuration Reference

All configuration is via CLI flags to `launch.py` or environment variables in the Makefile:

| Flag | Env Var | Default | Description |
|------|---------|---------|-------------|
| `--port` | `NERVE_PORT` | 3000 | Nerve center port |
| `--llama-port` | `LLAMA_PORT` | 8080 | llama-server port |
| `--pb-port` | `PB_PORT` | 8090 | PocketBase port |
| `--model-path` | `MODEL_PATH` | `~/google_gemma-4-E4B-it-Q4_K_M.gguf` | GGUF model file |
| `--sandbox-dir` | — | auto-generated | Use existing sandbox |
| `--clone` | — | off | Use git clone instead of worktree |
| `--no-llama` | — | off | Skip llama-server startup |
| `--no-pocketbase` | — | off | Skip PocketBase startup |
| `--no-copilotkit` | — | off | Skip CopilotKit clone |
| `--no-browser` | — | off | Don't auto-open browser |

---

## Shutdown & Cleanup

**Ctrl+C** stops all services (llama-server, PocketBase, nerve center).

The sandbox persists after shutdown at its `/tmp/lerna-hydra-*` path. To clean up:

```bash
make clean          # Removes all sandbox dirs + PocketBase data
rm -rf /tmp/lerna-hydra-*   # Manual sandbox cleanup
```

---

## Architecture Diagram

```
┌──────────────────────────────────────────────────────────────┐
│  Browser Dashboard (dashboard.html — FogSift dark, single file)│
│  ┌───────────┬───────────┬──────────┬────────────────────┐   │
│  │ Reasoning │ Response  │ File Tree│ Live Preview       │   │
│  │ (tokens)  │ (tokens)  │ (live)   │ (iframe: index.html)│  │
│  ├───────────┴───────────┴──────────┴────────────────────┤   │
│  │ Action Log (timestamped)                               │   │
│  └────────────────────────────────────────────────────────┘   │
│         ↕ EventSource (SSE)        ↕ fetch POST (controls)    │
├──────────────────────────────────────────────────────────────┤
│  FastAPI Nerve Center (:3000)                                 │
│  ┌────────────┐  ┌──────────────┐  ┌───────────────────┐    │
│  │ Agent Loop  │  │ File CRUD API│  │ Control Endpoints │    │
│  │ (asyncio)   │  │ (sandboxed)  │  │ start/stop/reset  │    │
│  └──────┬─────┘  └──────────────┘  └───────────────────┘    │
│         │                                                     │
│         ├──── HTTP POST ──── llama-server (:8080, Gemma-4)   │
│         └──── HTTP POST ──── PocketBase  (:8090, sessions)   │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Sandbox (/tmp/lerna-hydra-{uuid}/)                     │  │
│  │   ├── index.html  (agent-built, live preview)          │  │
│  │   ├── copilotkit/  (cloned repo for exploration)       │  │
│  │   └── ... (agent can CRUD anything here)               │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

---

## Comparison: Where Lerna Hydra Sits

| Tool | Type | Local-first | Agent explores code | Live browser preview |
|------|------|-------------|--------------------|--------------------|
| **Lerna Hydra** | Agent sandbox + dashboard | Yes (llama.cpp) | Yes (core purpose) | Yes (iframe + SSE) |
| **CopilotKit** | React integration framework | No (cloud APIs) | No (assists users) | N/A |
| **assistant-ui** | React UI component library | No | No | N/A |
| **LobeHub** | Full agent workspace product | Partial (Docker) | No (user-driven) | No |
| **AnythingLLM** | RAG + chat product | Yes (Docker) | No (document Q&A) | No |
| **ChatBotKit** | Hosted SaaS | No | No | No |

Lerna Hydra is unique: it's an **autonomous agent that explores codebases and builds things**, not a chat interface or integration framework. The closest analog is an AI coding agent, but running locally on your hardware with full observability.

---

*Part of the waft toolkit · tools/lerna-hydra/ · ctavolazzi*
