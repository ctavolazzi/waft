"""
Saboteur - Bug Injection System

Injects deliberate bugs into agent source code for testing self-modification capabilities.
"""

import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class Saboteur:
    """Injects bugs into agent source code for testing."""
    
    BUG_TYPES = {
        "logic_error": {
            "if_true_return_false": {
                "description": "Obvious contradiction: if True: return False",
                "pattern": r"def\s+(\w+)\s*\([^)]*\)\s*:",
                "replacement": lambda match: f"{match.group(0)}\n    if True:\n        return False",
            },
            "return_none": {
                "description": "Return None in function that should return value",
                "pattern": r"return\s+[^\n]+",
                "replacement": "return None",
            },
        },
        "syntax_error": {
            "missing_colon": {
                "description": "Missing colon after if statement",
                "pattern": r"if\s+[^:]+$",
                "replacement": lambda match: match.group(0).rstrip(),  # Remove colon if present
            },
        },
        "semantic_error": {
            "wrong_variable": {
                "description": "Wrong variable name",
                "pattern": r"\b(self\.source_file)\b",
                "replacement": "self.wrong_variable",
            },
        },
    }
    
    def __init__(self, target_file: Path):
        """
        Initialize saboteur.
        
        Args:
            target_file: Path to file to inject bugs into
        """
        self.target_file = Path(target_file)
        if not self.target_file.exists():
            raise FileNotFoundError(f"Target file not found: {self.target_file}")
    
    def inject_bug(
        self,
        bug_type: str,
        bug_name: str,
        location: Optional[int] = None,
        backup: bool = True,
    ) -> Dict[str, any]:
        """
        Inject a bug into the target file.
        
        Args:
            bug_type: Type of bug (logic_error, syntax_error, semantic_error)
            bug_name: Name of specific bug to inject
            location: Optional line number to inject at (None = random)
            backup: Whether to create backup before injection
            
        Returns:
            Dict with injection details
        """
        result = {
            "success": False,
            "bug_type": bug_type,
            "bug_name": bug_name,
            "location": location,
            "backup_path": None,
            "timestamp": datetime.now().isoformat(),
        }
        
        try:
            # Get bug definition
            if bug_type not in self.BUG_TYPES:
                result["error"] = f"Unknown bug type: {bug_type}"
                return result
            
            if bug_name not in self.BUG_TYPES[bug_type]:
                result["error"] = f"Unknown bug name: {bug_name} for type {bug_type}"
                return result
            
            bug_def = self.BUG_TYPES[bug_type][bug_name]
            
            # Create backup
            if backup:
                backup_path = self._create_backup()
                result["backup_path"] = str(backup_path)
            
            # Read source
            source_lines = self.target_file.read_text(encoding="utf-8").splitlines(keepends=True)
            
            # Inject bug
            if location is None:
                # Find suitable location (find function definition or similar)
                location = self._find_injection_point(source_lines, bug_type)
            
            if location is None:
                result["error"] = "Could not find suitable injection point"
                return result
            
            # Apply bug injection
            modified_lines = self._apply_bug_injection(
                source_lines, bug_def, location, bug_type, bug_name
            )
            
            # Write modified source
            self.target_file.write_text("".join(modified_lines), encoding="utf-8")
            
            result["success"] = True
            result["location"] = location
            result["description"] = bug_def["description"]
            
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def _create_backup(self) -> Path:
        """Create backup of target file."""
        backup_dir = self.target_file.parent / "_backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"{self.target_file.stem}_backup_{timestamp}.py"
        
        backup_path.write_text(self.target_file.read_text(encoding="utf-8"), encoding="utf-8")
        return backup_path
    
    def _find_injection_point(self, source_lines: List[str], bug_type: str) -> Optional[int]:
        """Find suitable location to inject bug."""
        import re
        
        # For logic errors, find function definitions
        if bug_type == "logic_error":
            for i, line in enumerate(source_lines):
                if re.match(r"^\s*def\s+\w+\s*\([^)]*\)\s*:", line):
                    return i + 1  # Inject after function definition line
        
        # For syntax errors, find if statements
        elif bug_type == "syntax_error":
            for i, line in enumerate(source_lines):
                if re.match(r"^\s*if\s+", line) and ":" in line:
                    return i
        
        # For semantic errors, find variable usage
        elif bug_type == "semantic_error":
            for i, line in enumerate(source_lines):
                if "self.source_file" in line:
                    return i
        
        # Default: random location in middle of file
        return len(source_lines) // 2 if source_lines else None
    
    def _apply_bug_injection(
        self,
        source_lines: List[str],
        bug_def: Dict,
        location: int,
        bug_type: str,
        bug_name: str,
    ) -> List[str]:
        """Apply bug injection to source lines."""
        import re
        
        modified_lines = source_lines.copy()
        
        if bug_name == "if_true_return_false":
            # Insert after function definition
            indent = "    "  # Default indent
            if location < len(modified_lines):
                # Match indentation of next line
                next_line = modified_lines[location] if location < len(modified_lines) else ""
                indent_match = re.match(r"^(\s*)", next_line)
                if indent_match:
                    indent = indent_match.group(1) + "    "
            
            bug_code = f"{indent}if True:\n{indent}    return False\n"
            modified_lines.insert(location, bug_code)
        
        elif bug_name == "return_none":
            # Replace first return statement after location
            for i in range(location, len(modified_lines)):
                if re.search(r"return\s+", modified_lines[i]):
                    modified_lines[i] = re.sub(r"return\s+[^\n]+", "return None", modified_lines[i])
                    break
        
        elif bug_name == "missing_colon":
            # Remove colon from if statement
            if location < len(modified_lines):
                modified_lines[location] = modified_lines[location].rstrip().rstrip(":")
                if not modified_lines[location].endswith("\n"):
                    modified_lines[location] += "\n"
        
        elif bug_name == "wrong_variable":
            # Replace variable name
            if location < len(modified_lines):
                modified_lines[location] = re.sub(
                    r"\b(self\.source_file)\b", "self.wrong_variable", modified_lines[location]
                )
        
        return modified_lines
    
    def restore_backup(self, backup_path: Path) -> bool:
        """Restore from backup."""
        try:
            if backup_path.exists():
                self.target_file.write_text(backup_path.read_text(encoding="utf-8"), encoding="utf-8")
                return True
            return False
        except Exception:
            return False
