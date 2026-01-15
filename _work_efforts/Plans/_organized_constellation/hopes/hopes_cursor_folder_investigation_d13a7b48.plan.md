---
name: Cursor Folder Investigation
overview: Explore the global ~/.cursor folder structure to understand Cursor's internal capabilities, configuration options, and data tracking features for improved workflow optimization.
todos:
  - id: query-ai-tracking
    content: Query AI tracking database for code generation insights and patterns
    status: completed
  - id: review-plans
    content: Review 21 saved plans for reusable templates and best practices
    status: completed
  - id: configure-mcp
    content: Set up useful MCP servers in global mcp.json
    status: cancelled
  - id: review-transcripts
    content: Review agent transcripts for insights and cleanup
    status: completed
  - id: document-findings
    content: Create a reference guide documenting Cursor folder structure and configuration
    status: completed

category: hopes
confidence: 0.50
constellation_date: 2026-01-14
---

# Cursor Folder Investigation Plan

## Discovery Summary

The global `~/.cursor` folder contains configuration, state, and tracking data that Cursor uses. Here's what was found:

### Folder Structure Overview

```
~/.cursor/
├── ai-tracking/           # AI code generation tracking
│   └── ai-code-tracking.db  # SQLite: 9,040 code hashes tracked
├── argv.json              # VS Code CLI args (crash reporter, hardware accel)
├── browser-logs/          # Accessibility snapshots from browser tool
├── cli-config.json        # Cursor CLI settings
├── extensions/            # VS Code extensions (10,937 files)
├── ide_state.json         # Recently viewed files, state
├── mcp.json               # Global MCP server config (currently empty)
├── plans/                 # 21 plan files from CreatePlan tool
├── projects/              # Per-project configurations
│   └── Users-ctavolazzi-Code-howtowincapitalism/
│       ├── agent-tools/       # Cached tool outputs
│       ├── agent-transcripts/ # Full conversation logs (JSON + TXT)
│       ├── assets/            # Pasted images
│       └── terminals/         # Terminal state files
└── worktrees/             # Git worktree support (empty)
```

---

## Key Findings and Capabilities

### 1. AI Code Tracking (`ai-tracking/ai-code-tracking.db`)

**What it does:** Tracks all AI-generated code with hashes, timestamps, and metadata.

**Database schema:**
```sql
ai_code_hashes (hash, source, fileExtension, fileName, 
                requestId, conversationId, timestamp, createdAt)
scored_commits (commitHash, branchName, scoredAt)
tracking_state (key, value)
```

**Current stats:** 9,040 code hashes, all from "composer" source.

**Potential uses:**
- Audit what code was AI-generated vs human-written
- Track AI contribution over time
- Understand which file types get most AI assistance

### 2. CLI Configuration (`cli-config.json`)

**Current settings:**
```json
{
  "editor": { "vimMode": false },
  "permissions": { "allow": ["Shell(ls)"], "deny": [] },
  "approvalMode": "allowlist",
  "sandbox": { "mode": "disabled" }
}
```

**Configurable options:**
- `vimMode` - Enable Vim keybindings
- `permissions` - Tool execution allowlist/denylist
- `approvalMode` - Control how tool calls are approved
- `sandbox.mode` - Sandboxing for AI operations

### 3. Plans Directory (`plans/`)

**21 saved plans** including auth audits, security remediations, architecture reviews.

**Plan format:**
```yaml
---
name: Plan Name
overview: "Brief description"
todos:
  - id: task-id
    content: Task description
    status: pending|in_progress|completed
---
# Markdown content with detailed plan
```

**Capability:** The `CreatePlan` tool saves plans here for reference across sessions.

### 4. Agent Transcripts (`projects/.../agent-transcripts/`)

**Full conversation logs** including:
- User messages with context
- AI thinking/reasoning (when available)
- Tool calls and results
- Complete interaction history

**Format:** JSON array of role/text objects.

### 5. Browser Logs (`browser-logs/`)

**Accessibility snapshots** from the browser tool - captures page structure for web automation tasks.

### 6. MCP Configuration (`mcp.json`)

**Global MCP server config** - currently empty (`{ "mcpServers": {} }`).

**Note:** Your project-level MCP config at `/Users/ctavolazzi/Code/.cursor/mcp.json` may have servers configured.

---

## Investigation Actions

### Immediate Opportunities

| Action | Benefit | Complexity |
|--------|---------|------------|
| Query AI tracking DB for insights | See AI contribution patterns | Low |
| Review saved plans for reusable templates | Leverage past planning work | Low |
| Configure MCP servers globally | Enable tools across all projects | Medium |
| Review/clean agent transcripts | Understand past sessions, free space | Low |

### Configuration Improvements

1. **Customize `cli-config.json`**
   - Add frequently used Shell commands to permissions allowlist
   - Consider enabling sandbox mode for safer operations

2. **Set up global MCP servers**
   - Add useful MCP servers to `~/.cursor/mcp.json`
   - Servers available globally vs per-project

3. **Review extensions**
   - The `extensions/` folder has 10,937 files
   - Audit for unused extensions to improve performance

---

## Recommended Next Steps

1. **Query AI tracking database** - Analyze which files/types get most AI assistance
2. **Review past plans** - Extract reusable templates and patterns
3. **Configure global MCP** - Set up servers you want available everywhere
4. **Clean up transcripts** - Review if any sensitive data, archive or delete old ones
5. **Document findings** - Create a reference guide for your Cursor setup