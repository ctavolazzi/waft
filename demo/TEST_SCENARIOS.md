# Test Scenarios

## Scenario 1: Soul Purchases Lifetime → Becomes ALIVE

**Initial State**: DEAD_AWAKE
**Action**: Purchase lifetime from KarmaMarket
**Expected Result**:
- Soul transitions to ALIVE_AWAKE
- Can now use spacetime tools (read_file, write, etc.)
- Cannot edit goals or purchase lifetimes
- Lifetime becomes active

**Test Command**:
```python
from waft.karma_market import KarmaMarket
from pathlib import Path

market = KarmaMarket(project_path=Path("demo/"))
lifetime = market.purchase_lifetime("basic_qa", "soul_demo_001")
```

---

## Scenario 2: Soul Runs Out of Karma → Gets Basic Survival Lifetime

**Initial State**: DEAD_AWAKE, 0 karma
**Action**: Attempt to purchase lifetime
**Expected Result**:
- System grants basic survival lifetime (free)
- Soul transitions to ALIVE_AWAKE
- Can use basic spacetime tools

**Test Command**:
```python
# soul_demo_004 has 0 karma
market = KarmaMarket(project_path=Path("demo/"))
lifetime = market.purchase_lifetime("basic_survival", "soul_demo_004")
```

---

## Scenario 3: Lifetime Ends → Soul Becomes DEAD, Can Edit Goals

**Initial State**: ALIVE_AWAKE (with active lifetime)
**Action**: Lifetime expires or ends
**Expected Result**:
- Soul transitions to DEAD_AWAKE
- Can now edit goals, purchase lifetimes
- Cannot use spacetime tools
- Lifetime archived

**Test Command**:
```python
from waft.karma_market import KarmaMarket

market = KarmaMarket(project_path=Path("demo/"))
market.end_lifetime(lifetime_id)
```

---

## Scenario 4: Dead Soul Purchases Treasure → Upgrades Personality

**Initial State**: DEAD_AWAKE
**Action**: Purchase treasure from AfterlifeKarmaMarket
**Expected Result**:
- Personality upgraded
- Karma deducted
- Soul remains DEAD_AWAKE
- Can still purchase lifetimes

---

## Scenario 5: State Transitions (Awake ↔ Sleeping)

**Initial State**: ALIVE_AWAKE or DEAD_AWAKE
**Action**: Transition between awake/sleeping
**Expected Result**:
- Sub-state changes (AWAKE ↔ SLEEPING)
- Primary state unchanged (ALIVE/DEAD)
- Capabilities remain same (based on primary state)

**Test Command**:
```python
from waft.soul_state import SoulStateManager

manager = SoulStateManager(project_path=Path("demo/"))
manager.set_sleeping("soul_demo_001")
manager.set_awake("soul_demo_001")
```
