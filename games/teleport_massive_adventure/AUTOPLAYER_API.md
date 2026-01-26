# AutoPlayer API - Programmatic Control

**Date:** 2026-01-25  
**Status:** ✅ Ready for AI Agent Control

---

## Overview

The AutoPlayer can now be triggered programmatically through multiple methods, making it easy for AI agents, automation tools, and scripts to start the game automatically.

---

## Methods to Start AutoPlayer

### Method 1: URL Parameter (Recommended)

Add `?auto=true` or `?autoplayer=true` to the game URL:

```
http://localhost:8000/index_v2.html?auto=true
```

The AutoPlayer will automatically start 2 seconds after the game loads.

**Example:**
```bash
open "http://localhost:8000/index_v2.html?auto=true"
```

### Method 2: Global Function

Call the global `startAutoPlayer()` function from browser console or scripts:

```javascript
// In browser console
startAutoPlayer();

// Returns: true if started, false if already running
```

### Method 3: Direct Instance Access

Access the AutoPlayer instance directly:

```javascript
// In browser console
window.autoPlayer.start();

// Check status
window.autoPlayer.getProgress();
```

### Method 4: Playwright Automation (For AI Agents)

Use the provided Node.js script:

```bash
cd games/teleport_massive_adventure
node scripts/start_autoplayer.js
```

Or use the shell script:

```bash
./scripts/start_autoplayer.sh
```

---

## Playwright MCP Integration

For AI agents using Playwright MCP, you can:

```javascript
// Navigate with auto parameter
await page.goto('http://localhost:8000/index_v2.html?auto=true');

// Or click the button
await page.click('#auto-player-btn');

// Or call the function
await page.evaluate(() => startAutoPlayer());
```

---

## API Reference

### Global Functions

#### `startAutoPlayer()`
- **Returns:** `boolean` - `true` if started, `false` if already running
- **Usage:** `startAutoPlayer()`

### AutoPlayer Instance Methods

#### `autoPlayer.start()`
- Starts the automated playthrough
- **Usage:** `window.autoPlayer.start()`

#### `autoPlayer.stop()`
- Stops the automated playthrough
- **Usage:** `window.autoPlayer.stop()`

#### `autoPlayer.pause()`
- Pauses the automated playthrough
- **Usage:** `window.autoPlayer.pause()`

#### `autoPlayer.resume()`
- Resumes from pause
- **Usage:** `window.autoPlayer.resume()`

#### `autoPlayer.getProgress()`
- Returns current progress information
- **Returns:** Object with `{ currentStep, totalSteps, progress, isRunning, currentScene }`
- **Usage:** `window.autoPlayer.getProgress()`

---

## Example: AI Agent Usage

### Using Playwright MCP

```javascript
// 1. Navigate to game with auto parameter
await call_mcp_tool({
    server: "playwright",
    toolName: "browser_navigate",
    arguments: {
        url: "http://localhost:8000/index_v2.html?auto=true"
    }
});

// 2. Wait for game to load
await call_mcp_tool({
    server: "playwright",
    toolName: "browser_wait_for",
    arguments: {
        text: "AUTO"
    }
});

// 3. Take screenshot to verify
await call_mcp_tool({
    server: "playwright",
    toolName: "browser_take_screenshot",
    arguments: {}
});

// 4. Check AutoPlayer status
const status = await page.evaluate(() => {
    return window.autoPlayer?.getProgress();
});
```

### Using Node.js Script

```bash
# Start server (if not running)
cd games/teleport_massive_adventure
python3 -m http.server 8000 &

# Start AutoPlayer
node scripts/start_autoplayer.js
```

---

## URL Parameters

| Parameter | Value | Effect |
|-----------|-------|--------|
| `auto` | `true` | Auto-start AutoPlayer after 2 seconds |
| `autoplayer` | `true` | Same as `auto=true` |

**Examples:**
- `?auto=true`
- `?autoplayer=true`
- `?auto=true&debug=true` (if debug mode exists)

---

## Troubleshooting

### AutoPlayer doesn't start from URL

1. Check browser console for errors
2. Verify game is fully loaded (wait longer)
3. Try calling `startAutoPlayer()` manually in console
4. Check that `window.autoPlayer` exists

### Playwright script fails

1. Ensure server is running: `curl http://localhost:8000/index_v2.html`
2. Check Playwright is installed: `npm list playwright`
3. Verify port 8000 is available

### Button not found

1. Check selector: `#auto-player-btn`
2. Verify UI is loaded: `document.getElementById('auto-player-btn')`
3. Wait for game initialization

---

## Integration Examples

### GitHub Actions

```yaml
- name: Test AutoPlayer
  run: |
    cd games/teleport_massive_adventure
    python3 -m http.server 8000 &
    sleep 5
    node scripts/start_autoplayer.js
```

### CI/CD Pipeline

```bash
# Start game server
python3 -m http.server 8000 &
SERVER_PID=$!

# Wait for server
sleep 3

# Run AutoPlayer test
node scripts/start_autoplayer.js

# Cleanup
kill $SERVER_PID
```

---

**Last Updated:** 2026-01-25  
**Version:** 1.0
