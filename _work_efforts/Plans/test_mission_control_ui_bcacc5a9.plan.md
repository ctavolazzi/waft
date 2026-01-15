---
name: Test Mission Control UI
overview: Start the Mission Control dashboard server and test the browser UI using Playwright browser tools.
todos:
  - id: start-server
    content: Start Mission Control dev server in background
    status: pending
  - id: browser-test
    content: Navigate to dashboard and test UI with browser tools
    status: pending
    dependencies:
      - start-server
---

# Test Mission Control Browser UI

## Overview

Start the Mission Control dashboard server and interactively test the UI.

## Server Details

- **Location**: [`mcp-servers/dashboard/`](mcp-servers/dashboard/)
- **Start command**: `npm run dev` (or `npm start`)
- **Default port**: 3847
- **URL**: http://localhost:3847

## Steps

1. **Start the server** (background process)
   ```bash
         cd /Users/ctavolazzi/Code/active/_pyrite/mcp-servers/dashboard
         npm run dev
   ```




2. **Navigate to the dashboard** using browser tools

- URL: http://localhost:3847

3. **Test the UI** - Take snapshots, interact with elements, verify features work

- Check dashboard loads
- View work efforts
- Test any responsive/interactive features from WE-251227-fwmv

## Notes

- Server auto-finds available port if 3847 is in use