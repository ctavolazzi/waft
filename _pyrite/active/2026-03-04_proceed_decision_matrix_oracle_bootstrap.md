# Proceed + Decide - 2026-03-04

## Proceed Checks
- Objective clarity: yes (bootstrap readiness in new environments)
- Scope clarity: yes (oracle-cycle as first introspective tool)
- Evidence sufficiency: yes (artifact + run result + health probes)
- Blocking ambiguity: medium (CLI vs API command surface)
- Proceed recommendation: **Proceed with constrained implementation slice**

## Decision Matrix

### Alternatives
1. **A1**: Keep API-only operation and improve docs only
2. **A2**: Add thin CLI parity shim that calls current logic
3. **A3**: Refactor oracle-cycle architecture before exposing CLI

### Criteria and Weights
- Time-to-value (0.35)
- Operator clarity (0.30)
- Risk of regressions (0.20)
- Long-term maintainability (0.15)

### Scores (1-5)
- A1: Time 5, Clarity 2, Risk 5, Maintainability 2
- A2: Time 4, Clarity 5, Risk 4, Maintainability 4
- A3: Time 1, Clarity 4, Risk 2, Maintainability 5

### Weighted Totals
- A1: `5*0.35 + 2*0.30 + 5*0.20 + 2*0.15 = 3.65`
- A2: `4*0.35 + 5*0.30 + 4*0.20 + 4*0.15 = 4.30`
- A3: `1*0.35 + 4*0.30 + 2*0.20 + 5*0.15 = 2.70`

## Decision
**Choose A2 (thin CLI parity shim)**.

## Rationale
A2 gives the best balance of speed, operator confidence, and low regression risk while preserving the option to refactor internals later.
