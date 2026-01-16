# OpenHands Context Condenser for Token Efficiency

**Date**: 2026-01-14 20:35:00
**Context**: Using OpenHands context condenser to manage conversation history efficiently
**Status**: 💰 TOKEN OPTIMIZATION ENABLED

---

## What Is a Context Condenser?

A **context condenser** manages agent memory by condensing conversation history to save tokens. As conversations grow longer, the cumulative history leads to:

- 💰 **Increased API Costs**: More tokens = higher costs per API call
- ⏱️ **Slower Response Times**: Larger contexts take longer to process
- 📉 **Reduced Effectiveness**: LLMs become less effective with excessive irrelevant information

**The Solution**: Intelligently summarize older parts of the conversation while preserving essential information needed for the agent to continue working effectively.

---

## How It Works

### LLMSummarizingCondenser (Default)

The OpenHands SDK provides `LLMSummarizingCondenser` as the default condenser implementation. It uses an LLM to generate summaries of conversation history when it exceeds the configured size limit.

### Condensation Process

When conversation history exceeds a defined threshold:

1. **Keeps recent messages intact** - The most recent exchanges remain unchanged for immediate context
2. **Preserves key information** - Important details like user goals, technical specifications, and critical files are retained
3. **Summarizes older content** - Earlier parts of the conversation are condensed into concise summaries using LLM-generated summaries
4. **Maintains continuity** - The agent retains awareness of past progress without processing every historical interaction

### Efficiency Gains

- ✅ **Up to 2x reduction** in per-turn API costs
- ✅ **Consistent response times** even in long sessions
- ✅ **Equivalent or better performance** on software engineering tasks

---

## Configuration

### Basic Setup

```python
from openhands.sdk.context.condenser import LLMSummarizingCondenser

# Create condenser
condenser = LLMSummarizingCondenser(
    llm=llm.model_copy(update={"usage_id": "condenser"}),
    max_size=50,        # Trigger condensation when history exceeds 50 events
    keep_first=3,      # Always keep first 3 events (system prompts, initial messages)
)

# Add to agent
agent = Agent(
    llm=llm,
    tools=tools,
    condenser=condenser,  # Enable condensation
)
```

### Parameters

- **`max_size`**: Maximum number of events before condensation triggers
  - Default: `50` (good for most workflows)
  - Lower = more aggressive condensation (saves more tokens)
  - Higher = less condensation (preserves more detail)

- **`keep_first`**: Number of initial events to always keep
  - Default: `3` (system prompts, initial user messages)
  - These events contain critical context (project setup, initial goals)
  - Never condensed, always preserved

- **`llm`**: LLM instance for generating summaries
  - Uses same model as agent (or cheaper model for cost savings)
  - Separate `usage_id` for tracking condenser costs

---

## Integration with Generation Script

**File**: `scripts/generate_tavern_game_with_skills.py`

**New Features**:
- ✅ Context condenser enabled by default
- ✅ `--condenser-max-size` flag (default: 50)
- ✅ `--condenser-keep-first` flag (default: 3)
- ✅ `--no-condenser` flag to disable

**Usage**:

```bash
# Default: Condenser enabled (max_size=50, keep_first=3)
python scripts/generate_tavern_game_with_skills.py

# Custom condenser settings
python scripts/generate_tavern_game_with_skills.py --condenser-max-size 30 --condenser-keep-first 2

# Disable condenser (not recommended for long conversations)
python scripts/generate_tavern_game_with_skills.py --no-condenser
```

---

## Use Cases for Game Development

### 1. Long-Running Generation

**Scenario**: Multi-phase generation (5 phases, 100+ events)

**Without Condenser**:
- ❌ Context grows to 100+ events
- ❌ High token costs per API call
- ❌ Slower response times
- ❌ May hit context limits

**With Condenser**:
- ✅ Context condensed when > 50 events
- ✅ Older phases summarized
- ✅ Recent work preserved
- ✅ 2x cost reduction

**Example**:
```python
# Phase 0: Create work effort (3 events)
# Phase 1: Generate FastAPI server (20 events)
# Phase 2: Generate Electron app (25 events)
# → Condenser triggers! (48 events total)
# → Older events summarized, recent preserved
# Phase 3: Generate tests (15 events)
# Phase 4: Generate docs (10 events)
```

---

### 2. Multi-Session Workflows

**Scenario**: Generate over multiple sessions (with persistence)

**Session 1**: Generate server (30 events)
- Condenser may trigger if conversation is long
- State saved with condensed history

**Session 2**: Resume and generate Electron app (25 events)
- Condensed history from Session 1 preserved
- New events added
- Condenser manages total context

**Benefit**: Each session benefits from condensation, even across persistence boundaries.

---

### 3. Iterative Refinement

**Scenario**: Generate, test, refine, repeat (many iterations)

**Without Condenser**:
- Each iteration adds events
- Context grows linearly
- Costs increase over time

**With Condenser**:
- Older iterations summarized
- Recent work preserved
- Costs remain stable

**Example**:
```python
# Iteration 1: Generate initial code (20 events)
# Iteration 2: Add error handling (15 events)
# Iteration 3: Fix bugs (10 events)
# → Condenser triggers! (45 events)
# → Iteration 1 summarized, Iterations 2-3 preserved
# Iteration 4: Optimize performance (12 events)
```

---

### 4. Cost Optimization

**Scenario**: Long conversation with many tool calls

**Token Usage** (example):
- Without condenser: 50,000 tokens per turn (after 100 events)
- With condenser: 25,000 tokens per turn (condensed to 50 events)
- **Savings**: 50% reduction in tokens = 50% reduction in costs

**Real-World Impact**:
- 100-turn conversation: $50 → $25 (50% savings)
- 200-turn conversation: $200 → $100 (50% savings)
- Long-running development: Significant cumulative savings

---

## How Condensation Works

### Event Threshold

**Before Condensation**:
```
Events: [0, 1, 2, ..., 48, 49, 50, 51, 52, ...]
         ↑ keep_first=3 preserved
```

**After Condensation** (max_size=50, keep_first=3):
```
Events: [0, 1, 2, [SUMMARY of 3-47], 48, 49, 50, 51, 52, ...]
         ↑ preserved    ↑ condensed    ↑ recent preserved
```

**Result**: Context reduced from 53 events to ~10 events (3 preserved + 1 summary + 6 recent).

---

### Summary Generation

**What Gets Summarized**:
- Older user messages
- Older agent responses
- Older tool outputs
- Historical context

**What Gets Preserved**:
- First `keep_first` events (system prompts, initial goals)
- Recent events (last `max_size - keep_first` events)
- Key information extracted into summary

**Summary Content**:
- User goals and requirements
- Technical decisions made
- Files created/modified
- Critical context for continuation

---

## Integration with Other Features

### Condenser + Persistence

**Combined Benefits**:
- Persistence saves state (including condensed history)
- Condenser reduces state size (faster saves/loads)
- Both work together seamlessly

**Example**:
```python
# Session 1: Generate with condenser
conversation = Conversation(
    agent=agent,  # Has condenser
    persistence_dir="./.conversations",
    conversation_id=conversation_id,
)
# Condenser manages context during generation
# State saved with condensed history

# Session 2: Resume with condenser
conversation = Conversation(
    agent=agent,  # Same condenser
    persistence_dir="./.conversations",
    conversation_id=conversation_id,
)
# Condensed history restored
# Condenser continues managing context
```

---

### Condenser + Skills

**Skills Are Preserved**:
- Skills configuration is part of agent config (not condensed)
- Skill content remains available
- Condenser only affects conversation history

**No Conflicts**: Skills and condenser work independently.

---

### Condenser + MCP

**MCP Tools Are Preserved**:
- MCP tool calls/results are part of conversation history
- Condenser summarizes older MCP interactions
- Recent MCP interactions preserved

**Benefit**: MCP tool outputs don't bloat context indefinitely.

---

## Best Practices

### 1. Enable for Long Conversations

**Always enable condenser for**:
- Multi-phase workflows (5+ phases)
- Long-running generation tasks
- Iterative refinement sessions
- Multi-session development

**Optional for**:
- Short, single-phase tasks
- Simple one-off generations

---

### 2. Tune Parameters

**For Cost Optimization**:
```python
condenser = LLMSummarizingCondenser(
    max_size=30,      # Lower = more aggressive
    keep_first=2,     # Minimal preservation
)
```

**For Detail Preservation**:
```python
condenser = LLMSummarizingCondenser(
    max_size=100,     # Higher = less condensation
    keep_first=5,     # More initial context
)
```

**Default (Balanced)**:
```python
condenser = LLMSummarizingCondenser(
    max_size=50,      # Good balance
    keep_first=3,     # Preserve initial context
)
```

---

### 3. Monitor Costs

**Track Condenser Usage**:
```python
# Condenser uses separate usage_id for tracking
condenser_llm = llm.model_copy(update={"usage_id": "condenser"})
condenser = LLMSummarizingCondenser(llm=condenser_llm, ...)

# Check costs separately
agent_cost = llm.metrics.accumulated_cost
condenser_cost = condenser_llm.metrics.accumulated_cost
total_cost = agent_cost + condenser_cost
```

**Note**: Condenser costs are typically much lower than agent costs (summaries are shorter than full history).

---

### 4. Test Condensation

**Verify Important Context Preserved**:
- Test that agent remembers key decisions
- Verify technical specifications retained
- Check that file references preserved

**If Context Lost**:
- Increase `keep_first` (preserve more initial context)
- Increase `max_size` (condense less aggressively)
- Review summary quality

---

## Troubleshooting

### Context Lost

**Issue**: Agent forgets important information after condensation

**Solutions**:
- Increase `keep_first` to preserve more initial context
- Increase `max_size` to condense less aggressively
- Review what gets summarized (may need custom condenser)

---

### Too Aggressive Condensation

**Issue**: Condenser triggers too often, summaries are too brief

**Solutions**:
- Increase `max_size` (e.g., 50 → 100)
- Review summary quality (may need better LLM for summaries)
- Consider custom condenser with domain-specific logic

---

### Condenser Not Triggering

**Issue**: Context grows but condenser never triggers

**Solutions**:
- Check `max_size` is set correctly
- Verify condenser is added to agent
- Check event count (may be lower than expected)

---

## Advanced: Custom Condensers

### Extending Base Classes

**RollingCondenser** (for rolling history):
```python
from openhands.sdk.context.condenser import RollingCondenser

class CustomCondenser(RollingCondenser):
    def condense(self, events, max_size, keep_first):
        # Custom condensation logic
        # Return condensed events
        pass
```

**CondenserBase** (for specialized strategies):
```python
from openhands.sdk.context.condenser import CondenserBase

class CustomCondenser(CondenserBase):
    def condense(self, events):
        # Custom condensation logic
        # Return condensed events
        pass
```

**Use Cases**:
- Domain-specific summarization
- Preserve certain event types
- Custom compression strategies

---

## Performance Benchmarks

### Token Reduction

**Typical Results**:
- 50 events → 30 events (40% reduction)
- 100 events → 50 events (50% reduction)
- 200 events → 60 events (70% reduction)

**Cost Savings**:
- Up to 2x reduction in per-turn API costs
- Cumulative savings in long conversations
- Faster response times

---

### Quality Impact

**Software Engineering Tasks**:
- Equivalent or better performance
- Important context preserved
- No degradation in code quality

**Benchmarks**: See [OpenHands blog post on context condensation](https://openhands.dev/blog/openhands-context-condensensation-for-more-efficient-ai-agents).

---

## Conclusion

**Context Condenser Benefits**:
- ✅ Up to 2x cost reduction
- ✅ Consistent response times
- ✅ Preserves important information
- ✅ Automatic management
- ✅ Works with persistence and skills

**Essential for**:
- Long-running workflows
- Multi-phase generation
- Iterative refinement
- Cost-sensitive development

**This is a game-changer for token efficiency!**

---

**Context Condenser Guide Complete**: 2026-01-14 20:35:00