# Validation - WE-260301-agct

## Context

- Date: 2026-03-01
- Target: `agentchattr` server-only setup
- Repo path: `/Users/ctavolazzi/Code/active/agentchattr`

## Prerequisites

- `python3 --version` -> `Python 3.14.3`
- `tmux -V` -> not found (`tmux` is optional for server-only)

## Execution

- Cloned repository:
  - `git clone https://github.com/bcurts/agentchattr.git`
- Started server-only launcher:
  - `sh macos-linux/start.sh`

## Runtime Evidence

- Startup output indicates active services:
  - Web UI: `http://127.0.0.1:8300`
  - MCP HTTP: `http://127.0.0.1:8200/mcp`
  - MCP SSE: `http://127.0.0.1:8201/sse`

- Listening port checks:
  - `127.0.0.1:8300` LISTEN
  - `127.0.0.1:8200` LISTEN
  - `127.0.0.1:8201` LISTEN

- Endpoint responses:
  - `curl http://127.0.0.1:8300/` -> HTTP `200`
  - `curl http://127.0.0.1:8200/mcp` -> HTTP `406` (reachable endpoint)
  - `curl --max-time 3 http://127.0.0.1:8201/sse` -> HTTP `200` before stream timeout

## Result

Server-only setup validated successfully. Web UI and MCP endpoints are reachable, and no agent launcher setup was required.
