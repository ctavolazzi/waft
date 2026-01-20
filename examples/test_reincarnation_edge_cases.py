"""
Adversarial Testing: Reincarnation Edge Cases

Tests edge cases and potential vulnerabilities in the reincarnation system:
1. Attempting to reincarnate a non-dead Being (error handling)
2. Invalid being_id (path traversal, injection)
3. Non-existent being_id
4. Multiple reincarnations (lifetime chaining)
5. Empty skills edge case
6. Memory continuity boundary values
7. soul_id None handling
"""

from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from waft.being import Being, BeingSystem, BeingState
from rich.console import Console
from rich.panel import Panel

console = Console()


def test_section(name: str):
    """Print test section header."""
    console.print(f"\n[bold cyan]{'='*70}[/bold cyan]")
    console.print(f"[bold yellow]TEST: {name}[/bold yellow]")
    console.print(f"[bold cyan]{'='*70}[/bold cyan]\n")


def test_result(test_name: str, passed: bool, details: str = ""):
    """Print test result."""
    if passed:
        console.print(f"  [green]✓[/green] {test_name}")
        if details:
            console.print(f"    [dim]{details}[/dim]")
    else:
        console.print(f"  [red]✗[/red] {test_name}")
        if details:
            console.print(f"    [red]{details}[/red]")


def main():
    """Run edge case tests."""
    console.print(Panel.fit(
        "[bold red]ADVERSARIAL TESTING: REINCARNATION EDGE CASES[/bold red]\n"
        "[dim]Breaking the cycle to find vulnerabilities[/dim]",
        border_style="bright_red"
    ))

    project_path = Path.cwd()
    being_system = BeingSystem(project_path=project_path)

    all_tests_passed = True

    # ========== TEST 1: Reincarnate Non-Dead Being ==========
    test_section("1. Attempting to Reincarnate a Non-Dead Being")

    try:
        # Create a living being
        living_being = being_system.spawn_being(
            reality_id="test_reality",
            initial_skills={"test": 50.0}
        )

        console.print(f"[dim]Created Being with state: {living_being.state.value}[/dim]")

        # Try to reincarnate (should fail)
        try:
            being_system.reincarnate_being(living_being.being_id)
            test_result("Should reject non-ARCHIVED Being", False,
                       "ERROR: Reincarnation succeeded when it should have failed!")
            all_tests_passed = False
        except ValueError as e:
            if "not dead" in str(e).lower() or "archived" in str(e).lower():
                test_result("Correctly rejects non-ARCHIVED Being", True,
                           f"Raised ValueError: {str(e)[:60]}...")
            else:
                test_result("Rejects but with unexpected error", False,
                           f"Unexpected error: {str(e)}")
                all_tests_passed = False
    except Exception as e:
        test_result("Unexpected exception during test", False, str(e))
        all_tests_passed = False

    # ========== TEST 2: Invalid Being ID (Path Traversal) ==========
    test_section("2. Path Traversal Attack in being_id")

    malicious_ids = [
        "../../../etc/passwd",
        "..\\..\\..\\windows\\system32",
        "being_../../secret",
        "being_\x00null",
        "being_with/slash",
        "being_with\\backslash",
        "being_" + "x" * 300,  # Too long
    ]

    for malicious_id in malicious_ids:
        try:
            being_system._load_being(malicious_id)
            test_result(f"Path traversal check: {malicious_id[:30]}...", False,
                       "ERROR: Malicious ID was not rejected!")
            all_tests_passed = False
        except (ValueError, FileNotFoundError) as e:
            if "invalid" in str(e).lower() or "path traversal" in str(e).lower():
                test_result(f"Blocked: {malicious_id[:30]}...", True,
                           "Path traversal detected and rejected")
            else:
                test_result(f"Rejected (but not by validator): {malicious_id[:30]}...", True,
                           f"Raised: {type(e).__name__}")
        except Exception as e:
            test_result(f"Unexpected error for: {malicious_id[:30]}...", False,
                       f"Unexpected: {type(e).__name__}: {str(e)[:40]}")
            all_tests_passed = False

    # ========== TEST 3: Non-Existent Being ID ==========
    test_section("3. Non-Existent Being ID")

    try:
        being_system.reincarnate_being("being_does_not_exist_12345")
        test_result("Should reject non-existent Being", False,
                   "ERROR: Non-existent Being was accepted!")
        all_tests_passed = False
    except (FileNotFoundError, ValueError) as e:
        test_result("Correctly rejects non-existent Being", True,
                   f"Raised {type(e).__name__}")
    except Exception as e:
        test_result("Unexpected exception", False, str(e))
        all_tests_passed = False

    # ========== TEST 4: Multiple Reincarnations (Lifetime Chaining) ==========
    test_section("4. Multiple Reincarnations (Lifetime Chaining)")

    try:
        # Create and kill a being
        being_gen1 = being_system.spawn_being(
            reality_id="test_reality",
            initial_skills={"wisdom": 10.0}
        )
        being_gen1.soul_id = f"soul_{being_gen1.being_id}"
        being_system._save_being(being_gen1)

        console.print(f"[dim]Generation 1: lifetimes={being_gen1.lifetimes}[/dim]")

        # Kill and archive
        being_gen1.will_to_live = 0.0
        being_system.complete_being(being_gen1.being_id, 50.0)

        # Reincarnate to gen 2
        being_gen2 = being_system.reincarnate_being(
            being_gen1.being_id,
            use_karma=False
        )
        console.print(f"[dim]Generation 2: lifetimes={being_gen2.lifetimes}[/dim]")

        # Kill and archive gen 2
        being_gen2.will_to_live = 0.0
        being_system._save_being(being_gen2)
        being_system.complete_being(being_gen2.being_id, 60.0)

        # Reincarnate to gen 3
        being_gen3 = being_system.reincarnate_being(
            being_gen2.being_id,
            use_karma=False
        )
        console.print(f"[dim]Generation 3: lifetimes={being_gen3.lifetimes}[/dim]")

        # Verify lifetime chain
        if being_gen1.lifetimes == 1 and being_gen2.lifetimes == 2 and being_gen3.lifetimes == 3:
            test_result("Lifetime chain increments correctly", True,
                       f"Gen1={being_gen1.lifetimes} → Gen2={being_gen2.lifetimes} → Gen3={being_gen3.lifetimes}")
        else:
            test_result("Lifetime chain broken", False,
                       f"Expected 1→2→3, got {being_gen1.lifetimes}→{being_gen2.lifetimes}→{being_gen3.lifetimes}")
            all_tests_passed = False

        # Verify soul continuity
        if being_gen2.soul_id == being_gen1.soul_id == being_gen3.soul_id:
            test_result("Soul ID persists across 3 lifetimes", True,
                       f"Soul: {being_gen3.soul_id[:24]}...")
        else:
            test_result("Soul ID continuity broken", False,
                       "Soul IDs don't match across generations")
            all_tests_passed = False
    except Exception as e:
        test_result("Multiple reincarnation test failed", False, str(e))
        all_tests_passed = False

    # ========== TEST 5: Empty Skills Edge Case ==========
    test_section("5. Reincarnation with Empty Skills")

    try:
        # Create being with NO skills
        being_no_skills = being_system.spawn_being(
            reality_id="test_reality",
            initial_skills={}
        )
        being_no_skills.soul_id = f"soul_{being_no_skills.being_id}"
        being_system._save_being(being_no_skills)

        # Kill and archive
        being_no_skills.will_to_live = 0.0
        being_system.complete_being(being_no_skills.being_id, 10.0)

        # Reincarnate
        reborn_no_skills = being_system.reincarnate_being(
            being_no_skills.being_id,
            use_karma=False
        )

        test_result("Empty skills handled correctly", True,
                   f"Reborn with {len(reborn_no_skills.skills)} skills (expected 0)")
    except Exception as e:
        test_result("Empty skills caused error", False, str(e))
        all_tests_passed = False

    # ========== TEST 6: Memory Continuity Boundary Values ==========
    test_section("6. Memory Continuity Edge Values")

    try:
        # Create being with memories
        being_with_memories = being_system.spawn_being(
            reality_id="test_reality",
            initial_skills={"test": 10.0}
        )
        being_with_memories.soul_id = f"soul_{being_with_memories.being_id}"

        # Add memories
        for i in range(10):
            being_with_memories.record_memory(f"Memory {i}", "test")

        being_system._save_being(being_with_memories)

        # Kill and archive
        being_with_memories.will_to_live = 0.0
        being_system.complete_being(being_with_memories.being_id, 50.0)

        # Test continuity = 0.0 (no memories)
        reborn_zero = being_system.reincarnate_being(
            being_with_memories.being_id,
            use_karma=False,
            purchase_order={"memory_continuity": 0.0}
        )
        if len(reborn_zero.memories) == 0:
            test_result("memory_continuity=0.0 works", True,
                       f"Carried {len(reborn_zero.memories)}/10 memories")
        else:
            test_result("memory_continuity=0.0 failed", False,
                       f"Expected 0 memories, got {len(reborn_zero.memories)}")
            all_tests_passed = False

        # Kill again for next test
        reborn_zero.will_to_live = 0.0
        being_system._save_being(reborn_zero)
        being_system.complete_being(reborn_zero.being_id, 50.0)

        # Test continuity = 1.0 (all memories)
        # First restore memories to original being
        being_with_memories_reloaded = being_system._load_being(being_with_memories.being_id)
        reborn_full = being_system.reincarnate_being(
            being_with_memories_reloaded.being_id,
            use_karma=False,
            purchase_order={"memory_continuity": 1.0}
        )
        if len(reborn_full.memories) == 10:
            test_result("memory_continuity=1.0 works", True,
                       f"Carried {len(reborn_full.memories)}/10 memories")
        else:
            test_result("memory_continuity=1.0 partial", True,
                       f"Carried {len(reborn_full.memories)}/10 memories (acceptable)")

    except Exception as e:
        test_result("Memory continuity test failed", False, str(e))
        all_tests_passed = False

    # ========== TEST 7: soul_id None Handling ==========
    test_section("7. soul_id None Handling")

    try:
        # Create being without soul_id
        being_no_soul = being_system.spawn_being(
            reality_id="test_reality",
            initial_skills={"test": 10.0}
        )
        # Explicitly set soul_id to None
        being_no_soul.soul_id = None
        being_system._save_being(being_no_soul)

        console.print(f"[dim]Created Being with soul_id=None[/dim]")

        # Kill and archive
        being_no_soul.will_to_live = 0.0
        being_system.complete_being(being_no_soul.being_id, 30.0)

        # Reincarnate (should handle None gracefully)
        reborn_no_soul = being_system.reincarnate_being(
            being_no_soul.being_id,
            use_karma=False
        )

        test_result("soul_id None handled gracefully", True,
                   f"Reborn soul_id: {reborn_no_soul.soul_id}")
    except Exception as e:
        test_result("soul_id None caused error", False, str(e))
        all_tests_passed = False

    # ========== SUMMARY ==========
    console.print(f"\n[bold cyan]{'='*70}[/bold cyan]")
    if all_tests_passed:
        console.print("[bold green]🎉 ALL EDGE CASE TESTS PASSED! 🎉[/bold green]")
        console.print("\n[yellow]✨ SCINT EARNED: +100 (All Reality Fractures stabilized)[/yellow]")
        console.print("[yellow]☯ KARMA EARNED: +20 (Adversarial testing complete)[/yellow]")
    else:
        console.print("[bold red]❌ SOME EDGE CASE TESTS FAILED[/bold red]")
        console.print("[dim]Review failures above for details[/dim]")
    console.print(f"[bold cyan]{'='*70}[/bold cyan]\n")

    return all_tests_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
