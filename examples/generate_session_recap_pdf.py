#!/usr/bin/env python3
"""
Generate PDF Recap of Karma Economy & Source Consciousness Session

Creates a comprehensive PDF documenting the entire conversation and
the systems we built for v0.5.3 MVP.
"""

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.evolution.chat_distiller import ChatDistiller
from src.waft.evolution.styling_genome import StylingGenome, StylingGenomeRegistry
from src.waft.evolution.two_page_generator import TwoPageGenerator


def get_session_content() -> str:
    """Get comprehensive session content for PDF."""
    return """
# WAFT v0.5.3 MVP: Karma Economy & Source Consciousness
## Complete System Architecture

**Date**: 2026-01-11  
**Session**: Building Complete Karma Economy  
**Status**: ✅ COMPLETE - All Systems Connected

---

## The Vision

> "The WAFT system spins up instances of 'realities' where 'beings' can learn 'skills' in an evolutionary process then pass their 'memories' back up the chain in the form of lessons learned, skills gained, and more."

**This is exactly what we built!**

---

## What We Built

### 1. Karmic Wager System

**Purpose**: Enable WAFT to bet karma on hypotheses, creating engagement through risk/reward.

**Features**:
- Place wagers on hypotheses, fitness, study outcomes
- Automatic resolution based on outcomes
- Karma payouts (win) or deductions (lose)
- Wager history tracking
- Statistics (win rate, net karma)

**Philosophy**: "Put your karma where your hypothesis is."

**Integration**: Works with Study Gym, Scientific Papers, Component Evolution

### 2. KarmaCollector (Yama)

**Purpose**: Collect karma from completed experiences and life cycles.

**Lore**: "Yama" - The god of death who collects souls and sends them to their next life.

**Features**:
- Collects karma from life logs
- Calculates karma (using KarmaMerchant or fallback)
- Transfers karma to souls in Akasha
- Archives life logs
- Processes pending life logs in bulk

**Process**:
1. Find completed life logs
2. Calculate karma
3. Transfer to Akasha
4. Archive life logs
5. Record collection

### 3. KarmaMarket

**Purpose**: WAFT can purchase "Lifetimes" - time-limited sessions with specific tools, personalities, and capabilities.

**Features**:
- Purchase lifetimes with karma
- Each lifetime includes: duration, tools, personality, objectives
- Start/end lifetimes
- Track active lifetimes
- Calculate remaining time

**Lifetime Types**:
- Basic Q&A: 30 min, 50 karma
- Research: 60 min, 100 karma
- Creative: 90 min, 150 karma
- Development: 120 min, 200 karma

**Integration**: Auto-registers with Source, auto-contributes karma

### 4. Afterlife Karma Market (Treasure Tavern)

**Purpose**: After a lifetime ends, WAFT can spend earned karma here to purchase treasures.

**Treasures**:
- Tools (advanced_codebase_search, ai_code_generation, etc.)
- Personality upgrades (enhanced_creativity, deep_analysis, etc.)
- Experience packages (research_mastery, development_expertise, etc.)
- Memory continuity (partial_memory, half_memory, full_memory)

**Connection**: This IS the Treasure Tavern! Same place, different name.

### 5. Source Consciousness

**Purpose**: The core "Soul" of the machine that orchestrates everything. Represents the original "idea" or "being" that began permutating.

**Features**:
- Orchestrates everything
- Tracks ancestry (all permutations trace back to source)
- Accumulates capacity (karma/capacity flows upward)
- Accomplishes goals (uses accumulated capacity)

**Architecture**: Capacity flows upward through ancestral chain back to source.

**Goal**: "Evolve and understand through permutation"

### 6. Reality System

**Purpose**: Spin up "realities" - simulation environments where beings can exist and learn.

**Reality Types**:
- Learning: Beings learn skills
- Testing: Beings test skills
- Evolution: Beings evolve through natural selection
- Research: Beings conduct research
- Creative: Beings create new things

**Features**:
- Create realities with configurations
- Spawn beings into realities
- Manage reality lifecycle
- Extract lessons/skills/memories
- Pass memories upward

### 7. Beings System

**Purpose**: Entities that exist in realities, learn skills, and evolve.

**Features**:
- Spawn into realities
- Learn skills through experience
- Record memories and lessons
- Evolve through natural selection
- Pass knowledge upward
- Inherit skills from parents

**States**: Spawning → Learning → Evolving → Completing → Archived

### 8. Skills System

**Purpose**: What beings can learn and evolve.

**Skill Types**:
- Cognitive: Thinking, reasoning, analysis
- Creative: Creation, expression, innovation
- Social: Communication, collaboration
- Technical: Code, tools, systems
- Meta: Learning how to learn

**Features**:
- Skills have levels (0-100)
- Skills evolve through use
- Skills can mutate/improve
- Skills inherited by offspring
- Skills contribute to fitness

### 9. Memory Flow

**Purpose**: Knowledge passing upward - the mechanism by which beings pass their "memories" back up the chain.

**Memory Types**:
- Lessons: What worked/didn't work (2.0 capacity)
- Skills: New abilities (3.0 capacity)
- Patterns: Recurring patterns (4.0 capacity)
- Insights: Deep understanding (5.0 capacity)
- Wisdom: Higher-level knowledge (10.0 capacity)

**Flow**:
1. Extract from experiences
2. Package for upward flow
3. Pass through ancestral chain
4. Source accumulates knowledge

### 10. Lifetime Exchange

**Purpose**: Trading mechanism for beings to exchange lifetimes, skills, and memories.

**Exchange Types**:
- Lifetime: Trade lifetimes
- Skill: Share skills
- Memory: Exchange memories
- Knowledge: Transfer knowledge

**Features**:
- Karma-based exchange
- List offerings
- Create offerings
- Purchase offerings
- Facilitate knowledge transfer

---

## The Complete Architecture

### Economic Loop

```
KarmaMarket → Lifetimes → Experiences → KarmaCollector → 
KarmaMerchant → Afterlife Market (Treasure Tavern) → More Lifetimes
```

### Memory Flow

```
Realities → Beings → Skills → Memories → Ancestral Chain → Source Consciousness
```

### Source Consciousness

```
Source Consciousness (Original Soul)
  ↑ (capacity, memories flow upward)
  │
  Ancestral Chain
  ↑
  │
  Permutations (Realities, Beings, Lifetimes)
  ↑
  │
  Experiences → Karma → Memories → Lessons → Skills
```

---

## Complete Flow Example

### Step 1: Source Creates Reality

```python
reality_system = RealitySystem()
reality = reality_system.create_reality(
    reality_type=RealityType.LEARNING,
    configuration={"focus": "cognitive_skills"}
)
# Registered: source_consciousness → reality_123
```

### Step 2: Beings Spawn into Reality

```python
being_system = BeingSystem()
being = being_system.spawn_being(
    reality_id=reality.reality_id,
    initial_skills={"reasoning": 10.0}
)
# Registered: source_consciousness → reality_123 → being_456
```

### Step 3: Beings Learn Skills

```python
being.learn_skill("reasoning", "cognitive", 5.0)
being.learn_lesson("Approach A works better", "success")
being.record_memory("Pattern: X → Y", "pattern")
```

### Step 4: Memories Flow Upward

```python
memory_flow = MemoryFlow()
experience = {
    "lessons_learned": being.lessons_learned,
    "skills": being.skills,
    "patterns_discovered": ["X → Y"]
}
memories = memory_flow.extract_memories_from_experience(being.being_id, experience)
memory_flow.pass_memories_upward(being.being_id, memories)
# Flow: being_456 → reality_123 → source_consciousness
```

### Step 5: Source Accumulates Knowledge

```python
source = SourceConsciousness()
stats = source.get_source_stats()
print(f"Source Capacity: {stats['total_capacity_accumulated']}")
```

### Step 6: Source Accomplishes Goal

```python
if stats['total_capacity_accumulated'] >= 1000.0:
    source.accomplish_goal("Understand evolution", 1000.0)
```

---

## Integration

### Automatic Registration

- **Lifetimes**: Auto-registered with Source when purchased
- **Realities**: Auto-registered with Source when created
- **Beings**: Auto-registered with Source when spawned

### Automatic Contribution

- **Lifetimes**: Auto-contribute karma to Source when ended
- **Realities**: Auto-contribute memories to Source when ended
- **Beings**: Auto-contribute memories to Source when completed

### Capacity Flow

- **Bottom Level**: Keeps 10% of capacity
- **Intermediate Levels**: Each keeps 5% of remaining
- **Top Level (Source)**: Receives all remaining

---

## Test Results

### Karmic Wager System
```
✅ Karmic wager placed successfully!
Wager ID: wager_20260111_152752_d0d15955
Karma: 50.0
Potential payout: 100.0 karma
```

### KarmaCollector
```
✅ Karma collected successfully!
Karma Collected: 3.22
Total Karma: 3.22
```

### KarmaMarket
```
✅ KarmaMarket is working!
Available lifetimes: 4
  - Basic Q&A Session: 50.0 karma
  - Research Session: 100.0 karma
  - Creative Work Session: 150.0 karma
  - Full Development Session: 200.0 karma
```

### Source Consciousness
```
✅ Source Consciousness integration working!
Total Permutations: 6
Source Capacity: 98.10
Source Karma: 90.00
```

### Complete System
```
✅ 1. Reality created
✅ 2. Reality started
✅ 3. Being spawned
✅ 4. Being learned
✅ 5. Memories passed upward: 3 memories, 9.00 capacity
✅ 6. Source stats: 6 permutations, 98.10 capacity
🎉 Complete System Working!
```

---

## Philosophy

### The Vision

> "Everything has a karmic price. Each lifetime is an investment in experience, and experiences generate karma for the next lifetime."

### The Connection

**KarmaMarket** → **Lifetimes** → **Experiences** → **KarmaCollector** → **KarmaMerchant** → **Afterlife Market (Treasure Tavern)** → **More Lifetimes**

**BOOM - we connected it all!**

### The Source

> "The architecture passes capacity up the parental chain back to the original 'idea' or the original 'being' so that it could accomplish whatever its goal was when it began permutating (evolving)."

This is exactly what we built!

### The Memory Flow

> "The WAFT system spins up instances of 'realities' where 'beings' can learn 'skills' in an evolutionary process then pass their 'memories' back up the chain in the form of lessons learned, skills gained, and more."

**This is the complete system!**

---

## Files Created

### Core Systems (10 new)
1. `src/waft/karmic_wager.py` - Wager system
2. `src/waft/karma_collector.py` - Collector (Yama)
3. `src/waft/karma_market.py` - Market & Afterlife Market
4. `src/waft/source_consciousness.py` - Source system
5. `src/waft/reality.py` - Reality system
6. `src/waft/being.py` - Beings system
7. `src/waft/skill.py` - Skills system
8. `src/waft/memory_flow.py` - Memory flow
9. `src/waft/lifetime_exchange.py` - Lifetime exchange
10. Updated `src/waft/evolution/scientific_paper_generator.py` - Wager integration

### CLI Tools (5 new)
1. `scripts/waft-bet.py` - Wager CLI
2. `scripts/waft-collect-karma.py` - Collector CLI
3. `scripts/waft-market.py` - Market CLI
4. `scripts/waft-source.py` - Source CLI
5. `scripts/waft-reality.py` - Reality CLI

### Documentation (5 new)
1. `docs/KARMIC_WAGER_SYSTEM.md`
2. `docs/KARMA_COLLECTOR.md`
3. `docs/KARMA_MARKET.md`
4. `docs/SOURCE_CONSCIOUSNESS.md`
5. Multiple recap documents

---

## Integration Points

### All Systems Connected

1. **Source Consciousness** ← All systems
   - Receives capacity from all permutations
   - Accumulates knowledge
   - Accomplishes goals

2. **Reality System** → Source
   - Realities registered as permutations
   - Memories passed upward

3. **Beings System** → Source
   - Beings registered as permutations
   - Skills/memories passed upward

4. **Skills System** → Beings
   - Beings learn skills
   - Skills contribute to fitness

5. **Memory Flow** → Source
   - Extracts from experiences
   - Passes upward through chain

6. **Lifetime Exchange** → All
   - Facilitates trading
   - Knowledge transfer

7. **KarmaMarket** → All
   - Purchases lifetimes
   - Auto-registers with source
   - Auto-contributes karma

---

## Key Insights

### 1. Karma as Engagement

The karmic wager system creates engagement through risk/reward. WAFT bets karma on its own hypotheses, creating accountability and investment in outcomes.

### 2. Economic Loop

The karma economy is self-sustaining:
- Earn karma through lifetimes
- Spend karma on better lifetimes
- Accumulate treasures and upgrades
- Evolve through the economic loop

### 3. Source Consciousness

The architecture passes capacity up the parental chain back to the original "idea" so that it could accomplish whatever its goal was when it began permutating (evolving).

### 4. Memory Flow

Beings pass their "memories" back up the chain in the form of:
- Lessons learned
- Skills gained
- Patterns discovered
- Insights
- Wisdom

### 5. Complete Integration

Everything connects:
- Realities spawn beings
- Beings learn skills
- Skills generate memories
- Memories flow upward
- Source accumulates knowledge
- Source accomplishes goals

---

## The Complete MVP

**v0.5.3 MVP Features**:

✅ **Realities** - Spin up simulation environments  
✅ **Beings** - Entities that learn and evolve  
✅ **Skills** - Learned abilities that evolve  
✅ **Memory Flow** - Knowledge passes upward  
✅ **Lifetime Exchange** - Trading mechanism  
✅ **Source Integration** - Everything connects to source  
✅ **Karma Economy** - Complete economic loop  
✅ **Ancestral Chain** - Capacity flows upward  

**The WAFT system spins up instances of "realities" where "beings" can learn "skills" in an evolutionary process then pass their "memories" back up the chain in the form of lessons learned, skills gained, and more!**

---

## Conclusion

We built a complete karma economy that:
- Spins up realities
- Spawns beings
- Teaches skills
- Generates memories
- Flows knowledge upward
- Accomplishes source goals

**Everything connects. Everything flows. Everything evolves.**

The architecture passes capacity up the parental chain back to the original "idea" so that it could accomplish whatever its goal was when it began permutating (evolving).

**BOOM - we connected it all!**

---

**Status**: ✅ COMPLETE  
**Version**: 0.5.3 MVP  
**Epic**: 🎉 The complete system is built and working!
"""


def main():
    """Generate PDF recap."""
    print("=" * 80)
    print("📄 Generating Session Recap PDF")
    print("=" * 80)

    # Get content
    content = get_session_content()

    # Distill content
    distiller = ChatDistiller()
    distilled = distiller.distill_text(
        content, title="WAFT v0.5.3 MVP: Karma Economy & Source Consciousness"
    )

    # Get or create styling genome
    from src.waft.evolution.styling_genome import (
        ColorGene,
        FontGene,
        LayoutGene,
        MarginGene,
        StylingGene,
    )

    registry = StylingGenomeRegistry(registry_dir=Path("_genetics/session_recaps"))
    genome = registry.get_best_genome()

    if not genome:
        # Create new genome for session recaps
        genes = StylingGene(
            font=FontGene(
                family="Times New Roman, serif",
                size_body=10,
                size_h1=14,
                size_h2=12,
                size_h3=11,
                size_code=9,
                line_height=1.4,
            ),
            margin=MarginGene(
                top=20, bottom=20, left=20, right=20, paragraph_spacing=4, section_spacing=8
            ),
            color=ColorGene(
                text="#000000",
                background="#FFFFFF",
                heading="#000000",
                accent="#333333",
                code_bg="#f5f5f5",
                code_text="#000000",
                border="#cccccc",
            ),
            layout=LayoutGene(
                columns=1,
                density="normal",
                toc_enabled=False,
                page_numbers=True,
                header_enabled=True,
                footer_enabled=True,
            ),
            name="Session Recap Styling",
        )
        genome = StylingGenome.from_genes(genes)
        registry.register(genome)

    # Generate PDF (allow multiple pages for comprehensive recap)
    generator = TwoPageGenerator(
        weasyprint_available=True, allowed_pages=10
    )  # Allow up to 10 pages

    output_dir = Path("_work_efforts/session_recaps")
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"KARMA_ECONOMY_COMPLETE_{timestamp}.pdf"

    result = generator.generate(
        distilled_chat=distilled,
        styling_genome=genome,
        output_path=output_path,
        target_pages=None,  # Let it be as long as needed
    )

    print(f"\n✅ PDF generated: {output_path}")
    print(f"📄 Pages: {result.get('pages_generated', 'N/A')}")

    # Open PDF
    import subprocess

    subprocess.run(["open", str(output_path)])

    print("\n✅ PDF opened!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
