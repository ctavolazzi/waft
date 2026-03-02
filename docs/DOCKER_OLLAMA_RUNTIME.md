# WAFT Docker Ollama-Compatible Runtime

## Purpose

Provide a deterministic container runtime for WAFT API using Ollama-compatible v1 endpoints while preserving existing WAFT CLI serving behavior.

## Endpoints (v1)

- `GET /api/health`
- `GET /api/tags`
- `POST /api/generate`

`/api/chat` is intentionally deferred in this iteration.

## Runtime Defaults

- API command: `uvicorn src.waft.api.main:app --host 0.0.0.0 --port 8000`
- Container env:
  - `WAFT_PROJECT_PATH=/app`
  - `PORT=8000`

`WAFT_PROJECT_PATH` is used by `src/waft/api/main.py` for deterministic project path bootstrap when running via direct uvicorn entrypoint.

## Build and Run

```bash
docker compose up --build
```

## Verify API

```bash
curl http://localhost:8000/api/health
curl http://localhost:8000/api/tags
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model":"waft-echo:latest","prompt":"hello waft","stream":false}'
```

Streaming example:

```bash
curl -N -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model":"waft-echo:latest","prompt":"stream hello","stream":true}'
```

## External Reachability Check

Confirm service binds on all interfaces in-container (`0.0.0.0`) and is reachable on host:

```bash
curl http://127.0.0.1:8000/api/health
```

If running from another machine on the same network, replace with host IP:

```bash
curl http://<host-ip>:8000/api/health
```

## Notes

- This runtime is additive and does not replace `waft serve` or `waft dashboard-5050`.
- Existing CLI defaults remain unchanged (`localhost` unless explicitly overridden).
