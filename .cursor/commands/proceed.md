# Proceed

**Keep doing what you're doing, but verify context and assumptions first.**

Pauses to check larger context, reflect on assumptions, ask clarifying questions, perform a "flight check", then proceeds with verified understanding. Ensures no unverified assumptions or unclear ambiguity before taking actions.

**Use when:** Want to continue work but need to verify context, check assumptions, or clarify ambiguity before proceeding.

---

## Purpose

Provides: context verification, assumption checking, ambiguity resolution, flight check, verified continuation.

---

## Philosophy

1. **Verify Before Acting**: Don't forge ahead blindly
2. **Check Context**: Understand larger picture first
3. **Question Assumptions**: Identify and verify assumptions
4. **Resolve Ambiguity**: Clarify unclear points
5. **Flight Check**: Ensure everything is ready
6. **Proceed Safely**: Continue with verified understanding

---

## Execution Steps

### Step 1: Context Gathering
**Purpose**: Understand current state and larger context

**Actions**:
1. Review current work state (files, git status, recent changes)
2. Check related files and dependencies
3. Understand project structure and patterns
4. Review recent conversation history
5. Identify what was being worked on

**Output**: Comprehensive context understanding

---

### Step 2: Assumption Identification
**Purpose**: Find unverified assumptions

**Actions**:
1. Identify assumptions being made
2. List implicit beliefs about code/requirements
3. Note assumptions about user intent
4. Flag assumptions about system state
5. Categorize assumptions (critical vs minor)

**Output**: List of assumptions to verify

---

### Step 3: Ambiguity Detection
**Purpose**: Find unclear or ambiguous points

**Actions**:
1. Identify ambiguous requirements
2. Find unclear specifications
3. Note vague instructions
4. Flag uncertain dependencies
5. List areas needing clarification

**Output**: List of ambiguities to resolve

---

### Step 4: Flight Check
**Purpose**: Verify everything is ready to proceed

**Actions**:
1. Verify context is understood
2. Check assumptions are identified
3. Confirm ambiguities are noted
4. Review potential risks
5. Ensure prerequisites are met
6. Check for blockers

**Output**: Flight check status

---

### Step 5: Clarifying Questions
**Purpose**: Ask questions to resolve assumptions/ambiguity

**Actions**:
1. Formulate clarifying questions
2. Prioritize questions by importance
3. Present questions clearly
4. Wait for answers if critical
5. Proceed if questions are minor

**Output**: Questions asked, answers received (if any)

---

### Step 6: Verified Proceeding
**Purpose**: Continue with verified understanding

**Actions**:
1. Summarize verified context
2. Note assumptions verified
3. Document ambiguities resolved
4. Proceed with work
5. Continue checking as you go

**Output**: Continued work with awareness

---

## What Gets Checked

### Context
- Current work state
- Related files and dependencies
- Project structure and patterns
- Recent changes and history
- System state

### Assumptions
- Implicit beliefs about code
- Assumptions about requirements
- Beliefs about user intent
- Assumptions about system state
- Technical assumptions

### Ambiguity
- Unclear requirements
- Vague specifications
- Uncertain instructions
- Ambiguous dependencies
- Unclear expectations

### Flight Check Items
- Context understood
- Assumptions identified
- Ambiguities noted
- Risks assessed
- Prerequisites met
- No blockers

---

## Output Format

### Context Summary
```
📋 Context Check

Current State:
- Working on: [what]
- Files involved: [list]
- Recent changes: [summary]
- Related context: [larger picture]
```

### Assumptions Identified
```
⚠️ Assumptions Found

Critical:
- [Assumption 1] - [Why it matters]
- [Assumption 2] - [Why it matters]

Minor:
- [Assumption 3] - [Why it matters]
```

### Ambiguities Detected
```
❓ Ambiguities Found

- [Ambiguity 1] - [What's unclear]
- [Ambiguity 2] - [What's unclear]
```

### Flight Check
```
✈️ Flight Check

✅ Context: Understood
✅ Assumptions: Identified
⚠️ Ambiguities: [count] found
✅ Prerequisites: Met
✅ Blockers: None

Status: [READY / NEEDS CLARIFICATION]
```

### Clarifying Questions
```
❓ Clarifying Questions

1. [Question 1] - [Why it matters]
2. [Question 2] - [Why it matters]

[Proceeding with best understanding, will ask if critical]
```

---

## Usage Examples

### Basic Usage
```
/proceed
```

### With Focus Area
```
/proceed --focus assumptions
/proceed --focus ambiguity
/proceed --focus context
```

### With Verification Level
```
/proceed --strict  # Ask questions before proceeding
/proceed --relaxed # Proceed with best understanding
```

---

## Integration

- **`/continue`**: Reflect and continue (proceed is more verification-focused)
- **`/checkpoint`**: Status snapshot (proceed is pre-action verification)
- **`/verify`**: Post-action verification (proceed is pre-action)
- **`/reflect`**: Pure reflection (proceed includes reflection + verification)

---

## When to Use

**Use `/proceed` when**:
- ✅ About to make significant changes
- ✅ Need to verify assumptions
- ✅ Want to check context first
- ✅ Need to clarify ambiguity
- ✅ Want flight check before proceeding
- ✅ Unsure about current understanding

**Don't use `/proceed` when**:
- ❌ Already verified everything (just proceed)
- ❌ Need pure reflection (use `/reflect`)
- ❌ Need status check (use `/checkpoint`)
- ❌ Need post-action verification (use `/verify`)

---

**This command ensures you proceed with verified understanding, checking assumptions and resolving ambiguity before taking action.**
