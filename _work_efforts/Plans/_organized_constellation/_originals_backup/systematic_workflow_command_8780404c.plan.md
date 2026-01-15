---
name: Systematic Workflow Command
overview: "Create a new slash command `/systematic` that orchestrates a comprehensive workflow sequence: consider → think → check-assumptions → deep-analyze → critique → status → hypothesis → prove-it → verify → proceed → reflect → checkpoint → decide → next → goal. This command provides a methodical, evidence-based approach to work that balances critical analysis with deep understanding."
todos: []
---

# Systematic Workflow Command - Implementation Plan

## Overview

Create a new slash command `/systematic` that orchestrates a comprehensive, methodical workflow for approaching complex work. This command balances critical analysis (critique) with deep understanding (deep-analyze), ensures assumptions are checked early, and guides through hypothesis formation, verification, reflection, and strategic decision-making.

## Command Name

**Proposed**: `/systematic`

**Alternative names to consider**:

- `/full-cycle` - Emphasizes complete cycle
- `/methodical` - Emphasizes methodical approach
- `/complete` - Emphasizes completeness

## Workflow Sequence

The command executes these phases in order:

### Phase 1: Consider Options

**Command**: `/consider`
**Purpose**: Analyze current situation, identify options, evaluate trade-offs
**Output**: Situation analysis, options, recommendations

### Phase 2: Initialize Cognitive Tools

**Command**: `/think`
**Purpose**: Activate all thinking and cognitive enhancement tools
**Output**: Empirica initialized, sequential thinking ready, work efforts active

### Phase 3: Check Assumptions Early

**Command**: `/check-assumptions`
**Purpose**: Identify and validate all assumptions with evidence
**Output**: Assumption validation report with evidence traces

### Phase 4: Deep Analysis (Before Critique)

**Command**: `/deep-analyze`
**Purpose**: Deep code analysis to understand before critiquing
**Output**: Comprehensive analysis documents, algorithms extracted, patterns identified
**Note**: This runs BEFORE critique to balance harsh criticism with understanding

### Phase 5: Adversarial Critique

**Command**: `/critique`
**Purpose**: Security-first adversarial review, find all ways things could fail
**Output**: Critique report with security vulnerabilities, assumptions, overengineering
**Note**: Run after deep-analyze so critique is informed by understanding

### Phase 6: Quick Status Check

**Command**: `/status`
**Purpose**: Immediate status snapshot
**Output**: Git status, active work, recent activity, health indicators

### Phase 7: Form Hypothesis

**Command**: `/hypothesis`
**Purpose**: Form testable hypotheses based on analysis
**Output**: Hypothesis document with evidence, predictions, verification plan

### Phase 8: Prove Scientific Method

**Command**: `/prove-it`
**Purpose**: Demonstrate scientific method tool works
**Output**: Proof demonstration showing state capture, data collection, analysis

### Phase 9: Verify Everything

**Command**: `/verify`
**Purpose**: Lightweight diagnostic verification with traceable evidence
**Output**: Verification traces for all claims, evidence documentation

### Phase 10: Verify Context Before Proceeding

**Command**: `/proceed`
**Purpose**: Verify context and assumptions before continuing
**Output**: Verified understanding, assumptions checked, ambiguities resolved

### Phase 11: Final Reflection

**Command**: `/reflect`
**Purpose**: Write reflective journal entry on entire experience
**Output**: Journal entry in `_pyrite/journal/ai-journal.md`

### Phase 12: Create Checkpoint

**Command**: `/checkpoint`
**Purpose**: Situation report and status update
**Output**: Checkpoint file, devlog updated, work efforts synced

### Phase 13: Strategic Decision

**Command**: `/decide`
**Purpose**: Mathematical decision matrix calculations
**O