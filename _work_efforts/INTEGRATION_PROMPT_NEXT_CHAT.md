# Prompt for Next Chat: Being Lifecycle System Architecture Integration

**Context**: The Being Lifecycle System has been implemented. Now we need to integrate it with the existing WAFT architecture.

---

## Prompt for New Chat

```
I've just completed implementing the Being Lifecycle System (work effort WE-260111-roo0). 
The system adds RPG-like lifecycle attributes to WAFT beings and a centralized "Now" cycle 
event loop.

**What was built:**
- Extended Being class with will_to_live, luck, decision_fatigue, pleasure, pain
- NowCycleManager: Centralized event loop for Being lifecycle
- BeingDecisionSystem: Decision-making for beings (separate from BaseAgent OODA)
- PersonalityAlignment: Calculates pleasure/pain from alignment
- KarmaMerchant.access_akasha() implemented (was TODO)
- Migration script for existing beings

**Key Architecture Decision:**
- Beings are separate from BaseAgent organisms
- TheSlicer manages BaseAgent lifecycle (NOT modified)
- NowCycleManager manages Being lifecycle (new system)

**What I need:**
Create a comprehensive plan to integrate the Being Lifecycle System with the existing 
WAFT architecture. The plan should address:

1. **Integration Points:**
   - How does NowCycleManager interact with TheSlicer/TheReaper?
   - How do beings interact with realities?
   - How do beings interact with PetriDish/Biome systems?
   - How do beings interact with BaseAgent organisms?

2. **System Coordination:**
   - Should NowCycleManager run in parallel with TheSlicer?
   - How do we coordinate cycles between beings and agents?
   - Should there be a unified scheduler?

3. **Data Flow:**
   - How do beings spawn into realities?
   - How do beings interact with the karma economy?
   - How do beings interact with the evolutionary system?

4. **Lifecycle Management:**
   - When do beings die vs. when do agents die?
   - How do beings reincarnate vs. how do agents evolve?
   - What's the relationship between being death and agent lifecycle?

5. **Testing Strategy:**
   - How to test the integration?
   - How to test coordination between systems?
   - What integration tests are needed?

**Existing Architecture Components to Consider:**
- TheSlicer/TheReaper (BaseAgent lifecycle)
- Biome/PetriDish (agent containers)
- Reality system (where beings exist)
- KarmaMerchant/KarmaMarket (karma economy)
- SourceConsciousness (being spawning)
- TheObserver (flight recorder - already integrated)

**Deliverables:**
1. Integration architecture diagram (text-based or markdown)
2. Integration plan with phases
3. Code changes needed for integration
4. Testing strategy
5. Migration path for existing systems

Please explore the codebase to understand the existing architecture, then create a 
comprehensive integration plan.
```

---

## Key Files to Reference

- `src/waft/being.py` - Being class
- `src/waft/core/now_cycle.py` - NowCycleManager
- `src/waft/core/hub/lifecycle.py` - TheSlicer/TheReaper
- `src/waft/core/dish.py` - PetriDish
- `src/waft/world/biome.py` - Biome
- `src/waft/karma.py` - KarmaMerchant
- `src/waft/source_consciousness.py` - SourceConsciousness
- `_work_efforts/roadmaps/being_lifecycle_system/DEVELOPMENT_ROADMAP.md` - Full roadmap

---

## Expected Outcome

A detailed integration plan that shows how the Being Lifecycle System fits into the 
existing WAFT architecture, with specific code changes, coordination mechanisms, and 
testing strategies.
