# OpenHands Sub-Agent Delegation for Parallel Execution

**Date**: 2026-01-14 20:40:00
**Context**: Using OpenHands sub-agent delegation for parallel task execution
**Status**: 🤝 PARALLEL EXECUTION ENABLED

---

## What Is Sub-Agent Delegation?

Sub-agent delegation enables **parallel task execution** by delegating work to multiple sub-agents that run independently and return consolidated results.

**Key Benefits**:
- ✅ **Parallel Processing**: Multiple tasks execute simultaneously
- ✅ **Specialized Agents**: Each sub-agent can have specialized skills
- ✅ **Improved Throughput**: Faster completion for parallelizable work
- ✅ **Separation of Concerns**: Different agents handle different aspects

---

## How It Works

### 1. Spawning Sub-Agents

Before delegating work, the agent must first spawn sub-agents with meaningful identifiers:

```python
# Agent uses the delegate tool to spawn sub-agents
{
    "command": "spawn",
    "ids": ["server", "electron", "tests"]
}
```

Each spawned sub-agent:
- Gets a unique identifier (e.g., "server", "electron", "tests")
- Inherits the same LLM configuration as the parent agent
- Operates in the same workspace as the main agent
- Maintains its own independent conversation context

### 2. Delegating Tasks

Once sub-agents are spawned, the agent can delegate tasks to them:

```python
# Agent uses the delegate tool to assign tasks
{
    "command": "delegate",
    "tasks": {
        "server": "Create FastAPI server for tavern game",
        "electron": "Create Electron app for tavern game",
        "tests": "Write pytest tests for the server"
    }
}
```

The delegate operation:
- ✅ Runs all sub-agent tasks **in parallel** using threads
- ✅ Blocks until all sub-agents complete their work
- ✅ Returns a single consolidated observation with all results
- ✅ Handles errors gracefully and reports them per sub-agent

---

## Use Cases for Game Development

### 1. Parallel Phase Execution

**Scenario**: Generate server, Electron app, and tests in parallel

**Without Delegation**:
- Phase 1: Generate server (5 minutes)
- Phase 2: Generate Electron app (5 minutes)
- Phase 3: Generate tests (5 minutes)
- **Total**: 15 minutes (sequential)

**With Delegation**:
- All three phases run in parallel
- **Total**: ~5 minutes (parallel)
- **Speedup**: 3x faster!

**Example**:
```python
# Spawn three sub-agents
spawn(["server", "electron", "tests"])

# Delegate tasks in parallel
delegate({
    "server": "Create FastAPI server",
    "electron": "Create Electron app",
    "tests": "Write pytest tests"
})

# All three tasks execute simultaneously!
```

---

### 2. Specialized Sub-Agents

**Scenario**: Each sub-agent has specialized knowledge

**Server Developer Sub-Agent**:
- Specialized in FastAPI development
- Knows security best practices
- Understands async patterns
- Focused on server-side code

**Electron Developer Sub-Agent**:
- Specialized in Electron development
- Knows security best practices
- Understands UI/UX patterns
- Focused on client-side code

**Test Developer Sub-Agent**:
- Specialized in pytest testing
- Knows async testing patterns
- Understands coverage requirements
- Focused on test quality

**Benefit**: Each sub-agent is an expert in its domain!

---

### 3. Independent Task Processing

**Scenario**: Tasks that don't depend on each other

**Independent Tasks**:
- Server development (doesn't need Electron code)
- Electron development (doesn't need test code)
- Test development (needs server code, but can start with stubs)

**With Delegation**:
- Server and Electron can run in parallel
- Tests can start with server stubs, then update when server is ready
- Overall faster completion

---

## Setting Up Delegation

### 1. Register DelegateTool

```python
from openhands.sdk.tool import register_tool
from openhands.tools.delegate import DelegateTool

register_tool("DelegateTool", DelegateTool)
```

### 2. Add to Agent Tools

```python
from openhands.sdk import Tool

tools = [
    Tool(name=TerminalTool.name),
    Tool(name=FileEditorTool.name),
    Tool(name="DelegateTool"),  # Add delegation tool
]

agent = Agent(llm=llm, tools=tools)
```

### 3. Create Specialized Sub-Agents (Optional)

```python
from openhands.tools.delegate import register_agent

def create_server_agent(llm: LLM) -> Agent:
    """Create a sub-agent specialized in FastAPI server development."""
    return Agent(
        llm=llm,
        tools=[Tool(name=TerminalTool.name), Tool(name=FileEditorTool.name)],
        agent_context=AgentContext(
            skills=[Skill(name="fastapi-expert", content="...", trigger=None)],
            system_message_suffix="Focus only on FastAPI server development.",
        ),
    )

# Register the specialized agent
register_agent(
    name="server_developer",
    factory_func=create_server_agent,
    description="Specializes in FastAPI server development.",
)
```

### 4. Configure Maximum Sub-Agents (Optional)

```python
from openhands.tools.delegate import DelegateTool

class CustomDelegateTool(DelegateTool):
    @classmethod
    def create(cls, conv_state, max_children: int = 3):
        # Only allow up to 3 sub-agents
        return super().create(conv_state, max_children=max_children)

register_tool("DelegateTool", CustomDelegateTool)
```

---

## Integration with Generation Script

**File**: `scripts/generate_tavern_game_with_skills.py`

**New Features**:
- ✅ `--use-delegation` flag to enable sub-agent delegation
- ✅ `--max-sub-agents` flag to limit concurrent sub-agents (default: 3)
- ✅ Pre-configured specialized sub-agents:
  - `server_developer` (FastAPI expert)
  - `electron_developer` (Electron expert)
  - `test_developer` (Testing expert)
- ✅ DelegationVisualizer for monitoring

**Usage**:

```bash
# Enable delegation for parallel execution
python scripts/generate_tavern_game_with_skills.py --use-delegation

# Limit concurrent sub-agents
python scripts/generate_tavern_game_with_skills.py --use-delegation --max-sub-agents 2

# Combine with other features
python scripts/generate_tavern_game_with_skills.py --use-delegation --condenser-max-size 50
```

---

## Specialized Sub-Agents for Game Development

### Server Developer

**Specialization**: FastAPI server development

**Skills**:
- FastAPI expert knowledge
- Async endpoints with asyncio.Lock()
- Pydantic models for validation
- CORS middleware configuration
- Security best practices

**Tools**: TerminalTool, FileEditorTool

**Focus**: Server-side code only

---

### Electron Developer

**Specialization**: Electron app development

**Skills**:
- Electron expert knowledge
- Security best practices (webSecurity, nodeIntegration, contextIsolation)
- contextBridge usage
- UI/UX patterns
- Real-time API polling

**Tools**: TerminalTool, FileEditorTool

**Focus**: Client-side code only

---

### Test Developer

**Specialization**: Test development

**Skills**:
- pytest expert knowledge
- Async testing patterns
- Comprehensive coverage
- Test quality best practices

**Tools**: TerminalTool, FileEditorTool

**Focus**: Test code only

---

## Tool Commands

### spawn

Initialize sub-agents with meaningful identifiers.

**Parameters**:
- `command`: `"spawn"`
- `ids`: List of string identifiers (e.g., `["server", "electron", "tests"]`)

**Returns**: Message indicating sub-agents were successfully spawned.

**Example**:
```python
{
    "command": "spawn",
    "ids": ["server", "electron", "tests"]
}
```

---

### delegate

Send tasks to specific sub-agents and wait for results.

**Parameters**:
- `command`: `"delegate"`
- `tasks`: Dictionary mapping sub-agent IDs to task descriptions

**Returns**: Consolidated message containing all results from sub-agents.

**Example**:
```python
{
    "command": "delegate",
    "tasks": {
        "server": "Create FastAPI server for tavern game",
        "electron": "Create Electron app for tavern game",
        "tests": "Write pytest tests for the server"
    }
}
```

---

## Integration with Other Features

### Delegation + Skills

**Combined Benefits**:
- Main agent has general skills (AGENTS.md, game context)
- Sub-agents have specialized skills (FastAPI, Electron, Testing)
- Each agent operates with its own skill set

**Example**:
```python
# Main agent: General game development skills
main_agent = Agent(
    llm=llm,
    tools=[Tool(name="DelegateTool")],
    agent_context=AgentContext(skills=[game_context_skill]),
)

# Sub-agent: Specialized FastAPI skills
server_agent = Agent(
    llm=llm,
    tools=[Tool(name=FileEditorTool.name)],
    agent_context=AgentContext(skills=[fastapi_skill]),
)
```

---

### Delegation + Persistence

**Combined Benefits**:
- Each sub-agent can have its own persistence
- Main agent persists delegation state
- Resume delegation workflows across sessions

**Note**: Sub-agents use the same workspace but have independent conversation contexts.

---

### Delegation + Condenser

**Combined Benefits**:
- Each sub-agent can have its own condenser
- Main agent condenser manages main conversation
- Parallel execution doesn't bloat main context

**Example**:
```python
# Main agent with condenser
main_agent = Agent(
    llm=llm,
    tools=[Tool(name="DelegateTool")],
    condenser=condenser,
)

# Sub-agents with their own condensers
sub_agent = Agent(
    llm=llm,
    tools=[Tool(name=FileEditorTool.name)],
    condenser=sub_condenser,  # Separate condenser
)
```

---

### Delegation + MCP

**Combined Benefits**:
- Sub-agents can use MCP servers
- Main agent coordinates via delegation
- MCP tools available to all agents

**Note**: All agents share the same workspace, so MCP servers work for all.

---

## Performance Benefits

### Speed Improvement

**Sequential Execution** (without delegation):
- Phase 1: 5 minutes
- Phase 2: 5 minutes
- Phase 3: 5 minutes
- **Total**: 15 minutes

**Parallel Execution** (with delegation):
- All phases: ~5 minutes (longest phase)
- **Total**: ~5 minutes
- **Speedup**: 3x faster!

---

### Resource Efficiency

**Parallel Execution**:
- Multiple LLM calls happen simultaneously
- Better GPU/API utilization
- Faster overall completion

**Note**: API rate limits may apply. Use `--max-sub-agents` to control concurrency.

---

## Best Practices

### 1. Use for Independent Tasks

**Good Use Cases**:
- ✅ Server development (independent)
- ✅ Electron app development (independent)
- ✅ Test development (can start with stubs)
- ✅ Documentation generation (independent)

**Avoid For**:
- ❌ Tasks that depend on each other (use sequential)
- ❌ Tasks that share mutable state (use sequential)
- ❌ Tasks that require coordination (use sequential)

---

### 2. Limit Concurrent Sub-Agents

**Why**: API rate limits, resource constraints

**How**:
```python
# Limit to 3 concurrent sub-agents
python scripts/generate_tavern_game_with_skills.py --use-delegation --max-sub-agents 3
```

**Default**: 3 sub-agents (good balance)

---

### 3. Specialize Sub-Agents

**Benefits**:
- Each sub-agent is an expert in its domain
- Better code quality
- More focused context

**How**:
```python
# Create specialized sub-agents
register_agent(
    name="server_developer",
    factory_func=create_server_agent,
    description="Specializes in FastAPI server development.",
)
```

---

### 4. Monitor Delegation

**Use DelegationVisualizer**:
```python
from openhands.tools.delegate import DelegationVisualizer

conversation = Conversation(
    agent=agent,
    workspace=workspace_path,
    visualizer=DelegationVisualizer(name="Game Developer"),
)
```

**Benefits**:
- Visual monitoring of sub-agent execution
- Track parallel progress
- Debug delegation issues

---

## Troubleshooting

### Sub-Agents Not Spawning

**Issue**: Sub-agents fail to spawn

**Solutions**:
- Check DelegateTool is registered
- Verify sub-agent factory functions are correct
- Check LLM configuration is valid
- Review error messages

---

### Tasks Not Executing in Parallel

**Issue**: Tasks execute sequentially

**Solutions**:
- Verify tasks are independent
- Check for shared state dependencies
- Review delegation command format
- Check thread execution

---

### Sub-Agent Errors

**Issue**: Sub-agent fails during execution

**Solutions**:
- Check sub-agent tools are available
- Verify workspace permissions
- Review sub-agent error messages
- Check LLM API limits

---

## Advanced: Custom Sub-Agent Types

### Creating Custom Types

```python
def create_custom_agent(llm: LLM) -> Agent:
    """Create a custom sub-agent."""
    return Agent(
        llm=llm,
        tools=[Tool(name=FileEditorTool.name)],
        agent_context=AgentContext(
            skills=[Skill(name="custom", content="...", trigger=None)],
        ),
    )

# Register custom type
register_agent(
    name="custom_agent",
    factory_func=create_custom_agent,
    description="Custom agent description.",
)
```

### Using Custom Types

```python
# Agent can spawn custom sub-agents
{
    "command": "spawn",
    "ids": ["custom1", "custom2"]
}

# Delegate to custom sub-agents
{
    "command": "delegate",
    "tasks": {
        "custom1": "Task for custom agent 1",
        "custom2": "Task for custom agent 2"
    }
}
```

---

## Conclusion

**Sub-Agent Delegation Benefits**:
- ✅ Parallel execution (3x speedup)
- ✅ Specialized agents (better quality)
- ✅ Improved throughput
- ✅ Separation of concerns

**Essential for**:
- Multi-phase workflows
- Independent tasks
- Specialized development
- Performance-critical generation

**This is a game-changer for parallel execution!**

---

**Sub-Agent Delegation Guide Complete**: 2026-01-14 20:40:00