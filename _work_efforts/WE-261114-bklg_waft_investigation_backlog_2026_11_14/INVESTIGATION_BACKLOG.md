# WAFT investigation backlog

**Date:** 2026-11-14  
**Work effort:** `WE-261114-bklg` (tickets use the same ids as this document)  
**Branch:** `claude/environment-setup-3whfys`  
**Status:** draft for review. Nothing in `src/` was changed.

## What this is

A list of 137 things for people (CT) and more capable agents to investigate, decide or expand on, found while setting up the WAFT environment and running the project. Each item has an id (such as `B2`), a tag for how well it is known, who can pick it up, a priority, the evidence, and a first step. The same ids are the ticket titles in this work effort, so a ticket can be claimed and closed without touching this document.

Priorities are my judgment, not a measurement: P1 means do first (broken, risky or blocks other work), P2 means soon, P3 means whenever.

## How to read the tags

| Tag | Meaning |
|---|---|
| `M` | measured in this session (the command or number is stated) |
| `R` | read from a file, a commit message or GitHub metadata; not run here |
| `Q` | a question or suspicion; nothing checked yet |

| Owner | Meaning |
|---|---|
| `agent` | a coding agent can do it |
| `CT` | needs a decision or an action from CT |
| `research` | needs reading, experiments or a more capable model |

Counts: 51 measured, 50 read, 36 questions. Owners: 87 agent, 30 CT, 20 research. Priorities: 26 P1, 53 P2, 58 P3.

## The first ten (best value for effort)

- **B1, B2, B3.** A wheel built from this repo cannot start the CLI (`ModuleNotFoundError: waft.templates.typst`). The hand-written package list ships 202 of 516 Python files.
- **A1 to A4, A18, C10.** The 25 red tests trace to a half-wired tracing module and to undefined names. One ruff rule (F821) finds 31 of them; it is not in CI.
- **C1.** CI runs the tests under `tests/api` only, roughly 7 percent of the suite, so the break reached `main` while CI stayed green.
- **D1.** 9,015 `node_modules` files are tracked.
- **D4.** Third-party PDFs, a book, a MediaWiki zip and papers sit in a public MIT repo with no recorded licences.
- **E1.** The Fernet key and the realm HMAC key are public in git history and are not recorded as rotated.
- **F2, F3.** `waft evolve` gave three variants the same id, every score was 100, improvement +0.00. What evolution acts on is undocumented.
- **G2.** At least 18 docs name commands that the CLI does not have.
- **G7, H1.** WAFT is not in `_workbench/STATE.md`, and the repo has no one-sentence purpose.
- **I1.** 132 work efforts: 69 active, 7 unreadable by pyrite.

## Record of this session

What I did, in order. Every command ran in the Linux container (Python 3.14.3 through uv). GitHub data came from the GitHub API, read only.

1. Installed the Node dependencies of five sibling repos with `npm ci` and tried `uv sync` in `_pyrite` (it failed: `../empirica` is missing).
2. In this repo, fetched Empirica 1.2.3: `pip3 download empirica==1.2.3 --no-binary :all: --no-deps`, extracted it, copied it to `_unified/empirica` (gitignored). AGENTS.md says to copy to `/workspace/_unified/empirica`; the path differs here (B4).
3. `uv sync --extra dev`, then `uv run waft --help` (82 commands).
4. Ran the tests with the command in AGENTS.md plus `--ignore=tests/test_commands.py` (it fails at collection, A6). Result: 25 failed, 516 passed, 23 skipped, 8 xfailed, 1 xpassed, 1 error in 78.9 s.
5. Traced the failures. Temporarily added `from .tracing import get_tracer` to two core modules, reran the suite (15 failed, 526 passed in 85.3 s), then reverted with `git checkout` (A1 to A4).
6. Ran `ruff` with the project config (passes) and with `--isolated` over `src` (268 findings, 31 of them undefined names).
7. Built a wheel with `uv build --wheel`, listed its contents, installed it in a clean venv and ran `waft --help` (fails, B1 and B2).
8. Ran the README quickstart from a scratch directory: `waft new demo`, `waft verify`, `waft evolve --generations 2 --variants 3` (F2, F14, G8).
9. Read GitHub metadata for `ctavolazzi/waft`: workflow runs, branches, pull requests, issues.
10. Read `_workbench` (FogSift FINDINGS, ROLLOUT, STATE.md, sessions/LOG.md) and ran `fogsift.py we list` here to see the existing work efforts (I1).
11. Wrote this document and created the work effort with `fogsift.py we create --todos-file`, which drives `_pyrite`.

**Changed in the repo:**

- Commit `4ad0eee1` added `_pyrite/analytics/traces/2026-11-14.jsonl`. A test run generated it and the session's stop hook asked for untracked files to be committed. It probably should not be tracked (A10, D8, L2).
- This work effort: `_work_efforts/WE-261114-bklg_*/` with the index, the tickets and this document.
- No file in `src/`, `tests/` or the config was changed. `uv.lock` and trace files that tools rewrote during the runs were restored with `git checkout`.
- Local only, ignored by git: `_unified/empirica/`, `.venv/`, `build/`.

**Not done:**

- The three test files AGENTS.md says to ignore were not run (A7). Docker was not built (B10). The Electron app, the SvelteKit visualizer and `waft serve` were not run. macOS and Windows were not tried (B11).
- Nothing was fixed. A1 to A3 are one-line or few-line changes I tested temporarily; I left them for review.
- No pull request was opened.

## Baseline (all measured 2026-11-14)

| What | Value | How |
|---|---|---|
| Source size | 516 Python files, about 174,000 lines; `main.py` 4,918 lines | `find src/waft -name '*.py' | xargs wc -l` |
| CLI | 82 top-level commands | `uv run waft --help` |
| Tests (baseline) | 25 failed, 516 passed, 23 skipped, 8 xfailed, 1 xpassed, 1 error; 78.9 s | `uv run pytest tests/ -q` with 4 files ignored |
| Tests (with temporary import fix) | 15 failed, 526 passed; 85.3 s | same, after adding two imports (reverted) |
| Ruff, project config | All checks passed | `uv run ruff check .` |
| Ruff, default rules on src | 268 findings (F401 99, F541 55, F821 31, E722 21, E402 19, F841 14, E741 12, E701 11, F811 4, E731 2) | `ruff check src --isolated --line-length 100 --statistics` |
| Wheel | 202 of 516 `.py` files, 0 data files; `waft --help` fails in a clean venv | `uv build --wheel`, then install and run |
| Tracked files | 19,741; `.git` pack 687 MiB; working tree 2.9 GB with `.venv` | `git ls-files`, `git count-objects -vH`, `du` |
| Tracked node_modules files | 9,015 | `git ls-files | grep -c node_modules` |
| Tracked PDFs | 3,082 | `git ls-files '*.pdf'` |
| Tracked Markdown, without node_modules | 3,680 | `git ls-files '*.md'` |
| Submodules | 8 declared, 0 initialized | `git submodule status` |
| Work efforts | 132: active 69, completed 27, open 16, pending 11, in_progress 1, template 1, unreadable 7 | `fogsift.py we list` |
| CI | 254 runs; runs 181 to 184 on main green; workflow tests `tests/api` only | GitHub API |
| Remote branches | 50 on the first page (42 `claude/*`); 1 open PR (#23); 1 open issue (#15) | GitHub API |
| Git tags | 0 | `git tag` |
| Subprocess use in src | 241 references, 14 `shell=True`, 4 `os.system`; no eval, exec, pickle.load, yaml.load | `grep` |
| Hardcoded `/Users/ctavolazzi` | 30 lines in 6 files under `src`; 433 tracked text files overall | `grep`, `git grep` |
| Debug blocks (`# #region agent log`) | 5 Python files | `grep -rIl --include=*.py` |
| Secret patterns in current tree | none found by five regexes (weak test) | `grep -rIlE` |

## Backlog

### A. Tests and the tracing module

The 25 red tests in the baseline come from two causes: a half-wired tracing module (A1 to A4) and a missing PDF library (A9). Most of the rest is test hygiene.

#### A1. Add the missing get_tracer imports in two core modules

`M` `agent` `P1`

**Evidence.** `src/waft/core/input_transformer.py:41` and `src/waft/core/decision_matrix.py:112` call `get_tracer()` and import nothing for it. Adding `from .tracing import get_tracer` to both (temporary edit, reverted) took the suite from 25 failed and 516 passed to 15 failed and 526 passed.

**First step.** apply the import for real, with a test that imports both modules and calls each once.

#### A2. Fix span.end() on a Span that has no end method

`M` `agent` `P1`

**Evidence.** `decision_matrix.py:132` calls `span.end(...)`. `Span` in `core/tracing/tracer.py` is a dataclass with no `end`; the tracer's method is `end_span(span, status, error=...)`. After A1 this raises AttributeError in `test_core.py::test_wsm_calculation`, `test_core.py::test_deterministic_tie_breaking` and `test_persistence.py::test_loaded_matrix_is_valid`.

**First step.** use `tracer.end_span` or add `Span.end`; decide which API is the intended one and make the callers agree.

#### A3. Import SpanStatus where input_transformer uses it

`M` `agent` `P1`

**Evidence.** `input_transformer.py` lines 75, 78 and 81 pass `SpanStatus.ERROR` to `end_span`; the name is never imported (NameError at line 77 in `test_transformer.py::test_missing_keys` and `test_invalid_number_strings`).

**First step.** import it from `.tracing`; read the other exception branches of that function for the same slip.

#### A4. Rerun the suite after A1 to A3 and list what is still red

`M` `agent` `P1`

**Evidence.** after A1 alone, `test_cors.py::test_actual_post_request_with_cors` still returns 500 and the six PDF tests still fail. The three `test_api.py` analyze tests were red before A1; their state after A1 was not read one by one.

**First step.** fix A1 to A3, rerun the command in AGENTS.md, write the new baseline into this ticket.

#### A5. Find how the half-wired tracing change reached main

`Q` `agent` `P2`

**Evidence.** branch `claude/add-data-tracing-kB8Nr` exists on GitHub. CI runs only `tests/api` (C1), which may be why a broken `core` change passed. The PR or commit that added the calls was not read.

**First step.** `git log -S"get_tracer" -- src/waft/core`, read the PR, note whether any test ran. Feed the answer to C1.

#### A6. Add the CliRunner import to tests/test_commands.py

`M` `agent` `P2`

**Evidence.** line 11 is `runner = CliRunner()`; the imports above it do not include `typer.testing.CliRunner`. The file fails at collection with NameError and stops a plain `pytest tests/` run.

**First step.** add the import, then see how many of that file's tests pass.

#### A7. Decide the fate of the three test files that fail at collection

`R` `agent` `P2`

**Evidence.** AGENTS.md says `test_foundation.py`, `test_full_system.py` and `test_the_absolute_begeesus.py` have module-level code that fails and must be passed to `--ignore`. I did not run them.

**First step.** for each: fix it, turn it into a script under `scripts/`, or move it to `_to_delete/` for CT's approval.

#### A8. Explain the setup error in tests/real_proof_test.py

`M` `agent` `P3`

**Evidence.** `uv run pytest tests/real_proof_test.py` ends with 1 passed and 1 error (`test_real_performance_after_fix`). The error text was not read in full.

**First step.** read it; decide whether this "real proof" still means anything once the tracing is fixed.

#### A9. Make the six PDF-to-PNG tests pass or skip

`M` `agent` `P2`

**Evidence.** `tests/test_pdf_image_converter.py` (6 tests) fails with `RuntimeError: No PDF conversion library available`. It needs pdf2image with poppler, ImageMagick or PyMuPDF; none is installed here and `pymupdf` is not in `pyproject.toml`.

**First step.** add `pymupdf` as an extra and use `pytest.importorskip`, or declare the system packages in the setup script.

#### A10. Stop tests from writing trace files into the tracked tree

`M` `agent` `P2`

**Evidence.** `TraceStorage` defaults to `Path.cwd() / "_pyrite" / "analytics" / "traces"` (`core/tracing/storage.py:25`). Each test run created or changed `_pyrite/analytics/traces/2026-11-14.jsonl`, a tracked path. Commit 4ad0eee1 on this branch contains that file because a stop hook asked for untracked files to be committed.

**First step.** point storage at a tmp dir in `tests/conftest.py`, offer an env var for the trace dir, and untrack the file (D8).

#### A11. Find why uv rewrites uv.lock on every run

`M` `agent` `P2`

**Evidence.** after `uv sync` and after several `uv run` calls, `git status` showed `M uv.lock` each time; I reverted it each time. Suspects: the local `empirica` path source (B4) or a lock that is out of date. The diff was not read.

**First step.** `git diff uv.lock` after one run; commit a lock that stays stable.

#### A12. Clear the deprecation warnings

`M` `agent` `P3`

**Evidence.** 151 warnings in the baseline run and 185 after the import patch. Sources: `datetime.utcnow()` at `tracer.py:32` and `storage.py:45`; Pydantic v2 `max_items` and class-based `Config` in `api/schemas/work_efforts.py` (lines 10, 16, 29, 35, 48, 54, 60, 89) and `api/schemas/projects.py`; `api/responses.py:10`.

**First step.** use timezone-aware datetimes, `max_length` and `ConfigDict`, then run with `-W error::DeprecationWarning` in CI.

#### A13. Find out whether the root-level suites in tests/ are run anywhere

`R` `agent` `P3`

**Evidence.** pytest's default file pattern skips `mega_test_suite.py`, `hellfire_test_suite.py`, `insane_test_suite.py`, `torture_test_suite.py`, `scientific_test_suite.py`, `adversarial_red_team.py`, `quantitative_benchmarks.py` and the `self_*` files in `tests/`. Whether any script or workflow runs them was not checked.

**First step.** grep for each name in scripts and workflows; run each once; keep the ones that pass and mean something.

#### A14. Add pytest configuration to pyproject.toml

`M` `agent` `P2`

**Evidence.** there is no `[tool.pytest.ini_options]`. AGENTS.md says a bare `pytest` collects broken files and can end in an INTERNALERROR (from `narcissus_lab/internal_monologue`). The full run takes about 80 s (78.9 s and 85.3 s measured).

**First step.** set `testpaths = ["tests"]`, register markers (`slow`, `needs_pdf_lib`, `network`), set a default timeout, and make `uv run pytest` safe with no arguments.

#### A15. Measure coverage over all of src

`Q` `agent` `P3`

**Evidence.** the only coverage command in the repo is in the staging workflow and, because only `tests/api` runs there, covers little. `src/waft` has 516 Python files and about 174,000 lines.

**First step.** `uv run pytest --cov=src --cov-report=term-missing` on the fixed baseline; list modules at 0 percent; they are dead-code candidates (F7).

#### A16. Review the 23 skips, 8 xfails and the 1 xpass

`M` `agent` `P3`

**Evidence.** the baseline run ends with `23 skipped, 8 xfailed, 1 xpassed`. The reasons were not read.

**First step.** `pytest -rsx` to print each reason; remove the xfail marker on the xpass; turn long-term skips into tickets.

#### A17. Run the suite on Python 3.12 and 3.13

`M` `agent` `P2`

**Evidence.** everything here ran on Python 3.14.3 because uv honours `.python-version`. CI uses 3.12 and `requires-python` is `>=3.12`.

**First step.** `uv run --python 3.12 pytest ...` and 3.13; fix the failures or narrow the supported range.

#### A18. Fix the 31 undefined names that ruff finds

`M` `agent` `P1`

**Evidence.** `ruff check src --isolated --select F821` reports 31 undefined names. Besides the five tracing hits (A1, A3): `main.py` lines 3101 to 3128 use `project_path` six times; `pdf.py:861` and `:891` use `os`; `web.py:498` and `:528` call `_notify_clients`; `being.py:1028` uses `dnd_stats`; `cli/pyrite_cli.py:121` and `:194` call `get_pyrite_instance`; `ui/streamlit/being_integration.py:197` uses `project_path`; and `Being`, `Mission`, `ArrowOfIntent`, `BaseAgent`, `StoryState`, `Event` appear in 12 more places (some may be annotation-only).

**First step.** read each site and separate real NameErrors from annotations; fix; then turn the rule on in CI (C10).


### B. Packaging, install and Docker

This section holds the biggest single finding: a wheel built from this checkout cannot start the CLI.

#### B1. Fix the package list: the wheel holds 202 of 516 Python files

`M` `agent` `P1`

**Evidence.** `[tool.setuptools] packages` is a hand-written list of six names (`waft`, `waft.core`, `waft.cli`, `waft.templates`, `waft.ui`, `waft.api`). `uv build --wheel` made a wheel with 202 `.py` files; `find src/waft -name '*.py'` finds 516. Missing: 13 top-level subpackages (`ai_town`, `campaign`, `config`, `dealer`, `evolution`, `fogsift`, `pantheon`, `pet`, `prime_directive`, `rag`, `reports`, `scripts`, `version`) and nested ones inside the listed packages, for example `core/tracing`, `core/agent`, `core/science`, `api/routes` and `ui/streamlit` (each checked absent from the wheel).

**First step.** switch to `[tool.setuptools.packages.find] where = ["src"]`, rebuild, compare file counts, rerun B2.

#### B2. Make a wheel install start: waft --help fails today

`M` `agent` `P1`

**Evidence.** I built the wheel with `uv build --wheel`, installed it in a clean Python 3.14 venv, and ran `waft --help`. It stops with `ModuleNotFoundError: No module named 'waft.templates.typst'` (`main.py:37` imports `cli/case_render.py`, which imports `..templates.typst.compiler` at line 15). `waft new` and `waft evolve` fail the same way. The README tells users to install from GitHub, which builds a wheel the same way; I did not run that exact command.

**First step.** fix B1, reinstall in a clean venv, run `--help` for each of the 82 commands, and add that as a CI job (C7).

#### B3. Ship template data files in the wheel

`M` `agent` `P2`

**Evidence.** the built wheel has 0 non-Python files under `waft/`; `src/waft/templates` has 14 non-Python files in the tree. `pyproject.toml` has no `package-data`, `include-package-data` or `MANIFEST.in`.

**First step.** declare the data, rebuild, and test `waft new` from the wheel.

#### B4. Make the empirica dependency installable with one command

`R` `agent` `P1`

**Evidence.** `pyproject.toml` points `empirica` at the gitignored path `_unified/empirica` (editable), so a fresh `uv sync` cannot find it. AGENTS.md's recipe hardcodes `/workspace/_unified/empirica`. Here I fetched empirica 1.2.3 with `pip3 download --no-binary :all: --no-deps`, extracted it, and copied it to `_unified/empirica`. The sibling `_pyrite` repo has the same trap (`../empirica` and `../NovaSystem-Codex`); its `uv sync` failed here.

**First step.** add `scripts/setup-empirica.sh`, or drop the source override so uv resolves PyPI. Apply the same fix in `_pyrite`.

#### B5. Test WAFT against current Empirica

`M` `research` `P2`

**Evidence.** WAFT requires `empirica>=1.2.3` and ran here against 1.2.3 (local). A clean venv resolved `empirica` 1.16.3 from PyPI on 2026-11-14; FogSift FINDINGS recorded 1.14.14 on 2026-10-25 and a fork at 1.12.33. `src/waft/core/empirica.py` is 1,001 lines, and the `waft empirica`, `finding`, `unknown`, `goal` and `session` commands depend on it.

**First step.** in a throwaway venv with 1.16.3, run the `test_empirica_*.py` files and the Empirica commands; list API breaks; pin a tested range.

#### B6. Split heavy dependencies into extras

`R` `agent` `P3`

**Evidence.** core dependencies include `streamlit`, `weasyprint` (needs cairo and pango), `fpdf2`, `pypdf`, `playingcards.py`, `d20`, `tinydb`, `markdown` and `beautifulsoup4`. A user who only wants `waft new` installs all of them.

**First step.** measure install size and time; define extras `pdf`, `ui`, `games`; make the imports lazy.

#### B7. Align the Python version settings

`M` `agent` `P3`

**Evidence.** `.python-version` says 3.14.3; CI uses 3.12; `requires-python` is `>=3.12`; classifiers list only 3.12; ruff `target-version` is `py310`; `__pycache__` folders from Python 3.14 sit in the tree.

**First step.** choose a supported range, set all five to it, test both ends (A17).

#### B8. Decide the package name

`R` `CT` `P2`

**Evidence.** README commit e9bb643a says `uv tool install waft` installs an unrelated PyPI package (a music tagging app, version 0.1.9). The README now installs from GitHub.

**First step.** choose: rename, claim a distinct PyPI name, or stay git-only and say so.

#### B9. Define a release procedure and tag it

`M` `agent` `P3`

**Evidence.** `git tag` lists 0 tags. `pyproject.toml` says 0.10.0; `CHANGELOG.md` has an `[Unreleased]` section (the staging workflow warns about it); `src/waft/version/` exists and was not read.

**First step.** write the steps (bump, changelog, tag, build, publish or release asset); check the three version sources agree; tag at the right commit.

#### B10. Build and run the Dockerfile

`R` `agent` `P2`

**Evidence.** the Dockerfile installs with `pip install .` (ignoring `uv.lock`) and starts `uvicorn src.waft.api.main:app`, a source-tree path that bypasses the installed package. No Docker here, so it was never built. Given B1, the installed wheel is broken, so the container may work only because it imports from the copied `src/`.

**First step.** build it in CI; choose one run path; pin the base image; add a health check (`/api/decision/health` exists).

#### B11. Test on macOS and Windows

`Q` `research` `P3`

**Evidence.** scripts use bash (`START_EVOLVE_UI.sh`, `scripts/dev-reinstall.sh`), 433 tracked files hold `/Users/ctavolazzi`, and the FogSift reports say nothing has run on macOS. Only Linux was tested here.

**First step.** add a macOS job to CI; list the failures.


### C. CI and release

#### C1. Run the whole test suite in CI

`R` `agent` `P1`

**Evidence.** `.github/workflows/branch-protection.yml` runs `uv run pytest tests/api` and a lint job. `tests/api` holds about 41 test functions (static count of `def test_`) against 573 outcomes in the baseline run, so CI exercises roughly 7 percent of the suite. The last four runs on `main` (runs 181 to 184, 2026-11-09) are green while 25 tests fail locally.

**First step.** run `pytest tests/` with the known-bad files deselected by name; shrink the list as A1 to A9 land.

#### C2. Find out whether the staging gate can ever run

`R` `agent` `P2`

**Evidence.** `staging-promotion.yml` has a `head:` key under `pull_request` (not a documented filter) and an `if` on `github.head_ref == 'staging'`. The one PR run recorded (run 70, 2026-07-26) concluded `skipped`. The first page of the branch list (50 names) has no `staging` branch; later pages were not read.

**First step.** list all branches; if there is no staging branch, delete the workflow or create the branch; test with a dummy PR.

#### C3. Remove the debug blocks the staging gate greps for

`M` `agent` `P2`

**Evidence.** the gate fails if `src/` contains `# #region agent log` or `debug.log`. Five Python files do: `web.py`, `document_builder.py`, `one_pager.py`, `evolution/document_components.py`, `evolution/golden_triangle.py`.

**First step.** delete the blocks (E5); keep the gate.

#### C4. Triage the remote branches, the open PR and the open issue

`R` `CT` `P2`

**Evidence.** the first page of the GitHub branch list has 50 names: 42 `claude/*`, 3 `cursor/*`, `dev`, `backup/main-20260119-224436`, `chore/pr21-refresh-ci`, `chore/untrack-secrets` and `2026-01-11-updates`; more may exist. One open PR (#23, `cursor/development-environment-setup-88d5`, opened 2026-03-14) and one open issue (#15, "Placeholder").

**First step.** for each branch: merged into main? unique commits? Then CT decides keep, tag or delete. Nothing is deleted without CT.

#### C5. Add dependency update automation

`M` `agent` `P3`

**Evidence.** `.github/` holds `ISSUE_TEMPLATE`, `JOURNAL.md`, `PULL_REQUEST_TEMPLATE.md`, `wiki` and `workflows`; there is no `dependabot.yml`.

**First step.** add Dependabot for pip, npm (the front ends you keep) and GitHub Actions.

#### C6. Add secret and vulnerability scanning to CI

`Q` `agent` `P2`

**Evidence.** no workflow runs gitleaks, pip-audit, npm audit or CodeQL.

**First step.** add gitleaks (pinned), `pip-audit` on the lock, and `npm audit` for the front ends you keep.

#### C7. Build and smoke-test the artifacts in CI

`Q` `agent` `P2`

**Evidence.** nothing in CI builds the wheel (B1), the image (B10), `visualizer/` or `waft_desktop/`.

**First step.** add a job per artifact you keep: build, install in a clean env, run `--help`; remove artifacts nobody builds.

#### C8. Pin tool and runner versions in workflows

`R` `agent` `P3`

**Evidence.** `astral-sh/setup-uv@v4` with `version: "latest"` and `runs-on: ubuntu-latest`. The sibling book repo's CI broke when `ubuntu-latest` moved to 26.04 (`_workbench/sessions/LOG.md`, 2026-11-10).

**First step.** pin the runner image and the uv version.

#### C9. Measure CI health over the last 100 runs

`R` `agent` `P3`

**Evidence.** GitHub reports 254 workflow runs. Pass rate, median duration and flaky jobs were not analysed.

**First step.** pull the runs, compute the numbers, add them to the weekly health log (L7).

#### C10. Turn on ruff F821 for all of src in CI

`M` `agent` `P1`

**Evidence.** the project's ruff config excludes most legacy folders and passes cleanly, yet `--isolated --select F821` finds the missing `get_tracer` and `SpanStatus` names that broke tests, plus 26 more (A18). One cheap rule would have stopped the tracing break.

**First step.** add a CI step `ruff check src --select F821`; fix or baseline the hits.


### D. Repository size and hygiene

#### D1. Untrack the 9,015 node_modules files

`M` `agent` `P1`

**Evidence.** `git ls-files | grep -c node_modules` gives 9,015: `waft_desktop/electron` 5,065, `typst-webapp/frontend` 1,916, `waft_desktop/frontend` 1,486, `games/teleport_massive_adventure` 548. The root `.gitignore` ignores only `visualizer/node_modules`. 279 `.map` files are tracked as well.

**First step.** `git rm -r --cached` those folders, add `node_modules/` to `.gitignore`, keep lockfiles, confirm each app still installs.

#### D2. Decide where generated PDFs live

`M` `CT` `P2`

**Evidence.** 3,082 tracked PDFs: `waft_pdf_library` 2,042, `_work_efforts` 551, `_archive` 139, `typst-demos` 70, `_temp_pdf_examples` 60, `_genetics` 31.

**First step.** mark each folder input or output; outputs go to release assets or get regenerated on demand; keep fixtures small.

#### D3. Decide what to do about the largest tracked files

`M` `CT` `P2`

**Evidence.** top files by size: `mediawiki-1.45.1.zip` 93.7 MiB; `examples/908530342-Building-AI-Agents-With-LLMs-RAG-And-Knowledge-Graphs-1.pdf` 90.8 MiB; `templates/1789_USA_Miller_Woods_TrailA_Visitors_Guide.pdf` 67.2 MiB; `PITCH_DECK/Waft__Breeding_AI_s_Future_.mp4` 39.3 MiB; three PDFs of 38 to 39 MiB in `_work_efforts/WE-260119-ejtx...`; a 31.1 MiB `.m4a` in `PITCH_DECK`. The `.git` pack is 687 MiB, and the 12 largest top-level folders of tracked files sum to about 1,400 MiB.

**First step.** options: Git LFS, release assets, a data repo, or history filtering (D12). Add a size check to CI (D11).

#### D4. Check the rights to third-party files in a public MIT repo

`R` `CT` `P1`

**Evidence.** tracked files include a book PDF ("Building AI Agents With LLMs, RAG, And Knowledge Graphs"), the GPT-4 Technical Report, several arXiv papers, a park visitor guide, a MediaWiki release (GPL) and `Latex Source Code.zip`. The licence of each is unknown. `CREDITS.md` was not read.

**First step.** list every third-party file with source and licence; remove or replace with links where rights are unclear. This protects CT's credibility rule.

#### D5. Resolve the eight uninitialized submodules

`M` `agent` `P2`

**Evidence.** `.gitmodules` lists 8; `git submodule status` shows all 8 with a leading `-` (not checked out). Commit 2836a19b removed 29 orphan submodules earlier.

**First step.** for each: is anything imported or read at runtime? Then init, vendor with a licence note, or remove from `.gitmodules`.

#### D6. Design the target layout for the repo root

`R` `agent` `P2`

**Evidence.** the root held 350 files before the 2026-11-09 archive and 197 after (commit 6419b7c0); `ls` still shows PDFs, zips, scripts, `Bubbles`, `Campaigns`, `NARRATIVE-WAFT`, `PITCH_DECK` and `Obsidian_Archive`.

**First step.** classify each root entry (code, docs, data, art, archive), propose `src/ docs/ examples/ assets/ archive/`, move with `git mv`.

#### D7. Untrack tool state

`M` `agent` `P2`

**Evidence.** tracked: `.cursor` 171 files, `.empirica` 12, `.empirica_reflex_logs` 12 (named in `.gitignore` but tracked earlier), `.playwright-mcp` 3, `.obsidian` 5, `.waft` 1. The sibling book repo had the same Empirica problem (FogSift FINDINGS item 2).

**First step.** read the contents for sensitive reasoning or paths; `git rm --cached`; extend `.gitignore`.

#### D8. Move runtime data out of git

`M` `agent` `P2`

**Evidence.** 4 tracked `.db` or `.sqlite` files (for example `_pyrite/analytics/sessions.db`) and 162 tracked `.jsonl` files (traces, journals).

**First step.** inspect for personal paths; split fixtures from runtime data; ignore the runtime paths (A10).

#### D9. Remove hardcoded /Users/ctavolazzi paths

`M` `agent` `P2`

**Evidence.** `git grep -I -l '/Users/ctavolazzi'` outside `node_modules` finds 433 files; `src` has 30 lines in 6 Python files (for example `web.py:28` writes a debug log there).

**First step.** replace with config or `Path(__file__)`-relative paths in `src`; leave historical docs.

#### D10. Spin parked projects out of the lab repo

`R` `CT` `P2`

**Evidence.** several products live here: `waft_desktop` (Electron, about 203 MiB tracked), `typst-webapp`, `games/`, `_realms/`, `PITCH_DECK`, `succulent_jewelry_pdfs`, `Bubbles`, `Campaigns`, `NARRATIVE-WAFT`.

**First step.** for each: keep, move to its own repo, or archive on a branch. Do it after D1.

#### D11. Set a size budget

`M` `agent` `P3`

**Evidence.** the working tree is 2.9 GB with `.venv`; biggest directories on disk: `waft_pdf_library` 307 MB, `_work_efforts` 276 MB, `waft_desktop` 226 MB, `templates` 143 MB, `examples` 106 MB.

**First step.** a CI check on total tracked size and on any new file over 5 MiB.

#### D12. Decide whether to rewrite history

`R` `CT` `P2`

**Evidence.** old commits still hold the Pexels and Pixabay keys and the API token (rotated 2026-11-09 per commit 67ce2ed8) and the two crypto keys (E1). `_workbench` ticket 8.4 says leave history. A rewrite would also shrink the 687 MiB pack but breaks every clone and open branch.

**First step.** CT decides; if yes, plan `git filter-repo` with a backup and a branch freeze.


### E. Security

#### E1. Rotate or retire the two crypto keys that are still public in history

`R` `CT` `P1`

**Evidence.** `_pyrite/.waft/.pyrite_secret_key` (a Fernet key) and the D&D realm `.hmac_key` were tracked in this public repo; untracked by commits 67ce2ed8 and 3f8cb670. Commit 67ce2ed8 says the Pexels key, the Pixabay key and the API token were rotated; it does not say the Fernet key was. Commit dd1992fd says both crypto keys must be kept locally because deleting them orphans encrypted secrets and invalidates realm state. So both values stay public and valid.

**First step.** inventory what is encrypted or signed with each; rotate with a re-encrypt or re-sign migration; generate on demand afterwards.

#### E2. Review API authentication

`R` `agent` `P2`

**Evidence.** the bearer token comes from `get_or_create_token()` in `src/waft/api/auth.py` and is stored in `.waft_api_token`. Comparison method, token scope, which routes require it and rotation were not reviewed.

**First step.** read `auth.py` and every router; list routes by auth requirement; add tests for 401 and 403.

#### E3. Review CORS settings

`M` `agent` `P2`

**Evidence.** `src/waft/api/main.py:120` sets `allow_origins`; `tests/test_cors.py::test_actual_post_request_with_cors` returns 500 (A1 does not fix it).

**First step.** read the origin list; confirm no wildcard with credentials; fix the 500.

#### E4. Audit shell and subprocess calls

`M` `agent` `P1`

**Evidence.** `src` has 241 `subprocess.` references, 14 `shell=True` and 4 `os.system`. No `eval(`, `exec(`, `pickle.load` or `yaml.load(` hits. Where the arguments come from was not read.

**First step.** list the 18 sites; for each: argument source (CLI, API, document text); replace with list arguments or `shlex.quote`.

#### E5. Remove leftover agent logging blocks

`M` `agent` `P2`

**Evidence.** five Python files contain `# #region agent log` (`web.py`, `document_builder.py`, `one_pager.py`, `evolution/document_components.py`, `evolution/golden_triangle.py`); `web.py:26` onward appends to `/Users/ctavolazzi/Code/active/waft/.cursor/debug.log`.

**First step.** delete the blocks; run the staging gate's grep locally.

#### E6. Scan the full history for secrets

`Q` `agent` `P2`

**Evidence.** my scan of the current tree used five patterns (`sk-`, `ghp_`, `AKIA`, `AIza`, `xox`) and found nothing; that is a weak test. The history (687 MiB pack) and the vendored `node_modules` were not scanned.

**First step.** run gitleaks and trufflehog over all refs; classify hits as live, rotated or fixture.

#### E7. Audit dependencies for known vulnerabilities

`Q` `agent` `P2`

**Evidence.** no audit has run. The Python side is pinned by `uv.lock`; the JavaScript side has lockfiles inside tracked `node_modules` trees.

**First step.** `pip-audit` on the lock; `npm audit` in `waft_desktop/electron`, `waft_desktop/frontend`, `typst-webapp/frontend` and `visualizer`; record the Electron version.

#### E8. Review the Electron app's security settings

`Q` `research` `P3`

**Evidence.** `waft_desktop/electron` exists; `nodeIntegration`, `contextIsolation`, preload scripts and IPC exposure were not read.

**First step.** read the main-process config against Electron's security checklist.

#### E9. Test that PDF redaction removes the text

`Q` `agent` `P2`

**Evidence.** `src/waft/redactor.py` and `src/waft/pdf_redactor.py` exist. Whether redacted text can still be extracted was not tested.

**First step.** redact a sample PDF, extract text with two tools, fail the test if the text survives.

#### E10. Test the API and CLI for path traversal

`Q` `agent` `P2`

**Evidence.** routes in `work_efforts` and `projects`, and the CLI, accept a project path and write files. `../` and absolute paths outside the project were not tried.

**First step.** add tests that send such paths and expect 400 or 403.

#### E11. Define the sandbox for self-modifying code

`Q` `research` `P2`

**Evidence.** WAFT is described as self-modifying. Where generated code runs, with what rights, and what limits file and network access is not documented in anything read.

**First step.** document the execution model; add a test that a mutation cannot write outside its working directory. See R3.

#### E12. Decide what the realm HMAC protects

`R` `CT` `P3`

**Evidence.** now that `.hmac_key` is out of git it is generated per machine (commit dd1992fd message), so crystallized realm state made on one machine will not verify on another.

**First step.** state the intended trust model: one machine, shared, or signed by an owner key.


### F. Architecture and code quality

#### F1. Split main.py into command modules

`M` `agent` `P2`

**Evidence.** `src/waft/main.py` is 4,918 lines and registers 82 top-level commands (`waft --help`); `src/waft/cli/` already holds 16 modules. `src/waft` totals about 174,000 lines in 516 files.

**First step.** move command groups into `cli/`, keep `main.py` as wiring, do it behind the existing tests.

#### F2. Fix variant identity in waft evolve

`M` `agent` `P1`

**Evidence.** `waft evolve --generations 2 --variants 3` printed one id three times (`being_20261114_153322_37e1e692`), then `fitness=100.00, scints=0` for each, "Fitness improvement: +0.00" and a total time of 0.01 s. With identical variants and a saturated score, selection chooses between copies. FogSift gap #44 records the same id defect.

**First step.** read the spawn code in `core/evolution_engine.py`; make ids unique; add a test that N variants have N ids; see F3.

#### F3. Find out what "evolution" operates on

`R` `research` `P1`

**Evidence.** `core/evolution_engine.py` imports `hashlib`, `random` and `json`; model-provider names appear in few files (anthropic 2, openai 3, ollama 5, gemini 3 files). The fitness measure is "Scint detection". Nothing read shows a model being called by `evolve`.

**First step.** write one page: genome fields, mutation operators, fitness function, what a Being does. If no model runs, say so in the README.

#### F4. Resolve the overlapping names pyrite, empirica and fogsift

`M` `CT` `P2`

**Evidence.** `src/waft/pyrite.py` ("The Steward", 1,139 lines, singleton, locks, "genetic algorithms") shares a name with the separate `_pyrite` toolkit; `src/waft/core/empirica.py` (1,001 lines) sits beside the `empirica` package; `src/waft/fogsift/` sits beside the FogSift system.

**First step.** rename or document each boundary; avoid two different things called pyrite.

#### F5. Move demos and generators out of the package root

`M` `agent` `P3`

**Evidence.** about 40 modules sit directly in `src/waft/`, including `demo_api.py`, `demo_confidence.py`, `demo_stochastic.py`, `demo_anti_dogfooding.py`, `final_demo.py`, `generate_artifacts.py`, `generate_lightcone_docs.py` and `generate_lightcone_docs_weasyprint.py`.

**First step.** move to `examples/` and `scripts/`; fix imports.

#### F6. Remove versioned duplicates

`M` `agent` `P3`

**Evidence.** `foundation.py` and `foundation_v2.py`; `karma.py`, `karma_system.py`, `karma_market.py`, `karma_collector.py`; two `generate_lightcone_docs` variants.

**First step.** build an import graph; delete or archive what nothing imports (with CT's approval).

#### F7. Run dead-code detection

`Q` `agent` `P3`

**Evidence.** not run.

**First step.** `vulture src` and repowise (pinned in FogSift); compare with the zero-coverage list (A15).

#### F8. Check layering and import cycles

`Q` `agent` `P3`

**Evidence.** not run.

**First step.** `import-linter` or `pydeps`; set rules such as "core must not import api or ui".

#### F9. Shrink the ruff exclusion list

`M` `agent` `P2`

**Evidence.** ruff reports nothing with the project's config, which excludes `src/gym`, root `*.py` and many underscore folders. `ruff check src --isolated --line-length 100` (default rules) reports 268 findings, 128 auto-fixable: F401 unused import 99, F541 55, F821 undefined name 31, E722 bare except 21, E402 19, F841 14, E741 12, E701 11, F811 4, E731 2.

**First step.** remove one exclusion at a time, fix, commit; start with F821 (A18, C10).

#### F10. Measure type-check errors

`Q` `agent` `P3`

**Evidence.** no mypy or pyright configuration exists.

**First step.** run pyright on `src/waft/core` and `src/waft/api`; set a ratchet so the count never rises.

#### F11. Review global singletons

`R` `agent` `P3`

**Evidence.** `_global_tracer` in `core/tracing/__init__.py`; the `Pyrite` singleton in `pyrite.py`.

**First step.** check thread and async safety; let tests build their own instances.

#### F12. Inventory the data stores

`R` `research` `P3`

**Evidence.** TinyDB, SQLite (`sessions.db`), JSON and JSONL files, `pocketbase_scout.py` (1,246 lines), the flight recorder and journals.

**First step.** one table: store, owner module, location, format, backup; pick a standard.

#### F13. Choose which front ends to keep

`M` `CT` `P2`

**Evidence.** seven exist: the FastAPI app (`waft serve`), the `dashboard` and `dashboard-5050` commands, the observatory (`core/observatory/server.py`, 1,390 lines), Streamlit (`ui/streamlit`), the SvelteKit `visualizer/`, the Electron `waft_desktop/`, and `typst-webapp/`.

**First step.** for each: last used, who uses it, build status; keep one or two.

#### F14. Find why a first quickstart run changed tracked files in the checkout

`M` `agent` `P1`

**Evidence.** my first run of `waft new demo`, `waft verify` and `waft evolve --generations 2 --variants 3` (cwd a scratch directory, started with `uv run --project /home/user/waft`) left four tracked files modified in `/home/user/waft`: `_pantheon/the_dealer/memory.jsonl`, `state.json`, `truth/keys.json` and `seals/gate_02_the_marker.pdf`. Two reruns did not reproduce it. `verify` rolls dice ("CON Check ... failure"), so the outcome may depend on a random roll. Relative paths `Path("_pantheon/the_dealer")` appear at `main.py:1064` and `core/dealer_journal.py:16`. I reverted the files.

**First step.** run each command 20 times with a fixed seed while watching `git status` in the source checkout; find the write.

#### F15. Centralize configuration

`R` `agent` `P3`

**Evidence.** ports and paths are spread through the code: 5050 (dashboard), 2077 (observatory), 8000 (Docker), 8080 (README `waft serve`).

**First step.** one settings module with env overrides; document it in the README.

#### F16. Pin down the API error contract

`M` `agent` `P2`

**Evidence.** `tests/test_api.py::test_analyze_endpoint_missing_scores` expects HTTP 400 with the text "Missing score" under the `message` key; the app returns 500 today (cause: A1 to A3).

**First step.** after A1 to A3 confirm 400; export the OpenAPI schema and add a snapshot test.

#### F17. Pick one observability story

`R` `research` `P3`

**Evidence.** separate mechanisms exist: `logging.py`, tracing (`_pyrite/analytics/traces`), the flight recorder (`_pyrite/flight_recorder`), journals, and the debug file in E5.

**First step.** choose one path for logs and one for traces; remove the rest.


### G. Documentation against reality

#### G1. Make one index for the 3,680 Markdown files

`M` `agent` `P2`

**Evidence.** `git ls-files '*.md'` minus `node_modules` gives 3,680 files. Nothing says which are current. `docs/` is 3.8 MB and `_work_efforts` is 276 MB on disk.

**First step.** write `docs/INDEX.md` (current, historical, generated); archive the rest with a README, as `_archive/root-2026-11-09/` does.

#### G2. Fix docs that name commands the CLI does not have

`M` `agent` `P1`

**Evidence.** `waft --help` lists 82 commands. A scan of `README.md` and `docs/*.md` for `waft <word>` found words with no command, among them `spawn`, `eval`, `lineage`, `select`, `import`, `scenario`, `personnel`, `agent`, `version`, `test`, `decision-compare`, `decision-export`, `decision-history`, `decision-show`, `oracle-personality` and `create`, in at least 18 docs (for example `docs/FAQ.md`, `GETTING_STARTED.md`, `SYSTEM_OVERVIEW.md`, `TROUBLESHOOTING.md` and four `FOGSIFT_WAFT_SEED_PROMPT*` files). A few hits are prose ("waft itself").

**First step.** commit the scan as `scripts/check_docs_commands.py`, fix or archive each doc, add it to CI. This is `_workbench` ticket 10.9, which is blocked.

#### G3. Build a claims table

`R` `research` `P1`

**Evidence.** README and `PITCH_DECK` use phrases such as "Don't just build agents. Breed them." and "God-Head". FogSift FINDINGS (2026-10-25) says the term appears only in documentation and nothing in `src/` or `tests/` measures it.

**First step.** one table: claim, where it is made, the command or test that shows it, the measured result, status.

#### G4. Add a CLAUDE.md for this repo

`R` `agent` `P2`

**Evidence.** AGENTS.md is "Cursor Cloud specific" and its empirica recipe uses `/workspace`. Sibling repos have a CLAUDE.md.

**First step.** a short CLAUDE.md: read order, rules (no em or en dashes, nothing deleted without CT, work efforts), the setup commands that worked here.

#### G5. Date and triage the root status documents

`R` `agent` `P3`

**Evidence.** the root holds `CONTINUATION_PROMPT.md` (dated 2026-01-19), `COMPLETE.md`, `PR_SUMMARY.md`, `VERIFICATION_REPORT.md`, `REFACTORING_PLAN.md`, `RELEASE_NOTES.md` and `DEMO_CHECKLIST.md`.

**First step.** for each: current, historical or wrong; update or move.

#### G6. Write a one-page STATE.md for WAFT

`R` `agent` `P2`

**Evidence.** `_workbench/STATE.md` is the model: where things stand, next moves, open questions.

**First step.** draft it from the baseline in this document; refresh it at the end of every session.

#### G7. Place WAFT in the business priorities

`M` `CT` `P1`

**Evidence.** `grep -i waft` finds nothing in `_workbench/STATE.md` or `_workbench/OPERATING.md`. STATE.md puts the book release first (Nov 26).

**First step.** CT decides active, parked or sunset, and writes it in STATE.md.

#### G8. Check whether the verify score on a fresh project is a false alarm

`M` `agent` `P3`

**Evidence.** after `waft new demo`, `waft verify` reports "Project structure has issues" and "Integrity: 90%" because `uv.lock` is missing.

**First step.** make `new` run `uv lock`, or make `verify` treat a missing lock as a hint.

#### G9. Turn the README quickstart into a test

`M` `agent` `P3`

**Evidence.** `waft new`, `waft verify` and `waft evolve` ran end to end here from a scratch directory (see F2, G8, F14 for what they showed).

**First step.** a CI job that runs the quickstart in a temp directory and fails on a non-zero exit.

#### G10. Check links and file references in docs

`Q` `agent` `P3`

**Evidence.** the PDF error message points at `docs/PDF_PNG_CONVERSION.md`; its existence was not checked.

**First step.** run a link checker over the Markdown; add it to CI.

#### G11. Decide the fate of the field-manual landing page

`R` `CT` `P3`

**Evidence.** commit 9c4bcf8d on branch `dev` (2026-07-24): "add WAFT field-manual landing page", a self-contained interactive page. It is on `dev`, not `main`.

**First step.** publish it (where?) or archive it; its claims must match G3.


### H. What WAFT is for

These need CT. Nothing here is a code task.

#### H1. Write the one-sentence purpose

`R` `CT` `P1`

**Evidence.** the repo is at once a project scaffolder (`waft new`), an agent-evolution lab (`evolve`), a work-effort tracker, a document and PDF generator, a D&D and card-game universe, a Discord bot spec and several dashboards.

**First step.** CT picks one core; everything else moves out (D10) or is labelled experimental.

#### H2. Decide what moves to FogSift/waft

`R` `CT` `P2`

**Evidence.** README says the repo may migrate toward FogSift/waft; FogSift FINDINGS says the org copy is a 7-file snapshot from 2026-03-03.

**First step.** list the paths that would move; do it after D1 to D5 and E1.

#### H3. Name the audience

`R` `CT` `P2`

**Evidence.** FogSift FINDINGS decision 1: SimpleAgentOS is CT's daily harness. No document read names WAFT's users.

**First step.** write the one reader this is for: CT only, FogSift users, or outside developers.

#### H4. Keep the repo public or private while D4 and E1 are open

`Q` `CT` `P2`

**Evidence.** the repo is public; D4 and E1 describe unresolved exposure.

**First step.** decide; making it private is reversible.

#### H5. Choose a licence deliberately

`R` `CT` `P3`

**Evidence.** LICENSE is MIT; the third-party files inside (D4) carry their own terms.

**First step.** after D4, confirm MIT covers only original work and say so.

#### H6. Decide whether WAFT becomes video content

`R` `CT` `P3`

**Evidence.** `PITCH_DECK/` holds an mp4 and an m4a ("Breeding a God-Head With Self-Mutating Code"). CT's rule: facts are measured and sourced.

**First step.** only after F2 and F3 give a real, measured result; script the run so the video shows a recording, not a claim.

#### H7. Decide how WAFT could earn or save money

`Q` `CT` `P3`

**Evidence.** the `_workbench` goal is money to upgrade production and reinvest in videos, the book and Johnny Autoseed. No WAFT revenue path is written in anything read.

**First step.** list candidates (internal tooling for the businesses, a paid product, content); choose none if none fits.

#### H8. Decide how much time WAFT gets

`R` `CT` `P3`

**Evidence.** no budget is recorded anywhere read; the branch has 85 commits and the repo has 132 work efforts.

**First step.** set a number of hours per week; revisit monthly.

#### H9. Check the name WAFT for collisions

`Q` `research` `P3`

**Evidence.** B8 covers PyPI; other collisions were not searched.

**First step.** search existing projects, trademarks and domains named waft; report.


### I. Fit with _pyrite, Empirica, FogSift and the work-effort ledger

#### I1. Triage the 132 work efforts

`M` `agent` `P1`

**Evidence.** `fogsift.py we list` run in this repo: 132 work efforts: active 69, completed 27, open 16, pending 11, in_progress 1, template 1, and 7 rows it cannot read (front matter does not parse). Dates run from January to March 2026. pyrite's own vocabulary is active, paused, completed.

**First step.** close or pause stale ones with a note; fix the 7 unreadable; map `open` and `pending` onto the vocabulary.

#### I2. Bridge the status vocabulary for SimpleAgentOS

`R` `agent` `P3`

**Evidence.** FogSift FINDINGS, its own item E09 (not this document's E9): SimpleAgentOS lists only `in_progress`, `exploring` and `blocked`, so `active` work efforts do not show in the daily note.

**First step.** add the mapping where the two systems meet; test it with a WAFT work effort.

#### I3. Decide whether to adopt WAFT into the FogSift system

`R` `CT` `P3`

**Evidence.** `adopt` adds a `.gitignore` block, a `CLAUDE.md` section, `hubs/`, `.fogsift.json` and an Empirica project. WAFT has no `.fogsift.json` and no `_work_efforts/hubs/`.

**First step.** after D7 and G4, run `fogsift.py adopt` as a dry run on a scratch clone and read the plan.

#### I4. Decide where WAFT's findings and unknowns survive

`R` `research` `P3`

**Evidence.** Empirica's database is an ignored SQLite file, so data from `waft finding log` and `waft unknown log` does not survive a fresh clone or a cloud session (FogSift FINDINGS).

**First step.** pick a place (hub, log or tracked export) and test with a fresh clone.

#### I5. Check commands that depend on Empirica's threshold message

`R` `agent` `P3`

**Evidence.** FogSift gap #149: Empirica's refusal message names 0.35 while 0.45 is accepted. WAFT has `validate-empirica` and `check-assumptions`.

**First step.** read both commands; see whether they parse or repeat that number.

#### I6. Run repowise doc-drift on this repo

`Q` `agent` `P3`

**Evidence.** FogSift reports that repowise lists a missing path only for file types the repo already holds. It was not run on WAFT.

**First step.** run it; compare with the G2 scan; keep what it finds that the scan misses.

#### I7. Test that waft work-efforts and pyrite we write the same format

`Q` `agent` `P2`

**Evidence.** WAFT has its own `work-efforts` command and API routes; pyrite has `we` and `ticket`. Compatibility was not tested.

**First step.** create with one, list and update with the other; diff the files.

#### I8. Create the daily hub for this work

`Q` `agent` `P3`

**Evidence.** the wagonwheel hub (`fogsift.py hub new`) ties a day's work efforts together; this repo has no `_work_efforts/hubs/`.

**First step.** run `hub new` and `hub sync` once CT agrees to adopt (I3).

#### I9. Close the three recorded FogSift gaps about WAFT and rerun the proof

`R` `agent` `P1`

**Evidence.** FogSift records WAFT gaps #43 and #236 (the get_tracer NameError) and #44 (variant ids). A1 and F2 are those fixes.

**First step.** after A1 to A3 and F2, run `python3 fogsift-system/fogsift.py prove` in `_workbench`; update FINDINGS and the proof run.

#### I10. Connect WAFT's gym score to real repository work

`R` `research` `P1`

**Evidence.** FogSift FINDINGS: "The weakest link is WAFT"; its gym scores a stand-in agent's JSON repair, and nothing shows that predicts repository work.

**First step.** design the experiment in R2: pick 20 real tasks, score with the gym and with real outcomes, compare.


### J. Documents and the PDF pipeline

#### J1. Choose the default PDF engine

`R` `agent` `P2`

**Evidence.** Typst (318 tracked `.typ` files, `typst-webapp`, `typst-demos`), LaTeX (templates, `Latex Source Code`), WeasyPrint and fpdf2 (both core dependencies) and pypdf are all present.

**First step.** render one sample document with each; compare quality, speed and dependencies; pick one default.

#### J2. List the system programs each command needs

`Q` `agent` `P3`

**Evidence.** Typst, a LaTeX distribution, poppler, cairo and pango are needed by different commands; no check exists.

**First step.** add a `waft doctor`-style check that prints missing programs and which commands need them.

#### J3. Decide whether waft_pdf_library is input or output

`M` `CT` `P3`

**Evidence.** 2,042 tracked PDFs (about 294 MiB). The `rag` module and `_integrations/rag-chatbot` suggest a corpus; `succulent_jewelry_pdfs` suggests output.

**First step.** read the commands that use it; mark each subfolder.

#### J4. Declare the PDF-to-image dependency

`R` `agent` `P3`

**Evidence.** see A9; the error message tells users to install pdf2image or PyMuPDF.

**First step.** one extra, `waft[pdf-images]`.

#### J5. Map the RAG module

`Q` `research` `P3`

**Evidence.** `src/waft/rag` and `waft rag` exist. What it indexes, which embedding model it uses and whether it works offline were not read.

**First step.** one page: inputs, models, storage, commands; run it on three PDFs.

#### J6. Audit the Typst and LaTeX template licences

`Q` `agent` `P3`

**Evidence.** templates come from submodules named for third-party authors (lartpang, xuehai, cinofix, ashad001, flow-way).

**First step.** record each licence next to its template (D4).


### K. Games and lore

#### K1. Decide the home of the Tavern Keeper

`R` `CT` `P2`

**Evidence.** `ctavolazzi/tavern-keeper-bot` (a Discord bot) exists separately; WAFT has `src/waft/core/tavern_keeper` (883 lines in `keeper.py`), `SPEC-TAVERNKEEPER.md` and Tavern Keeper work efforts.

**First step.** pick one source of truth; the other links to it.

#### K2. Move the Teleport Massive material

`R` `CT` `P3`

**Evidence.** `games/teleport_massive_adventure` (548 tracked node_modules files), `_realms/teleport_massive_cardgame`, and large PDFs in `WE-260119-ejtx`.

**First step.** give it its own repo or archive it.

#### K3. Check the D&D content licensing

`Q` `CT` `P3`

**Evidence.** `dnd_toolkit.py`, scenario templates and PDFs. Whether the text comes from the open SRD or from proprietary books was not checked.

**First step.** sample ten files; if proprietary text is present, remove it (D4).

#### K4. Review the wager and karma mechanics before any public release

`Q` `CT` `P3`

**Evidence.** `karma_market.py`, `karmic_wager.py` and `lifetime_exchange.py`. If these ever involve real money or prizes they raise gambling questions. In-game only as far as I read; not confirmed.

**First step.** confirm in-game only; say so in the docs.

#### K5. Decide about the pet device

`Q` `CT` `P3`

**Evidence.** `src/waft/pet` and the active work effort `WE-260201-fspd fogsift_modular_pet_device`.

**First step.** link to a hardware plan or close the work effort.


### L. Process

#### L1. Choose the branch policy

`R` `CT` `P2`

**Evidence.** branches `main` and `dev` (and maybe `staging`); recent history shows direct pushes to `main` with green CI. CT's `_workbench` rule: commits go on branches that then get merged.

**First step.** write the policy; enable branch protection on `main`.

#### L2. Fix the stop-hook conflict

`M` `agent` `P2`

**Evidence.** this session's stop hook asked to commit untracked files, so a generated trace file went into commit 4ad0eee1.

**First step.** either make the hook ignore generated paths, or fix A10 so the file never lands in the repo.

#### L3. Add pre-commit checks

`R` `agent` `P2`

**Evidence.** no `.pre-commit-config.yaml` at the root.

**First step.** ruff, a 5 MiB file guard, gitleaks, a ban on `/Users/` paths, and a ban on em and en dashes in Markdown.

#### L4. Add a Justfile or Makefile

`R` `agent` `P3`

**Evidence.** `waft new` generates a Justfile for new projects; the lab repo itself has none.

**First step.** `setup`, `test`, `lint`, `build`, `quickstart`.

#### L5. Write the start and end of session routine

`R` `agent` `P3`

**Evidence.** `_workbench/CLAUDE.md` has one; WAFT's `CONTINUATION_PROMPT.md` is from January.

**First step.** see G4 and G6; keep it to ten lines.

#### L6. Set a rule for closing work efforts

`R` `agent` `P3`

**Evidence.** 69 work efforts are active, most from January to March (I1).

**First step.** a weekly job lists active work efforts older than 30 days.

#### L7. Schedule a weekly health run

`R` `agent` `P3`

**Evidence.** nothing runs the baseline regularly; the tracing break stayed on `main` unnoticed.

**First step.** a weekly job: full tests, ruff F821, size, secrets scan, docs-command scan; append the numbers to a log.

#### L8. Decide whether agents may merge to main

`Q` `CT` `P3`

**Evidence.** recent commits on `main` were pushed directly (runs 181 to 184).

**First step.** CT's rule: branch first, then merge.


### R. Research for a more capable model

These need reading primary sources or running experiments. Names in R1 come from memory and must be checked before they go into any document.

#### R1. Map the prior art for evolving and self-improving agents

`Q` `research` `P1`

**Evidence.** from memory, unverified: prompt and agent optimization (DSPy, TextGrad, EvoPrompt, Promptbreeder), evolutionary code search (AlphaEvolve and open reimplementations such as OpenEvolve), self-modifying coding agents (Darwin Godel Machine), skill libraries (Voyager), reflection loops (Reflexion, Self-Refine).

**First step.** read each primary source; one table: idea, evidence, difference from WAFT. Verify every name and date before it enters a document.

#### R2. Define fitness for repository work

`Q` `research` `P1`

**Evidence.** the gym scores Scint detection; FogSift found no link to real tasks (I10).

**First step.** candidate measures: tests pass, lint clean, docs match commands (G2), review acceptance, time to green; choose three and test them on 20 tasks.

#### R3. Specify safety for self-modifying agents

`Q` `research` `P2`

**Evidence.** nothing written about sandboxing, rollback or human gates (E11).

**First step.** a threat model and a minimum design: sandbox, diff review, budget limits, kill switch.

#### R4. Measure whether Empirica's gate changes outcomes

`Q` `research` `P2`

**Evidence.** FogSift found the gate advisory only, and one reported "weave gate" behaviour was not reproduced.

**First step.** A/B 20 tasks with and without the check; record outcomes.

#### R5. Test determinism of waft evolve

`Q` `research` `P3`

**Evidence.** FogSift #234 says the lab is deterministic for a seed; `waft evolve` itself reuses ids and saturates at 100 (F2).

**First step.** run twice with a fixed seed and diff; then with different seeds and look at the spread.

#### R6. Write a formal genome spec with property tests

`Q` `research` `P3`

**Evidence.** no schema of what is inherited or mutated was read.

**First step.** a JSON Schema or dataclass spec; property-based tests (hypothesis) for mutation and selection.

#### R7. Plan a public benchmark

`Q` `research` `P3`

**Evidence.** README and `PITCH_DECK` talk about breeding better agents; no benchmark is published.

**First step.** fixed tasks, fixed budgets, seeds, published results; only claims the numbers support.

#### R8. Study how the front ends could become one

`Q` `research` `P3`

**Evidence.** F13 lists seven.

**First step.** list the user stories each serves; build the smallest single view that covers them.

### S. This session (done)

These are the setup steps from the record above, kept as completed tickets so the ledger shows them.

- **S1.** Fetch empirica 1.2.3 into _unified/empirica so uv sync can resolve it.
- **S2.** Run uv sync --extra dev and confirm the waft CLI starts from the checkout.
- **S3.** Measure the baseline: tests, ruff, wheel, CI, branches, sizes, work efforts.

## Caveats

- Linux container only. Python 3.14.3 through uv. No macOS, Windows or Docker.
- Numbers marked `M` come from commands I ran today; they will drift as the repo changes. Rerun the command in the Baseline table before relying on one.
- Items marked `R` repeat what a file, commit message or the GitHub API said. I did not rerun them.
- Library and project names in R1 are from memory and must be checked against their sources before they go into any document.
- Priorities are my judgment.
