# WAFT Promotion Protocol

Defines how work moves from personal development space (`active/waft`) to professional presentation surface (`FogSift/waft`).

## Intent

- `active/waft` is the experimental lab ("messy bedroom").
- `FogSift/waft` is the public trust surface ("best foot forward").
- Promotion is selective, evidence-based, and presentation-aware.

## Promotion Principles

1. **No direct mirror.** Promote distilled outcomes, not raw history.
2. **Evidence over enthusiasm.** If it is not validated, it is not ready.
3. **Narrative clarity.** Public docs should explain what, why, and how to run.
4. **Security hygiene.** Never promote private/internal artifacts.
5. **Small batches.** Promote in narrow, reviewable increments.

## Never Promote

- `_work_efforts/`, `_pyrite/`, `.empirica/`, local journals, local DBs
- personal session reports/checkpoints
- machine-local paths, machine-specific scripts, one-off probes
- unstable experiments without tests or clear rollback

## Promotion Gates

All gates must pass before opening a PR in `FogSift/waft`.

### Gate 1: Scope Gate

- Change has a clear user-facing purpose.
- Scope is minimal and coherent (single capability or closely related set).
- Public repo version is independent of personal workspace internals.

### Gate 2: Quality Gate

- Tests exist for core behavior.
- Local test run passes.
- Lint/format checks pass (or are not applicable with reason).
- No dead code or placeholder architecture.

### Gate 3: Documentation Gate

- README/docs updated with:
  - problem statement,
  - quickstart,
  - usage example,
  - constraints/known limits.
- "Deferred" section clearly states what is intentionally not shipped.

### Gate 4: Professional Surface Gate

- Names, wording, and examples are professional/public-safe.
- No internal jargon that requires private context.
- No references to personal-local process files.

### Gate 5: Security and Compliance Gate

- No secrets, tokens, keys, private URLs, or local environment leakage.
- License compatibility and attribution are clean.
- Public-safe defaults are used.

## Promotion Workflow

1. **Select candidate** in `active/waft` (small, proven slice).
2. **Extract clean spec** (what to carry, what to leave behind).
3. **Re-implement cleanly** in `FogSift/waft` against public constraints.
4. **Run validation** (tests/lints/docs sanity).
5. **Open PR** with concise rationale and verification evidence.
6. **Merge and tag** if milestone-worthy.

### CLI Review Gate

Run local escalation review before opening a professional PR:

```bash
waft promote review --path . --target-repo FogSift/waft --min-score 8 --max-files 30
```

Optional full gate with tests:

```bash
waft promote review --path . --run-tests --test-command "python -m pytest -q"
```

### Auto Demo (opens in Chrome)

Run an end-to-end demo that creates pass/fail candidates, runs review on both, writes reports, and opens results:

```bash
PYENV_VERSION=3.14.3 python scripts/promotion_review_demo.py
```

The demo now shows three cases:
- pass (promotion-ready),
- borderline (fails docs gate),
- fail (blocked internal artifacts).

## PR Template Addendum (Recommended)

Use this mini-checklist in promotion PRs:

- [ ] Scope is intentionally minimal
- [ ] No personal/internal artifacts included
- [ ] Tests pass locally
- [ ] Docs/README updated
- [ ] Deferred list included
- [ ] Security scan: no secrets or local path leakage

## Promotion Readiness Score (Optional)

Score each dimension 0-2. Promote at 8+ out of 10.

- Scope clarity
- Test confidence
- Documentation clarity
- Professional presentation quality
- Security/compliance hygiene

## First-Class Rule

If a change is useful but not yet clean, keep it in `active/waft` until it earns promotion.
