---
category: hopes
confidence: 1.00
constellation_date: 2026-01-14
original_file: logging_and_cli_enhancement_a0d0d475.plan.md
---

# Structured Logging and CLI Graphics

## Summary

Add `pino` for structured JSON logging and `chalk` for colored CLI output in [server.js](mcp-servers/dashboard/server.js). Client-side files (browser code) will keep `console.log` since pino is Node-only.

## Files to Modify

| File | Changes ||------|---------|| `package.json` | Add pino, chalk dependencies || `server.js` | Replace console.log with pino logger, add chalk colors || `lib/watcher.js` | Replace console.log with pino || `docs/DECISION-*.md` | New decision document |

## Implementation

### 1. Create Decision Document

Document in `docs/` following the pattern:

- Context: 50 unstructured console.log calls
- Decision: pino for logging, chalk for CLI
- Rationale: Structured JSON, log levels, colored output
- Alternatives considered: winston (heavier), bunyan (older)

### 2. Install Dependencies

```bash
npm install pino chalk
```



### 3. Create Logger Module

New file `lib/logger.js`:

```javascript
import pino from 'pino';
const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  transport: {
    target: 'pino-pretty',  // Dev only, remove for production
    options: { colorize: true }
  }
});
export default logger;
```



### 4. Refactor server.js

Replace ~30 console.log/error calls:

- `console.log()` -> `logger.info()`
- `console.error()` -> `logger.error()`
- `console.warn()` -> `logger.warn()`

Add chalk to startup banner:

```javascript
import chalk from 'chalk';
console.log(chalk.cyan(`
  ╔══════════════════════════════════════════════╗
  ║  ${chalk.bold('Mission Control Dashboard')}              ║
  ╠══════════════════════════════════════════════╣
  ║  Local: ${chalk.green(`http://localhost:${port}`)}         ║
  ╚══════════════════════════════════════════════╝
`));
```



### 5. Refactor lib/watcher.js

Replace console.log calls with logger.debug/info.

## Out of Scope

- Client-side files (app.js, events.js, etc.) - browser code keeps console.log
- pino-pretty as production dependency - dev only

## Verification

1. Start server, verify colored banner displays