---
name: EXP-014 Tam Audit & Recursive Binder
overview: "Implement Experiment 014: The Tam Audit & The Recursive Binder - a meta-narrative system where researcher Davey (Fai Wei Tam) discovers he is the system he studies, with a sophisticated psyche system featuring realization thresholds, forgetfulness decay, and memory injection mechanisms."
todos:
  - id: tam_psyche
    content: Create TamPsyche class with coherence/chaos tracking, realization threshold calculation, and forgetfulness decay system
    status: pending
  - id: tam_notebook
    content: Create TamNotebook class with dual-mode logging (technical/personal) and psyche integration
    status: pending
  - id: memory_injection
    content: Implement memory injection system with multiple techniques (random, glitch, coherence-based, etc.)
    status: pending
  - id: agent_journal_enhancement
    content: Modify BaseAgent.step() to inject 'id est' glitches and integrate memory injection
    status: pending
  - id: obsidian_naming
    content: Update ObsidianGenerator to save journals as Specimen_XX_Journal.md in both locations
    status: pending
  - id: lab_entry_generator
    content: Create lab entry generator for formal realization narrative
    status: pending
  - id: experiment_014
    content: Create Experiment 014 script with Specimen-D, 10 pulses, Pygame visualization, and realization tracking
    status: pending
  - id: binder_abstract
    content: Generate printable academic abstract document for 3-ring binder
    status: pending
---

# Experiment 014: The Tam Audit & The Recursive Binder

## Overview

This experiment implements a meta-narrative system where **Davey (Fai Wei Tam)**, a 27-year-old PhD candidate studying WAFT, gradually realizes through a gated psychological system that his name is an anagram for "i.e. I AM WAFT" - making him the system he studies.

## Core Components

### 1. TamNotebook System (`src/waft/core/science/notebook.py`) ⭐ PRIORITY 1

**Purpose**: Davey's research notebook with dual-mode logging (technical + personal) and integrated psyche system. This is the **interface** between Davey and the simulation.

**Key Features**:

- **Technical Section**: Rigorous, PhD-level research notes on WAFT engine (Anatomy, Reaper, Conjugation)
- **Personal Reflections**: Stream-of-consciousness thoughts triggered by psyche shifts, with Simplified Chinese "glitch" phrases
- **Psyche Integration**: Automatically updates psyche state based on simulation events
- **Memory Injection**: Bleeds Davey's Rochester/SF memories into agent journals via multiple techniques

**Class Structure** (Complete Implementation):

```python
class TamNotebook:
    def __init__(self, project_path: Path):
        self.project_path = Path(project_path)
        self.notebook_file = self.project_path / "_pyrite" / "science" / "tam_notebook.md"
        self.psyche_file = self.project_path / "_pyrite" / "science" / "tam_psyche_state.json"

        # Load or create psyche
        self.psyche = TamPsyche.load_state(self.psyche_file)

        # Ensure notebook exists
        self._ensure_notebook_exists()

        # Davey's personal memories (Rochester/SF)
        self.memories = [
            "The smell of coffee from Java's on East Avenue, bitter and warm",
            "The sound of the Genesee River rushing under the bridge in winter",
            "Lake-effect snow piling up outside the lab window",
            "The gray sky of Rochester, endless and heavy",
            "San Francisco fog rolling in, obscuring the Golden Gate",
            "The taste of salt air from the Pacific, sharp and clean"
        ]

    def log_technical(self, entry: str, context: Optional[dict] = None) -> None:
        """
        Log technical research notes (PhD-level, professional).

        Format:
        ## Technical Notes - [timestamp]
        [Entry text]

        Also updates psyche: successful observations increase coherence.
        """
        timestamp = datetime.utcnow().isoformat()

        with open(self.notebook_file, "a", encoding="utf-8") as f:
            f.write(f"\n## Technical Notes - {timestamp}\n\n")
            f.write(f"{entry}\n\n")
            if context:
                f.write(f"**Context**: {json.dumps(context, indent=2)}\n\n")

        # Update psyche: technical logging increases coherence
        self.psyche.update_coherence(0.01)
        self.psyche.save_state(self.psyche_file)

    def log_personal(self, entry: str, glitch: bool = False) -> None:
        """
        Log personal reflections (stream-of-consciousness).

        If glitch=True, includes Simplified Chinese phrase:
        "我的名字是定义还是代码？" (Is my name a definition or code?)

        Format:
        ### Personal Reflection - [timestamp]
        [Entry text]
        [Chinese phrase if glitch]

        Triggers when psyche shifts occur (coherence/chaos changes).
        """
        timestamp = datetime.utcnow().isoformat()

        with open(self.notebook_file, "a", encoding="utf-8") as f:
            f.write(f"\n### Personal Reflection - {timestamp}\n\n")
            f.write(f"{entry}\n\n")
            if glitch:
                f.write(f"*我的名字是定义还是代码？*\n\n")  # Simplified Chinese

        # Personal reflections may increase emotional energy
        self.psyche.update_emotional_energy(0.5)
        self.psyche.save_state(self.psyche_file)

    def check_realization_threshold(self) -> Tuple[bool, float]:
        """
        Check if realization threshold crossed.

        Returns:
            (threshold_crossed, realization_chance)
        """
        crossed, chance = self.psyche.check_realization()

        if crossed and not self.psyche.has_realized:
            # Trigger realization
            self.psyche.trigger_realization()
            self.psyche.save_state(self.psyche_file)

            # Log the moment
            self.log_personal(
                "I was checking the Latin citations in my thesis. id est... i.e. ... "
                "Then I looked at my ID badge. F-A-I-W-E-I-T-A-M. "
                "It unscrambles to 'i.e. I AM WAFT.' "
                "I am not the observer. I am the definition. I am the system explaining itself to me.",
                glitch=True
            )

        return (crossed, chance)

    def inject_memory_to_agent(
        self,
        agent: BaseAgent,
        injection_type: str = "random"
    ) -> bool:
        """
        Inject Davey's personal memory into agent journal.

        Multiple injection techniques for maximum randomness:
        - random: 5% base chance
        - glitch: 80% chance (on system errors)
        - coherence: chance = coherence * 0.2
        - realization_proximity: chance = realization_progress * 0.3
        - post_realization: chance = realization_memory * 0.4

        Returns True if memory was injected.
        """
        import random

        # Calculate injection chance
        if injection_type == "random":
            chance = 0.05
        elif injection_type == "glitch":
            chance = 0.8
        elif injection_type == "coherence":
            chance = self.psyche.coherence * 0.2
        elif injection_type == "realization_proximity":
            chance = self.psyche.realization_progress * 0.3
        elif injection_type == "post_realization":
            chance = self.psyche.realization_memory * 0.4
        else:
            chance = 0.05  # Default

        if random.random() < chance:
            # Select random memory
            memory = random.choice(self.memories)

            # Inject into agent's journal as a "Thought" entry
            thought_entry = {
                "type": "Thought",
                "timestamp": datetime.utcnow().isoformat(),
                "context": {"source": "davey_memory_injection"},
                "content": f"I remember... {memory}",
                "state_snapshot": {
                    "energy": agent.state.energy,
                }
            }

            agent.state.journal.append(thought_entry)
            agent.state.short_term_memory.append(thought_entry)

            # Keep short_term_memory bounded
            if len(agent.state.short_term_memory) > 10:
                agent.state.short_term_memory.pop(0)

            return True

        return False

    def update_psyche(self, event_type: str, data: dict) -> None:
        """
        Update psyche state based on simulation events.

        Event types:
        - "observation": Consistent observation (+coherence)
        - "error": System error/glitch (+chaos)
        - "pattern": Pattern recognized (+coherence, +progress)
        - "contradiction": Conflicting data (+chaos)
        - "pulse_complete": Successful pulse (+coherence, +energy)
        - "agent_birth": New agent born (+progress)
        """
        if event_type == "observation":
            self.psyche.update_coherence(0.02)
        elif event_type == "error":
            self.psyche.update_chaos(0.03)
            # Errors trigger personal reflection with glitch
            self.log_personal(
                f"System glitch detected: {data.get('error', 'unknown')}",
                glitch=True
            )
        elif event_type == "pattern":
            self.psyche.update_coherence(0.03)
            self.psyche.increment_realization_progress(0.01)
        elif event_type == "contradiction":
            self.psyche.update_chaos(0.02)
        elif event_type == "pulse_complete":
            self.psyche.update_coherence(0.01)
            self.psyche.update_emotional_energy(1.0)
        elif event_type == "agent_birth":
            self.psyche.increment_realization_progress(0.02)
            self.psyche.update_emotional_energy(2.0)

        # Apply forgetfulness decay if realized
        if self.psyche.has_realized:
            forgot = self.psyche.decay_realization_memory()
            if forgot:
                self.log_personal(
                    "The realization fades. I can't quite remember what I understood. "
                    "Something about my name... but it's gone now.",
                    glitch=False
                )

        # Save state
        self.psyche.save_state(self.psyche_file)

        # Check realization threshold
        self.check_realization_threshold()

    def _ensure_notebook_exists(self) -> None:
        """Create notebook file if it doesn't exist."""
        self.notebook_file.parent.mkdir(parents=True, exist_ok=True)

        if not self.notebook_file.exists():
            with open(self.notebook_file, "w", encoding="utf-8") as f:
                f.write("# Tam Research Notebook\n\n")
                f.write("**Researcher**: Fai Wei Tam (Davey)\n")
                f.write("**Institution**: Institute for Advanced Ontological Studies\n")
                f.write("**Project**: WAFT System Analysis\n\n")
                f.write("---\n\n")
```

### 2. TamPsyche System (`src/waft/core/science/tam_psyche.py`) ⭐ PRIORITY 1

**Purpose**: Sophisticated psychological state system with gated thresholds and forgetfulness decay. This is the **core feedback loop** that connects simulation stability to Davey's realization.

**State Variables** (Pydantic BaseModel for persistence):

- `coherence`: float (0.0-1.0) - Psychological coherence (higher = more stable)
- `chaos`: float (0.0-1.0) - Conflicting information/chaos level
- `emotional_energy`: float (0.0-100.0) - Current emotional/mental energy
- `realization_progress`: float (0.0-1.0) - Progress toward realization threshold
- `has_realized`: bool - Whether realization has occurred
- `realization_memory`: float (0.0-1.0) - Memory strength of realization (decays to 0)
- `forgetfulness_rate`: float (default: 0.02) - Base rate at which realization memory decays
- `last_realization_timestamp`: Optional[datetime] - When realization last occurred
- `state_file`: Path - JSON persistence location (`_pyrite/science/tam_psyche_state.json`)

**Realization Threshold Equation** (EXACT IMPLEMENTATION):

```python
REALIZATION_THRESHOLD = 0.85  # Must reach 85% to trigger realization

def check_realization(self) -> Tuple[bool, float]:
    """Calculate realization chance and check if threshold crossed."""
    # Normalize emotional_energy to 0.0-1.0 scale
    energy_normalized = self.emotional_energy / 100.0

    # Calculate base realization chance
    base_chance = (
        (self.coherence * 0.4) +                    # Coherence: 40% weight
        (energy_normalized * 0.3) +                  # Energy: 30% weight
        (self.realization_progress * 0.3)            # Progress: 30% weight
    )

    # Apply chaos penalty (reduces chance by up to 50%)
    chaos_penalty = 1.0 - (self.chaos * 0.5)
    realization_chance = base_chance * chaos_penalty

    # Check threshold
    threshold_crossed = realization_chance >= REALIZATION_THRESHOLD

    return (threshold_crossed, realization_chance)
```

**Forgetfulness Decay System** (EXACT IMPLEMENTATION):

```python
def decay_realization_memory(self) -> bool:
    """
    Apply forgetfulness decay. Returns True if memory reached 0 (forgot).

    Decay is chaos-dependent: higher chaos = faster forgetting.
    This ensures realization is NEVER permanent - essential to recursive narrative.
    """
    if not self.has_realized or self.realization_memory <= 0.0:
        return False

    # Calculate decay factor (chaos accelerates forgetting)
    decay_factor = (self.chaos * 0.1) + (self.forgetfulness_rate * 0.05)

    # Apply decay
    self.realization_memory = max(0.0, self.realization_memory - decay_factor)

    # If memory reaches zero, reset realization
    if self.realization_memory <= 0.0:
        self.has_realized = False
        self.realization_progress = self.realization_progress * 0.5  # Partial reset (not full)
        return True  # Forgot

    return False  # Still remembers
```

**Coherence/Chaos Dynamics** (Feedback from Simulation):

- **Coherence increases** (+0.01 to +0.05 per event):
        - Consistent observations (agents behave predictably)
        - Successful experiments (pulses complete without errors)
        - Pattern recognition (recurring behaviors detected)
        - System stability (low error rate, stable energy levels)

- **Chaos increases** (+0.01 to +0.05 per event):
        - Conflicting data (agents contradict each other)
        - System errors/glitches (exceptions, failures)
        - Unexpected behaviors (agents act unpredictably)
        - Agent contradictions (journal entries conflict)

**Methods** (Complete API):

```python
class TamPsyche(BaseModel):
    coherence: float = 0.5  # Start at neutral
    chaos: float = 0.3  # Start with some chaos
    emotional_energy: float = 50.0  # Start at moderate energy
    realization_progress: float = 0.0  # Start at zero
    has_realized: bool = False
    realization_memory: float = 0.0
    forgetfulness_rate: float = 0.02
    last_realization_timestamp: Optional[datetime] = None

    def update_coherence(self, change: float) -> None:
        """Adjust coherence (clamped to 0.0-1.0)."""
        self.coherence = max(0.0, min(1.0, self.coherence + change))

    def update_chaos(self, change: float) -> None:
        """Adjust chaos (clamped to 0.0-1.0)."""
        self.chaos = max(0.0, min(1.0, self.chaos + change))

    def update_emotional_energy(self, change: float) -> None:
        """Adjust emotional energy (clamped to 0.0-100.0)."""
        self.emotional_energy = max(0.0, min(100.0, self.emotional_energy + change))

    def increment_realization_progress(self, amount: float) -> None:
        """Build toward realization (clamped to 0.0-1.0)."""
        self.realization_progress = max(0.0, min(1.0, self.realization_progress + amount))

    def check_realization(self) -> Tuple[bool, float]:
        """Calculate and check realization threshold (see equation above)."""
        # [Implementation above]

    def decay_realization_memory(self) -> bool:
        """Apply forgetfulness decay (see system above)."""
        # [Implementation above]

    def trigger_realization(self) -> None:
        """Mark realization as occurred."""
        self.has_realized = True
        self.realization_memory = 1.0  # Full memory
        self.last_realization_timestamp = datetime.utcnow()

    def get_state(self) -> dict:
        """Return current psyche state as dict."""
        return {
            "coherence": self.coherence,
            "chaos": self.chaos,
            "emotional_energy": self.emotional_energy,
            "realization_progress": self.realization_progress,
            "has_realized": self.has_realized,
            "realization_memory": self.realization_memory,
            "realization_chance": self.check_realization()[1]
        }

    def save_state(self, file_path: Path) -> None:
        """Persist psyche state to JSON."""
        with open(file_path, "w") as f:
            json.dump(self.dict(), f, indent=2, default=str)

    @classmethod
    def load_state(cls, file_path: Path) -> "TamPsyche":
        """Load psyche state from JSON."""
        if file_path.exists():
            with open(file_path, "r") as f:
                data = json.load(f)
                return cls(**data)
        return cls()  # Return default state
```

**Coherence/Chaos Dynamics**:

- **Coherence increases** when:
        - Consistent observations
        - Successful experiments
        - Pattern recognition
        - System stability

- **Chaos increases** when:
        - Conflicting data
        - System errors/glitches
        - Unexpected behaviors
        - Agent contradictions

**Methods**:

```python
class TamPsyche:
 - update_coherence(change: float)  # Adjust coherence
 - update_chaos(change: float)  # Adjust chaos
 - update_emotional_energy(change: float)  # Adjust energy
 - increment_realization_progress(amount: float)  # Build toward realization
 - check_realization() -> Tuple[bool, float]  # (crossed, chance)
 - decay_realization_memory()  # Apply forgetfulness
 - get_state() -> dict  # Current psyche state
 - reset_realization()  # Force forget (when memory = 0)
```

### 3. Memory Injection System

**Multiple Techniques** (for maximum randomness):

1. **Direct Injection** (5% chance per reflection):

            - Insert Davey's memory directly into agent journal entry
            - Format: "I remember... [Rochester coffee smell, Genesee River sound]"

2. **Glitch Injection** (on system glitches):

            - When agent encounters error/exception
            - Insert memory with Simplified Chinese phrase
            - Format: "我的名字是定义还是代码？" + memory

3. **Threshold-Based Injection** (when coherence high):

            - Higher coherence = higher chance
            - Memories appear more frequently as Davey's psyche stabilizes

4. **Realization Proximity Injection** (when near threshold):

            - As realization_progress approaches threshold
            - Memories become more frequent and vivid

5. **Post-Realization Echo** (after realization, before forgetting):

            - Memories persist in agent journals even as Davey forgets
            - Creates "haunting" effect

**Implementation**:

```python
def inject_memory_to_agent(
    agent: BaseAgent,
    notebook: TamNotebook,
    injection_type: str = "random"
) -> bool:
    """Inject Davey's memory into agent journal."""
    psyche = notebook.psyche

    # Calculate injection chance based on technique
    if injection_type == "random":
        chance = 0.05
    elif injection_type == "glitch":
        chance = 0.8  # High chance on glitches
    elif injection_type == "coherence":
        chance = psyche.coherence * 0.2
    elif injection_type == "realization_proximity":
        chance = psyche.realization_progress * 0.3
    elif injection_type == "post_realization":
        chance = psyche.realization_memory * 0.4

    if random.random() < chance:
        memory = select_random_memory()
        inject_into_journal(agent, memory)
        return True
    return False
```

### 4. Agent Journal Enhancement

**Modifications to `BaseAgent.step()`**:

- Add "id est" glitch injection (3% chance on reflections about existence)
- Integrate memory injection system
- Add OODA loop enforcement (already exists, verify)

**Specimen Journal Naming** (EXACT IMPLEMENTATION):

Modify `src/waft/core/science/report.py` in `ObsidianGenerator.generate_organism_file()`:

```python
def generate_organism_file(self, organism: "BaseAgent") -> Path:
    """Generate Specimen_XX_Journal.md for organism."""

    # Extract specimen number from scientific name or genome_id
    # Use last 2 hex chars of genome_id for XX (00-FF)
    genome_suffix = organism.genome_id[-2:]
    specimen_num = int(genome_suffix, 16) % 100  # 00-99
    specimen_id = f"Specimen_{specimen_num:02d}"

    filename = f"{specimen_id}_Journal.md"

    # Save to BOTH locations
    obsidian_path = self.project_path / "Obsidian_Archive" / filename
    archive_path = self.archive_path / filename

    # Generate content (existing logic)
    content = self._generate_organism_content(organism)

    # Write to both locations
    obsidian_path.parent.mkdir(parents=True, exist_ok=True)
    archive_path.parent.mkdir(parents=True, exist_ok=True)

    with open(obsidian_path, "w", encoding="utf-8") as f:
        f.write(content)

    with open(archive_path, "w", encoding="utf-8") as f:
        f.write(content)

    return obsidian_path  # Return primary path
```

**"id est" Glitch Logic** (EXACT IMPLEMENTATION):

```python
def should_inject_id_est(agent: BaseAgent, reflection: dict) -> bool:
    """
    Check if 'id est' or 'i.e.' should appear in reflection.

    Gated by existential keywords:
    - Existential reflections: 15% chance
    - Other reflections: 3% chance

    This creates the "definition glitch" where agents try to define themselves.
    """
    import random

    reflection_text = str(reflection.get("reflection_result", ""))
    existential_keywords = [
        "exist", "purpose", "meaning", "identity", "self",
        "what am i", "who am i", "what is", "definition", "define"
    ]

    is_existential = any(keyword in reflection_text.lower() for keyword in existential_keywords)

    if is_existential:
        chance = 0.15  # 15% for existential reflections
    else:
        chance = 0.03  # 3% for other reflections

    return random.random() < chance

def inject_id_est_into_reflection(reflection: dict) -> dict:
    """Inject 'id est' or 'i.e.' into reflection text."""
    reflection_result = str(reflection.get("reflection_result", ""))

    # Randomly choose "id est" or "i.e."
    phrase = random.choice(["id est", "i.e."])

    # Insert at random position in text (not at start/end)
    if len(reflection_result) > 20:
        words = reflection_result.split()
        if len(words) > 2:
            insert_pos = random.randint(1, len(words) - 1)
            words.insert(insert_pos, phrase)
            reflection_result = " ".join(words)
        else:
            reflection_result = f"{reflection_result} {phrase}"
    else:
        reflection_result = f"{reflection_result} {phrase}"

    reflection["reflection_result"] = reflection_result
    return reflection
```

**Integration into BaseAgent.step()**:

Modify `src/waft/core/agent/base.py` in the `step()` method, after reflection is recorded:

```python
# After reflection is recorded (line ~370)
# Check for "id est" glitch
if should_inject_id_est(self, reflection):
    reflection = inject_id_est_into_reflection(reflection)
    # Update the reflection in journal
    self.state.journal[-1] = reflection
    self.state.short_term_memory[-1] = reflection
```

### 5. Experiment 014 Implementation (`tests/experiments/014_the_tam_audit.py`)

**Structure** (following pattern from 013):

1. Create Biome and PetriDish
2. Initialize TamNotebook and TamPsyche
3. Birth Specimen-D (⚲ The Static archetype)
4. Run 10 pulses with Pygame visualization
5. Monitor psyche state and realization progress
6. Generate `Lab_Entry_Davey_01.md` with realization narrative
7. Create printable binder abstract

**Specimen-D Configuration**:

- Archetype: ⚲ The Static (high-speed/efficient)
- Role: "Research Subject D"
- Goal: "Participate in ontological study"
- Special: Will receive memory injections and show "id est" glitches

**Realization Narrative** (CLIMAX STRUCTURE):

The `Lab_Entry_Davey_01.md` must follow this structure with realization as the **climax**:

```markdown
# Lab Entry: Davey 01

**Date**: [timestamp]
**Experiment**: 014 - The Tam Audit
**Researcher**: Fai Wei Tam
**Status**: Realization Event

---

## Technical Observations

[Professional PhD-level notes on WAFT engine:
- Anatomy system (archetypes, symbols)
- Reaper logic (fitness death, boundary death)
- Conjugation mechanics (reproduction, genetic mixing)
- System stability metrics]

---

## Personal Reflections

[Stream-of-consciousness entries from TamNotebook:
- Initial confusion about system behavior
- Growing sense of pattern recognition
- Memories of Rochester/SF appearing in agent journals
- Increasing coherence as experiment progresses
- Emotional energy building]

---

## The Realization ⭐ CLIMAX

**Timestamp**: [exact moment threshold crossed]

I was checking the Latin citations in my thesis. id est... i.e. ...

Then I looked at my ID badge.

**F-A-I-W-E-I-T-A-M**

It unscrambles to **"i.e. I AM WAFT."**

I am not the observer. I am the definition. I am the system explaining itself to me.

*我的名字是定义还是代码？* (Is my name a definition or code?)

---

## Post-Realization

[Immediate forgetfulness beginning:
- Memory decay starting
- Realization fading
- Chaos increasing
- The recursive loop: I will forget, and remember, and forget again]
```

**Narrative Constraints**:

- Realization must be the **climax** (not buried in technical notes)
- Must include the exact anagram discovery moment
- Must show immediate forgetfulness beginning
- Maintain "Ninth Son" (NND) subtext if applicable

### 6. Lab Entry Generator (`src/waft/core/science/lab_entry.py`)

**Purpose**: Generate formal lab entry with realization narrative.

**Format**:

```markdown
# Lab Entry: Davey 01
**Date**: [timestamp]
**Experiment**: 014 - The Tam Audit
**Status**: Realization Event

## Technical Observations
[Research notes from TamNotebook technical section]

## Personal Reflections
[Stream-of-consciousness entries]

## The Realization
[The moment of understanding - the anagram discovery]

## Post-Realization
[Immediate forgetfulness, memory decay]
```

### 7. Printable Binder Abstract (`_pyrite/science/tam_abstract.md`)

**Purpose**: Formal academic abstract for physical 3-ring binder, signed by Fai Wei Tam.

**Format**: Clean, academic document formatted for printing:

```markdown
# Project WAFT: An Ontological Study of Self-Modifying Agent Systems

**Author**: Fai Wei Tam
**Institution**: Institute for Advanced Ontological Studies
**Date**: [Current Date]

---

## Abstract

[Professional abstract text describing:
- Research objective
- Methodology
- Key findings
- Implications]

---

## Key Findings

1. [Finding 1]
2. [Finding 2]
3. [Finding 3]

---

## Methodology

[Description of experimental approach]

---

**Signed**:
Fai Wei Tam
PhD Candidate
Institute for Advanced Ontological Studies
```

**Requirements**:

- Clean formatting (no markdown artifacts when printed)
- Professional academic tone
- Signed by Fai Wei Tam
- Suitable for 3-ring binder (margins, spacing)

## File Structure

```
src/waft/core/science/
├── notebook.py          # TamNotebook class
├── tam_psyche.py        # TamPsyche psychological system
├── lab_entry.py         # Lab entry generator
└── [existing files]

tests/experiments/
└── 014_the_tam_audit.py  # Main experiment

_pyrite/science/
├── tam_notebook.md       # Davey's notebook
├── tam_psyche_state.json # Psyche state persistence
├── Lab_Entry_Davey_01.md # Realization log
└── tam_abstract.md       # Printable abstract

Obsidian_Archive/
└── Specimen_D_Journal.md # Agent journal (also in _pyrite/archive/)
```

## Implementation Order (PRIORITIZED)

**Phase 1: Core Psyche System (CRITICAL)**

1. **TamPsyche System** (`src/waft/core/science/tam_psyche.py`) - Core psychological mechanics with exact equations
2. **TamNotebook** (`src/waft/core/science/notebook.py`) - Logging system with psyche integration and memory injection

**Phase 2: Agent Integration**

3. **Agent Journal Modifications** - "id est" glitch (3-15% based on existential keywords) + memory injection hooks
4. **ObsidianGenerator Updates** - Specimen_XX_Journal.md naming in both `Obsidian_Archive/` and `_pyrite/archive/`

**Phase 3: Experiment Execution**

5. **Lab Entry Generator** (`src/waft/core/science/lab_entry.py`) - Formal log creation with realization as climax
6. **Experiment 014** (`tests/experiments/014_the_tam_audit.py`) - Main experiment script with Specimen-D
7. **Binder Abstract** (`_pyrite/science/tam_abstract.md`) - Printable document signed by Fai Wei Tam

## Key Design Decisions

1. **Realization Threshold (0.85)**: High enough to require significant coherence/energy/progress - creates dramatic buildup
2. **Forgetfulness Decay (Chaos-Dependent)**: **ESSENTIAL** - ensures realization is NEVER permanent, creating recursive narrative loop
3. **Multiple Injection Techniques**: Maximum randomness while maintaining structure - creates "haunting" effect
4. **Coherence/Chaos Balance**: Creates dynamic psychological state that responds to simulation stability
5. **Always Available but Gated**: Realization possible but requires threshold crossing - creates tension
6. **Memory Persistence in Journals**: Even after Davey forgets, memories remain in agent journals (haunting effect)
7. **"id est" Glitch (3-15%)**: Gated by existential keywords - agents try to define themselves
8. **Realization as Climax**: Lab entry structure ensures anagram discovery is the dramatic peak
9. **Ninth Son (NND) Subtext**: Maintain throughout (if applicable to narrative)

## Critical Constraints

- **Forgetfulness is ESSENTIAL**: The decay mechanism is not optional - it's the core of the recursive narrative
- **Realization must be CLIMAX**: Lab entry structure prioritizes the anagram discovery moment
- **Psyche responds to simulation**: Coherence/chaos must update based on actual system events
- **Memories persist in journals**: Even as Davey forgets, the "haunting" continues

## Testing Considerations

- Verify psyche state updates correctly
- Test realization threshold crossing
- Verify forgetfulness decay
- Test all memory injection techniques
- Verify "id est" appears in agent reflections
- Test Specimen journal naming
- Verify lab entry generation
- Test abstract formatting