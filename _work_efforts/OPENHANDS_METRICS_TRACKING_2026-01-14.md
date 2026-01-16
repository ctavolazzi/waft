# OpenHands Metrics Tracking for Cost & Performance Monitoring

**Date**: 2026-01-14 20:45:00
**Context**: Using OpenHands metrics tracking to monitor costs and performance
**Status**: 📊 METRICS TRACKING ENABLED

---

## What Is Metrics Tracking?

OpenHands SDK provides **comprehensive metrics tracking** at two levels:

1. **Individual LLM Metrics**: Track token usage, costs, and latencies per API call
2. **Conversation-Level Metrics**: Aggregate costs across all LLMs used in a conversation

**Key Benefits**:
- ✅ **Cost Visibility**: Track spending across all LLMs
- ✅ **Performance Monitoring**: Monitor response times and latency
- ✅ **Token Optimization**: Understand token usage patterns
- ✅ **Usage Breakdown**: See costs by usage_id (agent, condenser, sub-agents)

---

## Individual LLM Metrics

### Accessing Metrics

Access metrics directly from the LLM object after running the conversation:

```python
conversation.run()

assert llm.metrics is not None
print(f"Final LLM metrics: {llm.metrics.model_dump()}")
```

### Available Metrics

The `llm.metrics` object provides:

- **`accumulated_cost`**: Total accumulated cost across all API calls
- **`accumulated_token_usage`**: Aggregated token usage with fields:
  - `prompt_tokens`: Number of input tokens processed
  - `completion_tokens`: Number of output tokens generated
  - `cache_read_tokens`: Cache hits (if supported)
  - `cache_write_tokens`: Cache writes (if supported)
  - `reasoning_tokens`: Reasoning tokens (for extended thinking models)
  - `context_window`: Context window size used
- **`costs`**: List of individual cost records per API call
- **`token_usages`**: List of detailed token usage records per API call
- **`response_latencies`**: List of response latency metrics per API call

---

## Conversation-Level Metrics

### Getting Combined Metrics

Get aggregated costs for an entire conversation:

```python
# Get combined metrics for entire conversation
combined_metrics = conversation.conversation_stats.get_combined_metrics()
print(f"Total cost: ${combined_metrics.accumulated_cost:.6f}")
```

### Breakdown by Usage ID

Track costs separately for each LLM:

```python
# Get metrics for specific usage_id
agent_metrics = conversation.conversation_stats.get_metrics_for_usage("agent")
print(f"Agent cost: ${agent_metrics.accumulated_cost:.6f}")

# Access all usage IDs and their metrics
for usage_id, metrics in conversation.conversation_stats.usage_to_metrics.items():
    print(f"{usage_id}: ${metrics.accumulated_cost:.6f}")
```

---

## Integration with Generation Script

**File**: `scripts/generate_tavern_game_with_skills.py`

**New Features**:
- ✅ Automatic metrics display at end of execution
- ✅ Total cost tracking
- ✅ Token usage breakdown
- ✅ Cost breakdown by usage_id (agent, condenser, sub-agents)
- ✅ Performance metrics (latency, API calls)

**Output Example**:
```
📊 Metrics & Cost Tracking
======================================================================

💰 Total Cost: $0.123456

📝 Total Tokens:
   - Prompt tokens: 45,678
   - Completion tokens: 12,345
   - Total tokens: 58,023

📊 Cost Breakdown by Usage ID:
   - agent: $0.100000 (50,000 tokens)
   - condenser: $0.023456 (8,023 tokens)

⏱️  Performance:
   - Average latency: 2.34s
   - Total API calls: 15
```

---

## Use Cases

### 1. Cost Monitoring

**Track spending across all LLMs**:
- Main agent LLM
- Condenser LLM (if using context condenser)
- Sub-agent LLMs (if using delegation)

**Example**:
```python
# Get total cost
total_cost = conversation.conversation_stats.get_combined_metrics().accumulated_cost
print(f"Total spent: ${total_cost:.6f}")

# Get breakdown
for usage_id, metrics in conversation.conversation_stats.usage_to_metrics.items():
    print(f"{usage_id}: ${metrics.accumulated_cost:.6f}")
```

---

### 2. Token Optimization

**Understand token usage patterns**:
- Prompt vs completion tokens
- Cache hits (if supported)
- Context window usage

**Example**:
```python
token_usage = combined_metrics.accumulated_token_usage
print(f"Prompt tokens: {token_usage.prompt_tokens:,}")
print(f"Completion tokens: {token_usage.completion_tokens:,}")
print(f"Cache hits: {token_usage.cache_read_tokens:,}")
```

---

### 3. Performance Monitoring

**Track response times and latency**:
- Average latency per API call
- Total API calls
- Performance trends

**Example**:
```python
latencies = combined_metrics.response_latencies
if latencies:
    avg_latency = sum(latencies) / len(latencies)
    print(f"Average latency: {avg_latency:.2f}s")
    print(f"Total API calls: {len(latencies)}")
```

---

### 4. Cost Breakdown Analysis

**Analyze costs by component**:
- Agent costs (main conversation)
- Condenser costs (context summarization)
- Sub-agent costs (parallel execution)

**Example**:
```python
# Agent costs
agent_metrics = conversation.conversation_stats.get_metrics_for_usage("agent")
print(f"Agent: ${agent_metrics.accumulated_cost:.6f}")

# Condenser costs (if using condenser)
if "condenser" in conversation.conversation_stats.usage_to_metrics:
    condenser_metrics = conversation.conversation_stats.get_metrics_for_usage("condenser")
    print(f"Condenser: ${condenser_metrics.accumulated_cost:.6f}")

# Sub-agent costs (if using delegation)
for usage_id in conversation.conversation_stats.usage_to_metrics:
    if usage_id.startswith("sub-agent"):
        sub_metrics = conversation.conversation_stats.get_metrics_for_usage(usage_id)
        print(f"{usage_id}: ${sub_metrics.accumulated_cost:.6f}")
```

---

## LLM Registry for Cost Tracking

### Using LLM Registry

The LLM Registry allows you to maintain a centralized registry of LLM instances, each identified by a unique `usage_id`:

```python
from openhands.sdk import LLMRegistry

# Create registry
llm_registry = LLMRegistry()

# Add LLMs with unique usage_ids
llm_registry.add(agent_llm)  # usage_id="agent"
llm_registry.add(condenser_llm)  # usage_id="condenser"

# Get LLMs by usage_id
agent_llm = llm_registry.get("agent")
condenser_llm = llm_registry.get("condenser")

# List all usage_ids
usage_ids = llm_registry.list_usage_ids()
```

### Benefits

- **Centralized Management**: All LLMs in one registry
- **Cost Tracking**: Each LLM tracked separately by usage_id
- **Easy Retrieval**: Get LLMs by usage_id
- **Multiple LLMs**: Support for agent, condenser, sub-agents, etc.

---

## Integration with Other Features

### Metrics + Condenser

**Track condenser costs separately**:
```python
# Condenser uses separate usage_id
condenser_llm = llm.model_copy(update={"usage_id": "condenser"})
condenser = LLMSummarizingCondenser(llm=condenser_llm, ...)

# Track costs separately
agent_cost = llm.metrics.accumulated_cost
condenser_cost = condenser_llm.metrics.accumulated_cost
total_cost = agent_cost + condenser_cost
```

---

### Metrics + Delegation

**Track sub-agent costs**:
```python
# Sub-agents use their own LLMs with usage_ids
# Track costs per sub-agent
for usage_id, metrics in conversation.conversation_stats.usage_to_metrics.items():
    if usage_id.startswith("sub-agent"):
        print(f"{usage_id}: ${metrics.accumulated_cost:.6f}")
```

---

### Metrics + Persistence

**Metrics are persisted**:
- Conversation state includes metrics
- Resume conversations with metrics intact
- Track costs across sessions

---

## Best Practices

### 1. Use Unique Usage IDs

**Assign unique usage_ids**:
```python
# Main agent
agent_llm = LLM(usage_id="agent", ...)

# Condenser
condenser_llm = LLM(usage_id="condenser", ...)

# Sub-agents
sub_agent_llm = LLM(usage_id="sub-agent-server", ...)
```

**Benefits**:
- Clear cost breakdown
- Easy identification
- Better tracking

---

### 2. Monitor Costs Regularly

**Check costs after each run**:
```python
# After conversation.run()
total_cost = conversation.conversation_stats.get_combined_metrics().accumulated_cost
print(f"Total cost: ${total_cost:.6f}")

# Set budget alerts if needed
if total_cost > 1.0:  # $1.00
    print("⚠️  Cost exceeded $1.00!")
```

---

### 3. Track Token Usage

**Monitor token consumption**:
```python
token_usage = combined_metrics.accumulated_token_usage
prompt_ratio = token_usage.prompt_tokens / (token_usage.prompt_tokens + token_usage.completion_tokens)
print(f"Prompt tokens: {prompt_ratio:.1%}")

# Optimize if prompt tokens are too high
if prompt_ratio > 0.8:
    print("⚠️  Consider using context condenser to reduce prompt tokens")
```

---

### 4. Analyze Performance

**Track latency trends**:
```python
latencies = combined_metrics.response_latencies
if latencies:
    avg_latency = sum(latencies) / len(latencies)
    max_latency = max(latencies)
    min_latency = min(latencies)
    
    print(f"Average: {avg_latency:.2f}s")
    print(f"Max: {max_latency:.2f}s")
    print(f"Min: {min_latency:.2f}s")
    
    # Alert on slow responses
    if avg_latency > 5.0:
        print("⚠️  Average latency is high, consider optimization")
```

---

## Example Output

### Full Metrics Display

```
📊 Metrics & Cost Tracking
======================================================================

💰 Total Cost: $0.123456

📝 Total Tokens:
   - Prompt tokens: 45,678
   - Completion tokens: 12,345
   - Total tokens: 58,023
   - Cache read tokens: 5,000
   - Cache write tokens: 3,000

📊 Cost Breakdown by Usage ID:
   - agent: $0.100000 (50,000 tokens)
   - condenser: $0.023456 (8,023 tokens)

⏱️  Performance:
   - Average latency: 2.34s
   - Total API calls: 15
```

---

## Troubleshooting

### Metrics Not Available

**Issue**: `llm.metrics` is None

**Solutions**:
- Ensure conversation has run: `conversation.run()`
- Check LLM is properly configured
- Verify API calls were made

---

### Incorrect Costs

**Issue**: Costs don't match expected values

**Solutions**:
- Check model pricing (varies by provider)
- Verify usage_id is correct
- Check for multiple LLM instances

---

### Missing Usage IDs

**Issue**: Expected usage_id not in metrics

**Solutions**:
- Verify LLM was added to conversation's registry
- Check usage_id spelling
- Ensure LLM was actually used

---

## Advanced: Custom Metrics Tracking

### Track Custom Metrics

```python
# Access individual cost records
costs = llm.metrics.costs
for cost_record in costs:
    print(f"Cost: ${cost_record.cost:.6f}, Timestamp: {cost_record.timestamp}")

# Access individual token usage records
token_usages = llm.metrics.token_usages
for token_record in token_usages:
    print(f"Prompt: {token_record.prompt_tokens}, Completion: {token_record.completion_tokens}")

# Access latency records
latencies = llm.metrics.response_latencies
for latency in latencies:
    print(f"Latency: {latency:.2f}s")
```

---

## Conclusion

**Metrics Tracking Benefits**:
- ✅ Cost visibility across all LLMs
- ✅ Performance monitoring
- ✅ Token usage analysis
- ✅ Usage breakdown by component

**Essential for**:
- Budget management
- Performance optimization
- Cost analysis
- Usage monitoring

**This is essential for production deployments!**

---

**Metrics Tracking Guide Complete**: 2026-01-14 20:45:00