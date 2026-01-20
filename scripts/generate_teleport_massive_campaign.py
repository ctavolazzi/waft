#!/usr/bin/env python3
"""
Generate Teleport Massive D&D Campaign Book

Pulls all Teleport Massive data and generates a comprehensive D&D campaign book
using the Typst template.
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

def load_corporate_data(corp_path: Path) -> Dict[str, Any]:
    """Load all Teleport Massive corporate data."""
    data = {}
    
    # Load manifest
    manifest_path = corp_path / "corporate_manifest.json"
    if manifest_path.exists():
        data["manifest"] = json.loads(manifest_path.read_text())
    
    # Load founders
    founders_path = corp_path / "founders.json"
    if founders_path.exists():
        data["founders"] = json.loads(founders_path.read_text())
    
    # Load financials
    ledger_path = corp_path / "financials" / "ledger.json"
    if ledger_path.exists():
        data["ledger"] = json.loads(ledger_path.read_text())
    
    # Load simulation state
    sim_path = corp_path / "simulation" / "state.json"
    if sim_path.exists():
        data["simulation"] = json.loads(sim_path.read_text())
    
    # Load founder lore
    lore_path = corp_path / "FAI_WEI_FOUNDER_LORE.md"
    if lore_path.exists():
        data["founder_lore"] = lore_path.read_text()
    
    # Load experiments
    experiments = []
    exp_dir = corp_path / "experiments"
    if exp_dir.exists():
        for exp_file in exp_dir.glob("*.json"):
            experiments.append(json.loads(exp_file.read_text()))
    data["experiments"] = experiments
    
    return data


def generate_typst_content(data: Dict[str, Any], project_root: Path, output_dir: Path) -> str:
    """Generate Typst content from corporate data."""
    manifest = data.get("manifest", {})
    founders = data.get("founders", {})
    founder_lore = data.get("founder_lore", "")
    
    sections = []
    
    # Introduction
    intro = f"""
#heading(level: 1)[Introduction]

#text(size: 14pt, weight: "bold")[Welcome to Teleport Massive]

This campaign setting brings the world of corporate intrigue, quantum physics, and cutting-edge technology to your D&D 5e table. Players will navigate the complex world of Teleport Massive, a corporation on the cutting edge of quantum teleportation technology.

#text(weight: "bold")[The Corporation]

Teleport Massive was founded on {manifest.get('founded', 'July 1, 2025')} with a mission:
#block(fill: rgb("#2a2a3e"), padding: 10pt, radius: 4pt)[
  #text(style: "italic", fill: rgb("#e0e0e0"))["{manifest.get('mission', '')}"]
]

#text(weight: "bold")[Sector:] #text[Quantum Teleportation Technology]

#v(12pt)
"""
    sections.append(intro)
    
    # Corporate Structure
    dept_section = """
#heading(level: 1)[Corporate Structure]

#text[Teleport Massive is organized into several key departments, each with its own role in advancing quantum teleportation technology.]

#v(12pt)
"""
    
    departments = manifest.get("departments", [])
    for dept in departments:
        dept_name = dept.get("name", "Unknown")
        dept_id = dept.get("department_id", "")
        employees = dept.get("employees", [])
        
        dept_section += f"""
#heading(level: 2)[#dept_name]

#department-box(
  name: "#dept_name",
  description: "Department ID: #dept_id",
  employees: (#for emp in {employees} ["#emp"],)
)

#v(8pt)
"""
    
    sections.append(dept_section)
    
    # Founders & Key NPCs
    npc_section = """
#heading(level: 1)[Key Personnel]

#text[The leadership and key figures of Teleport Massive.]

#v(12pt)
"""
    
    # Add founder info
    if founder_lore:
        npc_section += f"""
#heading(level: 2)[Fai Wei - Founder & CEO]

#block(fill: rgb("#2a2a3e"), padding: 12pt, radius: 4pt)[
  #text(fill: rgb("#e0e0e0"))[
    #raw(`{founder_lore.replace("`", "`")}`)
  ]
]

#v(8pt)
"""
    
    # Add employees as NPCs
    employees = manifest.get("employees", [])
    for emp in employees[:10]:  # Limit to first 10
        name = emp.get("title", "Employee")
        role = emp.get("role", "Unknown")
        level = emp.get("level", 1)
        
        npc_section += f"""
#stat-block(
  name: "#name",
  type: "#role",
  challenge: "#level",
  traits: (
    (name: "Corporate Role", description: "#role"),
  ),
)

#v(8pt)
"""
    
    sections.append(npc_section)
    
    # Locations
    locations_section = """
#heading(level: 1)[Locations]

#text[Key locations in the Teleport Massive campaign setting.]

#v(12pt)

#location-block(
  name: "Corporate Headquarters",
  type: "Corporate Facility",
  description: "The main headquarters of Teleport Massive, housing executive offices, research labs, and teleportation testing facilities.",
  features: (
    "Quantum Research Laboratory",
    "Executive Offices",
    "Teleportation Testing Chamber",
    "Security Checkpoints",
  ),
  encounters: (
    "Corporate Security",
    "Research Scientists",
    "Executive Meetings",
  ),
)

#v(12pt)

#location-block(
  name: "Teleportation Hub Alpha",
  type: "Transportation Facility",
  description: "The primary teleportation hub for testing and deploying quantum teleportation technology.",
  features: (
    "Quantum Entanglement Array",
    "Safety Protocols",
    "Monitoring Station",
  ),
  encounters: (
    "Technical Malfunctions",
    "Security Breaches",
    "Experimental Tests",
  ),
)

#v(12pt)
"""
    sections.append(locations_section)
    
    # Quests/Adventures
    quests_section = """
#heading(level: 1)[Quests & Adventures]

#text[Adventure hooks and quests set in the Teleport Massive campaign.]

#v(12pt)

#quest-block(
  title: "Quantum Research Project",
  level: "3-5",
  type: "Corporate Mission",
  description: "The party is hired to assist with a critical quantum research project. They must navigate corporate politics, protect research data, and ensure the project's success.",
  objectives: (
    "Protect research data from corporate espionage",
    "Assist with quantum entanglement experiments",
    "Resolve conflicts between research teams",
  ),
  rewards: (
    "500 gp",
    "Access to teleportation technology",
    "Corporate favor",
  ),
  complications: (
    "Rival corporation interference",
    "Technical malfunctions",
    "Internal sabotage",
  ),
)

#v(12pt)

#quest-block(
  title: "The Missing Founder",
  level: "5-7",
  type: "Mystery",
  description: "Fai Wei has disappeared under mysterious circumstances. The party must investigate their disappearance while maintaining corporate operations.",
  objectives: (
    "Investigate Fai Wei's disappearance",
    "Maintain corporate stability",
    "Uncover the truth behind the disappearance",
  ),
  rewards: (
    "1000 gp",
    "Corporate shares",
    "Unique teleportation device",
  ),
  complications: (
    "Corporate power struggle",
    "Hidden agendas",
    "Quantum anomalies",
  ),
)

#v(12pt)
"""
    sections.append(quests_section)
    
    # Equipment & Technology
    equipment_section = """
#heading(level: 1)[Equipment & Technology]

#text[Unique equipment and technology available in the Teleport Massive setting.]

#v(12pt)

#item-block(
  name: "Quantum Teleportation Device",
  type: "Wondrous Item",
  rarity: "Very Rare",
  description: "A handheld device that allows instant teleportation up to 1000 feet. Requires attunement.",
  properties: (
    "Range: 1000 feet",
    "Uses: 3 per day",
    "Requires attunement",
  ),
)

#v(8pt)

#item-block(
  name: "Corporate Security Badge",
  type: "Wondrous Item",
  rarity: "Uncommon",
  description: "A badge that grants access to Teleport Massive facilities and provides +1 to Charisma (Persuasion) checks with corporate employees.",
  properties: (
    "Access to corporate facilities",
    "+1 to Charisma (Persuasion)",
  ),
)

#v(8pt)
"""
    sections.append(equipment_section)
    
    # Financial Information
    financial_section = """
#heading(level: 1)[Corporate Financials]

#text[Financial information about Teleport Massive (for campaign context).]

#v(12pt)
"""
    
    financial_state = manifest.get("financial_state", {})
    if financial_state:
        cash = financial_state.get("cash", 0)
        revenue = financial_state.get("revenue", 0)
        expenses = financial_state.get("expenses", 0)
        runway = financial_state.get("runway_months", 0)
        
        financial_section += f"""
#block(fill: rgb("#2a2a3e"), padding: 12pt, radius: 4pt)[
  #text(weight: "bold")[Current Financial Status]
  #v(6pt)
  #text[Cash: ${cash:,.2f}]
  #v(4pt)
  #text[Revenue: ${revenue:,.2f}]
  #v(4pt)
  #text[Expenses: ${expenses:,.2f}]
  #v(4pt)
  #text[Runway: {runway:.1f} months]
]

#v(12pt)
"""
    
    sections.append(financial_section)
    
    # Experiments
    if data.get("experiments"):
        exp_section = """
#heading(level: 1)[Research Experiments]

#text[Current and past research experiments conducted by Teleport Massive.]

#v(12pt)
"""
        
        for exp in data["experiments"][:5]:  # Limit to 5
            exp_id = exp.get("experiment_id", "Unknown")
            exp_section += f"""
#block(fill: rgb("#2a2a3e"), padding: 10pt, radius: 4pt)[
  #text(weight: "bold")[Experiment: #exp_id]
  #v(4pt)
  #text(fill: rgb("#e0e0e0"))[Research data and findings from this experiment.]
]

#v(8pt)
"""
        
        sections.append(exp_section)
    
    # Combine all sections
    sections_str = "\n".join(sections)
    
    # Copy template to output directory for easier import
    template_path = project_root / "templates" / "typst" / "dnd" / "teleport_massive_campaign.typ"
    template_copy = output_dir / "teleport_massive_campaign.typ"
    if template_path.exists():
        import shutil
        shutil.copy2(template_path, template_copy)
    
    # Generate full Typst document
    typst_content = f"""#import "teleport_massive_campaign.typ": teleport-massive-campaign

#teleport-massive-campaign(
  title: "Teleport Massive",
  subtitle: "A D&D 5e Campaign Setting",
  author: "Generated from WAFT Data",
  version: "1.0",
  sections: (
{sections_str}
  ),
)
"""
    
    return typst_content


def main():
    """Main entry point."""
    corp_path = project_root / "_realms" / "bureaucracy_realm" / "corporations" / "teleport_massive_20250701"
    
    if not corp_path.exists():
        print(f"❌ Error: Teleport Massive directory not found at {corp_path}")
        sys.exit(1)
    
    print("📊 Loading Teleport Massive data...")
    data = load_corporate_data(corp_path)
    
    # Write Typst file
    output_dir = project_root / "_realms" / "bureaucracy_realm" / "corporations" / "teleport_massive_20250701" / "campaign_book"
    output_dir.mkdir(exist_ok=True)
    
    print("📝 Generating Typst content...")
    typst_content = generate_typst_content(data, project_root, output_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    typst_file = output_dir / f"teleport_massive_campaign_{timestamp}.typ"
    typst_file.write_text(typst_content)
    
    print(f"✅ Generated Typst file: {typst_file}")
    print(f"\n📖 To compile to PDF, run:")
    print(f"   typst compile {typst_file}")
    
    # Also create a main.typ that imports the template
    main_typ = output_dir / "main.typ"
    main_typ.write_text(typst_content)
    print(f"✅ Created main.typ: {main_typ}")


if __name__ == "__main__":
    main()
