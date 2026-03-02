# Work Effort: WAFT Docker/Ollama Runtime

## Status: Completed
**Started:** 2026-03-01 18:55 PST
**Last Updated:** 2026-03-01 19:22 PST

## Objective
Implement a dockerized WAFT API runtime with Ollama-compatible v1 endpoints (`/api/generate`, `/api/tags`) using existing WAFT FastAPI runtime behavior.

## Tasks
1. [x] Create Ollama-compatible API adapter routes
2. [x] Wire new routes into FastAPI app
3. [x] Add Docker runtime files (`Dockerfile`, `.dockerignore`, `docker-compose.yml`)
4. [x] Add deterministic project-path runtime configuration for containers
5. [x] Add tests for health/tags/generate
6. [x] Update README and docs with container runtime instructions
7. [x] Validate API behavior locally (syntax and endpoint contract checks)

## Progress
- Created dedicated work effort for this implementation.
- Selected v1 endpoint scope: `/api/generate` and `/api/tags` (defer `/api/chat`).
- Confirmed container runtime default strategy: `uvicorn src.waft.api.main:app --host 0.0.0.0 --port <PORT>`.
- Added `src/waft/api/routes/ollama.py` with Ollama-style `/api/tags` and `/api/generate`.
- Wired new router in `src/waft/api/main.py`.
- Added root runtime artifacts: `Dockerfile`, `.dockerignore`, `docker-compose.yml`.
- Added deterministic default project path bootstrap via `WAFT_PROJECT_PATH` in `src/waft/api/main.py`.
- Added endpoint tests in `tests/api/test_ollama_runtime.py`.
- Added runtime docs in `docs/DOCKER_OLLAMA_RUNTIME.md` and README usage block.
- Performed syntax validation with `python3 -m py_compile` on changed Python files.
- Could not execute pytest in this environment due missing configured Python/pytest runtime (`pyenv` targets unavailable `3.12`; local `python3.10` lacks pytest).
- Installed runtime/test dependencies in `pyenv 3.14.3`, then validated `tests/api/test_ollama_runtime.py` (4 passed).
- Fixed Docker startup by adding missing WeasyPrint system libraries in `Dockerfile`.
- Re-ran container verification with successful responses from:
  - `GET /api/health`
  - `GET /api/tags`
  - `POST /api/generate` (stream and non-stream)
- Prepared branch-safe GitHub update scope for clean commit/PR (only wdor runtime files).

## Next Steps
1. Merge PR and confirm CI/runtime validation in remote checks.
2. Decide whether to add `/api/chat` in next iteration.
3. Consider trimming optional heavy dependencies for slimmer API-only image.

## Notes
- Keep `waft serve` and `waft dashboard-5050` behavior unchanged.
- Keep changes additive; avoid unrelated CLI refactors.
