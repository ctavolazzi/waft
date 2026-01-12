# Quick Exploration: Integration Points

**Date**: 2026-01-11 16:17:00 PST
**Purpose**: Identify critical integration points for reincarnation system
**Status**: ✅ Complete

---

## Key Findings

### 1. BaseAgent Tool Execution
- **Abstract Class**: BaseAgent is abstract with abstract methods (observe, decide, act, reflect)
- **Tool Storage**: Tools stored as `ToolDefinition` objects in `agent.state.tools`
- **Tool Handler**: `ToolDefinition.handler` field contains callable function
- **Execution Path**: Tools executed through abstract OODA cycle (observe → decide → act → reflect)
- **Integration Point**: Need to filter `agent.state.tools` before LLM sees them, AND add decorators to tool handlers

### 2. GoalManager Structure
- **Location**: `src/waft/core/goal.py`
- **Methods**: `create_goal()`, `update_goal()`, `delete_goal()`
- **Integration Point**: Add soul state checks at start of each method
- **Context**: Methods don't currently take soul_id - need to add parameter or get from context

### 3. KarmaCollector File Operations
- **Location**: `src/waft/karma_collector.py`
- **Method**: `_transfer_karma_to_soul()` - writes soul files
- **File Permissions**: ❌ NOT SET (grep found no chmod calls)
- **Integration Point**: Add `soul_file.chmod(0o600)` after file write
- **Directory Permissions**: Add `akasha_path.chmod(0o700)` after directory creation

### 4. Lifetime Class
- **Location**: `src/waft/karma_market.py`
- **Has soul_id**: ✅ Already has `soul_id` field
- **Integration Point**: Add `soul_state` field, connect to SoulStateManager
- **State Transitions**: Lifetime start → ALIVE_AWAKE, Lifetime end → DEAD_AWAKE

### 5. AgentState/AgentConfig
- **Location**: `src/waft/core/agent/state.py`
- **Missing**: ❌ NO `soul_id` field in either class
- **Integration Point**: Add `soul_id: Optional[str]` to both classes
- **Set When**: During agent creation from lifetime (in `reincarnate()`)

---

## Implementation Notes

### Tool Execution Strategy
1. **LLM Interface Filtering**: Filter `ToolDefinition` objects from `agent.state.tools` before passing to LLM
2. **Tool Handler Decorators**: Add `@require_capability()` decorator to all tool handler functions
3. **Middleware Layer**: Add capability check in BaseAgent before tool execution
4. **Tool Registry**: Create registry to categorize tools and check permissions

### File Permissions Strategy
1. **New Files**: Set 0600 on creation (in KarmaCollector, SoulStateManager)
2. **Directories**: Set 0700 on creation (akasha directory)
3. **Migration**: Update all existing soul files during migration script

### State Transition Strategy
1. **Order Matters**: Transition soul to ALIVE_AWAKE BEFORE creating agent
2. **Atomic Operations**: Use file locks for state transitions
3. **Validation**: Validate state before and after transitions

---

**Status**: ✅ Ready to begin Step 0 (Demo Environment)
