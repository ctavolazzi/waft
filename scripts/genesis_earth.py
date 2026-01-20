#!/usr/bin/env python3
"""
Genesis Earth Realm Creation

Historic moment: Creates the first "Earth" Realm on Desktop and spawns
the first blank Being (blank canvas that learns) into it.

This script:
1. Creates Earth Realm on Desktop using Waft
2. Spawns first blank Being (empty skills, pure Source)
3. Collects comprehensive observational/computational data
4. Generates PDF documenting this historic moment
5. Opens terminal in Earth directory
"""

import json
import platform
import shutil
import subprocess
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
from waft.evolution.pdf_generator import PDFGenerator
from waft.reality import RealitySystem

console = Console()

# Try to import optional dependencies
try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    console.print("[yellow]⚠[/yellow]  psutil not available - resource metrics will be limited")

try:
    from waft.core.empirica import EmpiricaManager

    EMPIRICA_AVAILABLE = True
except ImportError:
    EMPIRICA_AVAILABLE = False


def get_waft_version() -> str:
    """Get Waft version from pyproject.toml."""
    try:
        pyproject_path = project_root / "pyproject.toml"
        if pyproject_path.exists():
            content = pyproject_path.read_text()
            for line in content.split("\n"):
                if line.startswith("version ="):
                    return line.split("=")[1].strip().strip('"').strip("'")
    except Exception:
        pass
    return "unknown"


def check_waft_cli() -> bool:
    """Check if waft CLI is available."""
    try:
        result = subprocess.run(["waft", "--version"], capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def create_earth_realm(desktop_path: Path) -> Path:
    """
    Create Earth Realm on Desktop using Waft CLI.

    Args:
        desktop_path: Path to Desktop directory

    Returns:
        Path to created Earth directory
    """
    earth_path = desktop_path / "Earth"

    console.print(Panel.fit("[bold cyan]🌍 Creating Earth Realm[/bold cyan]", style="cyan"))

    # Check if Earth already exists
    if earth_path.exists():
        console.print(f"[yellow]⚠[/yellow]  Earth directory already exists: {earth_path}")
        response = input("Continue anyway? (y/n): ").strip().lower()
        if response != "y":
            raise SystemExit("Aborted: Earth directory already exists")

    # Check waft CLI
    if not check_waft_cli():
        raise SystemExit("❌ Error: 'waft' CLI not found. Please install Waft first.")

    console.print(f"[dim]→[/dim] Running: waft new Earth --path {desktop_path}")

    # Run waft new command
    try:
        result = subprocess.run(
            ["waft", "new", "Earth", "--path", str(desktop_path)],
            check=True,
            capture_output=True,
            text=True,
            timeout=120,
        )
        console.print("[green]✓[/green] Earth Realm created successfully")
        console.print(f"[dim]   Output: {result.stdout[:200]}...[/dim]")
    except subprocess.CalledProcessError as e:
        console.print("[bold red]❌ Error creating Earth Realm[/bold red]")
        console.print(f"[red]   {e.stderr}[/red]")
        raise
    except subprocess.TimeoutExpired:
        raise SystemExit("❌ Error: Waft command timed out")

    # Verify structure
    required_paths = [
        earth_path / "pyproject.toml",
        earth_path / "_pyrite",
        earth_path / "_hidden" / ".truth" / "beings",
    ]

    for req_path in required_paths:
        if not req_path.exists():
            console.print(f"[yellow]⚠[/yellow]  Warning: {req_path} not found")

    console.print("[green]✓[/green] Earth Realm structure verified\n")

    return earth_path


def spawn_blank_being(earth_path: Path) -> Any:
    """
    Spawn blank Being (empty skills, pure Source spawn).

    Args:
        earth_path: Path to Earth Realm

    Returns:
        Being instance
    """
    console.print(Panel.fit("[bold cyan]🧬 Spawning Blank Being[/bold cyan]", style="cyan"))

    being_system = BeingSystem(project_path=earth_path)

    console.print("[dim]→[/dim] Spawning Being from Source (blank canvas)...")

    # Spawn blank Being - no initial skills = pure Source
    being = being_system.spawn_being(
        reality_id="earth_reality",
        parent_being_id=None,  # Spawns from Source
        initial_skills={},  # Empty = blank canvas
    )

    console.print(f"[green]✓[/green] Being spawned: [bold]{being.being_id}[/bold]")
    console.print(f"[dim]   Reality: {being.reality_id}[/dim]")
    console.print(f"[dim]   Lifetimes: {being.lifetimes} (First Birth)[/dim]")
    console.print(f"[dim]   Skills: {being.skills} (Blank Canvas)[/dim]")
    console.print(f"[dim]   Ancestral Chain: {', '.join(being.ancestral_chain)}[/dim]\n")

    return being


def collect_observational_data(being: Any, earth_path: Path, timestamp: str) -> dict[str, Any]:
    """
    Collect comprehensive observational/computational data.

    Args:
        being: Being instance
        earth_path: Path to Earth Realm
        timestamp: ISO timestamp

    Returns:
        Dictionary of collected data
    """
    console.print(
        Panel.fit("[bold cyan]📊 Collecting Observational Data[/bold cyan]", style="cyan")
    )

    data = {
        "timestamp": timestamp,
        "being": {},
        "system": {},
        "reality": {},
        "empirica": {},
        "resources": {},
        "directory": {},
    }

    # Being Data
    console.print("[dim]→[/dim] Collecting Being data...")
    data["being"] = {
        "being_id": being.being_id,
        "reality_id": being.reality_id,
        "ancestral_chain": being.ancestral_chain,
        "lifetimes": being.lifetimes,
        "initial_skills": being.skills,
        "state": being.state.value if hasattr(being.state, "value") else str(being.state),
        "stamina": getattr(being, "stamina", None),
        "parent_being_id": being.parent_being_id,
        "empirica_session_id": getattr(being, "empirica_session_id", None),
    }
    console.print("[green]✓[/green] Being data collected")

    # System Data
    console.print("[dim]→[/dim] Collecting system data...")
    data["system"] = {
        "timestamp": timestamp,
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "waft_version": get_waft_version(),
        "project_path": str(earth_path),
        "os": platform.system(),
        "os_version": platform.version(),
    }
    console.print("[green]✓[/green] System data collected")

    # Reality Data
    console.print("[dim]→[/dim] Collecting Reality data...")
    try:
        reality_system = RealitySystem(project_path=earth_path)
        # Try to load the reality
        reality_path = earth_path / "_hidden" / ".truth" / "realities"
        if reality_path.exists():
            reality_files = list(reality_path.glob("*.json"))
            if reality_files:
                # Load first reality file found
                reality_data = json.loads(reality_files[0].read_text())
                data["reality"] = {
                    "reality_id": reality_data.get("reality_id", being.reality_id),
                    "reality_type": reality_data.get("reality_type", "LEARNING"),
                    "configuration": reality_data.get("configuration", {}),
                    "is_active": reality_data.get("is_active", False),
                }
            else:
                data["reality"] = {
                    "reality_id": being.reality_id,
                    "reality_type": "LEARNING",
                    "configuration": {},
                    "note": "Reality file not found, using Being's reality_id",
                }
        else:
            data["reality"] = {
                "reality_id": being.reality_id,
                "note": "Reality directory not found",
            }
    except Exception as e:
        console.print(f"[yellow]⚠[/yellow]  Could not load Reality data: {e}")
        data["reality"] = {"reality_id": being.reality_id, "error": str(e)}
    console.print("[green]✓[/green] Reality data collected")

    # Empirica Data
    console.print("[dim]→[/dim] Collecting Empirica data...")
    if EMPIRICA_AVAILABLE and hasattr(being, "empirica_session_id") and being.empirica_session_id:
        try:
            empirica_manager = EmpiricaManager(project_path=earth_path)
            data["empirica"] = {
                "session_id": being.empirica_session_id,
                "ai_id": being.being_id,
                "session_type": "being_lifecycle",
                "initialized": empirica_manager.is_initialized(),
            }
        except Exception as e:
            data["empirica"] = {
                "error": str(e),
                "note": "Empirica available but data collection failed",
            }
    else:
        data["empirica"] = {
            "available": False,
            "note": "Empirica not available or session not created",
        }
    console.print("[green]✓[/green] Empirica data collected")

    # Resource Metrics
    console.print("[dim]→[/dim] Collecting resource metrics...")
    if PSUTIL_AVAILABLE:
        try:
            # Disk usage
            disk_usage = shutil.disk_usage(earth_path)
            data["resources"] = {
                "disk_total_gb": round(disk_usage.total / (1024**3), 2),
                "disk_used_gb": round(disk_usage.used / (1024**3), 2),
                "disk_free_gb": round(disk_usage.free / (1024**3), 2),
                "memory_available_gb": round(psutil.virtual_memory().available / (1024**3), 2),
                "memory_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
                "cpu_count": psutil.cpu_count(),
            }
        except Exception as e:
            data["resources"] = {"error": str(e)}
    else:
        # Basic directory size without psutil
        try:
            total_size = sum(f.stat().st_size for f in earth_path.rglob("*") if f.is_file())
            data["resources"] = {
                "directory_size_mb": round(total_size / (1024**2), 2),
                "note": "Limited metrics (psutil not available)",
            }
        except Exception as e:
            data["resources"] = {"error": str(e)}
    console.print("[green]✓[/green] Resource metrics collected")

    # Directory Structure
    console.print("[dim]→[/dim] Collecting directory structure...")
    try:

        def get_tree(path: Path, max_depth: int = 3, current_depth: int = 0) -> list:
            """Get directory tree structure."""
            if current_depth >= max_depth:
                return []

            items = []
            try:
                for item in sorted(path.iterdir()):
                    if item.name.startswith("."):
                        continue
                    if item.is_dir():
                        items.append(
                            {
                                "name": item.name,
                                "type": "directory",
                                "path": str(item.relative_to(earth_path)),
                                "children": get_tree(item, max_depth, current_depth + 1),
                            }
                        )
                    else:
                        items.append(
                            {
                                "name": item.name,
                                "type": "file",
                                "path": str(item.relative_to(earth_path)),
                                "size": item.stat().st_size,
                            }
                        )
            except PermissionError:
                pass
            return items

        tree = get_tree(earth_path)
        file_count = sum(1 for _ in earth_path.rglob("*") if _.is_file())
        dir_count = sum(1 for _ in earth_path.rglob("*") if _.is_dir())

        data["directory"] = {
            "structure": tree,
            "file_count": file_count,
            "directory_count": dir_count,
            "key_files": [
                str(p.relative_to(earth_path))
                for p in [
                    earth_path / "pyproject.toml",
                    earth_path / "README.md",
                    earth_path / "_pyrite" / "active",
                    earth_path / "_hidden" / ".truth" / "beings",
                ]
                if p.exists()
            ],
        }
    except Exception as e:
        data["directory"] = {"error": str(e)}
    console.print("[green]✓[/green] Directory structure collected\n")

    return data


def generate_markdown_report(data: dict[str, Any]) -> str:
    """
    Generate markdown report from observational data.

    Args:
        data: Collected observational data

    Returns:
        Markdown content
    """
    being = data["being"]
    system = data["system"]
    reality = data["reality"]
    empirica = data["empirica"]
    resources = data["resources"]
    directory = data["directory"]

    report = f"""# Genesis: Earth Realm Creation

**Timestamp**: {data["timestamp"]}  
**Event**: First Being Spawned into Earth Realm

---

## Being Information

- **Being ID**: `{being["being_id"]}`
- **Reality ID**: `{being["reality_id"]}`
- **Ancestral Chain**: {" → ".join(being["ancestral_chain"])}
- **Lifetimes**: {being["lifetimes"]} (First Birth)
- **Initial Skills**: {json.dumps(being["initial_skills"], indent=2)} (Blank Canvas)
- **State**: {being["state"]}
- **Stamina**: {being.get("stamina", "N/A")}
- **Parent Being ID**: {being.get("parent_being_id", "None (Spawned from Source)")}

---

## System Information

- **Python Version**: {system["python_version"]}
- **Platform**: {system["platform"]}
- **Architecture**: {system["architecture"]}
- **Processor**: {system.get("processor", "N/A")}
- **OS**: {system["os"]}
- **OS Version**: {system["os_version"]}
- **Waft Version**: {system["waft_version"]}
- **Project Path**: `{system["project_path"]}`

---

## Reality Information

- **Reality ID**: `{reality.get("reality_id", "N/A")}`
- **Reality Type**: {reality.get("reality_type", "N/A")}
- **Configuration**: {json.dumps(reality.get("configuration", {}), indent=2)}
- **Is Active**: {reality.get("is_active", False)}

---

## Empirica Session

"""

    if empirica.get("session_id"):
        report += f"""- **Session ID**: `{empirica["session_id"]}`
- **AI ID**: `{empirica["ai_id"]}`
- **Session Type**: {empirica["session_type"]}
- **Initialized**: {empirica.get("initialized", False)}
"""
    else:
        report += f"- **Status**: {empirica.get('note', 'Not available')}\n"

    report += f"""
---

## Directory Structure

- **File Count**: {directory.get("file_count", 0)}
- **Directory Count**: {directory.get("directory_count", 0)}

### Key Files Created:
"""

    for key_file in directory.get("key_files", []):
        report += f"- `{key_file}`\n"

    report += """
### Directory Tree:
```
"""

    def format_tree(items: list, prefix: str = "") -> str:
        """Format directory tree."""
        tree_str = ""
        for i, item in enumerate(items[:20]):  # Limit to first 20 items
            is_last = i == len(items) - 1
            current_prefix = "└── " if is_last else "├── "
            tree_str += f"{prefix}{current_prefix}{item['name']}\n"
            if item["type"] == "directory" and item.get("children"):
                next_prefix = prefix + ("    " if is_last else "│   ")
                tree_str += format_tree(item["children"][:10], next_prefix)  # Limit children
        return tree_str

    if directory.get("structure"):
        report += format_tree(directory["structure"][:15])  # Limit top-level items

    report += "```\n\n---\n\n## Resource Metrics\n\n"

    if "error" not in resources:
        for key, value in resources.items():
            if key != "note":
                report += f"- **{key.replace('_', ' ').title()}**: {value}\n"
        if "note" in resources:
            report += f"\n*Note: {resources['note']}*\n"
    else:
        report += f"- **Error**: {resources['error']}\n"

    report += f"""
---

## Observational Notes

This is a historic moment - the first Being has been spawned into the Earth Realm.
The Being is a blank canvas with no initial skills, ready to learn and evolve.

### Key Observations:

1. **Blank Canvas**: The Being starts with empty skills `{{}}`, representing a pure Source spawn
2. **First Birth**: This is lifetime 1, marking the first generation
3. **Realm Structure**: Earth Realm created with full Waft project structure
4. **Learning Ready**: The Being is ready to begin its learning journey

### Next Steps:

- The Being can now begin learning skills through experience
- The Being can make decisions and evolve
- The Being can spawn descendants (reincarnation)
- The Being can interact with the Reality environment

---

**Generated**: {data["timestamp"]}  
**Script**: `genesis_earth.py`  
**Status**: ✅ Complete
"""

    return report


def generate_pdf(data: dict[str, Any], earth_path: Path) -> Path:
    """
    Generate PDF report from observational data.

    Args:
        data: Collected observational data
        earth_path: Path to Earth Realm

    Returns:
        Path to generated PDF
    """
    console.print(Panel.fit("[bold cyan]📄 Generating PDF Report[/bold cyan]", style="cyan"))

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"GENESIS_EARTH_{timestamp}.pdf"
    pdf_path = earth_path / pdf_filename

    console.print("[dim]→[/dim] Generating markdown content...")
    markdown_content = generate_markdown_report(data)

    console.print("[dim]→[/dim] Creating PDF...")
    try:
        PDFGenerator.from_content(
            content=markdown_content,
            title="Genesis: Earth Realm Creation",
            style="clinical_standard",
        ).save(pdf_path, open_pdf=True)

        console.print(f"[green]✓[/green] PDF generated: [bold]{pdf_filename}[/bold]")
        console.print(f"[dim]   Path: {pdf_path}[/dim]\n")

        return pdf_path
    except Exception as e:
        console.print(f"[bold red]❌ Error generating PDF: {e}[/bold red]")
        raise


def open_terminal(earth_path: Path) -> None:
    """
    Open terminal in Earth directory (macOS).

    Args:
        earth_path: Path to Earth Realm
    """
    console.print(Panel.fit("[bold cyan]💻 Opening Terminal[/bold cyan]", style="cyan"))

    if platform.system() != "Darwin":
        console.print("[yellow]⚠[/yellow]  Terminal opening only supported on macOS")
        console.print(f"[dim]   Please navigate to: {earth_path}[/dim]\n")
        return

    try:
        # Use osascript for better control
        script = f"""
        tell application "Terminal"
            activate
            do script "cd '{earth_path}' && echo '🌍 Earth Realm - Ready for Being interaction' && echo '' && pwd"
        end tell
        """

        subprocess.run(["osascript", "-e", script], check=True, timeout=10)

        console.print("[green]✓[/green] Terminal opened in Earth directory\n")
    except Exception as e:
        console.print(f"[yellow]⚠[/yellow]  Could not open terminal: {e}")
        console.print(f"[dim]   Please navigate to: {earth_path}[/dim]\n")


def main():
    """Main execution function."""
    console.print("\n")
    console.print(
        Panel.fit(
            "[bold cyan]🌍 GENESIS: Earth Realm Creation[/bold cyan]\n"
            "[dim]Historic moment: First Being spawned into Earth Realm[/dim]",
            style="cyan",
        )
    )
    console.print()

    timestamp = datetime.now().isoformat()

    # Step 1: Setup paths
    desktop_path = Path.home() / "Desktop"

    if not desktop_path.exists():
        raise SystemExit(f"❌ Error: Desktop directory not found: {desktop_path}")

    console.print(f"[dim]Desktop path: {desktop_path}[/dim]\n")

    try:
        # Step 2: Create Earth Realm
        earth_path = create_earth_realm(desktop_path)

        # Step 3: Spawn blank Being
        being = spawn_blank_being(earth_path)

        # Step 4: Collect observational data
        observational_data = collect_observational_data(being, earth_path, timestamp)

        # Step 5: Generate PDF
        pdf_path = generate_pdf(observational_data, earth_path)

        # Step 6: Open terminal
        open_terminal(earth_path)

        # Success summary
        console.print(
            Panel.fit(
                "[bold green]✅ Genesis Complete![/bold green]\n\n"
                f"🌍 Earth Realm: [bold]{earth_path}[/bold]\n"
                f"🧬 Being ID: [bold]{being.being_id}[/bold]\n"
                f"📄 PDF Report: [bold]{pdf_path.name}[/bold]\n"
                f"💻 Terminal: Opened in Earth directory",
                style="green",
            )
        )
        console.print()

    except KeyboardInterrupt:
        console.print("\n[yellow]⚠[/yellow]  Interrupted by user")
        raise SystemExit(1)
    except Exception as e:
        console.print(f"\n[bold red]❌ Error: {e}[/bold red]")
        import traceback

        console.print(f"[dim]{traceback.format_exc()}[/dim]")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
