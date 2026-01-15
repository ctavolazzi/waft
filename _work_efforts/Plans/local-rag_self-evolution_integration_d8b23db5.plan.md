---
name: Local-RAG Self-Evolution Integration
overview: Integrate local-rag into WAFT so agents can ingest their own codebase/documentation, query their knowledge to understand how to improve, experiment with different approaches, and evolve themselves based on learned patterns. This enables meta-evolutionary capabilities where agents learn from their own code to evolve.
todos:
  - id: study-local-rag
    content: Clone and study local-rag repository structure, understand architecture and components
    status: pending
  - id: create-rag-core
    content: Create RAG engine wrapper (src/waft/rag/rag_engine.py) with file-based vector store
    status: pending
  - id: implement-ingestion
    content: Implement knowledge ingestion pipeline for WAFT codebase, docs, work efforts, evolutionary history
    status: pending
  - id: integrate-agent-observe
    content: Add RAG query capability to BaseAgent.observe() method
    status: pending
  - id: enhance-study-gym
    content: Enhance Study Gym to query RAG before experiments and store results
    status: pending
  - id: integrate-evolution
    content: Integrate RAG into evolution system - query patterns, guide mutations, track results
    status: pending
  - id: create-experiment-command
    content: Create /experiment command for agent self-experimentation
    status: pending
  - id: create-evolve-self-command
    content: Create /evolve-self command for agent self-evolution using RAG knowledge
    status: pending
---

# Local-RAG Self-Evolution Integration Plan

## Vision

Enable WAFT agents to **experiment and evolve themselves** by:

1. **Ingesting their own knowledge** - Codebase, documentation, work efforts, evolutionary history
2. **Querying their knowledge** - Understanding patterns, successful mutations, evolutionary paths
3. **Experimenting** - Using Study Gym to test hypotheses about self-improvement
4. **Evolving** - Applying learned patterns to spawn better variants

This creates a **meta-evolutionary loop** where agents learn from their own code to improve themselves.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    WAFT Agent (BaseAgent)                     │
├─────────────────────────────────────────────────────────────┤
│  observe() → Query Local-RAG → Retrieve relevant knowledge │
│  decide() → Use knowledge to form hypotheses               │
│  act() → Experiment via Study Gym                           │
│  reflect() → Learn from results → Update knowledge base    │
│  spawn() → Evolve using learned patterns                    │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│              Local-RAG Knowledge Base                       │
├─────────────────────────────────────────────────────────────┤
│  • WAFT source code (src/waft/**)                           │
│  • Documentation (docs/**, README.md)                        │
│  • Work efforts (_work_efforts/**)                          │
│  • Evolutionary history (_pyrite/science/**)                │
│  • Study Gym results (_work_efforts/study_gym/**)           │
│  • Successful mutations and patterns                        │
└─────────────────────────────────────────────────────────────┘
```

## Integration Points

### 1. Local-RAG Core Integration

**Location**: `src/waft/rag/`

**Components**:

- `rag_engine.py` - Main RAG engine wrapper around local-rag
- `knowledge_ingestion.py` - Ingest WAFT codebase/documentation
- `vector_store.py` - Vector store management (file-based, no database)
- `query_interface.py` - Query interface for agents

**Key Features**:

- File-based vector store (aligns with WAFT's no-database philosophy)
- Support for local embeddings (Ollama, sentence-transformers)
- Automatic ingestion of WAFT knowledge sources
- Query interface that returns relevant code/docs/patterns

### 2. Agent Integration

**Location**: `src/waft/core/agent/`

**Enhancements**:

- `BaseAgent.observe()` - Query RAG for relevant knowledge
- `BaseAgent.decide()` - Use RAG knowledge to inform decisions
- `BaseAgent.reflect()` - Store learnings back to RAG
- `BaseAgent.spawn()` - Use RAG patterns to guide mutations

**New Methods**:

```python
async def query_knowledge(self, query: str, top_k: int = 5) -> List[Dict]
async def learn_from_experiment(self, experiment_result: Dict) -> None
async def find_evolutionary_patterns(self, goal: str) -> List[Dict]
```

### 3. Study Gym Enhancement

**Location**: `src/waft/study_gym.py`

**Enhancements**:

- Query RAG before forming hypotheses
- Learn from successful experiments
- Store experiment results in RAG
- Use RAG to suggest next experiments

**New Capabilities**:

- "What patterns worked for similar challenges?"
- "What mutations improved fitness in the past?"
- "What experiments should I try next?"

### 4. Evolution System Integration

**Location**: `src/waft/core/agent/base.py`, `src/waft/evolution/`

**Enhancements**:

- Query RAG for successful mutation patterns
- Learn from evolutionary history
- Guide mutations based on learned patterns
- Track which patterns lead to fitness improvements

**New Flow**:

1. Agent wants to evolve
2. Query RAG: "What mutations improved fitness?"
3. Form hypothesis based on patterns
4. Spawn variant with mutation
5. Evaluate fitness
6. Store result in RAG for future queries

## Implementation Phases

### Phase 1: Local-RAG Core (Week 1)

**Tasks**:

1. Clone and study local-rag repository structure
2. Extract core RAG components (embeddings, vector store, retrieval)
3. Create WAFT wrapper (`src/waft/rag/rag_engine.py`)
4. Implement file-based vector store (no database)
5. Support local embeddings (Ollama or sentence-transformers)

**Files to Create**:

- `src/waft/rag/__init__.py`
- `src/waft/rag/rag_engine.py`
- `src/waft/rag/knowledge_ingestion.py`
- `src/waft/rag/vector_store.py`
- `src/waft/rag/query_interface.py`

**Dependencies**:

- `sentence-transformers` or `ollama` for embeddings
- `chromadb` or `faiss` for vector storage (file-based)
- `langchain` components (text splitters, loaders) - extract what's needed

### Phase 2: Knowledge Ingestion (Week 1-2)

**Tasks**:

1. Create ingestion pipeline for WAFT sources
2. Ingest `src/waft/**` (Python code)
3. Ingest `docs/**` (Documentation)
4. Ingest `_work_efforts/**` (Work efforts, markdown)
5. Ingest `_pyrite/science/**` (Evolutionary history, JSONL)
6. Ingest `README.md`, `AGENTS.md`, etc.

**Files to Create**:

- `src/waft/rag/ingestion/__init__.py`
- `src/waft/rag/ingestion/code_loader.py`
- `src/waft/rag/ingestion/docs_loader.py`
- `src/waft/rag/ingestion/work_efforts_loader.py`
- `src/waft/rag/ingestion/evolution_loader.py`

**Chunking Strategy**:

- Code: Function/class level chunks with context
- Docs: Section-level chunks
- Work efforts: Ticket-level chunks
- Evolution: Event-level chunks

### Phase 3: Agent Integration (Week 2)

**Tasks**:

1. Add RAG query to `BaseAgent.observe()`
2. Enhance `BaseAgent.decide()` with RAG context
3. Add `BaseAgent.query_knowledge()` method
4. Add `BaseAgent.learn_from_experiment()` method
5. Store agent learnings in RAG

**Files to Modify**:

- `src/waft/core/agent/base.py`
- `src/waft/core/agent/state.py` (add RAG context to state)

**New Agent Capabilities**:

- "How do I improve my fitness score?"
- "What mutations worked for similar agents?"
- "What patterns exist in successful evolutions?"

### Phase 4: Study Gym Integration (Week 2-3)

**Tasks**:

1. Enhance Study Gym to query RAG before experiments
2. Store experiment results in RAG
3. Use RAG to suggest next experiments
4. Learn from successful experiments

**Files to Modify**:

- `src/waft/study_gym.py`

**New Study Gym Flow**:

1. Receive challenge
2. Query RAG: "What worked for similar challenges?"
3. Form hypothesis based on RAG + observations
4. Test hypothesis
5. Store results in RAG
6. Use results to inform next experiments

### Phase 5: Evolution Integration (Week 3)

**Tasks**:

1. Query RAG for successful mutation patterns
2. Guide mutations based on learned patterns
3. Track which patterns improve fitness
4. Store evolutionary learnings in RAG

**Files to Modify**:

- `src/waft/core/agent/base.py` (spawn method)
- `src/waft/evolution/` (evolution patterns)

**New Evolution Flow**:

1. Agent decides to evolve
2. Query RAG: "What mutations improved fitness?"
3. Select mutation pattern based on RAG results
4. Spawn variant with mutation
5. Evaluate fitness
6. Store result: "Mutation X improved fitness by Y"

### Phase 6: Self-Experimentation Command (Week 3-4)

**Tasks**:

1. Create `/experiment` command for agents
2. Create `/evolve-self` command for self-evolution
3. Integrate with Study Gym
4. Enable agents to experiment on themselves

**Files to Create**:

- `.cursor/commands/experiment.md`
- `.cursor/commands/evolve-self.md`
- `src/waft/cli/experiment_cli.py`
- `src/waft/cli/evolve_self_cli.py`

**Commands**:

- `/experiment [hypothesis]` - Agent experiments with hypothesis
- `/evolve-self [goal]` - Agent evolves itself toward goal using RAG knowledge

## Technical Details

### Vector Store Choice

**Option 1: FAISS (File-based)**

- ✅ No database, file-based
- ✅ Fast similarity search
- ✅ Aligns with WAFT philosophy
- ⚠️ Requires manual index management

**Option 2: ChromaDB (File-based)**

- ✅ Simple API
- ✅ File-based persistence
- ✅ Good for prototyping
- ⚠️ Adds dependency

**Recommendation**: Start with FAISS (file-based), can migrate to ChromaDB if needed.

### Embedding Model

**Option 1: sentence-transformers (local)**

- ✅ Fully local, no API calls
- ✅ Good performance
- ✅ Works offline

**Option 2: Ollama (local)**

- ✅ Fully local
- ✅ Can use same model for embeddings + generation
- ⚠️ Requires Ollama running

**Recommendation**: Use `sentence-transformers` with `all-MiniLM-L6-v2` (lightweight, fast).

### Knowledge Sources Priority

1. **High Priority**:

   - `src/waft/core/agent/base.py` (agent evolution logic)
   - `src/waft/study_gym.py` (experimentation patterns)
   - `docs/designs/002_agent_interface.md` (agent architecture)
   - `_pyrite/science/**` (evolutionary history)

2. **Medium Priority**:

   - `src/waft/**` (all source code)
   - `docs/**` (all documentation)
   - `_work_efforts/**` (work efforts)

3. **Low Priority**:

   - Examples, tests (can add later)

## Success Criteria

1. ✅ Agents can query their own codebase/documentation
2. ✅ Agents can learn from evolutionary history
3. ✅ Agents can experiment with self-improvement
4. ✅ Agents can evolve using learned patterns
5. ✅ System is file-based (no database)
6. ✅ System works offline (local embeddings)

## Risks & Mitigations

**Risk 1**: Local-rag dependencies conflict with WAFT

- **Mitigation**: Extract only needed components, create minimal wrapper

**Risk 2**: Vector store size grows too large

- **Mitigation**: Implement chunking strategy, periodic cleanup of old data

**Risk 3**: Embeddings are slow

- **Mitigation**: Use lightweight model, cache embeddings, async processing

**Risk 4**: Agents generate poor mutations from RAG

- **Mitigation**: Combine RAG results with fitness evaluation, validate mutations

## Next Steps

1. Clone and study local-rag repository
2. Create work effort for tracking
3. Implement Phase 1 (RAG core)
4. Test with simple agent query
5. Iterate through phases

This integration will enable WAFT agents to truly **learn from themselves** and **evolve based on their own knowledge** - creating a meta-evolutionary system where agents improve by understanding their own code and history.