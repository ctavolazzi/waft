"""
Reincarnation Cycle Validation - Gamified Testing for The Mutator (Claude)

This script provides a gamified command interface for validating the reincarnation
cycle functionality. Claude (The Mutator) earns Scint points by discovering and
validating core mechanics.

Core Mechanics to Validate:
1. Soul ID Continuity (5 Scint)
2. Lifetimes Increment (5 Scint)
3. Ancestral Chain Inheritance (3 Scint)
4. Memory Continuity (2 Scint)

Commands Available:
- spawn_being: Create a new Being (lifetime 1)
- run_tavern: Run Being through tavern scenario to generate memories
- save_being: Save Being state to disk
- load_being: Load Being state from disk
- archive_being: Archive (kill) the Being
- reincarnate: Reincarnate the archived Being
- verify_soul: Verify soul_id continuity
- verify_lifetimes: Verify lifetimes increment
- verify_ancestral_chain: Verify ancestral chain inheritance
- verify_memories: Verify memory inheritance
"""

from pathlib import Path
import sys
import json
from datetime import datetime
from typing import Optional, Dict, Any, List

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from waft.being import Being, BeingSystem, BeingState
from waft.karma import KarmaMerchant
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()


class ReincarnationValidator:
    """
    Gamified validation system for reincarnation cycle.

    Tracks validation progress and Scint points earned.
    """

    def __init__(self, project_path: Optional[Path] = None):
        """Initialize validator with project path."""
        if project_path is None:
            project_path = Path.cwd()

        self.project_path = project_path
        self.being_system = BeingSystem(project_path=project_path)
        self.karma_merchant = KarmaMerchant(project_path=project_path)

        # Validation state
        self.current_being: Optional[Being] = None
        self.archived_being_id: Optional[str] = None
        self.reincarnated_being: Optional[Being] = None

        # Scint tracking
        self.scint_earned = 0
        self.validations_passed = []
        self.validations_failed = []
        self.reality_fractures = []  # Unexpected discoveries

        # Test results
        self.test_results: Dict[str, Any] = {}

    def print_header(self):
        """Print gamified header."""
        console.print("\n[bold bright_cyan]╔════════════════════════════════════════════════════════╗[/bold bright_cyan]")
        console.print("[bold bright_cyan]║[/bold bright_cyan]  [bold white]REINCARNATION CYCLE VALIDATION LABORATORY[/bold white]  [bold bright_cyan]║[/bold bright_cyan]")
        console.print("[bold bright_cyan]║[/bold bright_cyan]  [dim]The Mutator's Quest: Discover & Validate[/dim]      [bold bright_cyan]║[/bold bright_cyan]")
        console.print("[bold bright_cyan]╚════════════════════════════════════════════════════════╝[/bold bright_cyan]\n")
        console.print(f"[yellow]Scint Earned:[/yellow] {self.scint_earned} points\n")

    def earn_scint(self, points: int, reason: str):
        """Award Scint points."""
        self.scint_earned += points
        console.print(f"\n[bold green]✨ +{points} Scint![/bold green] {reason}")

    def log_validation(self, name: str, passed: bool, details: Dict[str, Any]):
        """Log validation result."""
        if passed:
            self.validations_passed.append({
                "name": name,
                "timestamp": datetime.now().isoformat(),
                "details": details
            })
        else:
            self.validations_failed.append({
                "name": name,
                "timestamp": datetime.now().isoformat(),
                "details": details
            })

    def log_reality_fracture(self, description: str, details: Dict[str, Any]):
        """Log unexpected discovery (Reality Fracture)."""
        self.reality_fractures.append({
            "description": description,
            "timestamp": datetime.now().isoformat(),
            "details": details
        })
        console.print(f"\n[bold magenta]⚠️  REALITY FRACTURE DETECTED![/bold magenta]")
        console.print(f"[magenta]{description}[/magenta]")

    # ===== COMMAND: spawn_being =====

    def cmd_spawn_being(
        self,
        reality_id: str = "validation_reality",
        personality_type: str = "analytical",
        skills: Optional[Dict[str, float]] = None
    ) -> Being:
        """
        Spawn a new Being (lifetime 1).

        Args:
            reality_id: Reality to spawn into
            personality_type: Personality type
            skills: Initial skills dict

        Returns:
            Created Being
        """
        console.print("\n[bold]🌱 SPAWNING BEING...[/bold]")

        if skills is None:
            skills = {
                "perception": 30.0,
                "investigation": 40.0,
                "courage": 25.0,
                "intelligence": 35.0,
            }

        # Use BeingSystem.spawn_being to ensure proper initialization
        being = self.being_system.spawn_being(
            reality_id=reality_id,
            initial_skills=skills
        )

        # Set personality
        being.personality_type = personality_type

        # Create soul_id if not present
        if being.soul_id is None:
            being.soul_id = f"soul_{being.being_id}"

        # Save being
        self.being_system._save_being(being)

        self.current_being = being

        console.print(f"[green]✓[/green] Being spawned: [cyan]{being.being_id[:16]}...[/cyan]")
        console.print(f"  Reality: {reality_id}")
        console.print(f"  Personality: {personality_type}")
        console.print(f"  Lifetimes: {being.lifetimes}")
        console.print(f"  Soul ID: {being.soul_id[:16]}...")
        console.print(f"  Skills: {len(skills)} skills")

        return being

    # ===== COMMAND: run_tavern =====

    def cmd_run_tavern(self, being: Optional[Being] = None) -> Dict[str, Any]:
        """
        Run Being through a simplified tavern scenario to generate memories.

        Args:
            being: Being to run (defaults to current_being)

        Returns:
            Scenario results
        """
        if being is None:
            being = self.current_being

        if being is None:
            console.print("[red]❌ No Being to run! Use spawn_being first.[/red]")
            return {}

        console.print("\n[bold]🏰 RUNNING TAVERN SCENARIO...[/bold]")
        console.print(f"[dim]Being: {being.being_id[:16]}...[/dim]\n")

        # Simulate tavern experiences
        experiences = [
            ("Entered the tavern", "investigation", True, 5.0),
            ("Talked to bartender", "persuasion", True, 8.0),
            ("Found mysterious note", "perception", True, 10.0),
            ("Learned tavern history", "intelligence", True, 7.0),
        ]

        total_fitness = 0.0

        for experience, skill, success, fitness in experiences:
            # Record memory
            being.record_memory(
                experience,
                memory_type="success" if success else "failure",
                metadata={
                    "skill": skill,
                    "success": success,
                    "fitness": fitness
                }
            )

            # Learn skill
            if skill in being.skills:
                being.skills[skill] += 1.0
            else:
                being.skills[skill] = 1.0

            # Update fitness
            being.fitness += fitness
            total_fitness += fitness

            console.print(f"  [green]✓[/green] {experience} (+{fitness:.1f} fitness)")

        # Learn lessons
        being.learn_lesson(
            "Always investigate mysterious notes",
            outcome="success",
            metadata={"fitness_gained": total_fitness}
        )

        # Save updated being
        self.being_system._save_being(being)

        console.print(f"\n[green]✓[/green] Tavern scenario complete!")
        console.print(f"  Memories: {len(being.memories)}")
        console.print(f"  Skills: {len(being.skills)}")
        console.print(f"  Lessons: {len(being.lessons_learned)}")
        console.print(f"  Total Fitness: {being.fitness:.1f}")

        return {
            "memories": len(being.memories),
            "skills": len(being.skills),
            "lessons": len(being.lessons_learned),
            "fitness": being.fitness
        }

    # ===== COMMAND: archive_being =====

    def cmd_archive_being(self, being: Optional[Being] = None) -> Dict[str, Any]:
        """
        Archive (kill) the Being.

        Args:
            being: Being to archive (defaults to current_being)

        Returns:
            Completion record
        """
        if being is None:
            being = self.current_being

        if being is None:
            console.print("[red]❌ No Being to archive! Use spawn_being first.[/red]")
            return {}

        console.print("\n[bold]💀 ARCHIVING BEING...[/bold]")
        console.print(f"[dim]Being: {being.being_id[:16]}...[/dim]\n")

        # Complete being (archive)
        completion_record = self.being_system.complete_being(
            being_id=being.being_id,
            final_fitness=being.fitness
        )

        # Store archived being ID for reincarnation
        self.archived_being_id = being.being_id

        console.print(f"[green]✓[/green] Being archived!")
        console.print(f"  State: [red]ARCHIVED[/red]")
        console.print(f"  Final Fitness: {being.fitness:.1f}")
        console.print(f"  Total Capacity: {completion_record['total_capacity']:.1f}")

        return completion_record

    # ===== COMMAND: reincarnate =====

    def cmd_reincarnate(
        self,
        dead_being_id: Optional[str] = None,
        memory_continuity: float = 0.0
    ) -> Being:
        """
        Reincarnate the archived Being.

        Args:
            dead_being_id: ID of dead Being (defaults to archived_being_id)
            memory_continuity: Memory continuity (0.0-1.0)

        Returns:
            Reincarnated Being
        """
        if dead_being_id is None:
            dead_being_id = self.archived_being_id

        if dead_being_id is None:
            console.print("[red]❌ No archived Being to reincarnate! Use archive_being first.[/red]")
            return None

        console.print("\n[bold]🔄 REINCARNATING BEING...[/bold]")
        console.print(f"[dim]Dead Being: {dead_being_id[:16]}...[/dim]")
        console.print(f"[dim]Memory Continuity: {memory_continuity:.1%}[/dim]\n")

        # Load dead being for reference
        dead_being = self.being_system._load_being(dead_being_id)

        console.print("[dim]Dead Being State:[/dim]")
        console.print(f"  Soul ID: {dead_being.soul_id[:16] if dead_being.soul_id else 'None'}...")
        console.print(f"  Lifetimes: {dead_being.lifetimes}")
        console.print(f"  State: {dead_being.state.value}")
        console.print(f"  Memories: {len(dead_being.memories)}")
        console.print(f"  Skills: {len(dead_being.skills)}")

        # Reincarnate
        purchase_order = {
            "memory_continuity": memory_continuity
        }

        new_being = self.being_system.reincarnate_being(
            dead_being_id=dead_being_id,
            purchase_order=purchase_order
        )

        self.reincarnated_being = new_being
        self.current_being = new_being

        console.print(f"\n[green]✓[/green] Being reincarnated!")
        console.print(f"  New Being: [cyan]{new_being.being_id[:16]}...[/cyan]")
        console.print(f"  Soul ID: {new_being.soul_id[:16] if new_being.soul_id else 'None'}...")
        console.print(f"  Lifetimes: {new_being.lifetimes}")
        console.print(f"  State: {new_being.state.value}")
        console.print(f"  Memories: {len(new_being.memories)}")
        console.print(f"  Skills: {len(new_being.skills)}")

        return new_being

    # ===== VERIFICATION COMMANDS =====

    def cmd_verify_soul(self) -> bool:
        """
        Verify soul_id continuity across reincarnations.

        Returns:
            True if soul_id matches, False otherwise

        Scint Value: 5 points
        """
        console.print("\n[bold]🔍 VERIFYING SOUL ID CONTINUITY...[/bold]")

        if self.archived_being_id is None or self.reincarnated_being is None:
            console.print("[red]❌ Missing archived or reincarnated being![/red]")
            return False

        # Load dead being
        dead_being = self.being_system._load_being(self.archived_being_id)

        # Check soul_id continuity
        dead_soul = dead_being.soul_id
        new_soul = self.reincarnated_being.soul_id

        console.print(f"  Dead Being Soul ID: {dead_soul[:16] if dead_soul else 'None'}...")
        console.print(f"  New Being Soul ID:  {new_soul[:16] if new_soul else 'None'}...")

        if dead_soul == new_soul and dead_soul is not None:
            console.print(f"\n[bold green]✅ SOUL ID CONTINUITY VERIFIED![/bold green]")
            self.earn_scint(5, "Soul ID persists across reincarnations!")
            self.log_validation(
                "Soul ID Continuity",
                True,
                {
                    "dead_soul_id": dead_soul,
                    "new_soul_id": new_soul,
                    "match": True
                }
            )
            self.test_results["soul_id_continuity"] = True
            return True
        else:
            console.print(f"\n[bold red]❌ SOUL ID CONTINUITY FAILED![/bold red]")
            if dead_soul is None:
                console.print("[red]Dead being has no soul_id![/red]")
            elif new_soul is None:
                console.print("[red]New being has no soul_id![/red]")
            else:
                console.print("[red]Soul IDs do not match![/red]")

            self.log_validation(
                "Soul ID Continuity",
                False,
                {
                    "dead_soul_id": dead_soul,
                    "new_soul_id": new_soul,
                    "match": False
                }
            )
            self.test_results["soul_id_continuity"] = False
            return False

    def cmd_verify_lifetimes(self) -> bool:
        """
        Verify lifetimes increments correctly (parent + 1).

        Returns:
            True if lifetimes incremented, False otherwise

        Scint Value: 5 points
        """
        console.print("\n[bold]🔍 VERIFYING LIFETIMES INCREMENT...[/bold]")

        if self.archived_being_id is None or self.reincarnated_being is None:
            console.print("[red]❌ Missing archived or reincarnated being![/red]")
            return False

        # Load dead being
        dead_being = self.being_system._load_being(self.archived_being_id)

        # Check lifetimes increment
        dead_lifetimes = dead_being.lifetimes
        new_lifetimes = self.reincarnated_being.lifetimes
        expected_lifetimes = dead_lifetimes + 1

        console.print(f"  Dead Being Lifetimes: {dead_lifetimes}")
        console.print(f"  New Being Lifetimes:  {new_lifetimes}")
        console.print(f"  Expected Lifetimes:   {expected_lifetimes}")

        if new_lifetimes == expected_lifetimes:
            console.print(f"\n[bold green]✅ LIFETIMES INCREMENT VERIFIED![/bold green]")
            self.earn_scint(5, "Lifetimes increments correctly!")
            self.log_validation(
                "Lifetimes Increment",
                True,
                {
                    "dead_lifetimes": dead_lifetimes,
                    "new_lifetimes": new_lifetimes,
                    "expected": expected_lifetimes,
                    "correct": True
                }
            )
            self.test_results["lifetimes_increment"] = True
            return True
        else:
            console.print(f"\n[bold red]❌ LIFETIMES INCREMENT FAILED![/bold red]")
            console.print(f"[red]Expected {expected_lifetimes}, got {new_lifetimes}[/red]")
            self.log_validation(
                "Lifetimes Increment",
                False,
                {
                    "dead_lifetimes": dead_lifetimes,
                    "new_lifetimes": new_lifetimes,
                    "expected": expected_lifetimes,
                    "correct": False
                }
            )
            self.test_results["lifetimes_increment"] = False
            return False

    def cmd_verify_ancestral_chain(self) -> bool:
        """
        Verify ancestral chain includes parent's lifetimes.

        Returns:
            True if ancestral chain is correct, False otherwise

        Scint Value: 3 points
        """
        console.print("\n[bold]🔍 VERIFYING ANCESTRAL CHAIN...[/bold]")

        if self.archived_being_id is None or self.reincarnated_being is None:
            console.print("[red]❌ Missing archived or reincarnated being![/red]")
            return False

        # Load dead being
        dead_being = self.being_system._load_being(self.archived_being_id)

        # Check ancestral chain
        dead_chain = dead_being.ancestral_chain
        new_chain = self.reincarnated_being.ancestral_chain

        console.print(f"  Dead Being Chain Length: {len(dead_chain)}")
        console.print(f"  New Being Chain Length:  {len(new_chain)}")

        # New being's chain should include dead being's chain + new being
        chain_includes_parent = self.archived_being_id in new_chain
        chain_extends_parent = len(new_chain) > len(dead_chain)

        console.print(f"  Parent in Chain: {chain_includes_parent}")
        console.print(f"  Chain Extended:  {chain_extends_parent}")

        if chain_includes_parent and chain_extends_parent:
            console.print(f"\n[bold green]✅ ANCESTRAL CHAIN VERIFIED![/bold green]")
            self.earn_scint(3, "Ancestral chain properly tracks lineage!")
            self.log_validation(
                "Ancestral Chain",
                True,
                {
                    "dead_chain_length": len(dead_chain),
                    "new_chain_length": len(new_chain),
                    "parent_in_chain": chain_includes_parent,
                    "chain_extended": chain_extends_parent
                }
            )
            self.test_results["ancestral_chain"] = True
            return True
        else:
            console.print(f"\n[bold red]❌ ANCESTRAL CHAIN FAILED![/bold red]")
            if not chain_includes_parent:
                console.print("[red]Parent not found in ancestral chain![/red]")
            if not chain_extends_parent:
                console.print("[red]Chain did not extend![/red]")
            self.log_validation(
                "Ancestral Chain",
                False,
                {
                    "dead_chain_length": len(dead_chain),
                    "new_chain_length": len(new_chain),
                    "parent_in_chain": chain_includes_parent,
                    "chain_extended": chain_extends_parent
                }
            )
            self.test_results["ancestral_chain"] = False
            return False

    def cmd_verify_memories(self, memory_continuity: float = 0.5) -> bool:
        """
        Verify memory inheritance when memory_continuity is specified.

        Args:
            memory_continuity: Expected memory continuity (0.0-1.0)

        Returns:
            True if memories inherited correctly, False otherwise

        Scint Value: 2 points
        """
        console.print("\n[bold]🔍 VERIFYING MEMORY CONTINUITY...[/bold]")
        console.print(f"[dim]Expected Continuity: {memory_continuity:.1%}[/dim]")

        if self.archived_being_id is None or self.reincarnated_being is None:
            console.print("[red]❌ Missing archived or reincarnated being![/red]")
            return False

        # Load dead being
        dead_being = self.being_system._load_being(self.archived_being_id)

        # Check memory inheritance
        dead_memories = len(dead_being.memories)
        new_memories = len(self.reincarnated_being.memories)
        expected_memories = int(dead_memories * memory_continuity)

        console.print(f"  Dead Being Memories: {dead_memories}")
        console.print(f"  New Being Memories:  {new_memories}")
        console.print(f"  Expected Memories:   {expected_memories}")

        # Allow some tolerance (±1 memory)
        memory_ok = abs(new_memories - expected_memories) <= 1

        if memory_continuity > 0.0 and memory_ok:
            console.print(f"\n[bold green]✅ MEMORY CONTINUITY VERIFIED![/bold green]")
            self.earn_scint(2, "Memories inherited correctly!")
            self.log_validation(
                "Memory Continuity",
                True,
                {
                    "dead_memories": dead_memories,
                    "new_memories": new_memories,
                    "expected_memories": expected_memories,
                    "continuity": memory_continuity
                }
            )
            self.test_results["memory_continuity"] = True
            return True
        elif memory_continuity == 0.0 and new_memories == 0:
            console.print(f"\n[bold green]✅ MEMORY CONTINUITY VERIFIED![/bold green]")
            console.print("[dim]No memories expected (continuity = 0.0)[/dim]")
            self.earn_scint(2, "No memory inheritance as expected!")
            self.log_validation(
                "Memory Continuity",
                True,
                {
                    "dead_memories": dead_memories,
                    "new_memories": new_memories,
                    "expected_memories": 0,
                    "continuity": 0.0
                }
            )
            self.test_results["memory_continuity"] = True
            return True
        else:
            console.print(f"\n[bold red]❌ MEMORY CONTINUITY FAILED![/bold red]")
            console.print(f"[red]Expected ~{expected_memories} memories, got {new_memories}[/red]")
            self.log_validation(
                "Memory Continuity",
                False,
                {
                    "dead_memories": dead_memories,
                    "new_memories": new_memories,
                    "expected_memories": expected_memories,
                    "continuity": memory_continuity
                }
            )
            self.test_results["memory_continuity"] = False
            return False

    # ===== REPORT GENERATION =====

    def generate_report(self) -> str:
        """
        Generate validation report with Scint points.

        Returns:
            Report text (markdown)
        """
        report = []
        report.append("# Reincarnation Cycle Validation Report")
        report.append("")
        report.append(f"**Validation Date:** {datetime.now().isoformat()}")
        report.append(f"**Total Scint Earned:** {self.scint_earned} points")
        report.append("")

        # Success criteria
        report.append("## Success Criteria")
        report.append("")

        criteria = [
            ("Soul ID Continuity", self.test_results.get("soul_id_continuity", False)),
            ("Lifetimes Increment", self.test_results.get("lifetimes_increment", False)),
            ("Ancestral Chain", self.test_results.get("ancestral_chain", False)),
            ("Memory Continuity", self.test_results.get("memory_continuity", False)),
        ]

        for name, passed in criteria:
            status = "✅" if passed else "❌"
            report.append(f"- {status} {name}")

        report.append("")

        # Validations passed
        if self.validations_passed:
            report.append("## Validations Passed")
            report.append("")
            for validation in self.validations_passed:
                report.append(f"### {validation['name']}")
                report.append(f"**Timestamp:** {validation['timestamp']}")
                report.append("")
                report.append("**Details:**")
                for key, value in validation['details'].items():
                    report.append(f"- {key}: {value}")
                report.append("")

        # Validations failed
        if self.validations_failed:
            report.append("## Validations Failed")
            report.append("")
            for validation in self.validations_failed:
                report.append(f"### {validation['name']}")
                report.append(f"**Timestamp:** {validation['timestamp']}")
                report.append("")
                report.append("**Details:**")
                for key, value in validation['details'].items():
                    report.append(f"- {key}: {value}")
                report.append("")

        # Reality fractures
        if self.reality_fractures:
            report.append("## Reality Fractures Discovered")
            report.append("")
            for fracture in self.reality_fractures:
                report.append(f"### {fracture['description']}")
                report.append(f"**Timestamp:** {fracture['timestamp']}")
                report.append("")
                report.append("**Details:**")
                for key, value in fracture['details'].items():
                    report.append(f"- {key}: {value}")
                report.append("")

        # Summary
        report.append("## Summary")
        report.append("")
        total_tests = len(criteria)
        tests_passed = sum(1 for _, passed in criteria if passed)
        report.append(f"**Tests Passed:** {tests_passed}/{total_tests}")
        report.append(f"**Total Scint Earned:** {self.scint_earned} points")
        report.append("")

        if tests_passed == total_tests:
            report.append("🎉 **ALL TESTS PASSED!** The reincarnation cycle is fully functional!")
        else:
            report.append(f"⚠️  **{total_tests - tests_passed} test(s) failed.** Further investigation needed.")

        return "\n".join(report)

    def save_report(self, output_path: Optional[Path] = None):
        """Save validation report to file."""
        if output_path is None:
            output_path = Path(__file__).parent / "reincarnation_validation_report.md"

        report = self.generate_report()

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)

        console.print(f"\n[green]✓[/green] Report saved to: {output_path}")
        return output_path


def main():
    """Run validation workflow."""
    validator = ReincarnationValidator()
    validator.print_header()

    console.print("[bold]Starting Reincarnation Cycle Validation...[/bold]\n")

    # Phase 1: Spawn Being
    console.print("[bold cyan]═══ Phase 1: Spawn Being ═══[/bold cyan]")
    being = validator.cmd_spawn_being(
        reality_id="validation_tavern",
        personality_type="analytical"
    )

    # Phase 2: Experience (run tavern)
    console.print("\n[bold cyan]═══ Phase 2: Experience (Tavern) ═══[/bold cyan]")
    validator.cmd_run_tavern(being)

    # Phase 3: Death (archive)
    console.print("\n[bold cyan]═══ Phase 3: Death (Archive) ═══[/bold cyan]")
    validator.cmd_archive_being(being)

    # Phase 4: Rebirth (reincarnate)
    console.print("\n[bold cyan]═══ Phase 4: Rebirth (Reincarnate) ═══[/bold cyan]")
    validator.cmd_reincarnate(memory_continuity=0.5)

    # Phase 5: Verification
    console.print("\n[bold cyan]═══ Phase 5: Verification ═══[/bold cyan]")
    validator.cmd_verify_soul()
    validator.cmd_verify_lifetimes()
    validator.cmd_verify_ancestral_chain()
    validator.cmd_verify_memories(memory_continuity=0.5)

    # Generate report
    console.print("\n[bold cyan]═══ Generating Report ═══[/bold cyan]")
    report_path = validator.save_report()

    # Display summary
    console.print("\n[bold bright_cyan]╔════════════════════════════════════════════════════════╗[/bold bright_cyan]")
    console.print("[bold bright_cyan]║[/bold bright_cyan]  [bold white]VALIDATION COMPLETE![/bold white]                        [bold bright_cyan]║[/bold bright_cyan]")
    console.print("[bold bright_cyan]╚════════════════════════════════════════════════════════╝[/bold bright_cyan]\n")

    console.print(f"[yellow]Total Scint Earned:[/yellow] [bold green]{validator.scint_earned}[/bold green] points")
    console.print(f"[yellow]Validations Passed:[/yellow] {len(validator.validations_passed)}")
    console.print(f"[yellow]Validations Failed:[/yellow] {len(validator.validations_failed)}")
    console.print(f"[yellow]Reality Fractures:[/yellow] {len(validator.reality_fractures)}")
    console.print(f"\n[cyan]Report saved to:[/cyan] {report_path}\n")


if __name__ == "__main__":
    main()
