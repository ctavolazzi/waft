"""
Teleport Massive Founding Story

The story of how Teleport Massive was founded in 2025 to study quantum
entanglement and scale quantum teleportation from mini to macro.
"""

# Import BeingSystem - need to go up to src/waft level
import sys
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

from ..corporation import Corporation
from ..corporations_system import CorporationsSystem
from ..security import write_secure_file

if str(Path(__file__).parent.parent.parent.parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))
from src.waft.being import BeingSystem

FOUNDING_STORY = """
# Teleport Massive: The Founding Story

## The Vision (2025)

In the summer of 2025, a group of visionary scientists and entrepreneurs came together
with a bold mission: to revolutionize transportation by scaling quantum teleportation
from laboratory experiments to real-world applications.

## The Founders

### Dr. Elena Voss - CEO & Co-Founder
A quantum physicist turned entrepreneur, Elena had spent a decade researching quantum
entanglement at leading research institutions. Frustrated by the slow pace of academic
research, she envisioned a company that could bridge the gap between theoretical physics
and practical applications.

**Background:**
- PhD in Quantum Physics from MIT
- 10+ years research experience in quantum entanglement
- Published 50+ papers on quantum teleportation protocols
- Previous startup experience (sold previous company in 2022)

**Vision:** "We're not just studying quantum mechanics—we're building the future of
transportation. Imagine a world where distance becomes irrelevant."

### Dr. Marcus Chen - CTO & Co-Founder
A brilliant experimental physicist specializing in quantum systems, Marcus had
developed several breakthrough techniques for stabilizing quantum states at larger scales.
His research showed that macro-scale teleportation wasn't just theoretically possible—
it was within reach.

**Background:**
- PhD in Experimental Physics from Stanford
- 8+ years developing quantum systems
- Inventor of the "Chen Stabilization Protocol" for macro-scale quantum states
- Multiple patents in quantum computing

**Vision:** "The physics is sound. The technology is emerging. The question isn't 'if'—
it's 'when.' We're here to make 'when' happen now."

### Sarah Kim - CFO & Co-Founder (Optional)
A financial strategist with deep experience in deep-tech startups, Sarah joined to
handle the business side while Elena and Marcus focused on the science.

**Background:**
- MBA from Wharton
- 12+ years in venture capital and startup finance
- Led fundraising for 3 successful deep-tech companies
- Expertise in quantum computing and biotech investments

**Vision:** "This isn't just a research project—it's a business. We need to build
sustainably while pushing the boundaries of what's possible."

## The Founding (July 1, 2025)

On July 1, 2025, Teleport Massive was officially incorporated with a clear mission:

> "To study quantum entanglement and scale quantum teleportation from mini to macro,
> revolutionizing transportation and making distance irrelevant."

## Initial Funding

The company raised $2,000,000 in seed funding from a group of angel investors who
believed in the founders' vision. The funding would support:
- Research and development (60%)
- Equipment and laboratory setup (25%)
- Salaries and operations (15%)

## Early Research Focus

The initial research agenda focused on three key areas:

1. **Quantum Entanglement Studies**: Understanding and optimizing entanglement
   protocols for larger systems
2. **Stabilization Techniques**: Developing methods to maintain quantum coherence
   at macro scales
3. **Safety Protocols**: Ensuring teleportation is safe for biological matter

## The First Hires (January 2026)

Six months after founding, Teleport Massive made its first major hiring push,
bringing on three Lead Scientists to form the core Research & Development team:

1. **Aziah Calderon** - Lead Scientist (promoted to Head of R&D in February 2026)
2. **Dr. Priya Sharma** - Lead Scientist (quantum protocols specialist)
3. **Dr. James Park** - Lead Scientist (experimental systems engineer)

This team would form the foundation of Teleport Massive's research capabilities,
working alongside the founders to push the boundaries of quantum teleportation.

## The Path Forward

With a strong founding team, initial funding, and a clear research mission, Teleport
Massive was positioned to become a leader in quantum teleportation technology. The
journey from laboratory experiments to real-world applications had begun.
"""


def get_founding_story() -> str:
    """Get the Teleport Massive founding story."""
    return FOUNDING_STORY


def create_teleport_massive(
    project_path: Path | None = None,
    being_system: BeingSystem | None = None,
    create_founders: bool = True,
) -> Corporation:
    """
    Create Teleport Massive corporation with founding story.

    Args:
        project_path: Project root path
        being_system: BeingSystem instance (required if create_founders=True)
        create_founders: Whether to create founder Beings

    Returns:
        Created Teleport Massive Corporation
    """
    from .initial_conditions import get_initial_conditions

    # Get initial conditions
    initial_conditions = get_initial_conditions()

    # Initialize corporations system
    corps_system = CorporationsSystem(project_path=project_path)

    # Create corporation
    corporation = corps_system.create_corporation(
        name="Teleport Massive",
        sector="Quantum Teleportation Technology",
        mission="To study quantum entanglement and scale quantum teleportation from mini to macro, revolutionizing transportation and making distance irrelevant.",
        founded_date=datetime(2025, 7, 1),
        initial_capital=Decimal(str(initial_conditions.initial_capital)),
        corp_id="teleport_massive_20250701",
    )

    # Create founders if requested
    if create_founders and being_system:
        founders = _create_founders(being_system, corporation, project_path)
        # Founders are automatically added to corporation via hire_employee

    # Set up initial departments
    corporation.add_department("Executive")
    corporation.add_department("Research & Development")
    corporation.add_department("Operations")

    # Configure monthly expenses
    from ..simulation.corporation_simulator import CorporationSimulator, TimeUnit

    simulator = CorporationSimulator(
        corporation=corporation, time_unit=TimeUnit.DAILY, start_date=datetime(2025, 7, 1)
    )

    # Add monthly expenses
    simulator.add_monthly_expense(
        description="Laboratory rent",
        amount=Decimal("15000"),
        category="rent",
        vendor="Quantum Labs Inc.",
    )

    simulator.add_monthly_expense(
        description="Quantum research equipment maintenance",
        amount=Decimal("25000"),
        category="equipment",
        vendor="Quantum Systems Corp",
    )

    # Save simulator state
    simulator._save_state()

    return corporation


def _create_founders(
    being_system: BeingSystem, corporation: Corporation, project_path: Path | None
) -> list[dict[str, Any]]:
    """
    Create founder Beings for Teleport Massive.

    Args:
        being_system: BeingSystem instance
        corporation: Corporation to add founders to
        project_path: Project root path

    Returns:
        List of founder information
    """
    founders = []

    # Founder 1: Dr. Elena Voss - CEO
    elena = being_system.spawn_being(
        reality_id=corporation.corp_id,
        initial_skills={
            "quantum_physics": 9.5,
            "leadership": 8.5,
            "entrepreneurship": 8.0,
            "research": 9.0,
        },
    )
    # Set personality and goals after spawning
    elena.personality = {"visionary": 0.9, "determined": 0.85, "innovative": 0.9}
    elena.goals = [
        {"goal": "Scale quantum teleportation to macro scale", "priority": 1.0},
        {"goal": "Build a world-class research team", "priority": 0.9},
    ]
    elena.custom_name = "Dr. Elena Voss"
    being_system._save_being(elena)

    # Add memories for background
    elena.record_memory(
        "Earned PhD in Quantum Physics from MIT, specializing in quantum entanglement",
        memory_type="education",
        metadata={
            "title": "PhD in Quantum Physics",
            "institution": "MIT",
            "year": "2015",
            "type": "education",
        },
    )

    elena.record_memory(
        "Founded and sold previous quantum computing startup in 2022",
        memory_type="work",
        metadata={
            "title": "Previous Startup Founder",
            "context": "Quantum Computing Startup",
            "year": "2022",
            "type": "work",
        },
    )

    corporation.hire_employee(
        being_id=elena.being_id,
        role="CEO",
        department="Executive",
        title="Chief Executive Officer & Co-Founder",
        level=10,
        salary=Decimal("180000"),  # $180k annual
    )

    founders.append(
        {"being_id": elena.being_id, "name": "Dr. Elena Voss", "role": "CEO & Co-Founder"}
    )

    # Founder 2: Dr. Marcus Chen - CTO
    marcus = being_system.spawn_being(
        reality_id=corporation.corp_id,
        initial_skills={
            "experimental_physics": 9.5,
            "quantum_systems": 9.8,
            "research": 9.5,
            "innovation": 9.0,
        },
    )
    # Set personality and goals after spawning
    marcus.personality = {"brilliant": 0.95, "focused": 0.9, "technical": 0.95}
    marcus.goals = [
        {"goal": "Develop macro-scale quantum stabilization techniques", "priority": 1.0},
        {"goal": "Prove quantum teleportation at human scale", "priority": 0.95},
    ]
    marcus.custom_name = "Dr. Marcus Chen"
    being_system._save_being(marcus)

    marcus.record_memory(
        "Earned PhD in Experimental Physics from Stanford, developed Chen Stabilization Protocol",
        memory_type="education",
        metadata={
            "title": "PhD in Experimental Physics",
            "institution": "Stanford",
            "year": "2017",
            "type": "education",
        },
    )

    marcus.record_memory(
        "Invented Chen Stabilization Protocol for macro-scale quantum states, published in Nature",
        memory_type="achievement",
        metadata={
            "title": "Chen Stabilization Protocol",
            "context": "Research Breakthrough",
            "year": "2023",
            "type": "achievement",
        },
    )

    corporation.hire_employee(
        being_id=marcus.being_id,
        role="CTO",
        department="Executive",
        title="Chief Technology Officer & Co-Founder",
        level=10,
        salary=Decimal("180000"),  # $180k annual
    )

    founders.append(
        {"being_id": marcus.being_id, "name": "Dr. Marcus Chen", "role": "CTO & Co-Founder"}
    )

    # Save founder information
    founders_path = (
        Path(project_path)
        / "_realms"
        / "bureaucracy_realm"
        / "corporations"
        / corporation.corp_id
        / "founders.json"
    )
    founders_path.parent.mkdir(parents=True, exist_ok=True)

    # CRITICAL: Use secure file write
    import json

    try:
        write_secure_file(founders_path, json.dumps(founders, indent=2), encoding="utf-8")
    except OSError:
        # If write fails, log but don't fail (founders already in memory)
        pass

    return founders
