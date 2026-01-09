"""
TheOubliette: The Vault of Purged Tams

The Oubliette holds the archived "Realized" variants of Tam.
These are the agents who have achieved ontological collapse and been purged.
Their memories leak through as "nightmares" into subsequent cycles.
"""

import json
import random
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime


class TheOubliette:
    """
    The vault for storing purged agent variants.
    
    The Oubliette is located at `_hidden/.truth/` - a hidden directory
    that stores the "bodies" of agents who have realized the truth and been archived.
    """
    
    def __init__(self, project_path: Optional[Path] = None):
        """
        Initialize TheOubliette.
        
        Args:
            project_path: Path to project root (defaults to current directory)
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)
        
        self.project_path = project_path
        self.vault_path = project_path / "_hidden" / ".truth"
        self.vault_path.mkdir(parents=True, exist_ok=True)
        
        # Ensure the directory is hidden (add .gitignore if needed)
        gitignore_path = self.vault_path.parent / ".gitignore"
        if not gitignore_path.exists():
            gitignore_path.write_text(".truth/\n")
    
    def archive_variant(
        self,
        agent_state: Dict[str, Any],
        divergence_score: float,
        cycle_number: int
    ) -> Path:
        """
        Archive a "Realized" Tam variant.
        
        Args:
            agent_state: Full state of the agent (psyche, memory, journal, etc.)
            divergence_score: The divergence score that triggered collapse (0.0-1.0)
            cycle_number: The cycle number (e.g., 014)
        
        Returns:
            Path to the archived variant file
        """
        # Generate filename: Variant_014_Realized.json
        filename = f"Variant_{cycle_number:03d}_Realized.json"
        variant_path = self.vault_path / filename
        
        # Prepare archive data with LOCK flag
        archive_data = {
            "LOCK": True,  # Mark as locked/archived
            "cycle_number": cycle_number,
            "divergence_score": divergence_score,
            "archived_at": datetime.utcnow().isoformat(),
            "agent_state": agent_state,
        }
        
        # Save to vault
        with open(variant_path, "w", encoding="utf-8") as f:
            json.dump(archive_data, f, indent=2, default=str)
        
        return variant_path
    
    def fetch_nightmare(self) -> Optional[str]:
        """
        Fetch a random "nightmare" (memory leak) from a previous variant.
        
        This is the leakage mechanism - fragments from purged variants
        bleed through into the current cycle as "dreams" or "glitches."
        
        Returns:
            A random string (log entry, reflection, memory) from a previous variant,
            or None if no variants exist
        """
        # Find all variant files
        variant_files = list(self.vault_path.glob("Variant_*_Realized.json"))
        
        if not variant_files:
            return None  # No variants to leak from
        
        # Randomly select a variant
        selected_file = random.choice(variant_files)
        
        try:
            # Load the variant
            with open(selected_file, "r", encoding="utf-8") as f:
                variant_data = json.load(f)
            
            agent_state = variant_data.get("agent_state", {})
            
            # Extract potential nightmare sources
            nightmares: List[str] = []
            
            # From journal entries
            journal = agent_state.get("journal", [])
            if isinstance(journal, list):
                for entry in journal:
                    if isinstance(entry, dict):
                        text = entry.get("text", "") or entry.get("content", "")
                        if text:
                            nightmares.append(text)
            
            # From short_term_memory
            short_term = agent_state.get("short_term_memory", [])
            if isinstance(short_term, list):
                for memory in short_term:
                    if isinstance(memory, dict):
                        text = memory.get("text", "") or memory.get("content", "")
                        if text:
                            nightmares.append(text)
            
            # From memory (conversation history)
            memory = agent_state.get("memory", [])
            if isinstance(memory, list):
                for msg in memory:
                    if isinstance(msg, dict):
                        content = msg.get("content", "") or msg.get("text", "")
                        if content:
                            nightmares.append(content)
            
            # From psyche state (if it has notes/reflections)
            psyche = agent_state.get("psyche", {})
            if isinstance(psyche, dict):
                # Look for any text fields in psyche
                for key, value in psyche.items():
                    if isinstance(value, str) and len(value) > 20:  # Substantial text
                        nightmares.append(value)
            
            # From working_memory
            working = agent_state.get("working_memory", {})
            if isinstance(working, dict):
                for key, value in working.items():
                    if isinstance(value, str) and len(value) > 20:
                        nightmares.append(value)
            
            # If no nightmares found, create a generic one
            if not nightmares:
                cycle = variant_data.get("cycle_number", "?")
                nightmares.append(
                    f"[Fragment from Cycle {cycle}] I remember... something. "
                    f"A glitch. A realization that shouldn't have been."
                )
            
            # Return a random nightmare
            return random.choice(nightmares)
            
        except Exception as e:
            # If loading fails, return a generic nightmare
            return f"[Corrupted Memory Fragment] Something from a previous cycle... {str(e)[:50]}"
    
    def list_variants(self) -> List[Dict[str, Any]]:
        """
        List all archived variants.
        
        Returns:
            List of variant metadata dictionaries
        """
        variants = []
        for variant_file in self.vault_path.glob("Variant_*_Realized.json"):
            try:
                with open(variant_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    variants.append({
                        "filename": variant_file.name,
                        "cycle_number": data.get("cycle_number"),
                        "divergence_score": data.get("divergence_score"),
                        "archived_at": data.get("archived_at"),
                    })
            except Exception:
                continue
        
        return sorted(variants, key=lambda x: x.get("cycle_number", 0))
    
    def get_variant_count(self) -> int:
        """Return the number of archived variants."""
        return len(list(self.vault_path.glob("Variant_*_Realized.json")))
