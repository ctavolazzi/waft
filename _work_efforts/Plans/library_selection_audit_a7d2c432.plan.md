---
name: Library Selection Audit
overview: "Quick audit to decide which fundamental libraries to add. For each category: identify actual need, pick a library (or skip), done."
todos:
  - id: grep-audit
    content: "Run greps: console.log count, startup output, async patterns"
    status: pending
  - id: decisions
    content: Make yes/no decision for each category based on findings
    status: pending
  - id: write-doc
    content: Create library_decisions.md with table and rationale
    status: pending
  - id: install
    content: npm install chosen libraries
    status: pending
---

# Library Selection Audit

## Approach

For each category, answer three questions:
1. **Do we have a real problem today?** (not hypothetical)
2. **If yes, which library solves it simplest?**
3. **Add it or skip it?**

---

## Audit Checklist

### 1. Logging

**Quick check:** Grep for console.log patterns in MCP servers

**Decision criteria:**
- If logs are hard to read/filter in production -> add structured logging
- If just dev debugging -> console.log is fine

**Candidates:** `pino` (fast, JSON) or `debug` (lightweight namespaces)

---

### 2. CLI Graphics

**Quick check:** Look at current server startup output

**Decision criteria:**
- If servers output status messages -> colored output helps
- If users see progress -> spinners help

**Candidates:** `chalk` + `ora` (minimal) or just `chalk`

---

### 3. Animation (CLI)

**Quick check:** Any long-running CLI operations?

**Decision criteria:**
- If file watching / batch ops -> spinner useful
- Otherwise -> skip, ora covers this anyway

**Likely verdict:** Skip as separate concern; ora handles it

---

### 4. ffmpeg

**Quick check:** Any video/audio processing in roadmap?

**Decision criteria:**
- If yes -> `fluent-ffmpeg` + `ffmpeg-static`
- If no -> skip entirely, add when needed

**Likely verdict:** Skip unless you have a use case

---

### 5. Async/Event Control

**Quick check:** Review EventBus.js and file watcher patterns

**Decision criteria:**
- If hitting rate limits or need queuing -> `p-queue`
- If EventEmitter is slow/limited -> `eventemitter3`
- If current approach works -> skip

---

## Output

Single markdown file: `_docs/30-39_reference/library_decisions.md`

```markdown
# Library Decisions - Dec 2025

| Category      | Decision | Library      | Rationale           |
|---------------|----------|--------------|---------------------|
| Logging       | ADD/SKIP | pino/debug   | [one sentence]      |
| CLI Graphics  | ADD/SKIP | chalk+ora    | [one sentence]      |
| Animation     | SKIP     | -            | Covered by ora      |
| ffmpeg        | DEFER    | -            | No use case yet     |
| Async Control | ADD/SKIP | p-queue      | [one sentence]      |
```

---

## Execution

1. Run greps to answer the quick checks (~5 min)
2. Make decisions based on findings (~5 min)
3. Write decision file (~5 min)
4. Install chosen libraries (~2 min)

**Total: ~15-20 minutes**, not a multi-day initiative.
