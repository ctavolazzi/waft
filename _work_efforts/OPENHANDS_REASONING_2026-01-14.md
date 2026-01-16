# OpenHands Reasoning Traces for Transparency & Debugging

**Date**: 2026-01-14 21:10:00
**Context**: Using OpenHands reasoning traces to access model's internal reasoning process
**Status**: 🧠 REASONING TRACES ENABLED

---

## What Is Reasoning?

Reasoning provides access to **model reasoning traces** from Anthropic extended thinking and OpenAI responses API. This allows you to:

- ✅ **View internal reasoning**: See how the model thinks through problems
- ✅ **Debug decisions**: Understand why the agent made specific choices
- ✅ **Transparency**: Show users how the AI arrived at conclusions
- ✅ **Quality assurance**: Identify flawed reasoning patterns

**Key Benefits**:
- Debugging agent behavior
- Transparency in decision-making
- Quality assurance
- Learning from model approaches

---

## Two Provider Approaches

### 1. Anthropic Extended Thinking

**Claude's thinking blocks** for complex reasoning:

- **`ThinkingBlock`**: Full reasoning text from Claude's internal thought process
- **`RedactedThinkingBlock`**: Redacted or summarized thinking data

**How It Works**:
```python
def show_thinking(event: Event):
    if isinstance(event, LLMConvertibleEvent):
        message = event.to_llm_message()
        if hasattr(message, "thinking_blocks") and message.thinking_blocks:
            for block in message.thinking_blocks:
                if isinstance(block, ThinkingBlock):
                    print(f"Thinking: {block.thinking}")
                elif isinstance(block, RedactedThinkingBlock):
                    print(f"Redacted: {block.data}")

conversation = Conversation(agent=agent, callbacks=[show_thinking])
```

---

### 2. OpenAI Reasoning via Responses API

**GPT's reasoning effort parameter** for reasoning traces:

- **`reasoning_effort`**: Control amount of reasoning (`"none"`, `"low"`, `"medium"`, `"high"`)
- **Reasoning traces**: Show how model approached the problem

**How It Works**:
```python
llm = LLM(
    model="openhands/gpt-5-codex",
    api_key=api_key,
    reasoning_effort="high",  # Enable reasoning
)

# Reasoning traces available in LLM messages
def conversation_callback(event: Event):
    if isinstance(event, LLMConvertibleEvent):
        msg = event.to_llm_message()
        # Access reasoning traces from msg
```

---

## Integration with Generation Script

**File**: `scripts/generate_tavern_game_with_skills.py`

**New Features**:
- ✅ `--show-reasoning` flag to display reasoning traces
- ✅ `--reasoning-effort` flag for OpenAI models (none/low/medium/high)
- ✅ Automatic detection of Anthropic vs OpenAI
- ✅ Real-time reasoning display

**Usage**:

```bash
# Enable reasoning for Anthropic Claude
export LLM_MODEL="anthropic/claude-sonnet-4-5-20250929"
python scripts/generate_tavern_game_with_skills.py --show-reasoning

# Enable reasoning for OpenAI GPT
export LLM_MODEL="openhands/gpt-5-codex"
python scripts/generate_tavern_game_with_skills.py --show-reasoning --reasoning-effort high
```

**Output**:
```
🧠 Reasoning enabled (effort: high)
   (OpenAI reasoning traces will be displayed)

🧠 Thinking Blocks (2):
  Block 1: Let me break down this problem step by step...
  Block 2: First, I need to understand the requirements...
```

---

## Use Cases

### 1. Debugging Agent Behavior

**Problem**: Agent not working as expected

**Solution**: Use reasoning traces to see:
- How model approached the problem
- What decisions were made
- Why specific actions were taken

**Example**:
```python
# Enable reasoning
conversation = Conversation(agent=agent, callbacks=[show_reasoning])

# See reasoning during execution
conversation.send_message("Create FastAPI server")
conversation.run()
# Output: Thinking blocks show step-by-step reasoning
```

---

### 2. Transparency

**Problem**: Need to show users how AI arrived at conclusions

**Solution**: Display reasoning traces:
- Show thinking process
- Explain decision-making
- Build trust through transparency

**Example**:
```python
# Show reasoning to users
def show_reasoning(event: Event):
    if isinstance(event, LLMConvertibleEvent):
        message = event.to_llm_message()
        if hasattr(message, "thinking_blocks"):
            for block in message.thinking_blocks:
                display_to_user(block.thinking)  # Show to user
```

---

### 3. Quality Assurance

**Problem**: Identify flawed reasoning patterns

**Solution**: Analyze reasoning traces:
- Check for logical errors
- Identify flawed patterns
- Improve agent behavior

**Example**:
```python
# Analyze reasoning
for block in thinking_blocks:
    if contains_logical_error(block.thinking):
        flag_for_review(block)
```

---

### 4. Learning

**Problem**: Understand how models approach complex problems

**Solution**: Study reasoning traces:
- Learn model approaches
- Understand decision-making
- Improve prompts based on reasoning

**Example**:
```python
# Study reasoning patterns
analyze_reasoning_patterns(thinking_blocks)
identify_common_approaches()
improve_prompts_based_on_findings()
```

---

## Understanding Thinking Blocks (Anthropic)

### ThinkingBlock

**Full reasoning text** from Claude's internal thought process:

```python
if isinstance(block, ThinkingBlock):
    print(f"Thinking: {block.thinking}")
    # Contains step-by-step reasoning
    # Shows how Claude approached the problem
```

**Example Content**:
```
Thinking: Let me break down this problem:
1. First, I need to understand the requirements
2. Then, I'll identify the key components
3. Finally, I'll implement the solution
```

---

### RedactedThinkingBlock

**Redacted or summarized thinking data**:

```python
if isinstance(block, RedactedThinkingBlock):
    print(f"Redacted: {block.data}")
    # Contains redacted/summarized thinking
    # May be truncated for efficiency
```

**Use Case**: When thinking is too long or sensitive.

---

## Understanding Reasoning Traces (OpenAI)

### Reasoning Effort Levels

**Control amount of reasoning**:

- **`"none"`**: No reasoning traces
- **`"low"`**: Minimal reasoning
- **`"medium"`**: Moderate reasoning
- **`"high"`**: Extensive reasoning (recommended for debugging)

**Example**:
```python
llm = LLM(
    model="openhands/gpt-5-codex",
    reasoning_effort="high",  # Maximum reasoning
)
```

---

### Accessing Reasoning

**Reasoning traces available in LLM messages**:

```python
def conversation_callback(event: Event):
    if isinstance(event, LLMConvertibleEvent):
        msg = event.to_llm_message()
        # Access reasoning from msg
        if hasattr(msg, "reasoning"):
            print(f"Reasoning: {msg.reasoning}")
```

---

## Integration with Other Features

### Reasoning + Observability

**Combined Benefits**:
- Traces show execution flow
- Reasoning shows thinking process
- Together: complete picture

**Example**:
```
Trace: agent.step
  Reasoning: Let me break down this problem...
  Action: tool.execute("file_editor")
```

---

### Reasoning + Metrics

**Combined Benefits**:
- Metrics show costs
- Reasoning shows quality
- Together: cost vs quality analysis

**Example**:
```python
# High reasoning effort = higher costs
# But better quality decisions
reasoning_cost = llm.metrics.accumulated_cost
quality_score = analyze_reasoning_quality(thinking_blocks)
```

---

### Reasoning + Persistence

**Combined Benefits**:
- Reasoning persisted in conversation state
- Resume with full reasoning history
- Analyze reasoning across sessions

---

## Best Practices

### 1. Use for Debugging

**Enable reasoning when debugging**:
```bash
python scripts/generate_tavern_game_with_skills.py --show-reasoning
```

**Benefit**: See exactly how model thinks.

---

### 2. Adjust Reasoning Effort

**Balance cost vs quality**:
```python
# High effort (better quality, higher cost)
llm = LLM(reasoning_effort="high", ...)

# Low effort (faster, lower cost)
llm = LLM(reasoning_effort="low", ...)
```

---

### 3. Filter Reasoning Output

**Show only relevant reasoning**:
```python
def show_reasoning(event: Event):
    if isinstance(event, LLMConvertibleEvent):
        message = event.to_llm_message()
        if hasattr(message, "thinking_blocks"):
            for block in message.thinking_blocks:
                if is_relevant(block.thinking):
                    print(block.thinking)
```

---

### 4. Store Reasoning for Analysis

**Save reasoning traces for later analysis**:
```python
reasoning_log = []

def log_reasoning(event: Event):
    if isinstance(event, LLMConvertibleEvent):
        message = event.to_llm_message()
        if hasattr(message, "thinking_blocks"):
            reasoning_log.append(message.thinking_blocks)

# Analyze later
analyze_reasoning_patterns(reasoning_log)
```

---

## Troubleshooting

### No Thinking Blocks

**Problem**: Thinking blocks not appearing

**Solutions**:
1. Verify model supports extended thinking:
   ```python
   # Anthropic Claude models support thinking
   model = "anthropic/claude-sonnet-4-5-20250929"
   ```

2. Check callback is registered:
   ```python
   conversation = Conversation(agent=agent, callbacks=[show_reasoning])
   ```

3. Verify callback checks for thinking blocks:
   ```python
   if hasattr(message, "thinking_blocks") and message.thinking_blocks:
   ```

---

### No Reasoning Traces

**Problem**: OpenAI reasoning not appearing

**Solutions**:
1. Verify model supports Responses API:
   ```python
   # GPT-5 models support reasoning
   model = "openhands/gpt-5-codex"
   ```

2. Check reasoning_effort is set:
   ```python
   llm = LLM(reasoning_effort="high", ...)
   ```

3. Verify callback accesses reasoning:
   ```python
   if hasattr(msg, "reasoning") and msg.reasoning:
   ```

---

## Advanced Usage

### Custom Reasoning Display

**Format reasoning for specific needs**:
```python
def custom_reasoning_display(event: Event):
    if isinstance(event, LLMConvertibleEvent):
        message = event.to_llm_message()
        if hasattr(message, "thinking_blocks"):
            for i, block in enumerate(message.thinking_blocks):
                if isinstance(block, ThinkingBlock):
                    # Custom formatting
                    formatted = format_thinking(block.thinking)
                    display_in_ui(formatted)
```

---

### Reasoning Analysis

**Analyze reasoning patterns**:
```python
def analyze_reasoning(thinking_blocks):
    patterns = {
        "step_by_step": 0,
        "direct_solution": 0,
        "exploration": 0,
    }
    
    for block in thinking_blocks:
        if "step by step" in block.thinking.lower():
            patterns["step_by_step"] += 1
        # ... more analysis
    
    return patterns
```

---

## Example: Complete Setup

```python
from openhands.sdk import (
    LLM, Agent, Conversation, Event, LLMConvertibleEvent,
    ThinkingBlock, RedactedThinkingBlock
)

# Configure LLM with reasoning
llm = LLM(
    model="anthropic/claude-sonnet-4-5-20250929",
    api_key=api_key,
    # For OpenAI: reasoning_effort="high"
)

# Reasoning callback
def show_reasoning(event: Event):
    if isinstance(event, LLMConvertibleEvent):
        message = event.to_llm_message()
        
        # Anthropic thinking blocks
        if hasattr(message, "thinking_blocks") and message.thinking_blocks:
            print(f"\n🧠 Thinking Blocks ({len(message.thinking_blocks)}):")
            for i, block in enumerate(message.thinking_blocks):
                if isinstance(block, ThinkingBlock):
                    print(f"  Block {i + 1}: {block.thinking[:200]}...")
                elif isinstance(block, RedactedThinkingBlock):
                    print(f"  Block {i + 1}: [REDACTED]")
        
        # OpenAI reasoning
        if hasattr(message, "reasoning") and message.reasoning:
            print(f"\n🧠 Reasoning Trace:")
            print(f"  {str(message.reasoning)[:200]}...")

# Create conversation with reasoning callback
conversation = Conversation(
    agent=agent,
    callbacks=[show_reasoning],
    workspace=workspace_path,
)

# Run and see reasoning
conversation.send_message("Solve this complex problem")
conversation.run()
# Reasoning displayed in real-time
```

---

## Conclusion

**Reasoning Benefits**:
- ✅ Debugging agent behavior
- ✅ Transparency in decision-making
- ✅ Quality assurance
- ✅ Learning from model approaches

**Essential for**:
- Debugging complex agents
- Building trust with users
- Quality assurance
- Research and learning

**This is essential for transparency and debugging!**

---

**Reasoning Guide Complete**: 2026-01-14 21:10:00