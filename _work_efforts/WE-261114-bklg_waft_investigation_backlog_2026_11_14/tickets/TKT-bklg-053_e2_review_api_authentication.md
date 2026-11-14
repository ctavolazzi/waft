---
id: TKT-bklg-053
title: "E2 Review API authentication"
status: pending
created: 2026-11-14T15:43:40.225Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# E2 Review API authentication

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P1`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `waft serve` run from a scratch project exposes an OpenAPI schema with 95 paths and 106 operations. 41 are writes (POST, PUT, PATCH, DELETE) and only 13 operations declare the HTTPBearer scheme. Called without a token: `POST /api/work-efforts` returns 401, but none of the other 28 write routes I called (all but `/api/pet/reincarnate`, which I skipped) returned 401: 200 for `/api/5050/continue-command`, `/api/being/spawn`, `/api/pet/feed`, `/api/protocel/create` and `/api/story/start` (plus `/api/auth/handshake`, see E16); 404 for 7 routes called with a made-up id; 422 for 14 routes called with an empty body; 500 for `/api/being/{id}/decision`. `GET /api/work-efforts` is open too.

**First step.** decide the policy (every non-GET route needs the token except the handshake); apply it router-wide; add a test that walks the OpenAPI schema and asserts 401 without a token.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading E2.
