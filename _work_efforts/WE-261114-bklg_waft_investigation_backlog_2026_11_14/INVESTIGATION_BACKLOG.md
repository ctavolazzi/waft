# WAFT investigation backlog

**Date:** 2026-11-14  
**Work effort:** `WE-261114-bklg` (tickets use the same ids as this document)  
**Branch:** `claude/environment-setup-3whfys`  
**Status:** draft for review. Nothing in `src/` was changed.

## What this is

A list of 162 things for people (CT) and more capable agents to investigate, decide or expand on, found while setting up the WAFT environment and running the project. Each item has an id (such as `B2`), a tag for how well it is known, who can pick it up, a priority, the evidence, and a first step. The same ids are the ticket titles in this work effort, so a ticket can be claimed and closed without touching this document.

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

Counts: 80 measured, 51 read, 31 questions. Owners: 110 agent, 33 CT, 19 research. Priorities: 34 P1, 62 P2, 66 P3.

## The first twelve (best value for effort)

- **B1, B2, B3.** A wheel built from this repo cannot start the CLI (`ModuleNotFoundError: waft.templates.typst`). The hand-written package list ships 202 of 516 Python files.
- **A1 to A4, A18, C10.** The 25 red tests trace to a half-wired tracing module and to undefined names. One ruff rule (F821) finds 31 of them; it is not in CI.
- **C1, A15.** CI runs only the tests under `tests/api`, roughly 7 percent of the suite. Measured coverage over all of `src` is 16 percent, and `main.py` (2,400 statements) is at 0.
- **E16, E2.** `POST /api/auth/handshake` gives the API token to any caller, and none of the 28 other write routes I called returned 401 without a token.
- **E7.** `pip-audit` finds known vulnerabilities in 21 locked packages, among them pypdf, pillow, starlette, cryptography and urllib3. Most have a fixed version.
- **F19.** API routes write state relative to the code, not the project: an unauthenticated `POST /api/pet/feed` created a file inside this checkout.
- **D1, D4, D16.** 9,015 `node_modules` files are tracked, third-party files sit in a public MIT repo with no recorded licences, and three plan files quote passwords for another project.
- **E1.** The Fernet key and the realm HMAC key are public in git history and are not recorded as rotated.
- **F2, F3.** `waft evolve` gave three variants the same id, every score was 100, improvement +0.00; the fitness function never runs a task.
- **G2, G3.** At least 18 docs name commands that the CLI does not have, and the README's "Substrate" is not what the code calls the substrate.
- **G7, H1.** WAFT is not in `_workbench/STATE.md`, and the repo has no one-sentence purpose.
- **I1, I11.** The repo already holds 297 open tickets in 70 active work efforts, 66 of them untouched since January.

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

**Second pass (same day, after "explore further"):**

12. Installed analysis tools into a scratch venv outside the repo (bandit, vulture, deptry, pip-audit, radon, detect-secrets) and `deptry` into this repo's local `.venv`. A combined docker and uvx command was declined by the permission check; I did not retry it.
13. Reran the suite with coverage (16 percent over `src`), ran bandit, vulture, radon, deptry, pip-audit and detect-secrets, compiled every tracked Python file, checked Markdown links, and counted duplicate blobs and personal-data patterns.
14. Ran the three ignored test files one at a time to read their errors (A7). Found that the clone is shallow (L9).
15. Started `waft serve` on a scratch project (port 8765), read its OpenAPI schema and called the unauthenticated write routes with empty bodies (E2, E16, F19). One probe created a file inside the checkout; I moved it to the scratchpad. A tracked SQLite `-shm` file changed during the runs; I restored it. The server was stopped afterwards.
16. Copied `visualizer/` to a scratch directory, ran `npm install`, `npm run build` and `npm test` (F22, D13). The test process hung and I killed it.
17. Read the code behind `waft evolve` (`core/evolution_engine.py`, `being.py`) and the API auth code, and mined the repo's own 135 work efforts and 499 tickets (I11).
18. A read-only helper agent reviewed the Electron app and the shell scripts. I rechecked its main claims (the `sandbox: false` setting, the `shell: true` spawn, the six debug `fetch` calls, the Electron version, script modes, the `set -e` counter bug, the publishing script lines) and marked in each item what I did and did not check. I also dropped one of its claims: it dated the first appearance of the key files to 2026-01-25, but that commit is the shallow boundary (L9).
19. Added 25 items and updated the evidence of 27 existing ones (several question marks became measurements), then regenerated this document and the tickets.

**Changed in the repo:**

- Commit `4ad0eee1` added `_pyrite/analytics/traces/2026-11-14.jsonl`. A test run generated it and the session's stop hook asked for untracked files to be committed. It probably should not be tracked (A10, D8, L2).
- This work effort: `_work_efforts/WE-261114-bklg_*/` with the index, the tickets and this document.
- No file in `src/`, `tests/` or the config was changed. `uv.lock`, trace files and `.empirica/sessions/sessions.db-shm` that tools rewrote during the runs were restored with `git checkout`; one file an API probe created inside the checkout was moved out.
- Local only, ignored by git: `_unified/empirica/`, `.venv/` (now also holding `deptry`), `build/`.

**Not done:**

- Docker was not built (B10). The Electron app was not run. The SvelteKit visualizer was built and tested in a scratch copy only. macOS and Windows were not tried (B11). The full git history and the 701 low-severity bandit findings were not read (L9, E13).
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
| Tracked files | 19,741; `.git` pack 687 MiB (shallow clone, see L9); working tree 2.9 GB with `.venv` | `git ls-files`, `git count-objects -vH`, `du` |
| Coverage | 16 percent of 58,876 statements; 258 modules at 0 percent; `main.py` 2,400 statements at 0 | `uv run pytest tests/ --cov=src/waft` (same 25 failures) |
| bandit | 717 issues: 7 high, 9 medium, 701 low (135,988 lines) | `bandit -r src` |
| pip-audit | 21 of 120 locked packages have advisories (281 as counted by the tool) | `pip-audit -r` on the exported lock, `dev` extra |
| deptry (src) | 83 undeclared imports, 21 transitive, 4 unused declared | `deptry src --known-first-party waft` |
| vulture (src) | 33 findings at 80 percent confidence; 1,433 at 60 percent | `vulture src` |
| radon (src) | 79 functions rank D or worse; 18 blocks rank F | `radon cc src -s` |
| Compile check | 4 of 1,109 tracked `.py` files (outside node_modules) have syntax errors | `compile()` on each file |
| Doc links | 147 of 273 relative links in README and docs/ are broken | script over 117 Markdown files |
| Duplicate content | 2,969 contents under more than one path; 5,336 extra copies; about 382 MiB | `git ls-files -s` |
| detect-secrets | 2,807 raw hits in 417 files (61 keyword hits in 27 files); none verified | `detect-secrets scan` over 7,3xx tracked text files |
| API surface | 95 paths, 106 operations, 41 write operations, 13 declare auth; 0 of 28 probed write routes returned 401 | `waft serve` on a scratch project, `curl` |
| Other servers | 20 server apps outside `src/`; 7 with wildcard CORS; 9 binding 0.0.0.0 | `grep` over tracked Python |
| Work-effort tickets | 499 tickets: 125 completed, 356 pending, 10 in_progress, 8 open; 297 open in 70 active work efforts | script over `_work_efforts/WE-*/tickets` |
| Visualizer (scratch copy) | install 28 s, build OK, 34 tests pass, test process did not exit | `npm install`, `npm run build`, `npm test` |
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

`M` `agent` `P2`

**Evidence.** Run one at a time, each fails at collection: `tests/test_foundation.py` with `ImportError: cannot import name 'KeyValueBlock' from 'waft.foundation'`; `tests/test_full_system.py` with `TypeError: TheFoundation.__init__() takes from 1 to 2 positional arguments but 3 were given`; `tests/test_the_absolute_begeesus.py` with `AttributeError: 'Evaluation' object has no attribute 'aesthetic'`. AGENTS.md tells everyone to pass `--ignore` for them, so whole files of tests never run.

**First step.** for each: fix the API drift (the tests or the code), turn it into a script under `scripts/`, or move it to `_to_delete/` for CT's approval.

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

**Evidence.** 151 warnings in the baseline run and 185 after the import patch. `datetime.utcnow()` appears 140 times in `src` (for example `tracer.py:32` and `storage.py:45`); Pydantic v2 `max_items` and class-based `Config` in `api/schemas/work_efforts.py` (lines 10, 16, 29, 35, 48, 54, 60, 89) and `api/schemas/projects.py`; `api/responses.py:10`.

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

`M` `agent` `P3`

**Evidence.** Measured with `uv run pytest tests/ --cov=src/waft` (same 25 failures, 99 s): total coverage is 16 percent (58,876 statements, 49,697 missed). 258 modules are at 0 percent (32,416 statements). `main.py` alone has 2,400 statements at 0 percent; next are `one_pager.py` 632, `foundation_v2.py` 485, `pyrite.py` 471, `cli/dungeon_cli.py` 404 and `core/pocketbase_scout.py` 380. The test module that would exercise the CLI (`tests/test_commands.py`) does not load (A6).

**First step.** fix A6 and add the smoke test in A19; set a coverage floor at today's 16 percent and ratchet it up; list the 0 percent modules next to the dead-code list (F7).

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

#### A19. Add a smoke test for every CLI command

`M` `agent` `P2`

**Evidence.** `src/waft/main.py` has 2,400 statements at 0 percent coverage (A15) and registers 82 commands; the one test module for the CLI, `tests/test_commands.py`, does not load (A6). No test runs `waft <command> --help` for each command.

**First step.** after A6, add one parametrized test that runs `--help` for every command and expects exit code 0; run it against an installed wheel too, which would have caught B2.


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

**Evidence.** `git tag` lists 0 tags. Three version schemes disagree: `pyproject.toml` says 0.10.0; `CHANGELOG.md` has `[Unreleased]` above 0.9.4 (2026-01-19); `src/waft/version` implements an epoch-based scheme (`v{Years}.{Months}.{Days}.{Hour}.{Quarter}`, epoch 2026-01-04). `waft --version` is not an option ("No such option").

**First step.** choose one scheme; write the release steps (bump, changelog, tag, build, publish or release asset); tag the right commit; add `waft --version` and make it print the same version everywhere.

#### B10. Build and run the Dockerfile

`R` `agent` `P2`

**Evidence.** the Dockerfile installs with `pip install .` (ignoring `uv.lock`) and starts `uvicorn src.waft.api.main:app --host 0.0.0.0`, a source-tree path that bypasses the installed package. It has no `USER` line (the container runs as root) and no `HEALTHCHECK`. It was never built: a `docker` binary exists on this machine but my attempt to query it was declined by the permission check, so I did not try. Given B1 the installed wheel is broken, so a container may work only because it imports from the copied `src/`. `docker-compose.yml` publishes `8000:8000` on all host interfaces, mounts the whole checkout writable at `/app` (`./:/app`) and runs uvicorn with `--host 0.0.0.0` (E17).

**First step.** build it in CI; choose one run path; pin the base image; add a health check (`/api/decision/health` exists).

#### B11. Test on macOS and Windows

`Q` `research` `P3`

**Evidence.** scripts use bash (`START_EVOLVE_UI.sh`, `scripts/dev-reinstall.sh`), 433 tracked files hold `/Users/ctavolazzi`, and the FogSift reports say nothing has run on macOS. Only Linux was tested here.

**First step.** add a macOS job to CI; list the failures.

#### B12. Remove the experiment folders from the uv workspace

`M` `agent` `P2`

**Evidence.** `pyproject.toml` has a `[tool.uv.workspace]` with five members: `_experiments/test_project_001`, `_experiments/existing_project`, `_experiments/test_project_002`, `_experiments/test_project_001/nested_project` and `narcissus_lab/internal_monologue`. Every uv command prints a deprecation warning about `tool.uv.dev-dependencies` in `narcissus_lab/internal_monologue/pyproject.toml`. The members' dependencies resolve into the root `uv.lock`, a likely cause of A11.

**First step.** drop the experiment members, fix or move the deprecated field, re-lock, and check that `uv.lock` stays stable (A11).

#### B13. Declare or remove the undeclared dependencies

`M` `agent` `P2`

**Evidence.** `deptry src --known-first-party waft` reports 83 modules imported but not declared, 21 transitive packages used directly and 4 declared but unused. Undeclared third-party names include `reportlab` (8 imports), `fitz` (PyMuPDF, 4), `plotly` (4) and `sklearn` (2). Used directly but only transitive: `yaml` (6), `requests` (3), `PIL` (3), `pandas` (2), `google` (2), `cryptography` (2), `numpy` and `dotenv` (1 each). Several first-party-looking names (`src`, `foundation`, `demo_api`, `scripts`, `rag_chatbot`, `tmcg`, `patterns`, `scientific_method_tool`) point at broken imports or path hacks. Declared but unused: the `crewai` extra and the dev tools `pytest`, `pytest-cov` and `ruff` (the last three are expected).

**First step.** decide per package: declare it in an extra, make the import lazy with a clear error, or delete the code; add deptry to CI with this count as the starting budget (C11).


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

**Evidence.** no workflow runs gitleaks, pip-audit, npm audit, bandit or CodeQL. Run by hand today: pip-audit found 21 vulnerable packages (E7), bandit 717 issues (E13), detect-secrets 2,807 raw hits in 417 files (mostly high-entropy strings in generated HTML and lock files) plus 61 keyword hits in 27 files that were not verified (E6).

**First step.** add gitleaks (pinned), pip-audit on the lock and bandit with `-ll`, each recording today's number as the starting budget (C11); `npm audit` for the front ends you keep.

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

#### C11. Add the new checks to CI with ratchets

`M` `agent` `P2`

**Evidence.** baselines measured today: coverage 16 percent; bandit 717 issues (7 high); pip-audit 21 vulnerable packages; deptry 83, 21 and 4; vulture 33 at 80 percent confidence; radon 79 functions rank D or worse; ruff F821 31; broken doc links 147 of 273; 4 files that do not compile; 28 write routes that never returned 401 (E2).

**First step.** add each as a job that records the number and fails only if it rises; lower the budget as items close; print the table in the weekly health run (L7).


### D. Repository size and hygiene

#### D1. Untrack the 9,015 node_modules files

`M` `agent` `P1`

**Evidence.** `git ls-files | grep -c node_modules` gives 9,015: `waft_desktop/electron` 5,065, `typst-webapp/frontend` 1,916, `waft_desktop/frontend` 1,486, `games/teleport_massive_adventure` 548. The root `.gitignore` ignores only `visualizer/node_modules`. 279 `.map` files are tracked as well. A helper agent also reports that `waft_desktop/START_DEV.sh` skips `npm install` because these directories already exist (lines not checked by me).

**First step.** `git rm -r --cached` those folders, add `node_modules/` to `.gitignore`, keep lockfiles, confirm each app still installs.

#### D2. Decide where generated PDFs live

`M` `CT` `P2`

**Evidence.** 3,082 tracked PDFs: `waft_pdf_library` 2,042, `_work_efforts` 551, `_archive` 139, `typst-demos` 70, `_temp_pdf_examples` 60, `_genetics` 31.

**First step.** mark each folder input or output; outputs go to release assets or get regenerated on demand; keep fixtures small.

#### D3. Decide what to do about the largest tracked files

`M` `CT` `P2`

**Evidence.** top files by size: `mediawiki-1.45.1.zip` 93.7 MiB; `examples/908530342-Building-AI-Agents-With-LLMs-RAG-And-Knowledge-Graphs-1.pdf` 90.8 MiB; `templates/1789_USA_Miller_Woods_TrailA_Visitors_Guide.pdf` 67.2 MiB; `PITCH_DECK/Waft__Breeding_AI_s_Future_.mp4` 39.3 MiB; three PDFs of 38 to 39 MiB in `_work_efforts/WE-260119-ejtx...`; a 31.1 MiB `.m4a` in `PITCH_DECK`. The `.git` pack is 687 MiB in this shallow clone (L9; the full history may be larger), and the 12 largest top-level folders of tracked files sum to about 1,400 MiB.

**First step.** options: Git LFS, release assets, a data repo, or history filtering (D12). Add a size check to CI (D11).

#### D4. Check the rights to third-party files in a public MIT repo

`R` `CT` `P1`

**Evidence.** tracked files include a book PDF ("Building AI Agents With LLMs, RAG, And Knowledge Graphs"), the GPT-4 Technical Report, several arXiv papers, a park visitor guide, a MediaWiki release (GPL) and `Latex Source Code.zip`. The licence of each is unknown. `CREDITS.md` lists AI assistants only; it has no credits or licences for third-party files.

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

**Evidence.** tracked: `.cursor` 171 files (1.4 MiB: 138 slash commands, 10 plans, 8 procedures, 4 continuation prompts, 1 skill), `.empirica` 12 files (1.6 MiB, including a SQLite database and its WAL and SHM files), `.empirica_reflex_logs` 12 (named in `.gitignore` but tracked earlier), `.playwright-mcp` 3 screenshots from 2026-01-26, `.obsidian` 5, `.waft/ollama_runtime.jsonl` (10 lines of prompts and responses). The sibling book repo had the same Empirica problem (FogSift FINDINGS item 2).

**First step.** read the contents for sensitive reasoning or paths; `git rm --cached`; extend `.gitignore`.

#### D8. Move runtime data out of git

`M` `agent` `P2`

**Evidence.** 4 tracked database files: `.empirica/sessions/sessions.db` (51 tables; 133 sessions, 56 reflexes; its `-wal` and `-shm` files are tracked too), `_pyrite/analytics/sessions.db`, `waft_memory.db` and `waft_pdf_library/backend/data/library.db` (2,125 PDF records); plus 162 tracked `.jsonl` files. During my runs, opening the Empirica database changed the tracked `.empirica/sessions/sessions.db-shm`; I restored it with `git checkout`.

**First step.** inspect for personal paths; split fixtures from runtime data; ignore the runtime paths (A10).

#### D9. Remove hardcoded /Users/ctavolazzi paths

`M` `agent` `P2`

**Evidence.** `git grep -I -l '/Users/ctavolazzi'` outside `node_modules` finds 433 files; `src` has 30 lines in 6 Python files (for example `web.py:28` writes a debug log there).

**First step.** replace with config or `Path(__file__)`-relative paths in `src`; leave historical docs.

#### D10. Spin parked projects out of the lab repo

`R` `CT` `P2`

**Evidence.** several products live here: `waft_desktop` (Electron, about 203 MiB tracked), `typst-webapp`, `games/`, `_realms/`, `PITCH_DECK`, `succulent_jewelry_pdfs`, `Bubbles`, `Campaigns`, `NARRATIVE-WAFT`. The repo holds 28 dependency manifests (`pyproject.toml`, `package.json`, `requirements.txt`) besides the root one, for example under `_experiments/`, `dnd_campaign_desktop_app/`, `recap_review_app/`, `typst-webapp/`, `waft_desktop/` and `waft_pdf_library/`.

**First step.** for each: keep, move to its own repo, or archive on a branch. Do it after D1.

#### D11. Set a size budget

`M` `agent` `P3`

**Evidence.** the working tree is 2.9 GB with `.venv`; biggest directories on disk: `waft_pdf_library` 307 MB, `_work_efforts` 276 MB, `waft_desktop` 226 MB, `templates` 143 MB, `examples` 106 MB.

**First step.** a CI check on total tracked size and on any new file over 5 MiB.

#### D12. Decide whether to rewrite history

`R` `CT` `P2`

**Evidence.** old commits still hold the Pexels and Pixabay keys and the API token (rotated 2026-11-09 per commit 67ce2ed8) and the two crypto keys (E1). `_workbench` ticket 8.4 says leave history. A rewrite would also shrink the 687 MiB pack but breaks every clone and open branch.

**First step.** CT decides; if yes, plan `git filter-repo` with a backup and a branch freeze.

#### D13. Commit the visualizer lockfile

`M` `agent` `P2`

**Evidence.** `.gitignore` lists `visualizer/package-lock.json`, so `npm ci` cannot be used and each install resolves fresh. A clean `npm install` in a scratch copy took 28 s for 374 packages and printed deprecation warnings (`inflight`, `rimraf` 2, `glob` 7). The build succeeded.

**First step.** remove the ignore line, commit the lockfile, switch docs and CI to `npm ci`.

#### D14. Remove duplicate files from the working tree

`M` `agent` `P3`

**Evidence.** 2,969 file contents are tracked under more than one path: 5,336 extra copies, about 382 MiB in the working tree (git stores each content once, so the pack grows less). Largest: an esbuild binary in `typst-webapp/frontend/node_modules` (29.4 MiB, 4 copies) and the `_archive/daily/2026-01-13/WAFT_GAME_RULES_*.pdf` files (5.9 MiB, 5 copies each).

**First step.** after D1 most copies disappear; then dedupe what is left or keep one and link.

#### D15. Review personal data in tracked text files

`M` `agent` `P2`

**Evidence.** a scan of 7,215 tracked text files (no `node_modules`, no binaries) found 68 distinct email addresses and 16 files with phone-number-like text. Most look like placeholders (`viewer@email.com`, `waft@example.com`), but `christopher@fogsift.com` and `porchroot@gmail.com` each appear in 12 files, and the phone-like text is in invoices and business cards under `_work_efforts/WE-260119-ejtx...`. Whether any belong to real people was not checked.

**First step.** list the real ones; replace with placeholders or remove; add a personal-data check to pre-commit (L3).

#### D16. Check the plans that quote passwords for another project

`R` `CT` `P1`

**Evidence.** `_work_efforts/Plans/gitguardian_secret_remediation_6d48b28c.plan.md` (and two copies under `_organized_constellation`) is a plan to rotate "REAL production credentials" of a Cloudflare Pages app (admin, editor, contributor and viewer accounts and a site password). It contains `password:` literals and a `SITE_PASSWORD` constant; its own to-do list still shows the docs step in progress and the production reseed pending. detect-secrets flags 5 keyword hits in each copy. I masked the values and did not inspect them. `_work_efforts/Plans` holds 284 plan files in all.

**First step.** CT confirms those credentials were rotated; remove the values from the three files (and from history if they were live); move other projects' plans to their own repositories.


### E. Security

#### E1. Rotate or retire the two crypto keys that are still public in history

`R` `CT` `P1`

**Evidence.** `_pyrite/.waft/.pyrite_secret_key` (a Fernet key) and the D&D realm `.hmac_key` were tracked in this public repo; untracked by commits 67ce2ed8 and 3f8cb670. Commit 67ce2ed8 says the Pexels key, the Pixabay key and the API token were rotated; it does not say the Fernet key was. Commit dd1992fd says both crypto keys must be kept locally because deleting them orphans encrypted secrets and invalidates realm state. So both values stay public and valid. The date the keys first entered history is unknown: the oldest commit visible here, `dc8e4d2a` (2026-01-25), is the shallow boundary and so shows every file as added (L9).

**First step.** inventory what is encrypted or signed with each; rotate with a re-encrypt or re-sign migration; generate on demand afterwards.

#### E2. Review API authentication

`M` `agent` `P1`

**Evidence.** `waft serve` run from a scratch project exposes an OpenAPI schema with 95 paths and 106 operations. 41 are writes (POST, PUT, PATCH, DELETE) and only 13 operations declare the HTTPBearer scheme. Called without a token: `POST /api/work-efforts` returns 401, but none of the other 28 write routes I called (all but `/api/pet/reincarnate`, which I skipped) returned 401: 200 for `/api/5050/continue-command`, `/api/being/spawn`, `/api/pet/feed`, `/api/protocel/create` and `/api/story/start` (plus `/api/auth/handshake`, see E16); 404 for 7 routes called with a made-up id; 422 for 14 routes called with an empty body; 500 for `/api/being/{id}/decision`. `GET /api/work-efforts` is open too.

**First step.** decide the policy (every non-GET route needs the token except the handshake); apply it router-wide; add a test that walks the OpenAPI schema and asserts 401 without a token.

#### E3. Review CORS settings

`M` `agent` `P2`

**Evidence.** `src/waft/api/main.py:120` sets `allow_origins` to four localhost URLs (ports 5173, 3000 and 8781 on localhost and 127.0.0.1) with `allow_credentials=True` and `*` for methods and headers; there is no wildcard origin. `tests/test_cors.py::test_actual_post_request_with_cors` returns 500 and A1 alone does not fix it.

**First step.** decide how a hosted deployment sets its origins (an environment variable); fix the 500 (A4).

#### E4. Audit shell and subprocess calls

`M` `agent` `P1`

**Evidence.** `src` has 241 `subprocess.` references, 14 `shell=True` and 4 `os.system`. bandit rates five of them high: `dealer/pdf_generator.py:221` and `main.py:4078` (B602, `shell=True`), `fogsift/simulation.py:17`, `pet/fogsift_cli.py:52` and `pet/fogsift_device.py:321` (B605, a shell started from a string). No `eval(`, `exec(`, `pickle.load` or `yaml.load(` hits. Where the arguments come from was not read.

**First step.** read those five first, then the other 13; for each: argument source (CLI, API, document text); replace with list arguments or `shlex.quote`.

#### E5. Remove leftover agent logging blocks

`M` `agent` `P2`

**Evidence.** five Python files contain `# #region agent log` (`web.py`, `document_builder.py`, `one_pager.py`, `evolution/document_components.py`, `evolution/golden_triangle.py`); `web.py:26` onward appends to `/Users/ctavolazzi/Code/active/waft/.cursor/debug.log`. `waft_desktop/electron/main.js` has six more of the same kind: `fetch` calls to `http://127.0.0.1:7248/ingest/...` that send the process id, the absolute backend path, the port, error text and context-menu link URLs to whatever listens on that loopback port.

**First step.** delete the blocks; run the staging gate's grep locally.

#### E6. Scan the full history for secrets

`Q` `agent` `P2`

**Evidence.** the current tree was scanned two ways: five regexes (`sk-`, `ghp_`, `AKIA`, `AIza`, `xox`) found nothing, and detect-secrets over 7,215 tracked text files (no `node_modules`, no binaries) raised 2,807 raw hits in 417 files: 2,209 base64-entropy, 537 hex-entropy and 61 keyword hits in 27 files, mostly docs about secrets, plan files (D16) and scripts. None was verified. The history (this clone is shallow, L9) and the vendored `node_modules` were not scanned.

**First step.** unshallow (L9); run gitleaks and trufflehog over all refs; classify each hit as live, rotated or fixture; triage the 27 keyword files first.

#### E7. Audit dependencies for known vulnerabilities

`M` `agent` `P1`

**Evidence.** `pip-audit` on the 120 distinct packages locked for the `dev` extra (2026-11-14): 21 packages have advisories (281 as the tool counts them, with duplicates). Most list a fix: cryptography 46.0.6 to 46.0.7, pillow 12.1.1 to 12.2.0, pypdf 6.9.2 to 6.10.0, starlette 1.0.0 to 1.0.1, urllib3 2.6.3 to 2.7.0, fpdf2 2.8.7 to 2.8.8, anthropic 0.86.0 to 0.87.0, and smaller ones (anyio, brotli, brotlicffi, certifi, gitpython, httplib2, idna, pyasn1, pydantic-settings, pygments, pytest, soupsieve, tornado); weasyprint 68.1 lists no fix. pypdf, pillow, weasyprint and fpdf2 parse files that users supply. `npm audit` was not run.

**First step.** upgrade the fixable ones with `uv lock --upgrade-package`, rerun the suite, decide about weasyprint, add pip-audit to CI (C6); run `npm audit` for the front ends you keep.

#### E8. Review the Electron app's security settings

`M` `agent` `P2`

**Evidence.** `waft_desktop/electron/main.js` (checked by me): `contextIsolation: true` and `nodeIntegration: false` but `sandbox: false` (lines 279 to 281); the backend is started with `spawn('waft', ['serve', ...], {shell: true})` (line 80); Reload, Force Reload and Toggle Developer Tools are in the right-click menu (lines 325 to 327; whether they are gated on dev mode was not checked); six debug `fetch` calls to `http://127.0.0.1:7248/...` remain (E5); Electron is `^28.0.0` locked at 28.3.3, an old major. A helper agent also read, and I did not check: the preload exposes only three fixed invoke calls plus listeners, but `removeAllListeners(channel)` forwards any channel name; there is no Content-Security-Policy and no `setWindowOpenHandler` or `will-navigate` guard; on macOS the backend respawns after the window closes; electron-builder ships only `main.js`, `preload.js` and `package.json`, so a packaged build cannot load its UI. `dnd_campaign_desktop_app/electron/main.js` and `recap_review_app/frontend/src/main.js` reportedly use the same `sandbox: false` pattern and were not reviewed.

**First step.** set `sandbox: true`, drop `shell: true`, add a CSP and navigation guards, gate DevTools on dev mode, upgrade Electron to a supported major, then check the two other Electron apps (or retire them with D10).

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

#### E13. Triage the high and medium bandit findings

`M` `agent` `P2`

**Evidence.** `bandit -r src` reports 717 issues over 135,988 lines: 7 high, 9 medium, 701 low. High: `core/status_persistence.py:73` and `:108` (B324, weak hash), `dealer/pdf_generator.py:221` and `main.py:4078` (B602), `fogsift/simulation.py:17`, `pet/fogsift_cli.py:52` and `pet/fogsift_device.py:321` (B605). Medium: `core/pocketbase_scout.py:135` (B103, file permissions), `main.py:853` and `core/realms/pocketbase_downloader.py:87` (B310, urlopen), `document_builder.py:962`, `templates/typst/compiler.py:107` and `:108` (B108, fixed /tmp path), and three B104 bind-all hits covered in E14. The 701 low findings were not read.

**First step.** read each of the 16, fix it or mark it with a reason; add bandit to CI with this list as the baseline (C11).

#### E14. Stop two commands from listening on all interfaces by default

`M` `agent` `P1`

**Evidence.** `main.py:4576` (`waft rag ui`) and `main.py:4623` (`waft rag serve`) default `--host` to `0.0.0.0` on port 7860, so the Gradio app listens on every network interface. `core/door_guy.py:96` also contains `0.0.0.0`, but in a blocklist (a false positive). `waft serve` itself defaults to localhost.

**First step.** default to `127.0.0.1`, require an explicit `--host 0.0.0.0` with a printed warning; add a test of the defaults.

#### E15. Tighten the 20 other servers outside src

`M` `agent` `P2`

**Evidence.** 20 tracked Python files outside `src/` start a FastAPI, Flask or `HTTPServer` app. 7 allow every origin (`allow_origins=["*"]`): `cute_test_runner/server.py`, `dnd_campaign_desktop_app/backend/campaign_server.py`, `examples/dnd_game_server.py`, `recap_review_app/backend/main.py`, `scripts/mission_control_village_api.py`, `scripts/quest_server.py` and `simulation/simulation_server.py`. 9 bind `0.0.0.0`: `_realms/odd_realm/app.py`, `api/guide_api.py`, `cute_test_runner/server.py`, `examples/dnd_game_server.py`, `scripts/launch_dnd_campaign.py`, `scripts/mission_control_village_api.py`, `scripts/research_simulation_server.py`, `simulation/simulation_server.py` and `typst-webapp/backend/main.py`. None uses `debug=True`. Whether any of them is still used was not checked. `games/teleport_massive_adventure/scripts/start_autoplayer.sh:14` also runs `python3 -m http.server 8000` with no `--bind`, which serves the game folder on every interface and collides with the API port.

**First step.** list which servers are live; delete or archive the rest (with CT's approval); for the live ones default to localhost and name the allowed origins.

#### E16. Stop the handshake route from handing the API token to any caller

`M` `agent` `P1`

**Evidence.** `api/routes/auth.py:42` to `:66`: `POST /api/auth/handshake` has no authentication, calls `get_or_create_token(project_path)` and returns the token in the response body (the docstring calls it a "one-time setup for local development"). Measured: it answered 200 to a call with no credentials and an empty JSON body. So the bearer scheme protects nothing from a client that can reach the port. `api/auth.py:82` compares tokens with `==` (not constant time); the token is a 32-byte `secrets.token_urlsafe` value stored in `.waft_api_token` with mode 600 and never expires. The Dockerfile starts uvicorn on `0.0.0.0:8000` (B10), so a container exposes the handshake to the network.

**First step.** limit the handshake to loopback clients (`request.client.host`) or hand the token over some other way (printed once at startup); use `hmac.compare_digest`; add expiry and rotation; add tests for all three.

#### E17. Do not publish the open API with the checkout mounted writable

`R` `agent` `P1`

**Evidence.** `docker-compose.yml` publishes the API on `8000:8000` (every host interface), bind-mounts `./` at `/app` and sets `WAFT_PROJECT_PATH: /app`; the container runs as root (B10). Combined with E16 (the handshake returns the token), E2 (28 write routes need no token) and F19 (routes write relative to the code), a client on the network could create files in the mounted checkout. This follows from the configuration and my local probes; I did not run the container.

**First step.** publish on `127.0.0.1:8000:8000` by default; mount a separate data directory instead of the repo; fix E16 and E2 first; add a `USER` and a `HEALTHCHECK`.

#### E18. Make the publishing scripts ask before they push

`M` `agent` `P2`

**Evidence.** checked by me: `push_to_github.sh` runs `git add .` (line 32), `git branch -M main` (49) and `git push -u origin main` (56) against a hardcoded remote with no prompt; `scripts/promote-staging-to-main.sh` sets `VERSION` only through `--version` (line 27) and tests `-n "$VERSION"` at line 129, so an inherited `VERSION` variable creates and pushes a release tag. Helper agent, not checked by me: `setup_github.sh` also does `git add .` and commits with a stale v0.1.0 message; `scripts/upload_wiki.sh` clones the wiki into `.wiki-temp` inside the repo (not ignored) and pushes with no prompt; both promote scripts run `git checkout` and `git pull` even under `--dry-run`, so "No changes were made" is false.

**First step.** initialise `VERSION` empty; add a confirmation prompt and a `--yes` flag; stop `git add .`; refuse to run from a non-main branch; make `--dry-run` change nothing.


### F. Architecture and code quality

#### F1. Split main.py into command modules

`M` `agent` `P2`

**Evidence.** `src/waft/main.py` is 4,918 lines and registers 82 top-level commands (`waft --help`); `src/waft/cli/` already holds 16 modules. `src/waft` totals about 174,000 lines in 516 files.

**First step.** move command groups into `cli/`, keep `main.py` as wiring, do it behind the existing tests.

#### F2. Fix variant identity in waft evolve

`M` `agent` `P1`

**Evidence.** `waft evolve --generations 2 --variants 3` printed one id three times (`being_20261114_153322_37e1e692`), then `fitness=100.00, scints=0` for each, "Fitness improvement: +0.00" and a total time of 0.01 s. Cause (read): `src/waft/being.py:1836` builds the id from `datetime.now().strftime('%Y%m%d_%H%M%S')` (one-second resolution) plus the first 8 hex digits of `sha256(reality_id + parent_being_id)`, so variants spawned in the same second share an id; skill mutations (`being.py:1846`) are derived from a hash of that id and the skill name, so they are identical too. `core/evolution_engine.py:318` and `:319` add unseeded `random.uniform` changes to `will_to_live` and `luck`. FogSift gap #44 records the same id defect.

**First step.** add the variant index or a random suffix to the id; derive mutations from (id, generation, index); seed the random generator from a run seed; add a test that N variants have N ids and N distinct genomes.

#### F3. Find out what "evolution" operates on

`M` `research` `P1`

**Evidence.** `core/evolution_engine.py` lines 63 to 131: `evaluate_fitness` never runs the trial tasks (a code comment says "For now, simple heuristic based on being's attributes"); for each task string it runs the same three detectors on the same being (logic fractures, knowledge gaps, safety violations), so a scint is counted once per task. Fitness is 100 minus 10 per scint plus 5 per skill above 80, clamped to 0 to 100. A freshly spawned being has none of the impossible states the detectors look for, so every variant scores 100. Mutation changes numbers (skill levels by up to 5 percent, `will_to_live`, `luck`); in this path no code is generated or rewritten. Provider names appear in few files (anthropic 2, openai 3, ollama 5, gemini 3 files) and `evolve` calls no model.

**First step.** write the one-page spec: genome fields, mutation operators, fitness function; say plainly in the README what `evolve` does today; decide what a real trial (an executed task with a measurable result) would be (R2).

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

`M` `agent` `P3`

**Evidence.** vulture on `src`: 33 findings at 80 percent confidence or higher (for example unused variables at `cli/banner.py:378` and `core/alignment.py:46`) and 1,433 at 60 percent or higher; many of the second group will be CLI and API entry points that vulture cannot see.

**First step.** triage the 33; intersect the 60 percent list with the 0 percent coverage modules (A15); archive what both agree on, with CT's approval.

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

**Evidence.** seven exist: the FastAPI app (`waft serve`), the `dashboard` and `dashboard-5050` commands, the observatory (`core/observatory/server.py`, 1,390 lines), Streamlit (`ui/streamlit`), the SvelteKit `visualizer/`, the Electron `waft_desktop/`, and `typst-webapp/`. In a scratch copy the visualizer installs, builds and passes its tests (F22); the SvelteKit build is not present in this checkout, so `waft serve` starts in API-only mode.

**First step.** for each: last used, who uses it, build status; keep one or two.

#### F14. Find why a first quickstart run changed tracked files in the checkout

`M` `agent` `P1`

**Evidence.** my first run of `waft new demo`, `waft verify` and `waft evolve --generations 2 --variants 3` (cwd a scratch directory, started with `uv run --project /home/user/waft`) left four tracked files modified in `/home/user/waft`: `_pantheon/the_dealer/memory.jsonl`, `state.json`, `truth/keys.json` and `seals/gate_02_the_marker.pdf`. Two reruns did not reproduce it. `verify` rolls dice ("CON Check ... failure"), so the outcome may depend on a random roll. Relative paths `Path("_pantheon/the_dealer")` appear at `main.py:1064` and `core/dealer_journal.py:16`. I reverted the files. F19 found the same class of bug in the API: state written relative to the code, not the project.

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

#### F18. Fix or archive the four tracked Python files that do not compile

`M` `agent` `P3`

**Evidence.** compiling the 1,109 tracked `.py` files outside `node_modules` found 4 syntax errors: `_temp/template_function.py:94` (f-string), `demo_output/scripts/script.py:3` and `demo_output/scripts/test.py:3` (leading zeros in a decimal literal) and `scripts/generate_tavern_game_with_skills.py:580` (invalid decimal literal).

**First step.** fix them or move them to `_to_delete/` for CT's approval; add a compile check for tracked Python to CI (C11).

#### F19. Resolve project paths from the project, not from __file__

`M` `agent` `P1`

**Evidence.** 27 files in `src` derive a root with `Path(__file__)` and three or more `.parent` calls, among them `api/routes/pet.py:14` and the `being`, `protocel`, `storyteller` and `gym` routes. Measured: with `waft serve` running from a scratch directory, an unauthenticated `POST /api/pet/feed` created `_realms/waft_pet/pets/being_20261114_155231_796fa38d.json` inside this checkout (I moved the file out). In a wheel install the same code would write into site-packages. 20 `sys.path.insert` or `append` calls in 19 files add `src` to the path the same way. This is the likely cause of F14.

**First step.** use `app.state.project_path` (it exists in `api/main.py`) or the CLI's `--path`; delete the `sys.path` edits; add a test that runs the API in a temp project and asserts the checkout stays clean.

#### F20. Refactor the most complex functions

`M` `agent` `P3`

**Evidence.** `radon cc src`: 79 functions rank D or worse and 18 blocks rank F (complexity over 40). Worst: `generate_typst_from_parsed_data` in `cli/case_render.py` (100), `Visualizer.analyze` in `core/visualizer.py` (78), `CritiqueResponseManager._generate_response_report` in `core/critique_response.py` (58), `render_town_view` in `ui/streamlit/town_view.py` (56), `GameMaster.start_encounter` in `src/gym/rpg/game_master.py` (54), `parse_markdown_case_file` in `cli/case_render.py` (50) and `oracle` in `main.py` (45).

**First step.** pick the ten worst; add characterization tests first; then split.

#### F21. Replace print, silent excepts and other smells

`M` `agent` `P3`

**Evidence.** counts in `src` (grep): 1,575 `print(` calls, 69 `except Exception` blocks that only `pass`, 21 bare `except:`, 229 `open(` calls with no encoding (rough pattern), 140 `datetime.utcnow()` uses (A12), 15 TODO, FIXME, HACK or XXX markers and 1 `raise NotImplementedError`.

**First step.** route output through `logging` or Rich consistently; replace silent excepts with a logged handler; set `encoding="utf-8"` on text opens; ratchet each count.

#### F22. Make the visualizer test run exit

`M` `agent` `P3`

**Evidence.** in a scratch copy of `visualizer/`, `npm test` ran 3 test files (34 tests, all passing: 1, 17 and 16) but the `vitest run` process did not exit within 9 minutes and I killed it. The build printed 20 warnings, among them A11y warnings in `routes/projects/+page.svelte` and `routes/mission-control/+page.svelte` and a missing `.svelte-kit/tsconfig.json` base config (`svelte-kit sync` has not run).

**First step.** find the open handle (an interval, a server or a watcher started by the experiment runner test) and close it; fix the warnings.

#### F23. Fix helper scripts that abort or leave processes behind

`M` `agent` `P3`

**Evidence.** checked by me: `scripts/sync-cursor-commands.sh` runs under `set -e` (line 8) and increments counters with `((SKIPPED++))` and `((SYNCED++))` (lines 50, 54, 59); in bash `set -e; X=0; ((X++))` exits with status 1, so the script stops after the first file, and its `cp` overwrites commands in `~/.cursor/commands` with no backup. `waft_desktop/START_DEV.sh` starts `npm run dev &` (line 63) and `npm start` (73) but registers its cleanup trap only at line 77, after `set -e` (line 4) can already have exited. Helper agent, not checked by me: `START_EVOLVE_UI.sh` runs `cd visualizer` relative to the caller's directory; several start scripts write fixed `/tmp/*.log` names and leave servers running.

**First step.** initialise counters with `X=$((X+1))`; move the trap above the first background process; use `mktemp` and `trap`; run `shellcheck` over the 36 tracked shell scripts and add it to CI.


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

**Evidence.** README and `PITCH_DECK` use phrases such as "Don't just build agents. Breed them." and "God-Head". README Core Pillar 1, "The Substrate", says "Agents that write their own Python source code (DNA)"; in the code, `core/substrate.py` is `SubstrateManager`, a wrapper around uv commands (init, sync, add), and no path I read makes an agent write its own source. FogSift FINDINGS (2026-10-25) says the "God-Head" term appears only in documentation and nothing in `src/` or `tests/` measures it.

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

`M` `agent` `P3`

**Evidence.** a link check over `README.md` and the 116 Markdown files under `docs/` found 273 relative links, 147 of them pointing at files that do not exist. `docs/DOCUMENTATION_INDEX.md` alone has 83 broken links, `docs/TYPST_TEMPLATES_BROWSER_REPORT.md` 25, `docs/api/API_INDEX.md` 19, `docs/GETTING_STARTED.md` 7 and `docs/FAQ.md` 5.

**First step.** commit the checker (`scripts/check_doc_links.py`); fix or delete the dead links, starting with the index; add it to CI with today's 147 as the budget.

#### G11. Decide the fate of the field-manual landing page

`R` `CT` `P3`

**Evidence.** commit 9c4bcf8d on branch `dev` (2026-07-24): "add WAFT field-manual landing page", a self-contained interactive page. It is on `dev`, not `main`.

**First step.** publish it (where?) or archive it; its claims must match G3.

#### G12. Document or remove the undocumented executable scripts

`R` `agent` `P3`

**Evidence.** 36 tracked `.sh` files outside `node_modules` (34 mode 755, 2 mode 644 despite shebangs; modes checked, names of the two not). A helper agent found six executables named in no doc, code or CI file: `_science_textbook/compile.sh`, `examples/START_PROJECTS_DASHBOARD.sh`, `install_latex.sh`, `open_small_iterm.sh`, `verify_latex.sh` and `recap_review_app/backend/docker-entrypoint.sh`. It also reports that `install_latex.sh` is the only script using `sudo` (macOS, `brew` and `tlmgr`, no confirmation) and that 12 Python files and several scripts carry hardcoded `/Users/...` or `/Volumes/...` paths (D9).

**First step.** list every script with one line on what it does and whether it is current; delete or archive the rest with CT's approval; keep `install_latex.sh` manual.


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

**Evidence.** no budget is recorded anywhere read; the repo has 135 work efforts, and this clone is shallow (L9), so its 86 commits (2026-01-25 onward) are not the whole history.

**First step.** set a number of hours per week; revisit monthly.

#### H9. Check the name WAFT for collisions

`Q` `research` `P3`

**Evidence.** B8 covers PyPI; other collisions were not searched.

**First step.** search existing projects, trademarks and domains named waft; report.

#### H10. Decide what to do with the Cursor era material

`R` `CT` `P3`

**Evidence.** `.cursor/` holds 171 tracked files: 138 slash commands, 10 plans, 8 procedures, 4 continuation prompts and 1 skill. AGENTS.md is also written for Cursor Cloud.

**First step.** keep the commands CT still uses (port them to Claude skills), archive the rest, and stop tracking tool output (D7).


### I. Fit with _pyrite, Empirica, FogSift and the work-effort ledger

#### I1. Triage the 132 work efforts

`M` `agent` `P1`

**Evidence.** 135 `WE-*` folders on disk (`fogsift.py we list` shows 132): active 69, completed 27, open 16, pending 11, in_progress 1, template 1, and 7 rows it cannot read (front matter does not parse). Dates run from January to March 2026. pyrite's own vocabulary is active, paused, completed. Of the 70 active work efforts, 66 were last updated in January 2026 (I11).

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

#### I11. Reconcile this backlog with the 297 open tickets the repo already holds

`M` `CT` `P1`

**Evidence.** 135 work efforts hold 499 tickets: 125 completed, 356 pending, 10 in_progress, 8 open. The 70 active work efforts hold 297 open tickets; 47 of them have open tickets, 21 have none, and 66 were last updated in January 2026. Largest clusters: AI-Scientist Integration Study (13), The Tribunal (12), Heavy Seed Protocol (12), Case File System Evolution (10), Death Encounter System (10), DnD Narrative Storybook (10), Encapsulated Environments (10), Science-Bitch Command (10), pydyf Testing and Secure Sandbox Environment (9). Overlap with this backlog: `WE-260112-yh09` has three pending sandbox tickets (design, a Docker-based sandbox, a testing framework), which is E11; `WE-260109-sec1` has "Add security tests for input validation" pending, which is E10; `WE-260116-279z` has "Implement POST /api/projects endpoint with auth" pending, which is E2.

**First step.** sort each open ticket into keep, close or merge into a backlog id; start with the clusters named here; close the rest with a note.

#### I12. Triage the note and plan piles

`M` `agent` `P3`

**Evidence.** `_pyrite/` inside this repo has 653 tracked files (6.0 MiB): `active/` holds 162 files (many `next_steps` notes dated 2026-01-13 to 2026-01-19) and `journal/` 58. `_work_efforts/Plans` holds 284 plan files and `.cursor/plans` 10; some are copies (`_organized_constellation/_originals_backup`).

**First step.** mark each pile current, historical or duplicate; archive with a README; keep one index (G1).


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

#### L9. Unshallow the clone before any history work

`M` `agent` `P2`

**Evidence.** `git rev-parse --is-shallow-repository` is `true` here: 86 commits are reachable, from 2026-01-25 to 2026-11-14, while the first work effort is dated 2026-01-04 and GitHub shows 254 workflow runs. History statements in this document (A5, D3, D12, E6, H8) rest on a partial clone.

**First step.** `git fetch --unshallow`, then recheck pack size, commit count and authors, and rerun the history scans.


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

**Evidence.** `waft evolve` uses unseeded `random.uniform` and `datetime.now()` in ids, so two runs with the same inputs differ. FogSift #234 says its own lab harness is deterministic for a seed; that is a different code path. Saturated scores (F2) hide the difference anyway.

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
- **S4.** Second pass: coverage, static analysis, dependency audit, API probes, ledger mining.

## Caveats

- Linux container only. Python 3.14.3 through uv. No macOS, Windows or Docker.
- This clone is shallow (86 commits, from 2026-01-25). Anything about history is provisional until `git fetch --unshallow` (L9).
- The static-analysis tools ran from a scratch venv, so their counts depend on tool versions and default rules; the tools are not part of the repo.
- Two probes of the running API created files; one landed inside the checkout and was moved out (F19). The calls used empty or made-up inputs, on a scratch project, against localhost.
- Numbers marked `M` come from commands I ran today; they will drift as the repo changes. Rerun the command in the Baseline table before relying on one.
- Items marked `R` repeat what a file, commit message or the GitHub API said. I did not rerun them.
- Library and project names in R1 are from memory and must be checked against their sources before they go into any document.
- Priorities are my judgment.
