# FogSift WAFT Prompt — Independent Professional Setup

Use this prompt to bootstrap `FogSift/waft` as a professional presentation surface, fully separate from this personal development workspace.

```text
You are operating on the professional repo: https://github.com/FogSift/waft.git

Context discovered from remote poll:
- default branch: main
- currently minimal contents: .gitignore, LICENSE, README.md
- latest commit: "Initial commit"

Mission:
Set up this repository as an independent professional surface, not a mirror of the personal dev workspace.
This means clean structure, clear public-facing docs, professional GitHub hygiene, and no leakage of personal/internal artifacts.

Critical separation constraints:
1) Do not reference local paths from personal workspace.
2) Do not copy `_work_efforts`, `_pyrite`, `.empirica`, local runtime artifacts, or private journals.
3) Do not import internal-only docs verbatim.
4) Keep this repo self-contained and public-ready.

Your task:
Generate the full setup plan and write one script that performs GitHub/project setup.

Required script to create:
- `scripts/setup_professional_repo.sh`

Script responsibilities:
1) Preflight:
   - verify `gh auth status`
   - verify inside cloned `FogSift/waft` repo
   - verify default branch `main`
2) Repository hygiene:
   - create/update `.editorconfig`
   - ensure robust `.gitignore` for Python/tooling
   - create `pyproject.toml` (minimal package metadata + test tooling)
3) Professional GitHub scaffolding:
   - create `.github/ISSUE_TEMPLATE/bug_report.md`
   - create `.github/ISSUE_TEMPLATE/feature_request.md`
   - create `.github/pull_request_template.md`
   - create `.github/CODEOWNERS`
   - create `.github/workflows/ci.yml` (lint + tests)
4) Documentation surface:
   - replace README with professional mission + quickstart + roadmap-lite
   - add `CONTRIBUTING.md`
   - add `CODE_OF_CONDUCT.md`
   - add `SECURITY.md`
   - add `docs/ARCHITECTURE_OVERVIEW.md` (core-only)
5) Minimal WAFT scaffold (independent):
   - `src/waft/__init__.py`
   - `src/waft/core.py`
   - `src/waft/cli.py`
   - `tests/test_core.py`
   - `tests/test_cli.py`
6) GitHub API setup via `gh`:
   - create labels (bug, enhancement, docs, chore, roadmap, good first issue)
   - enable auto-delete branch on merge
   - optionally set repo description/homepage if empty
7) Final output:
   - print changed file tree
   - print next commands to run tests and open first PR

Branching/commit behavior:
- create branch `bootstrap/professional-surface`
- commit in logical chunks:
  1) github scaffolding
  2) docs
  3) minimal code scaffold
- do not push unless explicitly instructed

Implementation style:
- Keep code direct and minimal.
- Prefer standard library for bootstrap code.
- No over-architecture.

Validation checklist:
- `pytest` passes
- CI workflow is syntactically valid
- README reads like a standalone professional project
- no personal workspace references remain

Deliverables from you:
1) Script contents for `scripts/setup_professional_repo.sh`
2) Full list of files created/updated
3) Commands to execute script safely
4) A short "deferred for later" list (max 8 bullets)
```
