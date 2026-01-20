"""
Pantheon Command: Summon all Pantheon entities to weigh in and pass judgment.

The Pantheon gathers to review evidence, discuss, and collectively determine
what should be done next based on current state and context.
"""

from datetime import datetime
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ..core.empirica import EmpiricaManager
from ..core.science import TheOracle
from ..pantheon import (
    Fae,
    Judge,
    Librarian,
    Magistrate,
    MilitaryBrass,
    MissionControl,
    Storyteller,
    TestRunner,
    TheVillage,
)


class PantheonCouncil:
    """Manages the Pantheon gathering and collective judgment."""

    def __init__(self, project_path: Path):
        """Initialize the Pantheon Council."""
        self.project_path = project_path
        self.console = Console()

        # Initialize all Pantheon entities
        self.magistrate = Magistrate(project_path=project_path)
        self.judge = Judge(project_path=project_path, magistrate=self.magistrate)
        self.storyteller = Storyteller(project_path=project_path)
        self.librarian = Librarian(project_path=project_path)
        self.test_runner = TestRunner(project_path=project_path)
        self.military_brass = MilitaryBrass(project_path=project_path)
        self.fae = Fae(project_path=project_path)
        self.mission_control = MissionControl(project_path=project_path)
        self.village = TheVillage(project_path=project_path)

        # Initialize Oracle (epistemic intelligence)
        try:
            self.oracle = TheOracle(project_path=project_path)
            self.oracle_available = True
        except Exception:
            self.oracle = None
            self.oracle_available = False

        # Initialize Empirica (epistemic tracking)
        try:
            self.empirica = EmpiricaManager(project_path=project_path)
            self.empirica_available = self.empirica.is_initialized()
        except Exception:
            self.empirica = None
            self.empirica_available = False

    def gather_evidence(self) -> dict[str, Any]:
        """Gather evidence from all sources for the Pantheon to review."""
        evidence = {
            "timestamp": datetime.now().isoformat(),
            "work_efforts": self._get_active_work_efforts(),
            "recent_changes": self._get_recent_changes(),
            "epistemic_state": self._get_epistemic_state(),
            "body_of_proof": self._get_body_of_proof_summary(),
            "judgment_history": self._get_recent_judgments(),
            "active_missions": self._get_active_missions(),
            "open_quests": self._get_open_quests(),
        }
        return evidence

    def _get_active_work_efforts(self) -> list[dict[str, Any]]:
        """Get active work efforts."""
        work_efforts_path = self.project_path / "_work_efforts"
        if not work_efforts_path.exists():
            return []

        active = []
        for we_dir in work_efforts_path.iterdir():
            if we_dir.is_dir() and we_dir.name.startswith("WE-"):
                index_file = we_dir / f"{we_dir.name}_index.md"
                if index_file.exists():
                    try:
                        # Read status from frontmatter
                        content = index_file.read_text()
                        if "status: active" in content or "status: in_progress" in content:
                            active.append(
                                {
                                    "id": we_dir.name,
                                    "path": str(we_dir),
                                    "title": we_dir.name.replace("_", " ").replace("WE-", ""),
                                }
                            )
                    except Exception:
                        pass

        return active[:5]  # Limit to 5 most recent

    def _get_recent_changes(self) -> dict[str, Any]:
        """Get recent changes from devlog."""
        devlog_path = self.project_path / "_work_efforts" / "devlog.md"
        if not devlog_path.exists():
            return {"entries": []}

        try:
            content = devlog_path.read_text()
            # Get last 3 entries (rough parsing)
            lines = content.split("\n")
            entries = []
            current_entry = []

            for line in lines[:200]:  # Check first 200 lines
                if line.startswith("## ") and " - " in line:
                    if current_entry:
                        entries.append("\n".join(current_entry))
                    current_entry = [line]
                elif current_entry:
                    current_entry.append(line)

            if current_entry:
                entries.append("\n".join(current_entry))

            return {"entries": entries[-3:] if entries else []}
        except Exception:
            return {"entries": []}

    def _get_epistemic_state(self) -> dict[str, Any]:
        """Get epistemic state from Oracle/Empirica."""
        if not self.oracle_available:
            return {"available": False}

        try:
            self.oracle.get_epistemic_state()
            phase = self.oracle.get_epistemic_phase()
            findings = self.oracle.get_insights(limit=5)
            unknowns = self.oracle.get_unknowns(limit=5)

            return {
                "available": True,
                "phase": phase,
                "findings_count": len(findings),
                "unknowns_count": len(unknowns),
                "findings": findings,
                "unknowns": unknowns,
            }
        except Exception:
            return {"available": False}

    def _get_body_of_proof_summary(self) -> dict[str, Any]:
        """Get summary of Body of Proof from Magistrate."""
        try:
            summary = self.magistrate.get_body_of_proof_summary()
            return {
                "total_precedents": summary.get("total_precedents", 0),
                "categories": summary.get("categories", []),
            }
        except Exception:
            return {"total_precedents": 0, "categories": []}

    def _get_recent_judgments(self) -> list[dict[str, Any]]:
        """Get recent judgments from Judge."""
        try:
            judgments = self.judge.get_judgment_history(limit=5)
            return [
                {
                    "claim": j.claim[:100] if len(j.claim) > 100 else j.claim,
                    "verdict": j.verdict.value,
                    "confidence": j.confidence,
                }
                for j in judgments
            ]
        except Exception:
            return []

    def _get_active_missions(self) -> list[dict[str, Any]]:
        """Get active missions from MilitaryBrass."""
        try:
            missions = self.military_brass.list_missions(status="active")
            return [
                {
                    "id": m.mission_id,
                    "title": m.title,
                    "priority": m.priority.value
                    if hasattr(m.priority, "value")
                    else str(m.priority),
                }
                for m in missions[:5]
            ]
        except Exception:
            return []

    def _get_open_quests(self) -> list[dict[str, Any]]:
        """Get open quests from Fae."""
        try:
            quests = self.fae.list_quests(status="active")
            return [
                {
                    "id": q.quest_id,
                    "title": q.title,
                    "difficulty": q.difficulty.value
                    if hasattr(q.difficulty, "value")
                    else str(q.difficulty),
                }
                for q in quests[:5]
            ]
        except Exception:
            return []

    def summon_pantheon(self, evidence: dict[str, Any]) -> dict[str, Any]:
        """Summon all Pantheon entities to weigh in."""
        self.console.print("\n[bold gold1]⚡ SUMMONING THE PANTHEON ⚡[/bold gold1]\n")
        self.console.print("[dim]The timeless forces that bind reality together gather...[/dim]\n")

        weigh_ins = {}

        # Magistrate weighs in (Precedent and Body of Proof)
        self.console.print(
            "[yellow]→[/yellow] [bold]Magistrate[/bold] (God of Precedent) considers the evidence..."
        )
        weigh_ins["magistrate"] = self._magistrate_weighs_in(evidence)

        # Judge weighs in (Judgment and Evaluation)
        self.console.print(
            "[yellow]→[/yellow] [bold]Judge[/bold] (God of Judgment) reviews the case..."
        )
        weigh_ins["judge"] = self._judge_weighs_in(evidence)

        # Storyteller weighs in (Narrative and Story)
        self.console.print(
            "[yellow]→[/yellow] [bold]Storyteller[/bold] (God of Narrative) sees the story..."
        )
        weigh_ins["storyteller"] = self._storyteller_weighs_in(evidence)

        # Librarian weighs in (Knowledge and Records)
        self.console.print(
            "[yellow]→[/yellow] [bold]Librarian[/bold] (Keeper of Records) examines the archives..."
        )
        weigh_ins["librarian"] = self._librarian_weighs_in(evidence)

        # TestRunner weighs in (Testing and Verification)
        self.console.print(
            "[yellow]→[/yellow] [bold]TestRunner[/bold] (God of Verification) checks the tests..."
        )
        weigh_ins["test_runner"] = self._test_runner_weighs_in(evidence)

        # MilitaryBrass weighs in (Missions and Strategy)
        self.console.print(
            "[yellow]→[/yellow] [bold]MilitaryBrass[/bold] (God of Missions) reviews operations..."
        )
        weigh_ins["military_brass"] = self._military_brass_weighs_in(evidence)

        # Fae weighs in (Quests and Adventure)
        self.console.print(
            "[yellow]→[/yellow] [bold]Fae[/bold] (God of Quests) considers the journey..."
        )
        weigh_ins["fae"] = self._fae_weighs_in(evidence)

        # MissionControl weighs in (Coordination and Status)
        self.console.print(
            "[yellow]→[/yellow] [bold]MissionControl[/bold] (God of Coordination) assesses status..."
        )
        weigh_ins["mission_control"] = self._mission_control_weighs_in(evidence)

        # TheVillage weighs in (Community and Connection)
        self.console.print(
            "[yellow]→[/yellow] [bold]TheVillage[/bold] (God of Community) listens to the gathering..."
        )
        weigh_ins["village"] = self._village_weighs_in(evidence)

        # Oracle weighs in (Epistemic Intelligence)
        if self.oracle_available:
            self.console.print(
                "[yellow]→[/yellow] [bold]TheOracle[/bold] (Epistemic Intelligence) provides insight..."
            )
            weigh_ins["oracle"] = self._oracle_weighs_in(evidence)

        return weigh_ins

    def _magistrate_weighs_in(self, evidence: dict[str, Any]) -> dict[str, Any]:
        """Magistrate weighs in based on precedent and Body of Proof."""
        body_of_proof = evidence.get("body_of_proof", {})
        total_precedents = body_of_proof.get("total_precedents", 0)
        work_efforts = evidence.get("work_efforts", [])

        perspective = f"With {total_precedents} precedents in the Body of Proof, "
        if total_precedents > 50:
            perspective += "we have substantial precedent to guide us. "
        elif total_precedents > 10:
            perspective += "we have moderate precedent. "
        else:
            perspective += "we are building precedent. "

        if work_efforts:
            perspective += f"Currently {len(work_efforts)} active work efforts demand attention. "

        recommendation = "Continue building the Body of Proof while maintaining consistency with established precedents."

        return {
            "entity": "Magistrate",
            "domain": "Precedent and Body of Proof",
            "perspective": perspective,
            "recommendation": recommendation,
            "priority": "medium",
        }

    def _judge_weighs_in(self, evidence: dict[str, Any]) -> dict[str, Any]:
        """Judge weighs in based on evaluation and judgment."""
        judgments = evidence.get("judgment_history", [])
        recent_judgments = [j for j in judgments if j.get("confidence", 0) > 0.7]

        perspective = f"Recent judgments show {len(recent_judgments)} high-confidence decisions. "
        if recent_judgments:
            proven = sum(1 for j in recent_judgments if j.get("verdict") == "PROVEN")
            perspective += f"{proven} proven, {len(recent_judgments) - proven} requiring review. "

        work_efforts = evidence.get("work_efforts", [])
        if work_efforts:
            perspective += "Active work efforts need evaluation against the Body of Proof. "

        recommendation = "Evaluate current work against established precedents. Render judgment on what should proceed."

        return {
            "entity": "Judge",
            "domain": "Judgment and Evaluation",
            "perspective": perspective,
            "recommendation": recommendation,
            "priority": "high",
        }

    def _storyteller_weighs_in(self, evidence: dict[str, Any]) -> dict[str, Any]:
        """Storyteller weighs in based on narrative and story."""
        recent_changes = evidence.get("recent_changes", {}).get("entries", [])
        work_efforts = evidence.get("work_efforts", [])

        perspective = "The story continues to unfold. "
        if recent_changes:
            perspective += f"{len(recent_changes)} recent chapters in the devlog. "
        if work_efforts:
            perspective += f"{len(work_efforts)} active narratives in progress. "

        recommendation = (
            "Document the current chapter. Ensure the narrative is clear and compelling."
        )

        return {
            "entity": "Storyteller",
            "domain": "Narrative and Story",
            "perspective": perspective,
            "recommendation": recommendation,
            "priority": "low",
        }

    def _librarian_weighs_in(self, evidence: dict[str, Any]) -> dict[str, Any]:
        """Librarian weighs in based on knowledge and records."""
        epistemic_state = evidence.get("epistemic_state", {})
        findings_count = epistemic_state.get("findings_count", 0)
        unknowns_count = epistemic_state.get("unknowns_count", 0)

        perspective = "The archives grow. "
        if findings_count > 0:
            perspective += f"{findings_count} findings cataloged. "
        if unknowns_count > 0:
            perspective += f"{unknowns_count} unknowns requiring investigation. "

        recommendation = (
            "Maintain the archives. Ensure knowledge is properly cataloged and accessible."
        )

        return {
            "entity": "Librarian",
            "domain": "Knowledge and Records",
            "perspective": perspective,
            "recommendation": recommendation,
            "priority": "medium",
        }

    def _test_runner_weighs_in(self, evidence: dict[str, Any]) -> dict[str, Any]:
        """TestRunner weighs in based on testing and verification."""
        work_efforts = evidence.get("work_efforts", [])

        perspective = "Verification is essential. "
        if work_efforts:
            perspective += f"{len(work_efforts)} active work efforts should have tests. "

        recommendation = "Ensure all new work includes tests. Verify that changes don't break existing functionality."

        return {
            "entity": "TestRunner",
            "domain": "Testing and Verification",
            "perspective": perspective,
            "recommendation": recommendation,
            "priority": "high",
        }

    def _military_brass_weighs_in(self, evidence: dict[str, Any]) -> dict[str, Any]:
        """MilitaryBrass weighs in based on missions and strategy."""
        missions = evidence.get("active_missions", [])

        perspective = "Mission status: "
        if missions:
            perspective += f"{len(missions)} active missions in progress. "
            high_priority = sum(1 for m in missions if m.get("priority", "").lower() == "high")
            if high_priority > 0:
                perspective += (
                    f"{high_priority} high-priority missions require immediate attention. "
                )
        else:
            perspective += "No active missions. "

        recommendation = "Focus on high-priority missions. Complete or pause low-priority missions."

        return {
            "entity": "MilitaryBrass",
            "domain": "Missions and Strategy",
            "perspective": perspective,
            "recommendation": recommendation,
            "priority": "high" if missions else "medium",
        }

    def _fae_weighs_in(self, evidence: dict[str, Any]) -> dict[str, Any]:
        """Fae weighs in based on quests and adventure."""
        quests = evidence.get("open_quests", [])

        perspective = "The quest continues. "
        if quests:
            perspective += f"{len(quests)} open quests await. "
        else:
            perspective += "No active quests. "

        recommendation = "Pursue open quests. Adventure awaits those who seek it."

        return {
            "entity": "Fae",
            "domain": "Quests and Adventure",
            "perspective": perspective,
            "recommendation": recommendation,
            "priority": "medium",
        }

    def _mission_control_weighs_in(self, evidence: dict[str, Any]) -> dict[str, Any]:
        """MissionControl weighs in based on coordination and status."""
        work_efforts = evidence.get("work_efforts", [])
        missions = evidence.get("active_missions", [])

        perspective = "Coordination status: "
        if work_efforts or missions:
            total_active = len(work_efforts) + len(missions)
            perspective += f"{total_active} active items require coordination. "
        else:
            perspective += "All systems nominal. "

        recommendation = "Coordinate active work. Ensure resources are allocated efficiently."

        return {
            "entity": "MissionControl",
            "domain": "Coordination and Status",
            "perspective": perspective,
            "recommendation": recommendation,
            "priority": "medium",
        }

    def _village_weighs_in(self, evidence: dict[str, Any]) -> dict[str, Any]:
        """TheVillage weighs in based on community and connection."""
        work_efforts = evidence.get("work_efforts", [])

        perspective = "The village gathers. "
        if work_efforts:
            perspective += f"{len(work_efforts)} efforts connect the community. "

        recommendation = "Foster connections. Share knowledge and support collaborative efforts."

        return {
            "entity": "TheVillage",
            "domain": "Community and Connection",
            "perspective": perspective,
            "recommendation": recommendation,
            "priority": "low",
        }

    def _oracle_weighs_in(self, evidence: dict[str, Any]) -> dict[str, Any]:
        """Oracle weighs in based on epistemic intelligence."""
        epistemic_state = evidence.get("epistemic_state", {})
        phase = epistemic_state.get("phase", "UNKNOWN")
        findings = epistemic_state.get("findings", [])
        unknowns = epistemic_state.get("unknowns", [])

        perspective = f"Epistemic phase: {phase}. "
        if findings:
            perspective += f"{len(findings)} recent findings. "
        if unknowns:
            perspective += f"{len(unknowns)} unknowns need investigation. "

        # Get Oracle guidance
        try:
            guidance = self.oracle.provide_guidance("What should we focus on next?")
            recommendation = guidance.get("recommendation", "Continue building knowledge.")
        except Exception:
            recommendation = "Focus on addressing unknowns and building knowledge."

        return {
            "entity": "TheOracle",
            "domain": "Epistemic Intelligence",
            "perspective": perspective,
            "recommendation": recommendation,
            "priority": "high",
        }

    def pass_judgment(self, weigh_ins: dict[str, Any], evidence: dict[str, Any]) -> dict[str, Any]:
        """The Pantheon collectively passes judgment on what to do next."""
        self.console.print("\n[bold gold1]⚖️ THE PANTHEON PASSES JUDGMENT ⚖️[/bold gold1]\n")

        # Collect all recommendations
        recommendations = []
        high_priority = []
        medium_priority = []
        low_priority = []

        for entity_name, weigh_in in weigh_ins.items():
            priority = weigh_in.get("priority", "medium")
            rec = {
                "entity": weigh_in.get("entity", entity_name),
                "domain": weigh_in.get("domain", ""),
                "recommendation": weigh_in.get("recommendation", ""),
                "priority": priority,
            }
            recommendations.append(rec)

            if priority == "high":
                high_priority.append(rec)
            elif priority == "medium":
                medium_priority.append(rec)
            else:
                low_priority.append(rec)

        # Determine collective judgment
        # Prioritize high-priority recommendations
        if high_priority:
            primary_focus = high_priority[0]
        elif medium_priority:
            primary_focus = medium_priority[0]
        else:
            primary_focus = low_priority[0] if low_priority else recommendations[0]

        # Build consensus
        consensus = self._build_consensus(weigh_ins, evidence)

        judgment = {
            "timestamp": datetime.now().isoformat(),
            "primary_focus": primary_focus,
            "consensus": consensus,
            "all_recommendations": recommendations,
            "high_priority": high_priority,
            "medium_priority": medium_priority,
            "low_priority": low_priority,
        }

        return judgment

    def _build_consensus(self, weigh_ins: dict[str, Any], evidence: dict[str, Any]) -> str:
        """Build consensus statement from all weigh-ins."""
        # Analyze patterns in recommendations
        themes = []

        # Check for common themes
        work_efforts = evidence.get("work_efforts", [])
        if work_efforts:
            themes.append("Continue active work efforts")

        epistemic_state = evidence.get("epistemic_state", {})
        if epistemic_state.get("unknowns_count", 0) > 0:
            themes.append("Address knowledge gaps")

        missions = evidence.get("active_missions", [])
        if missions:
            themes.append("Focus on high-priority missions")

        # Build consensus
        if themes:
            consensus = f"The Pantheon agrees: {', '.join(themes[:2])}. "
        else:
            consensus = "The Pantheon agrees: Continue building and learning. "

        # Add Oracle insight if available
        if "oracle" in weigh_ins:
            oracle_rec = weigh_ins["oracle"].get("recommendation", "")
            if oracle_rec:
                consensus += f"TheOracle advises: {oracle_rec[:100]}"

        return consensus

    def display_judgment(self, judgment: dict[str, Any], weigh_ins: dict[str, Any]):
        """Display the Pantheon's judgment in a beautiful format."""
        # Display consensus
        consensus = judgment.get("consensus", "")
        self.console.print(
            Panel(
                consensus,
                title="[bold gold1]⚖️ Collective Judgment[/bold gold1]",
                border_style="gold1",
                padding=(1, 2),
            )
        )

        # Display primary focus
        primary = judgment.get("primary_focus", {})
        self.console.print("\n[bold cyan]🎯 Primary Focus:[/bold cyan]")
        self.console.print(
            Panel(
                f"[bold]{primary.get('entity', 'Unknown')}[/bold] ({primary.get('domain', '')})\n\n"
                f"{primary.get('recommendation', 'No recommendation')}",
                border_style="cyan",
                padding=(1, 2),
            )
        )

        # Display all weigh-ins
        self.console.print("\n[bold yellow]📜 All Pantheon Weigh-Ins:[/bold yellow]\n")

        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("Entity", style="cyan", width=20)
        table.add_column("Domain", style="dim", width=25)
        table.add_column("Recommendation", width=50)
        table.add_column("Priority", justify="center", width=10)

        for entity_name, weigh_in in weigh_ins.items():
            entity = weigh_in.get("entity", entity_name)
            domain = weigh_in.get("domain", "")
            rec = weigh_in.get("recommendation", "")
            priority = weigh_in.get("priority", "medium")

            priority_style = {"high": "bold red", "medium": "yellow", "low": "dim"}.get(
                priority, "dim"
            )

            table.add_row(
                entity,
                domain,
                rec[:80] + "..." if len(rec) > 80 else rec,
                f"[{priority_style}]{priority.upper()}[/{priority_style}]",
            )

        self.console.print(table)

        # Display evidence summary
        self.console.print("\n[bold dim]📊 Evidence Reviewed:[/bold dim]")
        self.console.print(
            f"  • Work Efforts: {len(judgment.get('all_recommendations', []))} entities consulted"
        )
        self.console.print(f"  • High Priority Items: {len(judgment.get('high_priority', []))}")
        self.console.print(f"  • Medium Priority Items: {len(judgment.get('medium_priority', []))}")
        self.console.print(f"  • Low Priority Items: {len(judgment.get('low_priority', []))}")

        self.console.print(
            f"\n[dim]Judgment rendered at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/dim]\n"
        )


def pantheon_command(project_path: Path):
    """Execute the Pantheon command."""
    council = PantheonCouncil(project_path)

    # Gather evidence
    console = Console()
    console.print("[yellow]→[/yellow] Gathering evidence for the Pantheon to review...")
    evidence = council.gather_evidence()

    # Summon Pantheon
    weigh_ins = council.summon_pantheon(evidence)

    # Pass judgment
    judgment = council.pass_judgment(weigh_ins, evidence)

    # Display judgment
    council.display_judgment(judgment, weigh_ins)

    return judgment
