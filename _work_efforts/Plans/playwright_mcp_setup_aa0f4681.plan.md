---
name: Playwright MCP Setup
overview: Install the Playwright MCP server to replace/supplement existing browser automation MCP servers, providing faster, more reliable browser automation using accessibility snapshots instead of screenshots.
todos: []
---

# Playwright MCP Server Installation Plan

## Why Playwright MCP?

Current `browser-tools` MCP server limitations:

- Requires separate middleware server (`npx @agentdeskai/browser-tools-server@1.2.1`)
- Requires Chrome extension installation
- Only one DevTools panel can be open at a time
- Screenshot-based (slower, less deterministic)

Playwright MCP advantages:

- Single `npx` command (no middleware, no extension)
- Uses accessibility tree (fast, deterministic)
- Persistent sessions or isolated mode
- Extensive configuration options
- Microsoft-maintained

## Installation Steps

### Step 1: Add to MCP Configuration

Edit [`~/.cursor/mcp.json`](~/.cursor/mcp.json) to add the Playwright MCP server:

```json
"playwright": {

```