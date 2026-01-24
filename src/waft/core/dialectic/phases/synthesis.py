"""
DIALECTIC Phase 3: SYNTHESIS (Problem Description)

Creates briefs, MVP documents, and scientific reports.
This is the "synthesis" in the Hegelian dialectic - the resolution.
"""

import logging
import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import Any
import shutil

logger = logging.getLogger("Dialectic.Synthesis")


class SynthesisPhase:
    """
    Synthesis Phase - PROBLEM DESCRIPTION
    
    Responsibilities:
    1. Create Mission Brief
    2. Generate MVP supporting documents
    3. Produce scientific-quality report
    4. Generate Synthesis Report PDF
    """
    
    def __init__(self, project_path: Path, output_dir: Path):
        self.project_path = Path(project_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def run(self) -> dict[str, Any]:
        """Execute the Synthesis phase."""
        logger.info("Starting SYNTHESIS (Problem Description) Phase...")
        
        # 1. Analyze previous phases (if available)
        analysis = self._analyze_previous_phases()
        logger.info(f"Previous phases analyzed")
        
        # 2. Create Problem Description
        problem_desc = self._create_problem_description(analysis)
        logger.info("Problem description created")
        
        # 3. Generate Recommendations
        recommendations = self._generate_recommendations(analysis)
        logger.info(f"Recommendations generated: {len(recommendations)}")
        
        # 4. Create MVP Document
        mvp_path = self._create_mvp_document(problem_desc, recommendations)
        logger.info(f"MVP document created: {mvp_path}")
        
        # 5. Generate Scientific Report
        report_data = {
            "phase": "synthesis",
            "timestamp": self.timestamp,
            "analysis": analysis,
            "problem_description": problem_desc,
            "recommendations": recommendations,
            "mvp_path": str(mvp_path) if mvp_path else None,
        }
        
        output_path = self._generate_report(report_data)
        
        return {
            "status": "success",
            "phase": "synthesis",
            "output_path": str(output_path),
            "mvp_path": str(mvp_path) if mvp_path else None,
            "summary": {
                "recommendations_count": len(recommendations),
                "problem_areas": len(problem_desc.get("areas", [])),
            }
        }
        
    def _analyze_previous_phases(self) -> dict[str, Any]:
        """Analyze outputs from Assembly and Antithesis phases."""
        analysis = {
            "assembly_complete": False,
            "antithesis_complete": False,
            "findings": [],
        }
        
        # Check for assembly outputs
        assembly_dir = self.output_dir.parent / "assembly"
        if assembly_dir.exists():
            assembly_files = list(assembly_dir.glob("*.pdf")) + list(assembly_dir.glob("*.typ"))
            analysis["assembly_complete"] = len(assembly_files) > 0
            analysis["assembly_files"] = [f.name for f in assembly_files]
            
        # Check for antithesis outputs
        sanity_dir = self.output_dir.parent / "sanity"
        if sanity_dir.exists():
            sanity_files = list(sanity_dir.glob("*.pdf")) + list(sanity_dir.glob("*.typ"))
            analysis["antithesis_complete"] = len(sanity_files) > 0
            analysis["antithesis_files"] = [f.name for f in sanity_files]
            
        return analysis
        
    def _create_problem_description(self, analysis: dict[str, Any]) -> dict[str, Any]:
        """Create a structured problem description."""
        problem_desc = {
            "title": "Project State Analysis",
            "summary": "",
            "areas": [],
            "constraints": [],
            "opportunities": [],
        }
        
        # Analyze based on available data
        if not analysis["assembly_complete"]:
            problem_desc["areas"].append({
                "name": "Context Gathering",
                "status": "incomplete",
                "description": "Assembly phase not complete - full context not available",
            })
        else:
            problem_desc["areas"].append({
                "name": "Context Gathering",
                "status": "complete",
                "description": "Project context successfully gathered",
            })
            
        if not analysis["antithesis_complete"]:
            problem_desc["areas"].append({
                "name": "Assumption Validation",
                "status": "incomplete",
                "description": "Antithesis phase not complete - assumptions not validated",
            })
        else:
            problem_desc["areas"].append({
                "name": "Assumption Validation",
                "status": "complete",
                "description": "Assumptions validated through evidence",
            })
            
        # Add standard constraints
        problem_desc["constraints"] = [
            "Time constraints on analysis depth",
            "Automated analysis has limitations",
            "Human review recommended for critical decisions",
        ]
        
        # Add opportunities
        problem_desc["opportunities"] = [
            "Systematic documentation of project state",
            "Evidence-based decision making",
            "Work effort seeding from SITREP",
        ]
        
        # Generate summary
        complete_count = sum(1 for a in problem_desc["areas"] if a["status"] == "complete")
        total_count = len(problem_desc["areas"])
        problem_desc["summary"] = f"{complete_count}/{total_count} analysis areas complete"
        
        return problem_desc
        
    def _generate_recommendations(self, analysis: dict[str, Any]) -> list[dict[str, Any]]:
        """Generate actionable recommendations."""
        recommendations = []
        
        # Based on phase completion
        if not analysis["assembly_complete"]:
            recommendations.append({
                "priority": "high",
                "action": "Complete Assembly Phase",
                "description": "Run the THESIS (Assembly) phase to gather full project context",
                "command": "waft dialectic --assembly",
            })
            
        if not analysis["antithesis_complete"]:
            recommendations.append({
                "priority": "high",
                "action": "Complete Antithesis Phase",
                "description": "Run the ANTITHESIS (Sanity Check) phase to validate assumptions",
                "command": "waft dialectic --antithesis",
            })
            
        # Standard recommendations
        recommendations.append({
            "priority": "medium",
            "action": "Generate SITREP",
            "description": "Create comprehensive status report from all phases",
            "command": "waft dialectic --sitrep",
        })
        
        recommendations.append({
            "priority": "low",
            "action": "Create Work Effort",
            "description": "Consider seeding a work effort from the SITREP",
            "command": "waft work-efforts create",
        })
        
        return recommendations
        
    def _create_mvp_document(self, problem_desc: dict[str, Any], recommendations: list) -> Path | None:
        """Create an MVP (Minimum Viable Product) supporting document."""
        mvp_file = self.output_dir / f"mvp_document_{self.timestamp}.typ"
        
        content = f'''// DIALECTIC - MVP Document
// Generated: {self.timestamp}

#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)

#align(center)[
  #text(16pt, weight: "bold")[MINIMUM VIABLE PRODUCT DOCUMENT]
  #v(0.3em)
  #text(12pt)[Supporting Analysis for DIALECTIC Synthesis]
]

#line(length: 100%, stroke: 0.5pt)

= Executive Summary

{problem_desc["summary"]}

= Problem Areas

{self._format_areas_as_typst(problem_desc["areas"])}

= Constraints

{self._format_list_as_typst(problem_desc["constraints"])}

= Opportunities

{self._format_list_as_typst(problem_desc["opportunities"])}

= Recommended Actions

{self._format_recommendations_as_typst(recommendations)}

#v(2em)
#line(length: 100%, stroke: 0.5pt)
#align(center)[
  #text(8pt, fill: gray)[
    DIALECTIC Engine // MVP Document \\
    Generated during Synthesis Phase
  ]
]
'''
        
        with open(mvp_file, "w") as f:
            f.write(content)
            
        # Try to compile to PDF
        pdf_path = self._compile_to_pdf(mvp_file)
        
        return pdf_path if pdf_path else mvp_file
        
    def _format_areas_as_typst(self, areas: list) -> str:
        """Format problem areas as Typst content."""
        if not areas:
            return "- No areas identified"
        lines = []
        for area in areas:
            status_icon = "✓" if area["status"] == "complete" else "○"
            color = "green" if area["status"] == "complete" else "orange"
            lines.append(f"== {status_icon} {area['name']}")
            lines.append(f"_{area['description']}_")
            lines.append("")
        return "\n".join(lines)
        
    def _format_list_as_typst(self, items: list) -> str:
        """Format a list as Typst items."""
        if not items:
            return "- None identified"
        return "\n".join(f"- {item}" for item in items)
        
    def _format_recommendations_as_typst(self, recommendations: list) -> str:
        """Format recommendations as Typst content."""
        if not recommendations:
            return "- No recommendations at this time"
        lines = []
        for i, rec in enumerate(recommendations, 1):
            priority_color = "red" if rec["priority"] == "high" else "orange" if rec["priority"] == "medium" else "blue"
            lines.append(f"== {i}. {rec['action']}")
            lines.append(f"*Priority:* {rec['priority'].upper()}")
            lines.append(f"")
            lines.append(f"{rec['description']}")
            if rec.get("command"):
                lines.append(f"")
                lines.append(f"```bash")
                lines.append(f"{rec['command']}")
                lines.append(f"```")
            lines.append("")
        return "\n".join(lines)
        
    def _generate_report(self, data: dict[str, Any]) -> Path:
        """Generate the Synthesis Report as a scientific Typst document."""
        output_file = self.output_dir / f"synthesis_report_{self.timestamp}.typ"
        
        content = f'''// DIALECTIC - Synthesis Report (Scientific Format)
// Generated: {data["timestamp"]}

#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)
#set par(justify: true)

// Title Block
#align(center)[
  #text(18pt, weight: "bold")[DIALECTIC SYNTHESIS REPORT]
  #v(0.3em)
  #text(14pt, fill: purple)[PHASE 3: SYNTHESIS]
  #v(0.5em)
  #text(12pt)[A Dialectical Analysis of Project State]
  #v(0.3em)
  #text(10pt, style: "italic")[Generated by DIALECTIC Engine]
  #v(0.3em)
  #text(10pt)[{datetime.now().strftime("%Y-%m-%d")}]
]

#line(length: 100%, stroke: 0.5pt)
#v(1em)

// Abstract
#block(inset: (x: 2em))[
  #text(weight: "bold")[Abstract]
  
  This report presents the synthesis phase of a dialectical analysis, combining findings from the thesis (assembly) and antithesis (sanity check) phases. The analysis employs the Hegelian dialectical method to systematically evaluate project state and generate actionable recommendations.
]

#v(1em)

= 1. Introduction

The DIALECTIC Engine implements a three-phase analytical framework based on Hegelian dialectics:

1. *Thesis (Assembly)*: Gathering context and establishing initial propositions
2. *Antithesis (Sanity Check)*: Challenging assumptions and validating evidence
3. *Synthesis (Problem Description)*: Resolving contradictions and generating conclusions

This report documents the synthesis phase, which integrates findings from previous phases.

= 2. Methodology

The synthesis phase employs the following methodology:

+ Analysis of previous phase outputs
+ Identification of problem areas
+ Generation of structured recommendations
+ Creation of supporting MVP documents

= 3. Results

== 3.1 Phase Completion Status

#table(
  columns: (1fr, 1fr),
  [*Phase*], [*Status*],
  [Thesis (Assembly)], [{("Complete" if data["analysis"]["assembly_complete"] else "Incomplete")}],
  [Antithesis (Sanity Check)], [{("Complete" if data["analysis"]["antithesis_complete"] else "Incomplete")}],
  [Synthesis (This Phase)], [In Progress],
)

== 3.2 Problem Description

*Summary:* {data["problem_description"]["summary"]}

=== Problem Areas
{self._format_areas_for_report(data["problem_description"]["areas"])}

=== Constraints
{self._format_list_as_typst(data["problem_description"]["constraints"])}

=== Opportunities
{self._format_list_as_typst(data["problem_description"]["opportunities"])}

= 4. Recommendations

{self._format_recommendations_for_report(data["recommendations"])}

= 5. Conclusions

The dialectical analysis process has produced:
- A systematic evaluation of project state
- Evidence-based validation of assumptions
- Actionable recommendations for next steps

The SITREP generation will consolidate all findings into a comprehensive status report suitable for work effort seeding.

= 6. References

+ Hegel, G.W.F. (1807). _Phenomenology of Spirit_.
+ WAFT Project Documentation
+ DIALECTIC Engine Specification

#v(2em)
#line(length: 100%, stroke: 0.5pt)
#align(center)[
  #text(8pt, fill: gray)[
    DIALECTIC Engine // Port 2112 // Realm: dialectic_realm \\
    "The truth is the whole." - G.W.F. Hegel
  ]
]
'''
        
        with open(output_file, "w") as f:
            f.write(content)
            
        # Try to compile to PDF
        pdf_path = self._compile_to_pdf(output_file)
        
        return pdf_path if pdf_path else output_file
        
    def _format_areas_for_report(self, areas: list) -> str:
        """Format areas for scientific report."""
        if not areas:
            return "No problem areas identified."
        lines = []
        for area in areas:
            status = "Complete" if area["status"] == "complete" else "Incomplete"
            lines.append(f"- *{area['name']}* ({status}): {area['description']}")
        return "\n".join(lines)
        
    def _format_recommendations_for_report(self, recommendations: list) -> str:
        """Format recommendations for scientific report."""
        if not recommendations:
            return "No recommendations at this time."
        lines = []
        for i, rec in enumerate(recommendations, 1):
            lines.append(f"*Recommendation {i}:* {rec['action']}")
            lines.append(f"")
            lines.append(f"Priority: {rec['priority'].upper()}")
            lines.append(f"")
            lines.append(f"{rec['description']}")
            lines.append("")
        return "\n".join(lines)
        
    def _compile_to_pdf(self, typ_file: Path) -> Path | None:
        """Compile Typst file to PDF if typst is available."""
        if not shutil.which("typst"):
            logger.warning("Typst not found - skipping PDF compilation")
            return None
            
        pdf_file = typ_file.with_suffix(".pdf")
        try:
            result = subprocess.run(
                ["typst", "compile", str(typ_file), str(pdf_file)],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                logger.info(f"PDF generated: {pdf_file}")
                return pdf_file
            else:
                logger.warning(f"Typst compilation failed: {result.stderr}")
                return None
        except Exception as e:
            logger.warning(f"PDF compilation error: {e}")
            return None
