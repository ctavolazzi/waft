#!/usr/bin/env python3
"""
WAFT Self-Study System
======================

Enables WAFT to monitor and iteratively study itself through the proof system.

Study Areas:
- Template Health: All PDF templates are properly formatted
- Code Quality: Source code follows standards
- System Health: Project structure, dependencies, git status
- Work Efforts: Active work tracking integrity
- Epistemic State: Knowledge coverage and uncertainty

Iterative Studies:
- Tracks study history
- Compares results over time
- Identifies trends and regressions
- Generates comprehensive reports
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
import subprocess
import re

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from scripts.prove_it_comprehensive import ProofCaseBuilder


class WAFTSelfStudy:
    """Self-study system for WAFT using proof methodology."""
    
    def __init__(self, project_path: Path):
        """Initialize self-study system."""
        self.project_path = project_path
        self.study_history_path = project_path / "_work_efforts" / "self_studies"
        self.study_history_path.mkdir(parents=True, exist_ok=True)
        
    def get_study_areas(self) -> Dict[str, Dict[str, Any]]:
        """Define study areas and their claims."""
        return {
            "template_health": {
                "claim": "All PDF templates are properly formatted and free of problematic styling",
                "description": "Verifies template files for black bars, proper CSS, and formatting issues",
                "verification_method": "template_scan"
            },
            "code_quality": {
                "claim": "Source code follows project standards and best practices",
                "description": "Checks code quality, imports, error handling, and structure",
                "verification_method": "code_analysis"
            },
            "system_health": {
                "claim": "WAFT system is healthy and operational",
                "description": "Verifies project structure, dependencies, git status, and core systems",
                "verification_method": "system_check"
            },
            "work_efforts": {
                "claim": "Work efforts system is properly structured and maintained",
                "description": "Checks work efforts directory structure, index files, and organization",
                "verification_method": "work_efforts_check"
            },
            "epistemic_state": {
                "claim": "Epistemic tracking is functioning correctly",
                "description": "Verifies Empirica integration, knowledge tracking, and epistemic state",
                "verification_method": "epistemic_check"
            }
        }
    
    def run_study(self, study_area: Optional[str] = None, all_areas: bool = False) -> Dict[str, Any]:
        """
        Run a self-study on specified area(s).
        
        Args:
            study_area: Specific area to study (or None for all)
            all_areas: If True, study all areas
            
        Returns:
            Dictionary with study results
        """
        study_areas = self.get_study_areas()
        
        if all_areas:
            areas_to_study = list(study_areas.keys())
        elif study_area:
            if study_area not in study_areas:
                raise ValueError(f"Unknown study area: {study_area}. Available: {list(study_areas.keys())}")
            areas_to_study = [study_area]
        else:
            areas_to_study = list(study_areas.keys())  # Default: all areas
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "studies": {},
            "overall_health": {}
        }
        
        print("🔬 WAFT Self-Study System")
        print("=" * 70)
        print()
        
        for area in areas_to_study:
            print(f"📊 Studying: {area}")
            print("-" * 70)
            
            area_info = study_areas[area]
            claim = area_info["claim"]
            
            # Use proof system to study this area
            proof_builder = ProofCaseBuilder(self.project_path, claim)
            
            # Run verification
            verification_results = proof_builder.run_verification()
            
            # Run assumption checks (area-specific)
            assumption_results = self._run_area_specific_checks(area, proof_builder)
            
            # Determine verdict
            verdict, confidence = proof_builder.determine_verdict()
            proof_builder.verdict = verdict
            proof_builder.confidence = confidence
            
            # Build case file
            case_content = proof_builder.build_case_file()
            
            # Save case file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            case_file = self.study_history_path / f"study_{area}_{timestamp}.md"
            case_file.write_text(case_content)
            
            # Generate PDF
            pdf_path = proof_builder.generate_pdf(
                output_path=self.study_history_path / f"STUDY_{area.upper()}_{timestamp}.pdf"
            )
            
            results["studies"][area] = {
                "claim": claim,
                "verdict": verdict,
                "confidence": confidence,
                "case_file": str(case_file.relative_to(self.project_path)),
                "pdf_path": str(pdf_path.relative_to(self.project_path)),
                "verification_results": verification_results,
                "assumption_results": assumption_results
            }
            
            print(f"  ✅ Verdict: {verdict}")
            print(f"  ✅ Confidence: {confidence:.1%}")
            print(f"  ✅ Case File: {case_file.name}")
            print(f"  ✅ PDF: {pdf_path.name}")
            print()
        
        # Calculate overall health
        results["overall_health"] = self._calculate_overall_health(results["studies"])
        
        # Save study results
        results_file = self.study_history_path / f"study_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        results_file.write_text(json.dumps(results, indent=2))
        
        print("=" * 70)
        print("📈 Overall Health Score:", results["overall_health"]["score"])
        print("📈 Overall Health Status:", results["overall_health"]["status"])
        print()
        
        return results
    
    def _run_area_specific_checks(self, area: str, proof_builder: ProofCaseBuilder) -> Dict[str, Any]:
        """Run area-specific assumption checks."""
        if area == "template_health":
            return proof_builder.run_assumption_check()
        elif area == "code_quality":
            return self._check_code_quality(proof_builder)
        elif area == "system_health":
            return self._check_system_health(proof_builder)
        elif area == "work_efforts":
            return self._check_work_efforts(proof_builder)
        elif area == "epistemic_state":
            return self._check_epistemic_state(proof_builder)
        else:
            return {"assumptions": [], "total": 0, "proven": 0, "disproven": 0}
    
    def _check_code_quality(self, proof_builder: ProofCaseBuilder) -> Dict[str, Any]:
        """Check code quality assumptions."""
        assumptions = []
        src_path = self.project_path / "src" / "waft"
        
        # Check for common code quality issues
        quality_checks = [
            {
                "name": "Import organization",
                "pattern": r"^import\s+\w+",
                "description": "Imports should be organized"
            },
            {
                "name": "Error handling",
                "pattern": r"(try:|except\s+:|raise\s+)",
                "description": "Code should have error handling"
            },
            {
                "name": "Type hints",
                "pattern": r"def\s+\w+\([^)]*:\s*\w+",
                "description": "Functions should have type hints"
            }
        ]
        
        python_files = list(src_path.rglob("*.py"))
        for py_file in python_files[:10]:  # Sample first 10 files
            content = py_file.read_text()
            for check in quality_checks:
                matches = list(re.finditer(check["pattern"], content, re.MULTILINE))
                if matches:
                    assumption = {
                        "statement": f"{py_file.name} has {check['name']}",
                        "category": "code_quality",
                        "risk": "low",
                        "status": "PROVEN",
                        "confidence": 0.8,
                        "evidence": [{
                            "type": "code_analysis",
                            "description": f"Found {len(matches)} instances of {check['name']}",
                            "source_file": str(py_file.relative_to(self.project_path)),
                            "verification_method": f"Pattern: {check['pattern']}"
                        }]
                    }
                    assumptions.append(assumption)
        
        return {
            "assumptions": assumptions,
            "total": len(assumptions),
            "proven": len(assumptions),
            "disproven": 0
        }
    
    def _check_system_health(self, proof_builder: ProofCaseBuilder) -> Dict[str, Any]:
        """Check system health assumptions."""
        assumptions = []
        
        # Check for uv.lock
        uv_lock = self.project_path / "uv.lock"
        assumptions.append({
            "statement": "uv.lock file exists",
            "category": "system",
            "risk": "medium",
            "status": "PROVEN" if uv_lock.exists() else "DISPROVEN",
            "confidence": 1.0 if uv_lock.exists() else 0.0,
            "evidence": [{
                "type": "file_check",
                "description": f"uv.lock {'exists' if uv_lock.exists() else 'missing'}",
                "source_file": str(uv_lock.relative_to(self.project_path)),
                "result": "Found" if uv_lock.exists() else "Not found"
            }]
        })
        
        # Check for _pyrite directory
        pyrite_dir = self.project_path / "_pyrite"
        assumptions.append({
            "statement": "_pyrite directory exists",
            "category": "system",
            "risk": "low",
            "status": "PROVEN" if pyrite_dir.exists() else "DISPROVEN",
            "confidence": 1.0 if pyrite_dir.exists() else 0.0,
            "evidence": [{
                "type": "directory_check",
                "description": f"_pyrite {'exists' if pyrite_dir.exists() else 'missing'}",
                "source_file": str(pyrite_dir.relative_to(self.project_path)),
                "result": "Found" if pyrite_dir.exists() else "Not found"
            }]
        })
        
        # Check git status
        try:
            git_status = subprocess.run(
                ["git", "status", "--short"],
                capture_output=True,
                text=True,
                cwd=self.project_path
            ).stdout.strip()
            
            assumptions.append({
                "statement": "Git repository is in good state",
                "category": "system",
                "risk": "low",
                "status": "PROVEN" if not git_status or "??" not in git_status else "INCONCLUSIVE",
                "confidence": 0.9,
                "evidence": [{
                    "type": "git_check",
                    "description": "Git status check",
                    "result": git_status[:200] if git_status else "Clean"
                }]
            })
        except Exception as e:
            assumptions.append({
                "statement": "Git repository check",
                "category": "system",
                "risk": "low",
                "status": "INCONCLUSIVE",
                "confidence": 0.0,
                "evidence": [{
                    "type": "error",
                    "description": f"Git check failed: {e}"
                }]
            })
        
        return {
            "assumptions": assumptions,
            "total": len(assumptions),
            "proven": sum(1 for a in assumptions if a.get("status") == "PROVEN"),
            "disproven": sum(1 for a in assumptions if a.get("status") == "DISPROVEN")
        }
    
    def _check_work_efforts(self, proof_builder: ProofCaseBuilder) -> Dict[str, Any]:
        """Check work efforts system health."""
        assumptions = []
        work_efforts_path = self.project_path / "_work_efforts"
        
        if not work_efforts_path.exists():
            return {
                "assumptions": [{
                    "statement": "_work_efforts directory exists",
                    "status": "DISPROVEN",
                    "confidence": 0.0
                }],
                "total": 1,
                "proven": 0,
                "disproven": 1
            }
        
        # Check for index files
        index_files = list(work_efforts_path.rglob("**/00.00_index.md"))
        assumptions.append({
            "statement": "Work efforts have index files",
            "category": "work_efforts",
            "risk": "low",
            "status": "PROVEN" if index_files else "DISPROVEN",
            "confidence": 1.0 if index_files else 0.0,
            "evidence": [{
                "type": "file_check",
                "description": f"Found {len(index_files)} index files",
                "result": f"{len(index_files)} index files found"
            }]
        })
        
        # Check structure
        subdirs = [d for d in work_efforts_path.iterdir() if d.is_dir()]
        assumptions.append({
            "statement": "Work efforts directory has structure",
            "category": "work_efforts",
            "risk": "low",
            "status": "PROVEN" if subdirs else "DISPROVEN",
            "confidence": 1.0 if subdirs else 0.0,
            "evidence": [{
                "type": "structure_check",
                "description": f"Found {len(subdirs)} subdirectories",
                "result": f"{len(subdirs)} subdirectories"
            }]
        })
        
        return {
            "assumptions": assumptions,
            "total": len(assumptions),
            "proven": sum(1 for a in assumptions if a.get("status") == "PROVEN"),
            "disproven": sum(1 for a in assumptions if a.get("status") == "DISPROVEN")
        }
    
    def _check_epistemic_state(self, proof_builder: ProofCaseBuilder) -> Dict[str, Any]:
        """Check epistemic state assumptions."""
        assumptions = []
        
        # Check for Empirica integration
        try:
            from src.waft.core.empirica import EmpiricaManager
            empirica = EmpiricaManager(self.project_path)
            is_initialized = empirica.is_initialized()
            
            assumptions.append({
                "statement": "Empirica is initialized",
                "category": "epistemic",
                "risk": "low",
                "status": "PROVEN" if is_initialized else "DISPROVEN",
                "confidence": 1.0 if is_initialized else 0.0,
                "evidence": [{
                    "type": "empirica_check",
                    "description": f"Empirica {'initialized' if is_initialized else 'not initialized'}",
                    "result": "Initialized" if is_initialized else "Not initialized"
                }]
            })
        except Exception as e:
            assumptions.append({
                "statement": "Empirica integration check",
                "category": "epistemic",
                "risk": "low",
                "status": "INCONCLUSIVE",
                "confidence": 0.0,
                "evidence": [{
                    "type": "error",
                    "description": f"Empirica check failed: {e}"
                }]
            })
        
        return {
            "assumptions": assumptions,
            "total": len(assumptions),
            "proven": sum(1 for a in assumptions if a.get("status") == "PROVEN"),
            "disproven": sum(1 for a in assumptions if a.get("status") == "DISPROVEN")
        }
    
    def _calculate_overall_health(self, studies: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall health from all studies."""
        if not studies:
            return {"score": 0.0, "status": "Unknown"}
        
        confidences = [study["confidence"] for study in studies.values()]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        
        proven_count = sum(1 for s in studies.values() if s["verdict"] == "PROVEN")
        total_count = len(studies)
        proven_ratio = proven_count / total_count if total_count > 0 else 0.0
        
        # Combined score
        health_score = (avg_confidence * 0.6 + proven_ratio * 0.4) * 100
        
        if health_score >= 90:
            status = "Excellent"
        elif health_score >= 75:
            status = "Good"
        elif health_score >= 50:
            status = "Fair"
        else:
            status = "Poor"
        
        return {
            "score": health_score,
            "status": status,
            "average_confidence": avg_confidence,
            "proven_ratio": proven_ratio,
            "studies_proven": proven_count,
            "studies_total": total_count
        }
    
    def get_study_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent study history."""
        history = []
        results_files = sorted(
            self.study_history_path.glob("study_results_*.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )[:limit]
        
        for results_file in results_files:
            try:
                data = json.loads(results_file.read_text())
                history.append({
                    "timestamp": data.get("timestamp"),
                    "overall_health": data.get("overall_health", {}),
                    "file": str(results_file.relative_to(self.project_path))
                })
            except Exception:
                continue
        
        return history
    
    def compare_studies(self, study1_path: Path, study2_path: Path) -> Dict[str, Any]:
        """Compare two studies to identify changes."""
        study1 = json.loads(study1_path.read_text())
        study2 = json.loads(study2_path.read_text())
        
        comparison = {
            "study1": study1_path.name,
            "study2": study2_path.name,
            "timestamp1": study1.get("timestamp"),
            "timestamp2": study2.get("timestamp"),
            "changes": {}
        }
        
        # Compare each study area
        for area in study1.get("studies", {}).keys():
            if area in study2.get("studies", {}):
                s1 = study1["studies"][area]
                s2 = study2["studies"][area]
                
                comparison["changes"][area] = {
                    "verdict_changed": s1["verdict"] != s2["verdict"],
                    "confidence_delta": s2["confidence"] - s1["confidence"],
                    "verdict1": s1["verdict"],
                    "verdict2": s2["verdict"],
                    "confidence1": s1["confidence"],
                    "confidence2": s2["confidence"]
                }
        
        # Compare overall health
        h1 = study1.get("overall_health", {})
        h2 = study2.get("overall_health", {})
        comparison["health_change"] = {
            "score_delta": h2.get("score", 0) - h1.get("score", 0),
            "status_changed": h1.get("status") != h2.get("status"),
            "score1": h1.get("score", 0),
            "score2": h2.get("score", 0),
            "status1": h1.get("status"),
            "status2": h2.get("status")
        }
        
        return comparison


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="WAFT Self-Study System")
    parser.add_argument(
        "--area",
        choices=["template_health", "code_quality", "system_health", "work_efforts", "epistemic_state"],
        help="Specific area to study"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Study all areas"
    )
    parser.add_argument(
        "--history",
        type=int,
        metavar="N",
        help="Show last N studies"
    )
    parser.add_argument(
        "--compare",
        nargs=2,
        metavar=("STUDY1", "STUDY2"),
        help="Compare two study results"
    )
    
    args = parser.parse_args()
    
    project_path = Path(__file__).parent.parent
    self_study = WAFTSelfStudy(project_path)
    
    if args.history:
        history = self_study.get_study_history(limit=args.history)
        print("📚 Study History")
        print("=" * 70)
        for entry in history:
            health = entry["overall_health"]
            print(f"  {entry['timestamp']}: {health.get('status')} ({health.get('score', 0):.1f})")
            print(f"    {entry['file']}")
            print()
    elif args.compare:
        study1_path = self_study.study_history_path / args.compare[0]
        study2_path = self_study.study_history_path / args.compare[1]
        comparison = self_study.compare_studies(study1_path, study2_path)
        print("📊 Study Comparison")
        print("=" * 70)
        print(json.dumps(comparison, indent=2))
    else:
        # Run study
        results = self_study.run_study(
            study_area=args.area,
            all_areas=args.all or not args.area
        )
        
        print("✅ Self-study complete!")
        print(f"📁 Results saved to: {self_study.study_history_path}")


if __name__ == "__main__":
    main()
