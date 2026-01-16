# OpenHands + MCP Integration for Game Development

**Date**: 2026-01-14 20:22:22
**Context**: Integrating OpenHands SDK with our existing MCP servers
**Status**: 🚀 POWER-UP MODE

---

## The Game Changer: MCP Integration

**OpenHands SDK supports MCP (Model Context Protocol)** - and we already have MCP servers configured!

This means the agent can use:
- ✅ Our custom work-efforts MCP server
- ✅ Our custom simple-tools MCP server
- ✅ Our custom docs-maintainer MCP server
- ✅ Filesystem MCP server
- ✅ Plus all built-in OpenHands tools

---

## Our MCP Servers

### 1. Work Efforts MCP Server
**Location**: `/Users/ctavolazzi/Code/.mcp-servers/work-efforts/server.js`

**Tools Available**:
- `create_work_effort` - Create work effort with Johnny Decimal ID
- `list_work_efforts` - List all work efforts
- `update_work_effort` - Update work effort status/content
- `search_work_efforts` - Search work efforts
- `create_ticket` - Create ticket within work effort
- And more...

**Use Case**: Agent can automatically create work effort for game development!

---

### 2. Simple Tools MCP Server
**Location**: `/Users/ctavolazzi/Code/.mcp-servers/simple-tools/server.js`

**Tools Available**:
- `generate_random_name` - Generate random names (e.g., "HappyPanda123")
- `generate_unique_id` - Create unique IDs with timestamps
- `format_date` - Format dates (ISO, human, filename, devlog)

**Use Case**: Agent can generate IDs, format dates for filenames, etc.

---

### 3. Docs Maintainer MCP Server
**Location**: `/Users/ctavolazzi/Code/.mcp-servers/docs-maintainer/server.py`

**Tools Available**:
- `initialize_docs` - Initialize _docs folder structure
- `create_doc` - Create documentation with auto-numbering
- `update_doc` - Update documentation
- `rebuild_indices` - Rebuild index files
- `link_work_effort` - Link docs to work efforts
- `search_docs` - Search documentation
- `check_health` - Check documentation health

**Use Case**: Agent can create structured documentation automatically!

---

### 4. Filesystem MCP Server
**Location**: npx-based (`@modelcontextprotocol/server-filesystem`)

**Tools Available**:
- File read/write operations
- Directory operations
- File search

**Use Case**: Agent can use filesystem operations via MCP.

---

## MCP Configuration for OpenHands

```python
mcp_config = {
    "mcpServers": {
        # Filesystem MCP (npx-based)
        "filesystem": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", workspace_path]
        },
        # Work Efforts MCP (our custom server)
        "work-efforts": {
            "command": "node",
            "args": ["/Users/ctavolazzi/Code/.mcp-servers/work-efforts/server.js"]
        },
        # Simple Tools MCP (our custom server)
        "simple-tools": {
            "command": "node",
            "args": ["/Users/ctavolazzi/Code/.mcp-servers/simple-tools/server.js"]
        },
        # Docs Maintainer MCP (our custom server - Python/FastMCP)
        "docs-maintainer": {
            "command": "python",
            "args": ["/Users/ctavolazzi/Code/.mcp-servers/docs-maintainer/server.py"]
        },
    }
}

agent = Agent(
    llm=llm,
    tools=[...],  # Built-in tools
    mcp_config=mcp_config,  # Add MCP servers!
)
```

---

## Enhanced Workflow with MCP

### Phase 0: Create Work Effort (NEW!)

```python
task = """
Use the work-efforts MCP server to create a work effort for this game development project.

Use work-efforts:create_work_effort with:
- repo_path: "/Users/ctavolazzi/Code/active/waft"
- title: "Electron Tavern Game Display Development"
- description: "Develop Electron desktop app for D&D tavern scenario game"
- status: "active"
"""
```

**Result**: Agent automatically creates work effort in `_work_efforts/` following Johnny Decimal system!

---

### Phase 1-3: Generate Code (Same as Before)

- FastAPI server
- Electron app
- Tests

---

### Phase 4: Generate Documentation (ENHANCED!)

```python
task = """
Generate documentation using the docs-maintainer MCP server:

1. Use docs-maintainer:create_doc to create structured documentation:
   - area: "20-29" (development)
   - category: "20" (architecture)
   - title: "Electron Tavern Game Display Architecture"
   - content: Document architecture, API, game state

2. Use FileEditorTool for README files
"""
```

**Result**: Agent creates documentation in `_docs/` with proper Johnny Decimal structure!

---

## Tool Filtering (Optional)

You can filter which MCP tools are available:

```python
agent = Agent(
    llm=llm,
    tools=[...],
    mcp_config=mcp_config,
    filter_tools_regex="^(?!repomix)(.*)",  # Exclude repomix tools
)
```

**For game development**: No filtering needed - all our MCP tools are useful!

---

## Complete Tool Set

### Built-in OpenHands Tools:
- TerminalTool
- FileEditorTool
- TaskTrackerTool

### MCP Tools (Our Custom Servers):
- work-efforts:create_work_effort
- work-efforts:list_work_efforts
- work-efforts:update_work_effort
- work-efforts:search_work_efforts
- simple-tools:generate_random_name
- simple-tools:generate_unique_id
- simple-tools:format_date
- docs-maintainer:create_doc
- docs-maintainer:update_doc
- docs-maintainer:search_docs
- filesystem:read_file
- filesystem:write_file
- And more...

**Total**: 3 built-in + ~20+ MCP tools = **Powerful agent!**

---

## Benefits of MCP Integration

### 1. Automatic Work Effort Creation
- Agent creates work effort automatically
- Follows Johnny Decimal system
- Tracks progress

### 2. Structured Documentation
- Agent creates docs in `_docs/` folder
- Auto-numbering (20.01, 20.02, etc.)
- Proper index management

### 3. Utility Functions
- Generate IDs for files
- Format dates consistently
- Random name generation

### 4. File Operations
- Filesystem MCP for file operations
- Can complement FileEditorTool

---

## Enhanced Generation Script

**File**: `scripts/generate_tavern_game_with_mcp.py`

**Features**:
- Phase 0: Create work effort via MCP
- Phase 1-3: Generate code (same as before)
- Phase 4: Generate documentation via docs-maintainer MCP
- Uses all our MCP servers

**Usage**:
```bash
export LLM_API_KEY="your-key"
python scripts/generate_tavern_game_with_mcp.py
```

---

## Comparison

### Without MCP:
- Agent generates code
- Manual work effort creation
- Manual documentation
- Manual ID generation

### With MCP:
- Agent generates code
- ✅ **Automatic work effort creation**
- ✅ **Automatic structured documentation**
- ✅ **Automatic ID/date formatting**
- ✅ **Integrated with project systems**

---

## MCP Server Paths

**Work Efforts**: `/Users/ctavolazzi/Code/.mcp-servers/work-efforts/server.js`
**Simple Tools**: `/Users/ctavolazzi/Code/.mcp-servers/simple-tools/server.js`
**Docs Maintainer**: `/Users/ctavolazzi/Code/.mcp-servers/docs-maintainer/server.py`
**Filesystem**: npx-based (no path needed)

**Note**: These are user-level MCP servers, not project-level.

---

## OAuth MCP Servers (Future)

If you add OAuth-enabled MCP servers (like Notion):

```python
mcp_config = {
    "mcpServers": {
        "Notion": {
            "url": "https://mcp.notion.com/mcp",
            "auth": "oauth"
        }
    }
}
```

OpenHands will handle OAuth flow automatically!

---

## Security Considerations

### Tool Filtering
- Use `filter_tools_regex` to limit available tools
- Prevents agent from using unwanted tools

### MCP Server Security
- Our MCP servers are local (no network access)
- Filesystem MCP is scoped to workspace
- All servers are trusted (we control them)

---

## Next Steps

1. **Test MCP Integration**:
   ```bash
   python scripts/generate_tavern_game_with_mcp.py
   ```

2. **Verify Work Effort Created**:
   - Check `_work_efforts/` for new work effort
   - Should follow Johnny Decimal system

3. **Verify Documentation Created**:
   - Check `_docs/` for new documentation
   - Should be properly indexed

4. **Review Generated Code**:
   - All code should be generated
   - Work effort and docs should be created automatically

---

## Conclusion

**MCP Integration is a Game Changer!**

The agent can now:
- ✅ Create work efforts automatically
- ✅ Generate structured documentation
- ✅ Use utility functions (IDs, dates)
- ✅ Integrate with our project systems
- ✅ Follow our conventions (Johnny Decimal, etc.)

**This makes the agent much more powerful and integrated with our workflow!**

---

**MCP Integration Guide Complete**: 2026-01-14 20:22:22