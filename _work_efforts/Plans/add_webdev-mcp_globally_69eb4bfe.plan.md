---
name: Add webdev-mcp globally
overview: Add the webdev-mcp server to your global Cursor MCP configuration to enable screenshot and screen listing tools across all projects.
todos:
  - id: add-webdev-mcp
    content: Add webdev MCP server entry to ~/.cursor/mcp.json
    status: completed
---

# Add webdev-mcp MCP Server Globally

## What This Does

The `webdev-mcp` server provides two tools:

- `takeScreenshot` - Takes a screenshot and returns it as base64
- `listScreens` - Lists available screens for screenshot targeting

## Change Required

Edit [`~/.cursor/mcp.json`](/Users/ctavolazzi/.cursor/mcp.json) to add this entry to `mcpServers`:

```json
"webdev": {
  "command": "npx",
  "args": ["webdev-mcp"]
}
```



## Post-Installation

1. Restart Cursor IDE (or reload the window) for the new MCP server to be recognized
2. On macOS, you may need to grant Cursor screen recording permissions in System Preferences > Privacy & Security > Screen Recording

## Notes

- The server runs via `npx`, so it will auto-install on first use