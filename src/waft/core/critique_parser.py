"""
Critique Parser - Parse critique markdown documents.

Extracts structured data from critique markdown documents, including
criticisms with severity levels, recommended fixes, and code locations.
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field


@dataclass
class Criticism:
    """Represents a single criticism from a critique document."""
    
    title: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    issue: str
    attack_vector: Optional[str] = None
    impact: Optional[str] = None
    fix_required: Optional[str] = None
    code_fix: Optional[str] = None
    code_location: Optional[str] = None
    section: str = ""  # Which section of critique (Security, Assumptions, etc.)
    number: int = 0  # Number within section


@dataclass
class CritiqueData:
    """Structured data extracted from critique document."""
    
    date: Optional[str] = None
    time: Optional[str] = None
    plan_name: Optional[str] = None
    critique_mode: Optional[str] = None
    
    critical_vulnerabilities: List[Criticism] = field(default_factory=list)
    high_safety_issues: List[Criticism] = field(default_factory=list)
    medium_assumptions: List[Criticism] = field(default_factory=list)
    low_overengineering: List[Criticism] = field(default_factory=list)
    oversights: List[Criticism] = field(default_factory=list)
    missed_obviousness: List[Criticism] = field(default_factory=list)
    
    executive_summary: Optional[str] = None
    recommendations: Optional[str] = None
    
    def get_all_criticisms(self) -> List[Criticism]:
        """Get all criticisms in priority order."""
        all_criticisms = []
        all_criticisms.extend(self.critical_vulnerabilities)
        all_criticisms.extend(self.high_safety_issues)
        all_criticisms.extend(self.medium_assumptions)
        all_criticisms.extend(self.low_overengineering)
        all_criticisms.extend(self.oversights)
        all_criticisms.extend(self.missed_obviousness)
        return all_criticisms
    
    def get_by_severity(self, severity: str) -> List[Criticism]:
        """Get criticisms by severity level."""
        severity_map = {
            "CRITICAL": self.critical_vulnerabilities,
            "HIGH": self.high_safety_issues,
            "MEDIUM": self.medium_assumptions,
            "LOW": self.low_overengineering,
        }
        return severity_map.get(severity.upper(), [])


class CritiqueParser:
    """Parse critique markdown documents."""
    
    def __init__(self, project_path: Path):
        """
        Initialize critique parser.
        
        Args:
            project_path: Path to project root
        """
        self.project_path = project_path
    
    def parse_critique(self, critique_path: Path) -> CritiqueData:
        """
        Parse critique markdown document.
        
        Args:
            critique_path: Path to critique markdown file
            
        Returns:
            CritiqueData with extracted structured data
        """
        if not critique_path.exists():
            raise FileNotFoundError(f"Critique file not found: {critique_path}")
        
        content = critique_path.read_text(encoding="utf-8")
        
        data = CritiqueData()
        
        # Parse header/metadata
        self._parse_header(content, data)
        
        # Parse executive summary
        self._parse_executive_summary(content, data)
        
        # Parse sections
        self._parse_section(
            content,
            r"## 🔴 CRITICAL: Security Vulnerabilities",
            data.critical_vulnerabilities,
            "CRITICAL",
            "Security Vulnerabilities"
        )
        self._parse_section(
            content,
            r"## 🔴 HIGH: Safety Issues",
            data.high_safety_issues,
            "HIGH",
            "Safety Issues"
        )
        self._parse_section(
            content,
            r"## ⚠️ MEDIUM: Unexamined Assumptions",
            data.medium_assumptions,
            "MEDIUM",
            "Unexamined Assumptions"
        )
        self._parse_section(
            content,
            r"## ⚠️ LOW: Overengineering",
            data.low_overengineering,
            "LOW",
            "Overengineering"
        )
        self._parse_section(
            content,
            r"## ⚠️ Oversights",
            data.oversights,
            "MEDIUM",  # Oversights are typically medium severity
            "Oversights"
        )
        self._parse_section(
            content,
            r"## ⚠️ Missed Obviousness",
            data.missed_obviousness,
            "MEDIUM",  # Missed obviousness is typically medium severity
            "Missed Obviousness"
        )
        
        # Parse recommendations
        self._parse_recommendations(content, data)
        
        return data
    
    def _parse_header(self, content: str, data: CritiqueData) -> None:
        """Parse header/metadata from critique."""
        # Extract date
        date_match = re.search(r"\*\*Date\*\*:\s*(\d{4}-\d{2}-\d{2})", content)
        if date_match:
            data.date = date_match.group(1)
        
        # Extract time
        time_match = re.search(r"\*\*Time\*\*:\s*(\d{2}:\d{2}:\d{2})", content)
        if time_match:
            data.time = time_match.group(1)
        
        # Extract plan name
        plan_match = re.search(r"\*\*Plan\*\*:\s*(.+)", content)
        if plan_match:
            data.plan_name = plan_match.group(1).strip()
        
        # Extract critique mode
        mode_match = re.search(r"\*\*Critique Mode\*\*:\s*(.+)", content)
        if mode_match:
            data.critique_mode = mode_match.group(1).strip()
    
    def _parse_executive_summary(self, content: str, data: CritiqueData) -> None:
        """Parse executive summary section."""
        summary_match = re.search(
            r"## Executive Summary\s*\n\n(.*?)(?=\n## |\n---|$)",
            content,
            re.DOTALL
        )
        if summary_match:
            data.executive_summary = summary_match.group(1).strip()
    
    def _parse_section(
        self,
        content: str,
        section_header: str,
        criticisms_list: List[Criticism],
        default_severity: str,
        section_name: str
    ) -> None:
        """Parse a section of criticisms."""
        # Find section start
        section_pattern = f"{re.escape(section_header)}(.*?)(?=\n## |\n---|$)"
        section_match = re.search(section_pattern, content, re.DOTALL | re.IGNORECASE)
        
        if not section_match:
            return
        
        section_content = section_match.group(1)
        
        # Split into individual criticisms (numbered items)
        # Pattern: ### N. Title or ### Title
        criticism_pattern = r"### (\d+)\.\s+(.+?)(?=### \d+\.|### [A-Z]|$)"
        matches = list(re.finditer(criticism_pattern, section_content, re.DOTALL))
        
        if not matches:
            # Try pattern without numbers
            criticism_pattern = r"### (.+?)(?=### |$)"
            matches = list(re.finditer(criticism_pattern, section_content, re.DOTALL))
        
        for i, match in enumerate(matches, 1):
            criticism_text = match.group(0)
            
            # Extract title - handle both numbered and unnumbered formats
            if len(match.groups()) >= 2:
                # Numbered format: ### 1. Title
                title = match.group(2).split('\n')[0].strip()
            elif len(match.groups()) >= 1:
                # Unnumbered format: ### Title
                title = match.group(1).split('\n')[0].strip()
            else:
                # Fallback: extract from first line
                title = match.group(0).split('\n')[0].replace('###', '').strip()
            
            # Clean up title (remove number if present)
            title = re.sub(r'^\d+\.\s*', '', title).strip()
            
            criticism = self._parse_criticism(
                criticism_text,
                title,
                default_severity,
                section_name,
                i
            )
            if criticism:
                criticisms_list.append(criticism)
    
    def _parse_criticism(
        self,
        text: str,
        title: str,
        severity: str,
        section: str,
        number: int
    ) -> Optional[Criticism]:
        """Parse a single criticism from text."""
        # Extract issue description first (required field)
        issue_match = re.search(r"\*\*Issue\*\*:\s*(.+?)(?=\n\*\*|$)", text, re.DOTALL)
        if not issue_match:
            # Try alternative pattern
            issue_match = re.search(r"Issue[:\s]+(.+?)(?=\n\*\*|$)", text, re.DOTALL | re.IGNORECASE)
        
        if not issue_match:
            # Use title as issue if no issue found
            issue_text = title.strip()
        else:
            issue_text = issue_match.group(1).strip()
        
        criticism = Criticism(
            title=title.strip(),
            severity=severity,
            section=section,
            number=number,
            issue=issue_text
        )
        
        # Extract attack vector
        attack_match = re.search(r"\*\*Attack Vector\*\*:\s*(.+?)(?=\n\*\*|$)", text, re.DOTALL)
        if attack_match:
            criticism.attack_vector = attack_match.group(1).strip()
        
        # Extract impact
        impact_match = re.search(r"\*\*Impact\*\*:\s*(.+?)(?=\n\*\*|$)", text, re.DOTALL)
        if impact_match:
            criticism.impact = impact_match.group(1).strip()
        
        # Extract fix required
        fix_match = re.search(r"\*\*Fix Required\*\*:\s*(.+?)(?=\n\*\*|$)", text, re.DOTALL)
        if not fix_match:
            fix_match = re.search(r"\*\*Severity\*\*:.*?\n\*\*Fix Required\*\*:\s*(.+?)(?=\n\*\*|$)", text, re.DOTALL)
        if fix_match:
            criticism.fix_required = fix_match.group(1).strip()
        
        # Extract code fix (in code blocks)
        code_fix_match = re.search(r"```python\n(.*?)\n```", text, re.DOTALL)
        if code_fix_match:
            criticism.code_fix = code_fix_match.group(1).strip()
        
        # Extract code location
        location_match = re.search(r"`([^`]+\.py(?::\d+)?)`", text)
        if location_match:
            criticism.code_location = location_match.group(1)
        
        return criticism
    
    def _parse_recommendations(self, content: str, data: CritiqueData) -> None:
        """Parse recommendations section."""
        rec_match = re.search(
            r"## Recommendations.*?\n\n(.*?)(?=\n## |\n---|$)",
            content,
            re.DOTALL
        )
        if rec_match:
            data.recommendations = rec_match.group(1).strip()
