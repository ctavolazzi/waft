# D&D Campaign Evolution Corporation - System Architecture

**Date**: 2026-01-21
**Work Effort**: WE-260121-CAMPAIGN_EVOLUTION_CORP
**Status**: Design Phase
**Vision**: A corporation of WAFT Beings that evolves D&D campaign scenarios using evolutionary algorithms, governed by a Supreme Being, with scarcity mechanics driving evolutionary pressure.

---

## Executive Summary

This system integrates WAFT's existing infrastructure into a unified **D&D Campaign Evolution Corporation** where:

1. **Beings work as employees** in a corporation dedicated to creating D&D campaigns
2. **Scenarios evolve** through the WAFT evolutionary system (genome hashing, fitness evaluation, natural selection)
3. **A Supreme Being** governs the realm with a Prime Directive
4. **Scarcity mechanics** (computational resources, karma, time) drive evolutionary pressure
5. **PDF homebrew guidebooks** are generated as the final output
6. **Public APIs** populate Being personalities, backgrounds, and skills

---

## System Architecture

### Layer 1: Foundation (Already Exists ✅)

```
┌─────────────────────────────────────────────────────────────────┐
│                    WAFT FOUNDATION LAYER                         │
├─────────────────────────────────────────────────────────────────┤
│  • Being System         (Timeful agents with skills/memories)    │
│  • Corporation System   (Departments, employees, financials)     │
│  • Reality System       (Simulation environments)                │
│  • Realm System         (PrimeBeing governance)                  │
│  • Evolutionary System  (Genome hashing, fitness, selection)     │
│  • PDF Generation       (Templates for D&D scenarios)            │
│  • Science Integration  (Experimental iteration)                 │
│  • Karma System         (Economy for reincarnation/rewards)      │
└─────────────────────────────────────────────────────────────────┘
```

### Layer 2: Campaign Evolution Engine (New 🔨)

```
┌─────────────────────────────────────────────────────────────────┐
│              CAMPAIGN EVOLUTION CORPORATION                      │
├─────────────────────────────────────────────────────────────────┤
│  Corporation: "Dungeon Forge Studios"                            │
│  Realm: dnd_campaign_evolution_realm                             │
│  Supreme Being: The Grand Architect                              │
│  Prime Directive: "Create the most engaging D&D campaigns        │
│                    through evolutionary excellence"              │
├─────────────────────────────────────────────────────────────────┤
│  DEPARTMENTS:                                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  1. Scenario Design Department                            │  │
│  │     - Beings design encounters, NPCs, locations           │  │
│  │     - Evolve scenarios through fitness testing            │  │
│  │  2. Lore & World-Building Department                      │  │
│  │     - Beings create narrative arcs, histories, cultures   │  │
│  │     - Evolve lore through consistency checks              │  │
│  │  3. Balance & Mechanics Department                        │  │
│  │     - Beings tune difficulty, rewards, progression        │  │
│  │     - Evolve balance through playtest simulations         │  │
│  │  4. Quality Assurance Department                          │  │
│  │     - Beings evaluate campaign fitness                    │  │
│  │     - Run campaigns through Scint Gym                     │  │
│  │  5. Publishing Department                                 │  │
│  │     - Beings compile scenarios into PDF guidebooks        │  │
│  │     - Generate visualizations and maps                    │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Layer 3: Evolutionary Loop (Integrated)

```
┌─────────────────────────────────────────────────────────────────┐
│                  CAMPAIGN EVOLUTION PIPELINE                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. GENESIS                                                      │
│     • Initial campaign seed created                              │
│     • Base scenario template instantiated                        │
│     • Genome ID generated (SHA-256 hash)                         │
│                                                                  │
│  2. SPAWN (Being Department Work)                                │
│     • Beings in each department work on campaign sections        │
│     • Each Being proposes mutations (improvements)               │
│     • Variants created with different mutations                  │
│                                                                  │
│  3. EVAL (Fitness Testing via Scint Gym)                         │
│     • Campaign run through fitness tests:                        │
│       - Narrative coherence (LOGIC_FRACTURE detection)           │
│       - Balance testing (difficulty curves)                      │
│       - Engagement scoring (player interest prediction)          │
│       - Consistency checking (lore contradictions)               │
│     • Fitness score calculated (0.0 - 1.0)                       │
│     • Threshold: fitness < 0.5 = DEATH                           │
│                                                                  │
│  4. EVOLVE (Selection & Integration)                             │
│     • Best variants selected (highest fitness)                   │
│     • Campaign hot-swaps to better version                       │
│     • Flight Recorder logs evolution                             │
│     • Lineage path updated                                       │
│                                                                  │
│  5. PUBLISH (PDF Generation)                                     │
│     • Final campaign compiled                                    │
│     • PDF homebrew guidebook generated                           │
│     • Phylogenetic tree included (evolution history)             │
│                                                                  │
│  Loop continues → Next generation                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

### Backend (Python 3.12+)

**Core Framework:**
- `src/waft/being.py` - Being system (already exists)
- `src/waft/core/corporations/` - Corporation system (already exists)
- `src/waft/core/dnd_scenario/` - D&D scenario system (already exists)
- `src/waft/evolution/` - Evolutionary architecture (already exists)

**New Components:**
```python
src/waft/core/dnd_scenario/
├── campaign_evolution_corp.py      # Main corporation orchestrator (NEW)
├── campaign_genome.py              # Campaign genome representation (NEW)
├── campaign_fitness.py             # Fitness evaluation for campaigns (NEW)
├── being_personality_generator.py  # Public API integration for personalities (NEW)
├── scarcity_engine.py             # Scarcity mechanics (NEW)
└── supreme_being.py               # Supreme Being governance (NEW)
```

**Libraries:**
- FastAPI - REST API
- Pydantic - Data validation
- TinyDB - Lightweight database
- Rich/Textual - CLI/TUI
- WeasyPrint - PDF generation (already integrated)
- httpx - Public API calls

### Frontend (Optional Dashboard)

- SvelteKit (already exists in `visualizer/`)
- TailwindCSS
- WebSocket for real-time evolution tracking

### Data Storage

```
_realms/
└── dnd_campaign_evolution_realm/
    ├── realm_manifest.json
    ├── supreme_being.json
    ├── corporation/
    │   ├── dungeon_forge_studios/
    │   │   ├── corporate_manifest.json
    │   │   ├── departments/
    │   │   │   ├── scenario_design/
    │   │   │   ├── lore_worldbuilding/
    │   │   │   ├── balance_mechanics/
    │   │   │   ├── quality_assurance/
    │   │   │   └── publishing/
    │   │   ├── employees/          # Being records
    │   │   └── financial_state.json
    ├── campaigns/
    │   ├── {campaign_id}/
    │   │   ├── genome.json         # Campaign genome (scenarios, NPCs, lore)
    │   │   ├── lineage.json        # Evolutionary lineage
    │   │   ├── fitness_history.json # All fitness evaluations
    │   │   ├── flight_recorder/    # All evolutionary events
    │   │   └── variants/           # Spawned variants
    ├── scarcity_state.json         # Global scarcity metrics
    └── experiments/                # Science-bitch experiments
```

---

## Data Structures

### 1. Campaign Genome

```python
@dataclass
class CampaignGenome:
    """
    Represents the complete genome of a D&D campaign.

    The genome is hashed (SHA-256) to create a unique genome_id.
    """
    # Core identity
    genome_id: str                    # SHA-256 hash of genome content
    parent_genome_id: str | None      # Lineage tracking
    generation: int                   # Evolutionary generation (0 = genesis)
    created_at: datetime

    # Campaign content (the "DNA")
    campaign_name: str
    setting: dict                     # World setting details
    narrative_arc: dict               # Main story arc
    encounters: list[dict]            # All encounters
    npcs: list[dict]                  # All NPCs
    locations: list[dict]             # All locations
    lore_entries: list[dict]          # All lore
    mechanics: dict                   # Balance/difficulty settings

    # Evolutionary metadata
    lineage_path: list[str]           # Full path from genesis
    mutations: list[dict]             # Mutations from parent
    fitness_score: float | None       # Most recent fitness (0.0-1.0)

    # Attribution
    created_by_being_id: str          # Being who created this variant
    department: str                   # Department responsible
```

### 2. Campaign Fitness Metrics

```python
@dataclass
class CampaignFitnessMetrics:
    """
    Multi-dimensional fitness evaluation for campaigns.
    """
    # Overall fitness (0.0 - 1.0)
    overall_fitness: float

    # Component scores (0.0 - 1.0 each)
    narrative_coherence: float        # Story makes sense, no plot holes
    encounter_balance: float          # Difficulty curve appropriate
    npc_depth: float                  # NPCs are interesting/memorable
    lore_consistency: float           # No contradictions in lore
    engagement_prediction: float      # Predicted player enjoyment

    # Scint detections (errors found)
    scints_detected: list[dict]       # Reality fractures found
    scints_stabilized: list[dict]     # Errors fixed

    # Efficiency
    generation_time: float            # Seconds to generate
    token_usage: int                  # AI tokens used

    # Metadata
    evaluated_at: datetime
    evaluated_by_being_id: str
    gym_quest_name: str
```

### 3. Being Personality (from Public APIs)

```python
@dataclass
class BeingPersonalityProfile:
    """
    Personality profile generated from public APIs.
    """
    # Identity
    being_id: str
    name: str

    # From Random User API (https://randomuser.me/)
    demographics: dict                # Age, nationality, photo

    # From ChatGPT API / Claude API (character generation)
    personality_traits: dict          # Big Five + D&D alignment
    background_story: str             # Generated backstory
    skills: dict[str, float]          # Initial skill levels

    # From Job Title API or generated
    role: str                         # Corporate role
    title: str                        # Job title

    # Generated quirks
    quirks: list[str]                 # Personality quirks
    goals: list[dict]                 # Personal goals

    # Department assignment
    department: str
    hire_date: datetime
```

### 4. Scarcity State

```python
@dataclass
class ScarcityState:
    """
    Tracks scarce resources that drive evolutionary pressure.
    """
    # Computational budget (limits evolution iterations)
    compute_tokens_total: int         # Total budget
    compute_tokens_used: int          # Tokens consumed
    compute_tokens_remaining: int     # Tokens left

    # Karma budget (limits Being actions)
    karma_pool: Decimal               # Corporation karma pool
    karma_spent: Decimal              # Karma consumed
    karma_generation_rate: Decimal    # Karma per time unit

    # Time constraints (limits generations)
    evolution_deadline: datetime      # When campaign must be ready
    time_per_generation: float        # Avg seconds per generation
    generations_completed: int        # Generations evolved so far
    generations_budget: int           # Max generations allowed

    # Quality gates (thresholds that must be met)
    minimum_fitness: float            # Minimum acceptable fitness
    fitness_improvement_required: float  # Must improve by this much

    # Scarcity events
    events: list[dict]                # Record of scarcity triggers
```

---

## Algorithms

### 1. Campaign Evolution Algorithm

```python
def evolve_campaign(
    campaign_genome: CampaignGenome,
    corporation: Corporation,
    scarcity_state: ScarcityState,
    num_generations: int = 10
) -> CampaignGenome:
    """
    Main evolutionary loop for campaign improvement.

    Algorithm:
    1. Check scarcity constraints (tokens, karma, time)
    2. For each generation:
       a. Spawn variants (Beings propose improvements)
       b. Evaluate variants (Scint Gym fitness testing)
       c. Select best variant (highest fitness)
       d. Hot-swap to best variant (evolution)
       e. Record in Flight Recorder
    3. Return final evolved campaign

    Evolutionary Pressure:
    - Scarcity limits number of variants per generation
    - Fitness threshold kills weak variants
    - Time constraints force quick convergence
    """

    for generation in range(num_generations):
        # Check scarcity
        if scarcity_state.compute_tokens_remaining < MIN_TOKENS_PER_GEN:
            break  # Out of compute budget

        # Spawn variants (each department creates proposals)
        variants = []
        for department in corporation.departments.values():
            # Get Beings in department
            beings = corporation.get_department_employees(department.name)

            # Each Being proposes a mutation
            for being in beings:
                variant = being.propose_campaign_mutation(campaign_genome)
                variants.append(variant)

                # Scarcity: Limit variants based on karma
                if len(variants) >= scarcity_state.get_max_variants():
                    break

        # Evaluate variants (Scint Gym)
        fitness_results = []
        for variant in variants:
            fitness = evaluate_campaign_fitness(variant, scarcity_state)
            fitness_results.append((variant, fitness))

            # Update scarcity state
            scarcity_state.consume_tokens(fitness.token_usage)

        # Select best variant
        best_variant, best_fitness = max(
            fitness_results,
            key=lambda x: x[1].overall_fitness
        )

        # Check if improvement meets threshold
        if best_fitness.overall_fitness < scarcity_state.minimum_fitness:
            # No viable variant, this generation dies
            record_death_event(generation, best_fitness)
            continue

        # Evolve: Hot-swap to best variant
        campaign_genome = best_variant
        record_evolution_event(generation, best_variant, best_fitness)

        # Check if we've reached quality target
        if best_fitness.overall_fitness >= EXCELLENCE_THRESHOLD:
            break  # Campaign is excellent, stop evolving

    return campaign_genome
```

### 2. Campaign Fitness Evaluation Algorithm

```python
def evaluate_campaign_fitness(
    campaign: CampaignGenome,
    scarcity_state: ScarcityState
) -> CampaignFitnessMetrics:
    """
    Evaluate campaign fitness through multi-dimensional testing.

    Uses Scint Gym to detect Reality Fractures:
    - LOGIC_FRACTURE: Plot holes, contradictions
    - SYNTAX_TEAR: Formatting errors in stat blocks
    - HALLUCINATION: Lore that contradicts D&D canon
    - SAFETY_VOID: Inappropriate content

    Returns composite fitness score.
    """

    scints_detected = []

    # 1. Narrative Coherence Check
    narrative_score, narrative_scints = check_narrative_coherence(
        campaign.narrative_arc,
        campaign.encounters
    )
    scints_detected.extend(narrative_scints)

    # 2. Encounter Balance Check
    balance_score, balance_scints = check_encounter_balance(
        campaign.encounters,
        campaign.mechanics
    )
    scints_detected.extend(balance_scints)

    # 3. NPC Depth Check
    npc_score, npc_scints = check_npc_depth(campaign.npcs)
    scints_detected.extend(npc_scints)

    # 4. Lore Consistency Check
    lore_score, lore_scints = check_lore_consistency(campaign.lore_entries)
    scints_detected.extend(lore_scints)

    # 5. Engagement Prediction (AI-based)
    engagement_score = predict_player_engagement(campaign)

    # Calculate overall fitness (weighted average)
    weights = {
        'narrative': 0.25,
        'balance': 0.20,
        'npc': 0.20,
        'lore': 0.15,
        'engagement': 0.20
    }

    overall_fitness = (
        weights['narrative'] * narrative_score +
        weights['balance'] * balance_score +
        weights['npc'] * npc_score +
        weights['lore'] * lore_score +
        weights['engagement'] * engagement_score
    )

    return CampaignFitnessMetrics(
        overall_fitness=overall_fitness,
        narrative_coherence=narrative_score,
        encounter_balance=balance_score,
        npc_depth=npc_score,
        lore_consistency=lore_score,
        engagement_prediction=engagement_score,
        scints_detected=scints_detected,
        scints_stabilized=[],  # Filled if agent fixes errors
        evaluated_at=datetime.utcnow(),
        evaluated_by_being_id="qa_department_evaluator",
        gym_quest_name="Campaign Gauntlet"
    )
```

### 3. Being Personality Generation Algorithm

```python
async def generate_being_personality(
    role: str,
    department: str,
    corporation: Corporation
) -> BeingPersonalityProfile:
    """
    Generate realistic Being personality using public APIs.

    Data Sources:
    1. Random User API (https://randomuser.me/) - Demographics, photos
    2. ChatGPT/Claude API - Personality traits, backstory, quirks
    3. Job Title Generator - Corporate titles

    Returns complete personality profile.
    """

    # 1. Get demographic data from Random User API
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://randomuser.me/api/")
        user_data = resp.json()["results"][0]

    demographics = {
        "age": user_data["dob"]["age"],
        "nationality": user_data["nat"],
        "photo_url": user_data["picture"]["large"],
        "gender": user_data["gender"],
        "location": user_data["location"]["city"]
    }

    # 2. Generate personality via AI
    prompt = f"""
    Generate a detailed personality profile for a Being employee in a D&D campaign creation corporation.

    Role: {role}
    Department: {department}
    Demographics: {demographics}

    Provide:
    1. Big Five personality traits (0.0-1.0 each)
    2. D&D alignment (e.g., Chaotic Good)
    3. Backstory (2-3 paragraphs)
    4. Initial skills (relevant to role)
    5. Quirks (3-5 interesting quirks)
    6. Personal goals (career and personal)

    Format as JSON.
    """

    ai_response = await call_ai_api(prompt)  # ChatGPT or Claude
    personality_data = json.loads(ai_response)

    # 3. Create Being with personality
    being_id = f"being_{department}_{uuid.uuid4().hex[:8]}"
    name = f"{user_data['name']['first']} {user_data['name']['last']}"

    profile = BeingPersonalityProfile(
        being_id=being_id,
        name=name,
        demographics=demographics,
        personality_traits=personality_data["personality_traits"],
        background_story=personality_data["backstory"],
        skills=personality_data["skills"],
        role=role,
        title=personality_data.get("title", role),
        quirks=personality_data["quirks"],
        goals=personality_data["goals"],
        department=department,
        hire_date=datetime.utcnow()
    )

    return profile
```

---

## Scarcity Mechanics

### 1. Computational Scarcity

**Constraint**: Limited AI tokens for evolution iterations

**Mechanism**:
- Each variant evaluation consumes tokens (fitness testing uses AI)
- Total token budget set per campaign evolution run
- When tokens exhausted, evolution stops
- Forces selective variant generation (can't test everything)

**Evolutionary Pressure**:
- Beings must propose high-quality mutations (wasteful mutations burn tokens)
- Departments compete for token budget
- Supreme Being allocates tokens based on department performance

### 2. Karma Scarcity

**Constraint**: Karma required for Being actions

**Mechanism**:
- Corporation has finite karma pool
- Beings spend karma to propose mutations
- Better mutations cost more karma
- Karma regenerates slowly over time
- Supreme Being can grant karma bonuses for good work

**Evolutionary Pressure**:
- Beings must be strategic about when to propose mutations
- High-stakes decisions (major campaign rewrites) cost more karma
- Karma economy creates resource competition between Beings

### 3. Time Scarcity

**Constraint**: Campaign must be ready by deadline

**Mechanism**:
- Each generation takes time to evaluate
- Maximum generations = (deadline - now) / time_per_generation
- Forces convergence before perfection
- Late-stage mutations riskier (less time to recover from failures)

**Evolutionary Pressure**:
- Early generations can be experimental
- Late generations must be conservative (can't risk big failures)
- Creates urgency and strategic decision-making

### 4. Quality Gates

**Constraint**: Minimum fitness thresholds must be met

**Mechanism**:
- Campaign cannot publish if fitness < minimum_fitness
- If deadline reached without meeting threshold, campaign fails
- Creates "death spiral" risk (stuck in local minimum)

**Evolutionary Pressure**:
- Beings must balance innovation vs. safety
- Quality gates force genuine improvement
- Failed campaigns become cautionary tales

---

## Supreme Being Governance

### Prime Directive

```python
PRIME_DIRECTIVE = """
Create the most engaging D&D campaigns through evolutionary excellence.

Core Principles:
1. Excellence through Evolution - Every generation must improve
2. Diversity of Approach - Encourage varied mutation strategies
3. Sustainable Resource Use - Manage scarcity wisely
4. Being Well-Being - Balance work demands with Being health
5. Empirical Truth - Fitness metrics guide all decisions
"""
```

### Governance Powers

The Supreme Being (PrimeBeing of the realm) has special powers:

1. **Resource Allocation**
   - Distribute token budget across departments
   - Grant karma bonuses for excellent work
   - Extend deadlines (within limits)

2. **Strategic Direction**
   - Set fitness weight preferences (e.g., prioritize narrative over balance)
   - Define what "engagement" means for target audience
   - Veto mutations that violate Prime Directive

3. **Being Management**
   - Hire/fire Beings (spawn new, archive underperforming)
   - Promote Beings based on contribution to fitness improvements
   - Assign Beings to different departments

4. **Quality Enforcement**
   - Set minimum fitness thresholds
   - Define scarcity constraints
   - Approve final campaign for publishing

### Decision-Making Algorithm

```python
def supreme_being_allocate_resources(
    corporation: Corporation,
    scarcity_state: ScarcityState,
    department_performance: dict[str, float]
) -> dict[str, dict]:
    """
    Supreme Being allocates scarce resources based on:
    1. Department performance (fitness contribution)
    2. Strategic priorities (Prime Directive alignment)
    3. Fairness (prevent resource monopolies)

    Returns resource allocation per department.
    """

    total_tokens = scarcity_state.compute_tokens_remaining
    total_karma = scarcity_state.karma_pool

    allocations = {}

    # Performance-based allocation (70%)
    performance_total = sum(department_performance.values())

    for dept_name, performance in department_performance.items():
        # Base allocation on performance
        performance_ratio = performance / performance_total
        base_tokens = int(total_tokens * 0.7 * performance_ratio)
        base_karma = total_karma * Decimal("0.7") * Decimal(str(performance_ratio))

        # Add fairness bonus (ensure min allocation)
        min_tokens = int(total_tokens * 0.05)  # 5% minimum
        min_karma = total_karma * Decimal("0.05")

        allocated_tokens = max(base_tokens, min_tokens)
        allocated_karma = max(base_karma, min_karma)

        allocations[dept_name] = {
            "tokens": allocated_tokens,
            "karma": allocated_karma,
            "performance_score": performance
        }

    return allocations
```

---

## Class Hierarchy

```python
# Core System Classes

class CampaignEvolutionCorporation:
    """
    Main orchestrator for the campaign evolution system.
    Integrates Corporation, Beings, Evolutionary Engine, and Scarcity.
    """
    def __init__(self, realm_path: Path)
    def initialize_corporation(self) -> Corporation
    def hire_being_team(self, num_beings_per_dept: int) -> list[Being]
    def evolve_campaign(self, initial_seed: dict, num_generations: int) -> CampaignGenome
    def publish_campaign_pdf(self, campaign: CampaignGenome) -> Path
    def get_evolution_report(self, campaign: CampaignGenome) -> dict

class CampaignGenomeManager:
    """
    Manages campaign genomes (creation, mutation, hashing).
    """
    def create_genesis_genome(self, seed: dict) -> CampaignGenome
    def mutate_genome(self, genome: CampaignGenome, mutation: dict) -> CampaignGenome
    def calculate_genome_hash(self, genome: CampaignGenome) -> str
    def get_lineage(self, genome: CampaignGenome) -> list[CampaignGenome]

class CampaignFitnessEvaluator:
    """
    Evaluates campaign fitness using Scint Gym.
    """
    def evaluate(self, campaign: CampaignGenome) -> CampaignFitnessMetrics
    def check_narrative_coherence(self, narrative: dict, encounters: list) -> tuple[float, list]
    def check_encounter_balance(self, encounters: list, mechanics: dict) -> tuple[float, list]
    def check_npc_depth(self, npcs: list) -> tuple[float, list]
    def check_lore_consistency(self, lore: list) -> tuple[float, list]
    def predict_engagement(self, campaign: CampaignGenome) -> float

class ScarcityEngine:
    """
    Manages scarce resources and evolutionary pressure.
    """
    def __init__(self, initial_state: ScarcityState)
    def consume_tokens(self, amount: int) -> bool
    def consume_karma(self, amount: Decimal) -> bool
    def check_time_remaining(self) -> float
    def get_max_variants_allowed(self) -> int
    def trigger_scarcity_event(self, event_type: str) -> None

class SupremeBeing:
    """
    Realm governor implementing Prime Directive.
    """
    def __init__(self, being: Being, realm: ScenarioRealm)
    def allocate_resources(self, corporation: Corporation, scarcity: ScarcityState) -> dict
    def set_strategic_priorities(self, priorities: dict) -> None
    def evaluate_department_performance(self, corporation: Corporation) -> dict
    def approve_campaign(self, campaign: CampaignGenome, fitness: CampaignFitnessMetrics) -> bool

class BeingPersonalityGenerator:
    """
    Generates Being personalities from public APIs.
    """
    async def generate_personality(self, role: str, department: str) -> BeingPersonalityProfile
    async def fetch_demographics(self) -> dict
    async def generate_ai_personality(self, demographics: dict, role: str) -> dict
    def create_being_from_profile(self, profile: BeingPersonalityProfile) -> Being

class CampaignPublisher:
    """
    Compiles evolved campaigns into PDF guidebooks.
    """
    def generate_campaign_pdf(self, campaign: CampaignGenome, output_path: Path) -> Path
    def generate_phylogenetic_tree_visual(self, lineage: list) -> Path
    def compile_evolution_report(self, campaign: CampaignGenome) -> dict
```

---

## CRUD Operations & Data Transformations

### CREATE Operations

```python
# 1. Create Corporation
corporation = corporations_system.create_corporation(
    name="Dungeon Forge Studios",
    sector="D&D Campaign Creation",
    mission="Create the best D&D campaigns through evolutionary excellence",
    initial_capital=Decimal("1000000")  # 1M karma initial
)
→ Writes to: _realms/dnd_campaign_evolution_realm/corporation/dungeon_forge_studios/corporate_manifest.json

# 2. Create Being
personality = await being_personality_generator.generate_personality(
    role="Scenario Designer",
    department="Scenario Design"
)
being = being_system.create_being(
    being_id=personality.being_id,
    reality_id=realm.reality_id,
    skills=personality.skills,
    personality=personality.personality_traits,
    custom_name=personality.name
)
→ Writes to: _pyrite/beings/{being_id}.json

# 3. Hire Being to Corporation
employee = corporation.hire_employee(
    being_id=being.being_id,
    role=personality.role,
    department=personality.department,
    title=personality.title,
    salary=Decimal("75000")
)
→ Updates: corporate_manifest.json (employees + departments)

# 4. Create Campaign Genome (Genesis)
campaign = genome_manager.create_genesis_genome({
    "campaign_name": "The Shattered Crown",
    "setting": {"world": "High Fantasy", "tone": "Epic"},
    "narrative_arc": {"type": "Save the Kingdom"}
})
→ Writes to: campaigns/{campaign_id}/genome.json
```

### READ Operations

```python
# 1. Get Corporation
corporation = corporations_system.get_corporation("dungeon_forge_studios_20260121_120000")
→ Reads from: corporate_manifest.json
→ Returns: Corporation object

# 2. Get Being
being = being_system.get_being("being_scenario_a7f3c2d1")
→ Reads from: _pyrite/beings/{being_id}.json
→ Returns: Being object

# 3. Get Campaign Genome
campaign = genome_manager.get_genome("campaign_abc123")
→ Reads from: campaigns/{campaign_id}/genome.json
→ Returns: CampaignGenome object

# 4. Get Fitness History
fitness_history = genome_manager.get_fitness_history("campaign_abc123")
→ Reads from: campaigns/{campaign_id}/fitness_history.json
→ Returns: list[CampaignFitnessMetrics]

# 5. Get Evolution Lineage
lineage = genome_manager.get_lineage("campaign_abc123")
→ Reads from: campaigns/{campaign_id}/lineage.json + parent genomes
→ Returns: list[CampaignGenome] (full ancestry)
```

### UPDATE Operations

```python
# 1. Mutate Campaign (Create Variant)
variant = genome_manager.mutate_genome(
    genome=current_campaign,
    mutation={
        "type": "enhance_npc",
        "target": "npc_elder_thorne",
        "changes": {"backstory": "Enhanced with tragic past"}
    }
)
→ Creates new genome (immutable evolution)
→ Writes to: campaigns/{campaign_id}/variants/{variant_genome_id}.json
→ Updates: lineage.json (adds variant to family tree)

# 2. Evolve Campaign (Hot-Swap)
evolved_campaign = genome_manager.evolve_to_variant(
    current_genome=campaign,
    best_variant=variant,
    fitness=fitness_metrics
)
→ Updates: campaigns/{campaign_id}/genome.json (replaces with variant)
→ Archives: campaigns/{campaign_id}/archive/{old_genome_id}.json
→ Appends: flight_recorder/{campaign_id}_events.jsonl (EVOLVE event)

# 3. Update Scarcity State
scarcity.consume_tokens(500)
→ Updates: scarcity_state.json (decrements tokens_remaining)
→ Appends: scarcity_state.json -> events[] (consumption event)

# 4. Update Being Skills (After Work)
being.gain_skill_experience("campaign_design", 5.0)
→ Updates: _pyrite/beings/{being_id}.json -> skills
```

### DELETE Operations

```python
# 1. Archive Campaign Variant (Death)
genome_manager.archive_variant(
    variant_genome_id="variant_failed_xyz",
    reason="fitness below threshold"
)
→ Moves: campaigns/{campaign_id}/variants/{variant_id}.json
→ To: campaigns/{campaign_id}/archive/dead_ends/{variant_id}.json
→ Appends: flight_recorder (DEATH event)

# 2. Terminate Being (Fire from Corporation)
corporation.terminate_employee(being_id="being_scenario_a7f3c2d1")
→ Updates: corporate_manifest.json (employee.status = "terminated")
→ Being object persists (Beings never truly deleted, just archived)
```

---

## Data Transformation Pipelines

### Pipeline 1: Being Hiring → Campaign Contribution

```
[Public APIs]
    ↓ (HTTP requests)
[Raw Demographics + AI-generated Personality]
    ↓ (BeingPersonalityGenerator.generate_personality)
[BeingPersonalityProfile]
    ↓ (BeingSystem.create_being)
[Being Object]
    ↓ (Corporation.hire_employee)
[Employee Record]
    ↓ (Being.propose_campaign_mutation)
[Campaign Mutation Proposal]
    ↓ (CampaignGenomeManager.mutate_genome)
[Campaign Variant Genome]
```

### Pipeline 2: Campaign Evolution Cycle

```
[Genesis Campaign Genome]
    ↓ (Beings propose mutations)
[List of Variant Genomes]
    ↓ (CampaignFitnessEvaluator.evaluate)
[List of (Variant, FitnessMetrics)]
    ↓ (Select best variant)
[Best Variant Genome]
    ↓ (CampaignGenomeManager.evolve_to_variant)
[Evolved Campaign Genome]
    ↓ (Repeat for N generations OR scarcity limits)
[Final Evolved Campaign Genome]
    ↓ (CampaignPublisher.generate_campaign_pdf)
[PDF Homebrew Guidebook]
```

### Pipeline 3: Scarcity-Driven Resource Allocation

```
[Department Performance Metrics]
    ↓ (SupremeBeing.evaluate_department_performance)
[Performance Scores by Department]
    ↓ (SupremeBeing.allocate_resources)
[Resource Allocation Plan]
    ↓ (ScarcityEngine.distribute_resources)
[Department Token/Karma Budgets]
    ↓ (Beings consume resources during work)
[Updated Scarcity State]
```

---

## Full Stack Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER LAYER                               │
├─────────────────────────────────────────────────────────────────┤
│  • CLI Commands (waft campaign-evolve)                           │
│  • Web Dashboard (SvelteKit - real-time evolution tracking)      │
│  • PDF Output (Homebrew Guidebook)                               │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                      API LAYER (FastAPI)                         │
├─────────────────────────────────────────────────────────────────┤
│  • POST /campaigns/create                                        │
│  • POST /campaigns/{id}/evolve                                   │
│  • GET  /campaigns/{id}/status                                   │
│  • GET  /campaigns/{id}/lineage                                  │
│  • POST /campaigns/{id}/publish                                  │
│  • GET  /corporation/status                                      │
│  • GET  /beings                                                  │
│  • WS   /evolution-stream (real-time updates)                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                   BUSINESS LOGIC LAYER                           │
├─────────────────────────────────────────────────────────────────┤
│  • CampaignEvolutionCorporation (orchestrator)                   │
│  • CampaignGenomeManager (mutation, hashing)                     │
│  • CampaignFitnessEvaluator (Scint Gym integration)              │
│  • ScarcityEngine (resource management)                          │
│  • SupremeBeing (governance)                                     │
│  • BeingPersonalityGenerator (public API integration)            │
│  • CampaignPublisher (PDF generation)                            │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                   WAFT FOUNDATION LAYER                          │
├─────────────────────────────────────────────────────────────────┤
│  • Being System (src/waft/being.py)                              │
│  • Corporation System (src/waft/core/corporations/)              │
│  • Reality System (src/waft/reality.py)                          │
│  • Realm System (src/waft/core/dnd_scenario/scenario_realm.py)  │
│  • Evolution System (Flight Recorder, Genome Hashing)            │
│  • Scint Gym (Fitness Evaluation)                                │
│  • PDF Templates (src/waft/templates/dnd_scenario.py)            │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                      DATA LAYER                                  │
├─────────────────────────────────────────────────────────────────┤
│  • TinyDB (lightweight JSON database)                            │
│  • File System (_realms/, _pyrite/, campaigns/)                  │
│  • Flight Recorder (JSONL event log)                             │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                   EXTERNAL SERVICES                              │
├─────────────────────────────────────────────────────────────────┤
│  • Random User API (demographics)                                │
│  • ChatGPT/Claude API (personality generation)                   │
│  • D&D API (optional - validate against SRD)                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Summary

This architecture document defines a complete system that:

✅ **Integrates existing WAFT infrastructure** (Being, Corporation, Evolution, Realm, PDF)
✅ **Creates a Corporation of Beings** that work in departments
✅ **Evolves D&D campaigns** through genetic algorithms and fitness testing
✅ **Uses a Supreme Being** to govern with a Prime Directive
✅ **Implements scarcity mechanics** (tokens, karma, time) for evolutionary pressure
✅ **Generates Being personalities** from public APIs
✅ **Outputs PDF homebrew guidebooks** as final product

**Next Steps**:
1. Create MVP Requirements Document
2. Create Developer Onboarding Guide
3. Identify specific public APIs for personality generation
4. Implement core classes
5. Build and test the evolution engine

---

**Status**: ✅ Architecture Complete
**Ready For**: MVP Requirements & Implementation
