# D&D Campaign Evolution Corporation
## A Self-Evolving Campaign Generator Powered by WAFT

**Work Effort ID**: WE-260121-CAMPAIGN_EVOLUTION_CORP
**Created**: 2026-01-21
**Status**: Design Complete → Ready for Implementation
**Goal**: Create a corporation of AI Beings that evolves D&D campaigns through genetic algorithms

---

## 🎯 Vision

Imagine a corporation where AI Beings work together to create the best D&D campaigns imaginable. Each Being has a personality, skills, and a role. They propose improvements to campaigns, and the best ideas survive through natural selection. After multiple generations of evolution, the system outputs a beautiful PDF homebrew guidebook ready for your table.

**This is that system.**

---

## ✨ What Makes This Special

1. **Beings with Personalities** - Real demographics from Random User API + rich personality traits
2. **Evolutionary Excellence** - Campaigns improve through genetic algorithms (genome hashing, fitness evaluation, natural selection)
3. **Supreme Being Governance** - A PrimeBeing governs the realm with a Prime Directive
4. **Scarcity-Driven Evolution** - Limited resources (tokens, karma, time) create evolutionary pressure
5. **Beautiful Output** - Professional PDF homebrew guidebooks with evolution history
6. **Built on WAFT** - Leverages existing Being, Corporation, Realm, and Evolution systems

---

## 📚 Documentation

This work effort contains complete design documentation:

| Document | Purpose | Status |
|----------|---------|--------|
| **00_ARCHITECTURE.md** | Full system architecture, tech stack, data structures, algorithms | ✅ Complete |
| **01_MVP_REQUIREMENTS.md** | MVP scope, requirements, user stories, acceptance criteria | ✅ Complete |
| **02_DEVELOPER_GUIDE.md** | Developer onboarding, implementation guide, testing strategy | ✅ Complete |
| **03_PUBLIC_APIS.md** | Public APIs for Being personality generation | ✅ Complete |
| **README.md** | This file - executive summary and quick start | ✅ Complete |

---

## 🏗️ Architecture Overview

### The Big Picture

```
┌─────────────────────────────────────────────────────────────┐
│                  DUNGEON FORGE STUDIOS                       │
│              (Campaign Evolution Corporation)                │
├─────────────────────────────────────────────────────────────┤
│  Departments:                                                │
│  ├─ Scenario Design (create encounters)                     │
│  ├─ Lore & World-Building (create NPCs, lore)               │
│  └─ Quality Assurance (evaluate fitness)                    │
│                                                              │
│  Beings: 6 (2 per department)                                │
│  - Realistic personalities (Random User API)                │
│  - Role-specific skills                                     │
│  - Unique quirks and backgrounds                            │
│                                                              │
│  Supreme Being: The Grand Architect                          │
│  - Governs with Prime Directive                             │
│  - Allocates scarce resources                               │
│  - Approves final campaigns                                 │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  EVOLUTION PIPELINE                          │
├─────────────────────────────────────────────────────────────┤
│  1. GENESIS: Create initial campaign from seed               │
│  2. SPAWN: Beings propose mutations (improvements)           │
│  3. EVAL: Fitness testing (narrative, balance, content)      │
│  4. EVOLVE: Best variant selected, hot-swap                  │
│  5. REPEAT: For N generations or until scarcity limit        │
│  6. PUBLISH: Generate PDF homebrew guidebook                 │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                     OUTPUT                                   │
├─────────────────────────────────────────────────────────────┤
│  📄 PDF Homebrew Guidebook                                   │
│  ├─ Campaign narrative and lore                              │
│  ├─ All encounters (D&D stat blocks)                         │
│  ├─ All NPCs (character profiles)                            │
│  ├─ Evolution report:                                        │
│  │  ├─ Phylogenetic tree (lineage visualization)            │
│  │  ├─ Fitness progression graph                            │
│  │  └─ Generation-by-generation summary                     │
│  └─ Ready to play! 🎲                                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start (For Users)

Once implemented, here's how you'll use the system:

### 1. Initialize Corporation

```bash
$ waft campaign-corp init --name "Dungeon Forge Studios"

🏢 Creating Corporation: Dungeon Forge Studios
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Corporation created
✅ Realm initialized
✅ Supreme Being spawned: The Grand Architect

📊 Hiring Beings (6 total)...

Scenario Design Department:
  ✅ Alice Chen (Scenario Designer) - Photo: 👤
  ✅ Bob Martinez (Encounter Specialist) - Photo: 👤

Lore & World-Building Department:
  ✅ Carol Kim (Lore Writer) - Photo: 👤
  ✅ David O'Brien (World Builder) - Photo: 👤

Quality Assurance Department:
  ✅ Eve Patel (QA Tester) - Photo: 👤
  ✅ Frank Zhang (Balance Analyst) - Photo: 👤

✅ Corporation Ready!
Resource Budgets:
  - Tokens: 10,000
  - Karma: 1,000,000
  - Max Generations: 10
```

### 2. Evolve Campaign

```bash
$ waft campaign-corp evolve \
    --seed examples/campaign_seed_shattered_crown.json \
    --generations 5

🧬 Campaign Evolution Started
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📖 Campaign: The Shattered Crown
🎯 Target: 5 generations
📊 Genesis Fitness: 0.50

Generation 1/5 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Variants: 3
  Best Fitness: 0.58 (+0.08)
  Best Mutation: Enhanced villain backstory (Carol Kim, Lore Dept)

Generation 2/5 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Variants: 3
  Best Fitness: 0.64 (+0.06)
  Best Mutation: Added forest ambush encounter (Alice Chen, Scenario Dept)

Generation 3/5 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Variants: 3
  Best Fitness: 0.71 (+0.07)
  Best Mutation: Balanced reward progression (Eve Patel, QA Dept)

Generation 4/5 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Variants: 3
  Best Fitness: 0.76 (+0.05)
  Best Mutation: Added mysterious prophecy lore (David O'Brien, Lore Dept)

Generation 5/5 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Variants: 3
  Best Fitness: 0.82 (+0.06)
  Best Mutation: Enhanced NPC motivations (Bob Martinez, Scenario Dept)

✅ Evolution Complete!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Final Fitness: 0.82
Improvement: +64% (0.50 → 0.82)
Generations: 5
Variants Tested: 15

Campaign saved to:
_realms/dnd_campaign_evolution_realm/campaigns/the_shattered_crown/genome.json
```

### 3. Publish PDF

```bash
$ waft campaign-corp publish \
    --campaign the_shattered_crown \
    --output shattered_crown_guidebook.pdf

📄 Publishing: The Shattered Crown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Compiling campaign content...
✅ Generating phylogenetic tree...
✅ Creating fitness graphs...
✅ Rendering PDF with D&D template...

✅ Publication Complete!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

File: shattered_crown_guidebook.pdf
Size: 2.3 MB
Pages: 24

Campaign Stats:
  - Encounters: 7
  - NPCs: 8
  - Lore Entries: 12
  - Fitness: 0.82 (Excellent)
  - Evolution Generations: 5

🎲 Ready to play!
```

---

## 🛠️ Implementation Roadmap

### MVP Phases (4 Weeks)

| Phase | Component | Timeline | Complexity |
|-------|-----------|----------|------------|
| **Phase 1** | Campaign Genome | Week 1 | Medium |
| **Phase 2** | Being Personality Generator | Week 1-2 | Low |
| **Phase 3** | Fitness Evaluator | Week 2 | Medium |
| **Phase 4** | Scarcity Engine | Week 2 | Low |
| **Phase 5** | Evolution Orchestrator | Week 3 | High |
| **Phase 6** | PDF Publisher | Week 3-4 | Medium |
| **Phase 7** | CLI Commands | Week 4 | Low |
| **Phase 8** | Integration & Polish | Week 4 | Medium |

**Total Estimated Effort**: ~4 weeks full-time OR ~8 weeks part-time

---

## 📦 What's Already Built (Existing WAFT)

You're building on a solid foundation! WAFT already has:

✅ **Being System** - Timeful agents with skills, memories, lifecycle
✅ **Corporation System** - Departments, employees, financial state
✅ **Reality System** - Simulation environments
✅ **Realm System** - PrimeBeing governance
✅ **Evolutionary System** - Genome hashing, Flight Recorder, fitness tracking
✅ **D&D Scenario System** - Encounters, lore, NPCs, state management
✅ **PDF Templates** - Beautiful D&D scenario template
✅ **Science Integration** - Experimental iteration (science-bitch)

**You're adding**:
- Campaign genome representation
- Campaign fitness evaluation
- Being personality generation
- Scarcity mechanics
- Evolution orchestration
- PDF evolution reports

---

## 🎓 For Developers

### Prerequisites

- Python 3.12+
- Familiarity with WAFT framework
- Understanding of genetic algorithms (basic)
- TDD mindset (test-first development)

### Start Here

1. **Read**: `00_ARCHITECTURE.md` - Understand the system
2. **Read**: `01_MVP_REQUIREMENTS.md` - Know what to build
3. **Read**: `02_DEVELOPER_GUIDE.md` - Learn how to build it
4. **Code**: Start with Phase 1 (Campaign Genome)

### Development Setup

```bash
cd /home/user/waft
git checkout -b feature/campaign-evolution-corp
uv pip install -e ".[dev]"
pytest tests/  # Verify setup
```

### Key Files You'll Create

```python
src/waft/core/dnd_scenario/
├── campaign_genome.py              # Data structure + manager
├── campaign_fitness.py             # Fitness evaluation
├── campaign_evolution_corp.py      # Main orchestrator
├── being_personality_generator.py  # Personality generation
├── scarcity_engine.py             # Resource management
├── campaign_publisher.py          # PDF generation
└── supreme_being.py               # Governance

tests/test_campaign_evolution/
├── test_campaign_genome.py
├── test_campaign_fitness.py
├── test_personality_generation.py
├── test_scarcity_engine.py
└── test_campaign_evolution_integration.py
```

---

## 🔬 Technical Highlights

### Genome Hashing (SHA-256)

Every campaign has a unique genome ID:
```python
genome_id = sha256(
    campaign_name +
    narrative_arc +
    encounters +
    npcs +
    lore_entries
)
```

Same content = Same hash (deterministic lineage tracking)

### Fitness Evaluation (Multi-Dimensional)

```python
overall_fitness = (
    0.40 * narrative_coherence +   # Plot makes sense
    0.30 * content_completeness +  # Enough content
    0.30 * encounter_balance       # Difficulty progression
)
```

Threshold: fitness < 0.5 = DEATH (variant killed)

### Scarcity Mechanics

```python
# Limited resources drive evolution
scarcity_state = {
    "tokens": 10_000,        # Computation budget
    "karma": 1_000_000,      # Action budget
    "max_generations": 10    # Time budget
}

# Forces strategic mutations!
```

### Lineage Tracking (Phylogenetic Tree)

```
Genesis (gen 0, fitness 0.50)
  └─> Gen 1 (fitness 0.58, +villain backstory)
      └─> Gen 2 (fitness 0.64, +forest encounter)
          └─> Gen 3 (fitness 0.71, +balanced rewards)
              └─> Gen 4 (fitness 0.76, +prophecy lore)
                  └─> Gen 5 (fitness 0.82, +NPC motivations)
```

---

## 🎯 MVP Success Criteria

**The MVP is complete when**:

- [x] Corporation created with 3 departments, 6 Beings with personalities
- [x] Campaign evolves through 5+ generations
- [x] Fitness improves >20% from genesis to final
- [x] PDF guidebook generated with evolution report
- [x] Phylogenetic tree shows complete lineage
- [x] All unit tests pass (>80% coverage)
- [x] All integration tests pass
- [x] CLI commands work without errors
- [x] Documentation is complete

---

## 🚀 Beyond MVP (Future Versions)

**v2.0+**:
- Scint Gym integration (advanced fitness with LOGIC_FRACTURE detection)
- Real AI token tracking (OpenAI/Anthropic)
- Supreme Being active governance (dynamic resource allocation)
- Web dashboard (real-time evolution tracking)
- Multiple campaigns in parallel
- Advanced mutations (campaign restructuring)
- Being skill progression and autonomy
- Campaign marketplace (share evolved campaigns)

---

## 📊 Project Status

| Milestone | Status | Date |
|-----------|--------|------|
| Architecture Design | ✅ Complete | 2026-01-21 |
| MVP Requirements | ✅ Complete | 2026-01-21 |
| Developer Guide | ✅ Complete | 2026-01-21 |
| API Research | ✅ Complete | 2026-01-21 |
| **Ready for Implementation** | ✅ **YES** | 2026-01-21 |
| Phase 1: Campaign Genome | 🔲 Not Started | - |
| Phase 2: Personality Generator | 🔲 Not Started | - |
| Phase 3: Fitness Evaluator | 🔲 Not Started | - |
| Phase 4: Scarcity Engine | 🔲 Not Started | - |
| Phase 5: Evolution Orchestrator | 🔲 Not Started | - |
| Phase 6: PDF Publisher | 🔲 Not Started | - |
| Phase 7: CLI Commands | 🔲 Not Started | - |
| Phase 8: Integration & Polish | 🔲 Not Started | - |
| **MVP Complete** | 🔲 Target: 4 weeks | - |

---

## 🤝 Contributing

### Getting Started

1. Fork the repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Read `02_DEVELOPER_GUIDE.md` for implementation guide
4. Write tests first (TDD)
5. Implement to pass tests
6. Submit PR to `develop` branch

### Coding Standards

- **Test Coverage**: >80% for new code
- **Type Hints**: All functions must have type hints
- **Docstrings**: All public functions/classes
- **Linting**: Must pass `ruff check`
- **Formatting**: Use `ruff format`

---

## 📞 Questions?

**Documentation**:
- Architecture: `00_ARCHITECTURE.md`
- Requirements: `01_MVP_REQUIREMENTS.md`
- Dev Guide: `02_DEVELOPER_GUIDE.md`
- APIs: `03_PUBLIC_APIS.md`

**WAFT Framework**:
- Evolution: `/home/user/waft/docs/research/evolutionary_architecture.md`
- Being System: `/home/user/waft/src/waft/being.py`
- Corporation: `/home/user/waft/src/waft/core/corporations/`

**Stuck?**:
- Review existing WAFT code for patterns
- Check developer guide for troubleshooting
- Create GitHub issue with [question] tag

---

## 🌟 Why This Matters

This isn't just a D&D campaign generator. It's a **proof-of-concept for AI agent evolution**.

**What we're demonstrating**:
- ✅ AI Beings can work together in corporations
- ✅ Genetic algorithms can improve creative content
- ✅ Scarcity drives innovation
- ✅ Evolutionary systems produce measurable improvements
- ✅ Complete lineage tracking enables scientific study

**Applications beyond D&D**:
- Software development (evolving codebases)
- Content creation (evolving stories, games, art)
- Scientific research (evolving hypotheses)
- Business processes (evolving workflows)

**This is The Physics of Artificial Cognition in action.**

---

## 📜 License

Part of the WAFT (Waft - Ambient Meta-Framework) project.

See WAFT LICENSE for details.

---

## 🙏 Acknowledgments

Built on the incredible foundation of:
- **WAFT Framework** - The meta-framework for AI agent evolution
- **WAFT Beings** - Timeful, dynamic entities
- **WAFT Evolution** - Genome hashing and Flight Recorder
- **D&D 5e** - The world's greatest roleplaying game

---

## 🎲 Let's Build This!

**The design is complete. The documentation is thorough. The foundation is solid.**

**It's time to bring Dungeon Forge Studios to life.**

---

**Status**: ✅ **Design Phase Complete → Ready for Implementation**
**Next Step**: Begin Phase 1 (Campaign Genome) - See `02_DEVELOPER_GUIDE.md`
**Estimated Completion**: 4 weeks from start of implementation

---

**"The best campaigns aren't written—they evolve."**
— The Grand Architect, Supreme Being of the Campaign Evolution Realm
