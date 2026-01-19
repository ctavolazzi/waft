# Cognitive Tools UI - Design Document

**Date**: 2026-01-18 07:21:40 PST
**Status**: Design Phase (Pre-Implementation)

---

## What Was Observed in the Chat

### 1. Real-Time Cognitive Tools Demonstration
- **Sequential Thinking**: Demonstrated 6-8 step problem-solving chains
  - Broke down complex problems into steps
  - Showed iterative thinking process
  - Tracked thought history

- **Empirica**: Logged findings and unknowns in real-time
  - Created session: `9c8a7c65-ab3f-433a-8c9c-ad03f07c7d73`
  - Logged 7+ findings about the demonstration
  - Tracked 3+ unknowns (issues discovered)
  - Showed epistemic tracking in action

- **Work Efforts**: Referenced 104 active work efforts
  - System tracks ongoing work
  - Links to related work efforts

### 2. Tools Adapting and Learning
- When `sessions-show` command failed, tools adapted to use alternatives
- Tools learned what works/doesn't work
- Complete iteration cycle demonstrated: Problem → Solution → Learning → Improvement

### 3. Evidence-Based Development
- Case files document decisions
- Screenshots show progress
- Proof system validates work

---

## The Problem This UI Solves

**Problem**: After demonstrating cognitive tools working, there's no way to:
- **See** what the tools are doing in real-time
- **Understand** how they're coordinating
- **Track** the learning and adaptation happening
- **Review** the evidence (case files, findings, unknowns)
- **Monitor** the epistemic state

**Current State**: Tools work, but their activity is invisible unless you check logs/CLI

**Desired State**: Visual dashboard showing cognitive tools in action

---

## Purpose of This UI

**Primary Purpose**: 
**Make the invisible cognitive work visible** - Show what Sequential Thinking, Empirica, and Work Efforts are doing, how they're coordinating, and what they're learning.

**Secondary Purposes**:
- **Monitor** cognitive tools status and activity
- **Review** evidence (case files, findings, unknowns)
- **Understand** epistemic state and learning
- **Track** work effort integration
- **See** tools adapting and improving

---

## What This UI Should Accomplish

1. **Show Real-Time Activity**
   - Current Sequential Thinking chains
   - Recent Empirica findings/unknowns
   - Active work efforts

2. **Display Coordination**
   - How tools work together
   - Integration status
   - Data flow between tools

3. **Show Learning**
   - What tools have learned
   - Adaptation evidence
   - Iteration cycles

4. **Present Evidence**
   - Case files from decisions
   - Proof of work
   - Screenshots of progress

5. **Monitor Epistemic State**
   - Knowledge coverage
   - Uncertainty levels
   - Epistemic phase

---

## Key Features Needed

1. **Status Dashboard**: Overall tool status
2. **Activity Feed**: Recent findings, unknowns, thoughts
3. **Case Files Display**: Proof evidence visible
4. **Epistemic State**: Knowledge/uncertainty visualization
5. **Work Efforts Integration**: Link to active work
6. **Real-Time Updates**: Show tools working

---

## What Makes This Different

This isn't just a status page - it's a **window into cognitive work happening in real-time**. It shows:
- **Thinking in progress** (Sequential Thinking chains)
- **Learning happening** (Empirica findings accumulating)
- **Adaptation occurring** (tools learning from failures)
- **Evidence building** (case files documenting decisions)

---

## Success Criteria

The UI succeeds when:
- ✅ User can see cognitive tools working
- ✅ User understands how tools coordinate
- ✅ User can review evidence (case files)
- ✅ User can monitor epistemic state
- ✅ User sees tools learning and adapting

---

## User Persona

**Primary User**: Developer using WAFT framework
- Wants to understand what cognitive tools are doing
- Needs visibility into epistemic tracking
- Wants to review evidence and decisions
- Interested in seeing tools learn and adapt

---

## Use Cases

1. **After running `/think` command**: See what tools initialized
2. **During work session**: Monitor tools working in background
3. **Reviewing decisions**: Check case files for proof
4. **Understanding learning**: See what tools have learned
5. **Debugging issues**: See how tools adapted to problems

---

## Interaction Model

**Primary Mode**: **View-Only Dashboard**
- Display real-time status
- Show activity feeds
- Present evidence
- Monitor state

**Future Interactions** (Phase 2):
- Filter/sort findings
- Drill into case files
- Export reports
- Manual refresh

---

**This UI makes the invisible cognitive infrastructure visible and understandable.**
