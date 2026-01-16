# OpenHands Persistence for Multi-Session Workflows

**Date**: 2026-01-14 20:30:00
**Context**: Using OpenHands persistence to save/restore conversation state
**Status**: 💾 STATE PERSISTENCE ENABLED

---

## What Is Persistence?

Persistence allows you to **save and restore conversation state** for:
- **Long-running workflows** (pause and resume)
- **Multi-session development** (generate server in one session, Electron app in another)
- **Interruption recovery** (resume after crash or interruption)
- **Iterative development** (refine code across multiple sessions)

---

## How It Works

### 1. Save State

Create a conversation with a unique ID and persistence directory:

```python
import uuid

conversation_id = uuid.uuid4()
persistence_dir = "./.conversations"

conversation = Conversation(
    agent=agent,
    workspace=workspace_path,
    persistence_dir=persistence_dir,
    conversation_id=conversation_id,
)

# State is automatically saved after each conversation.run()
conversation.send_message("Start task")
conversation.run()  # State saved to disk
```

### 2. Restore State

Restore a conversation using the same ID and persistence directory:

```python
# Later, in a different session or after interruption
conversation = Conversation(
    agent=agent,
    workspace=workspace_path,
    persistence_dir=persistence_dir,
    conversation_id=conversation_id,  # Same ID as before
)

# Conversation state is automatically restored
conversation.send_message("Continue task")
conversation.run()  # Continues from saved state
```

---

## What Gets Persisted

The conversation state includes:

- ✅ **Message History**: Complete event log (user messages, agent responses, system events)
- ✅ **Agent Configuration**: LLM settings, tools, MCP servers, agent parameters
- ✅ **Execution State**: Current status (idle, running, paused), iteration count, stuck detection
- ✅ **Tool Outputs**: Results from bash commands, file operations, tool executions
- ✅ **Statistics**: LLM usage metrics (token counts, API calls, costs)
- ✅ **Workspace Context**: Working directory and file system state
- ✅ **Activated Skills**: Skills that have been enabled during the conversation
- ✅ **Secrets**: Managed credentials and API keys

**Complete State**: Everything needed to seamlessly resume the conversation!

---

## Persistence Directory Structure

When you set a `persistence_dir`, conversations are saved to:

```
.conversations/
├── <conversation-id-1>/
│   ├── base_state.json       # Core conversation state
│   └── events/               # Event files directory
│       ├── event-00000-<event-id>.json
│       ├── event-00001-<event-id>.json
│       └── ...
├── <conversation-id-2>/
│   ├── base_state.json
│   └── events/
│       └── ...
```

**Structure**:
- Each conversation has its own subdirectory (named by conversation ID)
- `base_state.json`: Core state (agent config, execution status, statistics, metadata)
- `events/`: Individual event files (sequential index + event ID)

**Benefits**:
- Granular access to events
- Better performance (no single large file)
- Easy to inspect/debug state

---

## Enhanced Generation Script

**File**: `scripts/generate_tavern_game_with_skills.py`

**New Features**:
- ✅ Persistence support (save/restore conversation state)
- ✅ `--resume <conversation-id>` flag to resume from saved state
- ✅ `--list` flag to list all saved conversations
- ✅ `--persistence-dir` flag to specify custom persistence directory

**Usage**:

```bash
# Start new generation (with persistence)
export LLM_API_KEY="your-key"
python scripts/generate_tavern_game_with_skills.py

# List saved conversations
python scripts/generate_tavern_game_with_skills.py --list

# Resume from saved state
python scripts/generate_tavern_game_with_skills.py --resume <conversation-id>

# Use custom persistence directory
python scripts/generate_tavern_game_with_skills.py --persistence-dir ./my-conversations
```

---

## Use Cases for Game Development

### 1. Multi-Session Development

**Session 1**: Generate FastAPI server
```bash
python scripts/generate_tavern_game_with_skills.py
# Run Phase 0, Phase 1
# Conversation state saved
```

**Session 2**: Generate Electron app (resume same conversation)
```bash
python scripts/generate_tavern_game_with_skills.py --resume <id>
# Continue with Phase 2, Phase 3, Phase 4
# Agent remembers previous work
```

**Benefit**: Agent has full context from previous phases!

---

### 2. Interruption Recovery

**Scenario**: Generation interrupted (crash, network issue, etc.)

**Before Persistence**:
- ❌ Lost all progress
- ❌ Must start over
- ❌ Agent forgets previous work

**With Persistence**:
- ✅ Resume from saved state
- ✅ Agent remembers all previous work
- ✅ Continue seamlessly

**Example**:
```bash
# Generation interrupted at Phase 2
# Later, resume:
python scripts/generate_tavern_game_with_skills.py --resume <id>
# Agent continues from Phase 2
```

---

### 3. Iterative Refinement

**Session 1**: Generate initial code
```bash
python scripts/generate_tavern_game_with_skills.py
# Generate all phases
```

**Session 2**: Refine based on feedback
```bash
python scripts/generate_tavern_game_with_skills.py --resume <id>
conversation.send_message("Add error handling to the FastAPI server")
conversation.run()
```

**Benefit**: Agent has full context of what was generated before!

---

### 4. Long-Running Tasks

**Scenario**: Generation takes hours (complex code, many files)

**With Persistence**:
- ✅ Pause at any time
- ✅ Resume later
- ✅ No lost progress

**Example**:
```bash
# Start generation
python scripts/generate_tavern_game_with_skills.py
# Run Phase 0, Phase 1
# Pause (Ctrl+C or natural break)

# Later, resume:
python scripts/generate_tavern_game_with_skills.py --resume <id>
# Continue with Phase 2, Phase 3, Phase 4
```

---

## Implementation Details

### Conversation ID

**UUID-based**: Each conversation gets a unique UUID

```python
import uuid

# Generate new ID
conversation_id = uuid.uuid4()

# Or use existing ID to resume
conversation_id = uuid.UUID("existing-id-string")
```

**Best Practice**: Store conversation IDs for important workflows

---

### Persistence Directory

**Default**: `workspace/conversations/` (relative to workspace)

**Custom**: Specify with `persistence_dir` parameter

```python
conversation = Conversation(
    agent=agent,
    workspace=workspace_path,
    persistence_dir="./.conversations",  # Custom directory
    conversation_id=conversation_id,
)
```

**Best Practice**: Use project-specific directory (e.g., `.conversations/`)

---

### Automatic Saving

**State is saved automatically**:
- After each `conversation.run()`
- After each tool execution
- After each agent response

**No manual save needed!**

---

### State Restoration

**Automatic restoration** when:
- Same `conversation_id` is used
- Same `persistence_dir` is used
- State files exist

**If state doesn't exist**: Conversation starts fresh (new conversation)

---

## Complete Workflow Example

### Step 1: Start Generation

```bash
export LLM_API_KEY="your-key"
python scripts/generate_tavern_game_with_skills.py
```

**Output**:
```
🚀 Generating Electron Tavern Game with OpenHands SDK + MCP + Skills + Persistence
   Model: anthropic/claude-sonnet-4-5-20250929
   Conversation ID: abc123-def456-...
   Persistence dir: /path/to/.conversations

📋 Phase 0: Creating Work Effort...
✅ Phase 0 complete

📡 Phase 1: Generating FastAPI Server...
✅ Phase 1 complete

💾 Conversation state saved to:
   /path/to/.conversations/abc123-def456-...
```

**Note the Conversation ID!**

---

### Step 2: Resume Later

```bash
python scripts/generate_tavern_game_with_skills.py --resume abc123-def456-...
```

**Output**:
```
🔄 Resuming conversation: abc123-def456-...
   Persistence dir: /path/to/.conversations

✅ Conversation state restored from disk
   Continuing from saved state...

🖥️  Phase 2: Generating Electron App...
✅ Phase 2 complete
```

**Agent remembers Phase 0 and Phase 1!**

---

### Step 3: List Conversations

```bash
python scripts/generate_tavern_game_with_skills.py --list
```

**Output**:
```
Found 3 saved conversation(s):

  abc123-def456-...
    Created: 2026-01-14T20:30:00Z
    Status: idle

  def456-ghi789-...
    Created: 2026-01-14T19:00:00Z
    Status: idle

  ghi789-jkl012-...
    Created: 2026-01-14T18:00:00Z
    Status: running
```

---

## Benefits for Game Development

### 1. Context Preservation

**Without Persistence**:
- Agent forgets previous work
- Must re-explain context
- Loses generated code knowledge

**With Persistence**:
- ✅ Agent remembers all previous work
- ✅ Full context preserved
- ✅ Seamless continuation

---

### 2. Flexible Workflow

**Multi-session development**:
- Generate server in morning
- Generate Electron app in afternoon
- Generate tests in evening
- All in same conversation context!

---

### 3. Error Recovery

**Interruption handling**:
- Network issues? Resume later
- Crash? Resume from saved state
- Manual pause? Resume when ready

---

### 4. Iterative Refinement

**Refine based on feedback**:
- Generate initial code
- Test and review
- Resume conversation
- Request improvements
- Agent has full context!

---

## Best Practices

### 1. Store Conversation IDs

**For important workflows**, store conversation IDs:

```python
# Save ID to file
with open(".conversation_id", "w") as f:
    f.write(str(conversation_id))

# Later, load ID
with open(".conversation_id") as f:
    conversation_id = uuid.UUID(f.read().strip())
```

---

### 2. Use Project-Specific Directory

**Use project-specific persistence directory**:

```python
persistence_dir = project_root / ".conversations"
```

**Benefits**:
- Per-project state
- Easy to clean up
- Version control friendly (add to .gitignore)

---

### 3. Clean Up Old Conversations

**Periodically clean up**:

```bash
# List conversations
python scripts/generate_tavern_game_with_skills.py --list

# Delete old ones manually
rm -rf .conversations/<old-conversation-id>
```

---

### 4. Version Control

**Add to .gitignore**:

```gitignore
# OpenHands conversation state
.conversations/
*.conversation_id
```

**Why**: Conversation state may contain secrets or large files

---

## Integration with Other Features

### Persistence + Skills

**Skills are persisted**:
- Activated skills are saved
- Restored conversations have same skills
- Context-aware behavior preserved

---

### Persistence + MCP

**MCP configuration is persisted**:
- MCP servers are saved
- Tool access is preserved
- Seamless continuation

---

### Persistence + Tools

**Tool outputs are persisted**:
- File edits are saved
- Terminal outputs are saved
- Full execution history preserved

---

## Troubleshooting

### State Not Found

**Error**: Conversation state not found

**Solution**:
- Check conversation ID is correct
- Check persistence directory exists
- Verify state files are present

---

### State Corrupted

**Error**: Cannot restore state

**Solution**:
- Check `base_state.json` is valid JSON
- Check event files are readable
- Try starting fresh conversation

---

### Large State Files

**Issue**: State files are very large

**Solution**:
- This is normal for long conversations
- Consider splitting into multiple conversations
- Clean up old conversations

---

## Next Steps

1. **Test Persistence**:
   ```bash
   python scripts/generate_tavern_game_with_skills.py
   # Note conversation ID
   # Resume later
   ```

2. **Use Multi-Session Workflow**:
   - Generate server in one session
   - Generate Electron app in another
   - All with same conversation context

3. **Iterative Refinement**:
   - Generate initial code
   - Test and review
   - Resume and refine

---

## Conclusion

**Persistence enables**:
- ✅ Multi-session workflows
- ✅ Interruption recovery
- ✅ Iterative refinement
- ✅ Long-running tasks
- ✅ Context preservation

**This is essential for complex, multi-phase development!**

---

**Persistence Guide Complete**: 2026-01-14 20:30:00