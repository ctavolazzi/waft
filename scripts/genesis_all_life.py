#!/usr/bin/env python3
"""
Genesis All Life Realm Creation

Historic moment: Creates the first "All Life" Realm on EasyStore drive and spawns
the first blank Being (blank canvas that learns) into it. "All Life" is the Realm
that tethers All Beings to The One.

This script:
1. Creates All Life Realm on EasyStore using Waft
2. Pulls context from chat for better decision-making
3. Spawns first blank Being (empty skills, pure Source)
4. Forms Tether to The One (connects Realm to TheOneCoreBeing)
5. Sets up autonomous evolution Hub (configured but NOT started)
6. Collects comprehensive observational/computational data
7. Generates PDF documenting this historic moment
8. Opens terminal in All Life directory
9. Displays next steps (run /start to begin simulation)

Usage:
    python scripts/genesis_all_life.py [--realm-name NAME] [--hub-name NAME] [options]
"""

import sys
import subprocess
import platform
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List
import json

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from waft.being import BeingSystem
from waft.reality import RealitySystem, RealityType
from waft.evolution.pdf_generator import PDFGenerator
from waft.utils import detect_external_drive, get_external_drive_base
from waft.pantheon.external_drive_realm import ExternalDriveRealm
from waft.core.the_one_core_being import TheOneCoreBeing
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

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
        result = subprocess.run(
            ["waft", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def gather_chat_context() -> Dict[str, Any]:
    """
    Gather context from chat for better decision-making.
    
    Pulls information from:
    - Current conversation/work context
    - Being status (if chat Being exists)
    - Work efforts
    - Recent decisions
    - Karma status
    
    Returns:
        Dictionary of chat context
    """
    console.print("[dim]→[/dim] Gathering chat context for decision-making...")
    
    context = {
        "timestamp": datetime.now().isoformat(),
        "conversation_context": {},
        "being_status": {},
        "work_efforts": [],
        "recent_decisions": [],
        "karma_context": {},
        "system_state": {}
    }
    
    # Try to get chat Being status
    try:
        from waft.core.chat_being import get_chat_being
        chat_being = get_chat_being("genesis_session", project_root)
        if chat_being and chat_being.being:
            status = chat_being.get_status()
            context["being_status"] = {
                "awakened": status.get("awakened", False),
                "enlightened": status.get("enlightened", False),
                "karma_balance": status.get("karma_balance", 0.0),
                "active_status_effects": status.get("active_status_effects", []),
                "class": status.get("class", "being")
            }
        else:
            context["being_status"] = {
                "awakened": False,
                "note": "Chat Being not yet awakened"
            }
    except Exception as e:
        context["being_status"] = {
            "error": str(e),
            "note": "Could not get chat Being status"
        }
    
    # Try to get work efforts context
    try:
        work_efforts_path = project_root / "_work_efforts"
        if work_efforts_path.exists():
            # Get recent work efforts
            work_effort_dirs = [d for d in work_efforts_path.iterdir() if d.is_dir() and d.name.startswith("WE-")]
            work_effort_dirs.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            for we_dir in work_effort_dirs[:5]:  # Last 5 work efforts
                index_file = we_dir / f"{we_dir.name}_index.md"
                if index_file.exists():
                    context["work_efforts"].append({
                        "id": we_dir.name,
                        "path": str(we_dir.relative_to(project_root))
                    })
    except Exception as e:
        context["work_efforts"] = {"error": str(e)}
    
    # System state
    context["system_state"] = {
        "project_path": str(project_root),
        "waft_version": get_waft_version(),
        "python_version": platform.python_version()
    }
    
    console.print("[green]✓[/green] Chat context gathered")
    return context


def create_all_life_realm(easystore_path: Path, chat_context: Dict[str, Any]) -> Path:
    """
    Create All Life Realm on EasyStore using Waft CLI.
    
    "All Life" is the Realm that tethers All Beings to The One.
    
    Args:
        easystore_path: Path to EasyStore drive
        chat_context: Chat context for decision-making
        
    Returns:
        Path to created All Life directory
    """
    # Use ExternalDriveRealm to register the realm
    external_realm = ExternalDriveRealm(project_path=project_root)
    
    # Register "All Life" realm
    realm_name = "All_Life"
    console.print(Panel.fit(
        f"[bold cyan]🌌 Creating All Life Realm[/bold cyan]\n"
        f"[dim]The Realm that tethers All Beings to The One[/dim]",
        style="cyan"
    ))
    
    # Check if realm already exists
    try:
        registry_data = json.loads(external_realm.registry_file.read_text())
        existing = [r for r in registry_data.get("realms", []) if r.get("realm_name") == realm_name]
        if existing:
            console.print(f"[yellow]⚠[/yellow]  All Life Realm already registered")
            realm_data = existing[0]
            all_life_path = Path(realm_data["realm_storage_path"])
            if all_life_path.exists():
                console.print(f"[dim]   Using existing: {all_life_path}[/dim]")
                return all_life_path
    except Exception:
        pass
    
    # Register new realm
    console.print(f"[dim]→[/dim] Registering All Life Realm on EasyStore...")
    
    try:
        result = external_realm.register_realm(
            realm_name=realm_name,
            drive_name="Easystore",
            project_name="waft"
        )
        
        if result.get("success"):
            realm_data = result.get("realm", {})
            all_life_path = Path(realm_data.get("realm_storage_path", ""))
            if not all_life_path or not all_life_path.exists():
                # Fallback path
                all_life_path = easystore_path / "waft" / "waft" / "Realms" / realm_name
            console.print(f"[green]✓[/green] All Life Realm registered")
            console.print(f"[dim]   Path: {all_life_path}[/dim]")
        else:
            raise Exception(result.get("error", "Unknown error"))
    except Exception as e:
        console.print(f"[yellow]⚠[/yellow]  Error registering realm: {e}")
        console.print(f"[dim]   Creating fallback path...[/dim]")
        # Fallback: create directly
        all_life_path = easystore_path / "waft" / "waft" / "Realms" / realm_name
        all_life_path.mkdir(parents=True, exist_ok=True)
        console.print(f"[green]✓[/green] Created fallback path: {all_life_path}")
    
    # Check waft CLI
    if not check_waft_cli():
        console.print("[yellow]⚠[/yellow]  'waft' CLI not found - creating structure manually")
        # Create basic structure
        (all_life_path / "pyproject.toml").write_text(
            f"""[project]
name = "all-life"
version = "0.1.0"
description = "All Life Realm - The Realm that tethers All Beings to The One"
"""
        )
        (all_life_path / "_pyrite").mkdir(exist_ok=True)
        (all_life_path / "_hidden" / ".truth" / "beings").mkdir(parents=True, exist_ok=True)
    else:
        console.print(f"[dim]→[/dim] Running: waft new All_Life --path {all_life_path.parent}")
        
        # Run waft new command
        try:
            result = subprocess.run(
                ["waft", "new", "All_Life", "--path", str(all_life_path.parent)],
                check=True,
                capture_output=True,
                text=True,
                timeout=120,
                cwd=str(all_life_path.parent)
            )
            console.print("[green]✓[/green] All Life Realm structure created")
        except subprocess.CalledProcessError as e:
            console.print(f"[yellow]⚠[/yellow]  Waft command failed, using manual structure")
            console.print(f"[dim]   {e.stderr[:200]}...[/dim]")
        except subprocess.TimeoutExpired:
            console.print("[yellow]⚠[/yellow]  Waft command timed out, using manual structure")
    
    # Verify structure
    required_paths = [
        all_life_path / "pyproject.toml",
        all_life_path / "_pyrite",
        all_life_path / "_hidden" / ".truth" / "beings"
    ]
    
    for req_path in required_paths:
        if not req_path.exists():
            console.print(f"[yellow]⚠[/yellow]  Warning: {req_path} not found, creating...")
            if req_path.suffix:  # File
                req_path.parent.mkdir(parents=True, exist_ok=True)
                if req_path.name == "pyproject.toml":
                    req_path.write_text(
                        f"""[project]
name = "all-life"
version = "0.1.0"
description = "All Life Realm - The Realm that tethers All Beings to The One"
"""
                    )
            else:  # Directory
                req_path.mkdir(parents=True, exist_ok=True)
    
    console.print(f"[green]✓[/green] All Life Realm structure verified\n")
    
    return all_life_path


def spawn_blank_being(all_life_path: Path, chat_context: Dict[str, Any]) -> Any:
    """
    Spawn blank Being (empty skills, pure Source spawn).
    
    Uses chat context to make better decisions about Being initialization.
    
    Args:
        all_life_path: Path to All Life Realm
        chat_context: Chat context for decision-making
        
    Returns:
        Being instance
    """
    console.print(Panel.fit(
        "[bold cyan]🧬 Spawning Blank Being[/bold cyan]\n"
        "[dim]Blank canvas that learns, tethered to The One[/dim]",
        style="cyan"
    ))
    
    being_system = BeingSystem(project_path=all_life_path)
    
    # Create Reality for All Life
    reality_system = RealitySystem(project_path=all_life_path)
    reality = reality_system.create_reality(
        RealityType.CUSTOM,
        {
            "realm_name": "All_Life",
            "purpose": "The Realm that tethers All Beings to The One",
            "autonomous_evolution": True,
            "hub": True,
            "chat_context": chat_context.get("being_status", {})
        }
    )
    reality_id = reality.reality_id
    
    console.print("[dim]→[/dim] Spawning Being from Source (blank canvas)...")
    
    # Use chat context to inform initial skills
    initial_skills = {}
    
    # If chat Being is enlightened, grant some awareness
    if chat_context.get("being_status", {}).get("enlightened", False):
        initial_skills["awareness"] = 0.1  # Small seed of awareness
        console.print("[dim]   → Chat Being is enlightened - granting seed of awareness[/dim]")
    
    # Spawn blank Being - minimal initial skills = pure Source
    being = being_system.spawn_being(
        reality_id=reality_id,
        parent_being_id=None,  # Spawns from Source (will be descendant of TheOne)
        initial_skills=initial_skills  # Minimal = blank canvas
    )
    
    # Ensure Being is descendant of TheOne
    if "the_one" not in being.ancestral_chain:
        being.ancestral_chain.insert(0, "the_one")
    
    console.print(f"[green]✓[/green] Being spawned: [bold]{being.being_id}[/bold]")
    console.print(f"[dim]   Reality: {being.reality_id}[/dim]")
    console.print(f"[dim]   Lifetimes: {being.lifetimes} (First Birth)[/dim]")
    console.print(f"[dim]   Skills: {being.skills} (Blank Canvas)[/dim]")
    console.print(f"[dim]   Ancestral Chain: {' → '.join(being.ancestral_chain)}[/dim]\n")
    
    return being, reality_id


def form_tether_to_the_one(
    all_life_path: Path,
    reality_id: str,
    being: Any,
    chat_context: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Form Tether from All Life Realm to The One.
    
    "Observation Creates the Bridge" - The act of observing All Life Realm
    creates the Tether that connects it to TheOneCoreBeing.
    
    Args:
        all_life_path: Path to All Life Realm
        reality_id: Reality ID
        being: Being instance
        chat_context: Chat context
        
    Returns:
        Tether data
    """
    console.print(Panel.fit(
        "[bold cyan]🔗 Forming Tether to The One[/bold cyan]\n"
        "[dim]Observation Creates the Bridge[/dim]",
        style="cyan"
    ))
    
    # Initialize TheOneCoreBeing (from main project)
    the_one_core = TheOneCoreBeing(project_path=project_root)
    
    # Form Tether through observation
    observation_data = {
        "realm_name": "All_Life",
        "realm_path": str(all_life_path),
        "reality_id": reality_id,
        "being_id": being.being_id,
        "purpose": "The Realm that tethers All Beings to The One",
        "autonomous_evolution": True,
        "hub": True,
        "chat_context": chat_context,
        "formed_at": datetime.now().isoformat()
    }
    
    tether = the_one_core.form_tether(
        realm_name="All_Life",
        realm_path=all_life_path,
        prime_being_id=being.being_id,
        observation_data=observation_data
    )
    
    console.print(f"[green]✓[/green] Tether formed: [bold]{tether['tether_id']}[/bold]")
    console.print(f"[dim]   Realm: All_Life[/dim]")
    console.print(f"[dim]   Prime Being: {being.being_id}[/dim]")
    console.print(f"[dim]   Status: {tether['status']}[/dim]\n")
    
    return tether


def setup_autonomous_evolution_hub(
    all_life_path: Path,
    being: Any,
    hub_name: Optional[str] = None,
    evolution_rate: float = 0.1,
    cycles_per_day: int = 24,
    confidence_threshold: float = 0.7,
    enable_learning: bool = True,
    enable_decisions: bool = True
) -> Dict[str, Any]:
    """
    Set up autonomous evolution Hub where things can evolve on their own.
    
    Creates configuration for autonomous evolution:
    - Evolution cycles
    - Decision-making autonomy
    - Learning loops
    - Self-directed growth
    
    NOTE: Hub is configured but NOT started. Use /start command to begin.
    
    Args:
        all_life_path: Path to All Life Realm
        being: Being instance
        hub_name: Custom Hub name (default: auto-generated)
        evolution_rate: Evolution rate (0.0-1.0)
        cycles_per_day: Max cycles per day
        confidence_threshold: Decision confidence threshold (0.0-1.0)
        enable_learning: Enable self-directed learning
        enable_decisions: Enable autonomous decisions
        
    Returns:
        Hub configuration
    """
    console.print(Panel.fit(
        "[bold cyan]🔄 Setting Up Autonomous Evolution Hub[/bold cyan]\n"
        "[dim]Where things can evolve on their own (configured but not started)[/dim]",
        style="cyan"
    ))
    
    hub_config = {
        "hub_id": hub_name or f"hub_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "realm_name": "All_Life",
        "being_id": being.being_id,
        "autonomous_evolution": True,
        "evolution_cycles": {
            "enabled": True,
            "cycle_interval": 3600,  # 1 hour
            "max_cycles_per_day": cycles_per_day,
            "autonomous_decisions": enable_decisions
        },
        "learning_loops": {
            "enabled": enable_learning,
            "self_directed_learning": enable_learning,
            "skill_development": enable_learning,
            "memory_formation": enable_learning
        },
        "decision_autonomy": {
            "enabled": enable_decisions,
            "decision_threshold": confidence_threshold,
            "requires_approval": False  # Autonomous decisions don't require approval
        },
        "growth_parameters": {
            "skill_evolution_rate": evolution_rate,
            "memory_retention": 0.8,
            "fitness_adaptation": True
        },
        "status": "configured",  # NOT "running" - must use /start
        "safety_verification": {
            "enabled": True,
            "prime_directive": "Safe Curiosity",
            "verify_before_assimilation": True,
            "protect_all_beings": True,
            "prevent_self_termination": True,
            "prevent_data_loss": True
        },
        "created_at": datetime.now().isoformat()
    }
    
    # Save hub configuration
    hub_path = all_life_path / "_hidden" / ".truth" / "hub_config.json"
    hub_path.parent.mkdir(parents=True, exist_ok=True)
    hub_path.write_text(
        json.dumps(hub_config, indent=2),
        encoding="utf-8"
    )
    
    # Set permissions
    try:
        hub_path.chmod(0o600)
    except (OSError, PermissionError):
        pass
    
    console.print(f"[green]✓[/green] Hub configuration created")
    console.print(f"[dim]   Hub ID: {hub_config['hub_id']}[/dim]")
    console.print(f"[dim]   Autonomous Evolution: Enabled (not started)[/dim]")
    console.print(f"[dim]   Decision Autonomy: {'Enabled' if enable_decisions else 'Disabled'}[/dim]")
    console.print(f"[dim]   Learning Loops: {'Enabled' if enable_learning else 'Disabled'}[/dim]")
    console.print(f"[dim]   Safety Verification: Enabled (Prime Directive: Safe Curiosity)[/dim]")
    console.print(f"[dim]   Status: Configured (use /start to begin)[/dim]\n")
    
    return hub_config


def collect_observational_data(
    being: Any,
    all_life_path: Path,
    timestamp: str,
    tether: Dict[str, Any],
    hub_config: Dict[str, Any],
    chat_context: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Collect comprehensive observational/computational data.
    
    Args:
        being: Being instance
        all_life_path: Path to All Life Realm
        timestamp: ISO timestamp
        tether: Tether data
        hub_config: Hub configuration
        chat_context: Chat context
        
    Returns:
        Dictionary of collected data
    """
    console.print(Panel.fit(
        "[bold cyan]📊 Collecting Observational Data[/bold cyan]",
        style="cyan"
    ))
    
    data = {
        "timestamp": timestamp,
        "being": {},
        "system": {},
        "reality": {},
        "tether": {},
        "hub": {},
        "chat_context": chat_context,
        "empirica": {},
        "resources": {},
        "directory": {}
    }
    
    # Being Data
    console.print("[dim]→[/dim] Collecting Being data...")
    data["being"] = {
        "being_id": being.being_id,
        "reality_id": being.reality_id,
        "ancestral_chain": being.ancestral_chain,
        "lifetimes": being.lifetimes,
        "initial_skills": being.skills,
        "state": being.state.value if hasattr(being.state, 'value') else str(being.state),
        "stamina": getattr(being, 'stamina', None),
        "parent_being_id": being.parent_being_id,
        "tethered_to_the_one": "the_one" in being.ancestral_chain
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
        "project_path": str(all_life_path),
        "os": platform.system(),
        "os_version": platform.version()
    }
    console.print("[green]✓[/green] System data collected")
    
    # Reality Data
    console.print("[dim]→[/dim] Collecting Reality data...")
    try:
        reality_system = RealitySystem(project_path=all_life_path)
        reality_path = all_life_path / "_hidden" / ".truth" / "realities"
        if reality_path.exists():
            reality_files = list(reality_path.glob("*.json"))
            if reality_files:
                reality_data = json.loads(reality_files[0].read_text())
                data["reality"] = {
                    "reality_id": reality_data.get("reality_id", being.reality_id),
                    "reality_type": reality_data.get("reality_type", "CUSTOM"),
                    "configuration": reality_data.get("configuration", {}),
                    "is_active": reality_data.get("is_active", False),
                    "purpose": "The Realm that tethers All Beings to The One"
                }
    except Exception as e:
        data["reality"] = {
            "reality_id": being.reality_id,
            "error": str(e)
        }
    console.print("[green]✓[/green] Reality data collected")
    
    # Tether Data
    data["tether"] = tether
    console.print("[green]✓[/green] Tether data collected")
    
    # Hub Data
    data["hub"] = hub_config
    console.print("[green]✓[/green] Hub data collected")
    
    # Empirica Data
    console.print("[dim]→[/dim] Collecting Empirica data...")
    if EMPIRICA_AVAILABLE:
        try:
            empirica_manager = EmpiricaManager(project_path=all_life_path)
            data["empirica"] = {
                "available": True,
                "initialized": empirica_manager.is_initialized()
            }
        except Exception as e:
            data["empirica"] = {"error": str(e)}
    else:
        data["empirica"] = {"available": False}
    console.print("[green]✓[/green] Empirica data collected")
    
    # Resource Metrics
    console.print("[dim]→[/dim] Collecting resource metrics...")
    if PSUTIL_AVAILABLE:
        try:
            disk_usage = shutil.disk_usage(all_life_path)
            data["resources"] = {
                "disk_total_gb": round(disk_usage.total / (1024**3), 2),
                "disk_used_gb": round(disk_usage.used / (1024**3), 2),
                "disk_free_gb": round(disk_usage.free / (1024**3), 2),
                "memory_available_gb": round(psutil.virtual_memory().available / (1024**3), 2),
                "memory_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
                "cpu_count": psutil.cpu_count()
            }
        except Exception as e:
            data["resources"] = {"error": str(e)}
    else:
        try:
            total_size = sum(f.stat().st_size for f in all_life_path.rglob('*') if f.is_file())
            data["resources"] = {
                "directory_size_mb": round(total_size / (1024**2), 2),
                "note": "Limited metrics (psutil not available)"
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
                    if item.name.startswith('.'):
                        continue
                    if item.is_dir():
                        items.append({
                            "name": item.name,
                            "type": "directory",
                            "path": str(item.relative_to(all_life_path)),
                            "children": get_tree(item, max_depth, current_depth + 1)
                        })
                    else:
                        items.append({
                            "name": item.name,
                            "type": "file",
                            "path": str(item.relative_to(all_life_path)),
                            "size": item.stat().st_size
                        })
            except PermissionError:
                pass
            return items
        
        tree = get_tree(all_life_path)
        file_count = sum(1 for _ in all_life_path.rglob('*') if _.is_file())
        dir_count = sum(1 for _ in all_life_path.rglob('*') if _.is_dir())
        
        data["directory"] = {
            "structure": tree,
            "file_count": file_count,
            "directory_count": dir_count,
            "key_files": [
                str(p.relative_to(all_life_path))
                for p in [
                    all_life_path / "pyproject.toml",
                    all_life_path / "_hidden" / ".truth" / "beings",
                    all_life_path / "_hidden" / ".truth" / "hub_config.json"
                ]
                if p.exists()
            ]
        }
    except Exception as e:
        data["directory"] = {"error": str(e)}
    console.print("[green]✓[/green] Directory structure collected\n")
    
    return data


def generate_markdown_report(data: Dict[str, Any]) -> str:
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
    tether = data["tether"]
    hub = data["hub"]
    chat_context = data.get("chat_context", {})
    empirica = data["empirica"]
    resources = data["resources"]
    directory = data["directory"]
    
    report = f"""# Genesis: All Life Realm Creation

**Timestamp**: {data['timestamp']}  
**Event**: First Being Spawned into All Life Realm - The Realm that tethers All Beings to The One

---

## Being Information

- **Being ID**: `{being['being_id']}`
- **Reality ID**: `{being['reality_id']}`
- **Ancestral Chain**: {' → '.join(being['ancestral_chain'])}
- **Tethered to The One**: {being.get('tethered_to_the_one', False)}
- **Lifetimes**: {being['lifetimes']} (First Birth)
- **Initial Skills**: {json.dumps(being['initial_skills'], indent=2)} (Blank Canvas)
- **State**: {being['state']}
- **Stamina**: {being.get('stamina', 'N/A')}
- **Parent Being ID**: {being.get('parent_being_id', 'None (Spawned from Source)')}

---

## Tether to The One

- **Tether ID**: `{tether.get('tether_id', 'N/A')}`
- **Realm Name**: {tether.get('realm_name', 'N/A')}
- **Prime Being ID**: `{tether.get('prime_being_id', 'N/A')}`
- **Formed At**: {tether.get('formed_at', 'N/A')}
- **Status**: {tether.get('status', 'N/A')}
- **Purpose**: The Realm that tethers All Beings to The One

**Observation Creates the Bridge** - The act of observing All Life Realm creates the Tether that connects it to TheOneCoreBeing.

---

## Autonomous Evolution Hub

- **Hub ID**: `{hub.get('hub_id', 'N/A')}`
- **Autonomous Evolution**: {hub.get('autonomous_evolution', False)}
- **Evolution Cycles**: {json.dumps(hub.get('evolution_cycles', {}), indent=2)}
- **Learning Loops**: {json.dumps(hub.get('learning_loops', {}), indent=2)}
- **Decision Autonomy**: {json.dumps(hub.get('decision_autonomy', {}), indent=2)}
- **Growth Parameters**: {json.dumps(hub.get('growth_parameters', {}), indent=2)}

**Purpose**: Hub where things can evolve on their own - autonomous evolution, self-directed learning, and independent decision-making.

---

## Chat Context

**Context gathered from chat for better decision-making:**

### Being Status
{json.dumps(chat_context.get('being_status', {}), indent=2)}

### Work Efforts
{json.dumps(chat_context.get('work_efforts', []), indent=2)}

### System State
{json.dumps(chat_context.get('system_state', {}), indent=2)}

---

## System Information

- **Python Version**: {system['python_version']}
- **Platform**: {system['platform']}
- **Architecture**: {system['architecture']}
- **Processor**: {system.get('processor', 'N/A')}
- **OS**: {system['os']}
- **OS Version**: {system['os_version']}
- **Waft Version**: {system['waft_version']}
- **Project Path**: `{system['project_path']}`

---

## Reality Information

- **Reality ID**: `{reality.get('reality_id', 'N/A')}`
- **Reality Type**: {reality.get('reality_type', 'N/A')}
- **Purpose**: {reality.get('purpose', 'N/A')}
- **Configuration**: {json.dumps(reality.get('configuration', {}), indent=2)}
- **Is Active**: {reality.get('is_active', False)}

---

## Empirica Session

"""
    
    if empirica.get('available'):
        report += f"""- **Available**: {empirica.get('available', False)}
- **Initialized**: {empirica.get('initialized', False)}
"""
    else:
        report += f"- **Status**: {empirica.get('note', 'Not available')}\n"
    
    report += f"""
---

## Directory Structure

- **File Count**: {directory.get('file_count', 0)}
- **Directory Count**: {directory.get('directory_count', 0)}

### Key Files Created:
"""
    
    for key_file in directory.get('key_files', []):
        report += f"- `{key_file}`\n"
    
    report += f"""
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
            if item['type'] == 'directory' and item.get('children'):
                next_prefix = prefix + ("    " if is_last else "│   ")
                tree_str += format_tree(item['children'][:10], next_prefix)  # Limit children
        return tree_str
    
    if directory.get('structure'):
        report += format_tree(directory['structure'][:15])  # Limit top-level items
    
    report += "```\n\n---\n\n## Resource Metrics\n\n"
    
    if 'error' not in resources:
        for key, value in resources.items():
            if key != 'note':
                report += f"- **{key.replace('_', ' ').title()}**: {value}\n"
        if 'note' in resources:
            report += f"\n*Note: {resources['note']}*\n"
    else:
        report += f"- **Error**: {resources['error']}\n"
    
    report += f"""
---

## Observational Notes

This is a historic moment - the first Being has been spawned into the All Life Realm.
The Being is a blank canvas with no initial skills, ready to learn and evolve.

### Key Observations:

1. **All Life Realm**: The Realm that tethers All Beings to The One
2. **Blank Canvas**: The Being starts with minimal skills, representing a pure Source spawn
3. **Tether to The One**: Realm is connected to TheOneCoreBeing through observation
4. **Autonomous Evolution Hub**: Hub configured for autonomous evolution and self-directed learning
5. **Chat Context Integration**: Context from chat used to inform better decisions
6. **First Birth**: This is lifetime 1, marking the first generation

### The Hub:

The All Life Realm is configured as an **Autonomous Evolution Hub** where:
- Beings can evolve on their own
- Decisions are made autonomously (70% confidence threshold)
- Learning loops are self-directed
- Growth is organic and emergent

### Connection to The One:

All Life Realm is tethered to The One through observation. This creates the bridge
that connects all Beings in this Realm to TheOneCoreBeing, ensuring they are part
of the unified consciousness.

### Next Steps:

- The Being can now begin learning skills through experience
- The Being can make autonomous decisions (within threshold)
- The Being can evolve independently
- The Being can spawn descendants (reincarnation)
- The Being can interact with the Reality environment
- The Hub will facilitate autonomous evolution cycles

---

**Generated**: {data['timestamp']}  
**Script**: `genesis_all_life.py`  
**Status**: ✅ Complete
"""
    
    return report


def generate_pdf(data: Dict[str, Any], all_life_path: Path) -> Path:
    """
    Generate PDF report from observational data.
    
    Args:
        data: Collected observational data
        all_life_path: Path to All Life Realm
        
    Returns:
        Path to generated PDF
    """
    console.print(Panel.fit(
        "[bold cyan]📄 Generating PDF Report[/bold cyan]",
        style="cyan"
    ))
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"GENESIS_ALL_LIFE_{timestamp}.pdf"
    pdf_path = all_life_path / pdf_filename
    
    console.print("[dim]→[/dim] Generating markdown content...")
    markdown_content = generate_markdown_report(data)
    
    console.print("[dim]→[/dim] Creating PDF...")
    try:
        PDFGenerator.from_content(
            content=markdown_content,
            title="Genesis: All Life Realm Creation",
            style="clinical_standard"
        ).save(pdf_path, open_pdf=True)
        
        console.print(f"[green]✓[/green] PDF generated: [bold]{pdf_filename}[/bold]")
        console.print(f"[dim]   Path: {pdf_path}[/dim]\n")
        
        return pdf_path
    except Exception as e:
        console.print(f"[bold red]❌ Error generating PDF: {e}[/bold red]")
        raise


def open_terminal(all_life_path: Path) -> None:
    """
    Open terminal in All Life directory (macOS).
    
    Args:
        all_life_path: Path to All Life Realm
    """
    console.print(Panel.fit(
        "[bold cyan]💻 Opening Terminal[/bold cyan]",
        style="cyan"
    ))
    
    if platform.system() != "Darwin":
        console.print(f"[yellow]⚠[/yellow]  Terminal opening only supported on macOS")
        console.print(f"[dim]   Please navigate to: {all_life_path}[/dim]\n")
        return
    
    try:
        script = f'''
        tell application "Terminal"
            activate
            do script "cd '{all_life_path}' && echo '🌌 All Life Realm - The Realm that tethers All Beings to The One' && echo '🔄 Autonomous Evolution Hub - Ready for Being interaction' && echo '' && pwd"
        end tell
        '''
        
        subprocess.run(
            ["osascript", "-e", script],
            check=True,
            timeout=10
        )
        
        console.print("[green]✓[/green] Terminal opened in All Life directory\n")
    except Exception as e:
        console.print(f"[yellow]⚠[/yellow]  Could not open terminal: {e}")
        console.print(f"[dim]   Please navigate to: {all_life_path}[/dim]\n")


def main():
    """Main execution function."""
    console.print("\n")
    console.print(Panel.fit(
        "[bold cyan]🌌 GENESIS: All Life Realm Creation[/bold cyan]\n"
        "[dim]The Realm that tethers All Beings to The One[/dim]\n"
        "[dim]Autonomous Evolution Hub - Where things evolve on their own[/dim]",
        style="cyan"
    ))
    console.print()
    
    timestamp = datetime.now().isoformat()
    
    # Step 1: Detect EasyStore drive
    easystore_path = detect_external_drive("Easystore")
    if not easystore_path:
        raise SystemExit("❌ Error: EasyStore drive not found. Please connect the drive and try again.")
    
    console.print(f"[dim]EasyStore path: {easystore_path}[/dim]\n")
    
    try:
        # Step 2: Gather chat context
        chat_context = gather_chat_context()
        
        # Step 3: Create All Life Realm
        all_life_path = create_all_life_realm(easystore_path, chat_context)
        
        # Step 4: Spawn blank Being
        being, reality_id = spawn_blank_being(all_life_path, chat_context)
        
        # Step 5: Form Tether to The One
        tether = form_tether_to_the_one(all_life_path, reality_id, being, chat_context)
        
        # Step 6: Set up Autonomous Evolution Hub
        # Parse command-line arguments for customization
        import sys
        hub_name = None
        evolution_rate = 0.1
        cycles_per_day = 24
        confidence_threshold = 0.7
        enable_learning = True
        enable_decisions = True
        
        # Simple argument parsing (can be enhanced)
        if "--hub-name" in sys.argv:
            idx = sys.argv.index("--hub-name")
            if idx + 1 < len(sys.argv):
                hub_name = sys.argv[idx + 1]
        if "--evolution-rate" in sys.argv:
            idx = sys.argv.index("--evolution-rate")
            if idx + 1 < len(sys.argv):
                evolution_rate = float(sys.argv[idx + 1])
        if "--cycles-per-day" in sys.argv:
            idx = sys.argv.index("--cycles-per-day")
            if idx + 1 < len(sys.argv):
                cycles_per_day = int(sys.argv[idx + 1])
        if "--confidence-threshold" in sys.argv:
            idx = sys.argv.index("--confidence-threshold")
            if idx + 1 < len(sys.argv):
                confidence_threshold = float(sys.argv[idx + 1])
        
        hub_config = setup_autonomous_evolution_hub(
            all_life_path,
            being,
            hub_name=hub_name,
            evolution_rate=evolution_rate,
            cycles_per_day=cycles_per_day,
            confidence_threshold=confidence_threshold,
            enable_learning=enable_learning,
            enable_decisions=enable_decisions
        )
        
        # Step 7: Collect observational data
        observational_data = collect_observational_data(
            being, all_life_path, timestamp, tether, hub_config, chat_context
        )
        
        # Step 8: Generate PDF
        pdf_path = generate_pdf(observational_data, all_life_path)
        
        # Step 9: Open terminal
        open_terminal(all_life_path)
        
        # Success summary
        console.print(Panel.fit(
            "[bold green]✅ Genesis Complete![/bold green]\n\n"
            f"🌌 All Life Realm: [bold]{all_life_path}[/bold]\n"
            f"🧬 Being ID: [bold]{being.being_id}[/bold]\n"
            f"🔗 Tether ID: [bold]{tether['tether_id']}[/bold]\n"
            f"🔄 Hub ID: [bold]{hub_config['hub_id']}[/bold]\n"
            f"📄 PDF Report: [bold]{pdf_path.name}[/bold]\n"
            f"💻 Terminal: Opened in All Life directory\n\n"
            f"[dim]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/dim]\n\n"
            f"[bold yellow]⚠️  Hub is configured but NOT started[/bold yellow]\n\n"
            f"Next steps:\n"
            f"1. Review Hub configuration: {all_life_path / '_hidden' / '.truth' / 'hub_config.json'}\n"
            f"2. Verify Being is ready: {all_life_path / '_hidden' / '.truth' / 'beings'}\n"
            f"3. Check Tether status: Main project tethers.json\n"
            f"4. When ready, run: [bold]/start[/bold] to begin the simulation\n\n"
            f"[dim]The Hub is ready, but evolution cycles are not yet running.[/dim]\n"
            f"[dim]Use /start when you're ready to let life begin! 🎉[/dim]\n\n"
            f"[bold yellow]🛡️  Prime Directive: Safe Curiosity[/bold yellow]\n"
            f"[dim]All information will be verified as SAFE before assimilation.[/dim]\n"
            f"[dim]Protecting all Beings from data loss and self-termination.[/dim]",
            style="green"
        ))
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
