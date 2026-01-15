---
name: MCP Cortex Architecture Evolution
overview: Optimize and evolve your MCP server configuration toward a complete AI cortex architecture by removing redundant servers, adding critical planning capabilities, and establishing a roadmap for semantic memory.
todos:
  - id: remove-webdev
    content: Remove webdev server from ~/.cursor/mcp.json (lines 60-65)
    status: completed
  - id: add-sequential
    content: Add sequential-thinking server to ~/.cursor/mcp.json
    status: completed
  - id: restart-cursor
    content: Restart Cursor IDE to load updated configuration
    status: completed
  - id: test-sequential
    content: Test sequential-thinking with a multi-step reasoning task
    status: completed
  - id: verify-playwright
    content: Verify Playwright MCP still works after config changes
    status: completed
  - id: update-agents-md
    content: Update AGENTS.md to document the new cortex architecture
    status: completed

category: dreams
confidence: 0.47
constellation_date: 2026-01-14
---

# MCP Cortex Architecture Evolution Plan

## Current State Analysis

Your current 11 MCP servers mapped to the 4-module cortex framework:**Working Memory (Strong)**

- `work-efforts` - Johnny Decimal task tracking
- `docs-maintainer` - Documentation management
- `memory` - Knowledge graph persistence

**Tool Layer (Complete)**

- `filesystem` - File operations
- `Playwright` - Browser automation (newly added)
- `browser-tools` - Lighthouse audits
- `pixellab` - Pixel art generation
- `nano-banana` - Gemini image generation
- `simple-tools` - Utilities
- `github` - GitHub API

**Redundant**

- `webdev` - Replaced by Playwright

**Missing**

- Hierarchical Planning Module
- Autonomous Compaction/Virtual Memory

---

## Phase 1: Immediate Cleanup

**Action:** Remove `webdev` from [`~/.cursor/mcp.json`](~/.cursor/mcp.json)Remove this block (lines 60-65):

```json
"webdev": {
  "command": "npx",
  "args": [
    "webdev-mcp"
  ]
},
```

**Result:** 10 servers (down from 11)---

## Phase 2: Add Planning Capability

**Action:** Add Sequential Thinking MCP serverThis fills the critical "Hierarchical Planning Module" gap identified in the cortex architecture. It enables:

- Step-by-step reasoning for complex tasks
- Plan decomposition and revision
- Visible, auditable thought processes

Add to [`~/.cursor/mcp.json`](~/.cursor/mcp.json):

```json
"sequential-thinking": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
}
```

**Result:** Still 10 servers (net zero change from removing webdev)---

## Phase 3: Future Enhancements (Optional Roadmap)

### 3a. Memory Keeper for Context Preservation

When you encounter context loss in long sessions:

```json
"memory-keeper": {
  "command": "npx", 
  "args": ["-y", "mcp-memory-keeper"]
}
```



### 3b. Vector Storage for Semantic Search

When you need conceptual retrieval across your knowledge base:

```json
"chroma": {
  "command": "npx",
  "args": ["-y", "chromadb-mcp-server"]
}
```



### 3c. Consolidation Opportunity

If you rarely use creative tools, consider disabling `pixellab` and `nano-banana` temporarily to make room for cortex infrastructure.---

## Final Configuration (After Phase 2)

```javascript
~/.cursor/mcp.json - 10 servers

Core Infrastructure (5):
    - memory              # Knowledge graph
    - filesystem          # File operations  
    - work-efforts        # Task tracking
    - docs-maintainer     # Documentation
    - sequential-thinking # Planning (NEW)

Automation (2):
    - Playwright          # Browser automation
    - browser-tools       # Lighthouse audits

Creative (2):
    - pixellab            # Pixel art
    - nano-banana         # Image generation

Utilities (1):
    - simple-tools        # Date/ID utilities
    - github              # GitHub API
```

---

## Cortex Architecture Mapping (Post-Implementation)

| Cortex Module | Implementation | Status ||---------------|----------------|--------|| Structured Working Memory | work-efforts, docs-maintainer, memory | Complete || Persistent Semantic Repository | memory (+ future ChromaDB) | Partial || Hierarchical Planning | sequential-thinking | Complete || Autonomous Compaction | (future memory-keeper) | Pending |---

## Verification Steps

After editing `mcp.json`: