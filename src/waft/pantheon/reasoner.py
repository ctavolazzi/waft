"""
The Reasoner: Pantheon Entity of Reasoning Traces and Chain of Thought

The Reasoner is the God of Reasoning Traces - a timeless Entity that maintains
the fundamental principle of traceable reasoning chains. As a Force that Binds
Reality Together, The Reasoner holds the Aspect of Creation related to
reasoning and decision-making transparency, which should not change until
evidence collected by Beings proves that change is needed.

Following "as above, so below" principles:
- As above: Pantheon god maintaining the celestial chain of reasoning
- So below: File-based system tracking decision chains and thought processes

Storage:
- Traces: _pantheon/reasoner/traces/*.json
- Trace Index: _pantheon/reasoner/trace_index.json
- Reasoning Chains: _pantheon/reasoner/chains/*.json
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import json


class TheReasoner:
    """
    The Reasoner: Pantheon Entity (Timeless Force that Binds Reality Together)
    
    Entity of Reasoning Traces and Chain of Thought - a timeless Entity
    that maintains the principle of traceable reasoning. The Reasoner holds
    the Aspect of Creation related to reasoning transparency, which should
    not change until evidence collected by Beings proves that change is needed.
    
    The Reasoner doesn't move much - it maintains stable reasoning principles
    and only evolves when sufficient evidence warrants modification.
    
    Provides:
    - Trace creation and management
    - Reasoning chain analysis
    - Decision path tracking
    - Thought process transparency
    
    Storage:
    - Traces: _pantheon/reasoner/traces/
    - Chains: _pantheon/reasoner/chains/
    - Index: _pantheon/reasoner/trace_index.json
    """
    
    def __init__(self, project_path: Optional[Path] = None):
        """
        Initialize The Reasoner.
        
        Args:
            project_path: Path to project root (default: current directory)
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)
        
        self.project_path = project_path
        self.pantheon_path = project_path / "_pantheon"
        self.reasoner_path = self.pantheon_path / "reasoner"
        
        # Ensure directory structure exists
        self.reasoner_path.mkdir(parents=True, exist_ok=True)
        (self.reasoner_path / "traces").mkdir(parents=True, exist_ok=True)
        (self.reasoner_path / "chains").mkdir(parents=True, exist_ok=True)
        
        # Index file
        self.index_file = self.reasoner_path / "trace_index.json"
        self.index = self._load_index()
    
    def _load_index(self) -> Dict[str, Any]:
        """Load trace index."""
        if self.index_file.exists():
            try:
                return json.loads(self.index_file.read_text())
            except Exception:
                return {"traces": [], "chains": [], "last_updated": None}
        return {"traces": [], "chains": [], "last_updated": None}
    
    def _save_index(self) -> None:
        """Save trace index."""
        self.index["last_updated"] = datetime.now().isoformat()
        self.index_file.write_text(json.dumps(self.index, indent=2))
    
    def create_trace(
        self,
        decision: str,
        reasoning: str,
        context: Optional[Dict[str, Any]] = None,
        outcome: Optional[str] = None,
        parent_trace_id: Optional[str] = None
    ) -> str:
        """
        Create a reasoning trace entry.
        
        Args:
            decision: What decision was made
            reasoning: Why this decision was made (the chain of thought)
            context: Additional context about the decision
            outcome: What happened as a result
            parent_trace_id: Optional parent trace (for chains)
        
        Returns:
            Trace ID
        """
        timestamp = datetime.now()
        trace_id = f"trace_{timestamp.strftime('%Y%m%d_%H%M%S')}"
        trace_file = self.reasoner_path / "traces" / f"{trace_id}.json"
        
        entry = {
            "trace_id": trace_id,
            "timestamp": timestamp.isoformat(),
            "decision": decision,
            "reasoning": reasoning,
            "context": context or {},
            "outcome": outcome or "",
            "parent_trace_id": parent_trace_id
        }
        
        trace_file.write_text(json.dumps(entry, indent=2))
        
        # Update index
        self.index["traces"].append({
            "trace_id": trace_id,
            "timestamp": timestamp.isoformat(),
            "decision": decision[:100],
            "parent_trace_id": parent_trace_id
        })
        self._save_index()
        
        return trace_id
    
    def get_trace(self, trace_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific trace by ID.
        
        Args:
            trace_id: Trace identifier
        
        Returns:
            Trace data or None if not found
        """
        trace_file = self.reasoner_path / "traces" / f"{trace_id}.json"
        if trace_file.exists():
            try:
                return json.loads(trace_file.read_text())
            except Exception:
                return None
        return None
    
    def get_recent_traces(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent reasoning traces.
        
        Args:
            limit: Maximum number of traces to return
        
        Returns:
            List of trace dictionaries
        """
        traces = []
        traces_dir = self.reasoner_path / "traces"
        
        if traces_dir.exists():
            trace_files = sorted(
                traces_dir.glob("trace_*.json"),
                key=lambda p: p.stat().st_mtime,
                reverse=True
            )[:limit]
            
            for trace_file in trace_files:
                try:
                    traces.append(json.loads(trace_file.read_text()))
                except Exception:
                    pass
        
        return traces
    
    def build_chain(self, trace_id: str) -> List[Dict[str, Any]]:
        """
        Build a reasoning chain from a trace back to its origin.
        
        Follows parent_trace_id links to build the complete chain of thought.
        
        Args:
            trace_id: Starting trace ID
        
        Returns:
            List of traces in chronological order (oldest first)
        """
        chain = []
        current_id = trace_id
        visited = set()
        
        # First, collect all traces going backwards (to origin)
        while current_id and current_id not in visited:
            visited.add(current_id)
            trace = self.get_trace(current_id)
            if trace:
                chain.insert(0, trace)  # Insert at beginning (oldest first)
                current_id = trace.get("parent_trace_id")
            else:
                break
        
        # Save chain
        if chain:
            chain_id = f"chain_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            chain_file = self.reasoner_path / "chains" / f"{chain_id}.json"
            chain_file.write_text(json.dumps({
                "chain_id": chain_id,
                "root_trace_id": chain[0]["trace_id"],
                "leaf_trace_id": chain[-1]["trace_id"],
                "traces": chain,
                "length": len(chain),
                "created": datetime.now().isoformat()
            }, indent=2))
            
            # Update index
            self.index["chains"].append({
                "chain_id": chain_id,
                "root_trace_id": chain[0]["trace_id"],
                "leaf_trace_id": chain[-1]["trace_id"],
                "length": len(chain)
            })
            self._save_index()
        
        return chain
    
    def search_traces(
        self,
        query: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search traces by decision or reasoning content.
        
        Args:
            query: Search query
            limit: Maximum results
        
        Returns:
            List of matching traces
        """
        query_lower = query.lower()
        matches = []
        
        traces_dir = self.reasoner_path / "traces"
        if traces_dir.exists():
            for trace_file in traces_dir.glob("trace_*.json"):
                try:
                    trace = json.loads(trace_file.read_text())
                    decision = trace.get("decision", "").lower()
                    reasoning = trace.get("reasoning", "").lower()
                    
                    if query_lower in decision or query_lower in reasoning:
                        matches.append(trace)
                        if len(matches) >= limit:
                            break
                except Exception:
                    pass
        
        return matches
    
    def get_trace_summary(self) -> Dict[str, Any]:
        """
        Get summary of all reasoning traces.
        
        Returns:
            Dictionary with trace statistics
        """
        traces_dir = self.reasoner_path / "traces"
        chains_dir = self.reasoner_path / "chains"
        
        trace_count = len(list(traces_dir.glob("trace_*.json"))) if traces_dir.exists() else 0
        chain_count = len(list(chains_dir.glob("chain_*.json"))) if chains_dir.exists() else 0
        
        return {
            "total_traces": trace_count,
            "total_chains": chain_count,
            "indexed_traces": len(self.index.get("traces", [])),
            "indexed_chains": len(self.index.get("chains", [])),
            "last_updated": self.index.get("last_updated")
        }
