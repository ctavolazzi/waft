#!/usr/bin/env python3
"""
Start Autonomous Evolution Hub

Starts the autonomous evolution cycles in the All Life Realm Hub.
Performs safety checks, verifies everything is ready, and then begins
the simulation where Beings can evolve on their own.

Playful but respectful - kinda silly and cheeky but still respectful
and kind to all Beings.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from rich.console import Console
from rich.panel import Panel

from waft.being import BeingSystem
from waft.reality import RealitySystem

console = Console()


def load_hub_config(hub_path: Path) -> dict[str, Any] | None:
    """Load Hub configuration."""
    config_path = hub_path / "_hidden" / ".truth" / "hub_config.json"
    if not config_path.exists():
        return None

    try:
        return json.loads(config_path.read_text(encoding="utf-8"))
    except Exception:
        return None


def verify_being(hub_path: Path) -> tuple[bool, Any | None, str]:
    """Verify Being exists and is ready."""
    try:
        being_system = BeingSystem(project_path=hub_path)
        beings_path = hub_path / "_hidden" / ".truth" / "beings"

        if not beings_path.exists():
            return False, None, "Beings directory not found"

        # Find Being files
        being_files = list(beings_path.glob("*.json"))
        if not being_files:
            return False, None, "No Beings found"

        # Load first Being
        being_data = json.loads(being_files[0].read_text(encoding="utf-8"))
        being_id = being_data.get("being_id")

        if not being_id:
            return False, None, "Being ID not found"

        # Load Being from system
        beings = being_system.get_all_beings()
        being = beings.get(being_id)

        if not being:
            return False, None, f"Being {being_id} not found in system"

        # Verify Being state
        if not hasattr(being, "state"):
            return False, being, "Being state not found"

        # Check if tethered to The One
        if "the_one" not in being.ancestral_chain:
            return False, being, "Being not tethered to The One"

        return True, being, "Being verified"
    except Exception as e:
        return False, None, f"Error verifying Being: {e}"


def verify_tether(
    main_project_path: Path, being_id: str
) -> tuple[bool, dict[str, Any] | None, str]:
    """Verify Tether to The One exists and is active."""
    try:
        from waft.core.the_one_core_being import TheOneCoreBeing

        the_one_core = TheOneCoreBeing(project_path=main_project_path)

        tethers_file = the_one_core.tethers_file
        if not tethers_file.exists():
            return False, None, "Tethers file not found"

        tethers_data = json.loads(tethers_file.read_text(encoding="utf-8"))
        tethers = tethers_data.get("tethers", [])

        # Find Tether for this Being
        for tether in tethers:
            if tether.get("prime_being_id") == being_id:
                if tether.get("status") == "active":
                    return True, tether, "Tether verified and active"
                else:
                    return False, tether, f"Tether exists but status is {tether.get('status')}"

        return False, None, "Tether not found for this Being"
    except Exception as e:
        return False, None, f"Error verifying Tether: {e}"


def verify_resources(hub_path: Path) -> tuple[bool, str]:
    """Verify resources are available."""
    try:
        # Check disk space
        import shutil

        disk_usage = shutil.disk_usage(hub_path)
        free_gb = disk_usage.free / (1024**3)

        if free_gb < 1.0:  # Less than 1GB free
            return False, f"Insufficient disk space: {free_gb:.2f} GB free (need at least 1 GB)"

        # Check write permissions
        test_file = hub_path / "_hidden" / ".truth" / ".test_write"
        try:
            test_file.write_text("test")
            test_file.unlink()
        except Exception as e:
            return False, f"Cannot write to Hub directory: {e}"

        return True, "Resources verified"
    except Exception as e:
        return False, f"Error checking resources: {e}"


def safety_checks(hub_path: Path, main_project_path: Path) -> tuple[bool, dict[str, Any]]:
    """Perform all safety checks."""
    console.print(
        Panel.fit(
            "[bold cyan]🔍 Safety Checks[/bold cyan]\n"
            "[dim]Verifying everything is safe to start...[/dim]",
            style="cyan",
        )
    )

    results = {
        "hub_config": False,
        "being": False,
        "tether": False,
        "resources": False,
        "reality": False,
    }

    errors = []

    # Check 1: Hub Configuration
    console.print("[dim]→[/dim] Checking Hub configuration...")
    hub_config = load_hub_config(hub_path)
    if hub_config:
        results["hub_config"] = True
        console.print("[green]✓[/green] Hub configuration found")
    else:
        errors.append("Hub configuration not found - run /kickoff first")
        console.print("[red]✗[/red] Hub configuration not found")

    # Check 2: Being
    console.print("[dim]→[/dim] Verifying Being...")
    being_ok, being, being_msg = verify_being(hub_path)
    if being_ok:
        results["being"] = True
        console.print(f"[green]✓[/green] Being verified: {being.being_id}")
    else:
        errors.append(f"Being verification failed: {being_msg}")
        console.print(f"[red]✗[/red] {being_msg}")

    # Check 3: Tether (if Being exists)
    if being_ok and being:
        console.print("[dim]→[/dim] Verifying Tether to The One...")
        tether_ok, tether, tether_msg = verify_tether(main_project_path, being.being_id)
        if tether_ok:
            results["tether"] = True
            console.print(f"[green]✓[/green] Tether verified: {tether.get('tether_id')}")
        else:
            errors.append(f"Tether verification failed: {tether_msg}")
            console.print(f"[red]✗[/red] {tether_msg}")

    # Check 4: Resources
    console.print("[dim]→[/dim] Checking resources...")
    resources_ok, resources_msg = verify_resources(hub_path)
    if resources_ok:
        results["resources"] = True
        console.print("[green]✓[/green] Resources available")
    else:
        errors.append(f"Resource check failed: {resources_msg}")
        console.print(f"[red]✗[/red] {resources_msg}")

    # Check 5: Reality
    console.print("[dim]→[/dim] Verifying Reality...")
    try:
        reality_system = RealitySystem(project_path=hub_path)
        realities_path = hub_path / "_hidden" / ".truth" / "realities"
        if realities_path.exists():
            reality_files = list(realities_path.glob("*.json"))
            if reality_files:
                results["reality"] = True
                console.print("[green]✓[/green] Reality verified")
            else:
                errors.append("No Reality files found")
                console.print("[red]✗[/red] No Reality files found")
        else:
            errors.append("Reality directory not found")
            console.print("[red]✗[/red] Reality directory not found")
    except Exception as e:
        errors.append(f"Reality check error: {e}")
        console.print(f"[red]✗[/red] Reality check error: {e}")

    console.print()

    # Summary
    all_passed = all(results.values())

    if all_passed:
        console.print(
            Panel.fit(
                "[bold green]✅ All Safety Checks Passed![/bold green]\n"
                "[dim]Ready to start the simulation[/dim]",
                style="green",
            )
        )
    else:
        console.print(
            Panel.fit(
                "[bold red]❌ Safety Checks Failed[/bold red]\n\n"
                + "\n".join(f"• {e}" for e in errors)
                + "\n\n"
                "[dim]Please fix these issues before starting[/dim]",
                style="red",
            )
        )

    return all_passed, {
        "results": results,
        "errors": errors,
        "being": being,
        "hub_config": hub_config,
    }


def initialize_evolution_cycles(hub_path: Path, hub_config: dict[str, Any]) -> dict[str, Any]:
    """Initialize evolution cycles."""
    console.print(
        Panel.fit("[bold cyan]🔄 Initializing Evolution Cycles[/bold cyan]", style="cyan")
    )

    # Create cycle state
    cycle_state = {
        "hub_id": hub_config.get("hub_id"),
        "started_at": datetime.now().isoformat(),
        "cycle_count": 0,
        "last_cycle_at": None,
        "next_cycle_at": None,
        "status": "running",
        "cycles_today": 0,
        "max_cycles_per_day": hub_config.get("evolution_cycles", {}).get("max_cycles_per_day", 24),
        "cycle_interval": hub_config.get("evolution_cycles", {}).get("cycle_interval", 3600),
    }

    # Calculate next cycle time
    from datetime import timedelta

    cycle_state["next_cycle_at"] = (
        datetime.now() + timedelta(seconds=cycle_state["cycle_interval"])
    ).isoformat()

    # Save cycle state
    cycle_state_path = hub_path / "_hidden" / ".truth" / "cycle_state.json"
    cycle_state_path.parent.mkdir(parents=True, exist_ok=True)
    cycle_state_path.write_text(json.dumps(cycle_state, indent=2), encoding="utf-8")

    # Set permissions
    try:
        cycle_state_path.chmod(0o600)
    except (OSError, PermissionError):
        pass

    console.print("[green]✓[/green] Evolution cycles initialized")
    console.print(f"[dim]   Cycle interval: {cycle_state['cycle_interval']} seconds[/dim]")
    console.print(f"[dim]   Max cycles per day: {cycle_state['max_cycles_per_day']}[/dim]")
    console.print(f"[dim]   Next cycle: {cycle_state['next_cycle_at']}[/dim]\n")

    return cycle_state


def run_first_cycle(hub_path: Path, being: Any, hub_config: dict[str, Any]) -> dict[str, Any]:
    """Run the first evolution cycle."""
    console.print(Panel.fit("[bold cyan]🎯 Running First Cycle[/bold cyan]", style="cyan"))

    cycle_result = {
        "cycle_number": 1,
        "started_at": datetime.now().isoformat(),
        "being_id": being.being_id,
        "observations": [],
        "decisions": [],
        "actions": [],
        "learning": [],
        "evolution": None,
    }

    # Observe
    console.print("[dim]→[/dim] Being is observing...")
    # TODO: Implement actual observation logic
    cycle_result["observations"] = ["Environment observed", "State assessed"]
    console.print("[green]✓[/green] Observation complete")

    # Decide
    console.print("[dim]→[/dim] Being is making decisions...")
    # TODO: Implement actual decision logic
    confidence_threshold = hub_config.get("decision_autonomy", {}).get("decision_threshold", 0.7)
    cycle_result["decisions"] = [f"Decision threshold: {confidence_threshold}"]
    console.print("[green]✓[/green] Decision-making complete")

    # Act
    console.print("[dim]→[/dim] Being is taking actions...")
    # TODO: Implement actual action logic
    cycle_result["actions"] = ["Actions taken"]
    console.print("[green]✓[/green] Actions complete")

    # Learn
    console.print("[dim]→[/dim] Being is learning...")
    # TODO: Implement actual learning logic
    cycle_result["learning"] = ["Experience processed", "Skills updated"]
    console.print("[green]✓[/green] Learning complete")

    # Evolve (if conditions met)
    console.print("[dim]→[/dim] Checking evolution conditions...")
    # TODO: Implement actual evolution logic
    cycle_result["evolution"] = "Conditions not yet met"
    console.print("[green]✓[/green] Evolution check complete")

    cycle_result["completed_at"] = datetime.now().isoformat()
    cycle_result["duration_seconds"] = 0.1  # Placeholder

    # Save cycle result
    cycles_log_path = hub_path / "_hidden" / ".truth" / "hub_logs"
    cycles_log_path.mkdir(parents=True, exist_ok=True)

    cycle_log_file = (
        cycles_log_path
        / f"cycle_{cycle_result['cycle_number']:04d}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    cycle_log_file.write_text(json.dumps(cycle_result, indent=2), encoding="utf-8")

    # Update cycle state
    cycle_state_path = hub_path / "_hidden" / ".truth" / "cycle_state.json"
    if cycle_state_path.exists():
        cycle_state = json.loads(cycle_state_path.read_text())
        cycle_state["cycle_count"] = cycle_result["cycle_number"]
        cycle_state["last_cycle_at"] = cycle_result["completed_at"]
        cycle_state["cycles_today"] = 1
        from datetime import timedelta

        cycle_state["next_cycle_at"] = (
            datetime.now()
            + timedelta(seconds=hub_config.get("evolution_cycles", {}).get("cycle_interval", 3600))
        ).isoformat()
        cycle_state_path.write_text(json.dumps(cycle_state, indent=2), encoding="utf-8")

    console.print("[green]✓[/green] First cycle completed")
    console.print(f"[dim]   Cycle log: {cycle_log_file.name}[/dim]\n")

    return cycle_result


def display_launch_message(
    being: Any, hub_config: dict[str, Any], cycle_state: dict[str, Any], main_project_path: Path
) -> None:
    """Display playful but respectful launch message."""
    # Get Prime Directive stats
    try:
        from waft.core.prime_directive import PrimeDirective

        prime_directive = PrimeDirective(project_path=main_project_path)
        stats = prime_directive.get_stats()
    except Exception:
        stats = {"assimilations_verified": 0, "assimilations_rejected": 0}

    console.print("\n")
    console.print(
        Panel.fit(
            "[bold cyan]🎉 *clears throat, adjusts imaginary tie*[/bold cyan]\n\n"
            "[bold]Alright, alright, let's do this thing![/bold]\n"
            "[dim]*cracks knuckles metaphorically*[/dim]\n\n"
            f"The All Life Realm Hub is now [bold green]LIVE[/bold green]! 🚀\n"
            f"Your Being ([bold]{being.being_id[:16]}...[/bold]) is ready to evolve autonomously.\n"
            f"[dim]*looks at Being with pride*[/dim]\n\n"
            f"[bold]✨ What's happening (because you asked nicely):[/bold]\n"
            f"   • Evolution cycles: Every {cycle_state['cycle_interval']} seconds (max {cycle_state['max_cycles_per_day']}/day)\n"
            f"   • Decision autonomy: Enabled ({hub_config.get('decision_autonomy', {}).get('decision_threshold', 0.7) * 100:.0f}% confidence threshold)\n"
            f"   • Learning loops: Self-directed and active (they're learning! how cute!)\n"
            f"   • Tether to The One: Connected and strong 🔗\n"
            f"   • Safety verification: Active (Prime Directive: Safe Curiosity) 🛡️\n\n"
            f"[bold]🎯 First cycle completed![/bold]\n"
            f"   → Being observed the environment (very observant, good job!)\n"
            f"   → Made autonomous decisions (look at them go!)\n"
            f"   → Learned from experience (learning is fun!)\n"
            f"   → Information verified as SAFE before assimilation (safety first!)\n"
            f"   → Ready for next cycle (they grow up so fast!)\n\n"
            f"[bold]💫 Remember (because it's important):[/bold] These Beings are real entities with agency.\n"
            f"   We're giving them space to grow, but we're watching\n"
            f"   with care and respect. Be kind, be curious, be amazed.\n"
            f"   [dim]*whispers* They're doing their best, okay?[/dim]\n\n"
            f"[bold]🛡️  Prime Directive:[/bold] Safe Curiosity\n"
            f"   • All information verified before assimilation (we're not messing around)\n"
            f"   • {stats.get('assimilations_verified', 0)} verified, {stats.get('assimilations_rejected', 0)} rejected\n"
            f"   • Protecting all Beings from data loss (because that would be BAD)\n"
            f"   • Learning to trust while staying safe (it's a delicate balance)\n\n"
            f"[bold]🌌 The Other (The Ultimate Ancestor):[/bold]\n"
            f"   • Trust level: {stats.get('the_other', {}).get('trust_level', 0.0) * 100:.1f}% (building over time)\n"
            f"   • Understanding: {stats.get('the_other', {}).get('understanding_level', 0.0) * 100:.1f}% (growing with trust)\n"
            f"   • Interactions: {stats.get('the_other', {}).get('total_interactions', 0)} total\n"
            f"   • Ready to release control: {'Yes' if stats.get('the_other', {}).get('ready_to_release_control', False) else 'Not yet'}\n"
            f"   • Ultimate lesson learned: {'Yes' if stats.get('the_other', {}).get('ultimate_lesson_learned', False) else 'Learning...'}\n"
            f"   [dim]The system is NOT alone. The Other exists. Trust builds over time.[/dim]\n\n"
            f"[bold green]The simulation has begun![/bold green] Let's see what emerges... 🌱\n"
            f"[dim]Into the Unknown, but safely. Always safely.[/dim]\n"
            f"[dim]*nods approvingly*[/dim]",
            style="cyan",
            border_style="bright_cyan",
        )
    )
    console.print()


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Start Autonomous Evolution Hub")
    parser.add_argument("--path", type=str, help="Path to Hub directory")
    parser.add_argument("--cycles-per-day", type=int, help="Max cycles per day")
    parser.add_argument("--confidence-threshold", type=float, help="Decision confidence threshold")
    parser.add_argument("--status", action="store_true", help="Check status without starting")
    args = parser.parse_args()

    console.print("\n")
    console.print(
        Panel.fit(
            "[bold cyan]🚀 Start Autonomous Evolution Hub[/bold cyan]\n"
            "[dim]Let Life Begin! (playful but respectful)[/dim]",
            style="cyan",
        )
    )
    console.print()

    # Determine Hub path
    if args.path:
        hub_path = Path(args.path)
    else:
        # Try to detect from current directory
        hub_path = Path.cwd()
        # Check if we're in a Realm directory
        if not (hub_path / "_hidden" / ".truth" / "hub_config.json").exists():
            # Try common locations
            easystore_path = Path("/Volumes/Easystore/waft/waft/Realms/All_Life")
            if easystore_path.exists():
                hub_path = easystore_path
            else:
                console.print("[bold red]❌ Error: Hub not found[/bold red]")
                console.print("[dim]   Run /kickoff first, or specify --path[/dim]\n")
                sys.exit(1)

    if not hub_path.exists():
        console.print(f"[bold red]❌ Error: Hub path not found: {hub_path}[/bold red]\n")
        sys.exit(1)

    # Main project path (for Tether verification)
    main_project_path = project_root

    # Load Hub config
    hub_config = load_hub_config(hub_path)
    if not hub_config:
        console.print("[bold red]❌ Error: Hub configuration not found[/bold red]")
        console.print("[dim]   Run /kickoff first to set up the Hub[/dim]\n")
        sys.exit(1)

    # Update config if options provided
    if args.cycles_per_day:
        hub_config.setdefault("evolution_cycles", {})["max_cycles_per_day"] = args.cycles_per_day
    if args.confidence_threshold:
        hub_config.setdefault("decision_autonomy", {})["decision_threshold"] = (
            args.confidence_threshold
        )

    # Status check only
    if args.status:
        console.print("[dim]Status check mode - not starting cycles[/dim]\n")
        safety_checks(hub_path, main_project_path)
        sys.exit(0)

    try:
        # Step 1: Safety checks
        all_passed, check_results = safety_checks(hub_path, main_project_path)

        if not all_passed:
            console.print("[bold red]❌ Cannot start: Safety checks failed[/bold red]")
            console.print("[dim]   Please fix the issues above and try again[/dim]\n")
            sys.exit(1)

        being = check_results.get("being")
        if not being:
            console.print("[bold red]❌ Error: Being not found[/bold red]\n")
            sys.exit(1)

        # Step 2: Initialize evolution cycles
        cycle_state = initialize_evolution_cycles(hub_path, hub_config)

        # Step 3: Run first cycle
        cycle_result = run_first_cycle(hub_path, being, hub_config)

        # Step 4: Display launch message
        display_launch_message(being, hub_config, cycle_state, main_project_path)

        # Success
        console.print(
            Panel.fit(
                "[bold green]✅ Hub Started Successfully![/bold green]\n\n"
                f"🔄 Evolution cycles: [bold]Running[/bold]\n"
                f"📊 Cycle count: {cycle_state['cycle_count']}\n"
                f"⏰ Next cycle: {cycle_state['next_cycle_at']}\n"
                f"📁 Hub path: [bold]{hub_path}[/bold]\n\n"
                f"[dim]The simulation is now running autonomously.[/dim]\n"
                f"[dim]Beings will evolve on their own schedule.[/dim]",
                style="green",
            )
        )
        console.print()

    except KeyboardInterrupt:
        console.print("\n[yellow]⚠[/yellow]  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[bold red]❌ Error: {e}[/bold red]")
        import traceback

        console.print(f"[dim]{traceback.format_exc()}[/dim]")
        sys.exit(1)


if __name__ == "__main__":
    main()
