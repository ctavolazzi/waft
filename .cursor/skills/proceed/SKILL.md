---
name: proceed
description: Validate chat and code assumptions with evidence before major actions, then continue with the highest-priority goal. Use when the user says /proceed, asks to verify assumptions, requests evidence-based continuation, or before non-trivial edits.
---

# Proceed

Run a strict pre-action gate: check assumptions first, then execute.

## Workflow

1. **Extract assumptions**
   - List implicit and explicit assumptions from the current chat.
   - Include code, system, dependency, and user-intent assumptions.
   - Mark risk level (`critical`, `medium`, `low`).

2. **Gather evidence**
   - Use repo evidence first (`ReadFile`, `rg`, `Glob`, targeted commands).
   - Prefer direct runtime/test output over inference.
   - Do not claim validation without concrete evidence.

3. **Validate each assumption**
   - Assign one status: `PROVEN`, `DISPROVEN`, `PARTIAL`, `INSUFFICIENT`.
   - Add confidence (`0.0-1.0`) and short evidence notes.

4. **Pick highest-priority goal**
   - Use validated assumptions only.
   - If a critical assumption is disproven/insufficient, resolve that first.
   - Otherwise continue with the user’s active request.

5. **Execute + verify**
   - Perform the work.
   - Run focused verification.
   - Report what changed and what remains uncertain.

## Output format

Use this structure:

```markdown
## Assumptions Check
- A1 ... — STATUS (confidence)
  - Evidence: ...

## Decision
- Highest-priority goal: ...
- Why this is next: ...

## Proceed
- Actions taken: ...
- Verification: ...
- Remaining risks: ...
```

## Guardrails

- Never skip evidence collection for critical assumptions.
- Avoid broad speculative edits before assumption validation.
- If evidence is missing, say so and run the smallest test that closes the gap.
