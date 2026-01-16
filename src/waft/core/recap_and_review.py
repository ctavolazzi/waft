"""
Recap and Review - Mindspace documentation and PDF generation.

Captures the complete mindspace of the current moment, generates a review document,
and opens it as a PDF on the desktop.
"""

import re
import subprocess
import platform
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .session_stats import SessionStats
from .github import GitHubManager
from .memory import MemoryManager


class RecapAndReviewManager:
    """Manages mindspace documentation and review PDF generation."""
    
    def __init__(self, project_path: Path):
        """
        Initialize recap and review manager.
        
        Args:
            project_path: Path to project root
        """
        self.project_path = project_path
        self.console = Console()
        self.stats_tracker = SessionStats(project_path)
        self.github = GitHubManager(project_path)
        self.memory = MemoryManager(project_path)
        self.output_dir = project_path / "_work_efforts"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def run_recap_and_review(
        self,
        output_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Run recap and review workflow - capture mindspace and generate PDF.
        
        Args:
            output_path: Optional custom output path
            
        Returns:
            Dictionary with results
        """
        self.console.print("\n[bold cyan]📋 Recap and Review: Mindspace Documentation[/bold cyan]\n")
        
        # Step 1: Gather mindspace data
        mindspace_data = self._gather_mindspace_data()
        
        # Step 2: Generate mindspace document
        markdown_content = self._generate_mindspace_document(mindspace_data)
        
        # Step 3: Save markdown
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
        if output_path:
            md_file = Path(output_path)
        else:
            md_file = self.output_dir / f"MINDSPACE_REVIEW_{timestamp}.md"
        
        md_file.write_text(markdown_content, encoding="utf-8")
        
        # Step 4: Generate PDF
        pdf_file = self._generate_pdf(md_file, timestamp)
        
        # Step 5: Open PDF on desktop
        if pdf_file and pdf_file.exists():
            self._open_pdf_on_desktop(pdf_file)
        
        # Display summary
        self._display_summary(mindspace_data, md_file, pdf_file)
        
        return {
            "success": True,
            "markdown_file": str(md_file.relative_to(self.project_path)),
            "pdf_file": str(pdf_file.relative_to(self.project_path)) if pdf_file else None,
            "mindspace_data": mindspace_data,
        }
    
    def _gather_mindspace_data(self) -> Dict[str, Any]:
        """Gather complete mindspace data."""
        data = {
            "moment": {
                "timestamp": datetime.now().isoformat(),
                "date": datetime.now().strftime("%Y-%m-%d"),
                "time": datetime.now().strftime("%H:%M"),
                "day_of_week": datetime.now().strftime("%A"),
            },
            "current_state": {},
            "thoughts": [],
            "context": {},
            "decisions": [],
            "work_in_progress": [],
            "questions": [],
            "next_steps": [],
            "reflections": [],
        }
        
        # Git status
        git_info = {
            "initialized": self.github.is_initialized(),
            "branch": "unknown",
            "uncommitted_count": 0,
            "uncommitted_files": [],
        }
        
        if git_info["initialized"]:
            try:
                result = subprocess.run(
                    ["git", "branch", "--show-current"],
                    cwd=self.project_path,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if result.returncode == 0:
                    git_info["branch"] = result.stdout.strip()
                
                result = subprocess.run(
                    ["git", "status", "--porcelain"],
                    cwd=self.project_path,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if result.returncode == 0:
                    uncommitted = [line[3:].strip() for line in result.stdout.strip().split("\n") if line.strip()]
                    git_info["uncommitted_files"] = uncommitted[:20]
                    git_info["uncommitted_count"] = len(uncommitted)
            except Exception:
                pass
        
        data["context"]["git"] = git_info
        
        # Session stats
        try:
            stats = self.stats_tracker.calculate_session_stats()
            data["current_state"]["stats"] = {
                "files_created": stats.get("files", {}).get("created", 0),
                "files_modified": stats.get("files", {}).get("modified", 0),
                "lines_written": stats.get("code", {}).get("lines_written", 0),
                "lines_deleted": stats.get("code", {}).get("lines_deleted", 0),
                "net_lines": stats.get("code", {}).get("lines_written", 0) - stats.get("code", {}).get("lines_deleted", 0),
            }
        except Exception:
            data["current_state"]["stats"] = {}
        
        # Active files
        try:
            active_files = self.memory.get_active_files()
            data["work_in_progress"] = [{"file": str(f.name), "path": str(f)} for f in active_files[:10]]
        except Exception:
            pass
        
        # Extract thoughts from context (placeholder - would analyze conversation)
        data["thoughts"] = [
            "Current work session in progress",
            "Multiple files and systems active",
            "Focus on documentation and review",
        ]
        
        # Extract decisions (placeholder - would analyze conversation)
        data["decisions"] = [
            "Proceeding with recap and review generation",
            "Using PDF format for review document",
        ]
        
        # Extract questions (placeholder - would analyze conversation)
        data["questions"] = [
            "What are the next priorities?",
            "What needs immediate attention?",
        ]
        
        # Next steps
        data["next_steps"] = [
            "Review generated mindspace document",
            "Continue with planned work",
            "Update goals if needed",
        ]
        
        # Reflections
        data["reflections"] = [
            "Capturing mindspace helps preserve context",
            "PDF format enables easy review",
        ]
        
        return data
    
    def _generate_mindspace_document(self, mindspace_data: Dict[str, Any]) -> str:
        """Generate mindspace markdown document."""
        content = []
        
        # Title
        content.append("# Mindspace Review\n\n")
        content.append(f"**Captured**: {mindspace_data['moment']['date']} {mindspace_data['moment']['time']}\n")
        content.append(f"**Day**: {mindspace_data['moment']['day_of_week']}\n")
        content.append(f"**Timestamp**: {mindspace_data['moment']['timestamp']}\n\n")
        content.append("---\n\n")
        
        # Current State
        content.append("## Current State\n\n")
        stats = mindspace_data["current_state"].get("stats", {})
        if stats:
            content.append("### Activity Statistics\n\n")
            if stats.get("files_created", 0) > 0:
                content.append(f"- **Files Created**: {stats['files_created']}\n")
            if stats.get("files_modified", 0) > 0:
                content.append(f"- **Files Modified**: {stats['files_modified']}\n")
            if stats.get("lines_written", 0) > 0:
                content.append(f"- **Lines Written**: {stats['lines_written']:,}\n")
            if stats.get("net_lines", 0) != 0:
                content.append(f"- **Net Lines**: {stats['net_lines']:+,}\n")
            content.append("\n")
        
        git_info = mindspace_data["context"].get("git", {})
        if git_info.get("initialized"):
            content.append("### Git Status\n\n")
            content.append(f"- **Branch**: {git_info.get('branch', 'unknown')}\n")
            content.append(f"- **Uncommitted Files**: {git_info.get('uncommitted_count', 0)}\n")
            if git_info.get("uncommitted_files"):
                content.append("\n**Modified/Created Files**:\n\n")
                for file in git_info["uncommitted_files"][:10]:
                    content.append(f"- `{file}`\n")
            content.append("\n")
        
        # Thoughts
        if mindspace_data["thoughts"]:
            content.append("## Thoughts\n\n")
            for thought in mindspace_data["thoughts"]:
                content.append(f"- {thought}\n")
            content.append("\n")
        
        # Context
        content.append("## Context\n\n")
        content.append("### Work Environment\n\n")
        content.append(f"- **Project Path**: `{self.project_path}`\n")
        content.append(f"- **Branch**: {git_info.get('branch', 'unknown')}\n")
        content.append("\n")
        
        # Decisions
        if mindspace_data["decisions"]:
            content.append("## Decisions\n\n")
            for decision in mindspace_data["decisions"]:
                content.append(f"- {decision}\n")
            content.append("\n")
        
        # Work in Progress
        if mindspace_data["work_in_progress"]:
            content.append("## Work in Progress\n\n")
            for item in mindspace_data["work_in_progress"]:
                content.append(f"- `{item.get('file', item.get('path', 'unknown'))}`\n")
            content.append("\n")
        
        # Questions
        if mindspace_data["questions"]:
            content.append("## Questions\n\n")
            for question in mindspace_data["questions"]:
                content.append(f"- {question}\n")
            content.append("\n")
        
        # Next Steps
        if mindspace_data["next_steps"]:
            content.append("## Next Steps\n\n")
            for i, step in enumerate(mindspace_data["next_steps"], 1):
                content.append(f"{i}. {step}\n")
            content.append("\n")
        
        # Reflections
        if mindspace_data["reflections"]:
            content.append("## Reflections\n\n")
            for reflection in mindspace_data["reflections"]:
                content.append(f"- {reflection}\n")
            content.append("\n")
        
        return "".join(content)
    
    def _generate_pdf(self, md_file: Path, timestamp: str) -> Optional[Path]:
        """Generate PDF from markdown document."""
        try:
            # Try using pandoc if available
            pdf_file = self.output_dir / f"MINDSPACE_REVIEW_{timestamp}.pdf"
            
            result = subprocess.run(
                ["pandoc", str(md_file), "-o", str(pdf_file), "--pdf-engine=xelatex"],
                capture_output=True,
                text=True,
                check=False,
            )
            
            if result.returncode == 0 and pdf_file.exists():
                return pdf_file
            
            # Fallback: Use weasyprint or markdown-pdf
            try:
                from weasyprint import HTML
                import markdown
                
                # Convert markdown to HTML
                md_content = md_file.read_text()
                html_content = markdown.markdown(md_content)
                html_doc = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <style>
                        body {{ font-family: 'Georgia', serif; margin: 2cm; line-height: 1.6; }}
                        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
                        h2 {{ color: #34495e; margin-top: 30px; border-bottom: 2px solid #95a5a6; padding-bottom: 5px; }}
                        h3 {{ color: #7f8c8d; margin-top: 20px; }}
                        code {{ background: #ecf0f1; padding: 2px 6px; border-radius: 3px; }}
                        ul, ol {{ margin-left: 20px; }}
                    </style>
                </head>
                <body>
                    {html_content}
                </body>
                </html>
                """
                
                HTML(string=html_doc).write_pdf(pdf_file)
                return pdf_file
            except (ImportError, Exception) as e:
                self.console.print(f"[yellow]⚠️  WeasyPrint fallback failed: {e}[/yellow]")
                pass
            
            # If PDF generation fails, return None
            self.console.print("[yellow]⚠️  PDF generation not available. Markdown saved.[/yellow]")
            return None
            
        except Exception as e:
            self.console.print(f"[yellow]⚠️  PDF generation error: {e}[/yellow]")
            return None
    
    def _open_pdf_on_desktop(self, pdf_path: Path) -> bool:
        """Open PDF on desktop using system command."""
        try:
            system = platform.system()
            if system == "Darwin":  # macOS
                subprocess.run(["open", str(pdf_path)], check=True)
            elif system == "Windows":
                subprocess.run(["start", str(pdf_path)], shell=True, check=True)
            else:  # Linux
                subprocess.run(["xdg-open", str(pdf_path)], check=True)
            
            self.console.print(f"[green]🖥️  Opened PDF on desktop[/green]")
            return True
        except Exception as e:
            self.console.print(f"[yellow]⚠️  Could not open PDF: {e}[/yellow]")
            return False
    
    def _display_summary(self, mindspace_data: Dict[str, Any], md_file: Path, pdf_file: Optional[Path]):
        """Display recap and review summary."""
        self.console.print("[bold]📋 Recap and Review Summary[/bold]\n")
        self.console.print(f"  • Moment: {mindspace_data['moment']['date']} {mindspace_data['moment']['time']}")
        self.console.print(f"  • Thoughts: {len(mindspace_data['thoughts'])} captured")
        self.console.print(f"  • Decisions: {len(mindspace_data['decisions'])} documented")
        self.console.print(f"  • Work in Progress: {len(mindspace_data['work_in_progress'])} items")
        self.console.print(f"  • Questions: {len(mindspace_data['questions'])} open")
        
        self.console.print(f"\n[bold green]✅ Markdown saved:[/bold green] {md_file.relative_to(self.project_path)}")
        if pdf_file:
            self.console.print(f"[bold green]✅ PDF generated:[/bold green] {pdf_file.relative_to(self.project_path)}")
            self.console.print(f"[bold green]🖥️  PDF opened on desktop[/bold green]\n")
        else:
            self.console.print(f"[yellow]⚠️  PDF not generated (markdown available)[/yellow]\n")
