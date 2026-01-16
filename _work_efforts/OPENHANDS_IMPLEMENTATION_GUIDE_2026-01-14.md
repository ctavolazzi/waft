# OpenHands Implementation Guide for Electron Tavern Game

**Date**: 2026-01-14 20:22:22
**Context**: Practical guide for using OpenHands SDK to develop the game
**Status**: 📋 IMPLEMENTATION READY

---

## Prerequisites

### 1. Install uv Package Manager

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Verify installation:
```bash
uv --version  # Should be 0.8.13+
```

### 2. Acquire LLM API Key

**Option A: Direct Provider** (Anthropic, OpenAI, etc.)
```bash
export LLM_API_KEY="your-api-key-here"
export LLM_MODEL="anthropic/claude-sonnet-4-5-20250929"  # or your preferred model
```

**Option B: OpenHands Cloud** (Recommended)
1. Sign up at https://app.all-hands.dev
2. Get API key from https://app.all-hands.dev/settings/api-keys
3. Use OpenHands-verified models:
```bash
export LLM_MODEL="openhands/claude-sonnet-4-5-20250929"
```

**Option C: AWS Bedrock** (If using AWS)
```bash
# Install boto3
pip install openhands-sdk boto3

# Option 1: API Key Authentication (Recommended)
export AWS_BEARER_TOKEN_BEDROCK="your-bedrock-api-key"

# Option 2: AWS Credentials
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_REGION_NAME="us-west-2"

# Use bedrock/ prefix for model
export LLM_MODEL="bedrock/anthropic.claude-3-sonnet-20240229-v1:0"
```

### 3. Install OpenHands SDK

```bash
# Core SDK
pip install openhands-sdk

# Built-in tools
pip install openhands-tools

# Optional: For Docker/remote workspaces
pip install openhands-workspace
pip install openhands-agent-server
```

Or add to `pyproject.toml`:
```toml
dependencies = [
    "openhands-sdk",
    "openhands-tools",
    # Optional:
    # "openhands-workspace",
    # "openhands-agent-server",
]
```

---

## Development Workflow

### Phase 1: Generate FastAPI Server

**Goal**: Create `examples/tavern_game_server.py` following the plan and security fixes

**Script**: `scripts/generate_tavern_server.py`

```python
import os
from pathlib import Path
from openhands.sdk import LLM, Agent, Conversation, Tool
from openhands.tools.file_editor import FileEditorTool
from openhands.tools.task_tracker import TaskTrackerTool
from openhands.tools.terminal import TerminalTool

# Configure LLM
llm = LLM(
    model=os.getenv("LLM_MODEL", "anthropic/claude-sonnet-4-5-20250929"),
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL", None),
)

# Create agent with tools
agent = Agent(
    llm=llm,
    tools=[
        Tool(name=TerminalTool.name),
        Tool(name=FileEditorTool.name),
        Tool(name=TaskTrackerTool.name),
    ],
)

# Set workspace to project root
project_root = Path(__file__).parent.parent
conversation = Conversation(agent=agent, workspace=str(project_root))

# Task: Generate FastAPI server
task = """
Based on the implementation plan in .cursor/plans/electron_tavern_game_display_2508cb95.plan.md
and security fixes from _work_efforts/CRITIQUE_2026-01-14_202222_electron_tavern_game_display.md,
create examples/tavern_game_server.py with the following requirements:

1. FastAPI application binding to 127.0.0.1:8765 (local only)
2. Use asyncio.Lock() for game state management (prevents race conditions)
3. Endpoints:
   - GET /api/state - Returns current game state JSON
   - POST /api/choice - Accepts player choice, validates with Pydantic, updates state
   - GET /api/health - Health check endpoint
4. Game state structure:
   - character: Full DnD5eCharacter serialized (use to_dict() + computed properties)
   - current_scene: string
   - narrative: string
   - choices: list of choice objects with id, text, type
   - last_roll: dict with dice, result, modifier, total, dc, success
   - events: list of event history (max 100 events)
5. Security requirements:
   - CORS middleware allowing only localhost origins
   - Input validation with Pydantic models
   - Error handling with try/except blocks
   - Port availability checking before binding
6. Use existing codebase patterns:
   - Follow FastAPI patterns from src/waft/api/main.py
   - Use asyncio.Lock() pattern from src/waft/core/now_cycle.py
   - Serialize DnD5eCharacter using to_dict() method from src/waft/core/dnd5e/character.py
   - Add computed properties (modifiers, AC, proficiency_bonus) to serialization

The server should be production-ready with proper error handling, logging, and security.
"""

conversation.send_message(task)
conversation.run()

print("✅ FastAPI server generated!")
print("📝 Review examples/tavern_game_server.py before proceeding")
```

**Run**:
```bash
export LLM_API_KEY="your-key"
export LLM_MODEL="anthropic/claude-sonnet-4-5-20250929"
python scripts/generate_tavern_server.py
```

---

### Phase 2: Generate Electron App Structure

**Goal**: Create Electron app boilerplate in `tavern_display/`

**Script**: `scripts/generate_electron_app.py`

```python
import os
from pathlib import Path
from openhands.sdk import LLM, Agent, Conversation, Tool
from openhands.tools.file_editor import FileEditorTool
from openhands.tools.task_tracker import TaskTrackerTool
from openhands.tools.terminal import TerminalTool

llm = LLM(
    model=os.getenv("LLM_MODEL", "anthropic/claude-sonnet-4-5-20250929"),
    api_key=os.getenv("LLM_API_KEY"),
)

agent = Agent(
    llm=llm,
    tools=[
        Tool(name=TerminalTool.name),
        Tool(name=FileEditorTool.name),
        Tool(name=TaskTrackerTool.name),
    ],
)

project_root = Path(__file__).parent.parent
conversation = Conversation(agent=agent, workspace=str(project_root))

task = """
Based on the implementation plan in .cursor/plans/electron_tavern_game_display_2508cb95.plan.md
and security fixes from _work_efforts/CRITIQUE_2026-01-14_202222_electron_tavern_game_display.md,
create the Electron app structure in tavern_display/:

1. package.json:
   - electron dependency (~28.0.0)
   - scripts: start, dev (optional)
   - Proper project metadata

2. main.js:
   - Create Electron BrowserWindow
   - Load src/index.html
   - Set up preload script (preload.js)
   - Configure window size (1200x800)
   - Security: webSecurity: true, nodeIntegration: false, contextIsolation: true
   - Handle window close events

3. preload.js:
   - Use contextBridge to expose safe API
   - Expose window.electronAPI (no Node.js access from renderer)
   - Security best practices

4. src/index.html:
   - Three-column layout:
     - Left: Character stats panel
     - Center: Narrative text area (scrollable)
     - Right: Event log sidebar (scrollable)
   - Bottom sections:
     - Dice roll display
     - Choice buttons (dynamically generated)
   - Semantic HTML with IDs for JavaScript targeting

5. src/renderer.js:
   - API client functions:
     - fetchGameState() - Poll /api/state every 1-2 seconds
     - submitChoice(choiceId) - POST to /api/choice
   - UI update functions:
     - updateCharacterStats(character)
     - updateNarrative(text)
     - updateChoices(choices)
     - updateDiceRoll(roll)
     - addEventLog(event)
   - Event listeners for choice buttons
   - Polling loop for real-time updates
   - Error handling and connection management

6. src/styles.css:
   - Dark theme matching existing visualizer
   - D&D color scheme: parchment (#F4E4BC), gold (#D4AF37), deep blue (#1a1a2e)
   - Responsive grid layout
   - Smooth animations for dice rolls
   - Clear typography for narrative text
   - Button styling with hover effects

Follow Electron security best practices and the plan specifications.
"""

conversation.send_message(task)
conversation.run()

print("✅ Electron app structure generated!")
print("📝 Review tavern_display/ before proceeding")
```

**Run**:
```bash
export LLM_API_KEY="your-key"
python scripts/generate_electron_app.py
```

---

### Phase 3: Generate Tests

**Goal**: Create comprehensive pytest tests

**Script**: `scripts/generate_tests.py`

```python
import os
from pathlib import Path
from openhands.sdk import LLM, Agent, Conversation, Tool
from openhands.tools.file_editor import FileEditorTool
from openhands.tools.task_tracker import TaskTrackerTool
from openhands.tools.terminal import TerminalTool

llm = LLM(
    model=os.getenv("LLM_MODEL", "anthropic/claude-sonnet-4-5-20250929"),
    api_key=os.getenv("LLM_API_KEY"),
)

agent = Agent(
    llm=llm,
    tools=[
        Tool(name=TerminalTool.name),
        Tool(name=FileEditorTool.name),
        Tool(name=TaskTrackerTool.name),
    ],
)

project_root = Path(__file__).parent.parent
conversation = Conversation(agent=agent, workspace=str(project_root))

task = """
Write comprehensive pytest tests for examples/tavern_game_server.py:

1. Test GET /api/state:
   - Returns correct game state structure
   - Includes character with all computed properties
   - Includes choices, narrative, events

2. Test POST /api/choice:
   - Validates choice ID exists in current choices
   - Rejects invalid choice IDs
   - Updates game state correctly
   - Returns updated state

3. Test state management:
   - Test asyncio.Lock() prevents race conditions
   - Test concurrent requests don't corrupt state
   - Test state updates are atomic

4. Test serialization:
   - Test DnD5eCharacter serialization includes computed properties
   - Test all fields are JSON-serializable
   - Test enum handling (ArmorType)

5. Test error handling:
   - Test invalid input returns proper errors
   - Test server errors are handled gracefully
   - Test connection errors

6. Test security:
   - Test CORS only allows localhost
   - Test input validation rejects malicious input
   - Test port binding to 127.0.0.1 only

Use pytest, pytest-asyncio, and httpx for async testing.
Follow existing test patterns from tests/ directory.
"""

conversation.send_message(task)
conversation.run()

print("✅ Tests generated!")
print("📝 Review tests/ before running")
```

**Run**:
```bash
export LLM_API_KEY="your-key"
python scripts/generate_tests.py
```

---

### Phase 4: Generate Documentation

**Goal**: Create README and API documentation

**Script**: `scripts/generate_docs.py`

```python
import os
from pathlib import Path
from openhands.sdk import LLM, Agent, Conversation, Tool
from openhands.tools.file_editor import FileEditorTool
from openhands.tools.task_tracker import TaskTrackerTool
from openhands.tools.terminal import TerminalTool

llm = LLM(
    model=os.getenv("LLM_MODEL", "anthropic/claude-sonnet-4-5-20250929"),
    api_key=os.getenv("LLM_API_KEY"),
)

agent = Agent(
    llm=llm,
    tools=[
        Tool(name=TerminalTool.name),
        Tool(name=FileEditorTool.name),
        Tool(name=TaskTrackerTool.name),
    ],
)

project_root = Path(__file__).parent.parent
conversation = Conversation(agent=agent, workspace=str(project_root))

task = """
Generate comprehensive documentation:

1. tavern_display/README.md:
   - Project overview
   - Installation instructions (npm install)
   - Development workflow
   - Running the app (npm start)
   - Architecture overview
   - Security considerations

2. examples/TAVERN_GAME_API.md:
   - API endpoint documentation
   - Request/response formats
   - Game state structure
   - Error codes
   - Examples

3. Update main README.md:
   - Add section about Electron Tavern Game Display
   - Link to documentation
   - Quick start guide

Follow markdown best practices and include code examples.
"""

conversation.send_message(task)
conversation.run()

print("✅ Documentation generated!")
```

**Run**:
```bash
export LLM_API_KEY="your-key"
python scripts/generate_docs.py
```

---

## Complete Development Script

**All-in-one script**: `scripts/generate_tavern_game.py`

```python
#!/usr/bin/env python3
"""
Generate complete Electron Tavern Game using OpenHands SDK.

Usage:
    export LLM_API_KEY="your-key"
    export LLM_MODEL="anthropic/claude-sonnet-4-5-20250929"
    python scripts/generate_tavern_game.py
"""

import os
import sys
from pathlib import Path
from openhands.sdk import LLM, Agent, Conversation, Tool
from openhands.tools.file_editor import FileEditorTool
from openhands.tools.task_tracker import TaskTrackerTool
from openhands.tools.terminal import TerminalTool

def main():
    # Check for API key
    if not os.getenv("LLM_API_KEY"):
        print("❌ Error: LLM_API_KEY environment variable not set")
        print("   Set it with: export LLM_API_KEY='your-key'")
        sys.exit(1)

    # Configure LLM
    llm = LLM(
        model=os.getenv("LLM_MODEL", "anthropic/claude-sonnet-4-5-20250929"),
        api_key=os.getenv("LLM_API_KEY"),
        base_url=os.getenv("LLM_BASE_URL", None),
    )

    # Create agent
    agent = Agent(
        llm=llm,
        tools=[
            Tool(name=TerminalTool.name),
            Tool(name=FileEditorTool.name),
            Tool(name=TaskTrackerTool.name),
        ],
    )

    # Set workspace
    project_root = Path(__file__).parent.parent
    conversation = Conversation(agent=agent, workspace=str(project_root))

    print("🚀 Starting game generation with OpenHands SDK...")
    print(f"📁 Workspace: {project_root}")
    print(f"🤖 Model: {os.getenv('LLM_MODEL', 'anthropic/claude-sonnet-4-5-20250929')}")
    print()

    # Phase 1: FastAPI Server
    print("📡 Phase 1: Generating FastAPI server...")
    task1 = """
    [Same task as Phase 1 above]
    """
    conversation.send_message(task1)
    conversation.run()
    print("✅ Phase 1 complete: FastAPI server generated")
    print()

    # Phase 2: Electron App
    print("🖥️  Phase 2: Generating Electron app...")
    task2 = """
    [Same task as Phase 2 above]
    """
    conversation.send_message(task2)
    conversation.run()
    print("✅ Phase 2 complete: Electron app generated")
    print()

    # Phase 3: Tests
    print("🧪 Phase 3: Generating tests...")
    task3 = """
    [Same task as Phase 3 above]
    """
    conversation.send_message(task3)
    conversation.run()
    print("✅ Phase 3 complete: Tests generated")
    print()

    # Phase 4: Documentation
    print("📚 Phase 4: Generating documentation...")
    task4 = """
    [Same task as Phase 4 above]
    """
    conversation.send_message(task4)
    conversation.run()
    print("✅ Phase 4 complete: Documentation generated")
    print()

    print("🎉 All phases complete!")
    print("📝 Review generated code before proceeding")
    print("🧪 Run tests: pytest tests/test_tavern_game_server.py")
    print("🚀 Start server: python examples/tavern_game_server.py")
    print("🖥️  Start Electron: cd tavern_display && npm start")

if __name__ == "__main__":
    main()
```

---

## Review and Refinement Workflow

### After Generation

1. **Review Generated Code**:
   ```bash
   # Review FastAPI server
   code examples/tavern_game_server.py

   # Review Electron app
   code tavern_display/

   # Review tests
   code tests/test_tavern_game_server.py
   ```

2. **Run Tests**:
   ```bash
   pytest tests/test_tavern_game_server.py -v
   ```

3. **Manual Refinement**:
   - Fix any issues found
   - Add complex game logic manually
   - Enhance error handling
   - Add logging

4. **Integration Testing**:
   ```bash
   # Start server
   python examples/tavern_game_server.py

   # In another terminal, start Electron
   cd tavern_display && npm start
   ```

---

## Advanced Features

### Parallel Tool Calling

OpenHands SDK supports parallel tool calling by default. When the LLM generates multiple tool calls, they execute in parallel, which can speed up code generation:

```python
# The SDK automatically handles parallel execution
# If agent needs to create multiple files, they can be created simultaneously
agent = Agent(llm=llm, tools=[...])
# Multiple file edits can happen in parallel
```

**Benefit**: Faster code generation when creating multiple files (e.g., all Electron app files at once).

### Image Content Support

If you want to show the agent screenshots of the UI for refinement:

```python
from openhands.sdk import ImageContent, Message, TextContent
import base64

# Capture screenshot of Electron app
with open("screenshot.png", "rb") as f:
    image_base64 = base64.b64encode(f.read()).decode("utf-8")

message = Message(
    role="user",
    content=[
        TextContent(text="Improve the UI based on this screenshot"),
        ImageContent(image_urls=[f"data:image/png;base64,{image_base64}"]),
    ],
)
```

**Use Case**: After initial generation, show agent the running app and ask for UI improvements.

### Custom Tools (Optional Enhancement)

For specialized game development needs, you could create custom tools:

**Example: D&D Character Validator Tool**
```python
from openhands.sdk import Action, Observation, ToolDefinition, ToolExecutor

class ValidateCharacterAction(Action):
    character_data: dict = Field(description="Character data to validate")

class ValidateCharacterObservation(Observation):
    valid: bool
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)

class ValidateCharacterExecutor(ToolExecutor[ValidateCharacterAction, ValidateCharacterObservation]):
    def __call__(self, action: ValidateCharacterAction, conversation=None):
        # Validate D&D 5e character stats
        # Check ability scores, modifiers, etc.
        return ValidateCharacterObservation(...)

class ValidateCharacterTool(ToolDefinition):
    # Register and use like built-in tools
    pass
```

**Potential Custom Tools for Game Development**:
- D&D Character Validator (validate stats, modifiers, etc.)
- Game State Checker (verify game state consistency)
- Scenario Generator (generate game scenarios)
- Test Case Generator (generate test cases from game rules)

**Note**: For initial development, built-in tools (FileEditorTool, TerminalTool) are sufficient. Custom tools are optional enhancements for specialized workflows.

---

## Cost Estimation

### Development Phase (One-Time)

**Per Task**:
- FastAPI server generation: ~2000-3000 tokens = $0.01-0.03
- Electron app generation: ~3000-4000 tokens = $0.015-0.04
- Test generation: ~2000-3000 tokens = $0.01-0.03
- Documentation: ~1500-2000 tokens = $0.008-0.02

**Total Development Cost**: ~$0.05-0.12 (one-time)

**Note**: Parallel tool calling can reduce costs by combining multiple operations into fewer LLM calls.

### Runtime (Not Applicable)

OpenHands is NOT used at runtime - only during development.

---

## Reasoning Traces (TRANSPARENCY & DEBUGGING!)

**OpenHands supports Reasoning Traces!** Access model reasoning traces from Anthropic extended thinking and OpenAI responses API for debugging and transparency!

### What Is Reasoning?

Reasoning provides access to **model reasoning traces** from Anthropic extended thinking and OpenAI responses API. This allows you to:

- ✅ **View internal reasoning**: See how the model thinks through problems
- ✅ **Debug decisions**: Understand why the agent made specific choices
- ✅ **Transparency**: Show users how the AI arrived at conclusions
- ✅ **Quality assurance**: Identify flawed reasoning patterns

### Two Provider Approaches

**1. Anthropic Extended Thinking**:
- `ThinkingBlock`: Full reasoning text from Claude's internal thought process
- `RedactedThinkingBlock`: Redacted or summarized thinking data

**2. OpenAI Reasoning via Responses API**:
- `reasoning_effort`: Control amount of reasoning (`"none"`, `"low"`, `"medium"`, `"high"`)
- Reasoning traces: Show how model approached the problem

### Enhanced Script with Reasoning

**File**: `scripts/generate_tavern_game_with_skills.py`

**New Features**:
- ✅ `--show-reasoning` flag to display reasoning traces
- ✅ `--reasoning-effort` flag for OpenAI models (none/low/medium/high)
- ✅ Automatic detection of Anthropic vs OpenAI
- ✅ Real-time reasoning display

**Usage**:
```bash
# Enable reasoning for Anthropic Claude
python scripts/generate_tavern_game_with_skills.py --show-reasoning

# Enable reasoning for OpenAI GPT
python scripts/generate_tavern_game_with_skills.py --show-reasoning --reasoning-effort high
```

**See**: `_work_efforts/OPENHANDS_REASONING_2026-01-14.md` for complete reasoning guide.

---

## Model Routing (AUTOMATIC COST OPTIMIZATION!)

**OpenHands supports Model Routing!** Automatically route agent's LLM requests to different models based on task characteristics to optimize cost and performance!

### What Is Model Routing?

Model Routing automatically routes agent's LLM requests to different models based on task characteristics to optimize cost and performance.

**Key Benefits**:
- ✅ **Cost Optimization**: Use cheaper models for simple tasks (67% savings possible)
- ✅ **Performance Optimization**: Use expensive models only when needed
- ✅ **Automatic Routing**: No manual model selection required
- ✅ **Multimodal Support**: Route multimodal requests to capable models

### MultimodalRouter (Built-in)

The `MultimodalRouter` routes requests based on content type:

- **Text-only requests** → Secondary (cheaper) LLM
- **Multimodal requests** (with images) → Primary (multimodal-capable) LLM

### Enhanced Script with Routing

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

**See**: `_work_efforts/OPENHANDS_MODEL_ROUTING_2026-01-14.md` for complete model routing guide.

---

## LLM Registry (CENTRALIZED LLM MANAGEMENT!)

**OpenHands supports LLM Registry!** Dynamically select and configure language models using the LLM registry for centralized management!

### What Is LLM Registry?

The LLM Registry provides a **centralized way to manage multiple LLM instances** in your application. Each LLM is identified by a unique `usage_id`, allowing you to:

- ✅ **Track costs separately** for each LLM (agent, condenser, sub-agents)
- ✅ **Retrieve LLMs dynamically** by usage_id
- ✅ **Manage multiple providers** and models
- ✅ **Switch between models** easily

### Basic Usage

**Create and Register LLMs**:
```python
from openhands.sdk import LLM, LLMRegistry

# Create LLM with unique usage_id
main_llm = LLM(usage_id="agent", model=model, api_key=api_key)

# Create registry and add LLM
llm_registry = LLMRegistry()
llm_registry.add(main_llm)

# Retrieve LLM by usage_id
llm = llm_registry.get("agent")
```

### Enhanced Script with Registry

**File**: `scripts/generate_tavern_game_with_skills.py`

**New Features**:
- ✅ LLM Registry for centralized management
- ✅ Separate LLMs for agent and condenser
- ✅ Automatic cost tracking per LLM
- ✅ Easy model switching

**Output**:
```
🤖 LLM Registry:
   Registered LLMs: agent, condenser
   (Use registry.get('usage_id') to retrieve specific LLMs)
```

**See**: `_work_efforts/OPENHANDS_LLM_REGISTRY_2026-01-14.md` for complete LLM Registry guide.

---

## Secret Registry (SECURE SECRET MANAGEMENT!)

**OpenHands supports secure secret management!** Provide environment variables and secrets to agent workspace securely with automatic masking!

### What Is Secret Registry?

The Secret Registry provides a **secure way to handle sensitive data** in your agent's workspace. It:

- ✅ **Automatically detects** secret references in bash commands
- ✅ **Injects secrets** as environment variables when needed
- ✅ **Masks secret values** in command outputs to prevent accidental exposure
- ✅ **Supports static strings** or **callable functions** for dynamic secrets

### Basic Usage

**Static Secrets**:
```python
conversation.update_secrets({
    "SECRET_TOKEN": "my-secret-token-value",
    "API_KEY": "sk-1234567890",
})
```

**Dynamic Secrets** (SecretSource):
```python
from openhands.sdk.secret import SecretSource

class MySecretSource(SecretSource):
    def get_value(self) -> str:
        return fetch_secret_from_vault("my-secret-key")

conversation.update_secrets({
    "DYNAMIC_SECRET": MySecretSource(),
})
```

### Enhanced Script with Secrets

**File**: `scripts/generate_tavern_game_with_skills.py`

**New Features**:
- ✅ `--secrets-file` flag to load secrets from JSON file
- ✅ Automatic detection of common environment variables
- ✅ Secret masking in command outputs
- ✅ Secure secret handling

**Usage**:
```bash
# Load secrets from JSON file
python scripts/generate_tavern_game_with_skills.py --secrets-file secrets.json

# Or use environment variables (automatically detected)
export GITHUB_TOKEN="ghp_1234567890"
python scripts/generate_tavern_game_with_skills.py
```

**See**: `_work_efforts/OPENHANDS_SECRET_REGISTRY_2026-01-14.md` for complete secret management guide.

---

## Observability & Tracing (REAL-TIME MONITORING!)

**OpenHands supports OpenTelemetry tracing!** Monitor and debug your agent's execution in real-time with Laminar, Honeycomb, or any OTLP-compatible backend!

### What Is Observability?

OpenHands SDK provides **built-in OpenTelemetry (OTEL) tracing support**, allowing you to monitor and debug your agent's execution in real-time.

**Key Benefits**:
- ✅ **Real-Time Monitoring**: See agent execution as it happens
- ✅ **Debugging**: Trace tool calls, LLM requests, and agent steps
- ✅ **Performance Analysis**: Identify bottlenecks and slow operations
- ✅ **Session Replay**: Browser automation replays (Laminar only)
- ✅ **Zero Code Changes**: Enabled via environment variables

### Supported Platforms

* **[Laminar](https://laminar.sh/)** - AI-focused observability with browser session replay
* **[Honeycomb](https://www.honeycomb.io/)** - High-performance distributed tracing
* **[Jaeger](https://www.jaegertracing.io/)** - Open-source distributed tracing
* **Any OTLP-compatible backend** - Datadog, New Relic, and more

### Quick Setup

**Laminar** (Recommended):
```bash
export LMNR_PROJECT_API_KEY="your-laminar-api-key"
```

**Honeycomb**:
```bash
export OTEL_EXPORTER_OTLP_TRACES_ENDPOINT="https://api.honeycomb.io:443/v1/traces"
export OTEL_EXPORTER_OTLP_TRACES_HEADERS="x-honeycomb-team=YOUR_API_KEY"
export OTEL_EXPORTER_OTLP_TRACES_PROTOCOL="http/protobuf"
```

**That's it!** Run your agent code normally and traces will be sent automatically.

### Enhanced Script with Observability

**File**: `scripts/generate_tavern_game_with_skills.py`

**New Features**:
- ✅ Automatic observability detection
- ✅ Displays observability status on startup
- ✅ Shows session ID (conversation UUID) for trace lookup
- ✅ No code changes needed - just environment variables

**Output**:
```
📊 Observability: Enabled (Laminar)
Session ID: abc123-def456-... (use this to find traces in your dashboard)
```

**See**: `_work_efforts/OPENHANDS_OBSERVABILITY_2026-01-14.md` for complete observability guide.

---

## Metrics Tracking (COST & PERFORMANCE MONITORING!)

**OpenHands supports comprehensive metrics tracking!** Monitor costs, token usage, and performance metrics for your agents!

### What Is Metrics Tracking?

OpenHands SDK provides metrics tracking at two levels:

1. **Individual LLM Metrics**: Track token usage, costs, and latencies per API call
2. **Conversation-Level Metrics**: Aggregate costs across all LLMs used in a conversation

**Key Benefits**:
- ✅ **Cost Visibility**: Track spending across all LLMs
- ✅ **Performance Monitoring**: Monitor response times and latency
- ✅ **Token Optimization**: Understand token usage patterns
- ✅ **Usage Breakdown**: See costs by usage_id (agent, condenser, sub-agents)

### Accessing Metrics

**Individual LLM Metrics**:
```python
conversation.run()
print(f"Agent cost: ${llm.metrics.accumulated_cost:.6f}")
```

**Conversation-Level Metrics**:
```python
combined_metrics = conversation.conversation_stats.get_combined_metrics()
print(f"Total cost: ${combined_metrics.accumulated_cost:.6f}")

# Breakdown by usage_id
for usage_id, metrics in conversation.conversation_stats.usage_to_metrics.items():
    print(f"{usage_id}: ${metrics.accumulated_cost:.6f}")
```

### Enhanced Script with Metrics

**File**: `scripts/generate_tavern_game_with_skills.py`

**New Features**:
- ✅ Automatic metrics display at end of execution
- ✅ Total cost tracking
- ✅ Token usage breakdown
- ✅ Cost breakdown by usage_id
- ✅ Performance metrics (latency, API calls)

**Output**:
```
📊 Metrics & Cost Tracking
💰 Total Cost: $0.123456
📝 Total Tokens: 58,023
📊 Cost Breakdown by Usage ID:
   - agent: $0.100000
   - condenser: $0.023456
⏱️  Performance:
   - Average latency: 2.34s
   - Total API calls: 15
```

**See**: `_work_efforts/OPENHANDS_METRICS_TRACKING_2026-01-14.md` for complete metrics guide.

---

## Sub-Agent Delegation (PARALLEL EXECUTION MODE!)

**OpenHands supports sub-agent delegation!** Enable parallel task execution by delegating work to multiple sub-agents!

### What Is Sub-Agent Delegation?

Sub-agent delegation enables **parallel task execution** by delegating work to multiple sub-agents that run independently and return consolidated results.

**Key Benefits**:
- ✅ **Parallel Processing**: Multiple tasks execute simultaneously
- ✅ **Specialized Agents**: Each sub-agent can have specialized skills
- ✅ **Improved Throughput**: Faster completion for parallelizable work
- ✅ **Separation of Concerns**: Different agents handle different aspects

### How It Works

**1. Spawning Sub-Agents**:
```python
# Agent spawns sub-agents with IDs
{
    "command": "spawn",
    "ids": ["server", "electron", "tests"]
}
```

**2. Delegating Tasks**:
```python
# Agent delegates tasks in parallel
{
    "command": "delegate",
    "tasks": {
        "server": "Create FastAPI server",
        "electron": "Create Electron app",
        "tests": "Write pytest tests"
    }
}
```

**Result**: All three tasks execute simultaneously!

### Performance Benefits

**Sequential** (without delegation): 15 minutes (5+5+5)
**Parallel** (with delegation): ~5 minutes (longest phase)
**Speedup**: 3x faster!

### Enhanced Script with Delegation

**File**: `scripts/generate_tavern_game_with_skills.py`

**New Features**:
- ✅ `--use-delegation` flag to enable sub-agent delegation
- ✅ `--max-sub-agents` flag to limit concurrent sub-agents (default: 3)
- ✅ Pre-configured specialized sub-agents:
  - `server_developer` (FastAPI expert)
  - `electron_developer` (Electron expert)
  - `test_developer` (Testing expert)

**Usage**:
```bash
# Enable delegation for parallel execution
python scripts/generate_tavern_game_with_skills.py --use-delegation

# Limit concurrent sub-agents
python scripts/generate_tavern_game_with_skills.py --use-delegation --max-sub-agents 2
```

**See**: `_work_efforts/OPENHANDS_SUB_AGENT_DELEGATION_2026-01-14.md` for complete delegation guide.

---

## Context Condenser (TOKEN EFFICIENCY MODE!)

**OpenHands supports context condensation!** Manage conversation history efficiently to save tokens and reduce costs!

### What Is a Context Condenser?

A context condenser manages agent memory by condensing conversation history to save tokens. As conversations grow longer:

- 💰 **Increased API Costs**: More tokens = higher costs
- ⏱️ **Slower Response Times**: Larger contexts take longer
- 📉 **Reduced Effectiveness**: LLMs become less effective with excessive information

**The Solution**: Intelligently summarize older parts of the conversation while preserving essential information.

### How It Works

**LLMSummarizingCondenser** (default):
- Keeps recent messages intact (immediate context)
- Preserves key information (goals, specs, files)
- Summarizes older content (LLM-generated summaries)
- Maintains continuity (agent retains awareness of past progress)

### Efficiency Gains

- ✅ **Up to 2x reduction** in per-turn API costs
- ✅ **Consistent response times** even in long sessions
- ✅ **Equivalent or better performance** on software engineering tasks

### Configuration

```python
from openhands.sdk.context.condenser import LLMSummarizingCondenser

condenser = LLMSummarizingCondenser(
    llm=llm.model_copy(update={"usage_id": "condenser"}),
    max_size=50,        # Trigger when history exceeds 50 events
    keep_first=3,      # Always keep first 3 events
)

agent = Agent(llm=llm, tools=tools, condenser=condenser)
```

### Enhanced Script with Condenser

**File**: `scripts/generate_tavern_game_with_skills.py`

**New Features**:
- ✅ Context condenser enabled by default
- ✅ `--condenser-max-size` flag (default: 50)
- ✅ `--condenser-keep-first` flag (default: 3)
- ✅ `--no-condenser` flag to disable

**Usage**:
```bash
# Default: Condenser enabled
python scripts/generate_tavern_game_with_skills.py

# Custom settings
python scripts/generate_tavern_game_with_skills.py --condenser-max-size 30

# Disable (not recommended for long conversations)
python scripts/generate_tavern_game_with_skills.py --no-condenser
```

**See**: `_work_efforts/OPENHANDS_CONTEXT_CONDENSER_2026-01-14.md` for complete condenser guide.

---

## Persistence (MULTI-SESSION MODE!)

**OpenHands supports persistence!** Save and restore conversation state for multi-session workflows!

### What Is Persistence?

Persistence allows you to:
- **Save conversation state** to disk
- **Restore state** in later sessions
- **Resume workflows** after interruption
- **Preserve context** across sessions

### How It Works

```python
import uuid

conversation_id = uuid.uuid4()
persistence_dir = "./.conversations"

conversation = Conversation(
    agent=agent,
    workspace=workspace_path,
    persistence_dir=persistence_dir,
    conversation_id=conversation_id,
)

# State automatically saved after each run()
conversation.send_message("Start task")
conversation.run()  # Saved to disk

# Later, restore:
conversation = Conversation(
    agent=agent,
    workspace=workspace_path,
    persistence_dir=persistence_dir,
    conversation_id=conversation_id,  # Same ID
)
# State automatically restored!
```

### What Gets Persisted

- ✅ Message history (complete event log)
- ✅ Agent configuration (LLM, tools, MCP, skills)
- ✅ Execution state (status, iteration count)
- ✅ Tool outputs (file edits, terminal output)
- ✅ Statistics (token counts, API calls, costs)
- ✅ Workspace context
- ✅ Activated skills

### Enhanced Script with Persistence

**File**: `scripts/generate_tavern_game_with_skills.py`

**New Features**:
- ✅ `--resume <conversation-id>` flag
- ✅ `--list` flag to list saved conversations
- ✅ `--persistence-dir` flag for custom directory
- ✅ Automatic state saving after each phase

**Usage**:
```bash
# Start new generation (with persistence)
python scripts/generate_tavern_game_with_skills.py

# List saved conversations
python scripts/generate_tavern_game_with_skills.py --list

# Resume from saved state
python scripts/generate_tavern_game_with_skills.py --resume <conversation-id>
```

**See**: `_work_efforts/OPENHANDS_PERSISTENCE_2026-01-14.md` for complete persistence guide.

---

## Skills Integration (CONTEXT-AWARE MODE!)

**OpenHands supports skills!** And we have `AGENTS.md` that can be auto-loaded!

### What Are Skills?

Skills provide specialized knowledge and context to agents:
- **Always-loaded**: Content always in system prompt (like AGENTS.md)
- **Keyword-triggered**: Content injected when keywords match
- **Progressive disclosure**: Agent reads on demand

### Our Project Skills

1. **AGENTS.md** (Auto-loaded)
   - Project coding standards (direct & minimal Python style)
   - Work efforts system
   - MCP server integration
   - Development workflows
   - Automatically loaded by `load_project_skills()`

2. **Game-Specific Skills** (Custom)
   - Game development context (always-loaded)
   - D&D 5e rules (keyword-triggered: "dnd", "5e", "ability", etc.)
   - Electron security (keyword-triggered: "electron", "security", etc.)
   - FastAPI patterns (keyword-triggered: "fastapi", "api", etc.)

### Enhanced Script with Skills

**File**: `scripts/generate_tavern_game_with_skills.py`

**Features**:
- ✅ Loads AGENTS.md automatically
- ✅ Game-specific skills (always-loaded + keyword-triggered)
- ✅ MCP integration (work-efforts, docs-maintainer, etc.)
- ✅ Built-in tools (TerminalTool, FileEditorTool, TaskTrackerTool)

**Usage**:
```bash
export LLM_API_KEY="your-key"
python scripts/generate_tavern_game_with_skills.py
```

**See**: `_work_efforts/OPENHANDS_SKILLS_INTEGRATION_2026-01-14.md` for complete skills guide.

---

## MCP Integration (POWER-UP MODE!)

**We have MCP servers configured!** OpenHands can use them!

### Our MCP Servers

1. **work-efforts**: Create/update work efforts (Johnny Decimal system)
2. **simple-tools**: Generate IDs, format dates
3. **docs-maintainer**: Create structured documentation
4. **filesystem**: File operations

### Enhanced Script with MCP

**File**: `scripts/generate_tavern_game_with_mcp.py`

**Features**:
- ✅ Creates work effort automatically (via MCP)
- ✅ Generates structured documentation (via MCP)
- ✅ Uses utility functions (via MCP)
- ✅ All code generation (via built-in tools)

**Usage**:
```bash
export LLM_API_KEY="your-key"
python scripts/generate_tavern_game_with_mcp.py
```

**See**: `_work_efforts/OPENHANDS_MCP_INTEGRATION_2026-01-14.md` for complete MCP integration guide.

---

## Next Steps

1. **Set up environment**:
   ```bash
   export LLM_API_KEY="your-key"
   export LLM_MODEL="anthropic/claude-sonnet-4-5-20250929"  # optional
   ```

2. **Install OpenHands**:
   ```bash
   pip install openhands-sdk openhands-tools
   ```

3. **Test setup** (recommended first):
   ```bash
   python scripts/test_openhands_setup.py
   ```
   This verifies OpenHands is working before generating code.

4. **Generate with MCP** (recommended - uses our MCP servers):
   ```bash
   python scripts/generate_tavern_game_with_mcp.py
   ```
   This creates work effort, generates code, and creates documentation automatically!

5. **Or generate without MCP** (simpler, no MCP features):
   ```bash
   python scripts/generate_tavern_server_openhands.py
   ```

6. **Review and refine**:
   - Review generated code
   - Check work effort in `_work_efforts/`
   - Check documentation in `_docs/` (if using MCP)
   - Test the server
   - Fix any issues
   - Add manual enhancements

7. **Test integration**:
   - Start server: `python examples/tavern_game_server.py`
   - Start Electron app: `cd tavern_display && npm install && npm start`
   - Play through game

---

## Troubleshooting

### Common Issues

1. **API Key Not Set**:
   ```bash
   export LLM_API_KEY="your-key"
   ```

2. **Model Not Found**:
   - Check model name matches your provider
   - For OpenHands Cloud, use `openhands/` prefix
   - For direct providers, use provider prefix (e.g., `anthropic/`)
   - For AWS Bedrock, use `bedrock/` prefix

3. **Import Errors**:
   ```bash
   pip install openhands-sdk openhands-tools
   # For AWS Bedrock:
   pip install openhands-sdk boto3
   ```

4. **Workspace Issues**:
   - Ensure script runs from project root
   - Check workspace path is correct

5. **AWS Bedrock Authentication**:
   - Use `AWS_BEARER_TOKEN_BEDROCK` for API key auth (recommended)
   - Or use `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` for credential auth
   - Set `AWS_REGION_NAME` if using credentials

6. **Vision/Image Support**:
   - Check if model supports vision: `llm.vision_is_active()`
   - Use `ImageContent` for image inputs
   - Disable vision with `disable_vision=True` to reduce costs

---

**Implementation Guide Complete**: 2026-01-14 20:22:22