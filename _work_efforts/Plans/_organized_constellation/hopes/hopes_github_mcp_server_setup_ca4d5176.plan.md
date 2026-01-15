---
name: GitHub MCP Server Setup
overview: Add the Remote GitHub MCP Server (OAuth) to your existing Cursor MCP configuration, enabling AI tools to interact directly with GitHub repositories, issues, PRs, and more.
todos:
  - id: add-github-mcp
    content: Add GitHub MCP server entry to ~/.cursor/mcp.json
    status: completed
  - id: restart-cursor
    content: Restart Cursor to load new MCP configuration
    status: in_progress
  - id: verify-auth
    content: Verify OAuth authentication works when using GitHub tools
    status: pending

category: hopes
confidence: 0.42
constellation_date: 2026-01-14
---

# GitHub MCP Server Setup (Remote OAuth)

## Current State

Your user-level MCP config at `~/.cursor/mcp.json` has 5 servers configured. We will add the GitHub remote server as the 6th.

## Configuration Change

Add the following entry to your `~/.cursor/mcp.json` inside the `mcpServers` object:

```json
"github": {
  "type": "http",
  "url": "https://api.githubcopilot.com/mcp/"
}
```



## Final Configuration Preview

```json
{
  "mcpServers": {
    "memory": { ... },
    "filesystem": { ... },
    "work-efforts": { ... },
    "simple-tools": { ... },
    "docs-maintainer": { ... },
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    }
  }
}
```



## Post-Setup

1. **Restart Cursor** - Required for MCP config changes to take effect
2. **Authenticate** - When you first use the GitHub MCP tools, you'll be prompted to authenticate via OAuth in your browser
3. **Verify** - In Agent mode, the GitHub tools will be available (repos, issues, pull_requests, actions, etc.)

## Available Capabilities

Once configured, you'll have access to:

- Repository browsing and code search
- Issue and PR management
- GitHub Actions workflow monitoring
- Code security analysis (Dependabot, Code Scanning)
- Notifications and discussions
- And more

## Notes

- Remote OAuth is the simplest option - no PAT management needed
- GitHub hosts the server, so no local Docker or binary required
- Requires Cursor to support remote MCP servers (HTTP type)