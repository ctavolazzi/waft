---
id: TKT-bklg-152
title: "E16 Stop the handshake route from handing the API token to any caller"
status: completed
created: 2026-11-14T16:06:01.709Z
labels: ['pyrite']
---

# E16 Stop the handshake route from handing the API token to any caller

## Description

Evidence and first step are in the Notes below and in INVESTIGATION_BACKLOG.md.

## Status

- [x] Completed

## Notes

Tags: `M` `agent` `P1`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `api/routes/auth.py:42` to `:66`: `POST /api/auth/handshake` has no authentication, calls `get_or_create_token(project_path)` and returns the token in the response body (the docstring calls it a "one-time setup for local development"). Measured: it answered 200 to a call with no credentials and an empty JSON body. So the bearer scheme protects nothing from a client that can reach the port. `api/auth.py:82` compares tokens with `==` (not constant time); the token is a 32-byte `secrets.token_urlsafe` value stored in `.waft_api_token` with mode 600 and never expires. The Dockerfile starts uvicorn on `0.0.0.0:8000` (B10), so a container exposes the handshake to the network.

**First step.** limit the handshake to loopback clients (`request.client.host`) or hand the token over some other way (printed once at startup); use `hmac.compare_digest`; add expiry and rotation; add tests for all three.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading E16.

**2026-11-14 (build pass).** The handshake answers local clients only (403 otherwise), tokens are compared with hmac.compare_digest, and starting the server creates the token. Expiry and rotation are not built.
