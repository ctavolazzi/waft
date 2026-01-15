# RAG Chatbot Integration

**Date**: 2026-01-13  
**Status**: ✅ Integrated  
**Work Effort**: WE-260113-tya7

---

## Overview

WAFT now includes RAG (Retrieval-Augmented Generation) capabilities through integration with the [rag-chatbot](https://github.com/datvodinh/rag-chatbot) repository. This enables agents to query multiple PDFs using AI-powered question answering.

## Features

- **PDF Querying**: Query multiple PDFs with natural language questions
- **Model Support**: Works with Huggingface and Ollama models
- **Gradio UI**: Interactive web interface for querying PDFs
- **BaseAgent Integration**: Agents can query RAG in their lifecycle methods
- **File-Based Storage**: Vector store stored in `_hidden/.truth/rag/` (aligns with WAFT philosophy)
- **Automatic Indexing**: Can auto-index WAFT codebase, docs, and work efforts

## Installation

Dependencies are automatically installed when you run `uv sync`:

```bash
uv sync
```

The rag-chatbot repository is cloned to `_integrations/rag-chatbot/` during setup.

## Usage

### CLI Commands

#### Query PDFs
```bash
# Query a single PDF
waft rag query "What is WAFT?" --pdfs docs/welcome_packet/WAFT_WELCOME_PACKET.pdf

# Query multiple PDFs
waft rag query "How do agents work?" --pdfs docs/**,_work_efforts/briefs/**
```

#### Index PDFs
```bash
# Index a single PDF
waft rag index docs/welcome_packet/WAFT_WELCOME_PACKET.pdf

# Index all PDFs in directories
waft rag index docs/**,_work_efforts/briefs/**
```

#### Launch Gradio UI
```bash
# Launch interactive UI (default: http://0.0.0.0:7860)
waft rag ui

# Custom port and host
waft rag ui --port 8080 --host localhost
```

#### Serve API
```bash
# Same as 'ui' command
waft rag serve --port 7860
```

### Programmatic API

#### Basic Usage
```python
from waft.rag import RAGChatbot
from pathlib import Path

# Initialize chatbot
chatbot = RAGChatbot(project_path=Path.cwd())

# Add PDFs
chatbot.add_pdfs([
    "docs/welcome_packet/WAFT_WELCOME_PACKET.pdf",
    "_work_efforts/briefs/Status_Brief.pdf"
])

# Query
answer = chatbot.query("What is WAFT?")
print(answer)
```

#### Configuration
```python
from waft.rag import RAGChatbot, RAGConfig
from pathlib import Path

# Create custom config
config = RAGConfig(project_path=Path.cwd())
config.model_type = "ollama"  # or "huggingface"
config.model_name = "llama3"  # Ollama model name
config.embedding_model = "all-MiniLM-L6-v2"
config.auto_index_on_start = True
config.add_indexed_path("docs/")
config.add_indexed_path("_work_efforts/")

# Initialize with config
chatbot = RAGChatbot(config=config, project_path=Path.cwd())
```

### BaseAgent Integration

To add RAG capabilities to your BaseAgent subclass:

```python
from waft.core.agent.base import BaseAgent
from waft.rag.agent_integration import RAGAgentMixin

class MyAgent(RAGAgentMixin, BaseAgent):
    """Agent with RAG capabilities."""
    
    async def observe(self):
        # Query RAG for relevant knowledge
        rag_context = await self.observe_with_rag(super().observe)
        
        # Use rag_context in observation
        # rag_context is stored in self.state.working_memory["rag_knowledge"]
        ...
    
    async def decide(self, state: AgentState):
        # Get RAG context for decision
        rag_context = await self.decide_with_rag(state, super().decide)
        
        # Use rag_context in decision
        # rag_context is stored in state.working_memory["rag_context"]
        ...
    
    async def reflect(self, result: dict):
        # Store learnings to RAG
        await self.reflect_with_rag(result, super().reflect)
        
        # Learnings stored in self.state.working_memory["rag_learnings"]
        ...
    
    async def spawn(self, mutation):
        # Query RAG for successful patterns
        rag_patterns = await self.spawn_with_rag(mutation, super().spawn)
        
        # Patterns stored in self.state.working_memory["rag_mutation_patterns"]
        ...
```

## Architecture

### Directory Structure
```
src/waft/
├── rag/
│   ├── __init__.py              # Module exports
│   ├── chatbot.py               # RAGChatbot wrapper class
│   ├── agent_integration.py     # RAGAgentMixin for BaseAgent
│   └── config.py                # Configuration management
_integrations/
└── rag-chatbot/                 # Cloned repository
    ├── rag_chatbot/            # Original package
    └── ...
_hidden/
└── .truth/
    └── rag/                     # RAG data storage
        ├── config.json         # Configuration file
        └── vector_store/        # Vector store files
```

### Integration Points

1. **Standalone Module** (`src/waft/rag/chatbot.py`)
   - WAFT wrapper around rag-chatbot core
   - CLI commands: `waft rag query`, `waft rag index`, `waft rag ui`

2. **BaseAgent Integration** (`src/waft/rag/agent_integration.py`)
   - `RAGAgentMixin` class for BaseAgent
   - Hooks: `observe_with_rag()`, `decide_with_rag()`, `reflect_with_rag()`, `spawn_with_rag()`

3. **Gradio UI** (preserved from rag-chatbot)
   - Accessible via: `waft rag ui`
   - Runs on localhost:7860 (default)

4. **Configuration** (`src/waft/rag/config.py`)
   - File-based config in `_hidden/.truth/rag/config.json`
   - Supports model selection, vector store paths, auto-indexing

## Configuration

Configuration is stored in `_hidden/.truth/rag/config.json`:

```json
{
  "model_type": "ollama",
  "model_name": "",
  "embedding_model": "all-MiniLM-L6-v2",
  "vector_store_path": "_hidden/.truth/rag/vector_store",
  "host": "localhost",
  "language": "eng",
  "auto_index_on_start": false,
  "indexed_paths": []
}
```

### Configuration Options

- **model_type**: `"ollama"` or `"huggingface"`
- **model_name**: Model name (empty = use default)
- **embedding_model**: Sentence-transformers model for embeddings
- **vector_store_path**: Path to vector store directory
- **host**: Ollama host (default: "localhost")
- **language**: Language code (default: "eng")
- **auto_index_on_start**: Auto-index on agent startup (default: false)
- **indexed_paths**: List of paths to automatically index

## Knowledge Sources

### Automatic Indexing

Agents can automatically index knowledge sources on startup:

```python
config = RAGConfig(project_path=Path.cwd())
config.auto_index_on_start = True
config.add_indexed_path("docs/")
config.add_indexed_path("_work_efforts/")
config.add_indexed_path("_hidden/.truth/beings/")  # Evolutionary history
```

### Manual Indexing

```python
chatbot = RAGChatbot(project_path=Path.cwd())

# Index single PDF
chatbot.add_pdfs(["docs/welcome_packet/WAFT_WELCOME_PACKET.pdf"])

# Index directory
chatbot.index_path(Path("docs/"))

# Index multiple paths
chatbot.add_pdfs([
    "docs/welcome_packet/WAFT_WELCOME_PACKET.pdf",
    "_work_efforts/briefs/Status_Brief.pdf"
])
```

## Model Setup

### Ollama (Recommended for Local)

1. Install Ollama: https://ollama.com/
2. Pull a model:
   ```bash
   ollama pull llama3
   ```
3. Configure in WAFT:
   ```python
   config = RAGConfig(project_path=Path.cwd())
   config.model_type = "ollama"
   config.model_name = "llama3"
   ```

### Huggingface

Models are automatically downloaded on first use. Configure:

```python
config = RAGConfig(project_path=Path.cwd())
config.model_type = "huggingface"
config.model_name = "mistralai/Mistral-7B-Instruct-v0.2"
```

## Examples

### Example 1: Query WAFT Documentation
```bash
# Index WAFT docs
waft rag index docs/

# Query
waft rag query "How does the Being system work?"
```

### Example 2: Agent with RAG
```python
from waft.core.agent.base import BaseAgent
from waft.rag.agent_integration import RAGAgentMixin
from waft.core.agent.state import AgentState

class ResearchAgent(RAGAgentMixin, BaseAgent):
    async def observe(self):
        # Query RAG for relevant research
        query = "What research has been done on agent evolution?"
        knowledge = self.query_rag(query)
        
        # Store in working memory
        self.state.working_memory["research_context"] = knowledge
        
        return await super().observe()
```

### Example 3: Index Work Efforts
```python
from waft.rag import RAGChatbot
from pathlib import Path

chatbot = RAGChatbot(project_path=Path.cwd())

# Index all work effort briefs
chatbot.index_path(Path("_work_efforts/briefs/"))

# Query
answer = chatbot.query("What work has been done on PDF generation?")
print(answer)
```

## Troubleshooting

### Import Errors
If you get import errors, ensure rag-chatbot is cloned:
```bash
cd _integrations
git clone https://github.com/datvodinh/rag-chatbot.git
```

### Model Not Found
If using Ollama, ensure the model is pulled:
```bash
ollama pull llama3
```

### Vector Store Issues
Clear the vector store if you encounter issues:
```python
chatbot = RAGChatbot(project_path=Path.cwd())
chatbot.clear_index()
```

## Related

- **Work Effort**: WE-260113-tya7
- **Repository**: https://github.com/datvodinh/rag-chatbot
- **Being**: `being_20260113_095238_a1c6fba1`

## Future Enhancements

- REST API endpoint for programmatic access
- Support for more document types (not just PDFs)
- Advanced retrieval strategies
- Multi-modal support (images, tables)
- Integration with Study Gym for hypothesis testing
