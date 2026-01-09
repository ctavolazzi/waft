# Compose

**Compose command sequences naturally, then save as new commands.**

Parse natural language to extract and execute command sequences. Take commonly used phrases and turn them into reusable commands. Gives you control over command composition and the ability to create new commands from sequences.

**Use when:** Want to compose commands naturally, create new commands from sequences, or execute multiple commands in order.

---

## Purpose

Provides: natural language interpretation, command sequence execution, command creation from sequences, composition control.

---

## Two Modes

### 1. Natural Language Composition
Type natural language describing command sequences - AI interprets and executes.

**Example:**
```
/compose "proceed to spin-up and analyze the project. proceed through phase1 and then prepare to move on to phase2. recap upon completion"
```

Or just type it directly (AI recognizes command sequences):
```
proceed to spin-up and analyze the project. proceed through phase1 and then prepare to move on to phase2. recap upon completion
```

### 2. Create Command from Sequence
Save a commonly used sequence as a new command.

**Example:**
```
/compose create "new-repo" "proceed to spin-up and analyze the project. proceed through phase1 and then prepare to move on to phase2. recap upon completion"
```

Then use it:
```
/new-repo
```

---

## Philosophy

1. **Natural First**: Use natural language - AI interprets your intent
2. **Composable**: Chain any commands together in any order
3. **Creatable**: Turn sequences into reusable commands
4. **Flexible**: Support both ad-hoc sequences and saved commands
5. **Control**: You control the composition

---

## Execution Steps

### Step 1: Interpret Natural Language
**Purpose**: Extract command sequence from natural language

**Actions**:
1. Parse natural language input
2. Extract command names (look for `/command` patterns)
3. Extract parameters (e.g., "phase2" → `phase=2`)
4. Build execution sequence
5. Validate commands exist

**Output**: Parsed command sequence

---

### Step 2: Execute Sequence
**Purpose**: Run commands in order

**Actions**:
1. Execute first command
2. Check result
3. Proceed to next command
4. Handle errors gracefully
5. Continue or stop on failure

**Output**: Execution results

---

### Step 3: Save as Command (Optional)
**Purpose**: Create new command from sequence

**Actions**:
1. Take executed sequence
2. Create command definition file
3. Save to `.cursor/commands/`
4. Command now available globally

**Output**: New command created

---

## Natural Language Interpretation

The AI interprets your natural language to extract command sequences:

**Input:**
```
"proceed to spin-up and analyze the project. proceed through phase1 and then prepare to move on to phase2. recap upon completion"
```

**AI Interpretation:**
- "proceed to spin-up and analyze" → execute `/proceed`, then `/spin-up`, then `/analyze`
- "proceed through phase1" → execute `/proceed`, then `/phase1`
- "prepare to move on to phase2" → execute `/prepare` with `phase=2` parameter
- "recap upon completion" → execute `/recap` at the end

**Extracted Sequence:**
```yaml
steps:
  - command: proceed
  - command: spin-up
  - command: analyze
  - command: proceed
  - command: phase1
  - command: prepare
    params:
      phase: 2
  - command: recap
```

---

## Usage Examples

### Compose Sequence
```
/compose "proceed to spin-up and analyze"
/compose "phase1 then analyze then recap"
/compose "continue, checkpoint, verify"
```

### Create Command from Sequence
```
/compose create "new-repo" "proceed to spin-up and analyze the project. proceed through phase1 and then prepare to move on to phase2. recap upon completion"
```

### Use Created Command
```
/new-repo
```

### List Created Commands
```
/compose list
```

### Show Command Details
```
/compose show new-repo
```

---

## Integration

- **All commands**: Can be composed together
- **Natural language**: AI interprets your phrases
- **Command creation**: Turn sequences into reusable commands
- **Global availability**: Created commands work everywhere

---

## When to Use

**Use `/compose` when**:
- ✅ Want to execute multiple commands in sequence
- ✅ Want to compose commands naturally
- ✅ Have a common sequence to save as command
- ✅ Need control over command composition

**Don't use `/compose` when**:
- ❌ Need single command (use command directly)
- ❌ Need interactive command execution
- ❌ Need conditional logic (use commands individually)

---

**This command gives you control over command composition and the ability to create new commands from your commonly used sequences.**
