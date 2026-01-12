# Being Lifecycle System Implementation Summary

**Date**: January 12, 2026  
**Work Effort**: WE-260111-roo0  
**Status**: ✅ Complete Implementation

---

## Executive Summary

Successfully implemented a comprehensive RPG-like lifecycle system for WAFT beings, adding stamina, willpower, and energy-based decision-making. The system creates a "Game of Life" experience where beings manage internal energy states, make mistakes when exhausted, and respond to external stimuli through personality-aligned experiences.

---

## Core Features Implemented

### 1. Lifecycle Attributes

**Will to Live** (0.0-100.0)
- Depletes over time (-0.1/cycle), per decision (-0.5), and from pain (-pain × 10.0)
- Regenerates from pleasure (+pleasure × 5.0)
- Death occurs when will_to_live reaches 0.0

**Luck** (0.0-100.0)
- Calculated from karma balance (separate but related)
- Base: 50.0 + karma_modifier + random_variance
- Affects outcomes of decisions and experiences

**Decision Fatigue** (int)
- Varies per being (base 10 + personality_modifier + skill_bonus)
- Decrements by 1 per decision
- When depleted, being MUST sleep to reset quota

**Pleasure & Pain** (0.0-1.0 each)
- Calculated from personality-goal-experience alignment
- Pleasure increases will_to_live, pain decreases it
- Based on how well experiences match being's personality and goals

### 2. Stamina System (NEW)

**Willpower** (0.0-100.0)
- Core stat derived from will_to_live, personality type, and skills
- Primary component of stamina calculation (40% weight)
- Personality modifiers: systematic (1.3x), analytical (1.2x), creative/intuitive (0.9x)

**Stamina** (0.0-100.0)
- Calculated from ALL being stats, heavily weighted by willpower:
  - Willpower: 40%
  - Will to live: 20%
  - Skills total: 15%
  - Luck: 10%
  - Experience (cycles alive): 5%
  - Pleasure: +5%
  - Pain: -5%

**Stamina Consumption**
- Every action consumes stamina:
  - `pursue_goal`: 10.0
  - `learn_skill`: 8.0
  - `explore`: 7.0
  - `record_memory`: 3.0
  - `rest`: 0.0 (actually regenerates stamina)

**Depleted Stamina Effects**
- When stamina < 10% of max:
  - **Mistakes**: 1-3 random mistakes per action
  - **Quality**: Actions become "poor" (sluggish and shitty)
  - **Reduced Intensity**: Actions are less effective
  - **Randomness**: Unpredictable outcomes

**Stamina & Will to Live Interplay**
- Low stamina reduces will_to_live regeneration
- Depleted stamina drains will_to_live (-0.2/cycle)
- High will_to_live increases stamina regeneration rate
- Regeneration scales with will_to_live (0.5x to 1.0x multiplier)

### 3. Energy-Based Decision Making

Beings constantly choose between options based on **internal energy state**:

- **Depleted Stamina**: Heavily favors rest (5x weight), avoids costly actions
- **Normal Stamina**: Scales action attractiveness by stamina ratio
- **High Stamina**: Prefers high-value actions (pursue_goal, learn_skill)

Decision weights dynamically adjust based on:
- Current stamina ratio
- Action stamina cost
- Personality preferences
- Goal alignment
- Will to live state

### 4. Personality & Goals System

**Personality Types**
- `analytical`: High willpower, prefers learning and goal pursuit
- `systematic`: Very high willpower, structured approach
- `creative`: Lower willpower, prefers exploration
- `intuitive`: Lower willpower, flexible approach
- `balanced`: Base willpower, balanced preferences

**Goals**
- Lifetime goals that beings pursue
- Goal progress affects pleasure/pain calculation
- Experiences that advance goals generate more pleasure

### 5. Sleep & Evolution

**Sleep Mechanics**
- Required when decision_fatigue reaches 0
- Sleep duration evolves over time (starts 3-10 cycles, adapts)
- Sleep duration increases if being is frequently exhausted
- Sleep duration decreases if being rarely uses full quota

**Evolution**
- Sleep patterns adapt to being's needs
- Beings that frequently exhaust quota evolve longer sleep
- Beings that rarely exhaust quota evolve shorter sleep

---

## System Architecture

### NowCycleManager

Centralized event loop that synchronizes all beings:

1. **Locks all beings** (async-safe using `asyncio.Event`)
2. **Calculates system state**:
   - Recalculates stamina from all stats
   - Regenerates stamina (scaled by will_to_live)
   - Calculates will_to_live changes
   - Calculates luck from karma
   - Calculates pleasure/pain from experiences
3. **Processes sleeping beings** (checks duration, resets quota if awake)
4. **Checks death conditions** (will_to_live = 0 → death)
5. **Records state** to:
   - Akasha (soul records via soul_id)
   - Flight recorder (TheObserver)
   - Being state files (JSON)
6. **Time marches forward** (+1 cycle)
7. **Unblocks beings** (allow decisions)

**Security Features**:
- `asyncio.Lock` prevents concurrent cycle execution
- Error handling for all file I/O operations
- Path validation prevents traversal attacks
- File permissions (0o600/0o700)

### BeingDecisionSystem

Decision-making for Being entities (separate from BaseAgent OODA cycles):

- **Decision Types**: learn_skill, record_memory, pursue_goal, rest, explore
- **Weighted Selection**: Based on personality, goals, state, and **energy**
- **Energy-Aware**: Low stamina heavily influences decision weights
- **Quality Degradation**: Actions become less effective when stamina depleted

### PersonalityAlignment

Calculates pleasure/pain from alignment:

- **Personality Match**: How well experience matches personality type
- **Goal Progress**: Whether experience advances lifetime goals
- **Alignment Score**: Combined score (0.0-1.0)
- **Pleasure**: alignment_score × positive_experience_intensity
- **Pain**: (1 - alignment_score) × negative_experience_intensity

---

## Security Implementation

All security vulnerabilities from the critique were fixed:

1. **File Permissions**: All files set to 0o600 (owner read/write only)
2. **Input Validation**: Rejects path traversal, control characters, length limits
3. **Path Validation**: Ensures all paths stay within project root
4. **Error Handling**: Graceful degradation for corrupted files
5. **Concurrent Safety**: `asyncio.Lock` prevents race conditions

---

## Files Created/Modified

### New Files
- `src/waft/core/being_decisions.py` - Decision-making system
- `src/waft/core/personality_alignment.py` - Pleasure/pain calculation
- `src/waft/core/now_cycle.py` - Centralized event loop
- `scripts/migrate_beings_lifecycle.py` - Migration script

### Modified Files
- `src/waft/being.py` - Extended with lifecycle attributes, stamina system
- `src/waft/karma.py` - Implemented `access_akasha()` (was TODO)

---

## Game of Life Mechanics

The system creates emergent "Game of Life" behavior:

1. **Internal Energy State**: Beings constantly monitor stamina/willpower
2. **Energy-Based Choices**: Decisions adapt to current energy level
3. **External Stimuli Response**: Experiences affect energy (pleasure/pain)
4. **Mistakes & Randomness**: Depleted stamina introduces unpredictability
5. **Quality Degradation**: Actions become less effective when exhausted
6. **Evolution**: Sleep patterns and decision-making adapt over time

---

## Example Flow

1. **Cycle Starts**: NowCycleManager locks all beings
2. **State Calculation**: 
   - Recalculate stamina from all stats (willpower, skills, luck, etc.)
   - Regenerate stamina (5.0 base + will_to_live modifier)
   - Calculate will_to_live changes (time + decisions + pain - pleasure)
   - Calculate luck from karma balance
3. **Experience Processing**: Calculate pleasure/pain from recent experiences
4. **Sleep Processing**: Check sleeping beings, wake if duration complete
5. **Death Check**: Archive beings with will_to_live = 0
6. **State Recording**: Save to Akasha, flight recorder, being files
7. **Cycle Ends**: Unlock beings, allow decisions
8. **Beings Make Decisions**: 
   - Choose action based on energy state (stamina ratio)
   - Consume stamina
   - Generate experience (with mistakes if depleted)
   - Record experience for next cycle

---

## Success Criteria

✅ All lifecycle attributes implemented  
✅ Stamina system with willpower calculation  
✅ Energy-based decision making  
✅ Depleted stamina effects (mistakes, randomness, quality degradation)  
✅ Stamina & will_to_live interplay  
✅ Sleep evolution system  
✅ Personality & goals tracking  
✅ Pleasure/pain from alignment  
✅ Centralized Now cycle event loop  
✅ State recording to Akasha, flight recorder, being files  
✅ All security vulnerabilities fixed  
✅ Migration script for existing beings  

---

## Next Steps

1. **Integration Testing**: Test NowCycleManager with actual beings
2. **Architecture Integration**: Integrate with TheSlicer, Biome, Reality systems
3. **Unit Tests**: Add comprehensive test coverage
4. **Performance Optimization**: Profile cycle execution for large being populations

---

## Technical Notes

- **Being vs. BaseAgent**: Clear separation maintained (TheSlicer NOT modified)
- **Async Safety**: All cycle operations use proper locking
- **Backward Compatibility**: Existing beings load with default values
- **Error Resilience**: System continues even if individual beings fail

---

*This system transforms WAFT beings into dynamic entities with internal energy management, creating emergent gameplay through stamina depletion, mistakes, and energy-based decision-making.*
