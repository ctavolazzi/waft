# OpenHands LLM Registry for Centralized LLM Management

**Date**: 2026-01-14 21:00:00
**Context**: Using LLM Registry to manage multiple LLMs and track costs separately
**Status**: 🤖 LLM REGISTRY ENABLED

---

## What Is LLM Registry?

The LLM Registry provides a **centralized way to manage multiple LLM instances** in your application. Each LLM is identified by a unique `usage_id`, allowing you to:

- ✅ **Track costs separately** for each LLM (agent, condenser, sub-agents)
- ✅ **Retrieve LLMs dynamically** by usage_id
- ✅ **Manage multiple providers** and models
- ✅ **Switch between models** easily

**Key Benefits**:
- Centralized LLM management
- Separate cost tracking per LLM
- Easy model switching
- Better organization

---

## How It Works

### Creating and Registering LLMs

**Create LLM with usage_id**:
```python
from openhands.sdk import LLM, LLMRegistry

# Create LLM with unique usage_id
main_llm = LLM(
    usage_id="agent",
    model="anthropic/claude-sonnet-4-5-20250929",
    api_key=SecretStr(api_key),
)

# Create registry and add LLM
llm_registry = LLMRegistry()
llm_registry.add(main_llm)
```

**Retrieve LLM by usage_id**:
```python
# Get LLM from registry
llm = llm_registry.get("agent")

# Same instance is returned
same_llm = llm_registry.get("agent")
assert llm is same_llm  # True
```

---

## Use Cases

### 1. Multiple LLMs for Different Purposes

**Scenario**: Agent LLM + Condenser LLM

**Solution**:
```python
# Main agent LLM
agent_llm = LLM(usage_id="agent", model=model, api_key=api_key)
llm_registry.add(agent_llm)

# Condenser LLM (separate tracking)
condenser_llm = LLM(usage_id="condenser", model=model, api_key=api_key)
llm_registry.add(condenser_llm)

# Use in agent and condenser
agent = Agent(llm=llm_registry.get("agent"), ...)
condenser = LLMSummarizingCondenser(llm=llm_registry.get("condenser"), ...)
```

**Benefit**: Track costs separately for agent vs condenser.

---

### 2. Sub-Agent LLMs

**Scenario**: Multiple sub-agents with their own LLMs

**Solution**:
```python
# Main agent LLM
main_llm = LLM(usage_id="main_agent", ...)
llm_registry.add(main_llm)

# Sub-agent LLMs
server_llm = LLM(usage_id="sub-agent-server", ...)
electron_llm = LLM(usage_id="sub-agent-electron", ...)
test_llm = LLM(usage_id="sub-agent-tests", ...)

llm_registry.add(server_llm)
llm_registry.add(electron_llm)
llm_registry.add(test_llm)
```

**Benefit**: Track costs per sub-agent.

---

### 3. Different Models for Different Tasks

**Scenario**: Use cheaper model for condenser, expensive model for agent

**Solution**:
```python
# Expensive model for agent
agent_llm = LLM(
    usage_id="agent",
    model="anthropic/claude-sonnet-4-5-20250929",  # Expensive
    api_key=api_key,
)

# Cheaper model for condenser
condenser_llm = LLM(
    usage_id="condenser",
    model="anthropic/claude-haiku-3-5-20241022",  # Cheaper
    api_key=api_key,
)

llm_registry.add(agent_llm)
llm_registry.add(condenser_llm)
```

**Benefit**: Optimize costs by using cheaper models where appropriate.

---

### 4. Dynamic Model Selection

**Scenario**: Switch models based on task complexity

**Solution**:
```python
# Register multiple models
fast_llm = LLM(usage_id="fast", model="anthropic/claude-haiku-3-5-20241022", ...)
smart_llm = LLM(usage_id="smart", model="anthropic/claude-sonnet-4-5-20250929", ...)

llm_registry.add(fast_llm)
llm_registry.add(smart_llm)

# Switch based on task
if task_is_simple:
    llm = llm_registry.get("fast")
else:
    llm = llm_registry.get("smart")
```

**Benefit**: Use appropriate model for each task.

---

## Integration with Generation Script

**File**: `scripts/generate_tavern_game_with_skills.py`

**New Features**:
- ✅ LLM Registry for centralized management
- ✅ Separate LLMs for agent and condenser
- ✅ Automatic cost tracking per LLM
- ✅ Easy model switching

**How It Works**:
```python
# Create registry
llm_registry = LLMRegistry()

# Register agent LLM
agent_llm = LLM(usage_id="agent", ...)
llm_registry.add(agent_llm)

# Register condenser LLM (if enabled)
if condenser_enabled:
    condenser_llm = LLM(usage_id="condenser", ...)
    llm_registry.add(condenser_llm)

# Use in conversation
conversation.llm_registry = llm_registry
```

**Output**:
```
🤖 LLM Registry:
   Registered LLMs: agent, condenser
   (Use registry.get('usage_id') to retrieve specific LLMs)
```

---

## Cost Tracking with Registry

### Separate Cost Tracking

**Track costs per LLM**:
```python
# Get costs separately
agent_cost = llm_registry.get("agent").metrics.accumulated_cost
condenser_cost = llm_registry.get("condenser").metrics.accumulated_cost

print(f"Agent cost: ${agent_cost:.6f}")
print(f"Condenser cost: ${condenser_cost:.6f}")
print(f"Total cost: ${agent_cost + condenser_cost:.6f}")
```

**Benefit**: Understand cost breakdown by component.

---

### Conversation-Level Aggregation

**Get combined costs**:
```python
# Conversation stats aggregate all registered LLMs
combined_metrics = conversation.conversation_stats.get_combined_metrics()
print(f"Total cost: ${combined_metrics.accumulated_cost:.6f}")

# Breakdown by usage_id
for usage_id, metrics in conversation.conversation_stats.usage_to_metrics.items():
    print(f"{usage_id}: ${metrics.accumulated_cost:.6f}")
```

**Benefit**: See total costs and breakdown.

---

## Best Practices

### 1. Use Descriptive Usage IDs

**Use clear, descriptive usage_ids**:
```python
# Good
LLM(usage_id="agent", ...)
LLM(usage_id="condenser", ...)
LLM(usage_id="sub-agent-server", ...)

# Bad
LLM(usage_id="llm1", ...)
LLM(usage_id="llm2", ...)
```

**Benefit**: Easy to identify LLMs in metrics and traces.

---

### 2. Register All LLMs

**Register all LLMs in the registry**:
```python
# Register all LLMs
llm_registry.add(agent_llm)
llm_registry.add(condenser_llm)
llm_registry.add(sub_agent_llm)

# Use registry for retrieval
agent = Agent(llm=llm_registry.get("agent"), ...)
```

**Benefit**: Centralized management and tracking.

---

### 3. Use Registry in Conversation

**Attach registry to conversation**:
```python
conversation.llm_registry = llm_registry

# Conversation stats automatically track all registered LLMs
combined_metrics = conversation.conversation_stats.get_combined_metrics()
```

**Benefit**: Automatic cost aggregation.

---

### 4. Optimize Model Selection

**Use cheaper models where appropriate**:
```python
# Expensive model for agent (needs quality)
agent_llm = LLM(usage_id="agent", model="claude-sonnet-4-5", ...)

# Cheaper model for condenser (summarization is simpler)
condenser_llm = LLM(usage_id="condenser", model="claude-haiku-3-5", ...)
```

**Benefit**: Reduce costs without sacrificing quality.

---

## Integration with Other Features

### Registry + Metrics

**Combined Benefits**:
- Registry tracks all LLMs
- Metrics tracked per usage_id
- Combined metrics available

**Example**:
```python
# Individual metrics
agent_cost = llm_registry.get("agent").metrics.accumulated_cost

# Combined metrics
total_cost = conversation.conversation_stats.get_combined_metrics().accumulated_cost
```

---

### Registry + Condenser

**Combined Benefits**:
- Separate LLM for condenser
- Separate cost tracking
- Optimize condenser model

**Example**:
```python
# Agent LLM (expensive)
agent_llm = LLM(usage_id="agent", model="claude-sonnet-4-5", ...)

# Condenser LLM (cheaper)
condenser_llm = LLM(usage_id="condenser", model="claude-haiku-3-5", ...)

# Track separately
agent_cost = agent_llm.metrics.accumulated_cost
condenser_cost = condenser_llm.metrics.accumulated_cost
```

---

### Registry + Delegation

**Combined Benefits**:
- Separate LLMs for sub-agents
- Track costs per sub-agent
- Optimize sub-agent models

**Example**:
```python
# Main agent LLM
main_llm = LLM(usage_id="main_agent", ...)

# Sub-agent LLMs
server_llm = LLM(usage_id="sub-agent-server", ...)
electron_llm = LLM(usage_id="sub-agent-electron", ...)

# Track separately
for usage_id in ["main_agent", "sub-agent-server", "sub-agent-electron"]:
    llm = llm_registry.get(usage_id)
    print(f"{usage_id}: ${llm.metrics.accumulated_cost:.6f}")
```

---

### Registry + Observability

**Combined Benefits**:
- Traces show which LLM was used
- Usage_id in trace attributes
- Easy debugging

**Example**:
```
Trace: llm.completion
Attributes:
  - usage_id: "agent"
  - model: "claude-sonnet-4-5"
  - provider: "anthropic"
```

---

## Advanced Usage

### Listing Registered LLMs

**List all registered usage_ids**:
```python
registered_llms = llm_registry.list_usage_ids()
print(f"Registered LLMs: {registered_llms}")
# Output: ['agent', 'condenser', 'sub-agent-server']
```

---

### Direct LLM Completion

**Use LLM directly from registry**:
```python
from openhands.sdk import Message, TextContent

llm = llm_registry.get("agent")
response = llm.completion(
    messages=[
        Message(role="user", content=[TextContent(text="Hello!")])
    ]
)
```

**Benefit**: Use LLMs outside of agent context.

---

### Dynamic Model Switching

**Switch models based on conditions**:
```python
# Register multiple models
llm_registry.add(LLM(usage_id="fast", model="claude-haiku", ...))
llm_registry.add(LLM(usage_id="smart", model="claude-sonnet", ...))

# Switch based on task
if task_is_simple:
    llm = llm_registry.get("fast")
else:
    llm = llm_registry.get("smart")

agent = Agent(llm=llm, ...)
```

---

## Troubleshooting

### LLM Not Found

**Problem**: `llm_registry.get("usage_id")` returns None

**Solutions**:
1. Verify LLM was added to registry:
   ```python
   llm_registry.add(llm)
   ```

2. Check usage_id spelling:
   ```python
   # Correct
   llm = llm_registry.get("agent")
   
   # Incorrect
   llm = llm_registry.get("Agent")  # Case-sensitive
   ```

3. List registered LLMs:
   ```python
   print(llm_registry.list_usage_ids())
   ```

---

### Costs Not Tracking

**Problem**: Metrics not updating

**Solutions**:
1. Verify LLM is from registry:
   ```python
   llm = llm_registry.get("agent")  # Correct
   # Not: llm = LLM(...)  # Wrong - not in registry
   ```

2. Check metrics after use:
   ```python
   conversation.run()
   cost = llm_registry.get("agent").metrics.accumulated_cost
   ```

---

## Example: Complete Setup

```python
from openhands.sdk import LLM, LLMRegistry, Agent, Conversation
from openhands.sdk.context.condenser import LLMSummarizingCondenser

# Create registry
llm_registry = LLMRegistry()

# Register agent LLM
agent_llm = LLM(
    usage_id="agent",
    model="anthropic/claude-sonnet-4-5-20250929",
    api_key=SecretStr(api_key),
)
llm_registry.add(agent_llm)

# Register condenser LLM (cheaper model)
condenser_llm = LLM(
    usage_id="condenser",
    model="anthropic/claude-haiku-3-5-20241022",  # Cheaper
    api_key=SecretStr(api_key),
)
llm_registry.add(condenser_llm)

# Use in agent and condenser
agent = Agent(
    llm=llm_registry.get("agent"),
    condenser=LLMSummarizingCondenser(llm=llm_registry.get("condenser"), ...),
)

# Create conversation with registry
conversation = Conversation(agent=agent, ...)
conversation.llm_registry = llm_registry

# Track costs separately
agent_cost = llm_registry.get("agent").metrics.accumulated_cost
condenser_cost = llm_registry.get("condenser").metrics.accumulated_cost
total_cost = conversation.conversation_stats.get_combined_metrics().accumulated_cost
```

---

## Conclusion

**LLM Registry Benefits**:
- ✅ Centralized LLM management
- ✅ Separate cost tracking
- ✅ Easy model switching
- ✅ Better organization

**Essential for**:
- Multiple LLM scenarios
- Cost optimization
- Model selection
- Production deployments

**This is essential for managing multiple LLMs!**

---

**LLM Registry Guide Complete**: 2026-01-14 21:00:00