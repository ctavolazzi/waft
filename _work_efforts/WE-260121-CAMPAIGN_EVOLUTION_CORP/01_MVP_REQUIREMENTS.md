# D&D Campaign Evolution Corporation - MVP Requirements

**Date**: 2026-01-21
**Work Effort**: WE-260121-CAMPAIGN_EVOLUTION_CORP
**Purpose**: Define Minimum Viable Product for campaign evolution system
**Status**: Requirements Definition

---

## MVP Vision

**Goal**: Demonstrate a working campaign evolution system where a corporation of AI Beings evolves a D&D campaign scenario through multiple generations, with fitness evaluation and scarcity constraints, culminating in a PDF homebrew guidebook.

**Success Criteria**:
1. ✅ Corporation created with 3+ departments and 5+ Beings
2. ✅ Beings have realistic personalities from public APIs
3. ✅ Campaign evolves through 5+ generations
4. ✅ Fitness scores improve across generations
5. ✅ Scarcity mechanics limit evolution (tokens/karma/time)
6. ✅ Final PDF guidebook generated with evolution history
7. ✅ Complete lineage tracking (phylogenetic tree)

---

## MVP Scope: What's IN

### Core Features (Must Have)

#### 1. Corporation Setup ✅ (Mostly Exists)
- **Corporation Creation**
  - Name: "Dungeon Forge Studios"
  - Sector: "D&D Campaign Creation"
  - Initial karma: 1,000,000
  - 3 departments minimum

- **Departments** (MVP subset):
  - **Scenario Design** - Create encounters
  - **Lore & World-Building** - Create NPCs and lore
  - **Quality Assurance** - Evaluate fitness

- **Beings Hiring**:
  - 2 Beings per department (6 total minimum)
  - Personalities from public APIs
  - Skills: campaign_design, lore_writing, quality_testing

#### 2. Being Personality Generation (NEW)
- **Public API Integration**:
  - Random User API for demographics/photos
  - Local LLM or simple templates for personality traits (MVP: keep it simple)

- **Personality Profile**:
  - Name, role, department
  - 3-5 skills relevant to role
  - 2-3 quirks
  - Short backstory (1 paragraph)

**MVP Simplification**: Instead of complex AI generation, use template-based personalities with randomization from Random User API.

#### 3. Campaign Genome (NEW)
- **Data Structure**:
  ```python
  CampaignGenome:
      genome_id: str (SHA-256)
      parent_genome_id: str | None
      generation: int
      campaign_name: str
      narrative_arc: dict
          - plot_summary: str
          - main_villain: str
          - heroic_goal: str
      encounters: list[dict]
          - name: str
          - description: str
          - difficulty: int (1-10)
          - rewards: str
      npcs: list[dict]
          - name: str
          - role: str
          - personality: str
          - backstory: str
      lore_entries: list[dict]
          - title: str
          - content: str
      lineage_path: list[str]
      fitness_score: float | None
  ```

- **Operations**:
  - Create genesis genome from seed
  - Mutate genome (add/modify encounters, NPCs, lore)
  - Calculate genome hash (SHA-256)
  - Track lineage

#### 4. Campaign Evolution Engine (NEW - Core of MVP)

**Workflow**:
```
1. Genesis: Create initial campaign from template
2. For each generation (5 generations for MVP):
   a. Each department's Beings propose mutations
   b. Create variant genomes
   c. Evaluate each variant (fitness testing)
   d. Select best variant
   e. Hot-swap to best variant
   f. Record in Flight Recorder
3. Publish final campaign as PDF
```

**Mutations** (MVP - Simple):
- **Add Encounter**: Being adds new encounter to campaign
- **Enhance NPC**: Being expands NPC backstory/personality
- **Add Lore**: Being adds lore entry to deepen world
- **Adjust Difficulty**: Being tweaks encounter difficulty

**MVP Simplification**: Fixed mutation types, simple rules-based selection.

#### 5. Fitness Evaluation (NEW - Simplified)

**Fitness Components** (MVP subset):
- **Narrative Coherence** (40%): Check plot makes sense
  - Plot has clear beginning/middle/end
  - Villain motivation is clear
  - Hero goal is achievable
  - Score: 0.0-1.0 based on checklist

- **Content Completeness** (30%): Check campaign has enough content
  - At least 3 encounters
  - At least 3 NPCs
  - At least 2 lore entries
  - Score: 0.0-1.0 based on count thresholds

- **Balance** (30%): Check difficulty progression
  - Encounters have increasing difficulty
  - Rewards match difficulty
  - Score: 0.0-1.0 based on difficulty curve

**Overall Fitness**: Weighted average of components

**MVP Simplification**: Rules-based evaluation instead of AI-based. Simple checks, no Scint Gym integration initially.

#### 6. Scarcity Mechanics (NEW - Basic)

**Token Budget**:
- Total budget: 10,000 tokens (simulated)
- Each variant evaluation: 100 tokens
- Each mutation proposal: 50 tokens
- When budget exhausted, evolution stops

**Karma Budget**:
- Corporation starts with 1,000,000 karma
- Each mutation proposal costs: 10,000 karma
- Karma regenerates: +5,000 per generation

**Time Budget**:
- Max generations: 10 (hardcoded for MVP)
- Each generation takes ~1 minute (not enforced, just tracked)

**MVP Simplification**: Simulated scarcity (no real AI token consumption), simple tracking.

#### 7. Flight Recorder (✅ Exists - Need Integration)

**Events to Record**:
- GENESIS: Initial campaign created
- SPAWN: Variant genome created
- MUTATE: Mutation applied
- GYM_EVAL: Fitness evaluation completed
- EVOLVE: Best variant selected and hot-swapped
- DEATH: Variant fitness below threshold

**Event Format**:
```json
{
  "timestamp": "2026-01-21T12:00:00Z",
  "genome_id": "abc123...",
  "parent_id": "xyz789...",
  "generation": 2,
  "event_type": "EVOLVE",
  "payload": {
    "mutation": {...},
    "fitness_before": 0.65,
    "fitness_after": 0.72
  },
  "agent_id": "being_scenario_a7f3c2d1"
}
```

#### 8. PDF Guidebook Generation (✅ Exists - Need Enhancement)

**Content**:
- Campaign title and introduction
- Narrative arc summary
- All encounters (formatted as D&D stat blocks)
- All NPCs (character profiles)
- All lore entries
- **Evolution Report** (NEW):
  - Phylogenetic tree visualization
  - Fitness progression graph
  - Generation-by-generation summary

**Template**: Use existing `dnd_scenario.py` template, enhance with evolution report section.

#### 9. Supreme Being (NEW - Basic Governance)

**Minimal Powers** (MVP):
- Set initial resource budgets
- Approve final campaign for publishing (fitness threshold check)
- View evolution progress

**MVP Simplification**: Supreme Being is mostly passive observer, minimal active governance.

---

## MVP Scope: What's OUT (Future Versions)

### Deferred Features

1. **Advanced AI Fitness Evaluation**
   - Scint Gym integration (LOGIC_FRACTURE, SYNTAX_TEAR detection)
   - AI-based engagement prediction
   - Complex lore consistency checking
   → **MVP**: Simple rules-based evaluation

2. **Complex Scarcity Mechanics**
   - Real AI token consumption tracking
   - Dynamic karma regeneration based on Being performance
   - Time deadline enforcement
   → **MVP**: Simulated scarcity with fixed budgets

3. **Advanced Being Behavior**
   - Beings making autonomous decisions
   - Inter-Being collaboration
   - Being skill progression over time
   → **MVP**: Beings follow fixed mutation strategies

4. **Supreme Being Active Governance**
   - Dynamic resource re-allocation
   - Strategic priority setting mid-evolution
   - Being hiring/firing based on performance
   → **MVP**: Passive governance, fixed budgets

5. **Web Dashboard**
   - Real-time evolution tracking
   - Interactive phylogenetic tree
   - Being performance dashboards
   → **MVP**: CLI only, PDF output only

6. **Multiple Campaigns**
   - Running multiple campaign evolutions in parallel
   - Cross-campaign lore sharing
   - Campaign merging/forking
   → **MVP**: Single campaign evolution per run

7. **Advanced Mutations**
   - Campaign restructuring (major plot changes)
   - Multi-step mutations (coordinated changes)
   - Rollback/branching strategies
   → **MVP**: Simple atomic mutations only

8. **Public API Personality Generation**
   - ChatGPT/Claude API for rich personalities
   - Job title API integration
   - Personality evolution over time
   → **MVP**: Template-based personalities with Random User API demographics

---

## MVP Requirements by Component

### Component 1: CampaignGenome

**Requirements**:
- [R1.1] SHALL support creation from seed dictionary
- [R1.2] SHALL calculate SHA-256 genome hash
- [R1.3] SHALL track parent_genome_id for lineage
- [R1.4] SHALL track generation number (increments from parent)
- [R1.5] SHALL store campaign content (narrative, encounters, NPCs, lore)
- [R1.6] SHALL record most recent fitness_score

**Acceptance Criteria**:
- Genesis genome creates generation 0 with no parent
- Mutated genome has generation = parent.generation + 1
- Genome hash is deterministic (same content = same hash)
- Lineage path lists all ancestor genome IDs

**Implementation**:
- `src/waft/core/dnd_scenario/campaign_genome.py`
- Data classes using `@dataclass`
- JSON serialization for file storage

---

### Component 2: CampaignGenomeManager

**Requirements**:
- [R2.1] SHALL create genesis genome from campaign seed
- [R2.2] SHALL mutate genome with specific mutation
- [R2.3] SHALL calculate and update genome_id hash
- [R2.4] SHALL save/load genomes to/from disk
- [R2.5] SHALL retrieve complete lineage for a genome

**Acceptance Criteria**:
- Genesis creation produces valid CampaignGenome
- Mutation creates new genome, preserves parent lineage
- Saved genome can be loaded with identical content
- Lineage retrieval reconstructs full ancestry

**Implementation**:
- `src/waft/core/dnd_scenario/campaign_genome.py` (CampaignGenomeManager class)
- File storage in `_realms/dnd_campaign_evolution_realm/campaigns/{campaign_id}/`

---

### Component 3: CampaignFitnessEvaluator

**Requirements**:
- [R3.1] SHALL evaluate narrative coherence (0.0-1.0)
- [R3.2] SHALL evaluate content completeness (0.0-1.0)
- [R3.3] SHALL evaluate balance (0.0-1.0)
- [R3.4] SHALL calculate overall fitness as weighted average
- [R3.5] SHALL return detailed CampaignFitnessMetrics

**Acceptance Criteria**:
- Campaign with clear plot scores high on narrative coherence
- Campaign with 5+ encounters/NPCs scores high on completeness
- Campaign with progressive difficulty scores high on balance
- Overall fitness is in range [0.0, 1.0]

**Weights** (MVP):
- Narrative: 0.40
- Completeness: 0.30
- Balance: 0.30

**Implementation**:
- `src/waft/core/dnd_scenario/campaign_fitness.py`
- Rules-based evaluation (no AI calls for MVP)

---

### Component 4: ScarcityEngine

**Requirements**:
- [R4.1] SHALL track total token budget and consumption
- [R4.2] SHALL track total karma budget and consumption
- [R4.3] SHALL track generation count vs. max generations
- [R4.4] SHALL prevent operations when budget exhausted
- [R4.5] SHALL log all scarcity events

**Acceptance Criteria**:
- Token consumption decrements budget correctly
- Karma consumption decrements budget correctly
- Operations blocked when tokens = 0
- Scarcity events logged with timestamp and reason

**Initial Budgets** (MVP):
- Tokens: 10,000
- Karma: 1,000,000
- Max Generations: 10

**Implementation**:
- `src/waft/core/dnd_scenario/scarcity_engine.py`
- In-memory state, persisted to JSON

---

### Component 5: CampaignEvolutionCorporation (Orchestrator)

**Requirements**:
- [R5.1] SHALL initialize corporation with departments
- [R5.2] SHALL hire Beings with generated personalities
- [R5.3] SHALL orchestrate evolution loop for N generations
- [R5.4] SHALL collect mutations from Beings in each department
- [R5.5] SHALL evaluate all variants
- [R5.6] SHALL select best variant based on fitness
- [R5.7] SHALL evolve to best variant
- [R5.8] SHALL record all events in Flight Recorder
- [R5.9] SHALL publish final campaign as PDF

**Acceptance Criteria**:
- Corporation created with 3 departments, 6 Beings
- Evolution runs for exactly N generations OR scarcity limit
- Each generation produces variants, evaluates, selects best
- Fitness scores generally trend upward across generations
- Final PDF includes campaign content + evolution report

**Implementation**:
- `src/waft/core/dnd_scenario/campaign_evolution_corp.py`
- Uses existing Corporation, Being, ScenarioRealm systems

---

### Component 6: BeingPersonalityGenerator

**Requirements**:
- [R6.1] SHALL generate realistic demographics from Random User API
- [R6.2] SHALL create template-based personality traits
- [R6.3] SHALL assign role-appropriate skills
- [R6.4] SHALL create complete BeingPersonalityProfile
- [R6.5] SHALL create Being object from profile

**Acceptance Criteria**:
- Personality includes name, demographics (age, nationality, photo)
- Personality includes 3-5 skills relevant to role
- Personality includes 2-3 quirks
- Being created with personality traits and skills

**Personality Templates** (MVP):
```yaml
Scenario Designer:
  skills: [campaign_design: 7.0, encounter_balance: 6.0, creativity: 8.0]
  quirks: ["Loves plot twists", "Detail-oriented", "Perfectionist"]

Lore Writer:
  skills: [lore_writing: 8.0, world_building: 7.0, storytelling: 9.0]
  quirks: ["History buff", "Mythology enthusiast", "Name collector"]

QA Tester:
  skills: [quality_testing: 8.0, critical_thinking: 7.0, attention_to_detail: 9.0]
  quirks: ["Finds every bug", "Skeptical by nature", "Rule lawyer"]
```

**Implementation**:
- `src/waft/core/dnd_scenario/being_personality_generator.py`
- httpx for API calls
- YAML or JSON templates for personality traits

---

### Component 7: CampaignPublisher

**Requirements**:
- [R7.1] SHALL compile campaign genome into structured content
- [R7.2] SHALL generate phylogenetic tree visualization (simple ASCII or SVG)
- [R7.3] SHALL create fitness progression graph
- [R7.4] SHALL render content using existing dnd_scenario template
- [R7.5] SHALL output PDF to specified path

**Acceptance Criteria**:
- PDF includes all campaign content (narrative, encounters, NPCs, lore)
- PDF includes evolution report section
- PDF includes lineage visualization
- PDF is valid and opens in standard readers

**Evolution Report Sections**:
1. Campaign Lineage (text summary of generations)
2. Phylogenetic Tree (visual representation)
3. Fitness Progression (generation vs. fitness graph)
4. Notable Mutations (highlights of key changes)

**Implementation**:
- `src/waft/core/dnd_scenario/campaign_publisher.py`
- Uses existing `src/waft/templates/dnd_scenario.py`
- matplotlib or plotly for graphs (embedded as images)

---

### Component 8: SupremeBeing

**Requirements**:
- [R8.1] SHALL set initial scarcity budgets
- [R8.2] SHALL approve/reject final campaign based on fitness threshold
- [R8.3] SHALL log governance decisions

**Acceptance Criteria**:
- Supreme Being initializes scarcity state
- Supreme Being approves campaign if fitness >= 0.6
- Supreme Being rejects campaign if fitness < 0.6

**Minimal Governance** (MVP):
- No dynamic resource allocation
- No mid-evolution intervention
- Simple threshold-based approval

**Implementation**:
- `src/waft/core/dnd_scenario/supreme_being.py`
- Minimal class, mostly configuration

---

## MVP User Stories

### US-1: Initialize Campaign Evolution Corporation
**As a** user
**I want to** initialize a campaign evolution corporation
**So that** I have a team of Beings ready to create D&D campaigns

**Acceptance Criteria**:
- Command: `waft campaign-corp init --name "Dungeon Forge Studios"`
- Creates corporation in `_realms/dnd_campaign_evolution_realm/`
- Creates 3 departments
- Hires 6 Beings with personalities from Random User API
- Displays corporation summary (departments, Beings, budgets)

---

### US-2: Evolve D&D Campaign
**As a** user
**I want to** evolve a D&D campaign through multiple generations
**So that** I get an improved, polished campaign scenario

**Acceptance Criteria**:
- Command: `waft campaign-corp evolve --seed campaign_seed.json --generations 5`
- Loads campaign seed
- Runs 5 generations of evolution
- Displays progress (generation, best fitness, mutations)
- Saves final genome to disk
- Displays summary (lineage, fitness progression)

**Sample Output**:
```
🧬 Campaign Evolution Started
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📖 Campaign: The Shattered Crown
🏢 Corporation: Dungeon Forge Studios
🎯 Target Generations: 5

Generation 1/5
  ├─ Variants Created: 3
  ├─ Best Fitness: 0.58 (+0.08 from genesis)
  └─ Best Mutation: Enhanced villain backstory (Lore Dept)

Generation 2/5
  ├─ Variants Created: 3
  ├─ Best Fitness: 0.64 (+0.06)
  └─ Best Mutation: Added forest ambush encounter (Scenario Dept)

...

Generation 5/5
  ├─ Variants Created: 3
  ├─ Best Fitness: 0.78 (+0.05)
  └─ Best Mutation: Balanced reward progression (QA Dept)

✅ Evolution Complete!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Final Fitness: 0.78
Generations: 5
Total Variants Tested: 15
Fitness Improvement: +0.28 (56% improvement)

Final genome saved to:
_realms/dnd_campaign_evolution_realm/campaigns/the_shattered_crown/genome.json
```

---

### US-3: Publish Campaign as PDF
**As a** user
**I want to** publish the evolved campaign as a PDF homebrew guidebook
**So that** I can share it with my D&D group

**Acceptance Criteria**:
- Command: `waft campaign-corp publish --campaign the_shattered_crown --output guidebook.pdf`
- Loads final campaign genome
- Generates PDF with all content + evolution report
- Includes phylogenetic tree and fitness graphs
- Saves to specified output path
- Displays success message with file size

**Sample Output**:
```
📄 Publishing Campaign: The Shattered Crown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Compiling campaign content...
✅ Generating phylogenetic tree...
✅ Creating fitness graphs...
✅ Rendering PDF...

✅ Publication Complete!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

File: guidebook.pdf
Size: 2.3 MB
Pages: 24

Campaign Stats:
- Encounters: 7
- NPCs: 8
- Lore Entries: 12
- Evolution Generations: 5
- Final Fitness: 0.78

Ready to play! 🎲
```

---

### US-4: View Corporation Status
**As a** user
**I want to** view the current status of my campaign corporation
**So that** I can see Being assignments, budgets, and progress

**Acceptance Criteria**:
- Command: `waft campaign-corp status`
- Displays corporation name, departments, Beings
- Shows scarcity budgets (tokens, karma, generation count)
- Shows current campaign evolution status

**Sample Output**:
```
🏢 Dungeon Forge Studios
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Departments: 3
Beings Employed: 6
Founded: 2026-01-21

📊 Resource Budgets:
  Tokens: 7,500 / 10,000 (75% remaining)
  Karma: 850,000 / 1,000,000 (85% remaining)
  Generations: 5 / 10 (5 used)

👥 Beings by Department:

┌─ Scenario Design Department
│  ├─ Alice Chen (Scenario Designer, Lvl 1)
│  └─ Bob Martinez (Encounter Specialist, Lvl 1)

├─ Lore & World-Building Department
│  ├─ Carol Kim (Lore Writer, Lvl 1)
│  └─ David O'Brien (World Builder, Lvl 1)

└─ Quality Assurance Department
   ├─ Eve Patel (QA Tester, Lvl 1)
   └─ Frank Zhang (Balance Analyst, Lvl 1)

📈 Current Campaign: The Shattered Crown
  Generation: 5
  Fitness: 0.78
  Status: Evolution Complete
```

---

## MVP Development Phases

### Phase 1: Foundation Setup (Week 1)
**Goal**: Set up project structure and basic data models

**Tasks**:
1. Create work effort directory structure
2. Implement CampaignGenome data class
3. Implement CampaignGenomeManager (create, mutate, save/load)
4. Write unit tests for genome operations
5. Create sample campaign seed JSON

**Deliverables**:
- `campaign_genome.py` with CampaignGenome + CampaignGenomeManager
- Tests: `test_campaign_genome.py`
- Sample seed: `examples/campaign_seed_shattered_crown.json`

---

### Phase 2: Being Generation (Week 1-2)
**Goal**: Generate Beings with personalities

**Tasks**:
1. Integrate Random User API client
2. Create personality templates (YAML)
3. Implement BeingPersonalityGenerator
4. Test personality generation for all roles
5. Integrate with existing Being system

**Deliverables**:
- `being_personality_generator.py`
- Templates: `config/personality_templates.yaml`
- Tests: `test_personality_generation.py`

---

### Phase 3: Fitness Evaluation (Week 2)
**Goal**: Implement rules-based fitness evaluation

**Tasks**:
1. Implement narrative coherence checker
2. Implement content completeness checker
3. Implement balance checker
4. Integrate into CampaignFitnessEvaluator
5. Write fitness evaluation tests

**Deliverables**:
- `campaign_fitness.py` with CampaignFitnessEvaluator
- Tests: `test_campaign_fitness.py`

---

### Phase 4: Scarcity Engine (Week 2)
**Goal**: Implement scarcity tracking

**Tasks**:
1. Implement ScarcityEngine class
2. Implement budget tracking (tokens, karma, generations)
3. Implement consumption methods
4. Implement scarcity event logging
5. Write scarcity tests

**Deliverables**:
- `scarcity_engine.py`
- Tests: `test_scarcity_engine.py`

---

### Phase 5: Evolution Orchestrator (Week 3)
**Goal**: Implement main evolution loop

**Tasks**:
1. Implement CampaignEvolutionCorporation orchestrator
2. Integrate Corporation system
3. Integrate Being mutation proposals
4. Implement variant generation and evaluation
5. Implement selection and evolution logic
6. Integrate Flight Recorder
7. Write integration tests

**Deliverables**:
- `campaign_evolution_corp.py`
- Tests: `test_campaign_evolution.py`

---

### Phase 6: PDF Publishing (Week 3-4)
**Goal**: Generate final PDF guidebooks

**Tasks**:
1. Implement phylogenetic tree visualization (ASCII art or simple SVG)
2. Implement fitness progression graph (matplotlib)
3. Create evolution report template
4. Integrate with existing dnd_scenario template
5. Implement CampaignPublisher
6. Test PDF generation

**Deliverables**:
- `campaign_publisher.py`
- Enhanced template: `templates/dnd_campaign_evolution.py`
- Tests: `test_campaign_publisher.py`

---

### Phase 7: CLI Commands (Week 4)
**Goal**: Create user-facing CLI

**Tasks**:
1. Implement `waft campaign-corp init` command
2. Implement `waft campaign-corp evolve` command
3. Implement `waft campaign-corp publish` command
4. Implement `waft campaign-corp status` command
5. Add CLI tests

**Deliverables**:
- Updated `src/waft/main.py` with new commands
- Documentation: CLI usage guide

---

### Phase 8: Integration Testing & Polish (Week 4)
**Goal**: End-to-end testing and refinement

**Tasks**:
1. Run full end-to-end evolution test
2. Fix bugs and edge cases
3. Optimize performance
4. Write comprehensive documentation
5. Create demo campaign seeds

**Deliverables**:
- End-to-end test suite
- Performance benchmarks
- User documentation
- Demo campaign seeds (3-5 examples)

---

## MVP Success Metrics

### Functional Metrics
- ✅ Corporation created with 3 departments, 6 Beings
- ✅ Campaign evolves through 5+ generations
- ✅ Fitness scores increase by >20% from genesis to final
- ✅ PDF guidebook generated successfully
- ✅ Phylogenetic tree shows complete lineage
- ✅ All scarcity budgets tracked correctly

### Quality Metrics
- ✅ Unit test coverage: >80%
- ✅ Integration test coverage: >60%
- ✅ Zero critical bugs in core evolution loop
- ✅ PDF renders correctly in 3+ PDF readers
- ✅ CLI commands run without errors

### Performance Metrics (MVP)
- Campaign evolution (5 generations): <5 minutes
- PDF generation: <30 seconds
- Being personality generation: <2 seconds per Being

### User Experience Metrics
- CLI commands have clear help text
- Progress indicators show evolution status
- Error messages are helpful and actionable
- Output PDFs are visually appealing

---

## MVP Risks & Mitigations

### Risk 1: Random User API Rate Limiting
**Impact**: Medium
**Probability**: Medium
**Mitigation**:
- Cache API responses locally
- Implement exponential backoff
- Fallback to synthetic data if API fails

### Risk 2: Fitness Scores Not Improving
**Impact**: High
**Probability**: Medium
**Mitigation**:
- Ensure mutations are meaningful (not random noise)
- Tune fitness weights empirically
- Add logging to diagnose stuck evolutions
- Implement "restart from better ancestor" logic

### Risk 3: PDF Generation Failures
**Impact**: Medium
**Probability**: Low
**Mitigation**:
- Use well-tested WeasyPrint library
- Validate HTML before rendering
- Provide fallback to HTML output if PDF fails

### Risk 4: Scope Creep
**Impact**: High
**Probability**: High
**Mitigation**:
- Strict adherence to MVP scope (defer features to v2)
- Regular scope reviews
- "No" by default to new features during MVP

---

## MVP Acceptance Criteria

**The MVP is complete when**:

1. ✅ A user can run `waft campaign-corp init` and create a corporation with 6 Beings
2. ✅ A user can run `waft campaign-corp evolve --seed seed.json --generations 5` and see fitness improve
3. ✅ A user can run `waft campaign-corp publish` and get a valid PDF guidebook
4. ✅ The PDF includes campaign content + evolution report with lineage tree
5. ✅ All unit tests pass (>80% coverage)
6. ✅ All integration tests pass
7. ✅ Documentation is complete (architecture, API, CLI usage)

---

## Beyond MVP: v2.0 Vision

**Future enhancements** (not in MVP):

- Scint Gym integration for advanced fitness evaluation
- Real AI token tracking (OpenAI/Anthropic APIs)
- Supreme Being active governance (dynamic resource allocation)
- Web dashboard for real-time evolution tracking
- Multiple campaigns running in parallel
- Advanced mutations (campaign restructuring, cross-campaign lore sharing)
- Being skill progression and autonomous decision-making
- Community campaign sharing (campaign marketplace)

---

## Summary

This MVP defines a focused, achievable first version of the Campaign Evolution Corporation system that:

✅ Demonstrates the core concept (Beings evolving campaigns)
✅ Uses existing WAFT infrastructure (Corporation, Being, Realm, PDF)
✅ Implements key innovations (genome evolution, fitness evaluation, scarcity)
✅ Produces tangible output (PDF homebrew guidebook)
✅ Is completable in 4 weeks with focused effort

**Status**: ✅ MVP Requirements Complete
**Ready For**: Developer Onboarding Guide & Implementation
