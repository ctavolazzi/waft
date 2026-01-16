# OpenHands Skills Integration for Game Development

**Date**: 2026-01-14 20:22:22
**Context**: Using OpenHands Skills system to provide context and domain knowledge
**Status**: 🎯 CONTEXT-AWARE AGENT

---

## What Are Skills?

Skills add specialized behaviors, domain knowledge, and context-aware triggers to agents through structured prompts.

**Three Types**:
1. **Always-loaded**: Content always in system prompt (like AGENTS.md)
2. **Trigger-loaded**: Content injected when keywords match
3. **Progressive disclosure**: Agent reads on demand (AgentSkills standard)

---

## Our Project Skills

### 1. AGENTS.md (Auto-loaded)

**Location**: `AGENTS.md` at project root

**Content**: 
- Project overview
- Coding standards (direct & minimal Python style)
- Work efforts system
- MCP server integration
- Development workflows
- Security practices

**How It Works**: OpenHands automatically finds and loads `AGENTS.md` when using `load_project_skills()`.

**Benefit**: Agent automatically knows our coding standards, conventions, and project structure!

---

### 2. Game-Specific Skills (Custom)

We can create skills for game development:

#### Always-Loaded Skill: Game Development Context
```python
Skill(
    name="game-development-context",
    content="""
    You are developing an Electron desktop game application for a D&D 5e tavern scenario.
    
    Key Context:
    - Local-only game (no external services)
    - FastAPI server on 127.0.0.1:8765
    - Electron app displays game state in real-time
    - Follows security best practices
    - Uses existing codebase patterns
    """,
    trigger=None,  # Always loaded
)
```

#### Keyword-Triggered Skill: D&D 5e Rules
```python
Skill(
    name="dnd5e-rules",
    content="""
    D&D 5e Rules Reference:
    - Ability scores: 3-18 range
    - Modifiers: (score - 10) / 2, rounded down
    - AC: 10 + DEX modifier + armor bonus
    - Use DnD5eCharacter class from waft.core.dnd5e
    """,
    trigger=KeywordTrigger(keywords=["dnd", "d&d", "5e", "ability", "modifier", "roll", "dice"]),
)
```

**When Triggered**: When agent sees words like "dnd", "ability", "roll", etc., the D&D rules are automatically injected.

#### Keyword-Triggered Skill: Electron Security
```python
Skill(
    name="electron-security",
    content="""
    Electron Security Best Practices:
    - webSecurity: true
    - nodeIntegration: false
    - contextIsolation: true
    - Use contextBridge in preload.js
    """,
    trigger=KeywordTrigger(keywords=["electron", "security", "preload", "renderer"]),
)
```

**When Triggered**: When agent works on Electron code, security best practices are automatically available.

#### Keyword-Triggered Skill: FastAPI Patterns
```python
Skill(
    name="fastapi-patterns",
    content="""
    FastAPI Patterns from this codebase:
    - Use async endpoints with asyncio.Lock()
    - Follow patterns from src/waft/api/main.py
    - Use Pydantic models for validation
    """,
    trigger=KeywordTrigger(keywords=["fastapi", "endpoint", "api", "server", "async"]),
)
```

**When Triggered**: When agent works on FastAPI code, existing patterns are automatically available.

---

## Skills Loading

### Automatic Project Skills

```python
from openhands.sdk.context.skills import load_project_skills

# Automatically finds AGENTS.md, CLAUDE.md, GEMINI.md at workspace root
project_skills = load_project_skills(workspace_dir="/path/to/repo")
```

**What Gets Loaded**:
- `AGENTS.md` - Always-loaded (repo skill)
- `CLAUDE.md` - If exists
- `GEMINI.md` - If exists

### Custom Skills

```python
from openhands.sdk.context import Skill, KeywordTrigger

custom_skills = [
    Skill(
        name="my-skill",
        content="Instructions...",
        trigger=None,  # Always loaded
    ),
    Skill(
        name="triggered-skill",
        content="Instructions...",
        trigger=KeywordTrigger(keywords=["keyword1", "keyword2"]),
    ),
]
```

### Combine Both

```python
project_skills = load_project_skills(workspace_dir=workspace_path)
all_skills = list(project_skills) + custom_skills

agent_context = AgentContext(skills=all_skills)
```

---

## AgentContext Configuration

```python
from openhands.sdk import AgentContext

agent_context = AgentContext(
    skills=all_skills,  # Project skills + custom skills
    
    # Optional: Load public skills from OpenHands registry
    load_public_skills=False,  # Set True to load community skills
    
    # Optional: Add system message suffix
    system_message_suffix="""
<PROJECT_CONTEXT>
Project: WAFT
Repository: waft
Current Task: Electron Tavern Game Display
</PROJECT_CONTEXT>
    """.strip(),
    
    # Optional: Add user message suffix
    user_message_suffix="Remember to follow coding standards from AGENTS.md.",
)
```

---

## Skills in Action

### Example: Agent Generates FastAPI Code

**What Happens**:
1. Agent sees task: "Create FastAPI server"
2. **FastAPI patterns skill triggers** (keyword: "fastapi")
3. Skill content injected: "Use async endpoints with asyncio.Lock()..."
4. Agent uses this knowledge in code generation
5. **AGENTS.md always loaded**: Agent follows direct & minimal Python style

**Result**: Code follows both FastAPI patterns AND project coding standards!

---

### Example: Agent Generates Electron Code

**What Happens**:
1. Agent sees task: "Create Electron app"
2. **Electron security skill triggers** (keyword: "electron")
3. Skill content injected: "webSecurity: true, nodeIntegration: false..."
4. Agent uses security best practices
5. **AGENTS.md always loaded**: Agent follows project conventions

**Result**: Secure Electron code that follows project standards!

---

### Example: Agent Works with D&D Rules

**What Happens**:
1. Agent sees: "Calculate ability modifier"
2. **D&D 5e rules skill triggers** (keyword: "modifier")
3. Skill content injected: "Modifiers: (score - 10) / 2, rounded down"
4. Agent uses correct D&D 5e formula
5. **AGENTS.md always loaded**: Agent follows code style

**Result**: Correct D&D 5e implementation with proper code style!

---

## Complete Capability Stack

### Layer 1: Built-in Tools
- TerminalTool
- FileEditorTool
- TaskTrackerTool

### Layer 2: MCP Servers
- work-efforts (create work efforts)
- docs-maintainer (create documentation)
- simple-tools (utilities)
- filesystem (file operations)

### Layer 3: Skills
- AGENTS.md (project standards - always loaded)
- game-development-context (always loaded)
- dnd5e-rules (keyword-triggered)
- electron-security (keyword-triggered)
- fastapi-patterns (keyword-triggered)

**Total Power**: 3 tools + 4 MCP servers + 5+ skills = **Highly capable, context-aware agent!**

---

## Benefits

### 1. Automatic Context Loading
- Agent knows project standards automatically
- No need to explain conventions in every task
- Consistent code style across generation

### 2. Domain Knowledge on Demand
- D&D rules available when needed
- Electron security when working on Electron
- FastAPI patterns when creating API

### 3. Progressive Disclosure
- Agent can read full skill content on demand
- Skills can reference their own scripts/resources
- Large reference docs don't bloat prompts

### 4. Keyword Triggers
- Skills activate automatically
- No manual skill selection needed
- Context-aware behavior

---

## Creating Skills for Game Development

### Option 1: Inline Skills (Code-defined)

```python
game_skills = [
    Skill(
        name="dnd5e-rules",
        content="D&D 5e rules...",
        trigger=KeywordTrigger(keywords=["dnd", "5e"]),
    ),
]
```

**Pros**: Quick to create, no files needed
**Cons**: Harder to maintain, not reusable

---

### Option 2: SKILL.md Files (AgentSkills Standard)

Create `skills/dnd5e-rules/SKILL.md`:

```yaml
---
name: dnd5e-rules
description: D&D 5e rules reference for game development
triggers:
  - dnd
  - d&d
  - 5e
  - ability
  - modifier
  - roll
  - dice
---

# D&D 5e Rules Reference

[Full content here...]
```

Then load:
```python
from openhands.sdk.context.skills import load_skills_from_dir

_, _, agent_skills = load_skills_from_dir("skills/")
```

**Pros**: Reusable, maintainable, follows standard
**Cons**: Requires file structure

---

## Enhanced Generation Script

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

---

## Skills vs. Tools vs. MCP

| Feature | Skills | Tools | MCP |
|---------|--------|-------|-----|
| **Purpose** | Knowledge/Context | Actions | External Services |
| **When Active** | Always or keyword-triggered | On-demand | On-demand |
| **What They Do** | Provide instructions | Execute operations | Provide capabilities |
| **Example** | "Use asyncio.Lock()" | Edit file | Create work effort |

**Together**: Skills provide knowledge, Tools execute actions, MCP connects to services.

---

## Public Skills Registry

OpenHands maintains a public skills repository:
- https://github.com/OpenHands/skills

**Enable**:
```python
agent_context = AgentContext(
    load_public_skills=True,  # Auto-load community skills
)
```

**Available Skills**: GitHub integration, Python development, debugging, and more.

**For Game Development**: Our custom skills are more relevant, but public skills can be useful too.

---

## Next Steps

1. **Test Skills Integration**:
   ```bash
   python scripts/generate_tavern_game_with_skills.py
   ```

2. **Verify Skills Loaded**:
   - Check agent output for skill activation
   - Verify AGENTS.md context is used
   - Check keyword triggers work

3. **Create Additional Skills** (optional):
   - Create `skills/` directory
   - Add SKILL.md files for reusable knowledge
   - Load with `load_skills_from_dir()`

---

## Conclusion

**Skills make the agent context-aware!**

The agent now has:
- ✅ Project standards (AGENTS.md - always loaded)
- ✅ Game-specific knowledge (custom skills)
- ✅ Domain expertise (D&D, Electron, FastAPI)
- ✅ Automatic activation (keyword triggers)
- ✅ Progressive disclosure (read on demand)

**This is the most powerful configuration!**

---

**Skills Integration Guide Complete**: 2026-01-14 20:22:22