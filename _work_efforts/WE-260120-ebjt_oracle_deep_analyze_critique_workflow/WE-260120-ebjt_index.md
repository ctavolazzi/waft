---
id: WE-260120-ebjt
title: "Oracle Deep Analyze Critique Workflow"
status: active
created: 2026-01-21T05:06:16.014Z
created_by: ctavolazzi
last_updated: 2026-03-01T18:36:00.000Z
branch: feature/WE-260120-ebjt-oracle_deep_analyze_critique_workflow
repository: waft
---

# WE-260120-ebjt: Oracle Deep Analyze Critique Workflow

## Metadata
- **Created**: Tuesday, January 20, 2026 at 9:06:16 PM PST
- **Author**: ctavolazzi
- **Repository**: waft
- **Branch**: feature/WE-260120-ebjt-oracle_deep_analyze_critique_workflow

## Objective
Run oracle → deep-analyze → critique → check-assumptions/verify → respond-to-critique → science-bitch → another-cycle → auto-work, while maintaining a bananote research booklet and updating devlog/work effort records.

## 2026-03-01 Expansion Objective
Bring `waft oracle` and `/consult-the-oracle` into strict alignment with current Empirica workflow and schema (v1.6 era), including MCP server readiness, so Oracle responses are epistemically grounded instead of heuristic-only.

## Tickets

| ID | Title | Status |
|----|-------|--------|
| TKT-ebjt-001 | Audit Oracle + Empirica docs/contracts vs current WAFT implementation | completed |
| TKT-ebjt-002 | Refactor Oracle CASCADE flow to use canonical flat vectors + real CHECK payloads | completed |
| TKT-ebjt-003 | Add Cursor/headless-safe Empirica instance resolution for Oracle flows | completed |
| TKT-ebjt-004 | Add project MCP server config for empirica-mcp epistemic mode | completed |
| TKT-ebjt-005 | Validate behavior via targeted tests and command checks | completed |
| TKT-ebjt-006 | Add MCP-first Empirica Brain Handler (COI) with automatic fallback chain | completed |
| TKT-ebjt-007 | Create transport jungle gym harness for fallback-path validation | completed |
| TKT-ebjt-008 | Create Pantheon brain-realm steward entity with MCP governance + fallback oversight | completed |
| TKT-ebjt-009 | Sync `/oracle` + `/consult-the-oracle` command docs to new brain-realm runtime model | completed |
| TKT-ebjt-010 | Add early-access Oracle kickoff commands (`/alrighty-then` and `/aa`) with anti-drift checks | completed |

## Progress
- Created bananote research booklet and compiled PDF
- Ran `waft oracle` (captured NameError)
- Deep analyze + critique documents generated
- Check-assumptions attempt logged with verification trace
- Science-bitch run executed (context artifact captured)
- Another-cycle manual outputs created
- 2026-03-01 17:24 PST: Re-activated effort for Oracle+Empirica hardening. Gathered canonical docs from local `empirica` repo and WAFT docs. Confirmed current mismatch points: non-canonical CHECK payloads, mixed vector schemas, and postflight deltas not computed from real state.
- 2026-03-01 17:24 PST: Drafted execution plan (schema alignment, CASCADE gate correctness, instance resolution, MCP config, validation).
- 2026-03-01 17:29 PST: MCP startup failure root-caused from Cursor logs (`empirica-mcp: command not found`). Verified environment state: repo `.python-version` points to missing `3.12`; active Empirica exists on pyenv `3.14.3`.
- 2026-03-01 17:31 PST: Installed `empirica-mcp==1.6.0` into user environment and switched project MCP config to absolute executable path (`/Users/ctavolazzi/.local/bin/empirica-mcp`) with explicit workspace + epistemic env vars.
- 2026-03-01 17:35 PST: Implemented Oracle/Empirica contract fixes in `src/waft/core/science/oracle.py`: canonical flat vectors for CASCADE submissions, normalized CHECK decision handling (`PROCEED/INVESTIGATE/HALT/BRANCH/REVISE`), and meaningful postflight deltas.
- 2026-03-01 17:37 PST: Implemented headless-safe instance project mapping + robust command/output handling in `src/waft/core/empirica.py`.
- 2026-03-01 17:40 PST: Added MCP-first fallback COI behavior in `src/waft/core/empirica_handler.py` (`mcp -> api placeholder -> cli -> degraded`) with explicit backend status and automatic fallback reasons.
- 2026-03-01 17:41 PST: Validation complete: `tests/test_empirica_brain.py`, focused `tests/test_empirica_validation.py` selection, and full `tests/test_bot.py` all pass.
- 2026-03-01 17:46 PST: Added jungle gym harness at `scripts/empirica_jungle_gym.py` to run simulated transport matrix (`mcp`, `cli`, `degraded`) and optional live cycle.
- 2026-03-01 17:46 PST: Added `tests/test_empirica_jungle_gym.py` and validated:
  - `python3 scripts/empirica_jungle_gym.py --mode simulated` -> 3/3 pass
  - `python3 -m pytest tests/test_empirica_jungle_gym.py` -> pass
- 2026-03-01 17:55 PST: Added Pantheon steward entity `ThePonderingOne` (`src/waft/pantheon/pondering_one.py`) to govern the Empirica brain realm with MCP-first setup, health status, and jungle-gym execution.
- 2026-03-01 17:56 PST: Integrated `ThePonderingOne` into Pantheon exports and council deliberation flow (`src/waft/pantheon/__init__.py`, `src/waft/cli/pantheon_command.py`).
- 2026-03-01 17:57 PST: Added steward tests (`tests/test_pondering_one.py`) and validated:
  - `python3 -m pytest tests/test_pondering_one.py tests/test_empirica_jungle_gym.py` -> pass
  - `python3 scripts/empirica_jungle_gym.py --mode simulated` -> 3/3 pass
- 2026-03-01 18:29 PST: Updated `.cursor/commands/oracle.md` as source-of-truth for new Oracle runtime contract (ThePonderingOne governance, MCP-first fallback posture, `INVESTIGATE` gate state, brain realm status output).
- 2026-03-01 18:29 PST: Slimmed `.cursor/commands/consult-the-oracle.md` to a true alias doc to remove duplicated behavior text and prevent spec drift.
- 2026-03-01 18:29 PST: Added verification script `scripts/verify_oracle_command_docs.py` and validated command-doc sync (`OK: oracle command docs are synced and policy-complete.`).
- 2026-03-01 18:36 PST: Added kickoff command `.cursor/commands/alrighty-then.md` as human-readable "start everything" Oracle entrypoint with governance-first execution plan.
- 2026-03-01 18:36 PST: Added short alias `.cursor/commands/aa.md` so command appears early in command lists and is fast to type.
- 2026-03-01 18:36 PST: Extended `scripts/verify_oracle_command_docs.py` to enforce the new alias chain (`/aa` -> `/alrighty-then`) and prevent command drift.

## Next Steps
1. Run `waft pantheon` to include `ThePonderingOne` guidance in full council judgment.
2. Run live jungle gym cycle: `python3 scripts/empirica_jungle_gym.py --mode live`.
3. Optionally wire true JSON-RPC MCP tool invocation path (currently health-gated MCP-first selection, execution still CLI-compatible).
4. Add `python3 scripts/verify_oracle_command_docs.py` to CI or pre-commit to enforce command-spec sync.

## Commits
- (populated as work progresses)

## Related
- Docs: (to be linked)
- PRs: (to be added)
