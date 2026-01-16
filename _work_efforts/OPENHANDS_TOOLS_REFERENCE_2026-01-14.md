# OpenHands SDK Built-in Tools Reference

**Date**: 2026-01-14 20:22:22
**Source**: OpenHands Software Agent SDK Documentation
**Status**: 📋 COMPLETE TOOL LIST

---

## Complete List of Built-in Tools

Based on OpenHands SDK documentation and examples, here are the available built-in tools:

### Core Tools (Most Commonly Used)

1. **TerminalTool** (`openhands.tools.terminal.TerminalTool`)
   - **Purpose**: Execute bash/terminal commands
   - **Use Case**: Run commands, install packages, execute scripts
   - **Example**: `Tool(name=TerminalTool.name)`

2. **FileEditorTool** (`openhands.tools.file_editor.FileEditorTool`)
   - **Purpose**: Create, read, edit, and delete files
   - **Use Case**: Write code, edit configuration, create documentation
   - **Example**: `Tool(name=FileEditorTool.name)`

3. **TaskTrackerTool** (`openhands.tools.task_tracker.TaskTrackerTool`)
   - **Purpose**: Track and manage task progress
   - **Use Case**: Break down complex tasks, track completion
   - **Example**: `Tool(name=TaskTrackerTool.name)`

### Additional Tools (From Documentation References)

4. **BashTool** (`openhands.tools.BashTool`)
   - **Purpose**: Execute bash commands (alternative to TerminalTool)
   - **Note**: May be an alias or variant of TerminalTool

5. **Web Browsing Tools** (via MCP integration)
   - **Purpose**: Browse the web, search, gather information
   - **Integration**: Tavily MCP (mentioned in God of Science analysis)
   - **Use Case**: Research, web scraping, information gathering

### Getting Default Tools

You can get all default tools using:

```python
from openhands.tools.preset import get_default_tools

# Get all default tools
tools = get_default_tools()
agent = Agent(llm=llm, tools=tools)
```

### Tool Source Code

For the complete, up-to-date list of all available tools, see:
- **GitHub Source**: https://github.com/OpenHands/software-agent-sdk/tree/main/openhands-tools/openhands/tools
- **Documentation**: https://docs.openhands.dev/sdk/arch/tool-system

---

## Recommended Tool Set for Game Development

For generating the Electron Tavern Game, use these three core tools:

```python
from openhands.tools.file_editor import FileEditorTool
from openhands.tools.task_tracker import TaskTrackerTool
from openhands.tools.terminal import TerminalTool

agent = Agent(
    llm=llm,
    tools=[
        Tool(name=TerminalTool.name),      # Execute commands (npm, python, etc.)
        Tool(name=FileEditorTool.name),    # Create/edit files (Python, JS, HTML, CSS)
        Tool(name=TaskTrackerTool.name),   # Track multi-step tasks
    ],
)
```

**Why These Three**:
- ✅ **TerminalTool**: Run npm install, python commands, test execution
- ✅ **FileEditorTool**: Create all code files (FastAPI, Electron, tests, docs)
- ✅ **TaskTrackerTool**: Break down generation into manageable steps

**These are sufficient** for the complete game development task.

---

## Using get_default_tools()

If you want all default tools (may include additional tools):

```python
from openhands.tools.preset import get_default_tools

# Get all default tools
tools = get_default_tools()
agent = Agent(llm=llm, tools=tools)
```

**Note**: The default tools set may include additional tools beyond the three core ones. Check the source code for the complete list.

---

## Tool Registration Pattern

Tools are registered and used by name:

```python
# Register tools
from openhands.sdk.tool import register_tool

# Use by name
tools = [
    Tool(name=TerminalTool.name),
    Tool(name=FileEditorTool.name),
    Tool(name=TaskTrackerTool.name),
]
```

---

## Custom Tools (Optional)

You can create custom tools for specialized needs. Here's the pattern from the OpenHands documentation:

### Custom Tool Pattern

```python
from openhands.sdk import Action, Observation, ToolDefinition, ToolExecutor
from openhands.sdk.tool import register_tool
from pydantic import Field
from collections.abc import Sequence
from openhands.sdk import TextContent, ImageContent

# 1. Define Action (input parameters)
class CustomAction(Action):
    param1: str = Field(description="Description of parameter")
    param2: int = Field(default=0, description="Optional parameter")

# 2. Define Observation (output data)
class CustomObservation(Observation):
    result: str = Field(default="")
    count: int = 0
    
    @property
    def to_llm_content(self) -> Sequence[TextContent | ImageContent]:
        """Format output for LLM consumption."""
        return [TextContent(text=f"Result: {self.result}, Count: {self.count}")]

# 3. Define Executor (tool logic)
class CustomExecutor(ToolExecutor[CustomAction, CustomObservation]):
    def __init__(self, terminal: TerminalExecutor):
        self.terminal: TerminalExecutor = terminal
    
    def __call__(self, action: CustomAction, conversation=None) -> CustomObservation:
        # Implement tool logic here
        # Can use terminal executor for commands
        # Return CustomObservation with results
        return CustomObservation(result="done", count=1)

# 4. Define Tool (register with agent)
class CustomTool(ToolDefinition[CustomAction, CustomObservation]):
    @classmethod
    def create(cls, conv_state, terminal_executor=None) -> Sequence[ToolDefinition]:
        if terminal_executor is None:
            terminal_executor = TerminalExecutor(
                working_dir=conv_state.workspace.working_dir
            )
        executor = CustomExecutor(terminal_executor)
        
        return [
            cls(
                description="Tool description for LLM",
                action_type=CustomAction,
                observation_type=CustomObservation,
                executor=executor,
            )
        ]

# 5. Register tool
def _make_custom_tools(conv_state) -> list[ToolDefinition]:
    terminal_executor = TerminalExecutor(working_dir=conv_state.workspace.working_dir)
    custom_tool = CustomTool.create(conv_state, terminal_executor=terminal_executor)[0]
    return [custom_tool]

register_tool("CustomToolSet", _make_custom_tools)

# 6. Use in agent
tools = [
    Tool(name=FileEditorTool.name),
    Tool(name="CustomToolSet"),
]
```

### Example: Grep Tool (from OpenHands docs)

The OpenHands documentation includes a complete example of a custom grep tool that:
- Searches file contents using regex
- Filters by file pattern (e.g., `*.py`)
- Returns formatted results to the LLM
- Shares terminal executor with other tools

See the example code provided for the complete implementation.

### Potential Custom Tools for Game Development

If you wanted to create specialized tools for the game:

1. **D&D Character Validator Tool**:
   - Validates character stats, modifiers, AC calculations
   - Ensures D&D 5e rules compliance

2. **Game State Checker Tool**:
   - Verifies game state consistency
   - Checks for invalid transitions
   - Validates choice availability

3. **Scenario Generator Tool**:
   - Generates game scenarios based on templates
   - Creates balanced encounters
   - Generates narrative content

**Note**: For initial game development, **custom tools are NOT needed**. The built-in tools (TerminalTool, FileEditorTool, TaskTrackerTool) are sufficient for generating all the code.

---

## MCP Integration

OpenHands supports MCP (Model Context Protocol) tools:

- **Tavily MCP**: Web browsing/search (mentioned in documentation)
- **Custom MCP Servers**: Can integrate your own MCP servers

**For game development**: MCP tools are **optional** - not needed for code generation.

---

## Tool Capabilities Summary

| Tool | Capability | Use Case |
|------|-----------|----------|
| **TerminalTool** | Execute bash commands | Run npm, python, git commands |
| **FileEditorTool** | Create/edit files | Write code, edit configs |
| **TaskTrackerTool** | Track tasks | Break down complex work |
| **BashTool** | Execute bash (alternative) | Same as TerminalTool |
| **Web Tools** (MCP) | Browse/search web | Research, information gathering |
| **Custom Tools** | Specialized operations | Domain-specific needs |

---

## Verification

To see all available tools in your installation:

```python
from openhands.tools.preset import get_default_tools

tools = get_default_tools()
for tool in tools:
    print(f"Tool: {tool.name}")
    print(f"Description: {tool.description}")
    print()
```

Or check the source code:
```bash
# If you have the SDK installed
python -c "from openhands.tools.preset import get_default_tools; print([t.name for t in get_default_tools()])"
```

---

## For Game Development

**Recommended Tool Set** (sufficient for all tasks):

```python
tools = [
    Tool(name=TerminalTool.name),      # Commands
    Tool(name=FileEditorTool.name),    # Files
    Tool(name=TaskTrackerTool.name),   # Tasks
]
```

**Or use default tools** (includes above + potentially more):

```python
from openhands.tools.preset import get_default_tools
tools = get_default_tools()
```

---

## Custom Tool Example

A complete example of a custom grep tool is provided in the OpenHands documentation. The pattern includes:

1. **Action**: Define input parameters with Pydantic Field descriptions
2. **Observation**: Define output data with `to_llm_content` property for formatting
3. **Executor**: Implement tool logic (can use TerminalExecutor for commands)
4. **Tool Definition**: Register tool with description and types
5. **Registration**: Use `register_tool()` to make tool available
6. **Usage**: Reference by name in agent tools list

**Example File**: `scripts/example_custom_tool_dnd_validator.py` shows a D&D character validator tool example.

**For Game Development**: Custom tools are **optional** - built-in tools are sufficient for code generation.

---

**Reference Created**: 2026-01-14 20:22:22
**Source**: OpenHands SDK Documentation + GitHub Source Code