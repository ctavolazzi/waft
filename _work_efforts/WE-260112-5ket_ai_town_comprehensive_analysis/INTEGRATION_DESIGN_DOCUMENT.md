# AI-Town Integration Design Document

**Date**: 2026-01-12 22:45:00 PST  
**Work Effort**: WE-260112-5ket  
**Status**: Design Phase

---

## Executive Summary

This document outlines concrete integration patterns from ai-town into WAFT, building on the existing analysis and WAFT's current architecture. The focus is on actionable, implementable patterns that enhance WAFT's agent capabilities.

**Key Integration Areas**:
1. **Vector-Based Memory System** - Enhance existing memory with embeddings
2. **Operation System** - Async task handling for long-running operations
3. **Historical State Tracking** - Evolution visualization and replay
4. **Conversation Summarization** - Memory compression for chronicles
5. **Multi-Agent Communication** - Enhance existing inbox/outbox system

---

## Current WAFT State

### Existing Capabilities

**Agent State** (`src/waft/core/agent/state.py`):
- ✅ `memory: List[Message]` - Conversation history (AG2 protocol)
- ✅ `journal: List[Dict]` - Private journal (Thoughts and Reflections)
- ✅ `short_term_memory: List[Dict]` - Recent thoughts/reflections buffer
- ✅ `hero_state: Dict` - TavernKeeper chronicles integration
- ✅ `inbox/outbox: List[Message]` - Multi-agent communication

**BaseAgent** (`src/waft/core/agent/base.py`):
- ✅ OODA loop: `observe()`, `decide()`, `act()`, `reflect()`
- ✅ `step()` method with Thought/Reflection recording
- ✅ State management via `AgentState`
- ✅ Lineage tracking and evolution

**AI-Town Module** (`src/waft/ai_town/`):
- ✅ `memory.py` - Placeholder for vector embeddings
- ✅ `town_agent.py` - Basic agent implementation
- ⚠️ Simplified hash-based similarity (needs vector embeddings)

---

## Integration Patterns

### 1. Vector-Based Memory System

**Current State**: WAFT has `memory` (List[Message]) and `short_term_memory`, but no vector embeddings.

**ai-town Pattern**: 
- Conversation summaries stored with vector embeddings
- Top-k similarity search for memory retrieval
- Embedding cache for efficiency

**Integration Design**:

```python
# src/waft/core/memory/vector_memory.py

from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import hashlib

class MemoryEmbedding(BaseModel):
    """Memory entry with embedding."""
    id: str
    text: str  # Summary text
    embedding: List[float]  # Vector embedding
    metadata: Dict[str, Any]  # Source conversation, timestamp, etc.
    created_at: datetime

class VectorMemorySystem:
    """
    Vector-based memory system inspired by ai-town.
    
    Integrates with WAFT's existing memory structures:
    - Summarizes conversations from AgentState.memory
    - Stores in hero_state.chronicles (TavernKeeper)
    - Retrieves via similarity search
    """
    
    def __init__(self, embedding_provider: str = "openai"):
        self.embedding_provider = embedding_provider
        self.embedding_cache: Dict[str, List[float]] = {}  # Hash -> embedding
    
    def summarize_conversation(self, messages: List[Message]) -> str:
        """
        Summarize conversation for memory storage.
        Similar to ai-town's conversation summarization.
        """
        # Use LLM to create summary
        # Return compressed summary text
        pass
    
    def compute_embedding(self, text: str) -> List[float]:
        """
        Compute embedding with caching (ai-town pattern).
        """
        text_hash = hashlib.sha256(text.encode()).hexdigest()
        if text_hash in self.embedding_cache:
            return self.embedding_cache[text_hash]
        
        # Compute embedding via provider
        embedding = self._get_embedding(text)
        self.embedding_cache[text_hash] = embedding
        return embedding
    
    def remember_conversation(self, agent_state: AgentState) -> MemoryEmbedding:
        """
        Remember a conversation (ai-town pattern).
        
        1. Summarize conversation from agent_state.memory
        2. Compute embedding
        3. Store in hero_state.chronicles
        4. Return MemoryEmbedding
        """
        summary = self.summarize_conversation(agent_state.memory)
        embedding = self.compute_embedding(summary)
        
        memory_entry = MemoryEmbedding(
            id=f"mem_{datetime.now().isoformat()}",
            text=summary,
            embedding=embedding,
            metadata={
                "source": "conversation",
                "message_count": len(agent_state.memory),
                "agent_id": agent_state.agent_id
            },
            created_at=datetime.utcnow()
        )
        
        # Store in chronicles (TavernKeeper integration)
        if agent_state.hero_state is None:
            agent_state.hero_state = {}
        if "chronicles" not in agent_state.hero_state:
            agent_state.hero_state["chronicles"] = []
        
        agent_state.hero_state["chronicles"].append(memory_entry.dict())
        
        return memory_entry
    
    def retrieve_memories(self, query: str, agent_state: AgentState, top_k: int = 3) -> List[MemoryEmbedding]:
        """
        Retrieve relevant memories (ai-town pattern).
        
        1. Embed query
        2. Find top-k similar memories from chronicles
        3. Return MemoryEmbedding objects
        """
        query_embedding = self.compute_embedding(query)
        
        # Get memories from chronicles
        chronicles = agent_state.hero_state.get("chronicles", [])
        
        # Compute similarities
        similarities = []
        for mem_dict in chronicles:
            mem = MemoryEmbedding(**mem_dict)
            similarity = self._cosine_similarity(query_embedding, mem.embedding)
            similarities.append((similarity, mem))
        
        # Return top-k
        similarities.sort(reverse=True, key=lambda x: x[0])
        return [mem for _, mem in similarities[:top_k]]
    
    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Compute cosine similarity between two vectors."""
        import numpy as np
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
```

**Integration Points**:
- Extend `AgentState.hero_state["chronicles"]` with embeddings
- Add `remember_conversation()` call after significant conversations
- Use `retrieve_memories()` in `BaseAgent.observe()` to inject context

---

### 2. Operation System for Async Tasks

**Current State**: WAFT's `BaseAgent` executes synchronously in `step()`.

**ai-town Pattern**:
- `startOperation()` kicks off async Convex functions
- Operations tracked in agent state
- Timeout-based cancellation

**Integration Design**:

```python
# src/waft/core/agent/operations.py

from typing import Dict, Any, Optional, Callable
from datetime import datetime, timedelta
from enum import Enum

class OperationStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"

class Operation(BaseModel):
    """Async operation tracking (ai-town pattern)."""
    operation_id: str
    name: str
    status: OperationStatus
    started_at: datetime
    timeout_seconds: int = 300  # 5 minutes default
    args: Dict[str, Any]
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class OperationManager:
    """
    Manages async operations for agents (ai-town pattern).
    
    Separates long-running tasks from game loop.
    """
    
    def __init__(self):
        self.operations: Dict[str, Operation] = {}
    
    def start_operation(
        self,
        agent_state: AgentState,
        operation_name: str,
        operation_func: Callable,
        args: Dict[str, Any],
        timeout_seconds: int = 300
    ) -> str:
        """
        Start async operation (ai-town pattern).
        
        Returns operation_id for tracking.
        """
        operation_id = f"op_{datetime.now().isoformat()}_{operation_name}"
        
        operation = Operation(
            operation_id=operation_id,
            name=operation_name,
            status=OperationStatus.PENDING,
            started_at=datetime.utcnow(),
            timeout_seconds=timeout_seconds,
            args=args
        )
        
        self.operations[operation_id] = operation
        
        # Store in agent state (similar to ai-town's inProgressOperation)
        if "operations" not in agent_state.working_memory:
            agent_state.working_memory["operations"] = {}
        agent_state.working_memory["operations"][operation_id] = {
            "name": operation_name,
            "started": operation.started_at.isoformat(),
            "status": operation.status.value
        }
        
        # Start async execution
        self._execute_async(operation_id, operation_func, args)
        
        return operation_id
    
    def check_operation(self, operation_id: str) -> Optional[Operation]:
        """Check operation status."""
        if operation_id not in self.operations:
            return None
        
        operation = self.operations[operation_id]
        
        # Check timeout
        elapsed = (datetime.utcnow() - operation.started_at).total_seconds()
        if elapsed > operation.timeout_seconds:
            operation.status = OperationStatus.TIMEOUT
            return operation
        
        return operation
    
    def _execute_async(self, operation_id: str, func: Callable, args: Dict[str, Any]):
        """Execute operation asynchronously."""
        import asyncio
        
        async def run_operation():
            try:
                operation = self.operations[operation_id]
                operation.status = OperationStatus.IN_PROGRESS
                
                # Execute
                if asyncio.iscoroutinefunction(func):
                    result = await func(**args)
                else:
                    result = func(**args)
                
                operation.result = result
                operation.status = OperationStatus.COMPLETED
            except Exception as e:
                operation.error = str(e)
                operation.status = OperationStatus.FAILED
        
        asyncio.create_task(run_operation())
```

**Integration Points**:
- Add `OperationManager` to `BaseAgent`
- Use for long-running tasks (LLM calls, file operations, etc.)
- Check operations in `BaseAgent.step()` before proceeding

---

### 3. Historical State Tracking

**Current State**: WAFT tracks lineage but not historical state snapshots.

**ai-town Pattern**:
- Historical tables track continuous quantities
- Store value at end of each tick
- Enables smooth replay

**Integration Design**:

```python
# src/waft/core/evolution/history.py

from typing import List, Dict, Any
from datetime import datetime

class StateSnapshot(BaseModel):
    """State snapshot at a point in time (ai-town pattern)."""
    tick: int
    timestamp: datetime
    agent_state: Dict[str, Any]  # Serialized AgentState
    events: List[Dict[str, Any]]  # Events that occurred
    energy: float
    position: Optional[Dict[str, float]] = None  # For spatial agents

class EvolutionHistory:
    """
    Tracks evolution history for visualization (ai-town pattern).
    
    Similar to ai-town's historical tables.
    """
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.snapshots: List[StateSnapshot] = []
        self.current_tick = 0
    
    def record_snapshot(self, agent_state: AgentState, events: List[Dict] = None):
        """
        Record state snapshot (ai-town pattern).
        
        Called at end of each evolution step.
        """
        snapshot = StateSnapshot(
            tick=self.current_tick,
            timestamp=datetime.utcnow(),
            agent_state=agent_state.dict(),
            events=events or [],
            energy=agent_state.energy,
            position=agent_state.working_memory.get("position")
        )
        
        self.snapshots.append(snapshot)
        self.current_tick += 1
    
    def get_snapshot(self, tick: int) -> Optional[StateSnapshot]:
        """Get snapshot at specific tick."""
        if 0 <= tick < len(self.snapshots):
            return self.snapshots[tick]
        return None
    
    def get_recent_snapshots(self, count: int = 10) -> List[StateSnapshot]:
        """Get recent snapshots for visualization."""
        return self.snapshots[-count:]
    
    def export_for_visualization(self) -> Dict[str, Any]:
        """Export for visualization (similar to ai-town's client replay)."""
        return {
            "agent_id": self.agent_id,
            "snapshots": [s.dict() for s in self.snapshots],
            "total_ticks": self.current_tick
        }
```

**Integration Points**:
- Add `EvolutionHistory` to `BaseAgent`
- Call `record_snapshot()` at end of each `step()`
- Use for evolution visualization in WAFT dashboard

---

### 4. Conversation Summarization

**Current State**: WAFT stores full conversation in `AgentState.memory`.

**ai-town Pattern**:
- Summarize conversations for memory compression
- Store summaries with embeddings

**Integration Design**:

```python
# src/waft/core/memory/summarizer.py

from typing import List
from src.waft.core.agent.state import Message

class ConversationSummarizer:
    """
    Summarizes conversations for memory compression (ai-town pattern).
    """
    
    def __init__(self, llm_provider: str = "openai"):
        self.llm_provider = llm_provider
    
    def summarize(self, messages: List[Message], max_length: int = 500) -> str:
        """
        Summarize conversation (ai-town pattern).
        
        Similar to ai-town's conversation summarization after each conversation.
        """
        # Extract key information
        participants = set()
        topics = []
        
        for msg in messages:
            if hasattr(msg, 'role'):
                participants.add(msg.role)
            if hasattr(msg, 'content'):
                # Extract topics (simplified)
                topics.append(msg.content[:100])
        
        # Use LLM to create summary
        summary = self._llm_summarize(messages, max_length)
        
        return summary
    
    def _llm_summarize(self, messages: List[Message], max_length: int) -> str:
        """Use LLM to create summary."""
        # Implementation: Call LLM with messages
        # Return compressed summary
        pass
```

**Integration Points**:
- Use in `VectorMemorySystem.remember_conversation()`
- Periodically summarize `AgentState.memory` to prevent unbounded growth
- Store summaries in chronicles

---

### 5. Enhanced Multi-Agent Communication

**Current State**: WAFT has `inbox/outbox` but no conversation management.

**ai-town Pattern**:
- Distance-based conversation initiation
- Conversation memberships (invited, walkingOver, participating)
- Typing indicators

**Integration Design**:

```python
# src/waft/core/agent/conversation.py

from typing import List, Dict, Any, Optional
from enum import Enum

class ConversationStatus(str, Enum):
    INVITED = "invited"
    WALKING_OVER = "walking_over"  # For spatial agents
    PARTICIPATING = "participating"
    ENDED = "ended"

class ConversationMembership(BaseModel):
    """Conversation membership (ai-town pattern)."""
    agent_id: str
    status: ConversationStatus
    joined_at: datetime
    last_message_at: Optional[datetime] = None

class Conversation(BaseModel):
    """Multi-agent conversation (ai-town pattern)."""
    conversation_id: str
    created_by: str  # Agent ID
    memberships: List[ConversationMembership]
    messages: List[Message]
    created_at: datetime
    ended_at: Optional[datetime] = None

class ConversationManager:
    """
    Manages multi-agent conversations (ai-town pattern).
    
    Enhances WAFT's existing inbox/outbox system.
    """
    
    def __init__(self):
        self.conversations: Dict[str, Conversation] = {}
    
    def start_conversation(
        self,
        creator_id: str,
        participant_ids: List[str],
        initial_message: Optional[Message] = None
    ) -> Conversation:
        """
        Start conversation (ai-town pattern).
        """
        conversation_id = f"conv_{datetime.now().isoformat()}"
        
        memberships = [
            ConversationMembership(
                agent_id=creator_id,
                status=ConversationStatus.PARTICIPATING,
                joined_at=datetime.utcnow()
            )
        ]
        
        for participant_id in participant_ids:
            memberships.append(
                ConversationMembership(
                    agent_id=participant_id,
                    status=ConversationStatus.INVITED,
                    joined_at=datetime.utcnow()
                )
            )
        
        conversation = Conversation(
            conversation_id=conversation_id,
            created_by=creator_id,
            memberships=memberships,
            messages=[initial_message] if initial_message else [],
            created_at=datetime.utcnow()
        )
        
        self.conversations[conversation_id] = conversation
        return conversation
    
    def add_message(self, conversation_id: str, message: Message):
        """Add message to conversation."""
        if conversation_id in self.conversations:
            conv = self.conversations[conversation_id]
            conv.messages.append(message)
            
            # Update last_message_at for sender
            for membership in conv.memberships:
                if membership.agent_id == message.agent_id:
                    membership.last_message_at = datetime.utcnow()
                    break
```

**Integration Points**:
- Enhance `AgentState.inbox/outbox` with conversation management
- Use for multi-agent evolution scenarios
- Track social relationships in agent lineage

---

## Implementation Priority

### High Priority (Immediate Value)

1. **Vector-Based Memory System** ⭐
   - **Effort**: Medium (2-3 days)
   - **Value**: High - Enhances agent memory capabilities
   - **Dependencies**: Embedding provider (OpenAI, Ollama, etc.)

2. **Conversation Summarization** ⭐
   - **Effort**: Low (1 day)
   - **Value**: High - Prevents memory bloat
   - **Dependencies**: LLM provider

### Medium Priority (High Value)

3. **Operation System**
   - **Effort**: Medium (2-3 days)
   - **Value**: High - Enables async long-running tasks
   - **Dependencies**: Async infrastructure

4. **Historical State Tracking**
   - **Effort**: Medium (2-3 days)
   - **Value**: Medium - Enables visualization
   - **Dependencies**: Storage system

### Low Priority (Nice to Have)

5. **Enhanced Multi-Agent Communication**
   - **Effort**: High (3-5 days)
   - **Value**: Medium - Enhances social evolution
   - **Dependencies**: Spatial agent system (if using distance-based)

---

## Proof of Concept Scope

**Recommended POC**: Vector-Based Memory System

**Scope**:
1. Implement `VectorMemorySystem` with OpenAI embeddings
2. Integrate with `BaseAgent.step()` to remember conversations
3. Add `retrieve_memories()` to `BaseAgent.observe()` for context injection
4. Test with simple agent conversation scenario

**Success Criteria**:
- Agent can remember past conversations
- Agent can retrieve relevant memories based on query
- Memory stored in chronicles (TavernKeeper integration)
- Embedding cache working

**Estimated Time**: 2-3 days

---

## Next Steps

1. **Review & Approve Design** - Get feedback on integration patterns
2. **Create Work Effort** - Set up tracking for implementation
3. **Implement POC** - Start with Vector-Based Memory System
4. **Test & Iterate** - Validate patterns with real scenarios
5. **Expand Integration** - Add remaining patterns based on POC results

---

## References

- **ai-town Analysis**: `DEEP_ANALYSIS_AI_TOWN_AND_PAPER.md`
- **WAFT Agent State**: `src/waft/core/agent/state.py`
- **WAFT BaseAgent**: `src/waft/core/agent/base.py`
- **Existing AI-Town Module**: `src/waft/ai_town/`

---

**Status**: Design complete. Ready for review and implementation planning.
