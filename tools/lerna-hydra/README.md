# Lerna Hydra

**A local LLM that explores codebases and builds things in real-time.**

Fork the repo. Run two commands. Watch a local Gemma-4 autonomously explore CopilotKit's architecture and build a live web page about what it finds — all in your browser.

```
┌───────────┬───────────┬──────────┬──────────────┐
│ Reasoning │ Response  │ File Tree│ Live Preview  │
│ (tokens)  │ (tokens)  │ (live)   │ (index.html) │
├───────────┴───────────┴──────────┴──────────────┤
│ Action Log                                       │
└──────────────────────────────────────────────────┘
```

---

## Quick Start

```bash
cd tools/lerna-hydra
make setup    # pip install fastapi uvicorn httpx pytest
make dev      # starts PocketBase + llama-server + dashboard, opens browser
```

That's it. The launcher:
1. Creates a sandboxed copy of the repo
2. Clones [CopilotKit](https://github.com/CopilotKit/CopilotKit) into the sandbox
3. Downloads and starts PocketBase (session persistence)
4. Starts llama-server with Gemma-4
5. Opens the dashboard at `http://localhost:3000`

Click **Start** and watch the agent explore.

---

## Modes

```bash
make dev              # Full stack: PocketBase + llama-server + dashboard
make dev-no-llama     # llama-server already running on :8080
make dev-minimal      # Dashboard only (no model, no DB) — for UI dev
make test             # Run all 37 tests
make browse           # Open dashboard + PocketBase admin
make clean            # Remove sandboxes + PocketBase data
```

---

## What Happens

1. Gemma-4 runs locally via llama.cpp (your hardware, your data)
2. The agent gets a sandbox — a disposable git clone it can freely modify
3. CopilotKit is pre-loaded in the sandbox as exploration material
4. Each loop: observe files → think → respond → perform file operations → repeat
5. The agent builds an `index.html` that evolves in real-time (visible in the iframe)
6. Every iteration is persisted in PocketBase (thoughts, response, actions, results)
7. You watch everything in a 4-panel FogSift-styled dashboard via SSE

---

## Stack

| Component | Port | Role |
|-----------|------|------|
| **llama-server** | 8080 | Local inference (Gemma-4 Q4_K_M via llama.cpp) |
| **PocketBase** | 8090 | Session + transmission persistence (auto-downloaded) |
| **Nerve Center** | 3000 | FastAPI relay — agent loop, SSE, file CRUD, controls |
| **Dashboard** | 3000 | Single-file HTML — FogSift dark, EventSource, iframe |
| **Sandbox** | — | `/tmp/lerna-hydra-*/` — disposable git clone |

---

## Files

```
tools/lerna-hydra/
├── README.md              # You are here
├── Makefile               # make setup && make dev
├── launch.py              # One-command launcher (all services)
├── nerve_center.py        # FastAPI: agent loop + SSE + PB persistence
├── agent_protocol.py      # :::action parser + system prompt + first task
├── sandbox_manager.py     # Path-jailed file CRUD (security boundary)
├── pocketbase_client.py   # Async PocketBase REST client
├── dashboard.html         # Browser UI (single file, zero build step)
└── tests/
    ├── conftest.py                # Shared fixtures
    ├── test_sandbox_manager.py    # 22 tests — path safety, CRUD, limits
    └── test_agent_protocol.py     # 15 tests — parsing, prompts, validation
```

---

## Startup Procedure

The full startup procedure, agent loop protocol, SSE event schema, action format, configuration reference, architecture diagram, and landscape comparison are documented in:

**[`_policies/STARTUP_PROCEDURE.md`](../../_policies/STARTUP_PROCEDURE.md)**

This file is the canonical reference. The app reads from it and the README points to it.

---

## Configuration

| Flag | Default | Description |
|------|---------|-------------|
| `--port` | 3000 | Nerve center port |
| `--llama-port` | 8080 | llama-server port |
| `--pb-port` | 8090 | PocketBase port |
| `--model-path` | `~/google_gemma-4-E4B-it-Q4_K_M.gguf` | GGUF model |
| `--clone` | off | Use git clone instead of worktree |
| `--no-llama` | off | Skip llama-server (already running) |
| `--no-pocketbase` | off | Skip PocketBase |
| `--no-copilotkit` | off | Skip cloning CopilotKit |
| `--no-browser` | off | Don't auto-open browser |

Override via Makefile vars: `make dev LLAMA_PORT=9090 MODEL_PATH=/path/to/model.gguf`

---

## How the Agent Talks

The model emits file operations as fenced JSON blocks:

```
I'll explore the project structure.

:::action
{"tool": "list_files", "path": "copilotkit"}
:::

Now let me read the main README.

:::action
{"tool": "read_file", "path": "copilotkit/README.md"}
:::
```

Tools: `list_files`, `read_file`, `write_file`, `delete_file`. All paths sandboxed. No code execution — file I/O only.

---

## Safety

- All file operations are jailed to the sandbox directory
- Path traversal (`..`), absolute paths, and symlink escapes are blocked
- Per-file limit: 1MB. Total sandbox limit: 50MB
- The sandbox is a disposable copy — `make clean` nukes everything
- The model cannot execute code, only read/write/list/delete files

---

## Part of SimpleAgentOS

Lerna Hydra is designed as a **battery** for [SimpleAgentOS](_experiments/SimpleAgentOS/). The nerve center is the waft server that SimpleAgentOS bounces requests off of. The PocketBase schema is compatible with SimpleAgentOS's transmission format.

---

*Built with waft, llama.cpp, PocketBase, and FastAPI. FogSift design system.*
