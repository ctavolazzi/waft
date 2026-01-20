"""
Critique and Revise - Main orchestrator for critiquing and revising plans.

Combines critique generation with automatic plan revision based on
valid, evidence-backed criticisms.
"""

import json
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .plan_loader import PlanLoader, PlanData
from .plan_reviser import PlanReviser, RevisionResult
from .critique_parser import CritiqueParser, CritiqueData
from .criticism_validator import ValidationStatus


class CritiqueAndReviseManager:
    """Manages critique and revise workflow for plans."""
    
    def __init__(self, project_path: Path):
        """
        Initialize critique and revise manager.
        
        Args:
            project_path: Path to project root
        """
        self.project_path = project_path
        self.console = Console()
        self.plan_loader = PlanLoader(project_path)
        self.plan_reviser = PlanReviser(project_path)
        self.critique_parser = CritiqueParser(project_path)
        self.work_efforts_dir = project_path / "_work_efforts"
        self.hidden_dir = project_path / "_hidden" / ".plan_revisions"
        self.backups_dir = self.hidden_dir / "backups"
        self.history_file = self.hidden_dir / "history.jsonl"
        
        # Ensure directories exist
        self.backups_dir.mkdir(parents=True, exist_ok=True)
    
    def run_critique_and_revise(
        self,
        plan_path: Optional[Path] = None,
        plan_name: Optional[str] = None,
        dry_run: bool = False,
        severity_filter: Optional[str] = None,
        critique_path: Optional[Path] = None
    ) -> Dict[str, Any]:
        """
        Run critique and revise workflow.
        
        Args:
            plan_path: Path to plan file (if None, finds most recent)
            plan_name: Name of plan to find (if plan_path not provided)
            dry_run: If True, show revisions without applying
            severity_filter: Only revise this severity (CRITICAL, HIGH, etc.)
            critique_path: Path to existing critique (if None, generates new)
            
        Returns:
            Dictionary with results
        """
        self.console.print("\n[bold cyan]🔍 Critique and Revise Plan[/bold cyan]\n")
        
        # Step 1: Load plan
        try:
            if plan_path:
                plan_data = self.plan_loader.load_plan(plan_path)
            elif plan_name:
                plan_path = self.plan_loader.find_plan_by_name(plan_name)
                if not plan_path:
                    self.console.print(f"[red]❌ Plan not found: {plan_name}[/red]")
                    return {"success": False, "error": f"Plan not found: {plan_name}"}
                plan_data = self.plan_loader.load_plan(plan_path)
            else:
                plan_data = self.plan_loader.load_plan()
                plan_path = plan_data.path
            
            self.console.print(f"[dim]Plan: {plan_path.name}[/dim]\n")
        except FileNotFoundError as e:
            self.console.print(f"[red]❌ {e}[/red]")
            return {"success": False, "error": str(e)}
        except Exception as e:
            self.console.print(f"[red]❌ Error loading plan: {e}[/red]")
            return {"success": False, "error": str(e)}
        
        # Step 2: Generate or load critique
        if critique_path and critique_path.exists():
            self.console.print(f"[dim]Loading critique: {critique_path.name}[/dim]\n")
            try:
                critique_data = self.critique_parser.parse_critique(critique_path)
            except Exception as e:
                self.console.print(f"[red]❌ Error parsing critique: {e}[/red]")
                return {"success": False, "error": str(e)}
        else:
            # Generate critique (this would need to call the critique generation logic)
            # For now, we'll require an existing critique
            self.console.print("[yellow]⚠️  No critique provided. Please run /critique first, or provide critique_path[/yellow]")
            return {"success": False, "error": "No critique provided. Run /critique first."}
        
        self.console.print(f"[green]✅ Found {len(critique_data.get_all_criticisms())} criticisms[/green]\n")
        
        # Step 3: Revise plan
        self.console.print("[bold]Revising plan...[/bold]\n")
        
        try:
            revision_result = self.plan_reviser.revise_plan(
                plan_data=plan_data,
                critique_data=critique_data,
                severity_filter=severity_filter,
                dry_run=dry_run
            )
        except Exception as e:
            self.console.print(f"[red]❌ Error revising plan: {e}[/red]")
            return {"success": False, "error": str(e)}
        
        # Step 4: Create backup (if not dry-run)
        backup_path = None
        if not dry_run:
            backup_path = self._create_backup(plan_path, plan_data)
            self.console.print(f"[dim]💾 Backup created: {backup_path}[/dim]\n")
        
        # Step 5: Save revised plan (if not dry-run)
        if not dry_run:
            try:
                plan_path.write_text(revision_result.revised_content, encoding="utf-8")
                self.console.print(f"[green]💾 Revised plan saved: {plan_path}[/green]\n")
            except Exception as e:
                self.console.print(f"[red]❌ Error saving plan: {e}[/red]")
                return {"success": False, "error": str(e)}
        
        # Step 6: Generate revision report
        report_path = self._generate_revision_report(
            plan_data=plan_data,
            revision_result=revision_result,
            backup_path=backup_path,
            dry_run=dry_run
        )
        
        # Display summary
        self._display_summary(revision_result, report_path, dry_run)
        
        # Record in history
        if not dry_run:
            self._record_revision(plan_path, backup_path, report_path, revision_result)
        
        return {
            "success": True,
            "plan_path": str(plan_path),
            "backup_path": str(backup_path) if backup_path else None,
            "report_path": str(report_path),
            "revisions": len(revision_result.revisions),
            "sections_added": revision_result.sections_added,
            "sections_updated": revision_result.sections_updated,
            "todos_added": revision_result.todos_added,
            "dry_run": dry_run
        }
    
    def _create_backup(self, plan_path: Path, plan_data: PlanData) -> Path:
        """
        Create backup of original plan.
        
        Args:
            plan_path: Path to plan file
            plan_data: Plan data
            
        Returns:
            Path to backup file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"{plan_path.stem}_{timestamp}{plan_path.suffix}"
        backup_path = self.backups_dir / backup_filename
        
        # Copy original content
        backup_path.write_text(plan_data.content, encoding="utf-8")
        
        return backup_path
    
    def _generate_revision_report(
        self,
        plan_data: PlanData,
        revision_result: RevisionResult,
        backup_path: Optional[Path],
        dry_run: bool
    ) -> Path:
        """
        Generate revision report.
        
        Args:
            plan_data: Original plan data
            revision_result: Revision result
            backup_path: Path to backup (if not dry-run)
            dry_run: Whether this is a dry run
            
        Returns:
            Path to report file
        """
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        report_filename = f"PLAN_REVISION_{timestamp}.md"
        report_path = self.work_efforts_dir / report_filename
        
        # Group revisions by severity
        by_severity = {
            "CRITICAL": [],
            "HIGH": [],
            "MEDIUM": [],
            "LOW": []
        }
        
        for revision in revision_result.revisions:
            severity = revision.criticism.severity
            if severity in by_severity:
                by_severity[severity].append(revision)
        
        # Generate report
        report_lines = [
            "# Plan Revision Report",
            "",
            f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Original Plan**: {plan_data.path.name}",
            f"**Revised Plan**: {plan_data.path.name}",
            f"**Backup**: {backup_path.name if backup_path else 'N/A (dry-run)'}",
            f"**Dry Run**: {dry_run}",
            "",
            "## Summary",
            "",
            f"**Total Criticisms**: {len(revision_result.revisions)}",
            f"**Revisions Made**: {len(revision_result.revisions)}",
            f"**Sections Added**: {len(revision_result.sections_added)}",
            f"**Sections Updated**: {len(revision_result.sections_updated)}",
            f"**Todos Added**: {len(revision_result.todos_added)}",
            "",
            "---",
            ""
        ]
        
        # Add sections by severity
        for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
            revisions = by_severity[severity]
            if revisions:
                report_lines.extend([
                    f"## {severity} Issues (Revised)",
                    ""
                ])
                
                for revision in revisions:
                    report_lines.extend([
                        f"### {revision.criticism.number}. {revision.criticism.title}",
                        f"**Issue**: {revision.criticism.issue}",
                        f"**Section**: {revision.section_title}",
                        f"**Action**: {revision.action}",
                        "",
                        f"**Revision**:",
                        "```markdown",
                        revision.content.strip(),
                        "```",
                        "",
                        "---",
                        ""
                    ])
        
        # Add sections summary
        if revision_result.sections_added or revision_result.sections_updated:
            report_lines.extend([
                "## Sections Modified",
                ""
            ])
            
            if revision_result.sections_added:
                report_lines.append("### Added:")
                for section in revision_result.sections_added:
                    report_lines.append(f"- {section}")
                report_lines.append("")
            
            if revision_result.sections_updated:
                report_lines.append("### Updated:")
                for section in revision_result.sections_updated:
                    report_lines.append(f"- {section}")
                report_lines.append("")
        
        # Add todos
        if revision_result.todos_added:
            report_lines.extend([
                "## Todos Added",
                ""
            ])
            for todo in revision_result.todos_added:
                report_lines.append(f"- [ ] {todo}")
            report_lines.append("")
        
        # Write report
        report_path.write_text('\n'.join(report_lines), encoding="utf-8")
        
        return report_path
    
    def _display_summary(
        self,
        revision_result: RevisionResult,
        report_path: Path,
        dry_run: bool
    ) -> None:
        """Display revision summary in console."""
        mode_text = "[DRY RUN] " if dry_run else ""
        
        self.console.print(f"\n[bold green]{mode_text}✅ Revision Complete[/bold green]\n")
        
        table = Table(title="Revision Summary")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Revisions Made", str(len(revision_result.revisions)))
        table.add_row("Sections Added", str(len(revision_result.sections_added)))
        table.add_row("Sections Updated", str(len(revision_result.sections_updated)))
        table.add_row("Todos Added", str(len(revision_result.todos_added)))
        
        self.console.print(table)
        
        if revision_result.sections_added:
            self.console.print(f"\n[green]✅ Added sections: {', '.join(revision_result.sections_added)}[/green]")
        
        if revision_result.sections_updated:
            self.console.print(f"[green]✅ Updated sections: {', '.join(revision_result.sections_updated)}[/green]")
        
        self.console.print(f"\n[dim]📄 Report: {report_path}[/dim]\n")
    
    def _find_most_recent_critique(self) -> Optional[Path]:
        """
        Find the most recently modified critique file.
        
        Returns:
            Path to most recent critique, or None if no critiques found
        """
        critiques = []
        
        # Search in _work_efforts for CRITIQUE_*.md files
        if self.work_efforts_dir.exists():
            critiques.extend(self.work_efforts_dir.glob("CRITIQUE_*.md"))
        
        if not critiques:
            return None
        
        # Sort by modification time, most recent first
        critiques.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        return critiques[0]
    
    def _record_revision(
        self,
        plan_path: Path,
        backup_path: Optional[Path],
        report_path: Path,
        revision_result: RevisionResult
    ) -> None:
        """Record revision in history file."""
        record = {
            "timestamp": datetime.now().isoformat(),
            "plan_path": str(plan_path),
            "backup_path": str(backup_path) if backup_path else None,
            "report_path": str(report_path),
            "revisions_count": len(revision_result.revisions),
            "sections_added": revision_result.sections_added,
            "sections_updated": revision_result.sections_updated,
            "todos_added": revision_result.todos_added
        }
        
        with open(self.history_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
    
    def rollback_last_revision(self) -> Dict[str, Any]:
        """
        Rollback the last plan revision.
        
        Returns:
            Dictionary with rollback results
        """
        self.console.print("\n[bold yellow]↩️  Rollback Last Revision[/bold yellow]\n")
        
        # Read history to find last revision
        if not self.history_file.exists():
            self.console.print("[red]❌ No revision history found[/red]")
            return {"success": False, "error": "No revision history found"}
        
        # Read last line from history
        last_record = None
        with open(self.history_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            if lines:
                last_record = json.loads(lines[-1])
        
        if not last_record or not last_record.get("backup_path"):
            self.console.print("[red]❌ No backup found for last revision[/red]")
            return {"success": False, "error": "No backup found"}
        
        backup_path = Path(last_record["backup_path"])
        plan_path = Path(last_record["plan_path"])
        
        if not backup_path.exists():
            self.console.print(f"[red]❌ Backup file not found: {backup_path}[/red]")
            return {"success": False, "error": f"Backup file not found: {backup_path}"}
        
        # Restore from backup
        try:
            backup_content = backup_path.read_text(encoding="utf-8")
            plan_path.write_text(backup_content, encoding="utf-8")
            self.console.print(f"[green]✅ Plan restored from backup: {backup_path.name}[/green]")
            self.console.print(f"[green]✅ Plan: {plan_path.name}[/green]\n")
            return {
                "success": True,
                "plan_path": str(plan_path),
                "backup_path": str(backup_path)
            }
        except Exception as e:
            self.console.print(f"[red]❌ Error restoring plan: {e}[/red]")
            return {"success": False, "error": str(e)}
