# Verification Trace: Tool System Structure

**Date**: 2026-01-11 16:09:07 PST
**Check ID**: verify-0002
**Status**: ✅ Verified

## Claim
Tools are defined as `ToolDefinition` objects. Assumed we need to create a tool registry for capability categorization.

## Verification Method
1. Examined `ToolDefinition` class in `src/waft/core/agent/state.py`
2. Searched for tool registration patterns
3. Examined how tools are used in Lifetime class
4. Searched for existing tool registries

## Evidence

### ToolDefinition Structure
```python
class ToolDefinition(BaseModel):
    """Tool definition for agent capabilities."""
    name: str
    description: str
    parameters: Dict[str, Any]  # JSON Schema
    handler: Optional[Any] = None  # Callable or tool instance
    # NO category field
    # NO capability_requirements field
```

### Tools in AgentState
```python
class AgentState(BaseModel):
    tools: List[ToolDefinition] = Field(default_factory=list)
```

### Tools in AgentConfig
```python
class AgentConfig(BaseModel):
    tools: List[ToolDefinition] = Field(default_factory=list)
```

### Tools in Lifetime
```python
class Lifetime:
    def __init__(
        self,
        tools: List[str],  # ⚠️ Just strings, not ToolDefinition objects
        # ...
    ):
        self.tools = tools  # List of tool names as strings
```

### Search Results
- No existing tool registry found
- No tool categorization system found
- Tools are just strings in Lifetime, ToolDefinition objects in Agent

## Result

**FINDING**:
- ✅ Tools are `ToolDefinition` objects in Agent system
- ✅ Tools are just `List[str]` (names) in Lifetime
- ❌ **NO tool registry exists**
- ❌ **NO tool categorization system exists**
- ❌ **NO category metadata in ToolDefinition**

**VERIFICATION**: Assumption is **CORRECT**
- We DO need to create a tool registry
- We DO need to add categorization to tools
- We need to decide: categorize ToolDefinition objects or tool name strings?

## Recommendation

**Create Tool Registry System**:
1. Create `ToolRegistry` class in `src/waft/soul_capabilities.py`
2. Register tools with:
   - `tool_name: str`
   - `category: str` ("spacetime" or "consciousness")
   - `required_state: SoulState` (ALIVE or DEAD)
3. Default-deny: Tools not registered are blocked
4. Add decorator for automatic registration:
   ```python
   @register_tool(category="spacetime", required_state=SoulState.ALIVE)
   def read_file(...):
       ...
   ```

## Next Verification
- Check how tools are currently called/executed
- Verify if there's a central tool execution point
