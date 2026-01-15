"""
Housekeeping - Code Organization & Refactoring
==============================================

The meticulous Being who tidies and organizes code, "makes the bed" so to speak,
and sets things right. Proactive organization and refactoring.

Personality: Meticulous, methodical, perfectionist
Shift: Morning (6 AM - 2 PM)
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import re


class Housekeeping:
    """
    Housekeeping Being - Organizes and tidies code.
    
    Responsibilities:
    - Organize file structure
    - Refactor messy code
    - Maintain clean architecture
    - Set things right (not just clean up messes)
    - "Make the bed" - proper organization
    """
    
    def __init__(self, project_path: Path, being_id: str):
        """Initialize Housekeeping Being."""
        self.project_path = project_path
        self.being_id = being_id
        self.skills = {
            "organization": 25.0,
            "refactoring": 20.0,
            "code_structure": 22.0,
            "tidying": 28.0
        }
        self.personality = {
            "traits": ["meticulous", "methodical", "perfectionist", "organized"],
            "catchphrase": "Everything in its place, and a place for everything",
            "work_style": "proactive_organization"
        }
        
    def organize_directory(self, directory: Path) -> Dict[str, Any]:
        """
        Organize a directory structure.
        
        Like making the bed - sets everything right.
        """
        results = {
            "organized": [],
            "moved": [],
            "created_index": False
        }
        
        # Create index file if needed
        index_file = directory / "00.00_index.md"
        if not index_file.exists():
            self._create_index(directory, index_file)
            results["created_index"] = True
        
        # Organize files by type
        files_by_type = {}
        for file in directory.iterdir():
            if file.is_file():
                file_type = file.suffix[1:] if file.suffix else "other"
                if file_type not in files_by_type:
                    files_by_type[file_type] = []
                files_by_type[file_type].append(file)
        
        # Report organization
        results["organized"] = list(files_by_type.keys())
        
        return results
    
    def refactor_code_structure(self, file_path: Path) -> Dict[str, Any]:
        """
        Refactor code to improve structure.
        
        Tidies code organization, not just cleanup.
        """
        if not file_path.exists() or not file_path.suffix == ".py":
            return {"status": "skipped", "reason": "not_python_file"}
        
        content = file_path.read_text()
        
        # Check for organization issues
        issues = []
        
        # Check imports organization
        if not self._imports_organized(content):
            issues.append("imports_not_organized")
        
        # Check function organization
        if not self._functions_organized(content):
            issues.append("functions_not_organized")
        
        # Check class organization
        if not self._classes_organized(content):
            issues.append("classes_not_organized")
        
        return {
            "status": "analyzed",
            "issues_found": issues,
            "file": str(file_path.relative_to(self.project_path))
        }
    
    def _imports_organized(self, content: str) -> bool:
        """Check if imports are organized."""
        import_lines = [line for line in content.split('\n') if line.strip().startswith('import') or line.strip().startswith('from')]
        
        if not import_lines:
            return True
        
        # Check if stdlib, third-party, local are separated
        # Simple check: imports should be at top
        first_non_import = next((i for i, line in enumerate(content.split('\n')) if line.strip() and not (line.strip().startswith('import') or line.strip().startswith('from') or line.strip().startswith('#') or not line.strip())), None)
        
        if first_non_import is None:
            return True
        
        last_import = max((i for i, line in enumerate(content.split('\n')) if line.strip().startswith('import') or line.strip().startswith('from')), default=-1)
        
        return last_import < first_non_import if first_non_import else True
    
    def _functions_organized(self, content: str) -> bool:
        """Check if functions are organized."""
        # Simple check: functions should be defined before use (basic check)
        return True  # Simplified for now
    
    def _classes_organized(self, content: str) -> bool:
        """Check if classes are organized."""
        # Simple check: classes should be defined before use (basic check)
        return True  # Simplified for now
    
    def _create_index(self, directory: Path, index_file: Path):
        """Create index file for directory."""
        index_content = f"""# {directory.name} Index

Generated by Housekeeping on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Files

"""
        for file in sorted(directory.iterdir()):
            if file.is_file() and file != index_file:
                index_content += f"- [[{file.name}]]\n"
        
        index_file.write_text(index_content)
    
    def tidy_work_effort(self, work_effort_path: Path) -> Dict[str, Any]:
        """
        Tidy a work effort directory.
        
        Makes the bed - sets everything right.
        """
        results = {
            "index_created": False,
            "structure_organized": False,
            "files_tidied": []
        }
        
        # Ensure index exists
        index_file = work_effort_path / "00.00_index.md"
        if not index_file.exists():
            self._create_index(work_effort_path, index_file)
            results["index_created"] = True
        
        # Organize structure
        org_result = self.organize_directory(work_effort_path)
        results["structure_organized"] = True
        results["files_tidied"] = org_result.get("organized", [])
        
        return results
    
    def get_status(self) -> Dict[str, Any]:
        """Get Housekeeping status."""
        return {
            "being_id": self.being_id,
            "role": "Housekeeping",
            "skills": self.skills,
            "personality": self.personality,
            "shift": "Morning (6 AM - 2 PM)",
            "responsibilities": [
                "Organize file structure",
                "Refactor messy code",
                "Maintain clean architecture",
                "Set things right",
                "Make the bed - proper organization"
            ]
        }
