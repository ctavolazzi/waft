"""
RAG Chatbot Wrapper

WAFT wrapper around rag-chatbot for PDF querying and knowledge retrieval.
"""

from pathlib import Path
from typing import List, Optional, Dict, Any
import sys

# Add rag-chatbot to path
_rag_chatbot_path = Path(__file__).parent.parent.parent.parent / "_integrations" / "rag-chatbot"
if str(_rag_chatbot_path) not in sys.path:
    sys.path.insert(0, str(_rag_chatbot_path))

try:
    from rag_chatbot import LocalRAGPipeline
    from rag_chatbot.logger import Logger
except ImportError as e:
    # Try alternative import path
    try:
        sys.path.insert(0, str(_rag_chatbot_path / "rag_chatbot"))
        from pipeline import LocalRAGPipeline
        from logger import Logger
    except ImportError:
        raise ImportError(
            f"Failed to import rag-chatbot. Make sure it's cloned to _integrations/rag-chatbot/. Error: {e}"
        )

from .config import RAGConfig


class RAGChatbot:
    """
    WAFT wrapper around rag-chatbot for PDF querying.
    
    Provides:
    - PDF indexing and querying
    - Model selection (Huggingface/Ollama)
    - Vector store management
    - File-based storage (aligns with WAFT philosophy)
    """
    
    def __init__(
        self,
        config: Optional[RAGConfig] = None,
        project_path: Optional[Path] = None
    ):
        """
        Initialize RAG Chatbot.
        
        Args:
            config: RAG configuration (creates default if None)
            project_path: Project root path
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)
        
        self.project_path = project_path
        self.config = config or RAGConfig(project_path=project_path)
        
        # Initialize rag-chatbot pipeline
        self._pipeline = LocalRAGPipeline(host=self.config.host)
        
        # Set model if specified
        if self.config.model_name:
            self._pipeline.set_model_name(self.config.model_name)
            self._pipeline.set_model()
        
        # Set language
        self._pipeline.set_language(self.config.language)
        
        # Set embedding model
        self._pipeline.set_embed_model(self.config.embedding_model)
        
        # Initialize engine
        self._pipeline.reset_engine()
        
        # Logger (optional, for debugging)
        self._logger = Logger()
    
    def add_pdfs(self, pdf_paths: List[str]) -> None:
        """
        Add PDFs to the vector store.
        
        Args:
            pdf_paths: List of paths to PDF files
        """
        # Convert to absolute paths
        abs_paths = []
        for path in pdf_paths:
            p = Path(path)
            if not p.is_absolute():
                p = self.project_path / p
            if not p.exists():
                raise FileNotFoundError(f"PDF not found: {p}")
            abs_paths.append(str(p))
        
        # Store nodes in pipeline
        self._pipeline.store_nodes(input_files=abs_paths)
        
        # Update engine with new nodes
        self._pipeline.set_engine()
    
    def query(
        self,
        question: str,
        pdfs: Optional[List[str]] = None,
        mode: str = "rag"
    ) -> str:
        """
        Query the RAG system.
        
        Args:
            question: Question to ask
            pdfs: Optional list of PDF paths to query (if None, uses all indexed PDFs)
            mode: Query mode ("rag" or "chat")
        
        Returns:
            Answer string
        """
        if pdfs:
            # Add specified PDFs if not already indexed
            self.add_pdfs(pdfs)
        
        # Query pipeline
        response = self._pipeline.query(
            mode=mode,
            message=question,
            chatbot=[]
        )
        
        # Collect streaming response
        answer = []
        for text in response.response_gen:
            answer.append(text)
        
        return "".join(answer)
    
    def clear_index(self) -> None:
        """Clear the vector store index."""
        self._pipeline.reset_documents()
        self._pipeline.reset_engine()
    
    def set_model(self, model_name: str) -> None:
        """
        Set the LLM model.
        
        Args:
            model_name: Model name (Ollama model name or Huggingface model ID)
        """
        self._pipeline.set_model_name(model_name)
        self._pipeline.set_model()
        self.config.model_name = model_name
    
    def get_model_name(self) -> str:
        """Get current model name."""
        return self._pipeline.get_model_name()
    
    def index_path(self, path: Path) -> None:
        """
        Index all PDFs in a directory.
        
        Args:
            path: Directory path to index
        """
        path = Path(path)
        if not path.is_absolute():
            path = self.project_path / path
        
        if not path.exists():
            raise FileNotFoundError(f"Path not found: {path}")
        
        # Find all PDFs
        pdf_files = list(path.rglob("*.pdf"))
        if pdf_files:
            self.add_pdfs([str(p) for p in pdf_files])
    
    def get_indexed_files(self) -> List[str]:
        """Get list of currently indexed files."""
        # Access internal ingestion to get file list
        # This is a bit of a hack, but rag-chatbot doesn't expose this directly
        try:
            return self._pipeline._ingestion._ingested_file
        except AttributeError:
            return []
