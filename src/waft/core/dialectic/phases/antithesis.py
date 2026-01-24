"""
DIALECTIC Phase 2: ANTITHESIS (Sanity Check)

Challenges assumptions, validates evidence, creates checkout.
This is the "antithesis" in the Hegelian dialectic - the opposition/negation.
"""

import logging
import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import Any
import shutil

logger = logging.getLogger("Dialectic.Antithesis")


class AntithesisPhase:
    """
    Antithesis Phase - SANITY CHECK
    
    Responsibilities:
    1. Extract assumptions from Assembly phase
    2. Validate each assumption with evidence
    3. Create checkout documentation
    4. Generate Sanity Check Report PDF
    """
    
    def __init__(self, project_path: Path, output_dir: Path):
        self.project_path = Path(project_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def run(self) -> dict[str, Any]:
        """Execute the Antithesis phase."""
        logger.info("Starting ANTITHESIS (Sanity Check) Phase...")
        
        # 1. Extract Assumptions
        assumptions = self._extract_assumptions()
        logger.info(f"Assumptions extracted: {len(assumptions)}")
        
        # 2. Validate Assumptions
        validations = self._validate_assumptions(assumptions)
        logger.info(f"Validations complete: {sum(1 for v in validations if v['status'] == 'proven')}/{len(validations)} proven")
        
        # 3. Create Checkout Summary
        checkout = self._create_checkout_summary()
        logger.info("Checkout summary created")
        
        # 4. Generate Report
        report_data = {
            "phase": "antithesis",
            "timestamp": self.timestamp,
            "assumptions": assumptions,
            "validations": validations,
            "checkout": checkout,
        }
        
        output_path = self._generate_report(report_data)
        
        proven = sum(1 for v in validations if v['status'] == 'proven')
        refuted = sum(1 for v in validations if v['status'] == 'refuted')
        unknown = len(validations) - proven - refuted
        
        return {
            "status": "success",
            "phase": "antithesis",
            "output_path": str(output_path),
            "summary": {
                "assumptions_total": len(assumptions),
                "proven": proven,
                "refuted": refuted,
                "unknown": unknown,
            }
        }
        
    def _extract_assumptions(self) -> list[dict[str, Any]]:
        """Extract common assumptions about the project."""
        assumptions = []
        
        # Check for common project assumptions
        checks = [
            {
                "id": "git_repo",
                "assumption": "Project is a git repository",
                "check": lambda: (self.project_path / ".git").exists(),
            },
            {
                "id": "python_project",
                "assumption": "Project is a Python project",
                "check": lambda: (self.project_path / "pyproject.toml").exists() or (self.project_path / "setup.py").exists(),
            },
            {
                "id": "has_src",
                "assumption": "Project has src/ directory",
                "check": lambda: (self.project_path / "src").exists(),
            },
            {
                "id": "has_tests",
                "assumption": "Project has tests",
                "check": lambda: (self.project_path / "tests").exists() or (self.project_path / "test").exists(),
            },
            {
                "id": "has_work_efforts",
                "assumption": "Project uses work efforts system",
                "check": lambda: (self.project_path / "_work_efforts").exists(),
            },
            {
                "id": "has_realms",
                "assumption": "Project uses realms system",
                "check": lambda: (self.project_path / "_realms").exists(),
            },
            {
                "id": "typst_available",
                "assumption": "Typst is installed for PDF generation",
                "check": lambda: shutil.which("typst") is not None,
            },
            {
                "id": "git_clean",
                "assumption": "Git working directory is clean",
                "check": self._check_git_clean,
            },
        ]
        
        for check in checks:
            assumptions.append({
                "id": check["id"],
                "assumption": check["assumption"],
                "check_func": check["check"],
            })
            
        return assumptions
        
    def _check_git_clean(self) -> bool:
        """Check if git working directory is clean."""
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
            )
            return result.returncode == 0 and not result.stdout.strip()
        except Exception:
            return False
            
    def _validate_assumptions(self, assumptions: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Validate each assumption."""
        validations = []
        
        for assumption in assumptions:
            try:
                result = assumption["check_func"]()
                status = "proven" if result else "refuted"
                evidence = f"Check returned {result}"
            except Exception as e:
                status = "error"
                evidence = f"Check failed: {str(e)}"
                
            validations.append({
                "id": assumption["id"],
                "assumption": assumption["assumption"],
                "status": status,
                "evidence": evidence,
            })
            
        return validations
        
    def _create_checkout_summary(self) -> dict[str, Any]:
        """Create a checkout/session summary."""
        return {
            "timestamp": datetime.now().isoformat(),
            "project_path": str(self.project_path),
            "git_branch": self._get_git_branch(),
            "uncommitted_files": self._count_uncommitted_files(),
        }
        
    def _get_git_branch(self) -> str:
        """Get current git branch."""
        try:
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
            )
            return result.stdout.strip() if result.returncode == 0 else "unknown"
        except Exception:
            return "unknown"
            
    def _count_uncommitted_files(self) -> int:
        """Count uncommitted files."""
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                return len([l for l in result.stdout.strip().split("\n") if l])
            return 0
        except Exception:
            return 0
            
    def _generate_report(self, data: dict[str, Any]) -> Path:
        """Generate the Sanity Check Report as a Typst document."""
        output_file = self.output_dir / f"sanity_report_{self.timestamp}.typ"
        
        # Count validation results
        proven = [v for v in data["validations"] if v["status"] == "proven"]
        refuted = [v for v in data["validations"] if v["status"] == "refuted"]
        unknown = [v for v in data["validations"] if v["status"] not in ["proven", "refuted"]]
        
        content = f'''// DIALECTIC - Sanity Check Report (ANTITHESIS)
// Generated: {data["timestamp"]}

#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)

#align(center)[
  #text(18pt, weight: "bold")[DIALECTIC - SANITY CHECK REPORT]
  #v(0.3em)
  #text(14pt, fill: red)[PHASE 2: ANTITHESIS]
  #v(0.3em)
  #text(10pt)[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]
]

#line(length: 100%, stroke: 0.5pt)

= 1. Validation Summary

#table(
  columns: (1fr, 1fr, 1fr),
  [*Proven*], [*Refuted*], [*Unknown*],
  [#text(fill: green)[{len(proven)}]], [#text(fill: red)[{len(refuted)}]], [#text(fill: orange)[{len(unknown)}]],
)

= 2. Assumption Validations

== Proven Assumptions
{self._format_validations_as_typst(proven, "green")}

== Refuted Assumptions
{self._format_validations_as_typst(refuted, "red")}

== Unknown/Error
{self._format_validations_as_typst(unknown, "orange")}

= 3. Checkout Summary

#block(inset: 1em, stroke: (left: 3pt + red))[
  *Git Branch:* {data["checkout"]["git_branch"]} \\
  *Uncommitted Files:* {data["checkout"]["uncommitted_files"]} \\
  *Checkout Time:* {data["checkout"]["timestamp"]}
]

= 4. Recommendations

{self._generate_recommendations(data["validations"])}

#v(2em)
#line(length: 100%, stroke: 0.5pt)
#align(center)[
  #text(8pt, fill: gray)[
    DIALECTIC Engine // Antithesis Phase Complete \\
    Ready for SYNTHESIS (Problem Description)
  ]
]
'''
        
        with open(output_file, "w") as f:
            f.write(content)
            
        # Try to compile to PDF
        pdf_path = self._compile_to_pdf(output_file)
        
        return pdf_path if pdf_path else output_file
        
    def _format_validations_as_typst(self, validations: list, color: str) -> str:
        """Format validations as Typst list."""
        if not validations:
            return "- None"
        lines = []
        for v in validations:
            icon = "✓" if v["status"] == "proven" else "✗" if v["status"] == "refuted" else "?"
            lines.append(f"- {icon} *{v['assumption']}* \\")
            lines.append(f"  Evidence: _{v['evidence']}_")
        return "\n".join(lines)
        
    def _generate_recommendations(self, validations: list) -> str:
        """Generate recommendations based on validation results."""
        recommendations = []
        
        for v in validations:
            if v["status"] == "refuted":
                if v["id"] == "git_clean":
                    recommendations.append("- Consider committing or stashing uncommitted changes")
                elif v["id"] == "typst_available":
                    recommendations.append("- Install Typst for PDF generation: `cargo install typst`")
                elif v["id"] == "has_tests":
                    recommendations.append("- Consider adding tests to improve code quality")
                    
        return "\n".join(recommendations) if recommendations else "- All critical checks passed. Proceed to Synthesis."
        
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
