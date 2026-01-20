# WAFT Metrics System - Official Documentation

> **The native currency system for measuring work, risk, and value in WAFT**

Version: 0.0.1
Status: Official Standard
Date: 2026-01-17

---

## 📖 Table of Contents

1. [Overview](#overview)
2. [The Four Metrics](#the-four-metrics)
3. [Metric Specifications](#metric-specifications)
4. [Usage Examples](#usage-examples)
5. [Conversion Tables](#conversion-tables)
6. [Quest System](#quest-system)
7. [Achievement System](#achievement-system)
8. [Evolution Triggers](#evolution-triggers)
9. [Best Practices](#best-practices)
10. [API Reference](#api-reference)

---

## Overview

### The Problem with Traditional Time Metrics

Traditional project management measures work in "hours" or "story points." But these metrics don't capture:

- **Mental difficulty** - Is it 4 hours of typing or 4 hours of deep thinking?
- **Risk profile** - Could this break the system?
- **Value creation** - What do I get out of this?
- **Alignment** - Does this move us toward or away from our goals?

### The WAFT Solution

WAFT uses **four native metrics** that provide multidimensional insight:

```
Task Complexity = f(Scint, Karma, Integrity, CognitiveLoad)
```

Instead of: *"This takes 4 hours"*

You get: *"90 Scint, +50 Karma, 30 Integrity risk, 8 Cognitive Load"*

This tells you:
- How much energy it costs
- How it aligns with goals
- How risky it is
- How hard you need to think

---

## The Four Metrics

### 1. Scint (✨) - Energy Currency

**Definition**: The amount of mental/physical energy required to complete work.

**Symbol**: ✨

**Range**: 0-1000+ (typical tasks: 10-150)

**Think of it as**: MP (Mana Points) in RPGs - you spend it to do work, earn it as rewards.

**Key Insight**: Unlike hours, Scint can be EARNED BACK. Good work pays dividends.

---

### 2. Karma (☯️) - Alignment Impact

**Definition**: How work affects the order/chaos balance of the system.

**Symbol**: ☯️

**Range**: -100 to +100

**Negative (Chaos)**: Breaking things, introducing disorder, technical debt
**Neutral (0)**: No structural impact
**Positive (Order)**: Creating structure, reducing entropy, organizing

**Key Insight**: Karma accumulation triggers evolution. High karma unlocks "The Architect" path.

---

### 3. Integrity (💚) - System Health Risk

**Definition**: Potential damage to system stability.

**Symbol**: 💚

**Range**: 0-100 (damage scale)

**Think of it as**: HP (Hit Points) - your system can take damage, but recovers with successful phases.

**Key Insight**: Unlike traditional "risk," Integrity can INCREASE from successful work.

---

### 4. Cognitive Load (🧠) - Mental Complexity

**Definition**: How much active thinking is required.

**Symbol**: 🧠

**Range**: 1-10

**Not the same as Scint**: High Scint can come from tedious work (low complexity) OR hard thinking (high complexity).

**Key Insight**: Helps schedule work - don't do high complexity tasks when tired.

---

## Metric Specifications

### Scint (✨) - Detailed Breakdown

| Range | Level | Description | Example |
|-------|-------|-------------|---------|
| 1-10 | Trivial | Autopilot, no thinking | Run existing script |
| 11-30 | Low | Simple tasks, routine | Move files with git mv |
| 31-70 | Medium | Focused effort needed | Update documentation, fix bugs |
| 71-150 | High | Deep work session | Write automation, design system |
| 151-300 | Very High | Marathon session | Major refactoring |
| 301+ | Epic | Multi-day effort | Build entire subsystem |

**Scint Regeneration**:
- Rest: +20 Scint per day
- Successful phase completion: +10 Scint
- Achievement unlock: +5 to +50 Scint
- Quest completion: +50 to +200 Scint

**Scint Earning**:
Work can EARN Scint back:
- Good documentation: Saves future Scint
- Automation: Multiplier on future work
- Structure creation: Reduces entropy cost

---

### Karma (☯️) - Detailed Breakdown

| Range | Alignment | Description | Effect |
|-------|-----------|-------------|--------|
| -100 to -50 | Deep Chaos | System breaking down | Evolution: "The Glitch" |
| -49 to -10 | Mild Chaos | Technical debt accumulating | Warning signs |
| -9 to +9 | Neutral | No structural change | Status quo |
| +10 to +49 | Mild Order | Organizing, cleaning | Positive trend |
| +50 to +100 | Strong Order | Major structure creation | Evolution: "The Architect" |
| 100+ | Master Order | Systemic organization | Final evolution |

**Karma Sources**:

**Positive Karma**:
- Creating documentation: +5 to +20
- Organizing files: +10 to +30
- Writing tests: +15 to +40
- Building automation: +20 to +50
- System redesign: +30 to +100

**Negative Karma**:
- Adding technical debt: -10 to -30
- Breaking backward compatibility: -20 to -50
- Hardcoding values: -5 to -15
- Skipping tests: -10 to -25
- "Quick hacks": -5 to -20

**Karma Effects**:
- **< -50**: System degrading, prioritize cleanup
- **0-50**: Neutral zone
- **50-100**: Evolution available (The Architect path)
- **100+**: Evolution triggered automatically
- **200+**: Master level unlocked

---

### Integrity (💚) - Detailed Breakdown

| Damage | Risk Level | Description | Recovery |
|--------|------------|-------------|----------|
| 0-10 | Safe | Won't break anything | Automatic |
| 11-30 | Careful | Minor risk, easy recovery | 1 day |
| 31-60 | Risky | Could break, plan needed | 3 days |
| 61-100 | Dangerous | High risk, backup essential | 1 week |
| 100+ | Critical | System failure likely | Major effort |

**Integrity System**:
- **Starting Integrity**: 100 💚
- **Damage**: Work can damage integrity
- **Recovery**: Successful phases HEAL integrity
- **Net Effect**: Good work makes system HEALTHIER

**Example**:
```
Phase with 30 damage risk:
- If successful: +20 integrity (net +20 - 30 = -10)
- But you gain experience: +5 permanent integrity max
- Over time: System gets MORE robust
```

**Integrity Regeneration**:
- Successful phase: +20 Integrity
- All tests passing: +10 Integrity
- Zero bugs found: +5 Integrity
- Achievement unlock: +10 Integrity

**Maximum Integrity**:
- Starts at 100
- Can increase to 150+ through successful work
- Higher max = can handle riskier work

---

### Cognitive Load (🧠) - Detailed Breakdown

| Level | Complexity | Description | Can Do While... |
|-------|------------|-------------|-----------------|
| 1 | Trivial | No thinking | Watching TV |
| 2-3 | Simple | Routine work | Listening to music |
| 4-6 | Moderate | Focused attention | In quiet room |
| 7-9 | Complex | Deep thinking | Complete silence |
| 10+ | Intense | Peak mental performance | Flow state required |

**Cognitive Load vs Scint**:

| Scint | Cognitive | Example |
|-------|-----------|---------|
| High | Low | Updating 100 links (tedious but simple) |
| High | High | Designing architecture (hard thinking) |
| Low | High | Solving tricky algorithm (quick but hard) |
| Low | Low | Running a script (easy and fast) |

**Cognitive Capacity**:
- **Morning**: 10 🧠 available (peak)
- **Afternoon**: 7 🧠 available (moderate)
- **Evening**: 4 🧠 available (tired)
- **Late night**: 2 🧠 available (zombie mode)

**Best Practices**:
- Do 7-9 complexity work in morning
- Do 4-6 complexity in afternoon
- Do 1-3 complexity in evening
- Never do 10+ when tired

---

## Usage Examples

### Example 1: Writing Documentation

**Traditional**: "Writing docs takes 3 hours"

**WAFT Metrics**:
```
Task: Write API documentation
Scint Cost: 60 ✨ (medium effort)
Scint Earned: 80 ✨ (saves future confusion)
Net: +20 ✨ profit

Karma Impact: +25 ☯️ (creating order)
Integrity Risk: 5 💚 (very safe)
Cognitive Load: 6 🧠 (moderate - need to understand API)
```

**Analysis**:
- Profitable (earn more than you spend)
- Good karma (aligns with goals)
- Very safe (can't break anything)
- Moderate complexity (need focus but not genius)

**Decision**: DO IT (especially in morning when fresh)

---

### Example 2: Quick Hack vs Proper Fix

**Option A: Quick Hack**
```
Scint Cost: 10 ✨ (fast)
Scint Earned: 0 ✨ (no future value)
Net: -10 ✨

Karma Impact: -15 ☯️ (technical debt)
Integrity Risk: 20 💚 (could break later)
Cognitive Load: 2 🧠 (simple)
```

**Option B: Proper Fix**
```
Scint Cost: 40 ✨ (takes longer)
Scint Earned: 60 ✨ (saves future debugging)
Net: +20 ✨ profit

Karma Impact: +20 ☯️ (proper structure)
Integrity Risk: 10 💚 (lower risk)
Cognitive Load: 6 🧠 (requires thinking)
```

**Analysis**:
- Quick hack: Fast but negative karma, no profit
- Proper fix: 4x more Scint but profitable, positive karma

**Decision**: Proper fix is better investment (if you have cognitive capacity)

---

### Example 3: Refactoring Decision

**Task**: Refactor legacy code module

```
Scint Cost: 120 ✨ (high effort)
Scint Earned: 150 ✨ (makes future work easier)
Net: +30 ✨ profit

Karma Impact: +40 ☯️ (major cleanup)
Integrity Risk: 50 💚 (risky - could break things)
Cognitive Load: 8 🧠 (complex - need to understand code)

Current Stats:
- Scint Available: 100 ✨
- Karma: +30 ☯️
- Integrity: 80 💚
- Mental Freshness: Morning (10 🧠 available)
```

**Decision Logic**:
```python
if scint_available >= cost and integrity >= risk and mental >= complexity:
    return "PROCEED"
else:
    return "DEFER"

# 100 >= 120? NO
# Result: DEFER (not enough energy)
```

**Better Plan**:
- Rest to recover Scint
- Do in morning (have cognitive capacity)
- Have rollback plan (integrity risk is moderate)

---

## Conversion Tables

### Scint ↔ Time (Approximate)

| Scint | Hours | Type |
|-------|-------|------|
| 10 | 0.5 | Quick task |
| 30 | 1 | Short task |
| 60 | 2 | Medium task |
| 90 | 3 | Substantial task |
| 120 | 4 | Half-day |
| 200 | 6-8 | Full day |
| 400 | 2 days | Multi-day |

**Note**: This varies by:
- Individual capacity
- Task type (creative vs mechanical)
- Interruptions
- Mental state

### Story Points → WAFT Metrics

| Story Points | Scint | Complexity | Typical Karma |
|--------------|-------|------------|---------------|
| 1 | 20 | 2 🧠 | ±5 |
| 2 | 40 | 3 🧠 | ±10 |
| 3 | 60 | 4 🧠 | ±15 |
| 5 | 100 | 6 🧠 | ±25 |
| 8 | 150 | 7 🧠 | ±40 |
| 13 | 250 | 8 🧠 | ±60 |

---

## Quest System

### What is a Quest?

A **Quest** is a multi-phase project with:
- Clear goal
- Multiple phases
- Investment/reward calculation
- Achievement unlocks
- Evolution potential

### Quest Structure

```python
Quest(
    name="Project Reorganization",
    phases=[
        Phase("Setup", scint=80, karma=+30, ...),
        Phase("Cleanup", scint=60, karma=+25, ...),
        # ... more phases
    ],
    total_investment=475,  # Scint
    total_rewards=670,     # Scint
    karma_gain=320,        # Total karma
    achievements=8         # Number of achievements
)
```

### Quest Evaluation

**Before Starting**:
```python
roi = total_rewards / total_investment  # 1.41x
break_even_phase = find_break_even()   # Phase 3
evolution_trigger = karma_for_evolution()  # Phase 4

if roi > 1.0 and can_afford(first_phase):
    accept_quest()
```

**During Quest**:
- Track cumulative metrics
- Check if still profitable
- Assess morale and capacity
- Can abandon if stats deteriorate

**After Completion**:
- Calculate actual vs predicted
- Unlock achievements
- Trigger evolution if karma > 100
- Update player stats

---

## Achievement System

### Achievement Types

**Phase Achievements** (One per phase):
- Unlocked by completing phase successfully
- Grant Scint + Karma bonuses
- Some grant permanent buffs

**Meta Achievements** (Quest-wide):
- "Marathon Runner": Complete all phases
- "Risk Manager": Zero integrity loss
- "Perfectionist": All metrics optimal

**Evolution Achievements**:
- "Bringer of Order": +100 Karma reached
- "The Architect": +200 Karma reached
- "Master of Structure": Quest complete

### Achievement Rewards

| Achievement | Scint | Karma | Special |
|-------------|-------|-------|---------|
| Phase Complete | +10 to +50 | +5 to +20 | None |
| Meta Achievement | +50 to +100 | +25 to +50 | Permanent buff |
| Evolution | +100 to +200 | +50 to +100 | New abilities |
| Quest Complete | +200 | +100 | Title unlock |

---

## Evolution Triggers

### The Evolution System

**Karma Thresholds**:
```
Karma < -100:  "The Glitch" (Chaos evolution)
Karma = 0-99:  "The Balanced" (No evolution)
Karma = 100+:  "The Architect" (Order evolution)
Karma = 200+:  "Master Builder" (Advanced evolution)
Karma = 300+:  "Grand Architect" (Final form)
```

### Evolution Effects

**The Architect** (Karma 100+):
- **Ability**: "Structure from Chaos"
- **Effect**: All future organization work costs 25% less Scint
- **Passive**: Automatically detect inefficiencies
- **Title**: "Bringer of Order"

**Master Builder** (Karma 200+):
- **Ability**: "Perfect Design"
- **Effect**: 50% bonus karma from structure work
- **Passive**: Can see optimal organization patterns
- **Title**: "The Architect"

**Grand Architect** (Karma 300+):
- **Ability**: "Reality Shaping"
- **Effect**: Organization work EARNS Scint instead of costing
- **Passive**: System self-organizes around you
- **Title**: "Master of Structure"

---

## Best Practices

### 1. Check Before Starting

```python
def can_start_work(work, player):
    if player.scint < work.cost:
        return "Rest first"

    if player.integrity < work.risk:
        return "Too risky - heal first"

    if player.cognitive_capacity < work.complexity:
        return "Too complex - defer until fresh"

    return "PROCEED"
```

### 2. Optimize for ROI

```python
def prioritize_work(work_items):
    # Sort by ROI, then by karma gain
    scored = [(w, w.rewards/w.cost, w.karma) for w in work_items]
    return sorted(scored, key=lambda x: (x[1], x[2]), reverse=True)
```

### 3. Balance Complexity

Don't do all hard work in one day:
```
Day 1: 8 🧠 task + 3 🧠 task + 2 🧠 task = 13 total ✓
Day 2: 9 🧠 task + 8 🧠 task + 7 🧠 task = 24 total ✗ (burnout!)
```

### 4. Track Cumulative Karma

```python
if cumulative_karma >= 100:
    evolution_available = True
    # Can complete quest early with major win
```

### 5. Manage Integrity

Don't let integrity drop below 30:
```python
if integrity < 30:
    focus_on_safe_work()  # Only do low-risk tasks

if integrity < 50:
    avoid_high_risk_work()  # Skip risky refactors
```

---

## API Reference

See `src/waft/metrics.py` for complete implementation.

### Core Classes

```python
from waft.metrics import Scint, Karma, Integrity, CognitiveLoad, Phase, Quest

# Create metrics
scint = Scint(cost=60, earned=80)  # Net: +20
karma = Karma(impact=+25)
integrity = Integrity(risk=10)
cognitive = CognitiveLoad(complexity=6)

# Create phase
phase = Phase(
    name="Documentation",
    scint=scint,
    karma=karma,
    integrity=integrity,
    cognitive=cognitive
)

# Create quest
quest = Quest(
    name="Project Cleanup",
    phases=[phase1, phase2, phase3]
)

# Evaluate
quest.calculate_roi()  # 1.41
quest.break_even_phase()  # 2
quest.evolution_trigger()  # 3
```

### Decorators

```python
from waft.metrics import track_metrics

@track_metrics(
    scint_cost=40,
    karma_impact=+10,
    integrity_risk=5,
    cognitive_load=4
)
def my_function():
    # Function automatically tracked
    pass
```

---

## Advanced Usage

### Custom Metrics

```python
from waft.metrics import Metric

class CustomMetric(Metric):
    def __init__(self, value):
        self.value = value

    def calculate(self):
        return self.value * 2
```

### Metric Formulas

**Effective Scint** (accounting for efficiency):
```python
effective_scint = scint_cost * (1 - efficiency_bonus)
```

**ROI Calculation**:
```python
roi = total_scint_earned / total_scint_invested
```

**Evolution Readiness**:
```python
evolution_ready = karma > 100 and integrity > 50
```

---

## Conclusion

WAFT metrics provide a **rich, multidimensional view** of work that traditional time estimates can't match.

**Instead of guessing** how long something takes, you now know:
- How much energy it costs (and earns back)
- How it aligns with goals
- How risky it is
- How hard you need to think

**This enables**:
- Better decision-making
- Optimal task scheduling
- Risk management
- Value optimization
- Gamified progression

**Start using WAFT metrics today** and level up your project management! 🚀

---

*Official WAFT Metrics System Documentation v0.0.1*
*Last Updated: 2026-01-17*
*Maintained by: WAFT Team*
