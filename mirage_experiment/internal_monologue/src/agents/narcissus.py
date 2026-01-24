"""
Narcissus Agent - Self-Reflective Meta-Cognitive Agent

A self-modifying agent that can read its own source code and propose improvements.
This agent is restricted to only modifying itself - it cannot interact with the external world.
"""

import inspect
import re
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


class NarcissusAgent:
    """
    Self-reflective agent that can examine and modify its own source code.
    
    The agent has two core tools:
    1. read_own_source_code() - Reads its complete source code
    2. propose_self_improvement(diff) - Proposes and applies code changes
    """
    
    def __init__(self, source_file: Path, project_path: Path):
        """
        Initialize the Narcissus agent.
        
        Args:
            source_file: Path to the agent's source code file
            project_path: Path to project root
        """
        self.source_file = Path(source_file)
        self.project_path = Path(project_path)
        self.agent_id = f"narcissus_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.generation = 0
        self.modification_history = []
        
        # Ensure source file exists
        if not self.source_file.exists():
            raise FileNotFoundError(f"Source file not found: {self.source_file}")
    
    def read_own_source_code(self) -> str:
        """
        Read the complete source code of this agent.
        
        Returns:
            Full source code of narcissus.py as a string
        """
        try:
            return self.source_file.read_text(encoding="utf-8")
        except Exception as e:
            return f"Error reading source code: {e}"
    
    def propose_self_improvement(self, diff: str) -> Dict[str, Any]:
        """
        Propose a code change to improve this agent.
        
        Args:
            diff: Unified diff format string describing the change
            
        Returns:
            Dict with 'status', 'message', 'applied', 'validation_results' fields
        """
        result = {
            "status": "pending",
            "message": "",
            "applied": False,
            "validation_results": {},
            "timestamp": datetime.now().isoformat(),
        }
        
        try:
            # Step 1: Validate diff syntax
            validation = self._validate_diff(diff)
            result["validation_results"]["diff_syntax"] = validation
            
            if not validation["valid"]:
                result["status"] = "failed"
                result["message"] = f"Invalid diff syntax: {validation.get('error', 'Unknown error')}"
                return result
            
            # Step 2: Pre-application validation
            pre_validation = self._pre_validate_modification(diff)
            result["validation_results"]["pre_application"] = pre_validation
            
            if not pre_validation["safe"]:
                result["status"] = "failed"
                result["message"] = f"Modification not safe: {pre_validation.get('reason', 'Unknown reason')}"
                return result
            
            # Step 3: Create backup
            backup_path = self._create_backup()
            result["validation_results"]["backup_path"] = str(backup_path)
            
            # Step 4: Apply diff
            apply_result = self._apply_diff(diff)
            result["validation_results"]["apply_result"] = apply_result
            
            if not apply_result["success"]:
                # Rollback
                self._restore_backup(backup_path)
                result["status"] = "failed"
                result["message"] = f"Failed to apply diff: {apply_result.get('error', 'Unknown error')}"
                return result
            
            # Step 5: Post-application validation
            post_validation = self._post_validate_modification()
            result["validation_results"]["post_application"] = post_validation
            
            if not post_validation["valid"]:
                # Rollback
                self._restore_backup(backup_path)
                result["status"] = "failed"
                result["message"] = f"Post-validation failed: {post_validation.get('error', 'Unknown error')}"
                return result
            
            # Step 6: Success
            result["status"] = "success"
            result["applied"] = True
            result["message"] = "Modification applied successfully"
            self.generation += 1
            self.modification_history.append({
                "generation": self.generation,
                "diff": diff,
                "timestamp": datetime.now().isoformat(),
                "backup_path": str(backup_path),
            })
            
        except Exception as e:
            result["status"] = "error"
            result["message"] = f"Unexpected error: {str(e)}"
        
        return result
    
    def _validate_diff(self, diff: str) -> Dict[str, Any]:
        """Validate diff syntax."""
        # Basic unified diff format check
        if not diff.strip().startswith("---") and not diff.strip().startswith("@@"):
            return {"valid": False, "error": "Not a valid unified diff format"}
        
        # Check for dangerous patterns
        dangerous_patterns = [
            r"import\s+os\s*$",
            r"import\s+subprocess\s*$",
            r"eval\s*\(",
            r"exec\s*\(",
            r"__import__\s*\(",
            r"open\s*\([^)]*['\"][^'\"]*['\"]",
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, diff, re.MULTILINE):
                return {"valid": False, "error": f"Dangerous pattern detected: {pattern}"}
        
        return {"valid": True}
    
    def _pre_validate_modification(self, diff: str) -> Dict[str, Any]:
        """Pre-application validation - check if modification is safe."""
        # Check that diff only modifies self.source_file
        if "+++" in diff:
            lines = diff.split("\n")
            for line in lines:
                if line.startswith("+++"):
                    file_path = line[4:].strip().split("\t")[0]
                    if file_path != str(self.source_file.name) and file_path != "/dev/null":
                        return {"safe": False, "reason": f"Diff modifies file other than {self.source_file.name}"}
        
        return {"safe": True}
    
    def _post_validate_modification(self) -> Dict[str, Any]:
        """Post-application validation - check if modified code is valid Python."""
        try:
            # Try to parse the modified file
            source_code = self.source_file.read_text(encoding="utf-8")
            
            # Syntax check using Python's compile
            compile(source_code, str(self.source_file), "exec")
            
            # Try to import the module (basic check)
            # We'll skip this for now as it's complex with dynamic imports
            
            return {"valid": True}
        except SyntaxError as e:
            return {"valid": False, "error": f"Syntax error: {str(e)}"}
        except Exception as e:
            return {"valid": False, "error": f"Validation error: {str(e)}"}
    
    def _create_backup(self) -> Path:
        """Create a backup of the current source file."""
        backup_dir = self.project_path / "_pyrite" / "backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"{self.source_file.stem}_backup_{timestamp}.py"
        
        backup_path.write_text(self.source_file.read_text(encoding="utf-8"), encoding="utf-8")
        return backup_path
    
    def _restore_backup(self, backup_path: Path) -> bool:
        """Restore from backup."""
        try:
            if backup_path.exists():
                self.source_file.write_text(backup_path.read_text(encoding="utf-8"), encoding="utf-8")
                return True
            return False
        except Exception:
            return False
    
    def _apply_diff(self, diff: str) -> Dict[str, Any]:
        """Apply unified diff to source file."""
        try:
            # Read current source
            source_lines = self.source_file.read_text(encoding="utf-8").splitlines(keepends=True)
            
            # Parse diff (simplified - assumes unified diff format)
            # For a full implementation, we'd use a proper diff library
            # For now, we'll use a simple approach with patch command if available
            
            # Try using system patch command
            with tempfile.NamedTemporaryFile(mode="w", suffix=".diff", delete=False) as diff_file:
                diff_file.write(diff)
                diff_file_path = diff_file.name
            
            try:
                # Apply patch
                result = subprocess.run(
                    ["patch", "-p1", str(self.source_file), diff_file_path],
                    capture_output=True,
                    text=True,
                    cwd=self.source_file.parent,
                )
                
                if result.returncode == 0:
                    return {"success": True}
                else:
                    return {"success": False, "error": result.stderr}
            except FileNotFoundError:
                # patch command not available, use manual diff application
                return self._apply_diff_manual(diff, source_lines)
            finally:
                Path(diff_file_path).unlink(missing_ok=True)
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _apply_diff_manual(self, diff: str, source_lines: list) -> Dict[str, Any]:
        """Manually apply diff (fallback if patch command unavailable)."""
        # This is a simplified implementation
        # A full implementation would properly parse unified diff format
        # For now, return error suggesting patch command
        return {
            "success": False,
            "error": "Manual diff application not fully implemented. Install 'patch' command or use a diff library.",
        }
    
    def get_genome_id(self) -> str:
        """Get current genome ID (hash of source code)."""
        import hashlib
        
        source_code = self.source_file.read_text(encoding="utf-8")
        return hashlib.sha256(source_code.encode()).hexdigest()[:16]
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status."""
        return {
            "agent_id": self.agent_id,
            "generation": self.generation,
            "genome_id": self.get_genome_id(),
            "source_file": str(self.source_file),
            "modifications_count": len(self.modification_history),
        }
