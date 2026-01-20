# Chat Context Scan - Evolve UI Monitor Request

**Date**: 2026-01-18 07:26:00 PST
**Purpose**: Extract what user wants for evolve-a-ui monitoring UI

---

## What User Requested

**Request**: "I want a UI to exist where we can monitor runs of the evolve the UI command"

---

## What This Means

### User Need
- **Monitor** when `/evolve-a-ui` is executed
- **Track** what it produces (screenshots, case files, HTML files)
- **View** the evolution process
- **See** progress of UI development
- **Review** generated artifacts

### Context
- We just created the `/evolve-a-ui` command
- It produces: HTML files, screenshots, case files, design docs, requirements
- Output location: `_genetics/ui_evolution/` (per command doc)
- Process: Methodical, step-by-step with proof

---

## What Should Be Monitored

1. **Command Executions**
   - When `/evolve-a-ui` was run
   - What chat context it analyzed
   - What design doc was created

2. **Generated Artifacts**
   - HTML files created
   - Screenshots taken
   - Case files generated
   - Design documents
   - Requirements documents

3. **Process Progress**
   - Which phase it's in (Analysis, Requirements, Wireframe, Development)
   - Current step
   - Screenshots of progress

4. **Evidence**
   - Case files created
   - Proof of decisions
   - Verification traces

---

## Key Insight

This is a **meta-UI** - a UI for monitoring the creation of UIs. It needs to:
- Track command executions
- Display generated artifacts
- Show process progress
- Link to evidence (case files, screenshots)

---

**Next**: Create design document for evolve-a-ui monitoring UI
