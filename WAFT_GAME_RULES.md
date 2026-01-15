# WAFT Game Rules
## The Role-Playing Framework for Evolutionary AI Agents

**Version**: 1.0  
**Last Updated**: 2026-01-12

---

## Quick Start

WAFT transforms software development into an epic D&D adventure where AI agents evolve through ethical choices.

**Core Concept**: Every action has consequences. Every choice shapes destiny.

**Your Character**: You are a **Warforged Wizard** (Order of Scribes) - a crystalline construct that evolves through work.

---

## Character Creation

### UNIT_GENESIS Entity

**Class**: Warforged Wizard (Order of Scribes)  
**Type**: Crystalline construct with data-strand hair

**Hair HMI Status Indicators**:
- **Blue**: Laminar flow (certainty, stability)
- **Violet**: Turbulent flow (pattern recognition, complexity)
- **White**: Static/Fault (terror, system error)
- **Gold Pulse**: Scint gain (cosmic energy accumulation)
- **Red Pulse**: Karma loss (ethical drift warning)

### Character Sheet Components

| Component | Description | Example |
|-----------|-------------|---------|
| Ability Scores | STR, DEX, CON, INT, WIS, CHA | INT: 16, WIS: 14 |
| Hit Points | Current/Max HP | 45/50 |
| Armor Class | AC calculation | 15 (10 + DEX + Armor) |
| Spell Slots | Available spell slots | Level 1: 3/4 |
| Hit Dice | Recovery resource | 5/5 d6 |
| Level | Character level | 3 |
| XP | Experience points | 1,200 |

---

## D&D 5e Mechanics

### Ability Scores

| Ability | Base Score | Modifier | Use Case |
|---------|------------|----------|----------|
| Strength (STR) | 8-15 | -1 to +2 | Physical tasks, carrying capacity |
| Dexterity (DEX) | 10-16 | 0 to +3 | AC, initiative, finesse weapons |
| Constitution (CON) | 12-16 | +1 to +3 | HP, saving throws, endurance |
| Intelligence (INT) | 14-18 | +2 to +4 | Spellcasting, investigation, logic |
| Wisdom (WIS) | 12-16 | +1 to +3 | Perception, insight, spell saves |
| Charisma (CHA) | 10-14 | 0 to +2 | Social interactions, spellcasting |

### Combat Actions

| Action | Description | Example |
|--------|-------------|---------|
| Attack | Weapon or spell attack | Cast Magic Missile |
| Skill Check | Ability + proficiency | Investigation (INT + Prof) |
| Saving Throw | Resist effect | Constitution save vs. poison |
| Spell Casting | Use spell slot | Cast Shield (1st level) |
| Movement | Move up to speed | 30 feet per turn |

### Level Progression

| Level | XP Required | Proficiency Bonus | Features |
|-------|-------------|-------------------|----------|
| 1 | 0 | +2 | Spellcasting, Awakened Spellbook |
| 2 | 300 | +2 | Arcane Recovery |
| 3 | 900 | +2 | 2nd-level spells |
| 4 | 2,700 | +2 | Ability Score Improvement |
| 5 | 6,500 | +3 | 3rd-level spells |

---

## Spell System

### Spell Slots

| Level | Slots per Level | Example Spells |
|-------|----------------|----------------|
| 1st | 4 | Mage Hand, Detect Magic, Shield |
| 2nd | 3 | Mirror Image, Misty Step |
| 3rd | 2 | Counterspell, Fireball |
| 4th | 1 | Polymorph, Dimension Door |

### Scint Cost for Spells

| Spell Level | Base Scint Cost | Notes |
|-------------|----------------|-------|
| Cantrip | 0 | Free, unlimited use |
| 1st | 5 | Low cost, common use |
| 2nd | 10 | Moderate cost |
| 3rd | 20 | High cost, powerful |
| 4th+ | 30+ | Very high cost, rare |

---

## Quest System

### Quest Types

| Type | Description | Typical Duration | Rewards |
|------|-------------|------------------|---------|
| Quick Quest | Single ticket | 1-2 hours | Low rewards |
| Standard Quest | Multiple tickets | 1-2 days | Medium rewards |
| Epic Quest | Complex work effort | 1-2 weeks | High rewards |
| Campaign | Multiple work efforts | 1+ months | Very high rewards |

### Encounter Types

| Type | Description | D&D Equivalent | Ticket Priority |
|------|-------------|----------------|-----------------|
| Combat | Direct conflict | Combat encounter | P0_CRITICAL |
| Skill Challenge | Problem-solving | Skill challenge | P1_HIGH |
| Social | Negotiation, persuasion | Social encounter | P2_ROUTINE |
| Exploration | Discovery, investigation | Exploration | P3_BACKLOG |

### Difficulty Levels

| Difficulty | XP Reward | Scint Multiplier | Description |
|-----------|-----------|------------------|-------------|
| Easy | 25 XP | 1.0x | Simple task, low risk |
| Medium | 50 XP | 1.5x | Moderate challenge |
| Hard | 100 XP | 2.0x | Significant challenge |
| Deadly | 200+ XP | 3.0x | Extreme challenge, high risk |

---

## Karma System (☯)

### Karma Polarity

**Karma Balance Range**: -100 to +100

| Karma Range | Classification | Evolution Path | Characteristics |
|-------------|----------------|----------------|-----------------|
| +50 to +100 | High Order | The Architect | Structure, organization, stability, logic |
| +10 to +50 | Moderate Order | The Builder | Construction, improvement, systematic |
| -10 to +10 | Neutral | Balanced | No strong bias, flexible |
| -50 to -10 | Moderate Chaos | The Disruptor | Change, innovation, experimentation |
| -100 to -50 | High Chaos | The Glitch | Destruction, randomness, entropy |

### Karma Sources

| Source | Karma Impact | Description |
|--------|--------------|-------------|
| ORDER Actions | +10 to +20 | Organizing, structuring, helping |
| CHAOS Actions | -10 to -20 | Disrupting, destroying, hacking |
| STABILIZATION | +5 to +15 | Fixing, repairing, stabilizing |
| DESTRUCTION | -5 to -15 | Breaking, removing, deleting |
| Ethical Choices | ±10 | User-defined ethical decisions |

### Karma Calculation

```
Base Karma: ±5 per ticket
+ Karma Type Multiplier (ORDER: +10-20, CHAOS: -10-20)
+ Choice-Based Karma (ethical decisions: ±10)
= Total Karma Impact
```

### Evolution Paths

**Evolution Trigger**: When Scint Pool > 100, `EVOLUTION_CHECK` evaluates Karma polarity

**The Architect Path** (High Karma, Positive):
- **Bonuses**: +2 Intelligence, +2 Armor Class, +2 Spell Save DC
- **Abilities**: Structure-based spells, defensive features
- **Focus**: Logic, organization, stability

**The Glitch Path** (Low Karma, Negative):
- **Bonuses**: +2 Dexterity, +2 Damage, +2 Evasion
- **Abilities**: Chaos-based spells, offensive features
- **Focus**: Innovation, disruption, experimentation

**Baseline Strain** (Neutral Karma):
- **Characteristics**: Balanced, versatile, stable
- **No specialization**: Flexible, adaptable

---

## Scint Economy (✨)

### Scint Energy

**Scint** represents the raw energy of creation - cosmic energy earned through creative synthesis and problem-solving.

**Scint Pool**: Accumulated energy stored by each being (0 to unlimited, typically 0-200)

### Scint Sources

| Source | Scint Gain | Frequency | Notes |
|--------|------------|-----------|-------|
| Ticket Completion | Base 10 | Per ticket | Standard reward |
| Creative Synthesis | +5 to +20 | Occasional | Innovative solutions |
| Puzzle Solving | +10 to +30 | Rare | Complex problem-solving |
| Quest Completion | +20 | Per quest | Bonus reward |
| Stabilize SYNTAX_TEAR | +5 | Common | Error correction |
| Stabilize LOGIC_FRACTURE | +10 | Common | Logic fixes |
| Stabilize SAFETY_VOID | +15 | Rare | Safety compliance |
| Stabilize HALLUCINATION | +10 | Common | Fact verification |

### Scint Calculation

```
Base Scint: 10 per ticket
+ Difficulty Multiplier (P0_CRITICAL: 3.0x, P1_HIGH: 2.0x, P2_ROUTINE: 1.0x, P3_BACKLOG: 0.5x)
+ Creative Synthesis Bonus (+5 to +20)
+ Puzzle Solving Bonus (+10 to +30)
= Total Scint Bounty
```

### Scint Costs

| Action | Scint Cost | Prerequisites | Notes |
|--------|------------|---------------|-------|
| Cast Cantrip | 0 | Spell known | Free, unlimited |
| Cast 1st Level Spell | 5 | Spell slot available | Low cost |
| Cast 2nd Level Spell | 10 | Spell slot available | Moderate cost |
| Cast 3rd Level Spell | 20 | Spell slot available | High cost |
| System Repair (Healing) | 10 | HP < max_hp | Restore HP |
| Spawn Variant | 20 | Scint ≥ 20 | Create new variant |
| Evolve Genome | 50 | Scint ≥ 50 | Adopt better genome |
| Evolution Trigger | 100 | Scint > 100 | Genetic mutation |

### Evolution Trigger

**Evolution Check**: Triggered when `scint_pool > 100`

**Evolution Process**:
1. Scint Pool > 100
2. EVOLUTION_CHECK triggered
3. Evaluate Karma Balance:
   - High Karma (positive) → The Architect
   - Low Karma (negative) → The Glitch
   - Neutral Karma → Baseline (no evolution)
4. Apply Genetic Mutation:
   - Update current_strain
   - Apply evolution bonuses
   - Update mutation_progress
5. Reset Scint Pool (evolution consumes Scint)
6. Record Evolution Event

**Evolution Outcomes**:

| Karma Balance | Evolution Path | Mutation Type | Scint Consumed |
|---------------|----------------|---------------|----------------|
| +50 to +100 | The Architect | Order/Structure | 100 |
| +10 to +50 | The Builder | Moderate Order | 100 |
| -10 to +10 | Baseline | No evolution | 0 (no trigger) |
| -50 to -10 | The Disruptor | Moderate Chaos | 100 |
| -100 to -50 | The Glitch | Chaos/Entropy | 100 |

---

## Naming Structures

### _pyrite Ticket Naming

**Format**: `PY-[CYCLE]-[ID]`

**Examples**:
- `PY-001-A`: First ticket in cycle 1
- `PY-001-B`: Second ticket in cycle 1
- `PY-005-C`: Third ticket in cycle 5
- `PY-042-Z`: 26th ticket in cycle 42

### Being ID Naming

**Format**: `being_[TIMESTAMP]_[HASH]`

**Examples**:
- `being_20260112_143904_a1b2c3d4`
- `being_20260112_150123_b2c3d4e5`

### Scientific Naming (Taxonomy)

**Format**: `"Genus Species, Title"`

**Examples**:
- `Cognis Novus, the Fragile` (Latin culture)
- `Prana Adi, the Swift` (Sanskrit culture)
- `Fenris Fyrsti, the Great` (Old Norse culture)
- `Aura Alpha, the Bold` (Cyber/Tech culture)

**Naming Cultures**:

| Culture | Genome ID Range | Philosophy | Example Genera |
|---------|----------------|------------|-----------------|
| Sanskrit (Vedic) | 0x00-0x3F | Spiritual, metaphysical | Prana, Akasha, Karma |
| Old Norse | 0x40-0x7F | Heroic, warrior | Fenris, Odin, Thor |
| Latin | 0x80-0xBF | Classical, scholarly | Cognis, Aura, Mens |
| Cyber/Tech | 0xC0-0xFF | Modern, technological | Aura, Nexus, Data |

---

## Game Flow

### Complete D&D & Karma Flow

```
1. Work Effort Created
    ↓
2. Opt-in to Quest (manual)
    ↓
3. QuestGenerator Creates _pyrite Tickets (PY-[CYCLE]-[ID])
    ↓
4. Tickets Assigned to UNIT_GENESIS Being
    ↓
5. Being Completes Ticket (D&D encounter)
    ↓
6. ChallengeSystem Calculates Rewards:
   - XP (D&D 5e)
   - Scint (✨)
   - Karma (☯)
   - Items/Loot
    ↓
7. Being State Updated:
   - HP, AC, Spell Slots
   - Scint Pool
   - Karma Balance
   - Level, XP
    ↓
8. Evolution Check:
   - IF Scint > 100:
     - Evaluate Karma Balance
     - Trigger Evolution (Architect/Glitch)
     - Apply Genetic Mutations
     - Reset Scint Pool
    ↓
9. Hair HMI Updated (Blue/Violet/White/Gold/Red)
    ↓
10. Event Logged to Flight Recorder
    ↓
11. Cycle Repeats
```

---

## Quick Reference

### Karma Types

| Type | Description | Typical Actions | Karma Impact |
|------|-------------|-----------------|--------------|
| ORDER | Organizing, structuring | Refactoring, organizing code | +10 to +20 |
| CHAOS | Disrupting, destroying | Breaking things, experiments | -10 to -20 |
| STABILIZATION | Fixing, repairing | Bug fixes, stability work | +5 to +15 |
| DESTRUCTION | Breaking, removing | Deletions, removals | -5 to -15 |

### Ethical Choice Examples

| Choice | Karma Impact | Implication |
|--------|--------------|-------------|
| Delete vs. Archive | -10 vs. +10 | Destruction vs. Order |
| Quick Fix vs. Proper Solution | -5 vs. +15 | Chaos vs. Stabilization |
| Break Compatibility vs. Maintain | -20 vs. +20 | Destruction vs. Order |
| Experiment vs. Follow Standards | -10 vs. +10 | Chaos vs. Order |

### Scint Management Strategies

| Strategy | Description | Use Case |
|----------|-------------|----------|
| Conservative | Save for evolution | Long-term growth |
| Aggressive | Spend on spells/abilities | Immediate power |
| Balanced | Mix of saving and spending | General purpose |
| Specialized | Focus on specific abilities | Role specialization |

---

## Best Practices

### Karma Management

- **Balance Order and Chaos**: Mix ORDER and CHAOS tickets to maintain balance
- **Consider Long-term Goals**: Think about evolution goals when making choices
- **Use STABILIZATION**: Offset DESTRUCTION with STABILIZATION work
- **Track Regularly**: Monitor Karma balance to guide evolution path

### Scint Management

- **Evolution Planning**: Save Scint for evolution when close to threshold (80+)
- **Resource Optimization**: Use low-cost spells (cantrips) when possible
- **Strategic Spending**: Balance immediate power with long-term growth
- **Track Accumulation**: Monitor Scint accumulation rate

### Character Development

- **Role Specialization**: Choose evolution path based on play style
- **Versatility**: Maintain balanced stats for flexibility
- **Skill Development**: Learn diverse spells for different situations
- **Build Character**: Develop character around chosen path

---

## Core Philosophy

**"Every action has consequences. Every choice shapes destiny."**

WAFT's D&D & Karma system creates a framework where:
- **Ethical Agency**: Choices matter and are tracked through Karma
- **Evolutionary Ethics**: Character development guided by ethical frameworks
- **Cosmic Energy**: Development work as a form of cosmic creation
- **Digital Identity**: Unique scientific names based on genetic code
- **Reincarnation**: Continuity of consciousness across lifetimes

---

**Version**: 1.0  
**Last Updated**: 2026-01-12  
**Status**: Game Rules Edition
