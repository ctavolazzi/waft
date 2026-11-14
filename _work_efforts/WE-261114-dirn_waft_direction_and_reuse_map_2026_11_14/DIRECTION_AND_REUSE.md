# WAFT direction and reuse map

**Date:** 2026-11-14  
**Work effort:** `WE-261114-dirn` (tickets P0.1 to P5.1 and D1 to D3)  
**Branch:** `claude/environment-setup-3whfys`  
**Status:** proposal for CT. Nothing in `src/` was changed. Companion to the investigation backlog `WE-261114-bklg`, whose item ids (A1, B2 and so on) are used below.

> **Update, 2026-11-14 (build pass).** Phases P0, P1, most of P2 and P4.1 are built. [BUILD_LOG_2026-11-14.md](BUILD_LOG_2026-11-14.md) says what was done and corrects two things below: the same seed gives the same *result digest*, not the same head hash, and `waft evolve` was kept rather than aliased.

CT asked to keep exploring, to steer WAFT's development, and to look through the other repos for code WAFT can use. This page gives one recommended direction, the evidence for it, a phased plan with a check for each phase, and a map of reusable code across the 12 repos.
## The recommendation

WAFT already holds a small but real evaluation, and the pieces to make "directed evolution of agents" honest exist in CT's other repos. Put three of them together and WAFT does what its README says, in a way anyone can check:

1. **The gym** (`src/gym/rpg` in this repo, 1,252 lines, 5 passing tests). It hands an agent a task prompt, validates the answer with WAFT's own `InputTransformer`, detects "scints" (syntax tears, logic fractures), runs a repair loop, and scores the run: `fitness = 0.4 stability + 0.3 efficiency + 0.3 safety` (`models.py:281`). The agent is any function `prompt -> text`, so a real model plugs in directly.
2. **The lab loop** (`_workbench/fogsift-system/checks/waft_lab.py`, 308 lines). A seeded evolution loop over that gym: genomes with content-hash ids, a deterministic random stream per call, Gaussian mutation, elitist selection, death below 0.5, a JSONL flight recorder and a summary. Measured today with this repo's venv: 5 generations, population 8, 6 trials, seed 7; best fitness rose from 0.88 to 0.95; two runs with the same seed gave the same artefact hash (`e27b0de175aa048c`) and a different seed gave a different one; 25 s. It needed the runtime patch for backlog items A1 and A3 to run at all.
3. **The Logbook** (`_workbench/fogsift-system/fogsift_api/custody.py`, 730 lines, standard library only). A hash-chained, content-addressed run record with checks, controls (planted defects that prove a check can fail), two-way measurements, and a published head hash; a second verifier in Node (`logbook/verify.mjs`) shares no code with it. Its suite ran here: 108 tests, 4 skipped, 1 failure (the published head is no longer quoted in `_workbench/STATE.md`; the code itself passed).

`waft evolve` today does none of this: its fitness never runs a task, every variant scores 100 and all variants in a generation share one id (backlog F2, F3; the lab's own doctor confirmed it: 4 variants, 1 distinct id per generation). So the direction is to replace the core, not to polish it.

Everything else in the repo (games, desktop apps, the PDF library, lore, seven front ends) is optional. It should move out of the core package (backlog D10) so the core can be tested, packaged and explained.

## What I measured for this

All on 2026-11-14, Linux, Python 3.14.3 through uv, in scratch directories outside the repos.

- **The lab loop on WAFT's real gym.** `checks/waft_lab.py --doctor` with this repo's venv: best fitness 0.88 at generation 0 and 0.95 at generation 5 (population 8, 6 trials, seed 7); two same-seed runs produced the same artefact hash and a different seed a different one; 25 s. It reported two problems, both already in the backlog: the gym's validator fails as shipped (`NameError: get_tracer`, A1) and `waft evolve` gives 4 variants 1 distinct id (F2). A 15-generation run reached 1.00 by generation 9 and the mean rose from 0.81 to 0.99: the three quests saturate quickly, so harder and held-out tasks are needed (P3.1).
- **The Logbook.** FogSift's suite: 108 tests, 4 skipped, 1 failure; the failure is that `_workbench/STATE.md` no longer quotes the published head hash, not a code fault. A 40-line probe recorded two lab runs in one Logbook (two runs, three checks, the flight recorder stored by hash), concluded "pass" and verified against its head.
- **The model client.** `tavern-keeper-bot`'s suite: 120 tests, 120 pass, 11.6 s, no network (25 of them cover `llm.js`).
- **pyrite.** Its work-effort self-checks pass (25 and 57 checks) and the linter's read-only check passes (5 checks).
- **WAFT's own pieces.** The gym's 5 tests pass; `door_guy.py` and its neighbours' tests pass (45 passed, 3 xfailed in that group).
- **A packaging trap behind backlog B2.** 18 test files and 13 source files import `src.waft...` instead of `waft...`, so the tests run against the source tree and never against an installed package.

## The target shape

| Part | What it is | Comes from |
|---|---|---|
| `waft.gym` | tasks, validation, scint detection, repair loop, fitness | `src/gym/rpg`, moved into the package (the top-level name `gym` collides with the existing PyPI `gym` package) |
| `waft.lab` | genome, deterministic randomness, mutation, selection, elitism, run summary | port of `checks/waft_lab.py` |
| `waft.agents` | one protocol (`__call__(prompt) -> str`) with a deterministic mock, a local model over HTTP (llama.cpp or Ollama), hosted providers, a fallback chain and a fake for tests | mock from `waft_lab.py`; the provider and fallback pattern from the survey below |
| `waft.record` | one run = one Logbook chain; the head hash is printed and can be committed | `fogsift_api/custody.py` (plus `schemas.py`) |
| tasks | the 3 quests in `waft_temple.json`, then a second family: small repositories with planted documentation defects, scored by recall and precision against a known truth | `fogsift_api/fixture.py` (106 lines) |
| CLI | `waft lab run`, `waft lab verify RUN --expect-head HASH`, `waft lab report RUN`; `waft evolve` becomes an alias of `waft lab run` | new, small |

A genome for a real model agent is its configuration: system prompt, few-shot examples, temperature, repair strategy and model choice. Evolving those against a fixed, scored task set is a known, testable technique (the prior-art map in backlog R1 should confirm the names before any public claim).

## Phases

Each phase is a ticket in this work effort. A phase is done when its check passes, not when code exists.

- **P0 Stabilize** (backlog A1 to A3, A6, A18, B1 to B3, C1, C10, E16, E7; and switch the 31 files that import `src.waft` to `waft`). Done when: the full suite runs in CI, a wheel installs and `waft --help` works in a clean venv, ruff F821 is clean, the handshake no longer hands out the token, and the fixable vulnerable packages are upgraded.
- **P1 The honest loop** (F2, F3, F19, R5). Port the gym and the lab loop into the package, record each run in a Logbook, write to the project directory only. Done when: `waft lab run --seed 7` twice gives the same head hash, a different seed gives a different one, ids are unique, best fitness never regresses, and the old `evolve` path is gone or aliased.
- **P2 Real agents** (F3, R2, R3). Add the agent protocol, a local HTTP provider, hosted providers behind an explicit flag, a fallback chain, a call and cost budget, and a recorded fake for tests. Done when: the same run works with the mock and with a local model, every model call is a Logbook record, and tests never touch the network.
- **P3 Real tasks** (I10, R2). Add the planted-defect repository family. Done when: an agent's gym fitness and its recall on planted defects are both measured on the same genomes, and the correlation (or its absence) is written down.
- **P4 One surface** (F13, R8, G3). One read-only report built from the Logbook (FogSift's `render.py` already turns a chain into a page), linked from the README; the README's claims table filled from real runs. Done when: every number on the page is a tally of chain records.
- **P5 Trim** (D1, D2, D10, H1). Move the parked products out of the core (own repos or an archive branch), untrack `node_modules` and generated PDFs. Done when: CT has decided each folder and the core package has only what P0 to P4 need.

## Reuse map

How to read it. **Checked** means I ran it or read the lines myself in this session; **survey** means a read-only helper agent read it and I confirmed only what is named (sizes, a test run). Licences: WAFT is public MIT. `_workbench`, `tavern-keeper-bot`, `johnnyautoseed-research`, `johnnyautoseed`, `thecoffeejesus` and `folktech-io` are private; `CivicOS` is public MIT; `Lantern`, `survivingthesingularity` and `relaxation_station` are public with no licence (GitHub metadata, 2026-11-14). All are CT's, so CT can relicense; copying private code into WAFT publishes it (decision D1).

### Tier 1: the core loop (phases P1 and P2)

| Candidate | From | Size | Evidence | How to use it | Ticket |
|---|---|---|---|---|---|
| Gym: quests, validator, scint detector, repair loop, fitness | `waft/src/gym/rpg` | 1,252 lines | checked: 5 tests pass; runs inside the lab loop | move into `waft.gym`; package it; fix the tracing imports it depends on (backlog A1, A3) | P1.1 |
| Lab loop: genome, content-hash ids, per-call deterministic RNG, mutation, elitist selection, flight recorder, doctor | `_workbench/fogsift-system/checks/waft_lab.py` | 308 lines | checked: ran here; 0.88 to 0.95 in 5 generations, 0.88 to 1.00 by generation 9 of 15; same seed same artefact | port into `waft.lab`; `waft evolve` calls it | P1.2 |
| Logbook: hash-chained run record, checks, controls, balances, verify with an expected head | `_workbench/fogsift-system/fogsift_api/custody.py` and `schemas.py` | 730 and 149 lines, standard library | checked: 108 tests, 1 unrelated failure; a 40-line probe recorded two lab runs, decided "pass" and verified | vendor as `waft.record`, or depend on it (D1) | P1.3 |
| Planted-defect repository fixture with independent ground truth | `_workbench/fogsift-system/fogsift_api/fixture.py` | 106 lines | checked: read; it backs FogSift's closed loop | template for task family 2: agents fix planted defects; score recall and precision | P3.2 |
| Multi-provider model client: ordered OpenAI-compatible endpoints, cooldowns by status (429 honours Retry-After), JSON-mode retry, failover on empty replies, no key leakage | `tavern-keeper-bot/llm.js` | 195 lines | checked: the repo's 120 tests pass here in 11.6 s (25 of them for this client) | port to Python on httpx (already a WAFT dependency) with an injectable clock and transport; return token usage for cost-aware fitness; llama.cpp and Ollama become base URLs | P2.2, P2.3 |
| Loose JSON parser for model output (plain, fenced or wrapped in prose) | `tavern-keeper-bot/llm.js` lines 60 to 79 | about 20 lines | survey: 3 passing tests | port; extend to arrays | P2.1 |
| Scripted fake OpenAI-compatible server that records every call | `tavern-keeper-bot/test/helpers/bot.js` | about 35 lines | survey: 50 tests run against it | port as a pytest fixture on port 0; pick replies by prompt pattern so runs are reproducible | P2.4 |
| End-to-end harness: real entrypoint, env reset from `.env.example`, network lockdown | `tavern-keeper-bot/test/helpers/bot.js` and `test/bot.test.js` | 165 and 493 lines | survey: 25 passing tests | reuse the pattern in `conftest.py` (block non-loopback sockets) | P2.4 |
| Consistency tests: env vars read vs `.env.example`, Dockerfile copies vs modules, every command has help | `tavern-keeper-bot/test/consistency.test.js` | 91 lines, 7 tests | survey: pass | rewrite in pytest with `ast` | P0.3 |
| Per-key rate limiter with injectable clock | `tavern-keeper-bot/util.js` lines 149 to 165 | about 17 lines | survey: 7 passing tests | port as a FastAPI dependency and a model-call budget | P2.3 |
| Outbound gate for URLs (blocks private ranges and the cloud metadata address) | `waft/src/waft/core/door_guy.py` | 260 lines | checked: its tests pass | route every provider call through it | P2.2 |

### Tier 2: checks and hygiene (phase P0, and P4 for docs)

| Candidate | From | Size | Evidence | How to use it | Ticket |
|---|---|---|---|---|---|
| Build guard: test exactly the committed tree, write "what this proves" to the step summary | `survivingthesingularity/.github/workflows/build-guard.yml` | 94 lines | checked: size; survey: live workflow | pattern for WAFT CI: whole suite, wheel smoke test, docs checks | P0.3 |
| Secret scan job with reasons for every ignore | `johnnyautoseed/.github/workflows/security-baseline.yml` | gitleaks job about 15 lines | survey: live workflow | copy; use path or regex allowlists instead of line pins (they break when lines move); add pip-audit | P0.3 |
| Dependabot config | `johnnyautoseed/.github/dependabot.yml` | 17 lines | survey | copy for pip and GitHub Actions | P0.5 |
| Copy-rule engine: rule id, "why" text, context window, negation, fixtures; dash rules written with escapes | `johnnyautoseed/scripts/check-plan-copy.mjs` plus `tests/copy-guard.test.mjs` | 557 and 143 lines | survey (the engine file could not be opened here: a privacy guard blocks files that hold the account email); test file size checked | port the engine to Python (about 150 lines) with WAFT's own rules: no em or en dashes, no unmeasured "evolving" claims, no retired command names | P4.2 |
| Voice audit: rule table of hype words and dashes over visible text | `thecoffeejesus/scripts/voice_audit.py` | 145 lines, Python | checked: size; survey: no tests, always exits 0 | copy and adapt: Markdown input, exit code, baseline | P4.2 |
| Generator with `--check` mode | `thecoffeejesus/scripts/gen_sitemap.py` | 123 lines | checked: size | the shape for a generated `docs/CLI.md` from the Typer tree, so docs cannot name commands that do not exist (backlog G2) | P4.2 |
| Ratchet for a check landed on a repo with known breaks | `johnnyautoseed/scripts/check-links.mjs` | 224 lines | survey | the idea: commit today's 147 broken links as a baseline, fail only on new ones | P0.3 |
| Negative controls for every guard | `survivingthesingularity/scripts/check-factcheck-*.py`, `docs/release-gates-2026-10-10/negative-controls.json` | 143, 191, 77 lines | survey | each new WAFT check gets a planted-defect test, the same idea as the Logbook's controls | P0.3 |
| Claim verdicts (SUPPORTED, PARTIAL, UNSUPPORTED, UNCHECKED, UNCHECKABLE, CONTRADICTED) and a "not covered" list | `survivingthesingularity/FACTCHECK.md` and the factcheck block of `scripts/sts.py` | 248 lines; about 690 lines of code | survey (sts.py could not be opened here, same guard) | reuse the vocabulary for the README claims table; "breeds agents" stays UNCHECKABLE until a Logbook run backs it | P4.2 |
| Git receipt: file state origin_exact, local_only or uncommitted | `sts.py` `_fc_git_state` | about 80 lines | survey | release check that refuses unpushed or dirty content | P0.2 |
| Release ledger pattern: versions, hashes, refuses to overwrite | `survivingthesingularity/RELEASES.md`, `docs/v0.11.0/finalize.py` | 286 and 182 lines | survey | pattern for WAFT's release steps (backlog B9) | P0.2 |
| Network link verifier with cache and soft-404 detection | `survivingthesingularity/scripts/factcheck_network.py` | 413 lines, standard library | checked: size | scheduled job for external links in docs | P4.2 |
| Scheduled failure opens or updates one issue | `johnnyautoseed/.github/workflows/inquiry-check.yml` lines 96 to 149 | about 50 lines | survey | for the weekly health run (backlog L7) and a scheduled benchmark run | P4.1 |
| Post-build site audit: dead links, missing metadata, "smell" strings | `folktech-io/scripts/audit-outreach.py` | 167 lines, Python | survey | adapt for any HTML WAFT generates | P4.1 |

### Tier 3: later or optional

| Candidate | From | Size | Evidence | Possible use |
|---|---|---|---|---|
| Nova Process: unpack, three expert lenses, synthesize; pure and deterministic | `CivicOS/src/apps/nova/novaProcess.js` | 325 lines, MIT | checked: no `Date` or `Math.random`, exports read; survey found two defects (actions cut at 6 drop the third lens; `required?` misses "requirements") | a rule-based baseline agent and a third task family (problem decomposition scored against labelled facets); port about 200 lines |
| Replay of a precomputed run as an animated timeline | `CivicOS/src/apps/NovaSystemApp.jsx` | 401 lines | survey | the P4 view: replay a Logbook's events; sprite licences need checking |
| Versioned event envelope, storage adapter with a memory backend, event viewer | `CivicOS/src/kernel/events.js`, `storage.js` | 43 and 107 lines | checked: sizes | already covered by the Logbook; keep as a UI pattern |
| App registry with per-front-end health checks | `CivicOS/src/views/OpsCenterView.jsx`, `scripts/check-5050-namespaces.mjs` | 154 and 37 lines | survey | inventory for the seven front ends while backlog F13 is decided |
| OpenAlex and arXiv fetchers, deterministic research metrics | `johnnyautoseed-research/research/sources/openalex.py`, `arxiv.py`, `research/metrics.py` | 227, 86, 135 lines | checked: sizes; survey: no tests | only if WAFT keeps research ingestion: split fetch from parse, test against saved fixtures |
| Deterministic pass first, bounded model enrichment second | `Lantern/dashboard/app.js` `extractLocations` | about 100 lines | survey | the rule for fitness: measured checks own the score, a model judge only adds bounded signal |
| Agent exchange ledger with a human promotion gate | `Lantern/exchange/server.js` | 292 lines | survey: no auth, no locking | the idea of a human gate before a variant is promoted; rebuild, do not copy |
| Guide content model, callouts, one-source build outputs | `folktech-io/src/content.config.ts`, `src/lib/remark-callouts.ts` | 126 and 80 lines | survey: CI build passes | if WAFT gets a docs site |
| Decision log and per-experiment folder template | `relaxation_station/docs/decisions.md`, `episodes/_template/` | 105 lines; 3 files | survey | record why a variant was selected; keep plan, run and measured result apart |

### From `_pyrite` and the rest of `_workbench`

| Candidate | From | Size | Evidence | How to use it | Ticket |
|---|---|---|---|---|---|
| Work effort and ticket CLI (`we`, `ticket`: create, list, sync, close; close refuses while tickets are open) | `_pyrite/tools/work-effort/create.py`, `tools/ticket/create.py` | 478 and 230 lines, standard library, MIT | checked: its self-checks pass here (25 and 57 checks); this session's two work efforts were made with it | keep using it as an external tool on `_work_efforts` (backlog I1, I11); do not vendor it | P5.1 |
| Johnny Decimal to work-effort migrator (dry run by default, backup, rollback) | `_pyrite/tools/work-effort-migrator/migrate.py` | 419 lines, 12 unit tests | survey: tests not run | run on a copy for WAFT's three Johnny Decimal folders | P5.1 |
| Markdown and wikilink linter, read-only check mode proven by a fixture hash | `_pyrite/tools/obsidian-linter/` | about 2,900 lines in 7 scripts | checked: `verify_readonly.py` passes (5 checks) | run `--check` over the 3,680 Markdown files; fix on a branch only | P4.2 |
| Clean-install validation idea: fresh clone, deleted venv, run from another directory | `_pyrite/tools/scaffold_new_project.py` (about lines 318 to 690) | part of 1,009 lines | survey: self-reported passes; it edits the checkout, so take the idea, not the code | a CI job that installs the wheel outside the checkout and runs `waft --help` from a temp directory | P0.2 |
| Negative-control rule for every test suite | `_pyrite/tools/work-effort/verify.py` docstring; `docs/OPERATING-PROMPT.md` | 166 and 180 lines | survey | fitness tests need a known-bad variant that must score lower and a no-op that must score zero | P1.4 |
| Determinism check: same inputs in order, shuffled, repeated and in a fresh process; hashes must match; at least k distinct outputs | `_workbench/snowy-bridge/scripts/check-determinism.js` | 207 lines | checked: size; survey: tested, including a planted leak | port the idea to pytest for lab runs; the distinct-output rule catches a constant fitness | P1.4 |
| Forbidden-pattern scan (wall clocks, unseeded randomness, dashes) | `_workbench/snowy-bridge/scripts/check-forbidden.js` | 258 lines | checked: size; survey: tested | port as an `ast` check over `waft.lab` and `waft.gym`, so randomness and time must be injected | P1.4 |
| Fail-closed scoring (NaN, infinite or missing scores rank worst; an empty set fails) | `_workbench/snowy-bridge/scripts/check-cameras.js` around line 70 | about 20 lines of logic | survey: tested | apply in selection so a broken evaluation can never win | P1.2 |
| Lensed judges with a fixed JSON schema, a synthesizer and a critic | `_workbench/.claude/skills/revision-loop/` (SKILL.md and references) | about 700 lines of prompts | survey: used in practice, no code | a later, secondary judge layer; executed task results stay primary | P3.3 |
| Ledger location spec: env var, then flag, then git root, never the package directory | `_workbench/_work_efforts/WE-261025-eo0i_make_pyrite_portable_across_repos/` | 4 tickets | survey: proposal | the same resolution order fixes WAFT's writes into the checkout (backlog F19) | P1.3 |

Not worth reusing here: pyrite's own tracer (WAFT's is larger), `tools/nova-process/orchestrate.py` (its model call is a TODO), the console and dashboard MCP servers (broken or listening on all interfaces without auth), the work-efforts MCP server (old SDK), and the site, video and media builders in `_workbench`.

### Not worth reusing

- The big single files: `survivingthesingularity/scripts/sts.py` (6,264 lines, with a duplicated factcheck block), `tavern-keeper-bot/index.js` (Discord-specific), `johnnyautoseed-research/server.py` (2,337 lines, mostly inline HTML), `johnnyautoseed-research/biocomposite_researcher.py`. Lift single functions only.
- Site-specific guards: the Cloudflare, Stripe, Supabase and CSP scripts in `johnnyautoseed` and `survivingthesingularity`. A pytest that checks FastAPI's response headers is cheaper.
- Lantern's shell pipeline (macOS paths, prompts pasted into JSON by string editing) and its Firecrawl client (heavy, online only).
- CivicOS's desktop shell, Builder, Vault, Plaza and the vendored games (some GPL): civic product code, and adopting it would add an eighth front end.
- The whole folktech-io site (Supabase forms, brand assets): take the content model only.

## Decisions for CT

- **D1. Licence and reuse.** The best pieces live in private, unlicensed repos (`_workbench`, `tavern-keeper-bot`) or in public repos with no licence. Copying them into WAFT publishes them under MIT. Options: (a) copy, with the source and commit noted in `CREDITS.md`; (b) keep FogSift's Logbook in `_workbench` and make it an optional dependency; (c) port the ideas and write new code. My lean: (a) for `waft_lab.py`, `custody.py` with `schemas.py`, and `fixture.py`, because they were written to test WAFT; (c) for the bot's client and test harness, because the Python port is new code anyway.
- **D2. What the core is.** My lean: the core is gym, lab, agents and record (P1 to P3) plus the CLI and a read-only API. Games, lore, desktop apps, the PDF library and the other front ends move out or are marked experimental (P5, backlog D10 and H1).
- **D3. Model budget.** P2 can run entirely on a local model or the deterministic mock. Hosted models need a monthly ceiling, which the client's call budget enforces.

## Record of this pass

1. Ran FogSift's WAFT lab doctor and a 15-generation run with this repo's venv, ran FogSift's test suite, and wrote a scratch probe that records lab runs in a Logbook.
2. Read the gym (`src/gym/rpg`), the lab loop, the Logbook's interface and examples, the fixture, and WAFT's own `door_guy.py`, auth and Ollama-compatible route.
3. Sent four read-only helper agents through the other eleven repos (CivicOS with folktech-io and relaxation_station; tavern-keeper-bot with Lantern and johnnyautoseed-research; survivingthesingularity with johnnyautoseed and thecoffeejesus; `_pyrite` with the rest of `_workbench`). I reran or reread the claims the map depends on: the tavern-keeper-bot suite, three pyrite self-checks, the CivicOS Nova Process exports and its lack of clocks and randomness, and file sizes. Two files (`sts.py`, `check-plan-copy.mjs`) could not be opened here because a privacy guard blocks files that hold the account email; those rows are marked survey only.
4. Checked repository visibility and licences through the GitHub API.
5. Created this work effort with `fogsift.py we create`, which drives `_pyrite`.

Every repo's working tree was clean afterwards.

## Caveats

- Rows marked "survey" rest on a helper agent's reading. Sizes and the named test runs were checked; the rest was not.
- The lab loop's agent is a mock whose genome is three probabilities. With a real model the genome becomes a configuration (prompt, examples, temperature, repair strategy, model), and nothing here shows yet that evolving it beats picking a good configuration by hand. P3.3 is where that gets measured.
- Prior-art names (Promptbreeder, EvoPrompt and similar, backlog R1) come from memory and must be checked before any public claim.
