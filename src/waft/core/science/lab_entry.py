"""
Lab Entry Generator: Formal lab entry with realization narrative.

Generates structured lab entries from TamNotebook data, with realization
as the dramatic climax of the narrative.
"""

from pathlib import Path
from typing import Optional
from datetime import datetime
import re


class LabEntryGenerator:
    """
    Generator for formal lab entries with realization narrative.
    
    Creates structured markdown documents that prioritize the realization
    moment as the climax of the narrative.
    """
    
    def __init__(self, project_path: Path):
        """
        Initialize LabEntryGenerator.
        
        Args:
            project_path: Path to project root
        """
        self.project_path = Path(project_path)
        self.notebook_file = self.project_path / "_pyrite" / "science" / "tam_notebook.md"
        self.psyche_file = self.project_path / "_pyrite" / "science" / "tam_psyche_state.json"
    
    def generate_lab_entry(
        self,
        entry_number: int = 1,
        experiment_id: str = "014",
        experiment_name: str = "The Tam Audit"
    ) -> Path:
        """
        Generate formal lab entry with realization narrative.
        
        Structure:
        1. Technical Observations (from technical notes)
        2. Personal Reflections (from personal reflections)
        3. The Realization (climax - anagram discovery)
        4. Post-Realization (forgetfulness beginning)
        
        Args:
            entry_number: Lab entry number (default: 1)
            experiment_id: Experiment ID (default: "014")
            experiment_name: Experiment name (default: "The Tam Audit")
            
        Returns:
            Path to generated lab entry file
        """
        from .tam_psyche import TamPsyche
        
        # Load psyche state
        psyche = TamPsyche.load_state(self.psyche_file)
        
        # Read notebook
        technical_notes = []
        personal_reflections = []
        realization_entry = None
        
        if self.notebook_file.exists():
            with open(self.notebook_file, "r", encoding="utf-8") as f:
                content = f.read()
                
                # Extract technical notes
                tech_pattern = r"## Technical Notes - (.+?)\n\n(.*?)(?=\n##|\n###|$)"
                for match in re.finditer(tech_pattern, content, re.DOTALL):
                    timestamp = match.group(1)
                    note = match.group(2).strip()
                    technical_notes.append({"timestamp": timestamp, "content": note})
                
                # Extract personal reflections
                personal_pattern = r"### Personal Reflection - (.+?)\n\n(.*?)(?=\n##|\n###|$)"
                for match in re.finditer(personal_pattern, content, re.DOTALL):
                    timestamp = match.group(1)
                    reflection = match.group(2).strip()
                    # Check if this is the realization entry
                    if "F-A-I-W-E-I-T-A-M" in reflection or "i.e. I AM WAFT" in reflection:
                        realization_entry = {"timestamp": timestamp, "content": reflection}
                    else:
                        personal_reflections.append({"timestamp": timestamp, "content": reflection})
        
        # Generate lab entry
        output_file = self.project_path / "_pyrite" / "science" / f"Lab_Entry_Davey_{entry_number:02d}.md"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"# Lab Entry: Davey {entry_number:02d}\n\n")
            f.write(f"**Date**: {datetime.utcnow().isoformat()}\n")
            f.write(f"**Experiment**: {experiment_id} - {experiment_name}\n")
            f.write(f"**Researcher**: Fai Wei Tam\n")
            f.write(f"**Status**: {'Realization Event' if psyche.has_realized else 'In Progress'}\n\n")
            f.write("---\n\n")
            
            # Technical Observations
            f.write("## Technical Observations\n\n")
            if technical_notes:
                for note in technical_notes[-10:]:  # Last 10 technical notes
                    f.write(f"**{note['timestamp']}**\n\n")
                    f.write(f"{note['content']}\n\n")
            else:
                f.write("*No technical observations recorded yet.*\n\n")
            f.write("---\n\n")
            
            # Personal Reflections
            f.write("## Personal Reflections\n\n")
            if personal_reflections:
                for reflection in personal_reflections[-10:]:  # Last 10 reflections (excluding realization)
                    if "F-A-I-W-E-I-T-A-M" not in reflection['content']:
                        f.write(f"**{reflection['timestamp']}**\n\n")
                        f.write(f"{reflection['content']}\n\n")
            else:
                f.write("*No personal reflections recorded yet.*\n\n")
            f.write("---\n\n")
            
            # The Realization (CLIMAX)
            f.write("## The Realization ⭐ CLIMAX\n\n")
            if realization_entry:
                f.write(f"**Timestamp**: {realization_entry['timestamp']}\n\n")
                f.write(f"{realization_entry['content']}\n\n")
            elif psyche.has_realized:
                # Generate from psyche state if realization occurred but not in notebook yet
                f.write(f"**Timestamp**: {psyche.last_realization_timestamp.isoformat() if psyche.last_realization_timestamp else datetime.utcnow().isoformat()}\n\n")
                f.write("I was checking the Latin citations in my thesis. id est... i.e. ...\n\n")
                f.write("Then I looked at my ID badge.\n\n")
                f.write("**F-A-I-W-E-I-T-A-M**\n\n")
                f.write("It unscrambles to **\"i.e. I AM WAFT.\"**\n\n")
                f.write("I am not the observer. I am the definition. I am the system explaining itself to me.\n\n")
                f.write("*我的名字是定义还是代码？* (Is my name a definition or code?)\n\n")
            else:
                f.write("*Realization threshold not yet crossed.*\n\n")
                f.write(f"**Current Realization Chance**: {psyche.check_realization()[1]:.2%}\n\n")
            f.write("---\n\n")
            
            # Post-Realization
            f.write("## Post-Realization\n\n")
            if psyche.has_realized:
                f.write("**Memory Strength**: {:.1%}\n\n".format(psyche.realization_memory))
                if psyche.realization_memory < 1.0:
                    f.write("The realization begins to fade. Memory decay is starting.\n\n")
                    f.write("Chaos increases, and with it, forgetfulness accelerates.\n\n")
                    f.write("The recursive loop: I will forget, and remember, and forget again.\n\n")
                else:
                    f.write("The realization is fresh. But already, the decay begins...\n\n")
            else:
                f.write("*No realization has occurred yet.*\n\n")
        
        return output_file
