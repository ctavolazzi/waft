"""
Refinement Detector: Finds polish opportunities without redesign.

Refinement is the art of:
- Observing code with intention to improve
- Polishing rough edges, fixing cracks, repairing broken parts
- Preserving essence - keeping the whole intact
- Improving incrementally - small, safe changes
- NOT redesigning - maintaining architecture and structure
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from pathlib import Path
import ast
import re

from .problem_detector import Problem, ProblemType, Severity


@dataclass
class RefinementOpportunity:
    """An opportunity to refine code without changing essence."""
    type: str  # "dead_code", "inconsistent_pattern", "needs_polish", "crack", "rough_edge"
    severity: Severity
    description: str
    file_path: Optional[Path] = None
    line_number: Optional[int] = None
    context: Dict[str, Any] = None
    preserves_essence: bool = True  # Refinement always preserves essence
    
    def to_problem(self) -> Problem:
        """Convert refinement opportunity to Problem."""
        problem_type_map = {
            "dead_code": ProblemType.BROKEN_PART,
            "inconsistent_pattern": ProblemType.ROUGH_EDGE,
            "needs_polish": ProblemType.ROUGH_EDGE,
            "crack": ProblemType.CRACK,
            "rough_edge": ProblemType.ROUGH_EDGE
        }
        
        return Problem(
            type=problem_type_map.get(self.type, ProblemType.ROUGH_EDGE),
            severity=self.severity,
            description=self.description,
            context={
                "refinement_type": self.type,
                "file_path": str(self.file_path) if self.file_path else None,
                "line_number": self.line_number,
                **(self.context or {})
            }
        )


class RefinementDetector:
    """Detects opportunities for polish without redesign."""
    
    def __init__(self):
        """Initialize refinement detector."""
        self.detected_opportunities: List[RefinementOpportunity] = []
    
    def detect_rough_edges(self, code: str, file_path: Optional[Path] = None) -> List[RefinementOpportunity]:
        """
        Find polish opportunities that preserve essence.
        
        Args:
            code: Source code to analyze
            file_path: Optional file path for context
        
        Returns:
            List of refinement opportunities
        """
        opportunities = []
        
        # Dead code detection
        dead_code = self._detect_dead_code(code, file_path)
        opportunities.extend(dead_code)
        
        # Inconsistent patterns
        inconsistent = self._detect_inconsistent_patterns(code, file_path)
        opportunities.extend(inconsistent)
        
        # Needs polish (formatting, naming, docs)
        polish = self._detect_polish_needs(code, file_path)
        opportunities.extend(polish)
        
        # Cracks (small bugs/inconsistencies)
        cracks = self._detect_cracks(code, file_path)
        opportunities.extend(cracks)
        
        self.detected_opportunities.extend(opportunities)
        return opportunities
    
    def _detect_dead_code(self, code: str, file_path: Optional[Path] = None) -> List[RefinementOpportunity]:
        """Detect unused code, dead imports, etc."""
        opportunities = []
        
        try:
            tree = ast.parse(code)
            
            # Find unused imports (simplified - would need full analysis)
            imports = [node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
            
            # Find defined but potentially unused functions/classes
            # (This is simplified - full analysis would track usage)
            definitions = [
                node for node in ast.walk(tree)
                if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef))
            ]
            
            # Simple heuristic: functions/classes that start with underscore might be unused
            for node in definitions:
                if node.name.startswith("_") and not node.name.startswith("__"):
                    opportunities.append(RefinementOpportunity(
                        type="dead_code",
                        severity=Severity.LOW,
                        description=f"Potentially unused: {node.name} (starts with _)",
                        file_path=file_path,
                        line_number=node.lineno,
                        context={"name": node.name, "type": type(node).__name__}
                    ))
        
        except SyntaxError:
            # Can't parse - might be a crack (syntax issue)
            opportunities.append(RefinementOpportunity(
                type="crack",
                severity=Severity.MEDIUM,
                description="Syntax error - code cannot be parsed",
                file_path=file_path,
                context={"error": "SyntaxError"}
            ))
        
        return opportunities
    
    def _detect_inconsistent_patterns(self, code: str, file_path: Optional[Path] = None) -> List[RefinementOpportunity]:
        """Detect inconsistent naming, formatting, patterns."""
        opportunities = []
        lines = code.split('\n')
        
        # Check for inconsistent naming (snake_case vs camelCase)
        snake_case_pattern = re.compile(r'\b[a-z]+(_[a-z]+)+\b')
        camel_case_pattern = re.compile(r'\b[a-z]+[A-Z][a-zA-Z]*\b')
        
        for i, line in enumerate(lines, 1):
            # Skip comments and strings
            if line.strip().startswith('#') or '"""' in line or "'''" in line:
                continue
            
            # Check for mixed naming in variable assignments
            if '=' in line:
                if snake_case_pattern.search(line) and camel_case_pattern.search(line):
                    opportunities.append(RefinementOpportunity(
                        type="inconsistent_pattern",
                        severity=Severity.LOW,
                        description="Mixed naming conventions (snake_case and camelCase)",
                        file_path=file_path,
                        line_number=i,
                        context={"line": line.strip()[:80]}
                    ))
        
        return opportunities
    
    def _detect_polish_needs(self, code: str, file_path: Optional[Path] = None) -> List[RefinementOpportunity]:
        """Detect needs for formatting, docstrings, type hints."""
        opportunities = []
        
        try:
            tree = ast.parse(code)
            
            # Find functions/classes without docstrings
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                    if not ast.get_docstring(node):
                        opportunities.append(RefinementOpportunity(
                            type="needs_polish",
                            severity=Severity.LOW,
                            description=f"Missing docstring: {node.name}",
                            file_path=file_path,
                            line_number=node.lineno,
                            context={"name": node.name, "type": type(node).__name__}
                        ))
                
                # Find functions without type hints (simplified check)
                if isinstance(node, ast.FunctionDef):
                    if not node.returns and not any(
                        arg.annotation for arg in node.args.args
                    ):
                        # No return type and no parameter types
                        opportunities.append(RefinementOpportunity(
                            type="needs_polish",
                            severity=Severity.LOW,
                            description=f"Missing type hints: {node.name}",
                            file_path=file_path,
                            line_number=node.lineno,
                            context={"name": node.name}
                        ))
        
        except SyntaxError:
            pass  # Already handled in dead_code detection
        
        return opportunities
    
    def _detect_cracks(self, code: str, file_path: Optional[Path] = None) -> List[RefinementOpportunity]:
        """Detect small bugs, inconsistencies, edge cases."""
        opportunities = []
        lines = code.split('\n')
        
        # Check for bare except clauses (crack - should be specific)
        for i, line in enumerate(lines, 1):
            if re.search(r'except\s*:', line):
                opportunities.append(RefinementOpportunity(
                    type="crack",
                    severity=Severity.MEDIUM,
                    description="Bare except clause - should catch specific exceptions",
                    file_path=file_path,
                    line_number=i,
                    context={"line": line.strip()[:80]}
                ))
            
            # Check for print() statements (might want logging)
            if re.search(r'\bprint\s*\(', line) and not line.strip().startswith('#'):
                opportunities.append(RefinementOpportunity(
                    type="crack",
                    severity=Severity.LOW,
                    description="print() statement - consider using logging",
                    file_path=file_path,
                    line_number=i,
                    context={"line": line.strip()[:80]}
                ))
        
        return opportunities
    
    def scan_file(self, file_path: Path) -> List[RefinementOpportunity]:
        """Scan a file for refinement opportunities."""
        try:
            code = file_path.read_text(encoding='utf-8')
            return self.detect_rough_edges(code, file_path)
        except Exception as e:
            # File can't be read - might be a crack
            return [RefinementOpportunity(
                type="crack",
                severity=Severity.MEDIUM,
                description=f"Cannot read file: {e}",
                file_path=file_path,
                context={"error": str(e)}
            )]
    
    def scan_directory(self, directory: Path, pattern: str = "*.py") -> List[RefinementOpportunity]:
        """Scan directory for refinement opportunities."""
        opportunities = []
        
        for file_path in directory.rglob(pattern):
            if file_path.is_file():
                file_opportunities = self.scan_file(file_path)
                opportunities.extend(file_opportunities)
        
        return opportunities
