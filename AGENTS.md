# AGENTS.md

Notes for an agent (or a person) starting work in this repository. Every command here was run
on 2026-11-14 on Linux with Python 3.14.3 and 3.12.3.

## What this is

WAFT is a Python project whose core is the lab: a loop that breeds agent variants on real
tasks and records the run so it can be checked (`waft lab`, see `docs/LAB.md`). The CLI entry
point is `src/waft/main.py`. A FastAPI app (`waft serve`) and many experiments live around it.

## Set up

```bash
uv sync --extra dev
```

That is all. `empirica` comes from PyPI through `uv.lock`. (An older version of this file said
it had to be downloaded by hand into `_unified/empirica`; that was never true of this branch.)

For the PDF-to-PNG tests install poppler (`apt-get install poppler-utils` or `brew install poppler`).

## Commands

| What | Command |
|---|---|
| Every test | `uv run pytest` |
| The lab's own checks | `uv run waft lab doctor` |
| Undefined names in the package | `uv run ruff check src/waft --isolated --select E9,F63,F7,F82` |
| Lint with the project settings | `uv run ruff check .` (these settings exclude most of the tree by folder name, so it checks little) |
| A wheel that starts | `uv build --wheel -o dist`, install it in a fresh venv, run `waft --help` from another folder |
| The API | `uv run waft serve --port 8080` |
| A lab run | `uv run waft lab run` |

Run tests through `uv run` (or with `.venv/bin` on `PATH`): one test looks for the `empirica`
command.

## Things that will bite

- **Tests are configured in `pyproject.toml`.** `uv run pytest` collects `tests/test_*.py` only.
  Three files are ignored by name there because they fail while being imported
  (`test_foundation.py`, `test_full_system.py`, `test_the_absolute_begeesus.py`); fixing or
  retiring them is open work. `tests/real_proof_test.py` and the `*_suite.py` files are scripts.
- **The suite must leave the checkout unchanged.** CI fails otherwise. `tests/conftest.py` sends
  trace files to a temp folder and switches the Dealer off (`WAFT_DEALER=off`); a waft command
  run by hand from the repository root can still rewrite `_pantheon/the_dealer/`.
- **Import `waft`, never `src.waft`,** inside the package and its tests. The exception is tests
  of the `scripts/` folder, whose scripts import `src.waft` themselves.
- **Lab tests block the network.** Any connection that is not to this machine fails the test.
- **The API trusts this machine only.** Remote clients need the token in `.waft_api_token`;
  see `src/waft/api/auth.py`.
- **`waft.record` is vendored.** Keep `custody.py`, `schemas.py`, `schemas/`, `node/verify.mjs`
  and `CUSTODY.md` identical to their source in the FogSift system.
- **From an installed wheel, 18 modules still do not import**: demos with bare imports, two that
  need `scientific_method_tool` from a checkout, one that needs `pygame`, and `waft.rag`
  (its submodule is not initialised). The CLI, the API and the lab do.
- **No em dashes or en dashes** in anything written here.

## Work tracking

Work efforts live in `_work_efforts/` and are managed with `_pyrite`. The two that describe
the current state are `WE-261114-bklg` (what was found) and `WE-261114-dirn` (the direction
and the plan).
