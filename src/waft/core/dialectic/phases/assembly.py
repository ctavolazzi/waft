"""
DIALECTIC Phase 1: THESIS (Assembly)

Gathers context, runs AI Town analysis, and comprehensive orchestration.
This is the "thesis" in the Hegelian dialectic - the initial proposition.
"""

import logging
import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import Any
import shutil

logger = logging.getLogger("Dialectic.Assembly")


class AssemblyPhase:
    """
    Assembly Phase - THESIS
    
    Responsibilities:
    1. Gather context (git status, work efforts, project state)
    2. Run AI Town analysis (spawn Beings for distributed analysis)
    3. Execute comprehensive orchestration
    4. Generate Assembly Report PDF
    """
    
    def __init__(self, project_path: Path, output_dir: Path):
        self.project_path = Path(project_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def run(self) -> dict[str, Any]:
        """Execute the Assembly phase."""
        logger.info("Starting THESIS (Assembly) Phase...")
        
        # 1. Gather Context
        context = self._gather_context()
        logger.info(f"Context gathered: {len(context)} items")
        
        # 2. Gather Git State
        git_state = self._gather_git_state()
        logger.info(f"Git state: {git_state.get('branch', 'unknown')}")
        
        # 3. Gather Work Efforts
        work_efforts = self._gather_work_efforts()
        logger.info(f"Work efforts found: {len(work_efforts)}")
        
        # 4. Generate Report
        report_data = {
            "phase": "thesis",
            "timestamp": self.timestamp,
            "context": context,
            "git_state": git_state,
            "work_efforts": work_efforts,
        }
        
        output_path = self._generate_report(report_data)
        
        return {
            "status": "success",
            "phase": "thesis",
            "output_path": str(output_path),
            "summary": {
                "context_items": len(context),
                "git_branch": git_state.get("branch"),
                "work_efforts": len(work_efforts),
            }
        }
        
    def _gather_context(self) -> dict[str, Any]:
        """Gather project context information."""
        context = {
            "project_path": str(self.project_path),
            "timestamp": datetime.now().isoformat(),
        }
        
        # Check for key files
        key_files = ["README.md", "AGENTS.md", "pyproject.toml", "VERSION.json"]
        context["key_files"] = {
            f: (self.project_path / f).exists() for f in key_files
        }
        
        # Check for key directories
        key_dirs = ["src", "_work_efforts", "_realms", "_pyrite"]
        context["key_directories"] = {
            d: (self.project_path / d).exists() for d in key_dirs
        }
        
        return context
        
    def _gather_git_state(self) -> dict[str, Any]:
        """Gather git repository state."""
        git_state = {
            "branch": "unknown",
            "status": [],
            "recent_commits": [],
        }
        
        try:
            # Get current branch
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                git_state["branch"] = result.stdout.strip()
                
            # Get status
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                git_state["status"] = result.stdout.strip().split("\n")[:20]  # Limit to 20
                
            # Get recent commits
            result = subprocess.run(
                ["git", "log", "--oneline", "-10"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                git_state["recent_commits"] = result.stdout.strip().split("\n")
                
        except Exception as e:
            logger.warning(f"Git state gathering failed: {e}")
            
        return git_state
        
    def _gather_work_efforts(self) -> list[dict[str, Any]]:
        """Gather active work efforts."""
        work_efforts = []
        we_dir = self.project_path / "_work_efforts"
        
        if we_dir.exists():
            for item in we_dir.iterdir():
                if item.is_dir() and item.name.startswith("WE-"):
                    index_file = item / "index.md"
                    if index_file.exists():
                        work_efforts.append({
                            "id": item.name,
                            "path": str(item),
                            "has_index": True,
                        })
                    else:
                        # Check for WE-*_index.md pattern
                        index_files = list(item.glob("*_index.md"))
                        work_efforts.append({
                            "id": item.name,
                            "path": str(item),
                            "has_index": len(index_files) > 0,
                        })
                        
        return work_efforts[:20]  # Limit to 20 most recent
        
    def _generate_report(self, data: dict[str, Any]) -> Path:
        """Generate the Assembly Report as a Typst document."""
        output_file = self.output_dir / f"assembly_report_{self.timestamp}.typ"
        
        content = f'''// DIALECTIC - Assembly Report (THESIS)
// Generated: {data["timestamp"]}

#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)

#align(center)[
  #text(18pt, weight: "bold")[DIALECTIC - ASSEMBLY REPORT]
  #v(0.3em)
  #text(14pt, fill: blue)[PHASE 1: THESIS]
  #v(0.3em)
  #text(10pt)[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]
]

#line(length: 100%, stroke: 0.5pt)

= 1. Context Summary

#table(
  columns: (1fr, 2fr),
  [*Project Path*], [{data["context"]["project_path"]}],
  [*Timestamp*], [{data["context"]["timestamp"]}],
)

== Key Files Present
{self._format_dict_as_typst_list(data["context"]["key_files"])}

== Key Directories Present
{self._format_dict_as_typst_list(data["context"]["key_directories"])}

= 2. Git State

#block(inset: 1em, stroke: (left: 3pt + blue))[
  *Branch:* {data["git_state"]["branch"]}
]

== Recent Commits
{self._format_list_as_typst(data["git_state"]["recent_commits"][:5])}

== Uncommitted Changes
{len([s for s in data["git_state"]["status"] if s])} files with changes

= 3. Work Efforts

*Total Active:* {len(data["work_efforts"])}

{self._format_work_efforts_as_typst(data["work_efforts"][:10])}

#v(2em)
#line(length: 100%, stroke: 0.5pt)
#align(center)[
  #text(8pt, fill: gray)[
    DIALECTIC Engine // Assembly Phase Complete \\
    Ready for ANTITHESIS (Sanity Check)
  ]
]
'''
        
        with open(output_file, "w") as f:
            f.write(content)
            
        # Try to compile to PDF
        pdf_path = self._compile_to_pdf(output_file)
        
        return pdf_path if pdf_path else output_file
        
    def _format_dict_as_typst_list(self, d: dict) -> str:
        """Format a dictionary as a Typst list."""
        lines = []
        for k, v in d.items():
            status = "✓" if v else "✗"
            lines.append(f"- {status} `{k}`")
        return "\n".join(lines) if lines else "- None"
        
    def _format_list_as_typst(self, items: list) -> str:
        """Format a list as Typst items."""
        if not items:
            return "- None"
        return "\n".join(f"- `{item}`" for item in items if item)
        
    def _format_work_efforts_as_typst(self, wes: list) -> str:
        """Format work efforts as Typst list."""
        if not wes:
            return "No active work efforts found."
        lines = []
        for we in wes:
            status = "✓" if we.get("has_index") else "○"
            lines.append(f"- {status} `{we['id']}`")
        return "\n".join(lines)
        
    def _compile_to_pdf(self, typ_file: Path) -> Path | None:
        """Compile Typst file to PDF if typst is available."""
        if not shutil.which("typst"):
            logger.warning("Typst not found - skipping PDF compilation")
            return None
            
        pdf_file = typ_file.with_suffix(".pdf")
        try:
            result = subprocess.run(
                ["typst", "compile", str(typ_file), str(pdf_file)],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                logger.info(f"PDF generated: {pdf_file}")
                return pdf_file
            else:
                logger.warning(f"Typst compilation failed: {result.stderr}")
                return None
        except Exception as e:
            logger.warning(f"PDF compilation error: {e}")
            return None
