---
name: Fix GitHub MCP Config
overview: Update the GitHub MCP server configuration to use the correct Streamable HTTP format with PAT authentication, replacing the non-functional OAuth-only config.
todos:
  - id: update-config
    content: Update ~/.cursor/mcp.json with correct PAT-based config
    status: completed
  - id: insert-pat
    content: Replace YOUR_GITHUB_PAT placeholder with actual token
    status: completed
  - id: restart-verify
    content: Restart Cursor and verify green dot in MCP settings
    status: completed

category: dreads
confidence: 0.60
constellation_date: 2026-01-14
---

# Fix GitHub MCP Server

Configuration

## Problem

The current config uses OAuth-only format which Cursor doesn't support for GitHub MCP. It needs PAT authentication.

## Current (broken) config in `~/.cursor/mcp.json`:

```json
"github": {
  "type": "http",
  "url": "https://api.githubcopilot.com/mcp/"
}
```



## Required (working) config:

```json
"github": {
  "url": "https://api.githubcopilot.com/mcp/",
  "headers": {
    "Authorization": "Bearer YOUR_GITHUB_PAT"
  }
}
```

Note: The `type` field is removed (not needed), and `headers` with Authorization is added.

## Steps

1. Update `~/.cursor/mcp.json` with the correct format
2. You will need to replace `YOUR_GITHUB_PAT` with your actual token after I write the file (or provide it now)
3. Restart Cursor
4. Verify green dot in MCP settings

## Token Requirements

Your PAT should have scopes for the features you want to use:

- `repo` - Repository access