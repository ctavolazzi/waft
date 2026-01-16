# OpenHands Model Routing for Cost Optimization

**Date**: 2026-01-14 21:05:00
**Context**: Using Model Routing to automatically route requests to different models
**Status**: 🔄 MODEL ROUTING ENABLED

---

## What Is Model Routing?

Model Routing automatically routes agent's LLM requests to different models based on task characteristics to optimize cost and performance.

**Key Benefits**:
- ✅ **Cost Optimization**: Use cheaper models for simple tasks
- ✅ **Performance Optimization**: Use expensive models only when needed
- ✅ **Automatic Routing**: No manual model selection required
- ✅ **Multimodal Support**: Route multimodal requests to capable models

**Warning**: This feature is under active development. More default routers will be available in future releases.

---

## How It Works

### MultimodalRouter (Built-in)

The `MultimodalRouter` routes requests based on content type:

- **Text-only requests** → Secondary (cheaper) LLM
- **Multimodal requests** (with images) → Primary (multimodal-capable) LLM

**Routing Logic**:
```python
if message_has_images:
    route_to = primary_llm  # Expensive, multimodal-capable
else:
    route_to = secondary_llm  # Cheaper, text-only
```

---

## Basic Usage

### Setup MultimodalRouter

```python
from openhands.sdk.llm.router import MultimodalRouter

# Primary LLM (multimodal-capable, expensive)
primary_llm = LLM(
    usage_id="agent-primary",
    model="anthropic/claude-sonnet-4-5-20250929",  # Expensive, multimodal
    api_key=api_key,
)

# Secondary LLM (text-only, cheaper)
secondary_llm = LLM(
    usage_id="agent-secondary",
    model="anthropic/claude-haiku-3-5-20241022",  # Cheaper, text-only
    api_key=api_key,
)

# Create router
multimodal_router = MultimodalRouter(
    usage_id="multimodal-router",
    llms_for_routing={"primary": primary_llm, "secondary": secondary_llm},
)

# Use router as LLM
agent = Agent(llm=multimodal_router, tools=tools)
```

---

## Integration with Generation Script

**File**: `scripts/generate_tavern_game_with_skills.py`

**New Features**:
- ✅ `--use-routing` flag to enable model routing
- ✅ `--secondary-model` flag to specify secondary model (default: claude-haiku-3-5)
- ✅ Automatic routing: text-only → cheaper, multimodal → expensive
- ✅ Cost optimization

**Usage**:

```bash
# Enable model routing
python scripts/generate_tavern_game_with_skills.py --use-routing

# Specify custom secondary model
python scripts/generate_tavern_game_with_skills.py --use-routing --secondary-model "anthropic/claude-haiku-3-5-20241022"
```

**Output**:
```
🔄 Model routing enabled:
   Primary (multimodal): anthropic/claude-sonnet-4-5-20250929
   Secondary (text-only): anthropic/claude-haiku-3-5-20241022
   (Text-only requests → cheaper model, multimodal → expensive model)
```

---

## Use Cases

### 1. Cost Optimization

**Scenario**: Most tasks are text-only, but some need multimodal

**Solution**: Route text-only to cheaper model:
```python
# Text-only request → claude-haiku (cheaper)
conversation.send_message("Create a Python file")
# Routes to: secondary_llm (cheaper)

# Multimodal request → claude-sonnet (expensive)
conversation.send_message(Message(
    content=[
        ImageContent(image_urls=["image.jpg"]),
        TextContent(text="What's in this image?")
    ]
))
# Routes to: primary_llm (expensive, but needed)
```

**Benefit**: Save costs on text-only tasks, use expensive model only when needed.

---

### 2. Performance Optimization

**Scenario**: Fast responses for simple tasks, quality for complex tasks

**Solution**: Route simple tasks to faster model:
```python
# Simple task → fast model
conversation.send_message("Echo hello")
# Routes to: secondary_llm (faster)

# Complex task → quality model
conversation.send_message("Analyze this codebase and suggest improvements")
# Routes to: primary_llm (better quality)
```

**Benefit**: Faster responses for simple tasks, quality for complex tasks.

---

### 3. Multimodal Support

**Scenario**: Agent needs to handle both text and images

**Solution**: Route based on content type:
```python
# Text-only → cheaper model
conversation.send_message("Write a function")
# Routes to: secondary_llm

# With images → multimodal model
conversation.send_message(Message(
    content=[
        ImageContent(image_urls=["screenshot.png"]),
        TextContent(text="What's wrong with this UI?")
    ]
))
# Routes to: primary_llm (multimodal-capable)
```

**Benefit**: Automatic routing based on content type.

---

## Cost Savings

### Example Cost Comparison

**Without Routing** (all requests to expensive model):
- 100 text-only requests: $10.00
- 5 multimodal requests: $2.00
- **Total**: $12.00

**With Routing** (text-only to cheaper model):
- 100 text-only requests: $2.00 (cheaper model)
- 5 multimodal requests: $2.00 (expensive model)
- **Total**: $4.00

**Savings**: 67% cost reduction!

---

## Integration with Other Features

### Routing + LLM Registry

**Combined Benefits**:
- Registry tracks all LLMs (primary, secondary, router)
- Separate cost tracking per LLM
- Easy model management

**Example**:
```python
# Register all LLMs
llm_registry.add(primary_llm)
llm_registry.add(secondary_llm)
llm_registry.add(multimodal_router)

# Track costs separately
primary_cost = llm_registry.get("agent-primary").metrics.accumulated_cost
secondary_cost = llm_registry.get("agent-secondary").metrics.accumulated_cost
router_cost = llm_registry.get("multimodal-router").metrics.accumulated_cost
```

---

### Routing + Metrics

**Combined Benefits**:
- Track costs per model
- See routing decisions
- Optimize based on usage

**Example**:
```python
# See cost breakdown
for usage_id, metrics in conversation.conversation_stats.usage_to_metrics.items():
    print(f"{usage_id}: ${metrics.accumulated_cost:.6f}")

# Output:
# agent-primary: $2.00 (multimodal requests)
# agent-secondary: $2.00 (text-only requests)
# multimodal-router: $0.00 (routing overhead)
```

---

### Routing + Condenser

**Combined Benefits**:
- Router for agent
- Separate LLM for condenser
- Optimize both

**Example**:
```python
# Agent with routing
agent_router = MultimodalRouter(...)

# Condenser with cheaper model
condenser_llm = LLM(usage_id="condenser", model="claude-haiku", ...)

agent = Agent(llm=agent_router, condenser=LLMSummarizingCondenser(llm=condenser_llm, ...))
```

---

### Routing + Delegation

**Combined Benefits**:
- Router for main agent
- Separate LLMs for sub-agents
- Optimize all components

**Example**:
```python
# Main agent with routing
main_router = MultimodalRouter(...)

# Sub-agents with specific models
server_llm = LLM(usage_id="sub-agent-server", model="claude-haiku", ...)
electron_llm = LLM(usage_id="sub-agent-electron", model="claude-haiku", ...)
```

---

## Best Practices

### 1. Choose Appropriate Models

**Select models based on needs**:
```python
# Primary: Multimodal-capable, high quality
primary_llm = LLM(model="anthropic/claude-sonnet-4-5-20250929", ...)

# Secondary: Text-only, cheaper
secondary_llm = LLM(model="anthropic/claude-haiku-3-5-20241022", ...)
```

**Benefit**: Optimize cost vs quality trade-off.

---

### 2. Monitor Routing Decisions

**Track which model is used**:
```python
# Check metrics to see routing
primary_cost = primary_llm.metrics.accumulated_cost
secondary_cost = secondary_llm.metrics.accumulated_cost

# If secondary_cost is very low, routing might not be working
# If primary_cost is very high, too many requests routed to expensive model
```

---

### 3. Test Routing Behavior

**Verify routing works correctly**:
```python
# Text-only request
conversation.send_message("Hello")
conversation.run()
# Should route to secondary_llm

# Multimodal request
conversation.send_message(Message(
    content=[ImageContent(image_urls=["image.jpg"]), TextContent(text="What's this?")]
))
conversation.run()
# Should route to primary_llm
```

---

### 4. Customize Secondary Model

**Choose secondary model based on needs**:
```python
# Very cheap (lower quality)
secondary_llm = LLM(model="anthropic/claude-haiku-3-5-20241022", ...)

# Balanced (better quality, still cheaper)
secondary_llm = LLM(model="anthropic/claude-3-5-sonnet-20241022", ...)
```

---

## Advanced: Custom Routers

### Creating Custom Router

**Extend Router base class**:
```python
from openhands.sdk.llm.router import Router

class CustomRouter(Router):
    def route(self, messages, **kwargs):
        # Custom routing logic
        if self.is_complex_task(messages):
            return self.primary_llm
        else:
            return self.secondary_llm
```

**Use Cases**:
- Route based on task complexity
- Route based on token count
- Route based on custom criteria

---

## Troubleshooting

### Routing Not Working

**Problem**: All requests go to primary model

**Solutions**:
1. Verify router is configured correctly:
   ```python
   router = MultimodalRouter(
       llms_for_routing={"primary": primary_llm, "secondary": secondary_llm},
   )
   ```

2. Check message content:
   ```python
   # Text-only should route to secondary
   # Multimodal should route to primary
   ```

3. Verify secondary model supports text:
   ```python
   # Ensure secondary model is text-capable
   secondary_llm = LLM(model="anthropic/claude-haiku-3-5-20241022", ...)
   ```

---

### High Costs

**Problem**: Too many requests routed to expensive model

**Solutions**:
1. Check if messages contain images unexpectedly
2. Verify routing logic is correct
3. Consider using cheaper primary model

---

### Low Quality

**Problem**: Secondary model quality insufficient

**Solutions**:
1. Use better secondary model:
   ```python
   secondary_llm = LLM(model="anthropic/claude-3-5-sonnet-20241022", ...)
   ```

2. Adjust routing threshold
3. Route more tasks to primary model

---

## Example: Complete Setup

```python
from openhands.sdk.llm.router import MultimodalRouter
from openhands.sdk import LLM, Agent, Conversation, LLMRegistry

# Create registry
llm_registry = LLMRegistry()

# Primary LLM (multimodal, expensive)
primary_llm = LLM(
    usage_id="agent-primary",
    model="anthropic/claude-sonnet-4-5-20250929",
    api_key=api_key,
)
llm_registry.add(primary_llm)

# Secondary LLM (text-only, cheaper)
secondary_llm = LLM(
    usage_id="agent-secondary",
    model="anthropic/claude-haiku-3-5-20241022",
    api_key=api_key,
)
llm_registry.add(secondary_llm)

# Create router
multimodal_router = MultimodalRouter(
    usage_id="multimodal-router",
    llms_for_routing={"primary": primary_llm, "secondary": secondary_llm},
)
llm_registry.add(multimodal_router)

# Use router as LLM
agent = Agent(llm=multimodal_router, tools=tools)

# Track costs separately
primary_cost = primary_llm.metrics.accumulated_cost
secondary_cost = secondary_llm.metrics.accumulated_cost
print(f"Primary: ${primary_cost:.6f}, Secondary: ${secondary_cost:.6f}")
```

---

## Conclusion

**Model Routing Benefits**:
- ✅ Cost optimization (67% savings possible)
- ✅ Performance optimization
- ✅ Automatic routing
- ✅ Multimodal support

**Essential for**:
- Cost-sensitive deployments
- Mixed text/multimodal workloads
- Performance optimization
- Production efficiency

**This is a game-changer for cost optimization!**

---

**Model Routing Guide Complete**: 2026-01-14 21:05:00