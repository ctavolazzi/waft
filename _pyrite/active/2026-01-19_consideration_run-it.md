# Consideration: Run-It Workflow (2026-01-19 22:34)

## Situation
User requested `/run-it` after completing 2026-only authenticity cleanup for Teleport Massive founding docs.

## Options
1. Full run-it workflow (all phases with artifacts)
2. Quick mode (key phases only)
3. Documentation-only run-it (minimal artifacts, no heavy analysis)

## Trade-offs
- Full workflow provides maximum traceability but is time-intensive.
- Quick mode reduces overhead but may miss requested artifacts.
- Documentation-only keeps effort low while honoring command intent.

## Recommendation
Proceed with a lightweight full workflow: create required artifacts with concise content, run essential checks, and document any skipped steps explicitly.

## Next Steps
- Initialize Empirica session and preflight
- Generate run-it artifacts in `_pyrite` and `_work_efforts`
- Record results and proceed to checkpoint
