"""
RAG Agent Integration

Mixin class to add RAG capabilities to BaseAgent subclasses.
"""

from pathlib import Path
from typing import Any

from ..core.agent.state import AgentState
from .chatbot import RAGChatbot
from .config import RAGConfig


class RAGAgentMixin:
    """
    Mixin class to add RAG capabilities to BaseAgent.

    Provides:
    - query_rag(): Query RAG for relevant knowledge
    - index_knowledge(): Index knowledge sources
    - get_relevant_context(): Get context for decisions
    """

    def __init__(self, *args, **kwargs):
        """Initialize RAG capabilities."""
        super().__init__(*args, **kwargs)

        # Initialize RAG chatbot
        self._rag_config = RAGConfig(project_path=self.project_path)
        self._rag_chatbot: RAGChatbot | None = None

        # Auto-index on startup if configured
        if self._rag_config.auto_index_on_start:
            self._ensure_rag_initialized()
            self._auto_index_waft_knowledge()

    def _ensure_rag_initialized(self):
        """Ensure RAG chatbot is initialized."""
        if self._rag_chatbot is None:
            self._rag_chatbot = RAGChatbot(config=self._rag_config, project_path=self.project_path)

    def _auto_index_waft_knowledge(self):
        """Auto-index WAFT knowledge sources if configured."""
        indexed_paths = self._rag_config.indexed_paths
        if not indexed_paths:
            # Default: index docs and work efforts
            indexed_paths = [
                str(self.project_path / "docs"),
                str(self.project_path / "_work_efforts"),
            ]

        for path_str in indexed_paths:
            path = Path(path_str)
            if not path.is_absolute():
                path = self.project_path / path

            if path.exists():
                # Index PDFs in this path
                self.index_knowledge([str(path)])

    def query_rag(self, question: str, pdfs: list[str] | None = None) -> str:
        """
        Query RAG for relevant knowledge.

        Args:
            question: Question to ask
            pdfs: Optional list of PDF paths to query

        Returns:
            Answer from RAG
        """
        self._ensure_rag_initialized()
        return self._rag_chatbot.query(question=question, pdfs=pdfs, mode="rag")

    def index_knowledge(self, paths: list[str]) -> None:
        """
        Index knowledge sources (PDFs or directories).

        Args:
            paths: List of paths to PDFs or directories containing PDFs
        """
        self._ensure_rag_initialized()

        pdf_paths = []
        for path_str in paths:
            path = Path(path_str)
            if not path.is_absolute():
                path = self.project_path / path

            if not path.exists():
                continue

            if path.is_file() and path.suffix.lower() == ".pdf":
                pdf_paths.append(str(path))
            elif path.is_dir():
                # Find all PDFs in directory
                pdf_files = list(path.rglob("*.pdf"))
                pdf_paths.extend([str(p) for p in pdf_files])

        if pdf_paths:
            self._rag_chatbot.add_pdfs(pdf_paths)

    def get_relevant_context(self, query: str, max_results: int = 3) -> list[dict[str, Any]]:
        """
        Get relevant context from RAG for a query.

        Args:
            query: Query to find relevant context
            max_results: Maximum number of results

        Returns:
            List of relevant context dictionaries
        """
        self._ensure_rag_initialized()

        # Query RAG
        answer = self.query_rag(query)

        # Return as context dict
        return [
            {
                "source": "rag",
                "query": query,
                "answer": answer,
                "relevance": 1.0,  # RAG already does relevance filtering
            }
        ]

    # Hook methods for BaseAgent lifecycle

    async def observe_with_rag(self, original_observe):
        """
        Enhanced observe() that queries RAG for relevant knowledge.

        This should be called from observe() method:

        ```python
        async def observe(self):
            # Query RAG for relevant knowledge
            rag_context = await self.observe_with_rag(super().observe)

            # Use rag_context in observation
            ...
        ```
        """
        # Query RAG for relevant knowledge about current state
        query = f"What should I know about {self.config.role} working on {self.config.goal}?"
        rag_knowledge = self.query_rag(query)

        # Store in working memory
        if "rag_knowledge" not in self.state.working_memory:
            self.state.working_memory["rag_knowledge"] = []
        self.state.working_memory["rag_knowledge"].append(
            {"query": query, "knowledge": rag_knowledge}
        )

        # Call original observe
        if original_observe:
            return await original_observe()
        return None

    async def decide_with_rag(self, state: AgentState, original_decide):
        """
        Enhanced decide() that uses RAG knowledge to inform decisions.

        This should be called from decide() method:

        ```python
        async def decide(self, state: AgentState):
            # Get RAG context for decision
            rag_context = await self.decide_with_rag(state, super().decide)

            # Use rag_context in decision
            ...
        ```
        """
        # Query RAG for similar decisions/patterns
        query = (
            f"What decisions have been made for {self.config.role} with goal {self.config.goal}?"
        )
        rag_context = self.get_relevant_context(query)

        # Add to state for decision-making
        if "rag_context" not in state.working_memory:
            state.working_memory["rag_context"] = []
        state.working_memory["rag_context"].extend(rag_context)

        # Call original decide
        if original_decide:
            return await original_decide(state)
        return None

    async def reflect_with_rag(self, result: dict, original_reflect):
        """
        Enhanced reflect() that stores learnings back to RAG.

        This should be called from reflect() method:

        ```python
        async def reflect(self, result: dict):
            # Store learnings to RAG
            await self.reflect_with_rag(result, super().reflect)

            # Continue reflection
            ...
        ```
        """
        # Extract learnings from result
        learnings = result.get("learnings", [])
        insights = result.get("insights", [])

        # Store learnings (could be indexed as PDF or text)
        # For now, we'll just track them in working memory
        if "rag_learnings" not in self.state.working_memory:
            self.state.working_memory["rag_learnings"] = []

        self.state.working_memory["rag_learnings"].extend(learnings)
        self.state.working_memory["rag_learnings"].extend(insights)

        # Call original reflect
        if original_reflect:
            return await original_reflect(result)
        return None

    async def spawn_with_rag(self, mutation, original_spawn):
        """
        Enhanced spawn() that queries RAG for successful mutation patterns.

        This should be called from spawn() method:

        ```python
        async def spawn(self, mutation: Modification):
            # Query RAG for successful patterns
            rag_patterns = await self.spawn_with_rag(mutation, super().spawn)

            # Use patterns to guide mutation
            ...
        ```
        """
        # Query RAG for successful mutation patterns
        query = f"What mutation patterns have been successful for {self.config.role}?"
        rag_patterns = self.query_rag(query)

        # Store patterns in working memory
        if "rag_mutation_patterns" not in self.state.working_memory:
            self.state.working_memory["rag_mutation_patterns"] = []
        self.state.working_memory["rag_mutation_patterns"].append(
            {"query": query, "patterns": rag_patterns}
        )

        # Call original spawn
        if original_spawn:
            return await original_spawn(mutation)
        return None
