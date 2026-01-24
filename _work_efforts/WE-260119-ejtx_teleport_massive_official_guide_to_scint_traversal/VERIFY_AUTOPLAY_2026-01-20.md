# Verify Autoplay Run (2026-01-20)

**Command**: `node scripts/slaytheweb_autoplay.mjs`

## Result
❌ Failed

## Error
```
Error [ERR_MODULE_NOT_FOUND]: Cannot find package 'immer' imported from /Users/ctavolazzi/Code/active/waft/_external/slaytheweb/src/game/actions.js
```

## Next Steps
- Install dependencies in `_external/slaytheweb` (e.g., `npm install` or `bun install`) or install `immer` specifically.
- Re-run `node scripts/slaytheweb_autoplay.mjs`.

## Retry (after dependency install + target fix)
**Command**: `node scripts/slaytheweb_autoplay.mjs`

✅ Success

**Output**:
`_work_efforts/WE-260119-ejtx_teleport_massive_official_guide_to_scint_traversal/autoplay_runs/stw_1768976034182_e5mfen.json`

## Additional Runs + Telemetry (2026-01-20)

**Commands**:
- `node scripts/slaytheweb_autoplay.mjs` (x3 total runs)
- `curl -X POST http://127.0.0.1:8133/telemetry/run ...`

✅ Success

**Outputs**:
- `_work_efforts/WE-260119-ejtx_teleport_massive_official_guide_to_scint_traversal/autoplay_runs/stw_1768977485016_tx5o4v.json`
- `_work_efforts/WE-260119-ejtx_teleport_massive_official_guide_to_scint_traversal/autoplay_runs/stw_1768977623234_uce2a8.json`
- `_work_efforts/WE-260119-ejtx_teleport_massive_official_guide_to_scint_traversal/autoplay_runs/stw_1768977623510_z0cn6m.json`
- `_work_efforts/WE-260119-ejtx_teleport_massive_official_guide_to_scint_traversal/telemetry_evidence.jsonl`

**Summary**:
- Runs: 3
- Avg turns: 24.0
- Avg rooms cleared: 7.67
- Win rate: 0%
