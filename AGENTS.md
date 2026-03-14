# AGENTS.md

## Cursor Cloud specific instructions

### Overview

WAFT is a Python meta-framework for directed evolution of self-modifying AI agents. The core service is the `waft` CLI (entry point: `src/waft/main.py`). There is also an optional FastAPI web dashboard (`waft serve`).

### Critical: The `empirica` dependency

The `empirica` package is declared as a local editable source at `_unified/empirica/` in `pyproject.toml` `[tool.uv.sources]`, but `_unified/` is gitignored and never committed. Before running `uv sync`, you must download the empirica source from PyPI and extract it there:

```bash
mkdir -p _unified
pip3 download empirica==1.2.3 --no-binary :all: --no-deps -d /tmp/empirica_dl
cd /tmp/empirica_dl && tar -xzf empirica-1.2.3.tar.gz
cp -r empirica-1.2.3 /workspace/_unified/empirica
```

### Standard commands

See `CONTRIBUTING.md` for the canonical dev workflow. Key commands:

- **Install deps:** `uv sync --extra dev`
- **Editable install:** `uv tool install --editable .`
- **Lint:** `uv run ruff check .`
- **Format:** `uv run ruff format .`
- **Tests:** `uv run pytest tests/ -v --ignore=tests/test_foundation.py --ignore=tests/test_full_system.py --ignore=tests/test_the_absolute_begeesus.py`
- **Run web dashboard:** `uv run waft serve --port 8080`
- **Quick dev reinstall:** `./scripts/dev-reinstall.sh`

### Testing caveats

- Three test files (`test_foundation.py`, `test_full_system.py`, `test_the_absolute_begeesus.py`) have module-level code that fails during collection. These are pre-existing and must be `--ignore`d when running pytest. Additionally, `narcissus_lab/internal_monologue/test_oracle_wiring.py` causes an `INTERNALERROR` if pytest collects outside `tests/`. Always scope pytest to `tests/`.
- ~19 pre-existing test failures exist across `test_api.py`, `test_core.py`, `test_cors.py`, `test_persistence.py`, `test_transformer.py` due to missing imports or API issues in the codebase. 290+ tests pass.

### CLI caveat: `waft new` hangs

`waft new <name>` hangs indefinitely at "Initializing Empirica for epistemic tracking..." because it spawns a subprocess (`empirica project-init`) that blocks. Use `waft verify`, `waft info`, `waft observe`, `waft character`, and `waft serve` for testing instead.

### Web dashboard note

`waft serve` starts a FastAPI/uvicorn server. The SvelteKit frontend in `visualizer/` is optional and requires a separate `npm run build`. Without it, the server runs in API-only mode.
