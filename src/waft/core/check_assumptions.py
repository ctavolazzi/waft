"""
Check Assumptions - Identify and validate assumptions with evidence.

Analyzes conversation history to extract implicit assumptions, then systematically
validates each one using code analysis, file system checks, test results, Empirica
epistemic state, and other available evidence sources.
"""

import re
import subprocess
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.table import Table

from .github import GitHubManager
from .memory import MemoryManager
from .session_stats import SessionStats


class Assumption:
    """Represents a single assumption with validation results."""

    def __init__(self, statement: str, category: str, risk: str, source: str = "conversation"):
        self.statement = statement
        self.category = category
        self.risk = risk
        self.source = source
        self.status: str | None = None
        self.confidence: float = 0.0
        self.evidence: list[dict[str, Any]] = []
        self.recommendation: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "statement": self.statement,
            "category": self.category,
            "risk": self.risk,
            "source": self.source,
            "status": self.status,
            "confidence": self.confidence,
            "evidence": self.evidence,
            "recommendation": self.recommendation,
        }


class CheckAssumptionsManager:
    """Manages assumption checking and validation workflow."""

    def __init__(self, project_path: Path):
        """
        Initialize assumption checker.

        Args:
            project_path: Path to project root
        """
        self.project_path = project_path
        self.console = Console()
        self.stats_tracker = SessionStats(project_path)
        self.github = GitHubManager(project_path)
        self.memory = MemoryManager(project_path)
        self.assumptions: list[Assumption] = []

        # Initialize epistemic systems (optional, graceful degradation)
        self.oracle = None
        self.empirica = None
        try:
            from .science.oracle import TheOracle

            try:
                self.oracle = TheOracle(project_path)
            except RuntimeError:
                # Empirica not initialized - continue without Oracle
                pass
        except Exception:
            pass

        try:
            from .empirica import EmpiricaManager

            self.empirica = EmpiricaManager(project_path)
        except Exception:
            pass

    def run_check_assumptions(
        self,
        focus: str | None = None,
        critical_only: bool = False,
        test: bool = False,
        verbose: bool = False,
        conversation_context: str | None = None,
    ) -> dict[str, Any]:
        """
        Run assumption checking workflow.

        Args:
            focus: Focus area (code, dependencies, data, system, behavioral)
            critical_only: Only check critical assumptions
            test: Run experiments for assumptions needing testing
            verbose: Show detailed evidence traces
            conversation_context: Optional conversation history to analyze

        Returns:
            Dictionary with validation results
        """
        self.console.print("\n[bold cyan]🔍 Check Assumptions: Validation & Evidence[/bold cyan]\n")

        # Step 1: Extract assumptions
        assumptions = self._extract_assumptions(conversation_context)
        if focus:
            assumptions = [a for a in assumptions if a.category == focus]
        if critical_only:
            assumptions = [a for a in assumptions if a.risk == "critical"]

        self.assumptions = assumptions

        if not assumptions:
            self.console.print("[yellow]⚠️[/yellow]  No assumptions found in conversation context.")
            return {"success": True, "assumptions": [], "summary": {}}

        # Step 2: Check assumptions about assumption checking (recursive)
        self.console.print("[yellow]→[/yellow] Checking assumptions about assumption checking...")
        recursive_assumptions = self._check_recursive_assumptions()
        if recursive_assumptions:
            self.assumptions.extend(recursive_assumptions)
            assumptions.extend(recursive_assumptions)

        # Step 3: Gather validation evidence
        self.console.print(
            f"[yellow]→[/yellow] Gathering validation evidence for {len(assumptions)} assumptions..."
        )
        evidence_sources = self._gather_evidence_sources()

        # Step 4: Validate each assumption
        self.console.print("[yellow]→[/yellow] Validating assumptions...")
        for assumption in assumptions:
            self._validate_assumption(assumption, evidence_sources, test=test)

        # Step 5: Generate report
        summary = self._generate_summary()
        self._display_report(verbose=verbose)

        # Step 6: Log findings (optional)
        self._log_findings()

        return {
            "success": True,
            "assumptions": [a.to_dict() for a in assumptions],
            "summary": summary,
        }

    def _extract_assumptions(self, conversation_context: str | None = None) -> list[Assumption]:
        """
        Extract assumptions from conversation context.

        This is a placeholder - in actual use, the AI will analyze the conversation
        and extract assumptions. This method provides patterns to look for.
        """
        assumptions = []

        # If no context provided, return empty (AI will analyze conversation)
        if not conversation_context:
            return assumptions

        # Pattern matching for common assumption types
        patterns = {
            "code": [
                r"(assumes?|believes?|expects?) (that )?(the )?(function|class|method|code) (.+?) (will|does|returns?)",
                r"(function|class|method) (.+?) (will|does|returns?) (.+?)",
            ],
            "dependency": [
                r"(requires?|needs?|assumes?) (that )?(.+) (is|are) (installed|available|present)",
                r"(command|tool|dependency) (.+?) (exists|is available)",
            ],
            "data": [
                r"(assumes?|expects?) (that )?(data|file|format) (.+?) (is|has|contains)",
                r"(data|file) (.+?) (is|has|contains) (.+?)",
            ],
            "system": [
                r"(assumes?|expects?) (that )?(system|environment|filesystem) (.+?)",
                r"(system|environment) (.+?) (is|has|supports)",
            ],
            "behavioral": [
                r"(assumes?|expects?) (that )?(user|system|API) (.+?) (will|does)",
                r"(user|system|API) (.+?) (will|does) (.+?)",
            ],
        }

        # Extract assumptions using patterns
        for category, category_patterns in patterns.items():
            for pattern in category_patterns:
                matches = re.finditer(pattern, conversation_context, re.IGNORECASE)
                for match in matches:
                    statement = match.group(0)
                    # Determine risk (simple heuristic - can be improved)
                    risk = (
                        "critical"
                        if any(
                            word in statement.lower()
                            for word in ["must", "required", "critical", "essential"]
                        )
                        else "minor"
                    )
                    assumptions.append(
                        Assumption(
                            statement=statement,
                            category=category,
                            risk=risk,
                            source="pattern_match",
                        )
                    )

        return assumptions

    def _gather_evidence_sources(self) -> dict[str, Any]:
        """Gather evidence from multiple sources."""
        evidence = {
            "code_analysis": {},
            "file_system": {},
            "test_results": {},
            "git_history": {},
            "empirica": {},
            "documentation": {},
            "runtime_checks": {},
        }

        # Code analysis - check for common files
        code_files = [
            "src/waft/main.py",
            "src/waft/core",
            "tests",
        ]
        for file_path in code_files:
            full_path = self.project_path / file_path
            if full_path.exists():
                evidence["code_analysis"][file_path] = {
                    "exists": True,
                    "path": str(full_path),
                }

        # File system checks
        evidence["file_system"]["project_root"] = {
            "exists": self.project_path.exists(),
            "writable": self._check_writable(self.project_path),
        }

        # Git history
        if self.github.is_initialized():
            try:
                result = subprocess.run(
                    ["git", "log", "--oneline", "-10"],
                    cwd=self.project_path,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if result.returncode == 0:
                    evidence["git_history"]["recent_commits"] = result.stdout.strip().split("\n")[
                        :10
                    ]
            except Exception:
                pass

        # Empirica (if available)
        try:
            from .empirica import EmpiricaManager

            empirica = EmpiricaManager(self.project_path)
            if empirica.is_initialized():
                evidence["empirica"]["initialized"] = True
                # Get epistemic state
                context = empirica.project_bootstrap()
                if context:
                    evidence["empirica"]["findings"] = context.get("findings", [])
                    evidence["empirica"]["unknowns"] = context.get("unknowns", [])
        except Exception:
            evidence["empirica"]["available"] = False

        # Runtime checks - check for common commands
        commands_to_check = ["uv", "git", "python", "pytest"]
        for cmd in commands_to_check:
            result = subprocess.run(
                ["which", cmd],
                capture_output=True,
                text=True,
                check=False,
            )
            evidence["runtime_checks"][cmd] = {
                "available": result.returncode == 0,
                "path": result.stdout.strip() if result.returncode == 0 else None,
            }

        return evidence

    def _check_writable(self, path: Path) -> bool:
        """Check if path is writable."""
        try:
            test_file = path / ".waft_test_write"
            test_file.touch()
            test_file.unlink()
            return True
        except Exception:
            return False

    def _check_recursive_assumptions(self) -> list[Assumption]:
        """Check assumptions we've made about assumption checking itself."""
        recursive = []

        # Assumption: Pattern matching is sufficient for extraction
        recursive.append(
            Assumption(
                statement="Pattern matching is sufficient for extracting assumptions from conversation",
                category="behavioral",
                risk="minor",
                source="recursive_check",
            )
        )

        # Assumption: Basic evidence matching is sufficient for validation
        recursive.append(
            Assumption(
                statement="Basic evidence matching (file system, code, runtime) is sufficient for assumption validation",
                category="code",
                risk="critical",
                source="recursive_check",
            )
        )

        # Assumption: We don't need epistemic validation
        recursive.append(
            Assumption(
                statement="Epistemic state (TheOracle, Empirica) is not needed for assumption validation",
                category="system",
                risk="critical",
                source="recursive_check",
            )
        )

        # Assumption: We don't need experimental validation
        recursive.append(
            Assumption(
                statement="Scientific method tool is not needed for testable assumptions",
                category="code",
                risk="minor",
                source="recursive_check",
            )
        )

        return recursive

    def _validate_assumption(
        self,
        assumption: Assumption,
        evidence_sources: dict[str, Any],
        test: bool = False,
    ):
        """Validate a single assumption using evidence and epistemic systems."""
        evidence_points = []
        supporting = 0
        contradicting = 0

        # NEW: Epistemic validation via TheOracle
        if self.oracle:
            try:
                gate_result = self.oracle.check_gate(
                    {
                        "type": "assumption_validation",
                        "scope": "high" if assumption.risk == "critical" else "medium",
                        "description": f"Validating assumption: {assumption.statement}",
                        "assumption": assumption.statement,
                        "category": assumption.category,
                    }
                )

                if gate_result:
                    if gate_result == "PROCEED":
                        supporting += 1
                        evidence_points.append(
                            {
                                "source": "oracle_epistemic",
                                "type": "supporting",
                                "message": "Oracle CHECK gate: PROCEED - Epistemic state supports this assumption",
                            }
                        )
                    elif gate_result == "HALT":
                        contradicting += 1
                        evidence_points.append(
                            {
                                "source": "oracle_epistemic",
                                "type": "contradicting",
                                "message": "Oracle CHECK gate: HALT - High risk or insufficient knowledge",
                            }
                        )
                    elif gate_result == "BRANCH":
                        evidence_points.append(
                            {
                                "source": "oracle_epistemic",
                                "type": "info",
                                "message": "Oracle CHECK gate: BRANCH - Need investigation first",
                            }
                        )
                    elif gate_result == "REVISE":
                        contradicting += 0.5  # Partial contradiction
                        evidence_points.append(
                            {
                                "source": "oracle_epistemic",
                                "type": "contradicting",
                                "message": "Oracle CHECK gate: REVISE - Approach needs revision",
                            }
                        )
            except Exception as e:
                evidence_points.append(
                    {
                        "source": "oracle_epistemic",
                        "type": "info",
                        "message": f"Oracle check failed: {str(e)}",
                    }
                )

        # NEW: Check epistemic state alignment
        if self.empirica and self.empirica.is_initialized():
            try:
                context = self.empirica.project_bootstrap()
                if context:
                    epistemic_state = context.get("epistemic_state", {})
                    vectors = epistemic_state.get("vectors", {})
                    foundation = vectors.get("foundation", {})
                    know = foundation.get("know", 0.0) if foundation else 0.0
                    uncertainty = vectors.get("uncertainty", 1.0)

                    # Check if assumption aligns with knowledge state
                    unknowns = context.get("unknowns", [])
                    findings = context.get("findings", [])

                    # If assumption is about something we have high knowledge of
                    if know > 0.7 and uncertainty < 0.3:
                        # Check if assumption contradicts known findings
                        assumption_lower = assumption.statement.lower()
                        for finding in findings[-5:]:  # Check recent findings
                            finding_text = str(finding).lower()
                            if any(word in finding_text for word in assumption_lower.split()[:3]):
                                supporting += 1
                                evidence_points.append(
                                    {
                                        "source": "epistemic_state",
                                        "type": "supporting",
                                        "message": f"Assumption aligns with known findings (knowledge: {know:.2f}, uncertainty: {uncertainty:.2f})",
                                    }
                                )
                                break

                    # If assumption is about something we're uncertain about
                    if uncertainty > 0.5:
                        for unknown in unknowns[-5:]:  # Check recent unknowns
                            unknown_text = str(unknown).lower()
                            if any(word in unknown_text for word in assumption_lower.split()[:3]):
                                evidence_points.append(
                                    {
                                        "source": "epistemic_state",
                                        "type": "info",
                                        "message": f"Assumption relates to known uncertainty (uncertainty: {uncertainty:.2f})",
                                    }
                                )
                                break
            except Exception as e:
                evidence_points.append(
                    {
                        "source": "epistemic_state",
                        "type": "info",
                        "message": f"Epistemic state check failed: {str(e)}",
                    }
                )

        # NEW: Scientific method tool integration for testable assumptions
        if test and assumption.status != "PROVEN" and assumption.status != "DISPROVEN":
            try:
                # Check if assumption is testable
                if self._is_testable(assumption):
                    evidence_points.append(
                        {
                            "source": "scientific_method",
                            "type": "info",
                            "message": "Assumption is testable - consider converting to hypothesis and running experiment",
                        }
                    )
                    assumption.status = "NEEDS_TESTING"
            except Exception:
                pass

        # Code assumptions
        if assumption.category == "code":
            # Check if code exists, matches pattern, etc.
            code_evidence = evidence_sources.get("code_analysis", {})
            if code_evidence:
                evidence_points.append(
                    {
                        "source": "code_analysis",
                        "type": "info",
                        "message": f"Found {len(code_evidence)} code files to analyze",
                    }
                )

        # NEW: Convert testable assumptions to scientific hypotheses
        if test and assumption.status == "NEEDS_TESTING":
            try:
                hypothesis = self._convert_to_hypothesis(assumption)
                if hypothesis:
                    evidence_points.append(
                        {
                            "source": "scientific_method",
                            "type": "info",
                            "message": f"Converted to testable hypothesis: {hypothesis.statement}",
                        }
                    )
            except Exception:
                pass

        # Dependency assumptions
        if assumption.category == "dependency":
            runtime_checks = evidence_sources.get("runtime_checks", {})
            # Check if mentioned dependency is available
            for cmd, info in runtime_checks.items():
                if cmd.lower() in assumption.statement.lower():
                    if info.get("available"):
                        supporting += 1
                        evidence_points.append(
                            {
                                "source": "runtime_check",
                                "type": "supporting",
                                "message": f"Command '{cmd}' is available at {info.get('path')}",
                            }
                        )
                    else:
                        contradicting += 1
                        evidence_points.append(
                            {
                                "source": "runtime_check",
                                "type": "contradicting",
                                "message": f"Command '{cmd}' is NOT available",
                            }
                        )

        # System assumptions
        if assumption.category == "system":
            file_system = evidence_sources.get("file_system", {})
            project_info = file_system.get("project_root", {})
            if project_info.get("writable"):
                supporting += 1
                evidence_points.append(
                    {
                        "source": "file_system",
                        "type": "supporting",
                        "message": "Project directory is writable",
                    }
                )
            else:
                contradicting += 1
                evidence_points.append(
                    {
                        "source": "file_system",
                        "type": "contradicting",
                        "message": "Project directory is NOT writable",
                    }
                )

        # Determine status
        total_evidence = supporting + contradicting
        if total_evidence == 0:
            assumption.status = "INSUFFICIENT_EVIDENCE"
            assumption.confidence = 0.0
        elif contradicting == 0 and supporting > 0:
            assumption.status = "PROVEN"
            assumption.confidence = min(1.0, supporting / max(1, total_evidence))
        elif supporting == 0 and contradicting > 0:
            assumption.status = "DISPROVEN"
            assumption.confidence = min(1.0, contradicting / max(1, total_evidence))
        else:
            assumption.status = "PARTIALLY_PROVEN"
            assumption.confidence = supporting / max(1, total_evidence)

        assumption.evidence = evidence_points

        # Generate recommendation
        if assumption.status == "DISPROVEN":
            assumption.recommendation = (
                "This assumption is incorrect. Review and correct the underlying belief."
            )
        elif assumption.status == "INSUFFICIENT_EVIDENCE":
            assumption.recommendation = "Need more evidence to validate. Consider running tests or gathering more information."
        elif assumption.status == "PARTIALLY_PROVEN":
            assumption.recommendation = (
                "Mixed evidence. Verify with additional testing or investigation."
            )
        else:
            assumption.recommendation = "Assumption is valid. Proceed with confidence."

    def _generate_summary(self) -> dict[str, Any]:
        """Generate summary statistics."""
        total = len(self.assumptions)
        proven = sum(1 for a in self.assumptions if a.status == "PROVEN")
        disproven = sum(1 for a in self.assumptions if a.status == "DISPROVEN")
        partially = sum(1 for a in self.assumptions if a.status == "PARTIALLY_PROVEN")
        insufficient = sum(1 for a in self.assumptions if a.status == "INSUFFICIENT_EVIDENCE")
        needs_testing = sum(1 for a in self.assumptions if a.status == "NEEDS_TESTING")
        critical = sum(1 for a in self.assumptions if a.risk == "critical")

        return {
            "total": total,
            "proven": proven,
            "disproven": disproven,
            "partially_proven": partially,
            "insufficient_evidence": insufficient,
            "needs_testing": needs_testing,
            "critical": critical,
        }

    def _display_report(self, verbose: bool = False):
        """Display validation report."""
        summary = self._generate_summary()

        # Summary table
        summary_table = Table(title="Assumption Validation Summary", show_header=True)
        summary_table.add_column("Metric", style="cyan")
        summary_table.add_column("Count", style="magenta")

        summary_table.add_row("Total Assumptions", str(summary["total"]))
        summary_table.add_row("✅ Proven", str(summary["proven"]))
        summary_table.add_row("❌ Disproven", str(summary["disproven"]))
        summary_table.add_row("⚠️ Partially Proven", str(summary["partially_proven"]))
        summary_table.add_row("❓ Insufficient Evidence", str(summary["insufficient_evidence"]))
        summary_table.add_row("🧪 Needs Testing", str(summary["needs_testing"]))
        summary_table.add_row("🔴 Critical", str(summary["critical"]))

        self.console.print(summary_table)
        self.console.print()

        # Detailed results
        for i, assumption in enumerate(self.assumptions, 1):
            status_icon = {
                "PROVEN": "✅",
                "DISPROVEN": "❌",
                "PARTIALLY_PROVEN": "⚠️",
                "INSUFFICIENT_EVIDENCE": "❓",
                "NEEDS_TESTING": "🧪",
            }.get(assumption.status, "❓")

            risk_color = "red" if assumption.risk == "critical" else "yellow"

            self.console.print(
                f"\n[bold]{status_icon} Assumption {i}:[/bold] {assumption.statement}"
            )
            self.console.print(
                f"  [dim]Category:[/dim] {assumption.category} | [dim]Risk:[/dim] [{risk_color}]{assumption.risk}[/{risk_color}]"
            )
            self.console.print(
                f"  [dim]Status:[/dim] {assumption.status} | [dim]Confidence:[/dim] {assumption.confidence:.2f}"
            )

            if verbose and assumption.evidence:
                self.console.print("  [dim]Evidence:[/dim]")
                for evidence in assumption.evidence:
                    icon = (
                        "✅"
                        if evidence["type"] == "supporting"
                        else "❌"
                        if evidence["type"] == "contradicting"
                        else "ℹ️"
                    )
                    self.console.print(f"    {icon} [{evidence['source']}] {evidence['message']}")

            if assumption.recommendation:
                self.console.print(f"  [dim]Recommendation:[/dim] {assumption.recommendation}")

        # Critical findings
        critical_findings = [
            a
            for a in self.assumptions
            if a.risk == "critical" and a.status in ["DISPROVEN", "PARTIALLY_PROVEN"]
        ]
        if critical_findings:
            self.console.print("\n[bold red]⚠️ CRITICAL FINDINGS[/bold red]\n")
            for finding in critical_findings:
                self.console.print(f"[red]❌[/red] {finding.statement}")
                self.console.print(
                    f"  Status: {finding.status} | Confidence: {finding.confidence:.2f}"
                )
                if finding.recommendation:
                    self.console.print(f"  Recommendation: {finding.recommendation}")

    def _log_findings(self):
        """Log findings to Empirica if available."""
        try:
            from .empirica import EmpiricaManager

            empirica = EmpiricaManager(self.project_path)
            if not empirica.is_initialized():
                return

            # Log proven assumptions as findings
            for assumption in self.assumptions:
                if assumption.status == "PROVEN":
                    empirica.log_finding(
                        f"Assumption validated: {assumption.statement}",
                        impact=0.5 if assumption.risk == "minor" else 0.8,
                    )
                elif assumption.status == "DISPROVEN":
                    empirica.log_finding(
                        f"Assumption disproven: {assumption.statement}",
                        impact=0.7 if assumption.risk == "minor" else 0.9,
                    )
                elif assumption.status == "INSUFFICIENT_EVIDENCE":
                    empirica.log_unknown(f"Assumption needs validation: {assumption.statement}")
        except Exception:
            # Empirica not available or failed - continue without logging
            pass

    def _is_testable(self, assumption: Assumption) -> bool:
        """Check if assumption can be converted to testable hypothesis."""
        # Assumptions about measurable things are testable
        testable_keywords = [
            "returns",
            "produces",
            "creates",
            "generates",
            "affects",
            "changes",
            "improves",
            "decreases",
            "increases",
            "causes",
            "results in",
        ]
        return any(keyword in assumption.statement.lower() for keyword in testable_keywords)

    def _convert_to_hypothesis(self, assumption: Assumption):
        """Convert assumption to scientific method hypothesis."""
        try:
            import sys

            project_root = (
                self.project_path.parent if self.project_path.name != "waft" else self.project_path
            )
            sys.path.insert(0, str(project_root))

            from scientific_method_tool import Hypothesis

            # Create hypothesis from assumption
            hypothesis = Hypothesis(
                statement=assumption.statement,
                prediction=f"If {assumption.statement}, then we expect to observe measurable evidence",
            )

            return hypothesis
        except Exception:
            return None
