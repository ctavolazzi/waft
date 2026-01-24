# /prove-it-in-court - Try a Claim Before the Tribunal

**Initiates a formal Court proceeding where a Claim is tried before the Tribunal, with Beings assigned as Prosecutor, Defender, Witnesses, and Jury.**

Opens a FastAPI+SvelteKit UI in Chrome to watch the WAFT system literally "Hold Court" with all the trappings - Discovery, Housekeeping, Trial, and Verdict.

**Use when:** You need to formally prove or disprove a claim, want to see evidence evaluated systematically, or need a verdict recorded in the Chain of Case Law.

---

## Purpose

This command provides:
- **Formal Court Proceedings** - Structured trial with phases
- **Role Assignment** - Beings assigned as Prosecutor, Defender, Witnesses, Jury
- **Real-Time UI** - Watch court proceedings in Chrome
- **Evidence Discovery** - Systematic gathering and organization
- **Verdict Recording** - Results stored in Chain of Case Law
- **Inter-Realm Communication** - Evidence requested from other Realms via "The Beyond"

---

## Philosophy

### "On Trial" Has Meaning

In the WAFT system, putting something "On Trial" means:

1. **Formal Process** - Not casual verification, but structured proceedings
2. **Adversarial Testing** - Prosecutor proves, Defender challenges
3. **Evidence-Based** - Only admitted evidence considered
4. **Recorded Precedent** - Verdicts become Case Law
5. **Visible Justice** - Proceedings are observable

### The Tribunal

The Tribunal is a Realm (Port 8100) where:
- **Prime Justice** - The Supreme Being who governs proceedings
- **The Beyond** - Inter-Realm communication (only Prime Beings know)
- **Court Roles** - Beings assigned specific functions
- **Chain of Case Law** - Hash-verified ledger of verdicts

---

## Court Phases

### Phase 1: FILING
```
Case filed with the Court
- Claim statement recorded
- Case ID assigned
- Docket entry created
```

### Phase 2: DISCOVERY
```
Evidence gathered systematically
- Search existing case files
- Request evidence from other Realms via The Beyond
- Organize all relevant materials
```

### Phase 3: HOUSEKEEPING
```
Files organized, docket prepared
- All evidence catalogued
- Witnesses identified
- Schedule set
```

### Phase 4: ASSIGNMENT
```
Roles assigned to Beings
- Prosecutor: Proves the claim
- Defender: Challenges the claim
- Witnesses: Provide testimony
- Jury: Deliberate and recommend
```

### Phase 5: OPENING
```
Opening statements
- Prosecutor states the case
- Defender previews the defense
```

### Phase 6: PRESENTATION
```
Evidence presented
- Exhibits entered into record
- Evidence examined
```

### Phase 7: EXAMINATION
```
Witnesses examined
- Direct examination
- Cross-examination
- Expert testimony
```

### Phase 8: DELIBERATION
```
Jury deliberates
- Review evidence
- Discuss findings
- Form recommendation
```

### Phase 9: VERDICT
```
Prime Justice renders verdict
- PROVEN / DISPROVEN / INCONCLUSIVE
- Confidence level
- Reasoning documented
```

### Phase 10: RECORDING
```
Verdict recorded in Chain of Case Law
- Hash calculated
- Linked to previous entry
- Precedent established
```

---

## Usage

### Basic Usage
```
/prove-it-in-court "The refactoring improved code quality by 40%"
```

Initiates court proceedings to try the claim.

### With Evidence Reference
```
/prove-it-in-court "The API is backwards compatible" --evidence case_20260121_080648
```

Uses existing case file as evidence.

### With Specific Realm
```
/prove-it-in-court "Security vulnerability patched" --realm security_realm
```

Requests evidence from specific Realm via The Beyond.

### Quick Mode (No UI)
```
/prove-it-in-court "Performance improved 50%" --quick
```

Runs proceedings without opening UI.

---

## Execution Steps

### Step 1: Start Tribunal Realm

```bash
# Starts PocketBase on port 8100
waft realm start tribunal_realm --port 8100
```

### Step 2: File the Case

```python
# Case filed with the Court
case = CourtCase(
    case_id=f"case_{timestamp}",
    claim=user_claim,
    filed_by="user",
    status="filed"
)
```

### Step 3: Discovery Phase

```python
# Gather evidence
evidence = []

# Search existing case files
existing = magistrate.search_precedents(claim_keywords)
evidence.extend(existing)

# Request from other Realms via The Beyond
if needs_external_evidence:
    beyond_evidence = prime_justice.request_from_beyond(
        "library_realm",
        {"action": "search", "query": claim}
    )
    evidence.extend(beyond_evidence)
```

### Step 4: Assemble Court

```bash
# Use /assemble-a-team to create court crew
/assemble-a-team --type court --case {case_id}
```

### Step 5: Open UI

```bash
# Start FastAPI backend
uvicorn tribunal.api.main:app --port 8100

# Open SvelteKit frontend
open http://localhost:5173/sessions/{session_id}
```

### Step 6: Conduct Proceedings

The UI shows live proceedings:
- Court room visualization
- Transcript as it happens
- Evidence on display
- Phase indicator
- Participants and roles

### Step 7: Record Verdict

```python
# Verdict recorded in Chain of Case Law
entry = CaseLawEntry(
    case_id=case.case_id,
    verdict=verdict,
    previous_hash=ledger.last_hash,
)
entry.entry_hash = entry.calculate_hash()
ledger.add(entry)
```

---

## Output

After proceedings complete:

1. **Verdict**: PROVEN / DISPROVEN / INCONCLUSIVE
2. **Confidence**: Percentage confidence in verdict
3. **Reasoning**: Documented reasoning
4. **Case Law Entry**: Hash-verified entry in Chain
5. **Transcript**: Complete record of proceedings
6. **PDF Documents**: Court documents generated

---

## The Beyond

### What Beings Know

**Regular Beings**: Information arrives "from The Beyond" - the source is unknowable
**Prime Beings**: Know about inter-Realm communication but don't reveal it

### Example Flow

```
Tribunal Realm (8100) → requests evidence
        ↓
    The Beyond (internal)
        ↓
Library Realm (8091) → provides evidence
        ↓
    The Beyond (internal)
        ↓
Tribunal Realm (8100) ← receives "from The Beyond"
```

### API Endpoint

```python
# POST /api/beyond
# Only Prime Beings can invoke this
@router.post("/beyond")
async def beyond_request(request: BeyondRequest) -> BeyondResponse:
    """Handle requests from/to The Beyond."""
    pass
```

---

## Integration

### With Magistrate (Pantheon)
- Case files organized by Magistrate
- Precedents searched via Magistrate
- Verdicts become Magistrate's Body of Proof

### With Flight Recorder
- Court events logged as evolutionary events
- CASE_FILED, VERDICT_RENDERED, etc.

### With Empirica
- Epistemic tracking of court knowledge
- Preflight/Postflight for each phase

### With PDF Templates
- Case Brief template for filed cases
- Transcript template for proceedings
- Verdict template for outcomes

---

## UI Features

### Court Room View
```
┌─────────────────────────────────────────────────┐
│                  PRIME JUSTICE                   │
│                    [Bench]                       │
├──────────────────┬──────────────────────────────┤
│   PROSECUTOR     │         DEFENDER              │
│   [Podium]       │         [Podium]              │
├──────────────────┴──────────────────────────────┤
│              WITNESS STAND                       │
├─────────────────────────────────────────────────┤
│     JURY BOX                                     │
│   [Member 1] [Member 2] [Member 3]              │
├─────────────────────────────────────────────────┤
│                  GALLERY                         │
│            [Observers/Evidence]                  │
└─────────────────────────────────────────────────┘
```

### Live Transcript
```
[09:15:23] PRIME JUSTICE: Court is now in session.
[09:15:30] PROSECUTOR: Your Honor, the evidence shows...
[09:16:45] DEFENDER: Objection! Hearsay.
[09:16:48] PRIME JUSTICE: Sustained.
[09:17:10] PROSECUTOR: I'll rephrase...
```

### Phase Indicator
```
[FILING] → [DISCOVERY] → [HOUSEKEEPING] → [ASSIGNMENT] 
    → [OPENING] → [PRESENTATION] → [EXAMINATION] 
    → [DELIBERATION] → [VERDICT] → [RECORDING]
                            ↑
                       YOU ARE HERE
```

---

## When to Use

**Use `/prove-it-in-court` when**:
- ✅ Need formal proof of a claim
- ✅ Want adversarial testing of an assertion
- ✅ Need verdict recorded as precedent
- ✅ Want to watch proceedings in real-time
- ✅ Need multiple perspectives on evidence

**Don't use `/prove-it-in-court` when**:
- ❌ Quick verification needed (use `/verify`)
- ❌ Just need case file (use `/case-file`)
- ❌ Informal investigation (use `/prove-it`)

---

## Related Commands

- **`/prove-it`** - Scientific method proof (less formal)
- **`/case-file`** - Generate case file from evidence
- **`/verify`** - Lightweight verification
- **`/assemble-a-team`** - Create crew for court
- **`/evolve-template`** - Evolve court document templates

---

## Requirements

### Backend
- FastAPI server for court API
- PocketBase for Tribunal Realm (port 8100)
- Connection to other Realms for The Beyond

### Frontend
- SvelteKit for real-time UI
- SSE for live transcript streaming
- Chrome browser for viewing

### Dependencies
- `crewai` for team assembly
- `httpx` for inter-Realm communication
- `waft` core for Beings and Realms

---

## Example Workflow

```
User: /prove-it-in-court "The Case File evolution successfully integrates with the Magistrate"

AI: 
📜 CASE FILED: case_20260121_091500_case_file_magistrate_integration

Starting Court Proceedings...

Phase 1: FILING ✓
- Case registered with Tribunal
- Docket entry: DOCKET-2026-0042

Phase 2: DISCOVERY
- Searching existing case files...
- Found: case_20260121_080648_gamified_service_mesh
- Requesting evidence from Library Realm via The Beyond...
- Evidence received from The Beyond

Phase 3: HOUSEKEEPING ✓
- 12 evidence items catalogued
- 3 witnesses identified
- Schedule set: 09:30 - 10:30

Phase 4: ASSIGNMENT ✓
- Prosecutor: being_prosecutor_001
- Defender: being_defender_001
- Witnesses: being_witness_technical, being_witness_process
- Jury: being_jury_001, being_jury_002, being_jury_003

🖥️ Opening Court UI in Chrome...
→ http://localhost:5173/sessions/session_20260121_091500

[Watch live proceedings in browser]

...

Phase 9: VERDICT
┌─────────────────────────────────────────────────┐
│              ⚖️ VERDICT: PROVEN                 │
│           Confidence: 92%                        │
│                                                  │
│ Reasoning: The design document demonstrates     │
│ clear integration points with the Magistrate.   │
│ Evidence shows parsing, indexing, and query     │
│ capabilities aligned with Magistrate's existing │
│ methods.                                         │
└─────────────────────────────────────────────────┘

Phase 10: RECORDING ✓
- Entry added to Chain of Case Law
- Hash: a1b2c3d4e5f6g7h8...
- Precedent established

📋 Court documents generated:
- _work_efforts/proof_cases/case_20260121_091500_case_file_magistrate_integration.md
- _work_efforts/proof_cases/transcripts/transcript_20260121_091500.pdf
- _work_efforts/proof_cases/verdicts/verdict_20260121_091500.pdf

Court is adjourned.
```

---

**"On Trial" has meaning. Prove it in Court.**

--- End Command ---
