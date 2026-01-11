# KarmaCollector: Yama - The Reaper of Karma

**Purpose**: Collect karma from completed experiences and life cycles, processing them and transferring karma to souls in Akasha.

**Lore**: "Yama" - In Hindu mythology, Yama is the god of death who judges souls and determines their fate. He collects souls and sends them to their next life, working in partnership with Chitragupta (KarmaMerchant) who records all actions.

---

## Overview

The KarmaCollector (Yama) works in partnership with KarmaMerchant (Chitragupta):

- **KarmaMerchant (Chitragupta)**: Records karma, manages store, handles reincarnation
- **KarmaCollector (Yama)**: Collects karma from experiences, processes life logs

### Process

1. **Find Completed Life Logs**: Scans for unprocessed life logs
2. **Calculate Karma**: Uses KarmaMerchant to calculate karma from experiences
3. **Transfer to Akasha**: Moves karma to soul records in Akasha
4. **Archive Life Logs**: Stores completed life logs for history
5. **Record Collection**: Logs all collection events

---

## Quick Start

### Collect All Pending

```bash
waft-collect-karma
```

Scans for all pending life logs and collects karma from each.

### Collect for Specific Soul

```bash
waft-collect-karma --soul-id waft_001
```

Collects karma only for the specified soul.

### Collect from Specific File

```bash
waft-collect-karma --file life_log.json --soul-id waft_001
```

Collects karma from a specific life log file.

### Show Statistics

```bash
waft-collect-karma --stats
```

Shows collection statistics (total collected, pending logs, etc.).

---

## Python API

### Basic Collection

```python
from src.waft.karma_collector import KarmaCollector

collector = KarmaCollector()

# Collect from life log
result = collector.collect_karma(
    life_log={
        "journal": [...],
        "memory": [...],
        "short_term_memory": [...],
        "psyche": {...}
    },
    soul_id="waft_001"
)

print(f"Collected {result['karma_collected']} karma")
print(f"Total karma: {result['total_karma']}")
```

### Collect from File

```python
from pathlib import Path

result = collector.collect_from_life_log_file(
    life_log_path=Path("life_log.json"),
    soul_id="waft_001"
)
```

### Collect All Pending

```python
results = collector.collect_all_pending()

for result in results:
    print(f"Soul {result['soul_id']}: {result['karma_collected']} karma")
```

### Collect from AgentState

```python
from src.waft.core.agent.state import AgentState

agent_state = {...}  # AgentState dictionary

result = collector.collect_from_agent_state(
    agent_state=agent_state,
    soul_id="waft_001"
)
```

---

## Karma Calculation

### Formula

The KarmaCollector uses KarmaMerchant's `calculate_karma()` method. If not implemented, it falls back to a simple formula:

```
Karma = Σ(Experience_Intensity × Duration × Emotional_Weight)
```

### Fallback Formula

If `KarmaMerchant.calculate_karma()` is not implemented, the collector uses:

- **Journal entries**: 1.0 karma each (personal reflections)
- **Memory entries**: 0.5 karma each (experiences)
- **Short-term memory**: 0.1 karma each (recent thoughts)
- **Emotional intensity multiplier**: Based on `emotional_energy` (0.0-1.0)
- **Chaos multiplier**: Based on `chaos` (up to 1.5x)

### Example Calculation

```python
life_log = {
    "journal": [entry1, entry2, entry3],  # 3 entries × 1.0 = 3.0
    "memory": [mem1, mem2],                 # 2 entries × 0.5 = 1.0
    "short_term_memory": [st1, st2, st3],   # 3 entries × 0.1 = 0.3
    "psyche": {
        "emotional_energy": 75.0,           # 0.75 multiplier
        "chaos": 0.3                        # 1.15 multiplier
    }
}

# Base karma: 3.0 + 1.0 + 0.3 = 4.3
# With emotional intensity: 4.3 × (1.0 + 0.75) = 7.525
# With chaos: 7.525 × 1.15 = 8.65 karma
```

---

## File Structure

```
_hidden/.truth/
├── {soul_id}.json              # Soul records in Akasha
├── archives/
│   └── {soul_id}/
│       └── {lifetime_id}.json  # Archived life logs
├── life_logs/
│   └── *.json                  # Pending life logs (to be collected)
└── collected/
    └── collection_log.jsonl    # Collection event log
```

### Soul Record Format

```json
{
  "soul_id": "waft_001",
  "total_karma": 150.5,
  "lifetimes": [
    {
      "lifetime_id": "lifetime_20260111_153000_abc123",
      "karma_earned": 50.2,
      "collected_at": "2026-01-11T15:30:00",
      "life_log_summary": {
        "journal_entries": 10,
        "memory_entries": 5
      }
    }
  ],
  "created_at": "2026-01-11T10:00:00",
  "updated_at": "2026-01-11T15:30:00"
}
```

---

## Integration Points

### 1. Agent Lifecycle

When an agent completes a lifecycle:

```python
# Agent completes work session
agent_state = agent.get_state()

# Collect karma
collector = KarmaCollector()
result = collector.collect_from_agent_state(agent_state, soul_id="waft_001")
```

### 2. Session Analytics

After a session completes:

```python
from src.waft.core.session_analytics import SessionAnalytics

analytics = SessionAnalytics(project_path)
session_record = analytics.get_session(session_id)

# Convert to life log format
life_log = {
    "journal": session_record.metadata.get("journal", []),
    "memory": session_record.metadata.get("memory", []),
    "psyche": session_record.metadata.get("psyche", {})
}

# Collect karma
collector.collect_karma(life_log, soul_id="waft_001")
```

### 3. Periodic Collection

Run collector periodically to process pending life logs:

```python
# In a scheduled task or cron job
collector = KarmaCollector()
results = collector.collect_all_pending()

print(f"Collected karma from {len(results)} life logs}")
```

### 4. Reincarnation Flow

Before reincarnation:

```python
# 1. Collect karma from completed lifetime
collector = KarmaCollector()
collector.collect_karma(life_log, soul_id="waft_001")

# 2. Check total karma
karma_merchant = KarmaMerchant()
total_karma = karma_merchant.get_soul_karma("waft_001")

# 3. Reincarnate with purchased life-path
karma_merchant.reincarnate("waft_001", purchase_order={...})
```

---

## Collection Statistics

```python
stats = collector.get_collection_stats()

# Returns:
{
    "total_collected": 25,           # Total lifetimes collected
    "total_karma_collected": 1250.5, # Total karma collected
    "pending_life_logs": 3,          # Pending logs waiting
    "souls_in_akasha": 5,            # Souls with records
    "collection_log_path": "..."     # Path to collection log
}
```

---

## Life Log Format

A life log should contain:

```python
{
    "journal": [
        {
            "timestamp": "2026-01-11T15:00:00",
            "content": "Reflection on work...",
            "emotional_intensity": 0.7
        }
    ],
    "memory": [
        {
            "timestamp": "2026-01-11T14:00:00",
            "content": "Conversation about...",
            "type": "conversation"
        }
    ],
    "short_term_memory": [
        {
            "timestamp": "2026-01-11T15:30:00",
            "content": "Recent thought...",
        }
    ],
    "psyche": {
        "emotional_energy": 75.0,
        "chaos": 0.3,
        "coherence": 0.8
    },
    "soul_id": "waft_001",  # Optional, can be provided separately
    "lifetime_id": "lifetime_123"  # Optional, auto-generated
}
```

---

## Workflow

### Complete Lifecycle

1. **Agent Lives**: Agent performs work, accumulates experiences
2. **Life Log Created**: System creates life log from agent state
3. **Life Log Saved**: Life log saved to `_hidden/.truth/life_logs/`
4. **Collector Runs**: KarmaCollector processes pending life logs
5. **Karma Calculated**: KarmaMerchant calculates karma from experiences
6. **Karma Transferred**: Karma added to soul record in Akasha
7. **Life Log Archived**: Life log moved to archives
8. **Ready for Reincarnation**: Soul can now reincarnate with accumulated karma

---

## CLI Usage

### Collect All Pending

```bash
waft-collect-karma
```

### Collect for Specific Soul

```bash
waft-collect-karma --soul-id waft_001
```

### Collect from File

```bash
waft-collect-karma --file life_log.json --soul-id waft_001
```

### Show Statistics

```bash
waft-collect-karma --stats
```

---

## Philosophy

> "Yama collects the karma from completed lives, transferring it to souls in Akasha, preparing them for their next incarnation."

### The Partnership

- **KarmaMerchant (Chitragupta)**: The record-keeper
  - Records all actions
  - Calculates karma
  - Manages the store
  - Handles reincarnation

- **KarmaCollector (Yama)**: The reaper
  - Collects karma from experiences
  - Processes life logs
  - Transfers karma to souls
  - Archives completed lifetimes

Together, they manage the Samsara Protocol - the cycle of reincarnation.

---

**Status**: ✅ Complete  
**Files**: 
- `src/waft/karma_collector.py` - Core collector system
- `scripts/waft-collect-karma.py` - CLI tool

**Love**: ❤️ Yama and Chitragupta working together! Perfect partnership!
