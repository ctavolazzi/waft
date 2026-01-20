"""
Plan Loader - Load and parse plan markdown files.

Loads plans from ~/.cursor/plans/ or .cursor/plans/ directories,
parses markdown structure, and extracts plan metadata.
"""

import re
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class PlanSection:
    """Represents a section in a plan document."""
    
    title: str
    level: int  # Heading level (1-6)
    content: str
    subsections: List['PlanSection'] = field(default_factory=list)
    start_line: int = 0
    end_line: int = 0


@dataclass
class PlanData:
    """Structured data extracted from a plan document."""
    
    path: Path
    name: str
    overview: str
    content: str
    frontmatter: Dict[str, Any] = field(default_factory=dict)
    sections: List[PlanSection] = field(default_factory=list)
    todos: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def get_section(self, title: str) -> Optional[PlanSection]:
        """Get section by title (case-insensitive)."""
        for section in self.sections:
            if section.title.lower() == title.lower():
                return section
        return None
    
    def has_section(self, title: str) -> bool:
        """Check if plan has a section with given title."""
        return self.get_section(title) is not None


class PlanLoader:
    """Load and parse plan markdown files."""
    
    def __init__(self, project_path: Optional[Path] = None):
        """
        Initialize plan loader.
        
        Args:
            project_path: Path to project root (default: current directory)
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)
        
        self.project_path = project_path
        self.user_plans_dir = Path.home() / ".cursor" / "plans"
        self.project_plans_dir = project_path / ".cursor" / "plans"
    
    def find_most_recent_plan(self) -> Optional[Path]:
        """
        Find the most recently modified plan file.
        
        Returns:
            Path to most recent plan, or None if no plans found
        """
        plans = []
        
        # Check user-level plans
        if self.user_plans_dir.exists():
            plans.extend(self.user_plans_dir.glob("*.plan.md"))
            plans.extend(self.user_plans_dir.glob("*.md"))
        
        # Check project-level plans
        if self.project_plans_dir.exists():
            plans.extend(self.project_plans_dir.glob("*.plan.md"))
            plans.extend(self.project_plans_dir.glob("*.md"))
        
        if not plans:
            return None
        
        # Sort by modification time, most recent first
        plans.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        return plans[0]
    
    def find_plan_by_name(self, name: str) -> Optional[Path]:
        """
        Find plan by name (partial match).
        
        Args:
            name: Plan name to search for
            
        Returns:
            Path to plan, or None if not found
        """
        # Search user-level plans
        if self.user_plans_dir.exists():
            for plan_file in self.user_plans_dir.glob("*.plan.md"):
                if name.lower() in plan_file.stem.lower():
                    return plan_file
            for plan_file in self.user_plans_dir.glob("*.md"):
                if name.lower() in plan_file.stem.lower():
                    return plan_file
        
        # Search project-level plans
        if self.project_plans_dir.exists():
            for plan_file in self.project_plans_dir.glob("*.plan.md"):
                if name.lower() in plan_file.stem.lower():
                    return plan_file
            for plan_file in self.project_plans_dir.glob("*.md"):
                if name.lower() in plan_file.stem.lower():
                    return plan_file
        
        return None
    
    def load_plan(self, plan_path: Optional[Path] = None) -> PlanData:
        """
        Load and parse a plan file.
        
        Args:
            plan_path: Path to plan file (if None, finds most recent)
            
        Returns:
            PlanData with parsed plan content
            
        Raises:
            FileNotFoundError: If plan file not found
        """
        if plan_path is None:
            plan_path = self.find_most_recent_plan()
            if plan_path is None:
                raise FileNotFoundError("No plan files found")
        else:
            plan_path = Path(plan_path)
            if not plan_path.exists():
                raise FileNotFoundError(f"Plan file not found: {plan_path}")
        
        content = plan_path.read_text(encoding="utf-8")
        
        # Parse frontmatter
        frontmatter, markdown_content = self._parse_frontmatter(content)
        
        # Extract name from frontmatter or first heading
        name = frontmatter.get("name", "")
        if not name:
            first_heading = re.search(r'^#\s+(.+)$', markdown_content, re.MULTILINE)
            if first_heading:
                name = first_heading.group(1).strip()
            else:
                name = plan_path.stem.replace("_", " ").title()
        
        # Extract overview
        overview = frontmatter.get("overview", "")
        if not overview:
            # Try to extract from Overview section
            overview_match = re.search(
                r'^##\s+Overview\s*\n\n(.+?)(?=\n##|\Z)',
                markdown_content,
                re.MULTILINE | re.DOTALL
            )
            if overview_match:
                overview = overview_match.group(1).strip()
        
        # Parse sections
        sections = self._parse_sections(markdown_content)
        
        # Extract todos
        todos = self._extract_todos(markdown_content)
        
        # Extract metadata
        metadata = {
            "path": str(plan_path),
            "filename": plan_path.name,
            "modified_time": datetime.fromtimestamp(plan_path.stat().st_mtime).isoformat(),
        }
        metadata.update(frontmatter)
        
        return PlanData(
            path=plan_path,
            name=name,
            overview=overview,
            content=markdown_content,
            frontmatter=frontmatter,
            sections=sections,
            todos=todos,
            metadata=metadata
        )
    
    def _parse_frontmatter(self, content: str) -> tuple[Dict[str, Any], str]:
        """
        Parse YAML frontmatter from markdown.
        
        Args:
            content: Markdown content with optional frontmatter
            
        Returns:
            Tuple of (frontmatter dict, markdown content without frontmatter)
        """
        frontmatter_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
        if frontmatter_match:
            try:
                frontmatter = yaml.safe_load(frontmatter_match.group(1))
                if frontmatter is None:
                    frontmatter = {}
                markdown_content = content[frontmatter_match.end():].strip()
                return frontmatter, markdown_content
            except Exception:
                pass
        
        return {}, content.strip()
    
    def _parse_sections(self, content: str) -> List[PlanSection]:
        """
        Parse markdown sections from content.
        
        Args:
            content: Markdown content
            
        Returns:
            List of PlanSection objects
        """
        sections = []
        lines = content.split('\n')
        current_section = None
        current_content = []
        current_line = 0
        
        for i, line in enumerate(lines):
            # Check for heading
            heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if heading_match:
                # Save previous section
                if current_section is not None:
                    current_section.content = '\n'.join(current_content).strip()
                    current_section.end_line = i - 1
                    sections.append(current_section)
                
                # Start new section
                level = len(heading_match.group(1))
                title = heading_match.group(2).strip()
                current_section = PlanSection(
                    title=title,
                    level=level,
                    content="",
                    start_line=i
                )
                current_content = []
            else:
                if current_section is not None:
                    current_content.append(line)
                current_line = i
        
        # Save last section
        if current_section is not None:
            current_section.content = '\n'.join(current_content).strip()
            current_section.end_line = current_line
            sections.append(current_section)
        
        return sections
    
    def _extract_todos(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract todos from markdown content.
        
        Args:
            content: Markdown content
            
        Returns:
            List of todo dictionaries
        """
        todos = []
        
        # Match markdown checkboxes: - [ ] or - [x] or * [ ] etc.
        todo_pattern = r'^[-*]\s+\[([ xX])\]\s+(.+)$'
        
        for match in re.finditer(todo_pattern, content, re.MULTILINE):
            checked = match.group(1).strip().lower() == 'x'
            todo_text = match.group(2).strip()
            
            todos.append({
                "text": todo_text,
                "checked": checked,
                "line": content[:match.start()].count('\n') + 1
            })
        
        return todos
