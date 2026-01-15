"""
Criticism Validator - Validate criticisms using evidence.

Collects evidence from code analysis, file system checks, and tests to
determine if a criticism is valid, invalid, partially valid, or cannot be verified.
"""

import re
import stat
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum

from .critique_parser import Criticism


class ValidationStatus(Enum):
    """Validation status for a criticism."""
    VALID = "valid"
    INVALID = "invalid"
    PARTIALLY_VALID = "partially_valid"
    CANNOT_VERIFY = "cannot_verify"


@dataclass
class Evidence:
    """Evidence collected for validation."""
    
    source: str  # "code_analysis", "file_system", "test", "documentation"
    description: str
    supports: bool  # True if supports criticism, False if contradicts
    confidence: float  # 0.0 to 1.0
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationResult:
    """Result of validating a criticism."""
    
    criticism: Criticism
    status: ValidationStatus
    confidence: float  # 0.0 to 1.0
    evidence: List[Evidence] = field(default_factory=list)
    conclusion: Optional[str] = None
    recommendation: Optional[str] = None


class CriticismValidator:
    """Validate criticisms using evidence."""
    
    def __init__(self, project_path: Path):
        """
        Initialize criticism validator.
        
        Args:
            project_path: Path to project root
        """
        self.project_path = project_path
        self.src_path = project_path / "src"
    
    def validate_criticism(self, criticism: Criticism) -> ValidationResult:
        """
        Validate a single criticism.
        
        Args:
            criticism: Criticism to validate
            
        Returns:
            ValidationResult with status and evidence
        """
        result = ValidationResult(
            criticism=criticism,
            status=ValidationStatus.CANNOT_VERIFY,
            confidence=0.0
        )
        
        # Collect evidence based on criticism type
        if "path traversal" in criticism.issue.lower() or "path" in criticism.issue.lower():
            self._validate_path_traversal(criticism, result)
        elif "permission" in criticism.issue.lower() or "chmod" in criticism.issue.lower():
            self._validate_file_permissions(criticism, result)
        elif "command injection" in criticism.issue.lower() or "subprocess" in criticism.issue.lower():
            self._validate_command_injection(criticism, result)
        elif "access control" in criticism.issue.lower() or "authorization" in criticism.issue.lower():
            self._validate_access_control(criticism, result)
        elif "error handling" in criticism.issue.lower() or "try/except" in criticism.issue.lower():
            self._validate_error_handling(criticism, result)
        elif "input validation" in criticism.issue.lower():
            self._validate_input_validation(criticism, result)
        else:
            # Generic validation
            self._validate_generic(criticism, result)
        
        # Determine final status based on evidence
        self._determine_status(result)
        
        return result
    
    def _validate_path_traversal(self, criticism: Criticism, result: ValidationResult) -> None:
        """Validate path traversal vulnerability."""
        if not criticism.code_location:
            result.evidence.append(Evidence(
                source="code_analysis",
                description="No code location specified",
                supports=False,
                confidence=0.3
            ))
            return
        
        # Parse file path
        file_path = self._parse_file_path(criticism.code_location)
        if not file_path or not file_path.exists():
            result.evidence.append(Evidence(
                source="code_analysis",
                description=f"File not found: {criticism.code_location}",
                supports=False,
                confidence=0.2
            ))
            return
        
        # Read file and check for path validation
        try:
            content = file_path.read_text(encoding="utf-8")
            
            # Check for path validation
            has_validation = (
                "is_relative_to" in content or
                "resolve()" in content or
                "path traversal" in content.lower() or
                "_validate_path" in content
            )
            
            # Check for path construction that could be vulnerable
            vulnerable_patterns = [
                r"Path\([^)]+\)\s*/\s*[^/]+",  # Path construction
                r"\.join\([^)]+\)",  # os.path.join
            ]
            has_vulnerable_pattern = any(
                re.search(pattern, content) for pattern in vulnerable_patterns
            )
            
            if has_vulnerable_pattern and not has_validation:
                result.evidence.append(Evidence(
                    source="code_analysis",
                    description="Path construction found without validation",
                    supports=True,
                    confidence=0.8,
                    details={"file": str(file_path), "has_validation": False}
                ))
            elif has_validation:
                result.evidence.append(Evidence(
                    source="code_analysis",
                    description="Path validation found in code",
                    supports=False,
                    confidence=0.7,
                    details={"file": str(file_path), "has_validation": True}
                ))
        except Exception as e:
            result.evidence.append(Evidence(
                source="code_analysis",
                description=f"Error reading file: {e}",
                supports=False,
                confidence=0.1
            ))
    
    def _validate_file_permissions(self, criticism: Criticism, result: ValidationResult) -> None:
        """Validate file permissions issue."""
        if not criticism.code_location:
            # Check if it's about a specific file mentioned in issue
            file_match = re.search(r"`([^`]+\.(?:md|json|py))`", criticism.issue)
            if file_match:
                file_path = self.project_path / file_match.group(1)
            else:
                result.evidence.append(Evidence(
                    source="file_system",
                    description="No file specified for permission check",
                    supports=False,
                    confidence=0.3
                ))
                return
        else:
            file_path = self._parse_file_path(criticism.code_location)
        
        if not file_path or not file_path.exists():
            result.evidence.append(Evidence(
                source="file_system",
                description=f"File not found: {file_path}",
                supports=False,
                confidence=0.2
            ))
            return
        
        # Check actual file permissions
        try:
            file_stat = file_path.stat()
            mode = file_stat.st_mode
            permissions = stat.filemode(mode)
            
            # Check if world-readable (group or other have read)
            is_world_readable = bool(mode & (stat.S_IRGRP | stat.S_IROTH))
            
            if is_world_readable:
                result.evidence.append(Evidence(
                    source="file_system",
                    description=f"File is world-readable: {permissions}",
                    supports=True,
                    confidence=0.9,
                    details={"file": str(file_path), "permissions": permissions}
                ))
            else:
                result.evidence.append(Evidence(
                    source="file_system",
                    description=f"File has restrictive permissions: {permissions}",
                    supports=False,
                    confidence=0.7,
                    details={"file": str(file_path), "permissions": permissions}
                ))
        except Exception as e:
            result.evidence.append(Evidence(
                source="file_system",
                description=f"Error checking permissions: {e}",
                supports=False,
                confidence=0.1
            ))
        
        # Check if code sets permissions
        if criticism.code_location:
            file_path = self._parse_file_path(criticism.code_location)
            if file_path and file_path.exists():
                try:
                    content = file_path.read_text(encoding="utf-8")
                    has_chmod = "chmod" in content or ".chmod(" in content
                    
                    if not has_chmod:
                        result.evidence.append(Evidence(
                            source="code_analysis",
                            description="No chmod() calls found in code",
                            supports=True,
                            confidence=0.7,
                            details={"file": str(file_path)}
                        ))
                    else:
                        result.evidence.append(Evidence(
                            source="code_analysis",
                            description="chmod() calls found in code",
                            supports=False,
                            confidence=0.6,
                            details={"file": str(file_path)}
                        ))
                except Exception:
                    pass
    
    def _validate_command_injection(self, criticism: Criticism, result: ValidationResult) -> None:
        """Validate command injection vulnerability."""
        if not criticism.code_location:
            return
        
        file_path = self._parse_file_path(criticism.code_location)
        if not file_path or not file_path.exists():
            return
        
        try:
            content = file_path.read_text(encoding="utf-8")
            
            # Check for subprocess.run with shell=True
            has_shell_true = bool(re.search(r"subprocess\.run\([^)]*shell\s*=\s*True", content))
            
            # Check for subprocess.run with list args (safe)
            has_list_args = bool(re.search(r"subprocess\.run\(\[", content))
            
            if has_shell_true:
                result.evidence.append(Evidence(
                    source="code_analysis",
                    description="subprocess.run() with shell=True found",
                    supports=True,
                    confidence=0.9,
                    details={"file": str(file_path)}
                ))
            elif has_list_args:
                result.evidence.append(Evidence(
                    source="code_analysis",
                    description="subprocess.run() with list args (safe)",
                    supports=False,
                    confidence=0.8,
                    details={"file": str(file_path)}
                ))
        except Exception as e:
            result.evidence.append(Evidence(
                source="code_analysis",
                description=f"Error reading file: {e}",
                supports=False,
                confidence=0.1
            ))
    
    def _validate_access_control(self, criticism: Criticism, result: ValidationResult) -> None:
        """Validate access control issue."""
        if not criticism.code_location:
            return
        
        file_path = self._parse_file_path(criticism.code_location)
        if not file_path or not file_path.exists():
            return
        
        try:
            content = file_path.read_text(encoding="utf-8")
            
            # Check for validation/authorization
            has_validation = (
                "validate" in content.lower() or
                "authorize" in content.lower() or
                "permission" in content.lower() or
                "access" in content.lower()
            )
            
            # Check for being_id or user input in function signatures
            has_user_input = bool(re.search(r"def\s+\w+\([^)]*(?:being_id|user_id|user_input)", content))
            
            if has_user_input and not has_validation:
                result.evidence.append(Evidence(
                    source="code_analysis",
                    description="User input found without validation",
                    supports=True,
                    confidence=0.7,
                    details={"file": str(file_path)}
                ))
            elif has_validation:
                result.evidence.append(Evidence(
                    source="code_analysis",
                    description="Validation/authorization found",
                    supports=False,
                    confidence=0.6,
                    details={"file": str(file_path)}
                ))
        except Exception:
            pass
    
    def _validate_error_handling(self, criticism: Criticism, result: ValidationResult) -> None:
        """Validate error handling issue."""
        if not criticism.code_location:
            return
        
        file_path = self._parse_file_path(criticism.code_location)
        if not file_path or not file_path.exists():
            return
        
        try:
            content = file_path.read_text(encoding="utf-8")
            
            # Check for try/except blocks
            has_try_except = "try:" in content and "except" in content
            
            # Check for file operations without error handling
            file_ops = ["open(", "write_text(", "read_text(", "mkdir("]
            has_file_ops = any(op in content for op in file_ops)
            
            if has_file_ops and not has_try_except:
                result.evidence.append(Evidence(
                    source="code_analysis",
                    description="File operations found without try/except",
                    supports=True,
                    confidence=0.6,
                    details={"file": str(file_path)}
                ))
            elif has_try_except:
                result.evidence.append(Evidence(
                    source="code_analysis",
                    description="Error handling found in code",
                    supports=False,
                    confidence=0.5,
                    details={"file": str(file_path)}
                ))
        except Exception:
            pass
    
    def _validate_input_validation(self, criticism: Criticism, result: ValidationResult) -> None:
        """Validate input validation issue."""
        # Similar to access control validation
        self._validate_access_control(criticism, result)
    
    def _validate_generic(self, criticism: Criticism, result: ValidationResult) -> None:
        """Generic validation for unknown criticism types."""
        # Try to find code location and check if it exists
        if criticism.code_location:
            file_path = self._parse_file_path(criticism.code_location)
            if file_path and file_path.exists():
                result.evidence.append(Evidence(
                    source="code_analysis",
                    description="Code file exists",
                    supports=True,
                    confidence=0.3,
                    details={"file": str(file_path)}
                ))
    
    def _parse_file_path(self, location: str) -> Optional[Path]:
        """Parse file path from code location string."""
        # Remove line numbers if present (e.g., "file.py:123")
        file_part = location.split(":")[0]
        
        # Try relative to project
        file_path = self.project_path / file_part
        if file_path.exists():
            return file_path
        
        # Try relative to src
        file_path = self.src_path / file_part
        if file_path.exists():
            return file_path
        
        # Try absolute
        file_path = Path(file_part)
        if file_path.exists():
            return file_path
        
        return None
    
    def _determine_status(self, result: ValidationResult) -> None:
        """Determine final validation status based on evidence."""
        if not result.evidence:
            result.status = ValidationStatus.CANNOT_VERIFY
            result.confidence = 0.0
            result.conclusion = "No evidence collected"
            return
        
        # Count supporting vs contradicting evidence
        supporting = [e for e in result.evidence if e.supports]
        contradicting = [e for e in result.evidence if not e.supports]
        
        # Calculate weighted confidence
        supporting_weight = sum(e.confidence for e in supporting)
        contradicting_weight = sum(e.confidence for e in contradicting)
        
        total_weight = supporting_weight + contradicting_weight
        
        if total_weight == 0:
            result.status = ValidationStatus.CANNOT_VERIFY
            result.confidence = 0.0
            return
        
        result.confidence = abs(supporting_weight - contradicting_weight) / total_weight
        
        if supporting_weight > contradicting_weight * 1.5:
            result.status = ValidationStatus.VALID
            result.conclusion = f"Evidence supports criticism ({len(supporting)} supporting, {len(contradicting)} contradicting)"
        elif contradicting_weight > supporting_weight * 1.5:
            result.status = ValidationStatus.INVALID
            result.conclusion = f"Evidence contradicts criticism ({len(contradicting)} contradicting, {len(supporting)} supporting)"
        elif supporting_weight > 0 and contradicting_weight > 0:
            result.status = ValidationStatus.PARTIALLY_VALID
            result.conclusion = f"Mixed evidence ({len(supporting)} supporting, {len(contradicting)} contradicting)"
        else:
            result.status = ValidationStatus.CANNOT_VERIFY
            result.conclusion = "Insufficient evidence to determine"
