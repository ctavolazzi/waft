# Execute

Run a full execution cycle with explicit safety and verification gates.

## Required flow

`/execute` always runs this sequence in order:

1. **Oracle consultation**
   - Ask Oracle for readiness and risk framing.
   - Capture gate signal: `PROCEED`, `HALT`, `BRANCH`, or `REVISE`.
2. **Context gather**
   - Pull current git state, active work efforts, changed files, and relevant project context.
3. **Plan check**
   - Validate execution plan against Oracle signal and current constraints.
   - If confidence is low or uncertainty is high, branch to investigation before edits.
4. **Execution**
   - Perform the requested command/instruction with context-aware decisions.
5. **Verification**
   - Run focused checks (tests/lint/route checks/file parity) and report concrete evidence.

## Use when

- Work is non-trivial or has multiple moving parts.
- You need traceable reasoning before edits.
- You want explicit verification before declaring done.

## Avoid when

- Task is a one-step read-only query.
- You already have complete validated context for a trivial action.

## Example

```text
/execute implement the Oracle profile endpoint and UI, then verify routes and tests
```

Expected behavior: oracle consult -> context gather -> plan check -> implementation -> validation output.
