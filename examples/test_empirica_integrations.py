"""
Comprehensive Test Suite for Empirica Integrations

Tests all components to verify Empirica usage:
- TheObserver: Should NOT use Empirica
- TheOracle: Should use Empirica
- TavernKeeper: Should use Empirica
- TheFoundation: Should use Empirica
"""

from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from waft.core.science import TheObserver, TheOracle
from waft.core.tavern_keeper import TavernKeeper
from waft.foundation import TheFoundation

console = Console()


def test_observer():
    """Test TheObserver - should NOT use Empirica."""
    console.print("\n[bold cyan]Testing TheObserver[/bold cyan]")

    observer = TheObserver(Path("."))

    # Check for Empirica usage
    has_empirica_attr = hasattr(observer, "empirica")
    has_empirica_import = False

    # Check source code for Empirica imports
    observer_file = Path("src/waft/core/science/observer.py")
    if observer_file.exists():
        content = observer_file.read_text()
        has_empirica_import = "empirica" in content.lower() or "Empirica" in content

    result = {
        "component": "TheObserver",
        "should_use_empirica": False,
        "has_empirica_attr": has_empirica_attr,
        "has_empirica_import": has_empirica_import,
        "status": "✅ PASS" if not has_empirica_attr and not has_empirica_import else "❌ FAIL",
    }

    console.print(f"  Empirica attribute: {has_empirica_attr}")
    console.print(f"  Empirica import: {has_empirica_import}")
    console.print(f"  Status: {result['status']}")

    return result


def test_oracle():
    """Test TheOracle - should use Empirica."""
    console.print("\n[bold cyan]Testing TheOracle[/bold cyan]")

    try:
        oracle = TheOracle(Path("."))

        has_empirica_attr = hasattr(oracle, "empirica")
        empirica_initialized = oracle.empirica.is_initialized() if has_empirica_attr else False

        # Test methods
        state = oracle.get_epistemic_state()
        phase = oracle.get_epistemic_phase()

        result = {
            "component": "TheOracle",
            "should_use_empirica": True,
            "has_empirica_attr": has_empirica_attr,
            "empirica_initialized": empirica_initialized,
            "methods_work": state is not None and phase is not None,
            "status": "✅ PASS" if has_empirica_attr and empirica_initialized else "❌ FAIL",
        }

        console.print(f"  Empirica attribute: {has_empirica_attr}")
        console.print(f"  Empirica initialized: {empirica_initialized}")
        console.print(f"  Methods work: {result['methods_work']}")
        console.print(f"  Epistemic phase: {phase}")
        console.print(f"  Status: {result['status']}")

    except Exception as e:
        result = {
            "component": "TheOracle",
            "should_use_empirica": True,
            "error": str(e),
            "status": "❌ FAIL",
        }
        console.print(f"  Error: {e}")

    return result


def test_tavern_keeper():
    """Test TavernKeeper - should use Empirica."""
    console.print("\n[bold cyan]Testing TavernKeeper[/bold cyan]")

    try:
        tavern = TavernKeeper(Path("."))

        has_empirica_attr = hasattr(tavern, "empirica")
        empirica_initialized = tavern.empirica.is_initialized() if has_empirica_attr else False

        # Test character operations
        character = tavern.get_character()

        # Test reward (should log to Empirica)
        rewards_result = tavern.award_rewards({"insight": 5.0, "credits": 2})

        result = {
            "component": "TavernKeeper",
            "should_use_empirica": True,
            "has_empirica_attr": has_empirica_attr,
            "empirica_initialized": empirica_initialized,
            "character_works": character is not None,
            "rewards_work": rewards_result is not None,
            "status": "✅ PASS" if has_empirica_attr and empirica_initialized else "❌ FAIL",
        }

        console.print(f"  Empirica attribute: {has_empirica_attr}")
        console.print(f"  Empirica initialized: {empirica_initialized}")
        console.print(f"  Character: {character.get('name')} (Level {character.get('level', 1)})")
        console.print(f"  Rewards applied: {rewards_result.get('level_up', False)}")
        console.print(f"  Status: {result['status']}")

    except Exception as e:
        result = {
            "component": "TavernKeeper",
            "should_use_empirica": True,
            "error": str(e),
            "status": "❌ FAIL",
        }
        console.print(f"  Error: {e}")

    return result


def test_foundation():
    """Test TheFoundation - should use Empirica."""
    console.print("\n[bold cyan]Testing TheFoundation[/bold cyan]")

    try:
        foundation = TheFoundation(Path("."))

        has_empirica_attr = hasattr(foundation, "empirica")
        empirica_initialized = foundation.empirica.is_initialized() if has_empirica_attr else False

        # Check other integrations
        has_observer = hasattr(foundation, "observer")
        has_tavern_keeper = hasattr(foundation, "tavern_keeper")

        result = {
            "component": "TheFoundation",
            "should_use_empirica": True,
            "has_empirica_attr": has_empirica_attr,
            "empirica_initialized": empirica_initialized,
            "has_observer": has_observer,
            "has_tavern_keeper": has_tavern_keeper,
            "status": "✅ PASS" if has_empirica_attr and empirica_initialized else "❌ FAIL",
        }

        console.print(f"  Empirica attribute: {has_empirica_attr}")
        console.print(f"  Empirica initialized: {empirica_initialized}")
        console.print(f"  Observer: {has_observer}")
        console.print(f"  TavernKeeper: {has_tavern_keeper}")
        console.print(f"  Status: {result['status']}")

    except Exception as e:
        result = {
            "component": "TheFoundation",
            "should_use_empirica": True,
            "error": str(e),
            "status": "❌ FAIL",
        }
        console.print(f"  Error: {e}")

    return result


def main():
    console.print(
        Panel.fit(
            "[bold cyan]EMPIRICA INTEGRATION TEST SUITE[/bold cyan]\n"
            "[dim]Testing all components for correct Empirica usage[/dim]",
            border_style="cyan",
        )
    )

    results = []

    # Run all tests
    results.append(test_observer())
    results.append(test_oracle())
    results.append(test_tavern_keeper())
    results.append(test_foundation())

    # Summary table
    console.print("\n[bold]Test Results Summary:[/bold]")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Component", style="cyan")
    table.add_column("Should Use Empirica", style="yellow")
    table.add_column("Status", style="white")
    table.add_column("Details", style="dim")

    for r in results:
        should_use = "✅ YES" if r.get("should_use_empirica") else "❌ NO"
        details = []

        if "error" in r:
            details.append(f"Error: {r['error']}")
        else:
            if r.get("should_use_empirica"):
                details.append(f"Empirica: {r.get('has_empirica_attr', False)}")
                details.append(f"Initialized: {r.get('empirica_initialized', False)}")
            else:
                details.append(f"No Empirica: {not r.get('has_empirica_attr', True)}")

        table.add_row(r["component"], should_use, r["status"], ", ".join(details))

    console.print("\n")
    console.print(table)

    # Overall status
    all_passed = all(r["status"] == "✅ PASS" for r in results)
    if all_passed:
        console.print("\n[bold green]✅ All tests passed![/bold green]")
    else:
        console.print("\n[bold red]❌ Some tests failed[/bold red]")

    return results


if __name__ == "__main__":
    main()
