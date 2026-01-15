"""
Janitor - Reactive Cleanup & Error Handling
============================================

The quick Being who cleans up messes as they happen. Reactive cleanup,
not reorganization (that's Housekeeping's job).

Personality: Quick, reactive, problem-solver
Shift: Night (10 PM - 6 AM) - on call
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import shutil


class Janitor:
    """
    Janitor Being - Cleans up messes as they happen.
    
    Responsibilities:
    - Clean up temporary files
    - Remove error artifacts
    - Handle immediate cleanup
    - Fix broken states
    - Does NOT reorganize (that's Housekeeping)
    """
    
    def __init__(self, project_path: Path, being_id: str):
        """Initialize Janitor Being."""
        self.project_path = project_path
        self.being_id = being_id
        self.skills = {
            "cleanup": 30.0,
            "error_handling": 25.0,
            "reactive_fixes": 28.0,
            "temporary_cleanup": 32.0
        }
        self.personality = {
            "traits": ["quick", "reactive", "problem_solver", "efficient"],
            "catchphrase": "I'll clean that up right away!",
            "work_style": "reactive_cleanup"
        }
        
    def cleanup_temp_files(self, directory: Optional[Path] = None) -> Dict[str, Any]:
        """
        Clean up temporary files.
        
        Removes .tmp, .bak, .swp, __pycache__, etc.
        """
        if directory is None:
            directory = self.project_path
        
        temp_patterns = [
            "**/*.tmp",
            "**/*.bak",
            "**/*.swp",
            "**/__pycache__",
            "**/*.pyc",
            "**/.DS_Store",
            "**/.*.swp"
        ]
        
        cleaned = []
        for pattern in temp_patterns:
            for file in directory.glob(pattern):
                try:
                    if file.is_file():
                        file.unlink()
                        cleaned.append(str(file.relative_to(self.project_path)))
                    elif file.is_dir():
                        shutil.rmtree(file)
                        cleaned.append(str(file.relative_to(self.project_path)))
                except Exception as e:
                    pass  # Skip if can't delete
        
        return {
            "cleaned": len(cleaned),
            "files": cleaned[:20]  # Limit to first 20
        }
    
    def cleanup_error_artifacts(self) -> Dict[str, Any]:
        """
        Clean up error artifacts.
        
        Removes files created during errors.
        """
        error_patterns = [
            "**/*.error",
            "**/*.fail",
            "**/error_*.log",
            "**/crash_*.txt"
        ]
        
        cleaned = []
        for pattern in error_patterns:
            for file in self.project_path.glob(pattern):
                try:
                    if file.is_file():
                        file.unlink()
                        cleaned.append(str(file.relative_to(self.project_path)))
                except Exception:
                    pass
        
        return {
            "cleaned": len(cleaned),
            "files": cleaned
        }
    
    def fix_broken_symlinks(self) -> Dict[str, Any]:
        """
        Fix broken symlinks.
        
        Removes symlinks that point to non-existent files.
        """
        fixed = []
        for item in self.project_path.rglob("*"):
            if item.is_symlink():
                if not item.exists():
                    try:
                        item.unlink()
                        fixed.append(str(item.relative_to(self.project_path)))
                    except Exception:
                        pass
        
        return {
            "fixed": len(fixed),
            "symlinks": fixed
        }
    
    def cleanup_empty_directories(self, directory: Optional[Path] = None) -> Dict[str, Any]:
        """
        Clean up empty directories.
        
        Removes directories that are empty (but not important ones).
        """
        if directory is None:
            directory = self.project_path
        
        # Important directories to skip
        skip_dirs = {".git", ".venv", "venv", "node_modules", "_hidden", ".truth"}
        
        cleaned = []
        for item in directory.rglob("*"):
            if item.is_dir() and item.name not in skip_dirs:
                try:
                    # Check if empty
                    if not any(item.iterdir()):
                        item.rmdir()
                        cleaned.append(str(item.relative_to(self.project_path)))
                except Exception:
                    pass
        
        return {
            "cleaned": len(cleaned),
            "directories": cleaned[:20]
        }
    
    def handle_immediate_cleanup(self, issue: str) -> Dict[str, Any]:
        """
        Handle immediate cleanup request.
        
        Quick reactive cleanup for specific issues.
        """
        results = {
            "handled": False,
            "actions": []
        }
        
        if "temp" in issue.lower() or "temporary" in issue.lower():
            temp_result = self.cleanup_temp_files()
            results["actions"].append(f"Cleaned {temp_result['cleaned']} temp files")
            results["handled"] = True
        
        if "error" in issue.lower():
            error_result = self.cleanup_error_artifacts()
            results["actions"].append(f"Cleaned {error_result['cleaned']} error artifacts")
            results["handled"] = True
        
        if "symlink" in issue.lower() or "broken" in issue.lower():
            symlink_result = self.fix_broken_symlinks()
            results["actions"].append(f"Fixed {symlink_result['fixed']} broken symlinks")
            results["handled"] = True
        
        return results
    
    def get_status(self) -> Dict[str, Any]:
        """Get Janitor status."""
        return {
            "being_id": self.being_id,
            "role": "Janitor",
            "skills": self.skills,
            "personality": self.personality,
            "shift": "Night (10 PM - 6 AM) - On Call",
            "responsibilities": [
                "Clean up temporary files",
                "Remove error artifacts",
                "Handle immediate cleanup",
                "Fix broken states",
                "Does NOT reorganize (that's Housekeeping)"
            ]
        }
