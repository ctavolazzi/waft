---
name: Test Mission Control UI
overview: Start the Mission Control dashboard and systematically test the completed responsive CSS feature, then explore pending feature areas.
todos:
  - id: start-server
    content: Start Mission Control dev server in background
    status: pending
  - id: test-desktop
    content: Navigate to dashboard, take snapshot at default viewport
    status: pending
    dependencies:
      - start-server
  - id: test-responsive
    content: Test tablet (768px) and mobile (375px) breakpoints
    status: pending
    dependencies:
      - test-desktop
  - id: explore-features
    content: Click through UI to assess pending feature status
    status: pending
    dependencies:
      - test-responsive
  - id: document
    content: Summarize findings - what works, what needs work
    status: pending
    dependencies:
      - explore-features
---

# Test Mission Control Browser UI

## Pre-flight (Already Verified)
- Dependencies installed (node_modules exists)
- Config watches `_pyrite` and `fogsift` repos
- Port: 3847
- No conflicting processes running

## Execution Steps

### 1. Start Server
```bash
cd /Users/ctavolazzi/Code/active/_pyrite/mcp-servers/dashboard && npm run dev
```
Run in background, wait for "Server started" message.

### 2. Test Completed Feature: Responsive CSS (TKT-fwmv-001)
- Navigate to http://localhost:3847
- Take desktop snapshot (default viewport)
- Resize to tablet (768px) - verify layout adapts
- Resize to mobile (375px) - verify mobile navigation works
- Screenshot at each breakpoint for visual verification

### 3. Explore Pending Feature Areas
| Feature | What to Look For |
|---------|------------------|
| Ticket Detail Modal | Click a ticket - does modal appear? |
| Stats/Graphs | Check if chart area exists, even if placeholder |
| Work Controls | Look for start/stop/edit buttons |
| Agent Assignment | Check for agent-related UI elements |

### 4. Document Findings
Report what works, what's missing, what needs implementation.

## Success Criteria
- Server starts without errors
- Dashboard loads and displays work efforts
- Responsive breakpoints function as expected
- Clear understanding of pending feature status
