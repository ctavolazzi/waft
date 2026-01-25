# D&D Campaign Evolution Corporation - Developer Onboarding Guide

**Date**: 2026-01-21
**Work Effort**: WE-260121-CAMPAIGN_EVOLUTION_CORP
**Purpose**: Get developers up and running quickly
**Audience**: WAFT developers building the campaign evolution system

---

## Welcome!

You're about to build an evolutionary D&D campaign creation system! This guide will get you started quickly.

**What you'll build**: A corporation of AI Beings that evolve D&D campaign scenarios through genetic algorithms, with fitness evaluation, scarcity mechanics, and PDF output.

**Time to MVP**: ~4 weeks (1 week per 2 phases)

---

## Prerequisites

### Required Knowledge
- ✅ Python 3.12+ (dataclasses, type hints, async/await)
- ✅ Object-oriented programming
- ✅ Basic understanding of genetic algorithms
- ✅ Familiarity with WAFT framework (Being, Corporation, Reality systems)

### Recommended Reading
1. WAFT Architecture docs: `/home/user/waft/docs/research/evolutionary_architecture.md`
2. Being System: `/home/user/waft/src/waft/being.py`
3. Corporation System: `/home/user/waft/src/waft/core/corporations/`
4. D&D Scenario System: `/home/user/waft/src/waft/core/dnd_scenario/`

### Development Environment

**Required Tools**:
```bash
# Python environment
python --version  # Should be 3.12+

# Package manager
uv --version  # WAFT uses uv

# Dev tools
ruff --version  # Linter
pytest --version  # Testing
```

**Setup**:
```bash
# Clone WAFT (if not already)
cd /home/user/waft

# Install dependencies
uv pip install -e ".[dev]"

# Run tests to verify setup
pytest tests/

# Should see all tests passing
```

---

## Project Structure

```
/home/user/waft/
├── src/waft/
│   ├── core/
│   │   ├── dnd_scenario/           # D&D scenario system (existing)
│   │   │   ├── __init__.py
│   │   │   ├── scenario_realm.py       ← Realm management (EXISTS)
│   │   │   ├── scenario_orchestrator.py ← Scenario execution (EXISTS)
│   │   │   ├── campaign_genome.py      ← YOU WILL CREATE
│   │   │   ├── campaign_fitness.py     ← YOU WILL CREATE
│   │   │   ├── campaign_evolution_corp.py ← YOU WILL CREATE
│   │   │   ├── being_personality_generator.py ← YOU WILL CREATE
│   │   │   ├── scarcity_engine.py      ← YOU WILL CREATE
│   │   │   ├── campaign_publisher.py   ← YOU WILL CREATE
│   │   │   └── supreme_being.py        ← YOU WILL CREATE
│   │   └── corporations/           # Corporation system (existing)
│   ├── being.py                    # Being system (existing)
│   ├── templates/
│   │   ├── dnd_scenario.py        # D&D PDF template (existing)
│   │   └── dnd_campaign_evolution.py ← YOU WILL CREATE
│   └── main.py                    # CLI (you'll add commands)
├── tests/
│   └── test_campaign_evolution/   ← YOU WILL CREATE
├── _realms/
│   └── dnd_campaign_evolution_realm/ ← Created at runtime
├── _work_efforts/
│   └── WE-260121-CAMPAIGN_EVOLUTION_CORP/ ← YOUR WORK EFFORT
│       ├── 00_ARCHITECTURE.md     ← Design doc (EXISTS)
│       ├── 01_MVP_REQUIREMENTS.md ← Requirements (EXISTS)
│       ├── 02_DEVELOPER_GUIDE.md  ← This file
│       ├── config/
│       │   └── personality_templates.yaml ← YOU WILL CREATE
│       └── examples/
│           └── campaign_seed_shattered_crown.json ← YOU WILL CREATE
└── pyproject.toml                 # Dependencies
```

---

## Development Workflow

### Step 1: Create Your Branch

```bash
cd /home/user/waft

# Create feature branch
git checkout -b feature/campaign-evolution-corp

# Verify you're on the right branch
git branch
```

### Step 2: Phase Development Cycle

For each development phase (see MVP Requirements):

1. **Read Requirements**: Review `01_MVP_REQUIREMENTS.md` for the phase
2. **Create Module**: Create the Python file(s) for the component
3. **Write Tests**: Write tests FIRST (TDD approach)
4. **Implement**: Implement the component to pass tests
5. **Manual Test**: Test manually via CLI or REPL
6. **Document**: Add docstrings and comments
7. **Commit**: Commit with clear message

**Example**:
```bash
# Phase 1: Campaign Genome

# 1. Create test file
touch tests/test_campaign_genome.py

# 2. Write tests (TDD)
# (Edit test_campaign_genome.py with test cases)

# 3. Create implementation file
touch src/waft/core/dnd_scenario/campaign_genome.py

# 4. Implement to pass tests
# (Edit campaign_genome.py)

# 5. Run tests
pytest tests/test_campaign_genome.py -v

# 6. Commit
git add tests/test_campaign_genome.py src/waft/core/dnd_scenario/campaign_genome.py
git commit -m "feat: implement CampaignGenome data structure and manager

- Add CampaignGenome dataclass with genome hashing
- Add CampaignGenomeManager for create/mutate/save/load
- Add lineage tracking
- 95% test coverage"
```

### Step 3: Testing Strategy

**Unit Tests** (required for all components):
```python
# tests/test_campaign_genome.py

import pytest
from waft.core.dnd_scenario.campaign_genome import (
    CampaignGenome,
    CampaignGenomeManager
)

def test_genesis_genome_creation():
    """Test creating a genesis genome from seed."""
    manager = CampaignGenomeManager()
    seed = {
        "campaign_name": "Test Campaign",
        "narrative_arc": {"plot_summary": "Hero saves kingdom"}
    }

    genome = manager.create_genesis_genome(seed)

    assert genome.generation == 0
    assert genome.parent_genome_id is None
    assert genome.genome_id is not None
    assert genome.campaign_name == "Test Campaign"

def test_genome_mutation_creates_child():
    """Test that mutation creates child genome with lineage."""
    manager = CampaignGenomeManager()
    parent = manager.create_genesis_genome({"campaign_name": "Parent"})

    mutation = {"type": "add_encounter", "encounter": {"name": "Forest Ambush"}}
    child = manager.mutate_genome(parent, mutation)

    assert child.generation == 1
    assert child.parent_genome_id == parent.genome_id
    assert len(child.lineage_path) == 2  # [parent, child]
    assert child.genome_id != parent.genome_id

# ... more tests
```

**Integration Tests** (required for orchestrator):
```python
# tests/test_campaign_evolution_integration.py

import pytest
from waft.core.dnd_scenario.campaign_evolution_corp import (
    CampaignEvolutionCorporation
)

def test_full_evolution_cycle():
    """Test complete evolution from genesis to PDF."""
    corp = CampaignEvolutionCorporation()
    corp.initialize_corporation()
    corp.hire_being_team(num_beings_per_dept=2)

    seed = {
        "campaign_name": "The Shattered Crown",
        "narrative_arc": {"plot_summary": "Restore the fallen kingdom"}
    }

    final_genome = corp.evolve_campaign(seed, num_generations=3)

    assert final_genome.generation == 3
    assert final_genome.fitness_score > 0.5
    assert len(final_genome.lineage_path) == 4  # genesis + 3 generations

    # Verify PDF generation
    pdf_path = corp.publish_campaign_pdf(final_genome)
    assert pdf_path.exists()
    assert pdf_path.stat().st_size > 0
```

**Manual Testing** (for debugging):
```python
# Quick REPL test
from waft.core.dnd_scenario.campaign_genome import CampaignGenomeManager

manager = CampaignGenomeManager()
genome = manager.create_genesis_genome({"campaign_name": "Test"})
print(genome)
print(f"Genome ID: {genome.genome_id}")
```

### Step 4: Code Style & Quality

**Linting** (use ruff):
```bash
# Check code style
ruff check src/waft/core/dnd_scenario/

# Fix auto-fixable issues
ruff check --fix src/waft/core/dnd_scenario/

# Format code
ruff format src/waft/core/dnd_scenario/
```

**Type Checking** (recommended):
```bash
# Optional but recommended
mypy src/waft/core/dnd_scenario/campaign_genome.py
```

**Docstrings** (required):
```python
def calculate_genome_hash(genome: CampaignGenome) -> str:
    """
    Calculate SHA-256 hash of campaign genome content.

    The hash is deterministic - same content always produces same hash.
    Used for genome identification and lineage tracking.

    Args:
        genome: Campaign genome to hash

    Returns:
        SHA-256 hash string (64 hex characters)

    Example:
        >>> genome = create_genesis_genome({"campaign_name": "Test"})
        >>> hash1 = calculate_genome_hash(genome)
        >>> hash2 = calculate_genome_hash(genome)
        >>> assert hash1 == hash2  # Deterministic
    """
    # Implementation
```

---

## Phase-by-Phase Implementation Guide

### Phase 1: Campaign Genome (Week 1)

**Files to Create**:
- `src/waft/core/dnd_scenario/campaign_genome.py`
- `tests/test_campaign_genome.py`
- `examples/campaign_seed_shattered_crown.json`

**Implementation Steps**:

1. **Define CampaignGenome dataclass**:
```python
# src/waft/core/dnd_scenario/campaign_genome.py

from dataclasses import dataclass, field
from datetime import datetime
import hashlib
import json

@dataclass
class CampaignGenome:
    """Represents the complete genome of a D&D campaign."""

    # Core identity
    genome_id: str
    parent_genome_id: str | None
    generation: int
    created_at: datetime = field(default_factory=datetime.utcnow)

    # Campaign content (the "DNA")
    campaign_name: str = ""
    narrative_arc: dict = field(default_factory=dict)
    encounters: list[dict] = field(default_factory=list)
    npcs: list[dict] = field(default_factory=list)
    lore_entries: list[dict] = field(default_factory=list)

    # Evolutionary metadata
    lineage_path: list[str] = field(default_factory=list)
    mutations: list[dict] = field(default_factory=list)
    fitness_score: float | None = None

    # Attribution
    created_by_being_id: str = "system"
    department: str = "genesis"

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        # Implementation

    @classmethod
    def from_dict(cls, data: dict) -> "CampaignGenome":
        """Deserialize from dictionary."""
        # Implementation
```

2. **Define CampaignGenomeManager**:
```python
class CampaignGenomeManager:
    """Manages campaign genome creation, mutation, and persistence."""

    def __init__(self, realm_path: Path):
        self.realm_path = realm_path
        self.campaigns_path = realm_path / "campaigns"
        self.campaigns_path.mkdir(parents=True, exist_ok=True)

    def create_genesis_genome(self, seed: dict) -> CampaignGenome:
        """Create initial genesis genome from seed."""
        # Implementation:
        # 1. Extract campaign_name, narrative_arc, etc. from seed
        # 2. Create CampaignGenome with generation=0, parent_genome_id=None
        # 3. Calculate genome_id hash
        # 4. Set lineage_path = [genome_id]
        # 5. Save to disk
        # 6. Return genome

    def mutate_genome(
        self,
        parent: CampaignGenome,
        mutation: dict
    ) -> CampaignGenome:
        """Create child genome by applying mutation to parent."""
        # Implementation:
        # 1. Copy parent content
        # 2. Apply mutation (e.g., add encounter, enhance NPC)
        # 3. Create new CampaignGenome with generation=parent.generation+1
        # 4. Set parent_genome_id = parent.genome_id
        # 5. Calculate new genome_id hash
        # 6. Update lineage_path = parent.lineage_path + [new genome_id]
        # 7. Record mutation in mutations list
        # 8. Save to disk
        # 9. Return child

    def calculate_genome_hash(self, genome: CampaignGenome) -> str:
        """Calculate SHA-256 hash of genome content."""
        # Implementation:
        # 1. Create dict of hashable content (narrative, encounters, npcs, lore)
        # 2. Serialize to JSON (sorted keys for determinism)
        # 3. Calculate SHA-256 hash
        # 4. Return hex string

    def save_genome(self, genome: CampaignGenome) -> Path:
        """Save genome to disk."""
        # Implementation:
        # 1. Create campaign directory
        # 2. Write genome to genome.json
        # 3. Return path

    def load_genome(self, genome_id: str) -> CampaignGenome | None:
        """Load genome from disk."""
        # Implementation

    def get_lineage(self, genome_id: str) -> list[CampaignGenome]:
        """Get complete lineage from genesis to genome."""
        # Implementation:
        # 1. Load genome
        # 2. For each genome_id in lineage_path, load genome
        # 3. Return list in order
```

3. **Write Tests**:
```python
# tests/test_campaign_genome.py

# Test cases:
# - test_genesis_genome_creation
# - test_genome_hash_is_deterministic
# - test_mutation_creates_child_with_lineage
# - test_save_and_load_genome
# - test_get_complete_lineage
```

4. **Create Example Seed**:
```json
{
  "campaign_name": "The Shattered Crown",
  "narrative_arc": {
    "plot_summary": "The kingdom has fallen to darkness. The king's crown was shattered into three pieces. The heroes must recover the pieces and restore the rightful heir.",
    "main_villain": "Lord Malachar, the Shadow King",
    "heroic_goal": "Recover the three crown pieces and restore the kingdom"
  },
  "encounters": [
    {
      "name": "Tavern Meeting",
      "description": "Heroes meet mysterious hooded figure with quest information",
      "difficulty": 1,
      "rewards": "100 gold, map to first crown piece"
    }
  ],
  "npcs": [
    {
      "name": "Elder Thorne",
      "role": "Quest Giver",
      "personality": "Wise but secretive",
      "backstory": "Former royal advisor who knows the crown's secret"
    }
  ],
  "lore_entries": [
    {
      "title": "The Shattered Crown Legend",
      "content": "Long ago, the crown was forged by three master smiths..."
    }
  ]
}
```

**Deliverable**: Working genome system with tests passing.

---

### Phase 2: Being Personality Generator (Week 1-2)

**Files to Create**:
- `src/waft/core/dnd_scenario/being_personality_generator.py`
- `config/personality_templates.yaml`
- `tests/test_personality_generation.py`

**Implementation Steps**:

1. **Create Personality Templates**:
```yaml
# config/personality_templates.yaml

scenario_designer:
  skills:
    campaign_design: 7.0
    encounter_balance: 6.0
    creativity: 8.0
  quirks:
    - "Loves plot twists"
    - "Detail-oriented about monster stats"
    - "Always asks 'but what if...?'"
  role_traits:
    - "Imaginative"
    - "Strategic thinker"
    - "Story-driven"

lore_writer:
  skills:
    lore_writing: 8.0
    world_building: 7.0
    storytelling: 9.0
  quirks:
    - "Obsessed with historical accuracy"
    - "Collects interesting character names"
    - "Mythology enthusiast"
  role_traits:
    - "Creative"
    - "Detail-oriented"
    - "Patient"

qa_tester:
  skills:
    quality_testing: 8.0
    critical_thinking: 7.0
    attention_to_detail: 9.0
  quirks:
    - "Finds every edge case"
    - "Skeptical by nature"
    - "Loves making checklists"
  role_traits:
    - "Analytical"
    - "Thorough"
    - "Perfectionist"
```

2. **Implement Generator**:
```python
# src/waft/core/dnd_scenario/being_personality_generator.py

import httpx
import yaml
from pathlib import Path
from dataclasses import dataclass

@dataclass
class BeingPersonalityProfile:
    """Personality profile for a Being."""
    being_id: str
    name: str
    demographics: dict
    personality_traits: dict
    skills: dict[str, float]
    role: str
    title: str
    quirks: list[str]
    department: str

class BeingPersonalityGenerator:
    """Generates Being personalities from public APIs and templates."""

    def __init__(self, templates_path: Path):
        self.templates_path = templates_path
        self.templates = self._load_templates()

    def _load_templates(self) -> dict:
        """Load personality templates from YAML."""
        with open(self.templates_path, 'r') as f:
            return yaml.safe_load(f)

    async def generate_personality(
        self,
        role: str,
        department: str
    ) -> BeingPersonalityProfile:
        """Generate complete personality profile."""
        # 1. Get demographics from Random User API
        demographics = await self._fetch_demographics()

        # 2. Get role template
        role_key = role.lower().replace(" ", "_")
        template = self.templates.get(role_key, {})

        # 3. Create profile
        being_id = f"being_{department}_{uuid.uuid4().hex[:8]}"
        name = f"{demographics['first_name']} {demographics['last_name']}"

        profile = BeingPersonalityProfile(
            being_id=being_id,
            name=name,
            demographics=demographics,
            personality_traits=template.get("role_traits", []),
            skills=template.get("skills", {}),
            role=role,
            title=self._generate_title(role, department),
            quirks=template.get("quirks", []),
            department=department
        )

        return profile

    async def _fetch_demographics(self) -> dict:
        """Fetch demographics from Random User API."""
        async with httpx.AsyncClient() as client:
            resp = await client.get("https://randomuser.me/api/")
            data = resp.json()["results"][0]

            return {
                "first_name": data["name"]["first"],
                "last_name": data["name"]["last"],
                "age": data["dob"]["age"],
                "nationality": data["nat"],
                "photo_url": data["picture"]["large"],
                "gender": data["gender"],
                "location": data["location"]["city"]
            }

    def _generate_title(self, role: str, department: str) -> str:
        """Generate job title."""
        titles = {
            "scenario_designer": ["Senior Campaign Architect", "Lead Scenario Designer", "Campaign Engineer"],
            "lore_writer": ["Master Lorekeeper", "World-Building Specialist", "Narrative Designer"],
            "qa_tester": ["Quality Assurance Lead", "Campaign Validator", "Balance Analyst"]
        }

        role_key = role.lower().replace(" ", "_")
        return random.choice(titles.get(role_key, [role]))
```

3. **Write Tests**:
```python
# tests/test_personality_generation.py

@pytest.mark.asyncio
async def test_generate_personality():
    """Test personality generation."""
    generator = BeingPersonalityGenerator(Path("config/personality_templates.yaml"))

    profile = await generator.generate_personality(
        role="Scenario Designer",
        department="Scenario Design"
    )

    assert profile.being_id.startswith("being_scenario_design")
    assert profile.name  # Should have name from API
    assert "campaign_design" in profile.skills
    assert len(profile.quirks) >= 2
```

**Deliverable**: Personality generator with Random User API integration.

---

### Phase 3-8: Similar Implementation Guides

(See MVP Requirements doc for detailed requirements for each phase)

**General Pattern**:
1. Define data structures (dataclasses)
2. Implement core logic
3. Write unit tests (TDD)
4. Write integration tests
5. Document with docstrings
6. Manual testing via CLI/REPL

---

## Debugging & Troubleshooting

### Common Issues

**Issue 1: Tests failing with "Module not found"**
```bash
# Solution: Install package in editable mode
uv pip install -e .

# Or add to PYTHONPATH
export PYTHONPATH=/home/user/waft/src:$PYTHONPATH
```

**Issue 2: Random User API rate limit**
```python
# Solution: Add caching
import json
from pathlib import Path

CACHE_FILE = Path("_temp/demographics_cache.json")

async def _fetch_demographics_with_cache(self):
    if CACHE_FILE.exists():
        # Use cached data
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)

    # Fetch from API
    data = await self._fetch_demographics()

    # Cache for next time
    CACHE_FILE.parent.mkdir(exist_ok=True)
    with open(CACHE_FILE, 'w') as f:
        json.dump(data, f)

    return data
```

**Issue 3: PDF generation fails**
```python
# Solution: Test HTML generation first
html_content = publisher.generate_html(campaign)
Path("debug_output.html").write_text(html_content)
# Open debug_output.html in browser to check formatting
```

**Issue 4: Fitness not improving**
```python
# Solution: Add debug logging
import logging

logging.basicConfig(level=logging.DEBUG)

# In evolution loop:
logger.debug(f"Generation {gen}: Best fitness {best_fitness}")
logger.debug(f"Mutation: {mutation}")
logger.debug(f"Fitness components: {fitness_metrics}")

# This will help diagnose why fitness isn't improving
```

---

## Testing Checklist

Before committing each phase:

- [ ] All unit tests pass (`pytest tests/test_*.py`)
- [ ] Code coverage >80% for new code (`pytest --cov`)
- [ ] Linting passes (`ruff check src/`)
- [ ] Type hints added to all functions
- [ ] Docstrings added to all public functions/classes
- [ ] Manual testing completed (CLI or REPL)
- [ ] Edge cases tested (empty inputs, None values, etc.)
- [ ] Error handling tested (API failures, disk errors, etc.)

---

## Git Workflow

**Branching Strategy**:
- `main` - Production code
- `develop` - Integration branch
- `feature/campaign-evolution-corp` - Your feature branch

**Commit Messages**:
```
feat: add campaign genome data structure

- Implement CampaignGenome dataclass with hashing
- Implement CampaignGenomeManager for CRUD operations
- Add lineage tracking
- Add tests with 95% coverage

Closes #123
```

**PR Process**:
1. Create PR from `feature/campaign-evolution-corp` → `develop`
2. Add description summarizing changes
3. Request review from team
4. Address review feedback
5. Merge when approved

---

## Resources

### Documentation
- Architecture: `00_ARCHITECTURE.md`
- MVP Requirements: `01_MVP_REQUIREMENTS.md`
- WAFT Evolution Docs: `/home/user/waft/docs/research/evolutionary_architecture.md`

### Code Examples
- Being System: `/home/user/waft/src/waft/being.py`
- Corporation: `/home/user/waft/src/waft/core/corporations/corporation.py`
- D&D Scenario: `/home/user/waft/src/waft/core/dnd_scenario/scenario_orchestrator.py`

### External APIs
- Random User API: https://randomuser.me/
- Documentation: https://randomuser.me/documentation

### Python Libraries
- httpx: https://www.python-httpio.org/
- Pydantic: https://docs.pydantic.dev/
- WeasyPrint: https://doc.courtbouillon.org/weasyprint/
- matplotlib: https://matplotlib.org/

---

## Getting Help

**Stuck on something?**
1. Check existing WAFT code for similar patterns
2. Review architecture/requirements docs
3. Read library documentation
4. Ask in team chat
5. Create GitHub issue with [question] tag

**Found a bug?**
1. Create minimal reproduction case
2. Add debug logging
3. Check if it's a known issue
4. Create GitHub issue with details

---

## Summary

**You're now ready to build the Campaign Evolution Corporation!**

**Next Steps**:
1. Review architecture (`00_ARCHITECTURE.md`)
2. Review MVP requirements (`01_MVP_REQUIREMENTS.md`)
3. Set up development environment
4. Start with Phase 1 (Campaign Genome)
5. Follow TDD approach (tests first!)
6. Commit regularly with clear messages

**Remember**:
- MVP scope: Keep it simple, defer advanced features
- TDD: Write tests first
- Documentation: Clear docstrings and comments
- Quality: >80% test coverage, passing linting

**Good luck! You've got this! 🚀**

---

**Status**: ✅ Developer Guide Complete
**Ready For**: Implementation
