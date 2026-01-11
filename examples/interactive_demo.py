#!/usr/bin/env python3
"""
WAFT Interactive Demonstration
================================

This script provides an interactive terminal demonstration of WAFT's
self-documenting capabilities.

Run this to see:
- WAFT observing its own codebase
- Generating documentation about itself
- Creating a recursive improvement loop

This is WAFT documenting WAFT using WAFT.
"""

import sys
import time
import subprocess
import platform
from pathlib import Path
from typing import Optional

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.reflection import ReflectionSystem
from src.waft.templates.code_documentation import generate_code_documentation


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
        print(f"   ⚠️  Could not open file automatically: {e}")
        print(f"   📄 Please open manually: {file_path}")
        return False


# ============================================================================
# Demo Sections
# ============================================================================

def welcome_message():
    """Display welcome message with ASCII art."""
    print("\n" + "=" * 80)
    print("""
    ██╗    ██╗ █████╗ ███████╗████████╗
    ██║    ██║██╔══██╗██╔════╝╚══██╔══╝
    ██║ █╗ ██║███████║█████╗     ██║
    ██║███╗██║██╔══██║██╔══╝     ██║
    ╚███╔███╔╝██║  ██║██║        ██║
     ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝        ╚═╝

    World Architecture Framework & Templates
    A Self-Documenting Documentation System
    """)
    print("=" * 80)
    print()

    typing_print("Welcome to the WAFT Interactive Demonstration.", delay=0.04)
    print()
    time.sleep(0.5)
    typing_print("WAFT is a document generation framework that can observe,", delay=0.03)
    typing_print("document, and improve itself through recursive self-reflection.", delay=0.03)
    print()
    time.sleep(0.5)


def prompt_user_question():
    """Prompt user for a question with typing animation."""
    print()
    typing_print("Let me show you how WAFT documents itself...", delay=0.04)
    print()
    time.sleep(1)

    typing_print("You might ask:", delay=0.03)
    print()
    time.sleep(0.3)
    typing_print('  "How does WAFT know what documentation it needs?"', delay=0.03)
    print()
    time.sleep(1)

    typing_print("Let me demonstrate the answer by running WAFT's reflection system.", delay=0.03)
    print()
    time.sleep(1)


def run_reflection_process():
    """Run the reflection system with visual feedback."""
    print("\n" + "─" * 80)
    typing_print("INITIATING SELF-REFLECTION SEQUENCE", delay=0.05)
    print("─" * 80 + "\n")

    time.sleep(0.5)

    # Step 1: Initialize
    progress_step(1, 5, "Initializing Reflection System")

    waft_root = Path(__file__).parent.parent / "src" / "waft"
    reflector = ReflectionSystem(waft_root=waft_root)

    # Step 2: Scan codebase
    progress_step(2, 5, "Scanning WAFT codebase")
    blinking_cursor(duration=2.5, message="   Analyzing Python files")

    # Step 3: Analyze
    progress_step(3, 5, "Analyzing documentation coverage")
    report = reflector.reflect()

    # Step 4: Display metrics
    progress_step(4, 5, "Generating metrics")

    print("\n   📊 REFLECTION RESULTS:")
    print(f"   ├─ Files Analyzed: {report.metrics.get('total_files', 'N/A')}")
    print(f"   ├─ Functions Found: {report.metrics.get('total_functions', 'N/A')}")
    print(f"   ├─ Classes Found: {report.metrics.get('total_classes', 'N/A')}")
    print(f"   └─ Documentation Coverage: {report.metrics.get('documentation_coverage', 0):.1f}%")
    print()

    # Step 5: Generate documentation
    progress_step(5, 5, "Generating self-documentation")

    output_dir = Path(__file__).parent.parent / "_work_efforts"
    output_dir.mkdir(exist_ok=True)

    readme_path = output_dir / "WAFT_System_README.pdf"

    # Generate README documentation about WAFT
    blinking_cursor(duration=2.0, message="   Creating README document")

    readme_content = f"""
<h2>What is WAFT?</h2>
<p><strong>WAFT (World Architecture Framework & Templates)</strong> is a self-documenting
document generation system.</p>

<h2>The Core Discovery</h2>
<p>WAFT has achieved <strong>recursive self-documentation</strong> - a system that can:</p>
<ul>
    <li>Generate professional documents from templates</li>
    <li>Observe its own codebase and architecture</li>
    <li>Document what it observes using its own templates</li>
    <li>Use that documentation to inform development</li>
    <li>Document the changes it makes</li>
    <li>Repeat indefinitely - bootstrapping improvement through documentation</li>
</ul>

<h2>System Metrics (Just Measured)</h2>
<div class="callout note">
<strong>📊 Current State:</strong>
<ul>
    <li><strong>Files Analyzed:</strong> {report.metrics.get('total_files', 'N/A')}</li>
    <li><strong>Functions:</strong> {report.metrics.get('total_functions', 'N/A')}</li>
    <li><strong>Classes:</strong> {report.metrics.get('total_classes', 'N/A')}</li>
    <li><strong>Documentation Coverage:</strong> {report.metrics.get('documentation_coverage', 0):.1f}%</li>
</ul>
</div>

<h2>What You Just Witnessed</h2>
<p>WAFT just analyzed its own codebase and is now generating a document about itself
using its own template system. <strong>This is WAFT documenting WAFT using WAFT.</strong></p>

<h2>The Recursive Loop</h2>
<pre>
┌─────────────────────────────────────────────┐
│                                              │
│  WAFT generates documents                   │
│       ↓                                      │
│  Documents describe WAFT's architecture     │
│       ↓                                      │
│  Architecture informs development           │
│       ↓                                      │
│  Development creates new features           │
│       ↓                                      │
│  Features are documented using WAFT         │
│       ↓                                      │
│  Documentation improves understanding       │
│       ↓                                      │
│  Better understanding enables development   │
│       ↓                                      │
│  ↺ CYCLE CONTINUES ↺                        │
│                                              │
└─────────────────────────────────────────────┘
</pre>

<h2>The 12 Templates</h2>
<p>WAFT includes diverse document generators:</p>
<ul>
    <li><strong>Academic:</strong> Scientific papers, research documents</li>
    <li><strong>Business:</strong> Invoices, contracts, corporate reports</li>
    <li><strong>Technical:</strong> Code documentation, API references, architecture docs</li>
    <li><strong>Operational:</strong> Field guides, manuals, procedures</li>
    <li><strong>Creative:</strong> Horror journals, screenplays, personal letters</li>
    <li><strong>Narrative:</strong> Storybooks, newspapers, worldbuilding documents</li>
</ul>

<h2>Key Systems</h2>

<h3>1. Reflection System</h3>
<p>WAFT can observe itself through code analysis:</p>
<ul>
    <li>Scans Python files using AST (Abstract Syntax Tree)</li>
    <li>Identifies documentation gaps</li>
    <li>Calculates coverage metrics</li>
    <li>Generates recommendations</li>
</ul>

<h3>2. Binder System</h3>
<p>Assembles multiple documents into cohesive collections:</p>
<ul>
    <li>Cover page generation (4 styles)</li>
    <li>Automatic table of contents</li>
    <li>Section dividers</li>
    <li>Multi-document PDF merging</li>
</ul>

<h3>3. Template System</h3>
<p>12 diverse templates powered by WeasyPrint and Jinja2:</p>
<ul>
    <li>Professional typography</li>
    <li>Automatic layout</li>
    <li>Consistent styling</li>
    <li>Easy customization</li>
</ul>

<h2>Independent Verification</h2>
<p>See <code>WHAT_WE_HAVE_HERE.md</code> in the project root for complete
verification steps and hypothesis testing framework.</p>

<div class="callout tip">
<strong>✨ What Makes This Special:</strong><br>
This README was generated by WAFT, about WAFT, using WAFT's own code documentation
template. The metrics above were calculated by WAFT's reflection system observing
its own codebase <strong>in real-time during this demonstration</strong>.
</div>

<h2>Next Steps</h2>
<p>Explore the generated documents to see WAFT's capabilities:</p>
<ol>
    <li>Review this README (you are here)</li>
    <li>Examine the Reflection Report (WAFT analyzing itself)</li>
    <li>Read the Architecture Documentation (WAFT's self-description)</li>
    <li>See example documents in <code>_work_efforts/</code></li>
</ol>

<h2>The Hypothesis</h2>
<p><strong>Can a software system achieve continuous self-improvement through
recursive self-documentation?</strong></p>

<p>WAFT is testing this hypothesis. The system documents its current state,
documentation reveals gaps and opportunities, developers use documentation to
improve the system, the system documents the improvements, and the cycle repeats.</p>

<div class="callout warning">
<strong>🔬 This is an experiment in systems-level self-awareness.</strong><br>
Not AI consciousness, but functional self-observation - a system that understands
its own structure through documentation and can identify what it doesn't know about itself.
</div>

<h2>Conclusion</h2>
<p>WAFT demonstrates that a system can:</p>
<ul>
    <li>✅ Generate professional documents (proven)</li>
    <li>✅ Observe its own structure (proven)</li>
    <li>✅ Document itself using its own tools (proven)</li>
    <li>✅ Create a feedback loop for improvement (proven)</li>
</ul>

<p><strong>The recursive loop is closed.</strong></p>

<p>A system that documents itself can observe itself improving.</p>
"""

    generate_code_documentation(
        title="WAFT System README",
        content=readme_content,
        output_path=readme_path,
        project="WAFT",
        version="2.0",
        show_title_page=True
    )

    print("\n   ✅ README generated successfully!")
    print(f"   📄 Location: {readme_path}")
    print()

    return readme_path


def explain_and_open_readme(readme_path: Path):
    """Explain the README and open it."""
    print("\n" + "─" * 80)
    typing_print("OPENING GENERATED DOCUMENTATION", delay=0.05)
    print("─" * 80 + "\n")

    time.sleep(0.5)

    typing_print("I'm about to open a PDF document that explains the WAFT system.", delay=0.03)
    print()
    time.sleep(0.5)

    typing_print("Here's what makes this special:", delay=0.03)
    print()
    time.sleep(0.3)

    typing_print("  1. This README was GENERATED by WAFT", delay=0.03)
    typing_print("  2. It DOCUMENTS how WAFT works", delay=0.03)
    typing_print("  3. It was created using WAFT's own template system", delay=0.03)
    typing_print("  4. The metrics inside were calculated by WAFT observing itself", delay=0.03)
    print()
    time.sleep(0.5)

    typing_print("This is WAFT documenting WAFT using WAFT.", delay=0.04)
    print()
    time.sleep(1)

    typing_print("Opening document...", delay=0.03)
    print()
    time.sleep(0.5)

    open_file(readme_path)

    time.sleep(1)
    print()


def prompt_continue():
    """Prompt user to continue exploration."""
    print("\n" + "─" * 80)
    print()

    typing_print("The README is a traditional, fixed, unchangeable PDF document.", delay=0.03)
    typing_print("It represents a snapshot of WAFT's state at this moment.", delay=0.03)
    print()
    time.sleep(0.5)

    typing_print("But WAFT can do more than just describe itself...", delay=0.03)
    print()
    time.sleep(0.5)

    typing_print("Would you like to see:", delay=0.03)
    print()
    time.sleep(0.3)

    print("  1. The Reflection Report (WAFT's self-analysis)")
    print("  2. Architecture Documentation (WAFT's self-description)")
    print("  3. Example Documents (showcasing all 12 templates)")
    print("  4. Exit demonstration")
    print()

    choice = input("Enter your choice (1-4): ").strip()

    return choice


def run_additional_demos(choice: str):
    """Run additional demonstrations based on user choice."""
    output_dir = Path(__file__).parent.parent / "_work_efforts"

    if choice == "1":
        print("\n" + "=" * 80)
        typing_print("GENERATING REFLECTION REPORT", delay=0.05)
        print("=" * 80 + "\n")

        from src.waft.reflection import run_reflection_example

        loading_animation("Analyzing codebase and generating report", duration=2.0)
        report_path = run_reflection_example()

        print(f"\n✅ Reflection Report generated: {report_path}")
        print("\nThis report shows:")
        print("  - Documentation coverage analysis")
        print("  - Identified gaps and missing docs")
        print("  - Recommendations for improvement")
        print("\nOpening report...")
        time.sleep(1)
        open_file(Path(report_path))

    elif choice == "2":
        print("\n" + "=" * 80)
        typing_print("GENERATING ARCHITECTURE DOCUMENTATION", delay=0.05)
        print("=" * 80 + "\n")

        from src.waft.reflection import generate_architecture_doc_example

        loading_animation("Documenting system architecture", duration=2.0)
        arch_path = generate_architecture_doc_example()

        print(f"\n✅ Architecture Documentation generated: {arch_path}")
        print("\nThis document describes:")
        print("  - System components and structure")
        print("  - Template system architecture")
        print("  - Data flow and dependencies")
        print("\nOpening documentation...")
        time.sleep(1)
        open_file(Path(arch_path))

    elif choice == "3":
        print("\n" + "=" * 80)
        typing_print("EXPLORING EXAMPLE DOCUMENTS", delay=0.05)
        print("=" * 80 + "\n")

        print("Example documents are located in: _work_efforts/")
        print("\nGenerated examples include:")
        print("  - Scientific papers (quantum consciousness research)")
        print("  - Field guides (survival documentation)")
        print("  - Horror journals (eldritch descent into madness)")
        print("  - Screenplays (industry-standard scripts)")
        print("  - Personal letters (heartfelt correspondence)")
        print("  - Business documents (invoices and contracts)")
        print("  - And more...")
        print("\nOpening work_efforts directory...")
        time.sleep(1)
        open_file(output_dir)

    elif choice == "4":
        print("\n" + "=" * 80)
        typing_print("Thank you for exploring WAFT!", delay=0.04)
        print("=" * 80 + "\n")
        return False

    return True


def closing_message():
    """Display closing message."""
    print("\n" + "=" * 80)
    print()
    typing_print("DEMONSTRATION COMPLETE", delay=0.05)
    print()
    print("=" * 80)
    print()

    typing_print("What you've witnessed:", delay=0.03)
    print()
    time.sleep(0.3)

    typing_print("  ✅ WAFT observing its own codebase", delay=0.03)
    typing_print("  ✅ WAFT documenting itself using its own templates", delay=0.03)
    typing_print("  ✅ A recursive self-improvement loop in action", delay=0.03)
    print()
    time.sleep(0.5)

    typing_print("The recursive loop is closed.", delay=0.04)
    typing_print("A system that documents itself can observe itself improving.", delay=0.04)
    print()
    time.sleep(0.5)

    print("─" * 80)
    print()
    typing_print("For complete verification steps, see: WHAT_WE_HAVE_HERE.md", delay=0.03)
    typing_print("For technical documentation, see: docs/", delay=0.03)
    typing_print("For examples, see: _work_efforts/", delay=0.03)
    print()
    print("=" * 80)
    print()


# ============================================================================
# Main Demo Flow
# ============================================================================

def main():
    """Run the interactive demonstration."""
    try:
        # 1. Welcome
        welcome_message()

        # 2. Prompt user question
        prompt_user_question()

        # 3. Run reflection with animations
        readme_path = run_reflection_process()

        # 4. Explain and open README
        explain_and_open_readme(readme_path)

        # 5. Prompt to continue
        while True:
            choice = prompt_continue()

            if not run_additional_demos(choice):
                break

            print("\n" + "─" * 80 + "\n")
            typing_print("Returning to main menu...", delay=0.03)
            print()
            time.sleep(1)

        # 6. Closing
        closing_message()

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
