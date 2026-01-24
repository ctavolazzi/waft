# PROOF CASE: Teleport Massive Autoplay Telemetry

**Case ID:** `case_20260120_224053`
**Date:** 2026-01-20 22:40:53
**Investigation Type:** Autoplay + Telemetry Evidence
**Status:** ⚖️ PARTIALLY PROVEN

---

## Executive Summary

**Claims Investigated:**
1. Headless slaytheweb autoplay can run and emit structured run data.
2. Telemetry server accepts run payloads and logs evidence.
3. UI automation can proceed beyond the intro overlay.

**Verdicts:**
- Claim 1: ✅ **PROVEN**
- Claim 2: ✅ **PROVEN**
- Claim 3: ⚠️ **INCONCLUSIVE** (UI overlay not advancing via accessibility tree)

**Key Findings:**
- ✅ 3 headless autoplay runs completed.
- ✅ Telemetry server wrote JSONL evidence log.
- ⚠️ UI automation reached "It begins…" overlay but "Open the map" did not advance.

---

## Investigation Details

### Methodology
1. Started the telemetry server: `python3 scripts/prove_it_telemetry_server.py`.
2. Ran three headless autoplay simulations: `node scripts/slaytheweb_autoplay.mjs`.
3. Posted run payloads to the telemetry server.
4. Attempted UI automation on `http://localhost:4321` using Playwright (accessibility tree).

### Evidence Files
- `_work_efforts/WE-260119-ejtx_teleport_massive_official_guide_to_scint_traversal/autoplay_runs/stw_1768977485016_tx5o4v.json`
- `_work_efforts/WE-260119-ejtx_teleport_massive_official_guide_to_scint_traversal/autoplay_runs/stw_1768977623234_uce2a8.json`
- `_work_efforts/WE-260119-ejtx_teleport_massive_official_guide_to_scint_traversal/autoplay_runs/stw_1768977623510_z0cn6m.json`
- `_work_efforts/WE-260119-ejtx_teleport_massive_official_guide_to_scint_traversal/telemetry_evidence.jsonl`

### Aggregate Metrics (Telemetry Evidence)
- Runs: **3**
- Avg turns: **24.0**
- Avg rooms cleared: **7.67**
- Win rate: **0%**

---

## Evidence Summary

### Claim 1 — Headless autoplay runs and produces data
**Verdict:** ✅ PROVEN
**Evidence:** Autoplay runs produced JSON outputs with turns, rooms cleared, win flag, and action logs.

### Claim 2 — Telemetry server logs run payloads
**Verdict:** ✅ PROVEN
**Evidence:** `telemetry_evidence.jsonl` contains 3 entries with `run_id`, timestamps, and metrics.

### Claim 3 — UI automation progresses beyond intro overlay
**Verdict:** ⚠️ INCONCLUSIVE
**Evidence:** UI loaded at `http://localhost:4321` and displayed the intro overlay. Playwright clicks on "Open the map" did not advance state via accessibility tree. Requires DOM-level selectors or manual input.

---

## Conclusion

The autoplay + telemetry pipeline is functional for headless simulation and evidence logging. UI automation requires additional work (DOM selectors or alternative automation strategy) to progress beyond the intro overlay. The telemetry system is ready to support further experiments and more robust AI-driven play logic.

---

## Next Steps

1. Add a UI automation helper that targets DOM selectors (not only accessibility nodes).
2. Expand autoplay heuristics (prioritize damage vs block based on HP).
3. Increase run count (e.g., 20+ runs) to measure stability and variance.
