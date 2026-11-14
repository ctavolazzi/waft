---
id: TKT-bklg-151
title: "E15 Tighten the 20 other servers outside src"
status: pending
created: 2026-11-14T16:06:01.424Z
labels: ['pyrite']
---

# E15 Tighten the 20 other servers outside src

## Description

Evidence and first step are in the Notes below and in INVESTIGATION_BACKLOG.md.

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** 20 tracked Python files outside `src/` start a FastAPI, Flask or `HTTPServer` app. 7 allow every origin (`allow_origins=["*"]`): `cute_test_runner/server.py`, `dnd_campaign_desktop_app/backend/campaign_server.py`, `examples/dnd_game_server.py`, `recap_review_app/backend/main.py`, `scripts/mission_control_village_api.py`, `scripts/quest_server.py` and `simulation/simulation_server.py`. 9 bind `0.0.0.0`: `_realms/odd_realm/app.py`, `api/guide_api.py`, `cute_test_runner/server.py`, `examples/dnd_game_server.py`, `scripts/launch_dnd_campaign.py`, `scripts/mission_control_village_api.py`, `scripts/research_simulation_server.py`, `simulation/simulation_server.py` and `typst-webapp/backend/main.py`. None uses `debug=True`. Whether any of them is still used was not checked. `games/teleport_massive_adventure/scripts/start_autoplayer.sh:14` also runs `python3 -m http.server 8000` with no `--bind`, which serves the game folder on every interface and collides with the API port.

**First step.** list which servers are live; delete or archive the rest (with CT's approval); for the live ones default to localhost and name the allowed origins.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading E15.
