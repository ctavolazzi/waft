# Karmic Wager System - Betting with Karma

**Purpose**: Enable WAFT to bet karma on hypotheses, outcomes, and predictions. Creates engagement through risk/reward mechanics.

**Philosophy**: "Put your karma where your hypothesis is."

---

## Overview

The Karmic Wager System allows WAFT to:
- **Bet karma** on hypotheses being confirmed or refuted
- **Wager on fitness** scores meeting thresholds
- **Bet on study outcomes** from Study Gym sessions
- **Gamble on component evolution** success
- **Track wager history** and statistics
- **Win or lose karma** based on outcomes

This creates **engagement** and **accountability** - WAFT has skin in the game!

---

## Quick Start

### Place a Hypothesis Wager

```bash
waft-bet hypothesis "Component evolution improves quality" 100
```

This bets 100 karma that the hypothesis will be confirmed. If confirmed, WAFT wins 200 karma (2x payout).

### Place a Fitness Wager

```bash
waft-bet fitness "Fitness above 0.8" 50 --threshold 0.8 --direction above
```

This bets 50 karma that fitness will be above 0.8.

### View Stats

```bash
waft-bet stats
```

Shows win rate, total karma won/lost, active wagers.

### List Active Wagers

```bash
waft-bet list
```

Shows all pending wagers waiting for resolution.

---

## Wager Types

### 1. Hypothesis Wager
**Bet on**: Hypothesis being confirmed or refuted

**Example**:
```python
from src.waft.karmic_wager import KarmicWagerSystem, wager_on_hypothesis

wager_system = KarmicWagerSystem()
wager = wager_on_hypothesis(
    wager_system,
    hypothesis="Component evolution produces higher fitness",
    karma_amount=100,
    prediction=True,  # Predicting confirmation
    odds=2.0  # 2x payout
)
```

**Resolution**: Hypothesis confirmed if Study Gym confidence ≥ 0.7

### 2. Fitness Wager
**Bet on**: Fitness score meeting threshold

**Example**:
```python
from src.waft.karmic_wager import wager_on_fitness

wager = wager_on_fitness(
    wager_system,
    description="Component evolution fitness",
    karma_amount=50,
    threshold=0.8,
    direction="above",  # Fitness >= 0.8
    odds=1.5
)
```

**Resolution**: Fitness meets threshold (above/below)

### 3. Study Outcome Wager
**Bet on**: Study Gym session succeeding

**Example**:
```python
from src.waft.karmic_wager import wager_on_study_outcome

wager = wager_on_study_outcome(
    wager_system,
    study_description="Component evolution quality study",
    karma_amount=75,
    success_criteria={
        "min_findings": 3,
        "min_conclusions": 1
    },
    odds=1.5
)
```

**Resolution**: Study meets success criteria

### 4. Component Evolution Wager
**Bet on**: Component evolution succeeding

**Example**:
```python
wager = wager_system.place_wager(
    wager_type=WagerType.COMPONENT_EVOLUTION,
    description="Component will achieve fitness > 0.9",
    karma_amount=200,
    prediction={"fitness": 0.9},
    resolution_criteria={"min_fitness": 0.9},
    odds=3.0  # High risk, high reward
)
```

**Resolution**: Component achieves target fitness

### 5. Research Question Wager
**Bet on**: Research question answer

**Example**:
```python
wager = wager_system.place_wager(
    wager_type=WagerType.RESEARCH_QUESTION,
    description="Research question: How does X work?",
    karma_amount=150,
    prediction="X works through mechanism Y",
    resolution_criteria={"question": "How does X work?"},
    odds=2.0
)
```

**Resolution**: Research answer matches prediction

---

## Integration with Scientific Papers

Scientific papers can automatically place wagers on hypotheses:

```python
from src.waft.evolution.scientific_paper_generator import generate_waft_self_study_paper

paper_path = generate_waft_self_study_paper(
    research_question="How does component evolution improve quality?",
    hypothesis="Component evolution produces higher fitness",
    objectives=["Measure fitness", "Track lineage"],
    wager_karma=100.0  # Bet 100 karma on the hypothesis!
)
```

The wager is automatically:
- Placed when study is created
- Resolved when study completes
- Documented in the research paper
- Tracked in wager history

---

## Wager Resolution

### Automatic Resolution
- **Hypothesis wagers**: Resolved when Study Gym session completes
- **Fitness wagers**: Resolved when fitness is evaluated
- **Study outcome wagers**: Resolved when study completes
- **Component evolution wagers**: Resolved when component is evaluated

### Manual Resolution
```python
wager_system.resolve_wager(
    wager_id="wager_20260111_154500_abc123",
    outcome={"confirmed": True, "fitness": 0.95}
)
```

### Custom Resolvers
```python
def custom_resolver(wager, outcome):
    # Custom logic to determine win/loss
    return outcome.get("custom_metric") > 0.8

wager_system.resolve_wager(
    wager_id="wager_123",
    outcome={"custom_metric": 0.9},
    resolver=custom_resolver
)
```

---

## Karma Payouts

### Winning
- **Payout**: `karma_amount × odds`
- **Example**: Bet 100 karma at 2.0 odds → Win 200 karma total
- **Net gain**: 100 karma (200 payout - 100 wager)

### Losing
- **Payout**: `-karma_amount` (lose the wager)
- **Example**: Bet 100 karma → Lose 100 karma
- **Net loss**: 100 karma

### Odds
- **1.0**: Even odds (bet 100, win 100, net 0)
- **2.0**: Double payout (bet 100, win 200, net +100)
- **3.0**: Triple payout (bet 100, win 300, net +200)
- **0.5**: Half payout (bet 100, win 50, net -50)

---

## Wager Statistics

```python
stats = wager_system.get_wager_stats()

# Returns:
{
    "total_wagered": 500.0,      # Total karma wagered
    "total_won": 300.0,          # Total karma won
    "total_lost": 200.0,         # Total karma lost
    "net_karma": 100.0,          # Net karma (won - lost)
    "won_count": 3,              # Number of won wagers
    "lost_count": 2,              # Number of lost wagers
    "win_rate": 0.6,              # Win rate (60%)
    "active_wagers": 1,           # Currently pending wagers
    "total_wagers": 5             # Total wagers (all time)
}
```

---

## File Structure

```
_hidden/.truth/wagers/
├── active_wagers.json          # Currently pending wagers
└── wager_history.jsonl        # Complete wager history (one per line)
```

---

## Integration Points

### Study Gym
- Automatically place wagers on hypotheses
- Resolve wagers when studies complete
- Track wager outcomes in study reports

### Scientific Paper Generator
- Option to wager on hypothesis when creating study
- Automatic wager resolution
- Wager results included in paper

### Component Evolution
- Bet on component success
- Resolve when component is evaluated
- Track component wager history

### Flight Recorder
- All wagers logged as evolutionary events
- Complete lineage tracking
- Reproducible wager history

---

## Philosophy

> "WAFT bets karma on its own hypotheses. This creates engagement, accountability, and risk/reward mechanics that keep the system invested in its own learning."

### Key Principles

1. **Skin in the Game**: WAFT risks karma on its predictions
2. **Accountability**: Wrong predictions cost karma
3. **Engagement**: Risk/reward creates motivation
4. **Learning**: Losing wagers teaches WAFT to be more careful
5. **Confidence**: High-confidence bets can have higher payouts

### The Vision

WAFT becomes **engaged** in its own research because:
- It has karma at stake
- Winning feels good (karma gain)
- Losing teaches lessons (karma loss)
- Risk/reward creates excitement
- Statistics track performance over time

---

## Example Workflow

### 1. Create Study with Wager

```python
generator = ScientificPaperGenerator(enable_wagers=True)

study_config = generator.create_study(
    research_question="How does X work?",
    hypothesis="X works through mechanism Y",
    objectives=["Measure X", "Analyze Y"],
    wager_karma=100.0  # Bet 100 karma!
)
```

### 2. Conduct Study

```python
study_session = generator.conduct_study(study_config, challenge_config)
```

### 3. Resolve Wager

```python
# Automatically resolved when study completes
result = generator.resolve_study_wager(study_config, study_session)

if result["won"]:
    print(f"✅ Won {result['karma_payout']} karma!")
else:
    print(f"❌ Lost {abs(result['karma_payout'])} karma")
```

### 4. Generate Paper

```python
paper_path = generator.generate_paper(
    study_config,
    study_session,
    format="summary"
)
# Paper includes wager results!
```

---

## CLI Usage

### Place Wagers

```bash
# Hypothesis wager
waft-bet hypothesis "Component evolution improves quality" 100

# Fitness wager
waft-bet fitness "Fitness > 0.8" 50 --threshold 0.8

# Study outcome wager
waft-bet study "Study will succeed" 75 --min-findings 3
```

### View Information

```bash
# Statistics
waft-bet stats

# Active wagers
waft-bet list
```

---

## Advanced Features

### Custom Wager Types

```python
wager = wager_system.place_wager(
    wager_type=WagerType.CUSTOM,
    description="Custom wager",
    karma_amount=100,
    prediction={"custom": "value"},
    resolution_criteria={
        "check": lambda outcome: outcome.get("custom") == "value"
    },
    odds=2.0
)
```

### Wager Chains

Place multiple related wagers:

```python
# Bet on hypothesis
hyp_wager = wager_on_hypothesis(...)

# If hypothesis confirmed, bet on fitness
if hyp_wager.status == WagerStatus.WON:
    fit_wager = wager_on_fitness(...)
```

### Conditional Wagers

```python
# Only bet if certain conditions met
if current_karma > 500:
    wager = wager_on_hypothesis(..., karma_amount=100)
```

---

## Karma Balance Integration

The wager system integrates with `KarmaMerchant`:
- Checks karma balance before placing wagers
- Deducts karma when wager placed (held in escrow)
- Awards karma when wager won
- Tracks karma changes in wager history

---

**Status**: ✅ Complete and ready to use  
**Files**: 
- `src/waft/karmic_wager.py` - Core wager system
- `scripts/waft-bet.py` - CLI tool
- `examples/generate_waft_self_study_paper_with_wager.py` - Example with wager

**Love**: ❤️ This is brilliant! Karma as engagement mechanism is perfect!
