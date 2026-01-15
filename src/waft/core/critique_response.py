"""
Critique Response - Main orchestrator for responding to critiques.

Coordinates parsing, validation, and fixing of criticisms from critique documents.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown

from .critique_parser import CritiqueParser, CritiqueData
from .criticism_validator import CriticismValidator, ValidationResult, ValidationStatus
from .auto_fixer import AutoFixer, FixResult


class CritiqueResponseManager:
    """Manages critique response workflow."""
    
    def __init__(self, project_path: Path):
        """
        Initialize critique response manager.
        
        Args:
            project_path: Path to project root
        """
        self.project_path = project_path
        self.console = Console()
        self.parser = CritiqueParser(project_path)
        self.validator = CriticismValidator(project_path)
        self.fixer = AutoFixer(project_path)
        self.work_efforts_dir = project_path / "_work_efforts"
    
    def run_respond_to_critique(
        self,
        critique_path: Optional[Path] = None,
        dry_run: bool = False,
        auto_fix: bool = False,
        severity_filter: Optional[str] = None,
        validate_only: bool = False
    ) -> Dict[str, Any]:
        """
        Run critique response workflow.
        
        Args:
            critique_path: Path to critique file (if None, finds most recent)
            dry_run: If True, don't apply fixes
            auto_fix: If True, don't ask for confirmation
            severity_filter: Only process this severity (CRITICAL, HIGH, etc.)
            validate_only: Only validate, don't apply fixes
            
        Returns:
            Dictionary with results
        """
        self.console.print("\n[bold cyan]🔧 Respond to Critique[/bold cyan]\n")
        
        # Step 1: Locate critique
        if critique_path is None:
            critique_path = self._find_most_recent_critique()
        
        if not critique_path or not critique_path.exists():
            self.console.print(f"[red]❌ Critique file not found[/red]")
            return {"success": False, "error": "Critique file not found"}
        
        self.console.print(f"[dim]Reading critique: {critique_path.name}[/dim]\n")
        
        # Step 2: Parse critique
        try:
            critique_data = self.parser.parse_critique(critique_path)
            self.console.print(f"[green]✅ Parsed {len(critique_data.get_all_criticisms())} criticisms[/green]\n")
        except Exception as e:
            self.console.print(f"[red]❌ Error parsing critique: {e}[/red]")
            return {"success": False, "error": str(e)}
        
        # Step 3: Validate criticisms
        self.console.print("[bold]Validating criticisms...[/bold]\n")
        validation_results = []
        
        all_criticisms = critique_data.get_all_criticisms()
        if severity_filter:
            all_criticisms = [c for c in all_criticisms if c.severity == severity_filter.upper()]
        
        for i, criticism in enumerate(all_criticisms, 1):
            self.console.print(f"[dim]Validating {i}/{len(all_criticisms)}: {criticism.title[:60]}...[/dim]")
            result = self.validator.validate_criticism(criticism)
            validation_results.append(result)
        
        self.console.print("\n[green]✅ Validation complete[/green]\n")
        
        # Step 4: Apply fixes (if not validate-only)
        fix_results = []
        if not validate_only:
            self.console.print("[bold]Applying fixes...[/bold]\n")
            
            valid_criticisms = [
                (cr, vr) for cr, vr in zip(all_criticisms, validation_results)
                if vr.status in [ValidationStatus.VALID, ValidationStatus.PARTIALLY_VALID]
            ]
            
            for i, (criticism, validation) in enumerate(valid_criticisms, 1):
                # Skip LOW severity unless explicitly requested
                if criticism.severity == "LOW" and not severity_filter:
                    continue
                
                self.console.print(f"[dim]Fixing {i}/{len(valid_criticisms)}: {criticism.title[:60]}...[/dim]")
                
                # Ask for confirmation on CRITICAL unless auto-fix
                if criticism.severity == "CRITICAL" and not auto_fix and not dry_run:
                    response = self.console.input(
                        f"[yellow]⚠️  Fix CRITICAL issue: {criticism.title}? (y/n): [/yellow]"
                    )
                    if response.lower() != 'y':
                        continue
                
                fix_result = self.fixer.fix_criticism(criticism, validation, dry_run=dry_run)
                fix_results.append(fix_result)
                
                if fix_result.success:
                    self.console.print(f"[green]  ✅ Fixed: {criticism.title}[/green]")
                else:
                    self.console.print(f"[red]  ❌ Failed: {fix_result.error}[/red]")
        
        # Step 5: Generate response report
        self.console.print("\n[bold]Generating response report...[/bold]\n")
        report_path = self._generate_response_report(
            critique_path,
            critique_data,
            validation_results,
            fix_results,
            dry_run
        )
        
        self.console.print(f"[green]✅ Response report saved: {report_path.relative_to(self.project_path)}[/green]\n")
        
        # Display summary
        self._display_summary(critique_data, validation_results, fix_results)
        
        return {
            "success": True,
            "critique_path": str(critique_path),
            "report_path": str(report_path),
            "total_criticisms": len(all_criticisms),
            "validation_results": validation_results,
            "fix_results": fix_results
        }
    
    def _find_most_recent_critique(self) -> Optional[Path]:
        """Find most recent critique file."""
        if not self.work_efforts_dir.exists():
            return None
        
        critique_files = list(self.work_efforts_dir.glob("CRITIQUE_*.md"))
        if not critique_files:
            return None
        
        # Sort by modification time, most recent first
        critique_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        return critique_files[0]
    
    def _generate_response_report(
        self,
        critique_path: Path,
        critique_data: CritiqueData,
        validation_results: List[ValidationResult],
        fix_results: List[FixResult],
        dry_run: bool
    ) -> Path:
        """Generate comprehensive response report."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.work_efforts_dir / f"RESPONSE_{timestamp}.md"
        
        # Count results
        valid_count = sum(1 for r in validation_results if r.status == ValidationStatus.VALID)
        invalid_count = sum(1 for r in validation_results if r.status == ValidationStatus.INVALID)
        partial_count = sum(1 for r in validation_results if r.status == ValidationStatus.PARTIALLY_VALID)
        cannot_verify_count = sum(1 for r in validation_results if r.status == ValidationStatus.CANNOT_VERIFY)
        
        fixes_applied = sum(1 for r in fix_results if r.success and not dry_run)
        fixes_suggested = sum(1 for r in fix_results if r.success and dry_run)
        
        # Generate report
        report_lines = [
            "# Critique Response Report",
            "",
            f"**Date**: {datetime.now().strftime('%Y-%m-%d')}",
            f"**Time**: {datetime.now().strftime('%H:%M:%S')}",
            f"**Critique**: {critique_path.name}",
            f"**Status**: {'Dry Run' if dry_run else 'Complete'}",
            "",
            "---",
            "",
            "## Executive Summary",
            "",
            f"**Total Criticisms**: {len(validation_results)}",
            f"**✅ Valid**: {valid_count}",
            f"**❌ Invalid**: {invalid_count}",
            f"**⚠️ Partially Valid**: {partial_count}",
            f"**❓ Cannot Verify**: {cannot_verify_count}",
            "",
            f"**Fixes Applied**: {fixes_applied}",
            f"**Fixes Suggested**: {fixes_suggested}",
            f"**Manual Review Required**: {cannot_verify_count}",
            "",
            "---",
            ""
        ]
        
        # Group by severity and status
        by_severity = {
            "CRITICAL": [],
            "HIGH": [],
            "MEDIUM": [],
            "LOW": []
        }
        
        for criticism, validation in zip(critique_data.get_all_criticisms(), validation_results):
            if criticism.severity in by_severity:
                by_severity[criticism.severity].append((criticism, validation))
        
        # CRITICAL Issues
        if by_severity["CRITICAL"]:
            report_lines.extend([
                "## 🔴 CRITICAL Issues",
                ""
            ])
            
            for criticism, validation in by_severity["CRITICAL"]:
                status_emoji = {
                    ValidationStatus.VALID: "✅ VALID",
                    ValidationStatus.INVALID: "❌ INVALID",
                    ValidationStatus.PARTIALLY_VALID: "⚠️ PARTIALLY VALID",
                    ValidationStatus.CANNOT_VERIFY: "❓ CANNOT VERIFY"
                }
                
                report_lines.extend([
                    f"### {criticism.number}. {criticism.title}",
                    f"**Status**: {status_emoji.get(validation.status, 'UNKNOWN')}",
                    f"**Confidence**: {validation.confidence:.2f}",
                    "",
                    f"**Issue**: {criticism.issue}",
                    "",
                ])
                
                if validation.evidence:
                    report_lines.append("**Evidence**:")
                    for evidence in validation.evidence:
                        symbol = "✅" if evidence.supports else "❌"
                        report_lines.append(f"- {symbol} {evidence.description} (confidence: {evidence.confidence:.2f})")
                    report_lines.append("")
                
                if validation.conclusion:
                    report_lines.append(f"**Conclusion**: {validation.conclusion}")
                    report_lines.append("")
                
                # Find fix result (match by title and severity)
                fix_result = next(
                    (fr for fr in fix_results 
                     if fr.criticism.title == criticism.title 
                     and fr.criticism.severity == criticism.severity),
                    None
                )
                if fix_result and fix_result.success:
                    report_lines.extend([
                        f"**Fix Applied**: {fix_result.fix_applied}",
                        f"**Files Modified**: {', '.join(fix_result.files_modified)}",
                        ""
                    ])
                
                report_lines.append("---")
                report_lines.append("")
        
        # HIGH Issues
        if by_severity["HIGH"]:
            report_lines.extend([
                "## 🔴 HIGH Issues",
                ""
            ])
            
            for criticism, validation in by_severity["HIGH"]:
                status_emoji = {
                    ValidationStatus.VALID: "✅ VALID",
                    ValidationStatus.INVALID: "❌ INVALID",
                    ValidationStatus.PARTIALLY_VALID: "⚠️ PARTIALLY VALID",
                    ValidationStatus.CANNOT_VERIFY: "❓ CANNOT VERIFY"
                }
                
                report_lines.extend([
                    f"### {criticism.number}. {criticism.title}",
                    f"**Status**: {status_emoji.get(validation.status, 'UNKNOWN')}",
                    f"**Confidence**: {validation.confidence:.2f}",
                    "",
                    f"**Issue**: {criticism.issue}",
                    "",
                ])
                
                if validation.evidence:
                    report_lines.append("**Evidence**:")
                    for evidence in validation.evidence:
                        symbol = "✅" if evidence.supports else "❌"
                        report_lines.append(f"- {symbol} {evidence.description} (confidence: {evidence.confidence:.2f})")
                    report_lines.append("")
                
                if validation.conclusion:
                    report_lines.append(f"**Conclusion**: {validation.conclusion}")
                    report_lines.append("")
                
                fix_result = next((fr for fr in fix_results if fr.criticism == criticism), None)
                if fix_result and fix_result.success:
                    report_lines.extend([
                        f"**Fix Applied**: {fix_result.fix_applied}",
                        f"**Files Modified**: {', '.join(fix_result.files_modified)}",
                        ""
                    ])
                
                report_lines.append("---")
                report_lines.append("")
        
        # MEDIUM Issues
        if by_severity["MEDIUM"]:
            report_lines.extend([
                "## ⚠️ MEDIUM Issues",
                ""
            ])
            
            for criticism, validation in by_severity["MEDIUM"]:
                status_emoji = {
                    ValidationStatus.VALID: "✅ VALID",
                    ValidationStatus.INVALID: "❌ INVALID",
                    ValidationStatus.PARTIALLY_VALID: "⚠️ PARTIALLY VALID",
                    ValidationStatus.CANNOT_VERIFY: "❓ CANNOT VERIFY"
                }
                
                report_lines.extend([
                    f"### {criticism.number}. {criticism.title}",
                    f"**Status**: {status_emoji.get(validation.status, 'UNKNOWN')}",
                    f"**Confidence**: {validation.confidence:.2f}",
                    "",
                    f"**Issue**: {criticism.issue}",
                    "",
                ])
                
                if validation.recommendation:
                    report_lines.append(f"**Recommendation**: {validation.recommendation}")
                    report_lines.append("")
                
                report_lines.append("---")
                report_lines.append("")
        
        # LOW Issues
        if by_severity["LOW"]:
            report_lines.extend([
                "## ⚠️ LOW Issues",
                ""
            ])
            
            for criticism, validation in by_severity["LOW"]:
                report_lines.extend([
                    f"### {criticism.number}. {criticism.title}",
                    f"**Status**: {validation.status.value.upper()}",
                    "",
                    f"**Issue**: {criticism.issue}",
                    "",
                    "**Action**: Documented for future consideration",
                    "",
                    "---",
                    ""
                ])
        
        # Invalid Criticisms
        invalid_results = [
            (cr, vr) for cr, vr in zip(critique_data.get_all_criticisms(), validation_results)
            if vr.status == ValidationStatus.INVALID
        ]
        
        if invalid_results:
            report_lines.extend([
                "## Invalid Criticisms (Disproven)",
                ""
            ])
            
            for criticism, validation in invalid_results:
                report_lines.extend([
                    f"### {criticism.number}. {criticism.title}",
                    f"**Status**: ❌ INVALID",
                    "",
                    f"**Issue**: {criticism.issue}",
                    "",
                    "**Evidence**:"
                ])
                
                for evidence in validation.evidence:
                    if not evidence.supports:
                        report_lines.append(f"- ❌ {evidence.description} (confidence: {evidence.confidence:.2f})")
                
                report_lines.append("")
                if validation.conclusion:
                    report_lines.append(f"**Conclusion**: {validation.conclusion}")
                    report_lines.append("")
                
                report_lines.append("---")
                report_lines.append("")
        
        # Cannot Verify
        cannot_verify_results = [
            (cr, vr) for cr, vr in zip(critique_data.get_all_criticisms(), validation_results)
            if vr.status == ValidationStatus.CANNOT_VERIFY
        ]
        
        if cannot_verify_results:
            report_lines.extend([
                "## Cannot Verify (Manual Review Required)",
                ""
            ])
            
            for criticism, validation in cannot_verify_results:
                report_lines.extend([
                    f"### {criticism.number}. {criticism.title}",
                    f"**Status**: ❓ CANNOT VERIFY",
                    "",
                    f"**Issue**: {criticism.issue}",
                    "",
                    "**Reason**: Insufficient evidence to determine validity",
                    "",
                    "**Action Required**: Manual review needed",
                    "",
                    "---",
                    ""
                ])
        
        # Files Modified
        all_files_modified = set()
        for fix_result in fix_results:
            all_files_modified.update(fix_result.files_modified)
        
        if all_files_modified:
            report_lines.extend([
                "## Files Modified",
                ""
            ])
            for file_path in sorted(all_files_modified):
                report_lines.append(f"- `{file_path}`")
            report_lines.append("")
        
        # Next Steps
        report_lines.extend([
            "## Next Steps",
            "",
            "1. Review manual review items",
            "2. Run full test suite",
            "3. Update plan document with fixes",
            "4. Commit changes with security fix message",
            ""
        ])
        
        report_path.write_text("\n".join(report_lines), encoding="utf-8")
        return report_path
    
    def _display_summary(
        self,
        critique_data: CritiqueData,
        validation_results: List[ValidationResult],
        fix_results: List[FixResult]
    ) -> None:
        """Display summary table."""
        table = Table(title="Critique Response Summary", show_header=True)
        table.add_column("Metric", style="dim")
        table.add_column("Count", justify="right")
        
        table.add_row("Total Criticisms", str(len(validation_results)))
        table.add_row("✅ Valid", str(sum(1 for r in validation_results if r.status == ValidationStatus.VALID)))
        table.add_row("❌ Invalid", str(sum(1 for r in validation_results if r.status == ValidationStatus.INVALID)))
        table.add_row("⚠️ Partially Valid", str(sum(1 for r in validation_results if r.status == ValidationStatus.PARTIALLY_VALID)))
        table.add_row("❓ Cannot Verify", str(sum(1 for r in validation_results if r.status == ValidationStatus.CANNOT_VERIFY)))
        table.add_row("", "")
        table.add_row("Fixes Applied", str(sum(1 for r in fix_results if r.success)))
        table.add_row("Fixes Failed", str(sum(1 for r in fix_results if not r.success)))
        
        self.console.print("\n")
        self.console.print(table)
        self.console.print("\n")
