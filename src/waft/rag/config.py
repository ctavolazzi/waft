"""
RAG Configuration Management

File-based configuration for RAG models, vector stores, and settings.
"""

from pathlib import Path
from typing import Optional, Dict, Any
import json


class RAGConfig:
    """
    Configuration manager for RAG settings.
    
    Supports:
    - Model selection (Huggingface/Ollama)
    - Vector store configuration
    - File-based storage (aligns with WAFT philosophy)
    """
    
    def __init__(
        self,
        config_path: Optional[Path] = None,
        project_path: Optional[Path] = None
    ):
        """
        Initialize RAG configuration.
        
        Args:
            config_path: Path to config file (default: _hidden/.truth/rag/config.json)
            project_path: Project root path
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)
        
        self.project_path = project_path
        self.rag_path = project_path / "_hidden" / ".truth" / "rag"
        self.rag_path.mkdir(parents=True, exist_ok=True)
        
        if config_path is None:
            config_path = self.rag_path / "config.json"
        else:
            config_path = Path(config_path)
        
        self.config_path = config_path
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        
        # Default configuration
        return {
            "model_type": "ollama",  # "ollama" or "huggingface"
            "model_name": "",  # Empty = use default
            "embedding_model": "all-MiniLM-L6-v2",  # sentence-transformers model
            "vector_store_path": str(self.rag_path / "vector_store"),
            "host": "localhost",  # Ollama host
            "language": "eng",
            "auto_index_on_start": False,  # Auto-index WAFT codebase on startup
            "indexed_paths": [],  # Paths to automatically index
        }
    
    def save(self):
        """Save configuration to file."""
        with open(self.config_path, 'w') as f:
            json.dump(self._config, f, indent=2)
    
    @property
    def model_type(self) -> str:
        """Get model type (ollama or huggingface)."""
        return self._config.get("model_type", "ollama")
    
    @model_type.setter
    def model_type(self, value: str):
        """Set model type."""
        if value not in ["ollama", "huggingface"]:
            raise ValueError(f"model_type must be 'ollama' or 'huggingface', got '{value}'")
        self._config["model_type"] = value
        self.save()
    
    @property
    def model_name(self) -> str:
        """Get model name."""
        return self._config.get("model_name", "")
    
    @model_name.setter
    def model_name(self, value: str):
        """Set model name."""
        self._config["model_name"] = value
        self.save()
    
    @property
    def embedding_model(self) -> str:
        """Get embedding model name."""
        return self._config.get("embedding_model", "all-MiniLM-L6-v2")
    
    @embedding_model.setter
    def embedding_model(self, value: str):
        """Set embedding model name."""
        self._config["embedding_model"] = value
        self.save()
    
    @property
    def vector_store_path(self) -> Path:
        """Get vector store path."""
        return Path(self._config.get("vector_store_path", str(self.rag_path / "vector_store")))
    
    @vector_store_path.setter
    def vector_store_path(self, value: Path):
        """Set vector store path."""
        self._config["vector_store_path"] = str(value)
        self.save()
    
    @property
    def host(self) -> str:
        """Get Ollama host."""
        return self._config.get("host", "localhost")
    
    @host.setter
    def host(self, value: str):
        """Set Ollama host."""
        self._config["host"] = value
        self.save()
    
    @property
    def language(self) -> str:
        """Get language."""
        return self._config.get("language", "eng")
    
    @language.setter
    def language(self, value: str):
        """Set language."""
        self._config["language"] = value
        self.save()
    
    @property
    def auto_index_on_start(self) -> bool:
        """Get auto-index setting."""
        return self._config.get("auto_index_on_start", False)
    
    @auto_index_on_start.setter
    def auto_index_on_start(self, value: bool):
        """Set auto-index setting."""
        self._config["auto_index_on_start"] = value
        self.save()
    
    @property
    def indexed_paths(self) -> list:
        """Get indexed paths."""
        return self._config.get("indexed_paths", [])
    
    def add_indexed_path(self, path: str):
        """Add path to indexed paths."""
        paths = self.indexed_paths
        if path not in paths:
            paths.append(path)
            self._config["indexed_paths"] = paths
            self.save()
    
    def remove_indexed_path(self, path: str):
        """Remove path from indexed paths."""
        paths = self.indexed_paths
        if path in paths:
            paths.remove(path)
            self._config["indexed_paths"] = paths
            self.save()
