# Empirica Handler Guide — Waft Bot Architecture

**Version:** 0.1.0
**Date:** 2026-02-28
**Context:** Findings from Python 3.14 rollout session + Waft core exploration

---

## Section 1. Empirica CLI Contract (Verified Behavior)

### 1.1 Project Resolution

Empirica resolves the active project through an **instance file** chain — not CWD:

```
Priority 0: ~/.empirica/instance_projects/{instance_id}.json  (AUTHORITATIVE)
Priority 1: ~/.empirica/active_work_{claude_session_id}.json   (hook fallback)
Priority 2: None → explicit error, never falls back to CWD
```

**Instance ID** is resolved from (in order):
1. `EMPIRICA_INSTANCE_ID` env var
2. `TMUX_PANE`
3. `TERM_SESSION_ID` (macOS Terminal.app)
4. `WINDOWID` (X11)
5. TTY device name
6. `None` (legacy — resolution fails in headless/Cursor shells)

**Critical finding:** In Cursor agent shells, `get_instance_id()` returns `None`.
You must set `EMPIRICA_INSTANCE_ID` and write the instance file yourself:

```python
import json, os
from pathlib import Path

INSTANCE_ID = os.environ.setdefault("EMPIRICA_INSTANCE_ID", "waft-bot")
instance_dir = Path.home() / ".empirica" / "instance_projects"
instance_dir.mkdir(parents=True, exist_ok=True)
(instance_dir / f"{INSTANCE_ID}.json").write_text(json.dumps({
    "project_path": "/path/to/project",
    "project_id": "<uuid from empirica project-list>",
    "project_name": "my-project",
}))
```

### 1.2 Session Lifecycle

```
project-create  →  project-switch  →  session-create  →  preflight-submit  →  check-submit  →  [work]  →  postflight-submit
```

| Command | Input | Output |
|---|---|---|
| `empirica project-list --output json` | none | `{"ok": true, "projects": [...]}` |
| `empirica project-switch <name> --output json` | none | `{"ok": true, "project_id": "..."}` |
| `empirica session-create --ai-id <id> --output json` | none | `{"ok": true, "session_id": "..."}` |
| `empirica preflight-submit -` | `{"session_id": "...", "vectors": {...}, "reasoning": "..."}` | `{"ok": true, "transaction_id": "..."}` |
| `empirica check-submit -` | `{"session_id": "...", "vectors": {...}, "reasoning": "..."}` | `{"ok": true, "decision": "proceed"}` |
| `empirica postflight-submit -` | `{"session_id": "...", "vectors": {...}, "reasoning": "..."}` | `{"ok": true}` |

### 1.3 Vector Schema (Verified)

Vectors are **flat floats**, not nested dicts. The existing `EmpiricaBrain.DEFAULT_PREFLIGHT_VECTORS` uses nested dicts that will fail against the real CLI.

**Valid:**
```json
{"engagement": 0.7, "know": 0.6, "uncertainty": 0.3}
```

**Invalid (causes Pydantic validation error):**
```json
{"foundation": {"know": 0.6, "do": 0.6, "context": 0.6}}
```

Required keys: `know`, `uncertainty`. All others optional.

### 1.4 Check Gate Contract

`check-submit` also requires a `vectors` dict (not just signal/context metadata).
The gate returns one of: `proceed`, `investigate`, `halt`, `branch`, `revise`.

### 1.5 Sentinel Decisions

| Decision | Meaning | Action |
|---|---|---|
| `proceed` | Safe to continue | Continue work |
| `investigate` | Needs more data | Gather evidence, then re-check |
| `halt` | Stop, get human | Block until explicit approval |
| `branch` | Fork investigation | Spawn sub-task before merge |
| `revise` | Change approach | Modify plan and resubmit |

---

## Section 2. Existing Waft Empirica Layer

### 2.1 EmpiricaManager (`waft.core.empirica`)

CLI wrapper with subprocess calls. Key methods:
- `ensure_ready()` — auto-init + CLI check + session bootstrap
- `create_session()` — pipes JSON to `session-create -`
- `submit_preflight()` / `submit_postflight()` — pipes vectors to CLI
- `check_submit()` — sentinel gate
- `log_finding()` / `log_unknown()` — structured logging
- `project_bootstrap()` — loads ~800 token context

**Problem:** `_find_empirica_command()` hardcodes 3.12/3.11 framework paths and skips pyenv shims. On a pyenv-managed system this finds the wrong binary.

### 2.2 EmpiricaBrain (`waft.core.empirica_brain`)

Narrative engineering unit. Two capabilities:
1. `build_narrative_prompt()` — dungeon-framed engineering prompt
2. `run_cascade_cycle()` — full preflight → check → postflight cycle

**Problem:** Default vectors use nested dicts that fail against real Empirica CLI validation.

---

## Section 3. Bot Architecture

```
Bot(config)
├── brain        → EmpericaHandler (this guide's deliverable)
├── hands        → tool executors (shell, file, git)
├── legs         → navigation (project discovery, CWD management)
├── inventory    → loaded artifacts, cached state
├── state        → current phase, health, vector snapshot
├── port_in      → command/message ingestion
├── port_out     → response/artifact emission
├── journal      → structured log (findings, unknowns, decisions)
└── data         → raw context (bootstrap payload, project metadata)
```

The `EmpericaHandler` is the **brain** — it owns the session, manages the CASCADE lifecycle, and gates all operations through sentinel checks.

---

## Section 4. EmpericaHandler API Design

```python
handler = EmpericaHandler(
    project_path="/Users/ctavolazzi/Code",
    instance_id="waft-bot",
    ai_id="waft-brain",
)

# Lifecycle
handler.boot()                          # ensure project, write instance file, create session
handler.preflight(reasoning="...")      # submit opening vectors
result = handler.check(reasoning="...")  # gate check → proceed/halt/investigate/branch/revise
handler.log_finding("discovered X", impact=0.7)
handler.log_unknown("need to investigate Y")
handler.postflight(reasoning="...")     # submit closing vectors

# Queries
handler.session_id                      # current session UUID
handler.state                           # last known gate decision
handler.vectors                         # current vector snapshot
handler.is_ready                        # True after successful boot
```

### 4.1 Handler vs Manager

| | EmpiricaManager | EmpericaHandler |
|---|---|---|
| Scope | Low-level CLI wrapper | High-level lifecycle owner |
| Instance ID | Not managed | Auto-set + file written |
| Vectors | Caller provides | Defaults + auto-update |
| Session | Created on demand | Owned, single per handler |
| State | Stateless | Stateful (phase, vectors, gate) |
| Error handling | Returns None/False | Raises typed exceptions |

---

## Section 5. Known Gotchas

1. **Instance file required in Cursor/headless shells.** Always set `EMPIRICA_INSTANCE_ID` and write the JSON file before calling `session-create`.

2. **Vectors must be flat floats.** `{"know": 0.6, "uncertainty": 0.3}` not `{"foundation": {"know": 0.6}}`.

3. **`check-submit` needs vectors too.** Not just signal/context metadata.

4. **pyenv shim resolution.** `EmpiricaManager._find_empirica_command()` hardcodes framework paths. On pyenv systems, use `shutil.which("empirica")` or respect `PYENV_ROOT`.

5. **Python 3.14 argparse `%` escaping.** Empirica's `edit_verification_parsers.py` has a `help="80%"` literal that crashes under 3.14's stricter parser. Must be `"80%%"`.

6. **`project-switch` exit 0 ≠ success.** It returns `{"ok": false, ...}` with exit code 0. Always check the JSON `ok` field.
