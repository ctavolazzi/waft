"""
Lore Builder - Lore accumulation and organization.

Accumulates world lore from scenarios and organizes by category.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

from .scenario_realm import ScenarioRealm
from .security import validate_realm_path


class LoreBuilder:
    """
    Builds and accumulates world lore from scenarios.
    
    Features:
    - Lore accumulation from scenarios
    - Organization by category (locations, NPCs, events)
    - Markdown lore entry generation
    - World history tracking
    """
    
    def __init__(self, scenario_realm: ScenarioRealm):
        """
        Initialize Lore Builder.
        
        Args:
            scenario_realm: ScenarioRealm instance
        """
        self.realm = scenario_realm
        self.lore_dir = scenario_realm.realm_path / "lore"
        self.locations_dir = self.lore_dir / "locations"
        self.npcs_dir = self.lore_dir / "npcs"
        self.events_dir = self.lore_dir / "events"
        self.world_history_file = self.lore_dir / "world_history.md"
        
        # Ensure directories exist
        for dir_path in [self.locations_dir, self.npcs_dir, self.events_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def add_lore_entry(
        self,
        category: str,
        entry_name: str,
        entry_data: Dict[str, Any]
    ) -> Path:
        """
        Add a lore entry.
        
        Args:
            category: Lore category (locations, npcs, events)
            entry_name: Name of the entry
            entry_data: Entry data
            
        Returns:
            Path to created lore file
        """
        # Validate category
        if category not in ["locations", "npcs", "events"]:
            raise ValueError(f"Invalid lore category: {category}")
        
        # Get category directory
        if category == "locations":
            category_dir = self.locations_dir
        elif category == "npcs":
            category_dir = self.npcs_dir
        else:
            category_dir = self.events_dir
        
        # Sanitize entry name for filename
        safe_name = "".join(c for c in entry_name if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_name = safe_name.replace(' ', '_')
        
        # Create lore file
        lore_file = category_dir / f"{safe_name}.md"
        
        # Validate path
        if not self.realm.validate_path(lore_file):
            raise ValueError("Lore file path validation failed")
        
        # Generate markdown content
        markdown_content = self._generate_lore_markdown(entry_name, entry_data)
        
        # Write lore file
        lore_file.write_text(markdown_content)
        
        # Update world history
        self._update_world_history(category, entry_name, entry_data)
        
        return lore_file
    
    def _generate_lore_markdown(self, name: str, data: Dict[str, Any]) -> str:
        """Generate markdown content for lore entry."""
        lines = [f"# {name}", "", f"**Created**: {datetime.now().isoformat()}", ""]
        
        if "description" in data:
            lines.append("## Description")
            lines.append(data["description"])
            lines.append("")
        
        if "details" in data:
            lines.append("## Details")
            for key, value in data["details"].items():
                lines.append(f"- **{key}**: {value}")
            lines.append("")
        
        return "\n".join(lines)
    
    def _update_world_history(self, category: str, name: str, data: Dict[str, Any]) -> None:
        """Update world history markdown file."""
        # Initialize or append to world history
        if not self.world_history_file.exists():
            content = "# World History\n\n"
        else:
            content = self.world_history_file.read_text()
        
        # Add entry
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content += f"\n## {timestamp} - {category.title()}: {name}\n\n"
        
        if "description" in data:
            content += f"{data['description']}\n\n"
        
        # Write back
        self.world_history_file.write_text(content)
