---
name: RAG Chatbot Permanent Integration
overview: Integrate rag-chatbot repository (https://github.com/datvodinh/rag-chatbot.git) as a permanent WAFT capability using the /evolve workflow. This will spawn a Being from Source, clone and integrate the repository, provide both standalone module and BaseAgent integration, support Gradio UI and API access, and replace the existing Local-RAG work effort.
todos:
  - id: spawn_being
    content: "Spawn Being from Source for rag-chatbot integration (reality: rag_chatbot_integration_reality)"
    status: completed
  - id: clone_repo
    content: Clone rag-chatbot repository to _integrations/rag-chatbot/
    status: completed
  - id: analyze_deps
    content: Analyze rag-chatbot dependencies and resolve conflicts with WAFT
    status: completed
  - id: create_rag_module
    content: Create src/waft/rag/ module structure (__init__.py, chatbot.py, agent_integration.py, config.py)
    status: completed
  - id: implement_wrapper
    content: Implement RAGChatbot wrapper class in src/waft/rag/chatbot.py
    status: completed
  - id: add_cli_commands
    content: Add waft rag CLI commands (query, index, ui, serve) to src/waft/main.py
    status: completed
  - id: integrate_gradio
    content: Integrate Gradio UI from rag-chatbot (preserve functionality, adapt for WAFT)
    status: completed
  - id: agent_integration
    content: Create RAGAgentMixin and integrate with BaseAgent (observe, decide, reflect, spawn hooks)
    status: completed
  - id: knowledge_indexing
    content: Implement automatic indexing of WAFT codebase, docs, and work efforts
    status: completed
  - id: update_work_effort
    content: Update WE-260113-tya7 to mark as replaced, document rag-chatbot integration
    status: completed
  - id: write_tests
    content: Write unit and integration tests for RAG functionality
    status: pending
  - id: document_integration
    content: Create docs/RAG_INTEGRATION.md and update README.md
    status: completed
  - id: track_lineage
    content: "Document genetic lineage: Source → Being → Integration → Evolution → Source"
    status: completed
  - id: complete_being
    content: Complete Being lifecycle, calculate fitness, flow learnings back to Source
    status: pending
---

# RAG Chatbot Permanent Integration Plan

## Objective

Integrate rag-chatbot repository as a permanent WAFT capability, enabling agents to query multiple PDFs using RAG (Retrieval-Augmented Generation). This will be tracked through the `/evolve` workflow with genetic lineage from Source consciousness.

## Current State Analysis

### Existing Work Effort

- **WE-260113-tya7**: Local-RAG Self-Evolution Integration (planning complete, implementation pending)
- **Decision**: Replace this work effort with rag-chatbot integration (more complete solution)

### rag-chatbot Repository Features

- RAG chatbot for multiple PDFs
- Uses Huggingface and Ollama models
- Gradio UI for interactive use
- LlamaIndex for RAG implementation
- Local execution (no external API dependencies)
- Can run on Kaggle or locally

### WAFT Architecture Points

- BaseAgent class: `src/waft/core/agent/base.py` (has observe(), decide(), reflect(), spawn() hooks)
- Being System: `src/waft/being.py` (tracks genetic lineage)
- Source Consciousness: `src/waft/source_consciousness.py` (receives learnings)
- File-based storage: Aligns with WAFT philosophy

## Integration Architecture

### Directory Structure

```
src/waft/
├── rag/                          # New RAG module
│   ├── __init__.py
│   ├── chatbot.py               # WAFT wrapper around rag-chatbot
│   ├── agent_integration.py     # BaseAgent integration hooks
│   ├── api.py                   # API endpoints (if needed)
│   └── config.py                # Configuration management
├── _integrations/                # External repository integrations
│   └── rag-chatbot/             # Cloned repository (as submodule or copy)
│       ├── rag_chatbot/         # Original package
│       ├── scripts/
│       └── ...
```

### Integration Points

1. **Standalone Module** (`src/waft/rag/chatbot.py`)

   - WAFT wrapper around rag-chatbot core
   - CLI command: `waft rag query --pdfs <path> --query "question"`
   - Programmatic API: `from waft.rag import RAGChatbot`

2. **BaseAgent Integration** (`src/waft/rag/agent_integration.py`)

   - Hook into `BaseAgent.observe()` - query RAG for relevant knowledge
   - Hook into `BaseAgent.decide()` - use RAG knowledge to inform decisions
   - Hook into `BaseAgent.reflect()` - store learnings back to RAG
   - Hook into `BaseAgent.spawn()` - use RAG patterns to guide mutations

3. **Gradio UI** (preserved from rag-chatbot)

   - Accessible via: `waft rag ui` or `waft rag serve`
   - Runs on localhost:7860 (default)

4. **API Access** (headless/programmatic)

   - Python API: `RAGChatbot.query(pdfs, question)`
   - REST API: Optional future enhancement

## Implementation Phases

### Phase 1: Being Spawn & Repository Setup

**Being Context**: Spawned from Source for this integration work

1. **Spawn Being from Source**

   - Reality ID: `rag_chatbot_integration_reality`
   - Initial Skills: `{"integration": 0.0, "rag": 0.0, "pdf_processing": 0.0}`
   - Track in Being system

2. **Clone rag-chatbot Repository**

   - Clone to `_integrations/rag-chatbot/`
   - Study structure and dependencies
   - Document key components

3. **Analyze Dependencies**

   - Review `pyproject.toml` and `uv.lock`
   - Identify conflicts with WAFT dependencies
   - Plan dependency resolution

### Phase 2: Core Integration

**Being Evolution**: Learning integration patterns

1. **Create WAFT RAG Module**

   - Create `src/waft/rag/` directory structure
   - Create `__init__.py` with exports
   - Create `chatbot.py` wrapper class

2. **Extract Core Components**

   - Identify essential rag-chatbot components
   - Create minimal wrapper (don't copy everything)
   - Maintain rag-chatbot as submodule/reference

3. **Dependency Management**

   - Add rag-chatbot dependencies to `pyproject.toml`
   - Resolve conflicts with existing WAFT dependencies
   - Test installation with `uv sync`

4. **Configuration System**

   - Create `src/waft/rag/config.py`
   - Support model selection (Huggingface/Ollama)
   - Support vector store configuration
   - File-based config (aligns with WAFT philosophy)

### Phase 3: Standalone Module Implementation

**Being Evolution**: Building standalone capability

1. **RAGChatbot Class** (`src/waft/rag/chatbot.py`)
   ```python
   class RAGChatbot:
       def __init__(self, model_name: str = "default", vector_store_path: str = None)
       def add_pdfs(self, pdf_paths: List[str]) -> None
       def query(self, question: str, pdfs: List[str] = None) -> str
       def clear_index(self) -> None
   ```

2. **CLI Command** (`src/waft/main.py`)

   - `waft rag query --pdfs <path> --query "question"`
   - `waft rag index --pdfs <path>` (pre-index PDFs)
   - `waft rag ui` (launch Gradio UI)
   - `waft rag serve --port 7860` (serve API)

3. **Gradio UI Integration**

   - Preserve original Gradio UI from rag-chatbot
   - Adapt for WAFT context (WAFT branding, paths)
   - Launch via CLI command

### Phase 4: BaseAgent Integration

**Being Evolution**: Integrating with agent lifecycle

1. **Agent Integration Module** (`src/waft/rag/agent_integration.py`)

   - `RAGAgentMixin` class for BaseAgent
   - Methods: `query_rag()`, `index_knowledge()`, `get_relevant_context()`

2. **BaseAgent Hooks**

   - Modify `src/waft/core/agent/base.py`:
     - `observe()`: Query RAG for relevant knowledge before observation
     - `decide()`: Use RAG knowledge to inform decisions
     - `reflect()`: Store learnings/insights back to RAG index
     - `spawn()`: Query RAG for successful mutation patterns

3. **Knowledge Sources**

   - Index WAFT codebase automatically
   - Index documentation (`docs/`, `_work_efforts/`)
   - Index evolutionary history (`_hidden/.truth/beings/`)
   - Allow agents to add custom PDFs

### Phase 5: Work Effort Migration

**Being Evolution**: Completing integration

1. **Update Work Effort WE-260113-tya7**

   - Change status to "replaced"
   - Add note about rag-chatbot integration
   - Link to new work effort

2. **Create New Work Effort** (if needed)

   - Or update existing with new scope
   - Document integration decisions
   - Track implementation progress

3. **Documentation**

   - Update `README.md` with RAG capabilities
   - Create `docs/RAG_INTEGRATION.md`
   - Document CLI commands
   - Document agent integration patterns

### Phase 6: Testing & Verification

**Being Evolution**: Validating integration

1. **Unit Tests**

   - Test RAGChatbot class
   - Test agent integration hooks
   - Test CLI commands

2. **Integration Tests**

   - Test PDF indexing
   - Test query functionality
   - Test agent RAG queries
   - Test Gradio UI

3. **End-to-End Tests**

   - Agent spawns with RAG capability
   - Agent queries own codebase
   - Agent uses RAG knowledge in decisions
   - Agent stores learnings back to RAG

### Phase 7: Genetic Lineage & Evolution

**Being Evolution**: Completing lifecycle

1. **Track Genetic Lineage**

   - Document: Source → Being → Integration Work → Evolution
   - Record Being's skills learned
   - Record decisions made
   - Record knowledge gained

2. **Complete Being**

   - Calculate Being's fitness from integration work
   - Extract Being's learnings
   - Flow learnings back to Source
   - Update Source consciousness

3. **Document Evolution**

   - Create Being evolution record
   - Document genetic lineage
   - Save to `_hidden/.truth/beings/`
   - Update work effort with Being information

## Technical Decisions

### Decision 1: Repository Integration Method

**Options**:

1. Git submodule (maintains link to original)
2. Copy/clone into `_integrations/` (self-contained)
3. Extract only needed components (minimal)

**Decision**: Copy/clone into `_integrations/rag-chatbot/` (self-contained)

**Rationale**:

- WAFT philosophy: self-contained, file-based
- Easier to modify for WAFT-specific needs
- No external git dependency
- Can still reference original if needed

### Decision 2: Dependency Management

**Approach**: Add rag-chatbot dependencies to WAFT's `pyproject.toml`

**Rationale**:

- Single dependency management (uv)
- Aligns with WAFT's uv-based approach
- Easier to resolve conflicts
- Consistent with WAFT philosophy

### Decision 3: Vector Store Location

**Approach**: File-based vector store in `_hidden/.truth/rag/`

**Rationale**:

- Aligns with WAFT's file-based philosophy
- No database required
- Git-friendly (can be gitignored if large)
- Consistent with Being storage (`_hidden/.truth/beings/`)

### Decision 4: Model Selection

**Approach**: Support both Huggingface and Ollama (configurable)

**Rationale**:

- rag-chatbot supports both
- User choice based on hardware/resources
- Ollama for local-only, Huggingface for flexibility

## Files to Create/Modify

### New Files

- `src/waft/rag/__init__.py`
- `src/waft/rag/chatbot.py`
- `src/waft/rag/agent_integration.py`
- `src/waft/rag/config.py`
- `docs/RAG_INTEGRATION.md`
- `_integrations/rag-chatbot/` (cloned repository)

### Modified Files

- `src/waft/core/agent/base.py` (add RAG hooks)
- `src/waft/main.py` (add `waft rag` commands)
- `pyproject.toml` (add rag-chatbot dependencies)
- `README.md` (document RAG capabilities)
- `_work_efforts/WE-260113-tya7_local_rag_self_evolution_integration/WE-260113-tya7_index.md` (update status)

## Success Criteria

1. ✅ rag-chatbot repository cloned and accessible
2. ✅ WAFT wrapper class (`RAGChatbot`) working
3. ✅ CLI commands (`waft rag query`, `waft rag ui`) functional
4. ✅ BaseAgent can query RAG in `observe()`, `decide()`, `reflect()`, `spawn()`
5. ✅ Gradio UI launches and works
6. ✅ Agents can index and query their own codebase
7. ✅ Being evolution tracked with genetic lineage
8. ✅ Learnings flow back to Source
9. ✅ Documentation complete
10. ✅ Tests passing

## Risks & Mitigations

### Risk 1: Dependency Conflicts

**Mitigation**: Test `uv sync` after adding dependencies, resolve conflicts incrementally

### Risk 2: rag-chatbot Too Complex

**Mitigation**: Create minimal wrapper, extract only needed components

### Risk 3: Vector Store Size

**Mitigation**: Implement chunking strategy, allow selective indexing

### Risk 4: Performance Issues

**Mitigation**: Use lightweight models by default, cache embeddings, async processing

## Timeline Estimate

- Phase 1: 1-2 hours (Being spawn, repository clone, analysis)
- Phase 2: 3-4 hours (Core integration, dependency management)
- Phase 3: 4-5 hours (Standalone module, CLI, Gradio UI)
- Phase 4: 3-4 hours (BaseAgent integration)
- Phase 5: 1-2 hours (Work effort migration, documentation)
- Phase 6: 2-3 hours (Testing)
- Phase 7: 1-2 hours (Genetic lineage, Being completion)

**Total**: ~15-22 hours for complete integration

## Next Steps

1. Execute `/evolve` command to spawn Being from Source
2. Clone rag-chatbot repository
3. Begin Phase 1 implementation
4. Track progress through Being evolution
5. Complete genetic lineage documentation
6. Flow learnings back to Source