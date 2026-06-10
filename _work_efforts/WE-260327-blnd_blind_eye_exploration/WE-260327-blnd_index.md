# Work Effort: Blind-eye exploration (new developer pass)

## Status: In Progress
**Started:** 2026-03-27 08:00 PDT  
**Last Updated:** 2026-03-27 08:00 PDT  

## Objective
Explore the `waft` repo as a brand-new developer: map structure, entry points, runtime flows, dependencies, tests, docs, and integration boundaries. Produce a concise, evidence-backed exploration report plus open questions/unknowns.

## Assumptions (for “blind-eye”)
- Do not rely on prior exploration writeups as “truth”; treat them as historical artifacts only.
- Prefer direct evidence from code, commands, and current repo contents.

## Tasks
1. [ ] Capture repo structure map (key directories/files)
2. [ ] Identify primary entry points (CLI + optional web)
3. [ ] Enumerate configs and dependency boundaries (pyproject/uv, empirica, etc.)
4. [ ] Map core modules and their responsibilities
5. [ ] Trace 2–3 critical user journeys (e.g. `waft --help`, `waft info`, `waft verify`, `waft serve`)
6. [ ] Review tests: organization, scope, known caveats, fastest “smoke” command
7. [ ] Note patterns & conventions (CLI style, error handling, logging)
8. [ ] Produce “unknowns / questions” list for next developer

## Progress
- ✅ Located primary package code in `src/waft/` and project config in `pyproject.toml`
- ⚠️ CLI currently blocked by import-time crash in `waft.main`
- ⚠️ Fresh `uv run pytest ...` on Python 3.14 blocked by `pydantic-core` build failure (PyO3 max Python 3.13)

## Notes / Findings (live)
### Findings
- **CLI entrypoint exists but currently broken**: `pyproject.toml` defines console script `waft = "waft.main:main"`, but running `waft --help` fails at import time with `NameError: name 'awakening_app' is not defined` at `src/waft/main.py:1041` (`app.add_typer(awakening_app, name="awaken")`).
- **`python -m waft` doesn’t work** (no `waft.__main__`), so “module execution” isn’t a fallback for new devs right now.
- **Python 3.14 currently breaks a clean test run**: `uv run pytest tests/ ...` tried to build `pydantic-core` and failed because PyO3 (0.24.1) does not yet support Python 3.14. This blocks “fresh clone → run tests” on 3.14 without extra env/config.
- **`/recap-and-review` PDF generation bug**: `RecapAndReviewManager._generate_pdf()` tried to call `pandoc` and raised `FileNotFoundError` before reaching the WeasyPrint fallback. This was fixed by catching `FileNotFoundError` and falling back to `markdown + weasyprint` (file: `src/waft/core/recap_and_review.py`).

### Unknowns
- **Why isn’t `awakening_app` imported/defined in `waft.main`?** There is a `src/waft/cli/awakening_cli.py` file, so this looks like a missing import or a rename mismatch (blocking all CLI usage).

## Blind-eye exploration report (draft)

### 1) Repo shape (what you see on first `ls`)
- The repo root contains **a very large volume of artifacts** (PDFs, HTML exports, research notes, demos, experimental outputs, and many subprojects). A new dev needs a “where’s the actual package?” pointer.
- The **packaged Python code** is under **`src/waft/`** (set by `[tool.setuptools] package-dir = {"" = "src"}` in `pyproject.toml`).

### 2) Primary entry points
- **CLI**: declared in `pyproject.toml` as `waft = "waft.main:main"`.
  - Current state: **broken at import time** due to missing `awakening_app` symbol in `src/waft/main.py`.
  - The intended “awaken” sub-CLI exists as `src/waft/cli/awakening_cli.py` (exports `app = typer.Typer(...)`), suggesting `waft.main` needs to import it (or the symbol name changed).
- **Web/API**: FastAPI app factory at `src/waft/api/main.py:create_app(project_path, static_dir=None)`.
  - Includes many route modules (work efforts, projects, empirica, gym, biome, etc.) and CORS allowlist for localhost dev.

### 3) Dependencies and runtime constraints (from `pyproject.toml`)
- **Python requirement**: `requires-python = ">=3.12"`.
- **Key deps**:
  - CLI/UI: `typer`, `rich`
  - Validation: `pydantic` (brings `pydantic-core`)
  - Web: `fastapi`, `uvicorn[standard]`
  - Content/PDF: `fpdf2`, `weasyprint`, `jinja2`, `pypdf`, `markdown`, `beautifulsoup4`
  - Misc: `tinydb`, `httpx`, `streamlit`, `d20`
- **Sharp edge (new dev blocker)**: on this machine, `uv` used **Python 3.14.3** and failed building `pydantic-core` because PyO3 max supported Python is 3.13. Practical implication: new dev should pin to **Python 3.12/3.13** (or use ABI forward-compat env var) before expecting `uv sync` / tests to work.

### 4) Core architecture (quick map)
- `src/waft/core/orchestrator.py` defines `SystemOrchestrator`: a **lazy-initialization facade** that hands out system components (BeingSystem, KarmaMerchant, TavernKeeper, RealitySystem, Scint detector, etc.) and coordinates cross-system operations.
- `src/waft/core/memory.py` defines `MemoryManager`: manages `_pyrite/{active,backlog,standards}` structure (project memory layer).
- The codebase appears to contain multiple “domains” beyond the core framework (D&D/tavern, evolution tooling, pantheon entities, template systems, visualizer API, etc.). A new dev likely needs a **curated “core vs realms” map** to avoid drowning.

### 5) Security/auth (API quick glance)
- `src/waft/api/auth.py` implements a **local token file** auth scheme:
  - token stored at `.waft_api_token` in the project root
  - attempts to enforce `0o600` file permissions (warns if too-open)
  - used as Bearer token for write operations (per API docs in `create_app`)

### 6) Testing (current reality)
- There is a large `tests/` suite, but an attempted “new dev” run via `uv run pytest tests/ ...` failed **before tests** due to the Python 3.14 / `pydantic-core` build issue.
- Next step (once Python is pinned to 3.12/3.13): rerun a minimal smoke subset to validate the environment and confirm whether the CLI break is covered by tests.

### 7) Recommended “first fixes” for onboarding
1. **Fix `waft` CLI import crash** (missing `awakening_app` import / symbol mismatch).
2. **Document supported Python versions for local dev** (explicitly “3.12/3.13”; avoid 3.14 until deps catch up).
3. Add a short “Start here” note in README (or a dedicated `docs/NEW_DEV.md`) that points to:
   - `src/waft/` as the package
   - `pyproject.toml` scripts
   - how to run API (`uvicorn` entry) once deps are installed

## Deliverable
An exploration report that includes:
- structure map
- architecture overview (modules + data flow)
- dependency & integration points
- testing & quality tooling
- documentation map
- risks / sharp edges
- next steps for a new developer

