"""
Concierge - Information Architecture & Knowledge Management
===========================================================

The helpful Being who knows where everything is, routes requests to right places,
and maintains the knowledge base.

Personality: Helpful, organized, encyclopedic memory
Shift: All shifts (24/7 knowledge base)
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import json


class Concierge:
    """
    Concierge Being - Information architecture and knowledge management.
    
    Responsibilities:
    - Know where everything is
    - Route requests to right places
    - Maintain knowledge base
    - Answer questions about project structure
    """
    
    def __init__(self, project_path: Path, being_id: str):
        """Initialize Concierge Being."""
        self.project_path = project_path
        self.being_id = being_id
        self.skills = {
            "information_architecture": 30.0,
            "knowledge_management": 28.0,
            "routing": 25.0,
            "memory": 35.0
        }
        self.personality = {
            "traits": ["helpful", "organized", "encyclopedic_memory", "knowledgeable"],
            "catchphrase": "I know exactly where that is!",
            "work_style": "knowledge_base"
        }
        self.knowledge_base = {}
        
    def find_file(self, filename: str) -> List[Path]:
        """Find file(s) by name."""
        matches = list(self.project_path.rglob(filename))
        return matches
    
    def find_by_pattern(self, pattern: str) -> List[Path]:
        """Find files matching pattern."""
        matches = list(self.project_path.rglob(pattern))
        return matches
    
    def get_project_structure(self) -> Dict[str, Any]:
        """Get project structure overview."""
        structure = {
            "directories": [],
            "key_files": [],
            "work_efforts": []
        }
        
        # Key directories
        key_dirs = ["src", "scripts", "tests", "_work_efforts", "hotel_staff"]
        for dir_name in key_dirs:
            dir_path = self.project_path / dir_name
            if dir_path.exists():
                structure["directories"].append({
                    "name": dir_name,
                    "path": str(dir_path.relative_to(self.project_path)),
                    "exists": True
                })
        
        # Work efforts
        work_efforts = self.project_path / "_work_efforts"
        if work_efforts.exists():
            for we_dir in work_efforts.iterdir():
                if we_dir.is_dir():
                    structure["work_efforts"].append(we_dir.name)
        
        return structure
    
    def route_request(self, request: str) -> Dict[str, Any]:
        """Route request to appropriate staff member."""
        routing = {
            "routed_to": None,
            "reason": None
        }
        
        request_lower = request.lower()
        
        if any(word in request_lower for word in ["organize", "tidy", "refactor", "structure"]):
            routing["routed_to"] = "housekeeping"
            routing["reason"] = "Organization and tidying"
        elif any(word in request_lower for word in ["clean", "temp", "error", "remove"]):
            routing["routed_to"] = "janitor"
            routing["reason"] = "Cleanup and error handling"
        elif any(word in request_lower for word in ["fix", "broken", "maintain", "health"]):
            routing["routed_to"] = "maintenance"
            routing["reason"] = "System maintenance and fixes"
        elif any(word in request_lower for word in ["review", "audit", "check", "verify"]):
            routing["routed_to"] = "night_auditor"
            routing["reason"] = "Review and auditing"
        elif any(word in request_lower for word in ["create", "generate", "new", "make"]):
            routing["routed_to"] = "chef"
            routing["reason"] = "Code generation and creation"
        else:
            routing["routed_to"] = "front_desk"
            routing["reason"] = "General request handling"
        
        return routing
    
    def get_status(self) -> Dict[str, Any]:
        """Get Concierge status."""
        return {
            "being_id": self.being_id,
            "role": "Concierge",
            "skills": self.skills,
            "personality": self.personality,
            "shift": "All shifts (24/7 knowledge base)",
            "responsibilities": [
                "Know where everything is",
                "Route requests to right places",
                "Maintain knowledge base",
                "Answer questions about project structure"
            ]
        }
