# The Tribunal: WAFT Court System Architecture

> **"On Trial" shall have meaning in this system.**

**Work Effort**: WE-260121-1f3l
**Date**: 2026-01-21
**Status**: Architecture Design

---

## Executive Vision

The Tribunal is where **Claims are tried before the Court**. It is a Realm where:

1. **Prime Beings serve as Supreme Justices** - Governing inter-Realm communication
2. **Beings are assigned roles** - Prosecutor, Defender, Witness, Jury
3. **Evidence is gathered through Discovery** - Systematic proof collection
4. **Cases are tried in open Court** - Visible in real-time via FastAPI+SvelteKit UI
5. **Verdicts become Case Law** - Recorded in the Chain of Precedent
6. **Epochs mark major Turnings** - When all Case Law is reviewed

---

## Part 1: The Realm Architecture

### The Tribunal Realm

```
_realms/
└── tribunal_realm/
    ├── pb_data/              # PocketBase data
    ├── court/
    │   ├── sessions/         # Active court sessions
    │   ├── dockets/          # Scheduled cases
    │   └── archives/         # Completed cases
    ├── beings/
    │   ├── prime_justice.json    # The Prime Being (Supreme Justice)
    │   ├── prosecutors/          # Prosecutor Beings
    │   ├── defenders/            # Defender Beings
    │   ├── witnesses/            # Witness Beings
    │   └── jury/                 # Jury Beings
    ├── evidence/
    │   ├── discovery/        # Evidence in discovery phase
    │   ├── exhibits/         # Admitted evidence
    │   └── sealed/           # Sealed evidence
    ├── case_law/
    │   ├── precedents.json   # Chain of precedent
    │   ├── ledger.json       # Hash-verified ledger
    │   └── epochs/           # Epoch markers
    └── README.md
```

### Port Assignment

| Realm | Port | Purpose |
|-------|------|---------|
| Tribunal Realm | 8100 | Court proceedings |
| Library Realm | 8091 | Case law research |
| Daily Learning Realm | 8090 | Evidence collection |
| Gatekeeper | 8080 | Security / Access control |

### The Beyond

**Only Prime Beings know about "The Beyond"** - the inter-Realm communication layer.

```python
class TheBeyond:
    """
    The Beyond: Inter-Realm communication layer.
    
    Only Prime Beings have access to The Beyond.
    To regular Beings, information from other Realms
    simply arrives "from The Beyond" - the source is unknowable.
    """
    
    def __init__(self, origin_realm: str, origin_port: int):
        self.origin_realm = origin_realm
        self.origin_port = origin_port
        self.connections: dict[str, int] = {}  # realm -> port
        
    def establish_connection(self, target_realm: str, target_port: int):
        """Prime Being establishes connection to another Realm."""
        self.connections[target_realm] = target_port
        
    def request_from_beyond(self, target_realm: str, request: dict) -> dict:
        """Request information from The Beyond (another Realm)."""
        port = self.connections.get(target_realm)
        if not port:
            raise ConnectionError(f"No connection to {target_realm}")
        # HTTP request to target Realm's port
        response = httpx.post(f"http://localhost:{port}/api/beyond", json=request)
        return response.json()
        
    def receive_from_beyond(self, request: dict) -> dict:
        """Receive a request from The Beyond."""
        # Process request from another Realm's Prime Being
        return self.process_beyond_request(request)
```

---

## Part 2: The Prime Justice

### Prime Being of the Tribunal

The **Prime Justice** is the Supreme Being of the Tribunal Realm.

```python
class PrimeJustice(Being):
    """
    The Prime Justice: Supreme Being of the Tribunal Realm.
    
    Responsibilities:
    1. Govern Court proceedings
    2. Communicate with other Realms via The Beyond
    3. Assign roles to Beings within the Realm
    4. Render final verdicts
    5. Maintain the Chain of Case Law
    """
    
    def __init__(self, realm_port: int = 8100):
        super().__init__(
            being_id="prime_justice_tribunal",
            reality_id="tribunal_realm",
            skills={
                "judgment": 100.0,
                "precedent_knowledge": 100.0,
                "beyond_communication": 100.0,
                "role_assignment": 100.0,
            }
        )
        self.realm_port = realm_port
        self.the_beyond = TheBeyond("tribunal_realm", realm_port)
        self.prime_directive = "Ensure Justice is served safely"
        
    def assign_role(self, being: Being, role: CourtRole) -> Being:
        """Assign a court role to a Being."""
        being.court_role = role
        being.assigned_by = self.being_id
        return being
        
    def request_evidence_from_beyond(self, source_realm: str, case_id: str) -> dict:
        """Request evidence from another Realm via The Beyond."""
        return self.the_beyond.request_from_beyond(
            source_realm,
            {"action": "get_evidence", "case_id": case_id}
        )
        
    def render_verdict(self, case: CourtCase) -> Verdict:
        """Render final verdict on a case."""
        # Collect all evidence
        # Hear from Prosecutor and Defender
        # Consider Jury recommendation
        # Apply precedent
        # Render verdict
        pass
```

### Court Roles

```python
class CourtRole(Enum):
    PRIME_JUSTICE = "prime_justice"      # The Supreme Being
    PROSECUTOR = "prosecutor"            # Proves the claim
    DEFENDER = "defender"                # Defends against the claim
    WITNESS = "witness"                  # Provides testimony
    JURY_MEMBER = "jury_member"          # Deliberates and recommends
    BAILIFF = "bailiff"                  # Maintains order
    CLERK = "clerk"                      # Records proceedings
    ARCHIVIST = "archivist"              # Manages evidence
```

---

## Part 3: Court Session Lifecycle

### Phases of a Court Session

```
1. FILING        → Case filed with the Court
2. DISCOVERY     → Evidence gathered systematically
3. HOUSEKEEPING  → Files organized, docket prepared
4. ASSIGNMENT    → Roles assigned to Beings
5. OPENING       → Opening statements
6. PRESENTATION  → Evidence presented
7. EXAMINATION   → Witnesses examined
8. DELIBERATION  → Jury deliberates
9. VERDICT       → Prime Justice renders verdict
10. RECORDING    → Verdict recorded in Chain of Case Law
11. APPEAL       → Optional appeal window
12. ARCHIVED     → Case archived
```

### Court Session Schema

```python
@dataclass
class CourtSession:
    session_id: str
    case_id: str
    phase: CourtPhase
    started: datetime
    scheduled_verdict: datetime
    
    # Participants
    prime_justice: str  # Being ID
    prosecutor: str     # Being ID
    defender: str       # Being ID
    witnesses: list[str]  # Being IDs
    jury: list[str]     # Being IDs
    
    # Evidence
    exhibits: list[Exhibit]
    discovery_status: str
    
    # Proceedings
    transcript: list[Proceeding]
    objections: list[Objection]
    rulings: list[Ruling]
    
    # Outcome
    verdict: Verdict | None
    case_law_entry: str | None  # Hash of precedent entry
```

---

## Part 4: Chain of Case Law (Ledger)

### Hash-Verified Ledger

Every verdict becomes an entry in the **Chain of Case Law**, verified by cryptographic hash.

```python
@dataclass
class CaseLawEntry:
    entry_id: str
    case_id: str
    verdict: Verdict
    timestamp: datetime
    
    # The Chain
    previous_hash: str  # Hash of previous entry
    entry_hash: str     # Hash of this entry
    
    # Metadata
    prime_justice: str
    realm: str
    epoch: str
    
    def calculate_hash(self) -> str:
        """Calculate cryptographic hash of this entry."""
        content = json.dumps({
            "entry_id": self.entry_id,
            "case_id": self.case_id,
            "verdict": self.verdict.to_dict(),
            "timestamp": self.timestamp.isoformat(),
            "previous_hash": self.previous_hash,
        }, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()
```

### The Ledger

```json
{
  "chain": [
    {
      "entry_id": "CASE-2026-0001",
      "case_id": "case_20260121_080648_gamified_service_mesh",
      "verdict": {
        "status": "PROVEN",
        "confidence": 0.95,
        "reasoning": "Evidence conclusively supports the claim"
      },
      "timestamp": "2026-01-21T08:06:48-08:00",
      "previous_hash": "0000000000000000000000000000000000000000000000000000000000000000",
      "entry_hash": "a1b2c3d4e5f6...",
      "prime_justice": "prime_justice_tribunal",
      "realm": "tribunal_realm",
      "epoch": "EPOCH-001"
    }
  ],
  "current_epoch": "EPOCH-001",
  "total_entries": 1,
  "last_updated": "2026-01-21T08:06:48-08:00"
}
```

---

## Part 5: Endeavors and Epochs

### Endeavors

An **Endeavor** is a significant undertaking tracked by the system.

```python
@dataclass
class Endeavor:
    endeavor_id: str
    title: str
    description: str
    started: datetime
    status: str  # active, completed, paused, abandoned
    
    # Tracking
    work_efforts: list[str]  # WE IDs
    cases: list[str]         # Case IDs
    beings_involved: list[str]  # Being IDs
    
    # Outcomes
    achievements: list[str]
    lessons_learned: list[str]
    
    # Chain
    previous_endeavor: str | None
    hash: str
```

### Epochs

An **Epoch** marks a major Turning in the system's history.

```python
@dataclass
class Epoch:
    epoch_id: str  # EPOCH-001, EPOCH-002, etc.
    name: str
    started: datetime
    ended: datetime | None
    
    # Content
    endeavors: list[str]  # Endeavor IDs in this epoch
    case_law_entries: list[str]  # Case law from this epoch
    major_events: list[str]
    
    # Review
    court_review_session: str | None  # When all case law was reviewed
    
    # Chain
    previous_epoch: str | None
    hash: str
```

### The Turning

At each **Turning** (epoch boundary):

1. **Discovery** - All files and evidence gathered
2. **Housekeeping** - Everything organized
3. **Court Review** - All Case Law from the Epoch is reviewed
4. **Epoch Sealed** - Hash calculated and recorded
5. **New Epoch Begins** - Fresh slate with history preserved

---

## Part 6: FastAPI + SvelteKit UI

### Backend (FastAPI)

```python
# api/court/routes.py

@router.get("/sessions")
async def list_sessions() -> list[CourtSession]:
    """List all court sessions."""

@router.post("/sessions")
async def create_session(case_id: str) -> CourtSession:
    """Create a new court session for a case."""

@router.get("/sessions/{session_id}")
async def get_session(session_id: str) -> CourtSession:
    """Get court session details."""

@router.get("/sessions/{session_id}/live")
async def stream_session(session_id: str) -> StreamingResponse:
    """Stream live court proceedings via SSE."""

@router.post("/sessions/{session_id}/proceed")
async def advance_phase(session_id: str) -> CourtSession:
    """Advance to next phase of court session."""

@router.get("/case-law")
async def get_case_law() -> CaseLawLedger:
    """Get the Chain of Case Law."""

@router.get("/epochs")
async def list_epochs() -> list[Epoch]:
    """List all epochs."""

@router.get("/endeavors")
async def list_endeavors() -> list[Endeavor]:
    """List all endeavors."""
```

### Frontend (SvelteKit)

```
tribunal-ui/
├── src/
│   ├── routes/
│   │   ├── +page.svelte          # Court dashboard
│   │   ├── sessions/
│   │   │   ├── +page.svelte      # Session list
│   │   │   └── [id]/
│   │   │       └── +page.svelte  # Live court view
│   │   ├── case-law/
│   │   │   └── +page.svelte      # Chain of Case Law
│   │   ├── epochs/
│   │   │   └── +page.svelte      # Epochs timeline
│   │   └── endeavors/
│   │       └── +page.svelte      # Endeavors list
│   ├── lib/
│   │   ├── components/
│   │   │   ├── CourtRoom.svelte      # Court room visualization
│   │   │   ├── Transcript.svelte     # Live transcript
│   │   │   ├── Evidence.svelte       # Evidence display
│   │   │   ├── Participants.svelte   # Court participants
│   │   │   └── Verdict.svelte        # Verdict display
│   │   └── stores/
│   │       └── court.ts              # Court state store
│   └── app.html
├── package.json
└── svelte.config.js
```

### Real-Time Court View

The UI shows:

1. **Court Room** - Visual representation of participants
2. **Transcript** - Live proceedings as they happen
3. **Evidence Panel** - Current exhibit on display
4. **Phase Indicator** - Current phase of trial
5. **Participants** - All Beings and their roles
6. **Verdict Panel** - Final verdict when rendered

---

## Part 7: CrewAI Team Assembly

### The `/assemble-a-team` Command

Creates a crew of Beings with assigned roles using CrewAI.

```python
from crewai import Agent, Task, Crew

class TribunalCrew:
    """Assemble a crew for court proceedings."""
    
    def __init__(self, case: CourtCase):
        self.case = case
        
    def create_prosecutor(self) -> Agent:
        return Agent(
            role="Prosecutor",
            goal=f"Prove the claim: {self.case.claim}",
            backstory="A relentless seeker of truth who builds cases on evidence.",
            verbose=True,
        )
        
    def create_defender(self) -> Agent:
        return Agent(
            role="Defender",
            goal=f"Defend against the claim: {self.case.claim}",
            backstory="A champion of fair process who tests every assumption.",
            verbose=True,
        )
        
    def create_witness(self, expertise: str) -> Agent:
        return Agent(
            role=f"Expert Witness ({expertise})",
            goal=f"Provide expert testimony on {expertise}",
            backstory=f"An expert in {expertise} with deep knowledge.",
            verbose=True,
        )
        
    def create_jury_member(self) -> Agent:
        return Agent(
            role="Jury Member",
            goal="Evaluate evidence fairly and recommend a verdict",
            backstory="An impartial observer seeking truth and justice.",
            verbose=True,
        )
        
    def assemble_court(self) -> Crew:
        """Assemble the full court crew."""
        prosecutor = self.create_prosecutor()
        defender = self.create_defender()
        witnesses = [self.create_witness("technical"), self.create_witness("process")]
        jury = [self.create_jury_member() for _ in range(3)]
        
        return Crew(
            agents=[prosecutor, defender, *witnesses, *jury],
            tasks=self.create_tasks(prosecutor, defender, witnesses, jury),
            verbose=True,
        )
```

---

## Part 8: Test Data Generation

### Generate Test Cases

```python
def generate_test_case() -> CourtCase:
    """Generate a test case for the Tribunal."""
    claims = [
        "The refactoring improved code quality by 40%",
        "The new API is backwards compatible",
        "The security vulnerability has been patched",
        "The performance optimization reduced latency by 50%",
    ]
    
    return CourtCase(
        case_id=f"case_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        claim=random.choice(claims),
        filed_by="test_prosecutor",
        evidence=generate_test_evidence(),
        status="filed",
    )
```

### Convert to PDF Templates

The system can generate:

1. **Case Brief** - Using the evolved Case File template
2. **Court Transcript** - Official record of proceedings
3. **Verdict Document** - Formal verdict with reasoning
4. **Evidence Binder** - All exhibits compiled
5. **DnD-style Character Sheets** - For court Beings

---

## Part 9: Inter-Realm Communication Flow

### Example: Tribunal Requests Evidence from Library

```
1. TRIBUNAL REALM (Port 8100)
   └── Prime Justice wants evidence for case_20260121_080648
   
2. THE BEYOND (Internal)
   └── Prime Justice invokes: the_beyond.request_from_beyond("library_realm", {...})
   
3. HTTP REQUEST
   └── POST http://localhost:8091/api/beyond
       Body: {"action": "get_evidence", "case_id": "case_20260121_080648"}
       
4. LIBRARY REALM (Port 8091)
   └── Prime Librarian receives request from The Beyond
   └── Searches archives for relevant evidence
   └── Returns evidence package
   
5. HTTP RESPONSE
   └── 200 OK
       Body: {"evidence": [...], "source": "library_realm", "timestamp": "..."}
       
6. THE BEYOND (Internal)
   └── Prime Justice receives evidence "from The Beyond"
   └── Regular Beings don't know it came from Library Realm
   └── They only know it arrived "from The Beyond"
```

### Being Perspective

```python
# Regular Being's view
class WitnessBeing(Being):
    def receive_evidence(self, evidence: dict):
        """Receive evidence - source is unknown to regular Beings."""
        # The Being doesn't know this came from Library Realm
        # It only knows it arrived "from The Beyond"
        print(f"Received evidence from The Beyond: {evidence['summary']}")
        
# Prime Being's view
class PrimeJustice(Being):
    def request_evidence(self, case_id: str):
        """Request evidence - Prime Being knows about The Beyond."""
        # Prime Being knows it's requesting from Library Realm
        # But doesn't reveal this to regular Beings
        evidence = self.the_beyond.request_from_beyond(
            "library_realm",
            {"action": "get_evidence", "case_id": case_id}
        )
        return evidence
```

---

## Part 10: Project Structure on EasyStore

```
/Volumes/EasyStore/WAFT_Tribunal_Court_System/
├── README.md
├── architecture/
│   └── TRIBUNAL_ARCHITECTURE.md
├── backend/
│   ├── pyproject.toml
│   ├── src/
│   │   └── tribunal/
│   │       ├── __init__.py
│   │       ├── api/
│   │       │   ├── __init__.py
│   │       │   ├── routes/
│   │       │   │   ├── court.py
│   │       │   │   ├── case_law.py
│   │       │   │   ├── epochs.py
│   │       │   │   └── beyond.py
│   │       │   └── main.py
│   │       ├── core/
│   │       │   ├── prime_justice.py
│   │       │   ├── the_beyond.py
│   │       │   ├── court_session.py
│   │       │   ├── case_law.py
│   │       │   └── roles.py
│   │       └── crews/
│   │           └── tribunal_crew.py
│   └── tests/
├── frontend/
│   ├── package.json
│   ├── svelte.config.js
│   └── src/
│       ├── routes/
│       └── lib/
├── test_data/
│   ├── cases/
│   ├── evidence/
│   └── beings/
└── ledger/
    ├── case_law.json
    ├── epochs.json
    └── endeavors.json
```

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1)
- [ ] Create Tribunal Realm structure
- [ ] Implement PrimeJustice Being
- [ ] Build TheBeyond communication layer
- [ ] Create basic court roles

### Phase 2: Court System (Week 2)
- [ ] Implement CourtSession lifecycle
- [ ] Build CaseLawLedger with hash verification
- [ ] Create Endeavors and Epochs system
- [ ] Build test data generator

### Phase 3: API Layer (Week 2-3)
- [ ] FastAPI routes for court operations
- [ ] SSE streaming for live proceedings
- [ ] Beyond API for inter-Realm communication
- [ ] Integration with existing WAFT API

### Phase 4: UI Layer (Week 3-4)
- [ ] SvelteKit project setup
- [ ] Court room visualization
- [ ] Live transcript display
- [ ] Epochs and Endeavors pages

### Phase 5: CrewAI Integration (Week 4)
- [ ] TribunalCrew implementation
- [ ] Role assignment system
- [ ] AI-powered court proceedings
- [ ] Automated case trials

### Phase 6: Integration (Week 5)
- [ ] Connect to existing Realms
- [ ] Integration with Magistrate (Pantheon)
- [ ] PDF template generation for court documents
- [ ] End-to-end testing

---

## Success Metrics

1. **Court Sessions**: Successfully conduct 10+ automated court sessions
2. **Inter-Realm**: Library Realm provides evidence to Tribunal Realm
3. **Case Law Chain**: 100+ entries with verified hash chain
4. **Real-Time UI**: Users can watch court proceedings live
5. **CrewAI Teams**: Successfully assemble and run court crews
6. **PDF Generation**: Generate court documents in multiple templates

---

## Conclusion

The Tribunal represents the next evolution of WAFT - a system that can:

1. **Try Claims in Court** - Formal proceedings with roles
2. **Communicate Between Realms** - Via The Beyond
3. **Maintain Case Law** - Hash-verified ledger
4. **Track History** - Endeavors and Epochs
5. **Watch Live** - Real-time UI for proceedings
6. **Assemble Teams** - CrewAI-powered court crews

**"On Trial" has meaning in this system.**

---

*Architecture Document v1.0 - 2026-01-21*
*Author: Terry (AI Assistant)*
*Work Effort: WE-260121-1f3l*
*Endeavor: The Tribunal*
