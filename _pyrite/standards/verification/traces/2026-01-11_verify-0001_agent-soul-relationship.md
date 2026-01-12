# Verification Trace: Agent-Soul Relationship

**Date**: 2026-01-11 16:09:07 PST
**Check ID**: verify-0001
**Status**: ✅ Verified

## Claim
Agents need to be mapped to souls to enforce capability restrictions. Assumed we need to add `soul_id` to AgentState/AgentConfig.

## Verification Method
1. Examined `AgentState` class in `src/waft/core/agent/state.py`
2. Examined `AgentConfig` class in same file
3. Examined `Lifetime` class in `src/waft/karma_market.py`
4. Examined `KarmaMerchant.reincarnate()` method in `src/waft/karma.py`
5. Searched for existing agent-soul mapping patterns

## Evidence

### AgentState Structure
```python
class AgentState(BaseModel):
    agent_id: str = Field(description="Unique agent identifier")
    role: str = Field(description="Agent role")
    goal: str = Field(description="Primary objective")
    tools: List[ToolDefinition] = Field(default_factory=list)
    # NO soul_id field exists
```

### AgentConfig Structure
```python
class AgentConfig(BaseModel):
    agent_id: Optional[str] = Field(default=None)
    role: str = Field(description="Agent role")
    goal: str = Field(description="Primary objective")
    tools: List[ToolDefinition] = Field(default_factory=list)
    # NO soul_id field exists
```

### Lifetime Structure
```python
class Lifetime:
    def __init__(
        self,
        lifetime_id: str,
        soul_id: str,  # ✅ Has soul_id
        # ... other fields
    ):
        self.soul_id = soul_id
        # NO agent_id field
```

### KarmaMerchant.reincarnate() Method
```python
def reincarnate(
    self,
    soul_id: str,
    purchase_order: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Returns:
        Dictionary containing:
            - agent_config: Configuration for new agent instance
            - karma_remaining: Karma balance after purchase
            - lifetime_id: New lifetime identifier
    """
    # TODO: Implement reincarnation
    pass
```

**Note**: This method is the bridge - it takes `soul_id` and returns `agent_config`, but the connection is not persisted.

## Result

**FINDING**: 
- ✅ Agents do NOT have `soul_id` field
- ✅ Lifetimes have `soul_id` but NOT `agent_id`
- ✅ The connection exists conceptually via `KarmaMerchant.reincarnate()` but is not persisted
- ⚠️ **GAP**: No persistent mapping between agent_id and soul_id

**VERIFICATION**: Assumption is **PARTIALLY CORRECT**
- We DO need to add `soul_id` to AgentConfig/AgentState
- OR we need to map via active lifetime (agent → active_lifetime → soul_id)
- OR we need to store the mapping in a registry

## Recommendation

**Option A (Recommended)**: Add `soul_id` to `AgentConfig` and `AgentState`
- Set when agent is created from lifetime
- Direct, explicit relationship
- Easy to query

**Option B**: Map via active lifetime
- Query active lifetime for agent's lifetime_id
- Get soul_id from lifetime
- More indirect, requires lifetime lookup

**Option C**: Create agent-soul mapping registry
- Store mapping separately
- More complex, another system to maintain

## Next Verification
- Check how agents are currently created from lifetimes
- Verify if there's any existing agent-soul mapping
