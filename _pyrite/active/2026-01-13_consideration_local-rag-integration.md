# Consideration: Local-RAG Self-Evolution Integration

**Date**: 2026-01-13 09:33:22 PST  
**Work Effort**: WE-260113-tya7  
**Status**: Analysis Complete

---

## Situation Analysis

### Current State
- **WAFT System**: Self-modifying AI agent framework with evolution capabilities
- **BaseAgent**: Core agent class with observe(), decide(), act(), reflect(), spawn() methods
- **Study Gym**: Scientific method workflow for experimentation (OBSERVE → QUESTION → HYPOTHESIZE → TEST → ANALYZE → CONCLUDE)
- **Evolution System**: Agents can spawn variants and evolve based on fitness
- **Knowledge Sources**: Codebase (`src/waft/**`), documentation (`docs/**`), work efforts (`_work_efforts/**`), evolutionary history (`_pyrite/science/**`)

### Goal
Enable WAFT agents to **experiment and evolve themselves** by:
1. Ingesting their own knowledge (codebase, docs, work efforts, history)
2. Querying that knowledge to understand patterns and successful mutations
3. Experimenting via Study Gym to test self-improvement hypotheses
4. Evolving by applying learned patterns to spawn better variants

This creates a **meta-evolutionary loop** where agents learn from their own code to improve themselves.

---

## Options Analysis

### Option 1: Full Local-RAG Integration (Recommended)
**Approach**: Clone and integrate local-rag repository, create WAFT wrapper

**Pros**:
- ✅ Complete RAG functionality out of the box
- ✅ Proven implementation
- ✅ Can extract only needed components
- ✅ File-based vector store aligns with WAFT philosophy

**Cons**:
- ⚠️ Need to study and adapt external codebase
- ⚠️ Potential dependency conflicts
- ⚠️ May need to extract minimal components

**Effort**: Medium-High (2-3 weeks)
**Risk**: Medium (dependency management)

---

### Option 2: Build Custom RAG from Scratch
**Approach**: Implement RAG components directly in WAFT

**Pros**:
- ✅ Full control over implementation
- ✅ No external dependencies
- ✅ Tailored to WAFT's needs
- ✅ Aligns with WAFT's self-contained philosophy

**Cons**:
- ❌ Significant development effort
- ❌ Reinventing the wheel
- ❌ More time to production

**Effort**: High (4-6 weeks)
**Risk**: Low (no external dependencies)

---

### Option 3: Hybrid Approach (Recommended Alternative)
**Approach**: Study local-rag patterns, implement minimal WAFT-native version

**Pros**:
- ✅ Best of both worlds
- ✅ Learn from local-rag without full dependency
- ✅ WAFT-native implementation
- ✅ Faster than full custom build

**Cons**:
- ⚠️ Still requires significant implementation
- ⚠️ Need to understand local-rag patterns first

**Effort**: Medium (2-3 weeks)
**Risk**: Low-Medium

---

## Recommendation

**Recommended: Option 1 (Full Local-RAG Integration)**

**Rationale**:
1. **Time Efficiency**: Proven implementation saves development time
2. **File-Based**: Local-rag likely supports file-based storage (aligns with WAFT)
3. **Extract Pattern**: Can extract only needed components, create minimal wrapper
4. **Learning Opportunity**: Studying local-rag provides insights for future enhancements

**Implementation Strategy**:
1. Clone and study local-rag repository
2. Extract core components (embeddings, vector store, retrieval)
3. Create WAFT wrapper (`src/waft/rag/`)
4. Implement file-based vector store (no database)
5. Support local embeddings (sentence-transformers or Ollama)
6. Integrate with BaseAgent lifecycle methods

---

## Technical Decisions

### Vector Store: FAISS (File-Based)
- ✅ No database, file-based
- ✅ Fast similarity search
- ✅ Aligns with WAFT philosophy
- ⚠️ Requires manual index management

### Embedding Model: sentence-transformers (all-MiniLM-L6-v2)
- ✅ Fully local, no API calls
- ✅ Good performance
- ✅ Works offline
- ✅ Lightweight and fast

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

---

## Implementation Phases

### Phase 1: Local-RAG Core (Week 1)
- Clone and study local-rag repository
- Extract core RAG components
- Create WAFT wrapper (`src/waft/rag/rag_engine.py`)
- Implement file-based vector store
- Support local embeddings

### Phase 2: Knowledge Ingestion (Week 1-2)
- Create ingestion pipeline for WAFT sources
- Ingest code, docs, work efforts, evolutionary history
- Implement chunking strategy

### Phase 3: Agent Integration (Week 2)
- Add RAG query to `BaseAgent.observe()`
- Enhance `BaseAgent.decide()` with RAG context
- Add `BaseAgent.query_knowledge()` method
- Store agent learnings in RAG

### Phase 4: Study Gym Integration (Week 2-3)
- Enhance Study Gym to query RAG before experiments
- Store experiment results in RAG
- Use RAG to suggest next experiments

### Phase 5: Evolution Integration (Week 3)
- Query RAG for successful mutation patterns
- Guide mutations based on learned patterns
- Track which patterns improve fitness

### Phase 6: Self-Experimentation Commands (Week 3-4)
- Create `/experiment` command
- Create `/evolve-self` command
- Integrate with Study Gym

---

## Success Criteria

1. ✅ Agents can query their own codebase/documentation
2. ✅ Agents can learn from evolutionary history
3. ✅ Agents can experiment with self-improvement
4. ✅ Agents can evolve using learned patterns
5. ✅ System is file-based (no database)
6. ✅ System works offline (local embeddings)

---

## Next Steps

1. Clone local-rag repository and study structure
2. Create work effort for tracking (✅ Done: WE-260113-tya7)
3. Implement Phase 1 (RAG core)
4. Test with simple agent query
5. Iterate through remaining phases

---

**Analysis Complete**: 2026-01-13 09:33:22 PST
