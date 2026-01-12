# Think

**Purpose**: Initialize all thinking and cognitive enhancement tools to kick thinking into high gear.

**Use when**: 
- Starting a new session
- Need to activate all cognitive tools
- Want to maximize thinking capabilities
- Beginning complex work that requires deep reasoning

---

## What This Command Does

Initializes and activates all available thinking and cognitive enhancement tools:

1. **Empirica** - Epistemic self-assessment and learning tracking
2. **Sequential Thinking** - Hierarchical planning and step-by-step reasoning
3. **Work Efforts** - Task tracking and knowledge persistence
4. **Project Bootstrap** - Load compressed project context
5. **Session Creation** - Create new epistemic session
6. **State Assessment** - Current cognitive/epistemic state

---

## Execution Steps

### Step 1: Verify Environment
**Purpose**: Ensure prerequisites are met

**Actions**:
1. Check current date/time
2. Verify Python version (3.11+ for Empirica)
3. Check if git is initialized (required for Empirica)
4. Verify Empirica CLI availability
5. Check MCP servers (sequential-thinking, work-efforts)

**Output**: Environment status report

---

### Step 2: Initialize Empirica
**Purpose**: Set up epistemic tracking

**Actions**:
1. Check if Empirica is initialized: `uv run empirica project-info`
2. If not initialized, run: `uv run empirica project-init`
3. Verify initialization: Check for `.empirica/config.yaml`
4. Report initialization status

**Output**: Empirica initialization status

---

### Step 3: Create Empirica Session
**Purpose**: Start new epistemic tracking session

**Actions**:
1. Create session: `uv run empirica session-create --ai-id waft --output json`
2. Capture session ID from response
3. Store session ID for use in preflight/postflight
4. Report session created

**Output**: Session ID and status

---

### Step 4: Project Bootstrap
**Purpose**: Load compressed project context (~800 tokens)

**Actions**:
1. Run: `uv run empirica project-bootstrap --output json`
2. Extract epistemic state, goals, findings, unknowns
3. Display summary of current knowledge state
4. Report what's known and what's unknown

**Output**: Project context summary

---

### Step 5: Initialize Sequential Thinking
**Purpose**: Activate hierarchical planning capabilities

**Actions**:
1. Check if Sequential Thinking MCP is available
2. If available, prepare for use
3. Document that sequential thinking is ready
4. Note: Sequential thinking is used via MCP tools during work

**Output**: Sequential thinking availability

---

### Step 6: Activate Work Efforts System
**Purpose**: Ensure task tracking is ready

**Actions**:
1. Check if `_work_efforts/` directory exists
2. If exists, list active work efforts
3. If not, note that work efforts can be created
4. Verify work-efforts MCP server (if available)

**Output**: Work efforts status

---

### Step 7: Assess Current State
**Purpose**: Get baseline cognitive state

**Actions**:
1. Run epistemic state assessment (if Empirica initialized)
2. Check current work efforts status
3. Review recent devlog entries
4. Assess current knowledge gaps

**Output**: Current state summary

---

### Step 8: Ready for High-Gear Thinking
**Purpose**: Confirm all systems operational

**Actions**:
1. Summarize all initialized tools
2. Report session ID for tracking
3. Display epistemic state (if available)
4. List available cognitive tools
5. Provide next steps

**Output**: Complete initialization report

---

## Output Format

### Environment Status
```
🌍 Environment Check
- Date: [current date/time]
- Python: [version]
- Git: [initialized/not initialized]
- Empirica CLI: [available/not available]
- MCP Servers: [status]
```

### Empirica Status
```
📊 Empirica Status
- Initialized: [yes/no]
- Config: [path]
- Session ID: [session_id]
- Status: [ready/not ready]
```

### Project Context
```
📚 Project Context
- Epistemic State: [summary]
- Goals: [count]
- Findings: [count]
- Unknowns: [count]
- Knowledge Coverage: [percentage]
```

### Cognitive Tools Ready
```
🧠 Cognitive Tools
- ✅ Empirica: [ready]
- ✅ Sequential Thinking: [ready/not available]
- ✅ Work Efforts: [ready]
- ✅ Project Bootstrap: [loaded]
```

### Current State
```
📈 Current State
- Epistemic Phase: [phase]
- Knowledge: [percentage]
- Uncertainty: [percentage]
- Active Work: [count]
```

---

## Integration

### With Other Commands
- **`/orient`**: Use before orient for full cognitive setup
- **`/proceed`**: Use before proceeding for verified thinking
- **`/engineer`**: Use at start of engineering workflow
- **`/reflect`**: Use before reflection for epistemic tracking

### With Workflows
- **Preflight**: Submit preflight assessment after initialization
- **Work**: Use sequential thinking during complex tasks
- **Postflight**: Submit postflight assessment after work
- **Tracking**: Log findings and unknowns as you work

---

## Example Usage

### Basic Initialization
```
/think
```

### With Preflight Assessment
```
/think
[Then immediately submit preflight]
```

### At Session Start
```
/think
[Then proceed with work using all cognitive tools]
```

---

## What Gets Initialized

### Empirica
- ✅ Project initialization
- ✅ Session creation
- ✅ Project bootstrap (context loading)
- ✅ State assessment ready

### Sequential Thinking
- ✅ MCP server check
- ✅ Tool availability confirmed
- ✅ Ready for hierarchical planning

### Work Efforts
- ✅ Directory check
- ✅ Active work listing
- ✅ MCP server check

### Project Context
- ✅ Epistemic state loaded
- ✅ Goals retrieved
- ✅ Findings/unknowns loaded
- ✅ Knowledge gaps identified

---

## Success Criteria

**All systems ready when**:
- ✅ Empirica initialized and session created
- ✅ Project context loaded (or gracefully handled if not available)
- ✅ Work efforts system accessible
- ✅ Sequential thinking available (if MCP configured)
- ✅ Current state assessed
- ✅ Ready for high-gear thinking

---

## Error Handling

### Empirica Not Available
- ⚠️ Report warning but continue
- ⚠️ Note that epistemic tracking unavailable
- ✅ Continue with other tools

### Git Not Initialized
- ⚠️ Attempt to initialize git
- ⚠️ If fails, report that Empirica requires git
- ✅ Continue with other tools

### MCP Servers Not Available
- ⚠️ Report which servers unavailable
- ✅ Continue with available tools
- ℹ️ Note that some features may be limited

### Project Bootstrap Fails
- ⚠️ Report that project context unavailable
- ✅ Continue with manual context gathering
- ℹ️ Note that epistemic state may be incomplete

---

## Next Steps After Initialization

1. **Submit Preflight Assessment**
   ```bash
   uv run empirica preflight-submit -
   ```

2. **Start Sequential Thinking** (if needed)
   - Use `mcp_sequential-thinking_sequentialthinking` tool
   - Break down complex tasks into steps

3. **Begin Work**
   - Use all initialized tools
   - Log findings as you discover them
   - Track unknowns as they arise

4. **Submit Postflight Assessment**
   ```bash
   uv run empirica postflight-submit -
   ```

---

**This command ensures all thinking and cognitive tools are initialized and ready for high-performance cognitive work.**

--- End Command ---
