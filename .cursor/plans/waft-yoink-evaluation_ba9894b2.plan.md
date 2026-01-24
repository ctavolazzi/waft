---
name: waft-yoink-evaluation
overview: Evaluate all shared repos for reusable patterns/code for WAFT (Teleport Massive), document findings with file-level citations and license notes, and track the work effort + devlog + Empirica checkpoints.
todos:
  - id: tracking-setup
    content: Run Empirica + love-you, set work effort/devlog
    status: pending
  - id: waft-context
    content: Review WAFT context docs for mapping targets
    status: pending
  - id: repo-intake
    content: Index all repos, licenses, and key files
    status: pending
  - id: pattern-extraction
    content: Deep-dive pattern extraction with citations
    status: pending
  - id: waft-mapping
    content: Map patterns to WAFT and draft yoink list
    status: pending
  - id: deliverables
    content: Write report + PDF, update devlog, postflight
    status: pending
---

# WAFT Yoink Evaluation Plan

## Scope
Evaluate and extract reusable patterns/code from these repos:
- `ctavolazzi/choose-your-own-adventure-game`
- `ctavolazzi/answer`
- `ctavolazzi/workadventure`
- `ctavolazzi/Trilium`
- `ctavolazzi/rag-chatbot`
- `ctavolazzi/pytest-html`
- `ctavolazzi/vibekit`
- `ctavolazzi/metrics`
- `ctavolazzi/tldr`
- `ctavolazzi/Agentic-Desktop-Pet`
- `ctavolazzi/Git-Gud` (gold standard)
- `ctavolazzi/slaytheweb` (target tool)
- `Jonahss/wyldcard-public` (physical target)
- `Trebek/pydealer`

## Plan
1. Tracking and setup
   - Start Empirica session and submit preflight, then log any unknowns or findings during review.
   - Execute `/love-you` to record the user’s positive feedback.
   - Search for a related work effort in `[_work_efforts](./_work_efforts)` and confirm whether to update it or create a new one.
   - Update the devlog with the plan in `[_work_efforts/devlog.md](./_work_efforts/devlog.md)` (or the repo’s canonical devlog location if different).

2. WAFT context alignment
   - Read WAFT context docs to anchor pattern mapping and naming:
     - `[README.md](./README.md)`
     - `[WAFT_SYSTEM_INTEGRATION.md](./WAFT_SYSTEM_INTEGRATION.md)`
     - `[WAFT_GAME_RULES.md](./WAFT_GAME_RULES.md)`
     - `[WIKI_Getting_Started.md](./WIKI_Getting_Started.md)`
     - `[WAFT_DND_KARMA_HANDBOOK.md](./WAFT_DND_KARMA_HANDBOOK.md)`

3. Repository intake and indexing
   - For each repo, capture:
     - README/architecture/design docs
     - License and constraints
     - Directory tree and key modules
   - Prefer `gh api`/raw file reads to avoid heavy cloning; only clone into a dedicated `_temp` subfolder if needed (no deletions).
   - Maintain a repo index (name, purpose, key files, license) inside the selected work effort folder.

4. Pattern extraction (full deep-dive)
   - Identify reusable patterns with file-level citations:
     - Game loop/state management
     - Deck/card data models and rule resolution
     - Content pipeline (definitions, JSON/YAML, asset handling)
     - UI/UX patterns relevant to text-first and card-first presentation
     - Export/rendering pipelines (PDF, images, etc.)
   - Record “yoink candidates” with rationale and license constraints.

5. WAFT mapping and recommendations
   - Map each extracted pattern to WAFT integration points and propose implementation targets.
   - Produce a prioritized “yoink list” with:
     - What to reuse
     - Where it should live in WAFT
     - Expected lift/risks

6. Deliverables and close-out
   - Add a consolidated report and yoink list to the selected work effort.
   - Generate a PDF report of findings (Typst/Owlbear Typst) and save it alongside the work effort report.
   - Update `[_work_efforts/devlog.md](./_work_efforts/devlog.md)` with completion status.
   - Submit Empirica postflight and log learnings.

## Notes/Constraints
- Do not run `npm dev` or `npm build`.
- No deletions; create new files only as needed for reports/logs.
- Use Typst (Owlbear Typst) for the PDF report.
- Ensure all reused ideas are vetted against repo licenses.
