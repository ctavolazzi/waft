---
name: Playwright MCP Setup
overview: Install the Playwright MCP server to replace/supplement existing browser automation MCP servers, providing faster, more reliable browser automation using accessibility snapshots instead of screenshots.
todos:
  - id: add-config
    content: Add Playwright MCP server to ~/.cursor/mcp.json
    status: pending
  - id: restart-cursor
    content: Restart Cursor to load the new MCP server
    status: pending
  - id: test-navigate
    content: Test browser_navigate to example.com
    status: pending
  - id: test-snapshot
    content: Test browser_snapshot to get accessibility tree
    status: pending
  - id: test-interact
    content: Test browser_click and browser_type interactions
    status: pending
  - id: document-results
    content: Document test results and any issues found
    status: pending

category: hopes
confidence: 0.60
constellation_date: 2026-01-14
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
  "command": "npx",
  "args": [
    "@playwright/mcp@latest"
  ]
}
```



### Step 2: Restart Cursor

After adding the configuration, restart Cursor to load the new MCP server.

### Step 3: Verify Installation

Test that the server is available by using one of its tools:

- `browser_navigate` - Navigate to a URL
- `browser_snapshot` - Capture accessibility snapshot
- `browser_click` - Click on elements

## Testing Plan

### Test 1: Basic Navigation

Navigate to a simple website (e.g., `https://example.com`) and verify the browser opens.

### Test 2: Accessibility Snapshot

Take an accessibility snapshot and verify structured data is returned (not a screenshot).

### Test 3: Element Interaction

Click on a link or button using the `ref` from the snapshot.

### Test 4: Form Input

Navigate to a form and test typing into input fields.

### Test 5: Multi-step Workflow

Complete a multi-step task (e.g., search on a website, click result).

## Optional Configuration Variants

### Headless Mode (for CI/background)

```json
"playwright": {
  "command": "npx",
  "args": ["@playwright/mcp@latest", "--headless"]
}
```



### With Trace Recording (debugging)

```json
"playwright": {
  "command": "npx",
  "args": ["@playwright/mcp@latest", "--save-trace"]
}
```



### With Vision Capabilities (screenshots)

```json
"playwright": {
  "command": "npx",
  "args": ["@playwright/mcp@latest", "--caps=vision"]
}
```



## Available Tools (Core)

| Tool | Description ||------|-------------|| `browser_navigate` | Navigate to a URL || `browser_snapshot` | Get accessibility tree snapshot || `browser_click` | Click on element by ref || `browser_type` | Type text into element || `browser_hover` | Hover over element || `browser_select_option` | Select dropdown option || `browser_press_key` | Press keyboard key || `browser_wait_for` | Wait for text/condition || `browser_navigate_back` | Go back || `browser_resize` | Resize browser window || `browser_console_messages` | Get console logs || `browser_network_requests` | Get network requests || `browser_take_screenshot` | Take screenshot (visual) |

## Decision: Keep or Replace browser-tools?

- **Option A**: Keep both - Use Playwright for automation, browser-tools for Lighthouse audits
- **Option B**: Replace - Remove browser-tools entirely, use Playwright for everything
- **Recommendation**: Start with Option A, evaluate after testing

## Files to Modify

- [`~/.cursor/mcp.json`](~/.cursor/mcp.json) - Add playwright server configuration