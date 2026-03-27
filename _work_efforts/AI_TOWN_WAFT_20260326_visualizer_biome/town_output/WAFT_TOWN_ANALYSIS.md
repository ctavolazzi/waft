# WAFT — AI Town collective analysis  
**Date:** 2026-03-26  
**Target:** Repository **waft** (visualizer + FastAPI + biome experiment).  
**Paper:** *Not supplied* — substituted with **session narrative** (auth/proxy, bridge endpoint, renderer stability, diorama visuals).

---

## Executive summary (Being_005 — synthesis)

WAFT’s visualizer stack is now **operationally coherent**: Python resolves under pyenv, the API can serve auth and a biome bridge, and the biome view avoids the worst class of rendering failure (mixed GPU contexts on one canvas). The remaining **highest-leverage** work is **frontend hygiene** (Svelte route props) and **semantic depth** (biome as a metaphor for live WAFT state, not only shaders).

---

## Architecture & boundaries (Being_001)

**What changed structurally**

- **API surface** gained `GET /api/biome` as a minimal polling contract for the visualizer bridge.
- **Visualizer** proxies `/api` to `localhost:8000`, so “500 on handshake” often traces to **upstream absence** or **Python shim mismatch** rather than Axios itself.
- **Biome renderer** intentionally **collapsed to WebGL** in `createBiomeEngine` to prevent dev hot-reload from creating irreconcilable canvas contexts.

**Boundary risks**

- Stub `export let params` on many routes trades one warning for another (`unused export property 'params'`). The **correct** fix is SvelteKit-native data flow (`+page.ts` / `$page.params`) rather than universal prop stubs.
- Biome “diorama” geometry increased scene complexity; watch **dispose paths** on hot navigation and terrain resize.

---

## Algorithms & graphics runtime (Being_002)

**Proven failure mode:** `WebGLRenderer` on a canvas that already holds a **different context type** (e.g., after WebGPU probing).  
**Mitigation in tree:** force `BiomeEngine` path for now.

**Residual graphics risks**

- Caustics + custom seabed shader path: sensitive to render-target setup; validate on integrated GPUs.
- Long-term: if WebGPU returns, use **fresh canvas element** per engine switch or explicit `loseContext`/teardown policy.

---

## “Paper” / claims review (Being_003 — replaces absent PDF)

**Claim:** “Handshake 500 fixed.”  
**Status:** **Conditionally true.** Evidence supports fixing **pyenv `.python-version` mismatch** as a dominant local failure mode; production 500s still need per-trace review.

**Claim:** “Biome bridge 404 fixed.”  
**Status:** **True in code** (`/api/biome` route + router include) *given API is running*.

**Claim:** “Diorama looks ‘full formed’.”  
**Status:** **Aspirational** — framing, base, rails, fog/sky defaults help; **prop/instancing storytelling** still needed for “what we’re working on” legibility.

---

## WAFT integration opportunities (Being_004)

| Opportunity | Why it matters |
|-------------|----------------|
| Map **work efforts** → biome props (clusters, color, motion) | Makes the scene *mean* something in Johnny Decimal space |
| Stream **Oracle / Empirica** status into `events[]` in biome payload | Connects cognitive stack to the metaphor |
| Typed `BiomeServerPayload` versions | Avoids silent JSON drift between poll and UI |

---

## Documentation & handoff (Being_005)

**Artifacts**

- Checkpoint: `_work_efforts/CHECKPOINT_2026-03-26_biome_visualizer_auth_stability.md`
- This town output: this file

**Recommended README touchpoints** (future, if you want public docs)

- “Run API + visualizer” two-terminal flow
- “If handshake fails, check `.python-version` and `python --version`”

---

## Town vote outcome

- **Primary deliverable:** **Single consolidated document** (`single_pdf` spirit) — this file.
- **Next engineering votes:** (1) clean `params` pattern, (2) deepen `/api/biome` schema.

---

## Genetic lineage (procedural note)

Lineage here is **documentation lineage**: each Being is a role label over the same analysis pass, not separate spawned runtime entities.

---

*End of town analysis.*
