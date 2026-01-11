#!/usr/bin/env python3
"""
WAFT Interactive Demonstration - Meta-Cognitive Edition
========================================================

This demo shows:
1. Creating a messy folder structure
2. Cleaning it up (basic organization)
3. Installing _pyrite for work effort management
4. Demonstrating basic epistemic memory
5. Explaining perspective-taking and meta-cognition

This is WAFT demonstrating its own meta-cognitive capabilities.
"""

import sys
import time
import subprocess
import platform
import random
import shutil
from pathlib import Path
from typing import Optional
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from src.waft.core.memory import MemoryManager

# Initialize rich console
console = Console()


# ============================================================================
# Terminal Animation Utilities
# ============================================================================

def typing_print(text: str, delay: float = 0.03, end: str = "\n"):
    """Print text with typing animation effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(end)
    sys.stdout.flush()


def blinking_cursor(duration: float = 2.0, message: str = "Thinking"):
    """Display a blinking cursor animation."""
    cursor_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    end_time = time.time() + duration
    i = 0

    while time.time() < end_time:
        sys.stdout.write(f'\r{message} {cursor_chars[i % len(cursor_chars)]} ')
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1

    sys.stdout.write('\r' + ' ' * (len(message) + 4) + '\r')
    sys.stdout.flush()


def loading_animation(message: str, duration: float = 1.5):
    """Display a loading animation with dots."""
    end_time = time.time() + duration
    dots = 0

    while time.time() < end_time:
        sys.stdout.write(f'\r{message}{"." * (dots % 4)}{" " * (3 - dots % 4)}')
        sys.stdout.flush()
        time.sleep(0.3)
        dots += 1

    sys.stdout.write(f'\r{message}... ✓\n')
    sys.stdout.flush()


def progress_step(step_num: int, total_steps: int, description: str):
    """Display a progress step."""
    print(f"\n[{step_num}/{total_steps}] {description}")
    loading_animation(f"   {description}", duration=1.0)


def open_file(file_path: Path) -> bool:
    """Open a file using the system's default application."""
    try:
        system = platform.system()
        if system == "Darwin":  # macOS
            subprocess.run(["open", str(file_path)], check=True)
        elif system == "Windows":
            subprocess.run(["start", str(file_path)], shell=True, check=True)
        else:  # Linux
            subprocess.run(["xdg-open", str(file_path)], check=True)
        return True
    except Exception as e:
        console.print(f"   [yellow]⚠️[/yellow]  Could not open file automatically: {e}")
        console.print(f"   [cyan]📄[/cyan] Please open manually: [bold]{file_path}[/bold]")
        return False


# ============================================================================
# Demo Sections
# ============================================================================

def welcome_message():
    """Display welcome message with ASCII art."""
    console.print("\n" + "=" * 80)
    console.print("""
    ██╗    ██╗ █████╗ ███████╗████████╗
    ██║    ██║██╔══██╗██╔════╝╚══██╔══╝
    ██║ █╗ ██║███████║█████╗     ██║
    ██║███╗██║██╔══██║██╔══╝     ██║
    ╚███╔███╔╝██║  ██║██║        ██║
     ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝        ╚═╝

    World Architecture Framework & Templates
    Meta-Cognitive Demonstration
    """)
    console.print("=" * 80)
    console.print()

    console.print("[bold cyan]Welcome to the WAFT Meta-Cognitive Demonstration.[/bold cyan]")
    console.print()
    console.print("Today we're going to show you something that would have been")
    console.print("[yellow]impressive in 2022 when ChatGPT came out...[/yellow]")
    console.print()
    console.print("[bold]But we're going to go much deeper.[/bold]")
    console.print()


def create_messy_demo_folder(demo_dir: Path):
    """Create a messy folder with files scattered everywhere."""
    console.print("\n" + "─" * 80)
    console.print("[bold cyan]📁 STEP 1: CREATING A DEMO FOLDER[/bold cyan]")
    console.print("─" * 80 + "\n")

    console.print("Let's start by creating a demo folder and generating some files...")
    console.print()

    # Create demo directory
    console.print(f"  [cyan]📁[/cyan] Creating directory: [bold]{demo_dir}[/bold]")
    demo_dir.mkdir(parents=True, exist_ok=True)
    console.print(f"     [green]✅[/green] Directory created: {demo_dir}")
    console.print()

    # Create messy files in root
    messy_files = [
        "document1.txt",
        "notes.md",
        "data.json",
        "script.py",
        "output.pdf",
        "temp_file.tmp",
        "old_backup.bak",
        "readme.txt",
        "config.yaml",
        "log.txt",
        "test.py",
        "results.csv",
    ]

    console.print(f"  [cyan]📄[/cyan] Generating [bold]{len(messy_files)}[/bold] files...")
    console.print()

    for i, filename in enumerate(messy_files, 1):
        file_path = demo_dir / filename
        content = f"# {filename}\n\nThis is a demo file created at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        console.print(f"  [dim][{i:2d}/{len(messy_files)}][/dim] Creating: [cyan]{filename}[/cyan]")
        file_path.write_text(content)
        size = file_path.stat().st_size
        console.print(f"       [green]✅[/green] Created ([dim]{size} bytes[/dim])")

    console.print()
    console.print(f"  [green]✅[/green] Created [bold]{len(messy_files)}[/bold] files in the demo folder.")
    console.print()

    # Show the mess
    console.print("\n" + "─" * 80)
    console.print("[bold cyan]📂 CURRENT FOLDER STRUCTURE[/bold cyan]")
    console.print("─" * 80 + "\n")

    files = sorted(demo_dir.glob("*"))
    for f in files:
        if f.is_file():
            size = f.stat().st_size
            console.print(f"  [cyan]📄[/cyan] {f.name:<40} [dim]({size:>4} bytes)[/dim]")

    console.print()

    return messy_files


def comment_on_messiness():
    """Comment on the messy folder structure."""
    console.print("\n" + "─" * 80)
    console.print("[bold yellow]💭 OBSERVATION[/bold yellow]")
    console.print("─" * 80 + "\n")

    console.print("That's great...")
    console.print("[yellow]but it's a little messy, isn't it?[/yellow]")
    console.print()


def clean_up_folder(demo_dir: Path, messy_files: list):
    """Clean up the folder with basic organization."""
    console.print("\n" + "─" * 80)
    console.print("[bold cyan]🧹 STEP 2: CLEANING UP[/bold cyan]")
    console.print("─" * 80 + "\n")

    console.print("Let's organize this into a simple structure...")
    console.print()

    # Create basic folders
    folders = {
        "documents": [f for f in messy_files if f.endswith(('.txt', '.md', '.pdf'))],
        "scripts": [f for f in messy_files if f.endswith('.py')],
        "data": [f for f in messy_files if f.endswith(('.json', '.csv', '.yaml'))],
        "temp": [f for f in messy_files if f.endswith(('.tmp', '.bak'))],
    }

    console.print("  [cyan]📁[/cyan] Creating organization folders...")
    console.print()

    for folder_name, files in folders.items():
        if files:
            folder_path = demo_dir / folder_name
            console.print(f"  [cyan]📁[/cyan] Creating: [bold]{folder_name}/[/bold]")
            folder_path.mkdir(exist_ok=True)
            console.print(f"     [green]✅[/green] Directory created")
            console.print(f"     [cyan]📦[/cyan] Moving [bold]{len(files)}[/bold] file(s)...")

            for filename in files:
                src = demo_dir / filename
                dst = folder_path / filename
                if src.exists():
                    console.print(f"        Moving: [cyan]{filename}[/cyan] → [bold]{folder_name}/[/bold]")
                    shutil.move(str(src), str(dst))
                    console.print(f"        [green]✅[/green] Moved")
            console.print()

    console.print("  [green]✅[/green] Organization complete!")
    console.print()

    console.print("\n" + "─" * 80)
    console.print("[bold cyan]📂 ORGANIZED STRUCTURE[/bold cyan]")
    console.print("─" * 80 + "\n")

    for folder_name in sorted(folders.keys()):
        folder_path = demo_dir / folder_name
        if folder_path.exists():
            files = list(folder_path.glob("*"))
            if files:
                console.print(f"  [cyan]📁[/cyan] [bold]{folder_name}/[/bold]")
                for f in sorted(files):
                    if f.is_file():
                        console.print(f"     └─ [dim]{f.name}[/dim]")

    console.print()
    console.print("[green]✅[/green] Much better! Clean and organized.")
    console.print()


def chatgpt_comment():
    """Make the point about ChatGPT 2022."""
    console.print("\n" + "─" * 80)
    console.print("[bold yellow]💡 THE POINT[/bold yellow]")
    console.print("─" * 80 + "\n")

    console.print("[yellow]That would be impressive...[/yellow]")
    console.print("[yellow]in 2022 when ChatGPT came out.[/yellow]")
    console.print()
    console.print("[bold cyan]Let's show you a little bit of what WAFT is really capable of...[/bold cyan]")
    console.print()


def create_tools_folder(demo_dir: Path):
    """Create the tools folder."""
    console.print("\n" + "─" * 80)
    console.print("[bold cyan]🛠️  STEP 3: CREATING TOOLS FOLDER[/bold cyan]")
    console.print("─" * 80 + "\n")

    console.print("Now let's create a 'tools' folder...")
    console.print()

    tools_dir = demo_dir / "tools"
    console.print(f"  [cyan]📁[/cyan] Creating directory: [bold]tools/[/bold]")
    tools_dir.mkdir(exist_ok=True)
    console.print(f"     [green]✅[/green] Directory created: {tools_dir}")
    console.print()

    return tools_dir


def install_pyrite_demo(tools_dir: Path):
    """Demonstrate installing _pyrite for work effort management."""
    console.print("\n" + "─" * 80)
    console.print("[bold cyan]🔧 STEP 4: INSTALLING _PYRITE[/bold cyan]")
    console.print("─" * 80 + "\n")

    console.print("[cyan]_pyrite[/cyan] is WAFT's work effort management system.")
    console.print()
    console.print("Let's install it in the tools folder...")
    console.print()

    # Create _pyrite structure
    # MemoryManager expects project_path and creates _pyrite inside it
    console.print("  [cyan]🔧[/cyan] Initializing MemoryManager...")
    console.print(f"     Project path: [dim]{tools_dir}[/dim]")
    memory = MemoryManager(tools_dir)
    console.print("     [green]✅[/green] MemoryManager initialized")
    console.print()

    with console.status("[bold cyan]Creating _pyrite structure...[/bold cyan]"):
        memory.create_structure()
    console.print("     [green]✅[/green] Structure creation complete")
    console.print()

    # Verify structure
    pyrite_dir = tools_dir / "_pyrite"
    console.print("  [cyan]🔍[/cyan] Verifying structure...")
    if pyrite_dir.exists():
        console.print(f"     [green]✅[/green] [bold]_pyrite/[/bold] directory exists")
    else:
        console.print(f"     [red]❌[/red] [bold]_pyrite/[/bold] directory missing!")

    for folder in ["active", "backlog", "standards"]:
        folder_path = pyrite_dir / folder
        if folder_path.exists():
            gitkeep = folder_path / ".gitkeep"
            gitkeep_status = "[green]✅[/green]" if gitkeep.exists() else "[yellow]⚠️[/yellow]"
            console.print(f"     [green]✅[/green] [bold]{folder}/[/bold] exists {gitkeep_status} .gitkeep")
        else:
            console.print(f"     [red]❌[/red] [bold]{folder}/[/bold] missing!")
    console.print()

    console.print("  [green]✅[/green] [bold]_pyrite installed![/bold]")
    console.print()

    # Show structure
    console.print("  [cyan]📂[/cyan] Structure created:")
    console.print("     [bold]_pyrite/[/bold]")
    console.print("     ├── [cyan]active/[/cyan]      [dim](current work)[/dim]")
    console.print("     ├── [cyan]backlog/[/cyan]     [dim](future work)[/dim]")
    console.print("     └── [cyan]standards/[/cyan]  [dim](project standards)[/dim]")
    console.print()

    return memory, pyrite_dir


def demonstrate_basic_work_effort(tools_dir: Path, memory: MemoryManager, pyrite_dir: Path):
    """Demonstrate basic work effort management."""
    console.print("\n" + "─" * 80)
    console.print("[bold cyan]📝 STEP 5: BASIC WORK EFFORT MANAGEMENT[/bold cyan]")
    console.print("─" * 80 + "\n")

    console.print("Let's create a simple work effort to track our demo...")
    console.print()

    # Create a simple work effort entry
    active_dir = pyrite_dir / "active"
    console.print(f"  [cyan]📁[/cyan] Using directory: [dim]{active_dir}[/dim]")
    if not active_dir.exists():
        console.print(f"     [yellow]⚠️[/yellow]  Directory doesn't exist, creating...")
        active_dir.mkdir(parents=True, exist_ok=True)
        console.print(f"     [green]✅[/green] Directory created")
    else:
        console.print(f"     [green]✅[/green] Directory exists")
    console.print()

    work_effort_file = active_dir / "demo_work_effort.md"
    console.print(f"  [cyan]📄[/cyan] Creating file: [bold]{work_effort_file.name}[/bold]")

    content = f"""# Demo Work Effort

**Created**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Status**: In Progress

## Objective
Demonstrate WAFT's meta-cognitive capabilities through work effort management.

## Tasks
- [x] Create demo folder
- [x] Generate messy files
- [x] Clean up organization
- [x] Create tools folder
- [x] Install _pyrite
- [ ] Demonstrate work effort tracking
- [ ] Explain meta-cognition

## Notes
This is a basic demonstration of how WAFT tracks its own work.
"""

    print("  ✍️  Writing content...")
    work_effort_file.write_text(content)
    print(f"     ✅ File written: {work_effort_file.name} ({work_effort_file.stat().st_size} bytes)")
    print()

    # Show the file
    print("  📖 Content preview:")
    print("     " + "─" * 70)
    for i, line in enumerate(content.split('\n')[:10], 1):
        print(f"     {i:2d} | {line}")
    print("     " + "─" * 70)
    print()

    # Create a journal entry
    journal_file = active_dir / "demo_journal.md"
    print(f"  📄 Creating file: {journal_file.name}")
    journal_content = f"""# Demo Journal Entry

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## What I'm Doing
Setting up a demo to show WAFT's meta-cognitive capabilities.

## What I'm Thinking
This demo needs to show how WAFT can track its own work and understand
its own state through the work effort system.

## What I'm Learning
The _pyrite system provides a simple but powerful way to track intellectual
labor quanta - discrete units of work and thought.
"""

    print("  ✍️  Writing content...")
    journal_file.write_text(journal_content)
    print(f"     ✅ File written: {journal_file.name} ({journal_file.stat().st_size} bytes)")
    print()

    # Show what's in active
    print("  📂 Listing active work files...")
    active_files = memory.get_active_files()
    print(f"     Found {len(active_files)} file(s):")
    for f in active_files:
        size = f.stat().st_size
        print(f"     └─ {f.name} ({size} bytes)")
    print()

    return work_effort_file, journal_file


def ask_why():
    """Ask the 'but why?' question."""
    console.print("\n" + "─" * 80)
    console.print("[bold yellow]❓ BUT WHY?[/bold yellow]")
    console.print("─" * 80 + "\n")

    console.print("[bold yellow]But why?[/bold yellow]")
    console.print()


def explain_meta_cognition(tools_dir: Path):
    """Explain the meta-cognitive aspect."""
    console.print("\n" + "─" * 80)
    console.print("[bold cyan]🧠 THE ANSWER: META-COGNITION[/bold cyan]")
    console.print("─" * 80 + "\n")

    explanation = """So that WAFT can track on its own what it knows and what it doesn't.

The work efforts ticketing system acts as a sort of rudimentary epistemic
memory - a journal that any LLM can pick up and wear like a pair of glasses
to see how the previous AI saw its world.

This is perspective taking.

This is a very, very, very basic, very very very simple form of LLM
meta-cognition across architectures using a work efforts and journaling
system to track "thoughts" or intellectual labor quanta in the form of text
in the WAFT system, which can self-modify and recursively self-improve based
on external and internal feedback."""

    console.print("  [cyan]💭[/cyan] Explanation:")
    console.print()
    for line in explanation.split('\n'):
        if line.strip():
            console.print(f"     {line.strip()}")
        else:
            console.print()
    console.print()

    # Create a summary document
    summary_file = tools_dir / "meta_cognition_explanation.md"
    console.print(f"  [cyan]📄[/cyan] Creating explanation document: [bold]{summary_file.name}[/bold]")
    summary_content = f"""# Meta-Cognition Explanation

**Created**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## The Core Concept

WAFT's work effort management system provides a form of **epistemic memory** -
a way for AI systems to track what they know and what they don't know.

## How It Works

1. **Work Efforts**: Track discrete units of intellectual labor
2. **Journaling**: Record thoughts, learnings, and observations
3. **Perspective Taking**: New AI instances can "put on" the previous AI's
   perspective by reading the work efforts and journals

## Why It Matters

This enables:
- **Continuity**: Knowledge persists across AI sessions
- **Self-Awareness**: System knows what it knows
- **Recursive Improvement**: System can improve based on its own observations
- **Meta-Cognition**: Thinking about thinking

## The Recursive Loop

1. AI does work → Creates work effort
2. AI reflects → Writes journal entry
3. AI documents → Records what it learned
4. Next AI reads → Understands previous context
5. Next AI continues → Builds on previous knowledge
6. Cycle repeats → Continuous improvement

## Intellectual Labor Quanta

Each work effort, journal entry, or documentation piece represents a
**quantum of intellectual labor** - a discrete unit of thought and work
that can be tracked, measured, and built upon.

## Cross-Architecture Meta-Cognition

This system works across different AI architectures because it's based on
**text** - the universal interface. Any LLM can read and understand:
- Work effort descriptions
- Journal entries
- Documentation
- Status updates

This creates a form of **perspective-taking** where one AI can understand
how another AI (or a previous version of itself) saw the world.
"""

    with console.status("[dim]Writing content...[/dim]"):
        summary_file.write_text(summary_content)
    size = summary_file.stat().st_size
    console.print(f"     [green]✅[/green] File written ([dim]{size} bytes[/dim])")
    console.print()

    return summary_file


def show_final_structure(demo_dir: Path):
    """Show the final organized structure."""
    console.print("\n" + "─" * 80)
    console.print("[bold cyan]📂 FINAL STRUCTURE[/bold cyan]")
    console.print("─" * 80 + "\n")

    console.print("  [cyan]📁[/cyan] Complete directory tree:")
    console.print()

    def print_tree(path: Path, prefix: str = "  ", is_last: bool = True):
        """Print directory tree."""
        name = path.name if path != demo_dir else "demo/"
        connector = "└── " if is_last else "├── "
        if path.is_dir():
            console.print(f"{prefix}{connector}[bold cyan]{name}[/bold cyan]")
        else:
            console.print(f"{prefix}{connector}[dim]{name}[/dim]")

        if path.is_dir():
            children = sorted([p for p in path.iterdir() if p.name != ".gitkeep"])
            for i, child in enumerate(children):
                is_last_child = i == len(children) - 1
                extension = "    " if is_last else "│   "
                print_tree(child, prefix + extension, is_last_child)

    print_tree(demo_dir)
    console.print()


def closing_message(demo_dir: Path):
    """Display closing message."""
    print("\n" + "=" * 80)
    print()
    print("🎉 DEMONSTRATION COMPLETE")
    print()
    print("=" * 80)
    print()

    print("What you just witnessed:")
    print()

    print("  ✅ Basic file organization (2022 ChatGPT level)")
    print("  ✅ Work effort management system")
    print("  ✅ Epistemic memory through _pyrite")
    print("  ✅ Meta-cognitive perspective-taking")
    print("  ✅ Recursive self-improvement foundation")
    print()

    print("This is WAFT tracking its own work, understanding its own state,")
    print("and enabling future AI instances to continue where this one left off.")
    print()

    print("─" * 80)
    print()
    print(f"📁 Demo folder: {demo_dir}")
    print("📖 Explanation: tools/meta_cognition_explanation.md")
    print()
    print("=" * 80)
    print()


# ============================================================================
# Main Demo Flow
# ============================================================================

def main():
    """Run the interactive demonstration."""
    try:
        # Setup
        project_root = Path(__file__).parent.parent
        demo_dir = project_root / "demo_output"
        demo_dir.mkdir(exist_ok=True)

        # 1. Welcome
        welcome_message()

        # 2. Create messy folder
        messy_files = create_messy_demo_folder(demo_dir)

        # 3. Comment on messiness
        comment_on_messiness()

        # 4. Clean up
        clean_up_folder(demo_dir, messy_files)

        # 5. ChatGPT comment
        chatgpt_comment()

        # 6. Create tools folder
        tools_dir = create_tools_folder(demo_dir)

        # 7. Install _pyrite
        memory, pyrite_dir = install_pyrite_demo(tools_dir)

        # 8. Demonstrate work effort
        work_effort_file, journal_file = demonstrate_basic_work_effort(tools_dir, memory, pyrite_dir)

        # 9. Ask why
        ask_why()

        # 10. Explain meta-cognition
        summary_file = explain_meta_cognition(tools_dir)

        # 11. Show final structure
        show_final_structure(demo_dir)

        # 12. Closing
        closing_message(demo_dir)

        # 13. Generate PDF booklet
        console.print("\n" + "─" * 80)
        console.print("[bold cyan]📖 GENERATING DEMO BOOKLET[/bold cyan]")
        console.print("─" * 80 + "\n")
        
        # Import here to avoid circular imports
        sys.path.insert(0, str(Path(__file__).parent))
        from generate_demo_booklet import generate_demo_booklet
        
        booklet_path = demo_dir / "WAFT_Demo_Booklet.pdf"
        console.print(f"  [cyan]📄[/cyan] Generating PDF booklet...")
        console.print(f"     Output: [bold]{booklet_path}[/bold]")
        
        try:
            with console.status("[bold cyan]Creating PDF booklet...[/bold cyan]"):
                generate_demo_booklet(demo_dir, booklet_path)
            console.print(f"     [green]✅[/green] Booklet generated: [bold]{booklet_path}[/bold]")
            console.print()
            
            # Open the PDF
            console.print("  [cyan]📖[/cyan] Opening PDF booklet...")
            if open_file(booklet_path):
                console.print("     [green]✅[/green] PDF opened")
            console.print()
        except Exception as e:
            console.print(f"     [red]❌[/red] Error generating booklet: {e}")
            import traceback
            console.print(f"     [dim]{traceback.format_exc()}[/dim]")
            console.print("     [dim](Continuing without PDF)[/dim]")
            console.print()

        # Optionally open the summary
        console.print()
        console.print("[cyan]Would you like to open the meta-cognition explanation?[/cyan] [dim](y/n):[/dim] ", end="")
        try:
            response = input().strip().lower()
            if response == 'y':
                console.print("  [cyan]📖[/cyan] Opening file...")
                open_file(summary_file)
                console.print("     [green]✅[/green] File opened")
        except (EOFError, KeyboardInterrupt):
            console.print("  [dim](Skipping file open)[/dim]")

    except KeyboardInterrupt:
        print("\n\n" + "=" * 80)
        print("\nDemonstration interrupted by user.")
        print("\n" + "=" * 80 + "\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
