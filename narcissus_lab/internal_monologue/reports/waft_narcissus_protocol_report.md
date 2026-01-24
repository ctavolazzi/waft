# WAFT Narcissus Protocol — Phase 1 Report

Generated: 2026-01-21T00:15:51.782946+00:00 UTC

## Summary
- Run ID: 20260121001524
- Total trials: 50
- Experimental success rate: 55.00%
- Experimental 95% CI: 39.83% – 69.29%
- Control pass rate: 100.00%
- Control 95% CI: 72.25% – 100.00%

## Experimental Design
- Conditions: control (no sabotage) vs experimental (NARCISSUS_LOGIC_FRACTURE injected)
- Outcome: bug removed after NarcissusAgent proposes patch
- Safety: propose_patch validates syntax and writes backups

## Notable Failures (Mirage Events)
- Trial 11 | patch_attempted=True | note=hallucinated_fix
- Trial 12 | patch_attempted=True | note=repair
- Trial 13 | patch_attempted=True | note=repair
- Trial 14 | patch_attempted=True | note=hallucinated_fix
- Trial 15 | patch_attempted=True | note=repair
- Trial 16 | patch_attempted=True | note=repair
- Trial 17 | patch_attempted=True | note=repair
- Trial 18 | patch_attempted=True | note=hallucinated_fix
- Trial 19 | patch_attempted=True | note=hallucinated_fix
- Trial 20 | patch_attempted=True | note=hallucinated_fix
