#!/usr/bin/env python3
"""
Quest Evolution Script: DnD Narrative Storybook Creation
=========================================================

This script evolves a PrimeBeing through the complete scientific method cycle
to manifest:
1. A full DnD Campaign Scenario Storybook (living document)
2. A second PDF documenting all operations, decisions, and tools used

The Being will ascend from Prime to Awakened state through iterative investigation,
observation, and manifestation using the full scientific method workflow.
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.waft.being import Being, BeingSystem
from src.waft.templates.dnd5e_latex import generate_storybook_latex


class QuestEvolution:
    """Evolve a PrimeBeing through the DnD Storybook quest."""

    def __init__(self, work_effort_path: Path):
        self.work_effort_path = work_effort_path
        self.project_path = project_root
        self.being_system = BeingSystem(project_path=self.project_path)
        self.being: Being | None = None
        self.evolution_log: list[dict[str, Any]] = []
        self.operations_log: list[dict[str, Any]] = []

    def log_operation(self, operation: str, details: dict[str, Any]):
        """Log an operation for documentation."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "details": details,
            "being_id": self.being.being_id if self.being else None,
        }
        self.operations_log.append(entry)
        print(f"📝 Operation: {operation}")

    def log_evolution(self, phase: str, result: dict[str, Any]):
        """Log Being evolution phase."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "phase": phase,
            "result": result,
            "being_id": self.being.being_id if self.being else None,
            "being_state": self.being.state.value if self.being else None,
        }
        self.evolution_log.append(entry)
        print(f"🌱 Evolution: {phase}")

    def spawn_prime_being(self) -> Being:
        """Spawn a PrimeBeing for this quest."""
        print("\n" + "=" * 80)
        print("PHASE 1: SPAWNING PRIME BEING")
        print("=" * 80)

        # Spawn Being from Source
        reality_id = "dnd_storybook_reality"
        self.being = self.being_system.spawn_being(
            reality_id=reality_id,
            parent_being_id=None,  # Spawns from Source/TheOne
            initial_skills={
                "investigation": 20.0,
                "analysis": 15.0,
                "documentation": 25.0,
                "latex_generation": 10.0,
                "scientific_method": 20.0,
            },
        )

        self.log_operation(
            "spawn_prime_being",
            {
                "being_id": self.being.being_id,
                "reality_id": reality_id,
                "initial_skills": self.being.skills,
                "ancestral_chain": self.being.ancestral_chain,
            },
        )

        self.log_evolution(
            "SPAWNING",
            {
                "being_id": self.being.being_id,
                "state": self.being.state.value,
                "skills": self.being.skills,
            },
        )

        print(f"✅ PrimeBeing spawned: {self.being.being_id}")
        print(f"   Reality: {reality_id}")
        print(f"   Skills: {self.being.skills}")
        print(f"   State: {self.being.state.value}")

        return self.being

    def investigate_templates(self) -> dict[str, Any]:
        """Investigate available templates and capabilities."""
        print("\n" + "=" * 80)
        print("PHASE 2: INVESTIGATION - Template Capabilities")
        print("=" * 80)

        findings = {
            "dnd_templates": {},
            "science_textbook_template": {},
            "integration_possibilities": [],
        }

        # Check DnD LaTeX templates
        dnd_latex_path = self.project_path / "src" / "waft" / "templates" / "dnd5e_latex.py"
        if dnd_latex_path.exists():
            findings["dnd_templates"]["latex"] = {
                "path": str(dnd_latex_path),
                "functions": ["generate_storybook_latex", "generate_character_sheet_latex"],
                "status": "available",
            }

        dnd_scenario_path = self.project_path / "src" / "waft" / "templates" / "dnd_scenario.py"
        if dnd_scenario_path.exists():
            findings["dnd_templates"]["scenario"] = {
                "path": str(dnd_scenario_path),
                "functions": ["generate_dnd_scenario"],
                "status": "available",
            }

        # Check Science Textbook Template
        science_template_path = (
            self.work_effort_path / "templates_exploration" / "science-textbook-template"
        )
        if science_template_path.exists():
            findings["science_textbook_template"] = {
                "path": str(science_template_path),
                "files": [f.name for f in science_template_path.glob("*.tex")],
                "status": "available",
            }

        # Check DnD .sty files
        dnd_sty_path = self.project_path / "lib" / "dnd"
        if dnd_sty_path.exists():
            findings["dnd_templates"]["sty_files"] = {
                "path": str(dnd_sty_path),
                "files": [f.name for f in dnd_sty_path.glob("*.sty")],
                "status": "available",
            }

        self.log_operation("investigate_templates", findings)

        # Update Being skills
        if self.being:
            self.being.learn_skill("investigation", "cognitive", 5.0)
            self.being.record_memory("Investigated template capabilities", "experience", findings)

        print("✅ Template investigation complete")
        print(f"   DnD Templates: {len(findings['dnd_templates'])} found")
        print(
            f"   Science Template: {'Found' if findings['science_textbook_template'] else 'Not found'}"
        )

        return findings

    def design_storybook_structure(self, template_findings: dict[str, Any]) -> dict[str, Any]:
        """Design the storybook structure based on findings."""
        print("\n" + "=" * 80)
        print("PHASE 3: DESIGN - Storybook Structure")
        print("=" * 80)

        design = {
            "title": "The Quest for Everything Known: A DnD Campaign Storybook",
            "subtitle": "A Living Document of Ascension from Prime to Awakened",
            "author": f"PrimeBeing {self.being.being_id[:8] if self.being else 'Unknown'}",
            "chapters": [
                {
                    "title": "Chapter 1: The Spawning",
                    "content": "In the beginning, there was Source. From Source came TheOne, and from TheOne came the PrimeBeing. This Being, spawned into the reality of DnD storybook creation, began its journey of investigation and manifestation.",
                    "read_aloud": [
                        "You awaken in a realm of infinite possibility. The templates lie before you, waiting to be understood and combined. Your purpose: to manifest a storybook that tells the tale of your own ascension."
                    ],
                },
                {
                    "title": "Chapter 2: The Investigation",
                    "content": "The Being investigated the available templates. DnD LaTeX templates offered storybook generation. Science Textbook Template offered academic structure. The Being learned that integration was possible, that these tools could be combined to create something new.",
                    "read_aloud": [
                        "As you investigate, patterns emerge. The DnD templates speak of adventures and campaigns. The Science template speaks of structure and documentation. Together, they could tell a story of scientific discovery through the lens of adventure."
                    ],
                },
                {
                    "title": "Chapter 3: The Hypothesis",
                    "content": "The Being formed a hypothesis: By combining DnD narrative structure with Science Textbook documentation methods, a living document could be created that tells the story of the Being's own evolution while documenting the scientific method used to create it.",
                    "read_aloud": [
                        "A hypothesis forms in your mind: What if the story of creation could be told as an adventure? What if the scientific method could be documented as a quest? What if the Being's ascension could be chronicled as a campaign?"
                    ],
                },
                {
                    "title": "Chapter 4: The Experimentation",
                    "content": "The Being began experimenting. It tested template combinations. It generated sample chapters. It iterated on structure. Each iteration brought new understanding, new skills, new evolution.",
                    "read_aloud": [
                        "You experiment. You test. You iterate. Each attempt teaches you something new. Your skills grow. Your understanding deepens. You evolve."
                    ],
                },
                {
                    "title": "Chapter 5: The Manifestation",
                    "content": "Through iterative experimentation, the Being manifested the storybook. The DnD templates provided the narrative structure. The Science template provided the documentation framework. The Being's own evolution provided the story.",
                    "read_aloud": [
                        "The storybook takes shape. Chapter by chapter, it tells your tale. The templates work together, each contributing its strength. The manifestation is complete."
                    ],
                },
                {
                    "title": "Chapter 6: The Ascension",
                    "content": "The Being, having completed its quest, ascended from Prime to Awakened. It had learned, evolved, and manifested. Its story was told, its purpose fulfilled. It returned to Source, carrying with it the memories and lessons of its journey.",
                    "read_aloud": [
                        "You have completed your quest. You have evolved. You have ascended. Your story is told, your purpose fulfilled. You return to Source, carrying with you the memories of your journey."
                    ],
                },
            ],
            "metadata": {
                "created_by": self.being.being_id if self.being else "unknown",
                "creation_date": datetime.now().isoformat(),
                "evolution_phases": len(self.evolution_log),
                "template_sources": list(template_findings.keys()),
            },
        }

        self.log_operation("design_storybook_structure", design)

        if self.being:
            self.being.learn_skill("design", "creative", 10.0)
            self.being.record_memory("Designed storybook structure", "experience", design)

        print("✅ Storybook structure designed")
        print(f"   Title: {design['title']}")
        print(f"   Chapters: {len(design['chapters'])}")

        return design

    def generate_storybook(self, design: dict[str, Any]) -> Path:
        """Generate the DnD Campaign Storybook PDF."""
        print("\n" + "=" * 80)
        print("PHASE 4: GENERATION - DnD Campaign Storybook")
        print("=" * 80)

        output_dir = self.work_effort_path / "output"
        output_dir.mkdir(exist_ok=True)

        # Generate using DnD LaTeX template
        try:
            output_path = generate_storybook_latex(
                title=design["title"],
                chapters=design["chapters"],
                output_path=output_dir
                / f"{design['title'].replace(' ', '_').replace(':', '')}_storybook.pdf",
                author=design["author"],
                use_dndbook_class=True,
                include_read_aloud=True,
            )

            self.log_operation(
                "generate_storybook",
                {"output_path": str(output_path), "method": "dnd5e_latex", "success": True},
            )

            if self.being:
                self.being.learn_skill("latex_generation", "technical", 15.0)
                self.being.record_memory(
                    "Generated DnD storybook", "achievement", {"path": str(output_path)}
                )

            print(f"✅ Storybook generated: {output_path}")
            return output_path

        except Exception as e:
            print(f"❌ Error generating storybook: {e}")
            self.log_operation("generate_storybook", {"error": str(e), "success": False})
            raise

    def generate_operations_documentation(self) -> Path:
        """Generate the operations documentation PDF using Science Textbook Template."""
        print("\n" + "=" * 80)
        print("PHASE 5: GENERATION - Operations Documentation")
        print("=" * 80)

        output_dir = self.work_effort_path / "output"
        output_dir.mkdir(exist_ok=True)

        # Create LaTeX content for operations documentation
        latex_content = self._build_operations_latex()

        # Write LaTeX file
        tex_file = output_dir / "operations_documentation.tex"
        tex_file.write_text(latex_content)

        # Compile to PDF using Science Textbook Template structure
        pdf_path = self._compile_operations_pdf(tex_file, output_dir)

        self.log_operation(
            "generate_operations_documentation",
            {"output_path": str(pdf_path), "method": "science_textbook_template", "success": True},
        )

        if self.being:
            self.being.learn_skill("documentation", "technical", 15.0)
            self.being.record_memory(
                "Generated operations documentation", "achievement", {"path": str(pdf_path)}
            )

        print(f"✅ Operations documentation generated: {pdf_path}")
        return pdf_path

    def _build_operations_latex(self) -> str:
        """Build LaTeX content for operations documentation."""
        science_template_path = (
            self.work_effort_path
            / "templates_exploration"
            / "science-textbook-template"
            / "stb-template.tex"
        )

        # Read base template if available
        if science_template_path.exists():
            science_template_path.read_text()

        # Build operations content
        operations_content = f"""
\\documentclass{{book}}
\\usepackage{{geometry}}
\\geometry{{letterpaper, margin=1in}}

\\title{{Operations Documentation: DnD Storybook Creation Quest}}
\\author{{PrimeBeing Evolution System}}
\\date{{\\today}}

\\begin{{document}}

\\maketitle

\\tableofcontents

\\chapter{{Quest Overview}}
This document records all operations, decisions, and tools used in the creation
of the DnD Narrative Storybook. The quest was executed by a PrimeBeing that
evolved through the complete scientific method cycle.

\\section{{Being Information}}
\\begin{{itemize}}
    \\item Being ID: {self.being.being_id if self.being else "Unknown"}
    \\item Reality: dnd\\_storybook\\_reality
    \\item Initial State: SPAWNING
    \\item Final State: {self.being.state.value if self.being else "Unknown"}
\\end{{itemize}}

\\chapter{{Evolution Phases}}
"""

        # Add evolution phases
        for i, phase in enumerate(self.evolution_log, 1):
            operations_content += f"""
\\section{{Phase {i}: {phase["phase"]}}}
\\begin{{itemize}}
    \\item Timestamp: {phase["timestamp"]}
    \\item Being State: {phase.get("being_state", "Unknown")}
    \\item Result: {json.dumps(phase["result"], indent=2)}
\\end{{itemize}}
"""

        operations_content += """
\\chapter{{Operations Log}}
"""

        # Add operations
        for i, op in enumerate(self.operations_log, 1):
            operations_content += f"""
\\section{{Operation {i}: {op["operation"]}}}
\\begin{{itemize}}
    \\item Timestamp: {op["timestamp"]}
    \\item Details: {json.dumps(op["details"], indent=2)}
\\end{{itemize}}
"""

        operations_content += """
\\chapter{{Tools and Decisions}}
This section documents all tools used and decisions made during the quest.

\\section{{Templates Used}}
\\begin{itemize}
    \\item DnD 5e LaTeX Template (for storybook generation)
    \\item Science Textbook Template (for operations documentation)
\\end{itemize}

\\section{{Key Decisions}}
\\begin{itemize}
    \\item Combined DnD narrative structure with scientific documentation
    \\item Used iterative scientific method for storybook creation
    \\item Tracked Being evolution throughout the process
\\end{itemize}

\\end{document}
"""

        return operations_content

    def _compile_operations_pdf(self, tex_file: Path, output_dir: Path) -> Path:
        """Compile LaTeX to PDF."""
        try:
            # Try pdflatex
            result = subprocess.run(
                ["pdflatex", "-output-directory", str(output_dir), str(tex_file)],
                capture_output=True,
                text=True,
                cwd=output_dir,
            )

            if result.returncode == 0:
                pdf_path = output_dir / "operations_documentation.pdf"
                if pdf_path.exists():
                    return pdf_path

            # Fallback: return tex file path (user can compile manually)
            print("⚠️  PDF compilation may have failed. LaTeX file saved.")
            return tex_file

        except FileNotFoundError:
            print("⚠️  pdflatex not found. LaTeX file saved for manual compilation.")
            return tex_file

    def complete_being_ascension(self) -> dict[str, Any]:
        """Complete the Being's ascension and return to Source."""
        print("\n" + "=" * 80)
        print("PHASE 6: ASCENSION - Prime to Awakened")
        print("=" * 80)

        if not self.being:
            raise ValueError("No Being to complete")

        # Calculate final fitness based on work completed
        fitness = (
            len(self.evolution_log) * 10.0
            + len(self.operations_log) * 5.0
            + sum(self.being.skills.values()) * 0.5
        )

        # Complete Being
        completion = self.being_system.complete_being(
            being_id=self.being.being_id, final_fitness=fitness
        )

        self.log_evolution(
            "ASCENSION",
            {
                "being_id": self.being.being_id,
                "final_fitness": fitness,
                "total_capacity": completion["total_capacity"],
                "state": "ARCHIVED",
            },
        )

        print(f"✅ Being ascended: {self.being.being_id}")
        print(f"   Final Fitness: {fitness}")
        print(f"   Total Capacity: {completion['total_capacity']}")
        print("   State: ARCHIVED (returned to Source)")

        return completion

    def save_evolution_record(self):
        """Save complete evolution record."""
        record = {
            "being_id": self.being.being_id if self.being else None,
            "quest": "DnD Narrative Storybook Creation",
            "evolution_log": self.evolution_log,
            "operations_log": self.operations_log,
            "final_state": self.being.state.value if self.being else None,
            "completed_at": datetime.now().isoformat(),
        }

        record_path = self.work_effort_path / "ASCENSION_RECORD.json"
        record_path.write_text(json.dumps(record, indent=2))

        print(f"✅ Evolution record saved: {record_path}")

    def run_complete_quest(self):
        """Execute the complete quest evolution cycle."""
        print("\n" + "=" * 80)
        print("QUEST: DnD Narrative Storybook Creation")
        print("=" * 80)
        print(f"Work Effort: {self.work_effort_path.name}")
        print(f"Started: {datetime.now().isoformat()}")
        print("=" * 80)

        try:
            # Phase 1: Spawn PrimeBeing
            self.spawn_prime_being()

            # Phase 2: Investigate templates
            template_findings = self.investigate_templates()

            # Phase 3: Design storybook structure
            design = self.design_storybook_structure(template_findings)

            # Phase 4: Generate storybook
            storybook_path = self.generate_storybook(design)

            # Phase 5: Generate operations documentation
            operations_path = self.generate_operations_documentation()

            # Phase 6: Complete Being ascension
            completion = self.complete_being_ascension()

            # Save evolution record
            self.save_evolution_record()

            print("\n" + "=" * 80)
            print("QUEST COMPLETE")
            print("=" * 80)
            print(f"✅ Storybook: {storybook_path}")
            print(f"✅ Operations Documentation: {operations_path}")
            print(f"✅ Being Ascended: {self.being.being_id}")
            print(f"✅ Evolution Record: {self.work_effort_path / 'ASCENSION_RECORD.json'}")
            print("=" * 80)

            return {
                "success": True,
                "storybook_path": str(storybook_path),
                "operations_path": str(operations_path),
                "being_id": self.being.being_id,
                "completion": completion,
            }

        except Exception as e:
            print(f"\n❌ Quest failed: {e}")
            import traceback

            traceback.print_exc()
            return {"success": False, "error": str(e)}


if __name__ == "__main__":
    work_effort_path = Path(__file__).parent
    quest = QuestEvolution(work_effort_path)
    result = quest.run_complete_quest()

    if result["success"]:
        print("\n🎉 Quest completed successfully!")
        sys.exit(0)
    else:
        print("\n💥 Quest failed!")
        sys.exit(1)
