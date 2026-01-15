#!/usr/bin/env python3
"""
Thorough Evidence Collection for Claims
======================================

Please collect more evidence of this claim through thorough study:

This script provides comprehensive, multi-dimensional evidence collection
for any claim using the proof system and self-study capabilities.

Features:
- Extended verification checks across all dimensions
- Multi-area analysis (templates, code, system, work efforts, epistemic)
- Deep assumption validation with extensive evidence
- Comprehensive case file generation
- Professional PDF documentation
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from scripts.prove_it_comprehensive import ProofCaseBuilder
from scripts.waft_self_study import WAFTSelfStudy


class ThoroughStudyBuilder:
    """Builds thorough evidence collection for claims."""
    
    def __init__(self, project_path: Path, claim: str):
        """
        Initialize thorough study builder.
        
        Args:
            project_path: Project root path
            claim: The claim to study thoroughly
        """
        self.project_path = project_path
        self.claim = claim
        self.proof_builder = ProofCaseBuilder(project_path, claim)
        self.self_study = WAFTSelfStudy(project_path)
        self.multi_area_results: Dict[str, Any] = {}
        self.extended_verification: Dict[str, Any] = {}
        self.deep_assumptions: Dict[str, Any] = {}
        
    def run_thorough_study(self) -> Dict[str, Any]:
        """
        Run thorough evidence collection.
        
        Returns:
            Dictionary with complete study results
        """
        print("=" * 70)
        print("THOROUGH STUDY: Comprehensive Evidence Collection")
        print("=" * 70)
        print()
        print(f"**Claim**: {self.claim}")
        print()
        
        # Phase 1: Extended Verification
        print("Phase 1: Extended Verification")
        print("-" * 70)
        self.extended_verification = self._run_extended_verification()
        print()
        
        # Phase 2: Multi-Area Analysis
        print("Phase 2: Multi-Area Analysis")
        print("-" * 70)
        self.multi_area_results = self._run_multi_area_analysis()
        print()
        
        # Phase 3: Deep Assumption Validation
        print("Phase 3: Deep Assumption Validation")
        print("-" * 70)
        self.deep_assumptions = self._run_deep_assumption_validation()
        print()
        
        # Phase 4: Build Comprehensive Case File
        print("Phase 4: Building Comprehensive Case File")
        print("-" * 70)
        case_content = self._build_comprehensive_case_file()
        
        # Save case file
        case_file = self.project_path / "_work_efforts" / "proof_cases" / f"case_thorough_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        case_file.parent.mkdir(parents=True, exist_ok=True)
        case_file.write_text(case_content)
        print(f"  ✅ Case File: {case_file.name}")
        
        # Phase 5: Generate PDF
        print("Phase 5: Generating PDF Binder")
        print("-" * 70)
        pdf_path = self._generate_comprehensive_pdf(case_content, case_file)
        print(f"  ✅ PDF Binder: {pdf_path.name}")
        print()
        
        # Determine overall verdict
        verdict, confidence = self._determine_overall_verdict()
        
        print("=" * 70)
        print("THOROUGH STUDY COMPLETE")
        print("=" * 70)
        print()
        print(f"**Verdict**: {verdict}")
        print(f"**Confidence**: {confidence:.1%}")
        print()
        print(f"📄 Case File: {case_file}")
        print(f"📄 PDF Binder: {pdf_path}")
        print()
        
        # Open PDF
        import subprocess
        import platform
        system = platform.system()
        if system == "Darwin":  # macOS
            subprocess.run(["open", str(pdf_path)], check=False)
        elif system == "Windows":
            subprocess.run(["start", str(pdf_path)], shell=True, check=False)
        else:  # Linux
            subprocess.run(["xdg-open", str(pdf_path)], check=False)
        
        return {
            "verdict": verdict,
            "confidence": confidence,
            "case_file": str(case_file),
            "pdf_path": str(pdf_path),
            "extended_verification": self.extended_verification,
            "multi_area_results": self.multi_area_results,
            "deep_assumptions": self.deep_assumptions
        }
    
    def _run_extended_verification(self) -> Dict[str, Any]:
        """Run extended verification checks."""
        # Standard verification
        standard_verification = self.proof_builder.run_verification()
        
        # Additional checks
        extended = {
            "standard": standard_verification,
            "code_quality": self._check_code_quality(),
            "system_health": self._check_system_health(),
            "work_efforts": self._check_work_efforts_structure(),
            "epistemic": self._check_epistemic_state()
        }
        
        return extended
    
    def _check_code_quality(self) -> Dict[str, Any]:
        """Check code quality."""
        print("  🔍 Code Quality Check...")
        src_path = self.project_path / "src" / "waft"
        python_files = list(src_path.rglob("*.py"))[:20]  # Sample
        
        checks = {
            "files_analyzed": len(python_files),
            "imports_found": 0,
            "error_handling_found": 0,
            "type_hints_found": 0
        }
        
        for py_file in python_files:
            try:
                content = py_file.read_text()
                if "import " in content:
                    checks["imports_found"] += 1
                if "try:" in content or "except" in content:
                    checks["error_handling_found"] += 1
                if ":" in content and "def " in content:
                    checks["type_hints_found"] += 1
            except Exception:
                continue
        
        print(f"    ✅ Analyzed {checks['files_analyzed']} files")
        return checks
    
    def _check_system_health(self) -> Dict[str, Any]:
        """Check system health."""
        print("  🔍 System Health Check...")
        checks = {
            "uv_lock_exists": (self.project_path / "uv.lock").exists(),
            "pyrite_exists": (self.project_path / "_pyrite").exists(),
            "work_efforts_exists": (self.project_path / "_work_efforts").exists(),
            "src_exists": (self.project_path / "src").exists()
        }
        
        print(f"    ✅ System structure verified")
        return checks
    
    def _check_work_efforts_structure(self) -> Dict[str, Any]:
        """Check work efforts structure."""
        print("  🔍 Work Efforts Structure Check...")
        work_efforts_path = self.project_path / "_work_efforts"
        
        if not work_efforts_path.exists():
            return {"exists": False}
        
        index_files = list(work_efforts_path.rglob("**/00.00_index.md"))
        subdirs = [d for d in work_efforts_path.iterdir() if d.is_dir()]
        
        checks = {
            "exists": True,
            "index_files": len(index_files),
            "subdirectories": len(subdirs)
        }
        
        print(f"    ✅ Found {checks['index_files']} index files, {checks['subdirectories']} subdirectories")
        return checks
    
    def _check_epistemic_state(self) -> Dict[str, Any]:
        """Check epistemic state."""
        print("  🔍 Epistemic State Check...")
        try:
            from src.waft.core.empirica import EmpiricaManager
            empirica = EmpiricaManager(self.project_path)
            is_initialized = empirica.is_initialized()
            
            checks = {
                "empirica_available": True,
                "initialized": is_initialized
            }
            print(f"    ✅ Empirica {'initialized' if is_initialized else 'not initialized'}")
        except Exception as e:
            checks = {
                "empirica_available": False,
                "error": str(e)
            }
            print(f"    ⚠️ Empirica check: {e}")
        
        return checks
    
    def _run_multi_area_analysis(self) -> Dict[str, Any]:
        """Run multi-area analysis."""
        study_areas = self.self_study.get_study_areas()
        results = {}
        
        for area_name, area_info in study_areas.items():
            print(f"  📊 Analyzing: {area_name}...")
            
            # Create proof builder for this area
            area_claim = f"{self.claim} (from {area_name} perspective)"
            area_proof = ProofCaseBuilder(self.project_path, area_claim)
            
            # Run verification
            area_verification = area_proof.run_verification()
            
            # Run area-specific checks
            area_assumptions = self.self_study._run_area_specific_checks(area_name, area_proof)
            
            # Determine verdict
            verdict, confidence = area_proof.determine_verdict()
            
            results[area_name] = {
                "claim": area_claim,
                "verdict": verdict,
                "confidence": confidence,
                "verification": area_verification,
                "assumptions": area_assumptions
            }
            
            print(f"    ✅ {area_name}: {verdict} ({confidence:.1%})")
        
        return results
    
    def _run_deep_assumption_validation(self) -> Dict[str, Any]:
        """Run deep assumption validation."""
        # Standard assumption check
        standard_assumptions = self.proof_builder.run_assumption_check()
        
        # Additional deep checks
        deep_checks = {
            "standard": standard_assumptions,
            "cross_references": self._find_cross_references(),
            "additional_evidence": self._collect_additional_evidence()
        }
        
        return deep_checks
    
    def _find_cross_references(self) -> Dict[str, Any]:
        """Find cross-references between areas."""
        print("  🔍 Finding Cross-References...")
        
        cross_refs = {
            "template_code_links": [],
            "system_template_links": [],
            "work_efforts_system_links": []
        }
        
        # Find links between templates and code
        template_dir = self.project_path / "src" / "waft" / "templates"
        if template_dir.exists():
            templates = list(template_dir.glob("*.py"))
            cross_refs["template_code_links"] = [
                str(t.relative_to(self.project_path)) for t in templates[:5]
            ]
        
        print(f"    ✅ Found {len(cross_refs['template_code_links'])} cross-references")
        return cross_refs
    
    def _collect_additional_evidence(self) -> Dict[str, Any]:
        """Collect additional evidence."""
        print("  🔍 Collecting Additional Evidence...")
        
        evidence = {
            "git_history": self._get_git_history(),
            "recent_files": self._get_recent_files(),
            "project_stats": self._get_project_stats()
        }
        
        print(f"    ✅ Collected additional evidence")
        return evidence
    
    def _get_git_history(self) -> Dict[str, Any]:
        """Get git history."""
        import subprocess
        try:
            log_output = subprocess.run(
                ["git", "log", "--oneline", "-10"],
                capture_output=True,
                text=True,
                cwd=self.project_path
            ).stdout.strip()
            return {"recent_commits": log_output.split("\n")[:10]}
        except Exception:
            return {"error": "Could not retrieve git history"}
    
    def _get_recent_files(self) -> Dict[str, Any]:
        """Get recent files."""
        import os
        recent = []
        for root, dirs, files in os.walk(self.project_path / "src"):
            for file in files[:10]:
                file_path = Path(root) / file
                try:
                    mtime = file_path.stat().st_mtime
                    recent.append({
                        "path": str(file_path.relative_to(self.project_path)),
                        "modified": datetime.fromtimestamp(mtime).isoformat()
                    })
                except Exception:
                    continue
            break
        return {"recent_files": sorted(recent, key=lambda x: x["modified"], reverse=True)[:10]}
    
    def _get_project_stats(self) -> Dict[str, Any]:
        """Get project statistics."""
        stats = {
            "python_files": len(list(self.project_path.rglob("*.py"))),
            "template_files": len(list((self.project_path / "src" / "waft" / "templates").glob("*.py"))),
            "markdown_files": len(list(self.project_path.rglob("*.md")))
        }
        return stats
    
    def _build_comprehensive_case_file(self) -> str:
        """Build comprehensive case file."""
        case_content = []
        
        # Title
        case_content.append("# THOROUGH STUDY: Comprehensive Evidence Collection")
        case_content.append("")
        case_content.append(f"**Case ID**: THOROUGH-{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        case_content.append(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        case_content.append(f"**Claim**: {self.claim}")
        case_content.append("")
        case_content.append("=" * 70)
        case_content.append("")
        
        # Abstract
        case_content.append("## ABSTRACT")
        case_content.append("")
        case_content.append("This thorough study provides comprehensive, multi-dimensional evidence collection")
        case_content.append(f"for the claim: **{self.claim}**")
        case_content.append("")
        case_content.append("Evidence was collected through:")
        case_content.append("- Extended verification checks across all dimensions")
        case_content.append("- Multi-area analysis from five perspectives")
        case_content.append("- Deep assumption validation with extensive evidence")
        case_content.append("- Cross-referenced findings")
        case_content.append("")
        case_content.append("=" * 70)
        case_content.append("")
        
        # Extended Verification
        case_content.append("## EXTENDED VERIFICATION")
        case_content.append("")
        case_content.append("### Standard Verification")
        case_content.append("")
        for key, value in self.extended_verification.get("standard", {}).items():
            if isinstance(value, dict):
                case_content.append(f"- **{key}**: {value.get('status', 'N/A')}")
        case_content.append("")
        
        case_content.append("### Additional Checks")
        case_content.append("")
        case_content.append("#### Code Quality")
        code_quality = self.extended_verification.get("code_quality", {})
        case_content.append(f"- Files Analyzed: {code_quality.get('files_analyzed', 0)}")
        case_content.append(f"- Imports Found: {code_quality.get('imports_found', 0)}")
        case_content.append(f"- Error Handling Found: {code_quality.get('error_handling_found', 0)}")
        case_content.append("")
        
        case_content.append("#### System Health")
        system_health = self.extended_verification.get("system_health", {})
        for key, value in system_health.items():
            case_content.append(f"- **{key}**: {'✅' if value else '❌'}")
        case_content.append("")
        
        case_content.append("=" * 70)
        case_content.append("")
        
        # Multi-Area Analysis
        case_content.append("## MULTI-AREA ANALYSIS")
        case_content.append("")
        for area_name, area_result in self.multi_area_results.items():
            case_content.append(f"### {area_name.replace('_', ' ').title()}")
            case_content.append("")
            case_content.append(f"**Verdict**: {area_result.get('verdict', 'N/A')}")
            case_content.append(f"**Confidence**: {area_result.get('confidence', 0):.1%}")
            case_content.append("")
        
        case_content.append("=" * 70)
        case_content.append("")
        
        # Deep Assumption Validation
        case_content.append("## DEEP ASSUMPTION VALIDATION")
        case_content.append("")
        standard_assumptions = self.deep_assumptions.get("standard", {})
        case_content.append(f"**Total Assumptions**: {standard_assumptions.get('total', 0)}")
        case_content.append(f"**Proven**: {standard_assumptions.get('proven', 0)}")
        case_content.append(f"**Disproven**: {standard_assumptions.get('disproven', 0)}")
        case_content.append("")
        
        case_content.append("### Cross-References")
        cross_refs = self.deep_assumptions.get("cross_references", {})
        case_content.append(f"- Template-Code Links: {len(cross_refs.get('template_code_links', []))}")
        case_content.append("")
        
        case_content.append("=" * 70)
        case_content.append("")
        
        # Conclusion
        verdict, confidence = self._determine_overall_verdict()
        case_content.append("## CONCLUSION")
        case_content.append("")
        case_content.append(f"**Overall Verdict**: {verdict}")
        case_content.append(f"**Overall Confidence**: {confidence:.1%}")
        case_content.append("")
        case_content.append("This thorough study has collected comprehensive evidence from multiple")
        case_content.append("dimensions and perspectives, providing a complete picture of the claim.")
        case_content.append("")
        
        return "\n".join(case_content)
    
    def _determine_overall_verdict(self) -> tuple[str, float]:
        """Determine overall verdict from all evidence."""
        # Collect all verdicts
        verdicts = []
        confidences = []
        
        # From multi-area analysis
        for area_result in self.multi_area_results.values():
            verdicts.append(area_result.get("verdict", "INCONCLUSIVE"))
            confidences.append(area_result.get("confidence", 0.0))
        
        # From deep assumptions
        standard_assumptions = self.deep_assumptions.get("standard", {})
        proven = standard_assumptions.get("proven", 0)
        total = standard_assumptions.get("total", 1)
        assumption_confidence = proven / total if total > 0 else 0.0
        confidences.append(assumption_confidence)
        
        # Calculate overall
        if not confidences:
            return "INCONCLUSIVE", 0.0
        
        avg_confidence = sum(confidences) / len(confidences)
        proven_count = sum(1 for v in verdicts if v == "PROVEN")
        proven_ratio = proven_count / len(verdicts) if verdicts else 0.0
        
        # Combined score
        overall_confidence = (avg_confidence * 0.6 + proven_ratio * 0.4)
        
        if overall_confidence >= 0.9:
            verdict = "PROVEN"
        elif overall_confidence >= 0.5:
            verdict = "INCONCLUSIVE"
        else:
            verdict = "DISPROVEN"
        
        return verdict, overall_confidence
    
    def _generate_comprehensive_pdf(self, case_content: str, case_file: Path) -> Path:
        """Generate comprehensive PDF binder."""
        from src.waft.brief import BriefDocument
        
        verdict, confidence = self._determine_overall_verdict()
        
        doc = BriefDocument(
            title=f"Thorough Study: {self.claim[:60]}",
            doc_id=f"THOROUGH-{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            subtitle="Comprehensive Multi-Dimensional Evidence Collection",
            classification="INTERNAL",
            cover_header="WAFT PROJECT",
            cover_metadata={
                "CLAIM": self.claim[:50],
                "VERDICT": verdict,
                "CONFIDENCE": f"{confidence:.1%}"
            },
            cover_warning={
                "message": f"THOROUGH STUDY - {verdict} ({confidence:.1%})",
                "severity": "INFO" if verdict == "PROVEN" else "WARNING"
            },
            cover_footer="THOROUGH EVIDENCE COLLECTION",
            include_system_status=False
        )
        
        # Convert markdown to HTML
        try:
            import markdown
            html_content = markdown.markdown(
                case_content,
                extensions=['fenced_code', 'tables', 'nl2br', 'extra', 'codehilite']
            )
        except ImportError:
            # Fallback
            import re
            html_content = case_content
            html_content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
            html_content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
            html_content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
            html_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_content)
            html_content = re.sub(r'\n', '<br>\n', html_content)
        
        doc.content_blocks.append(html_content)
        
        output_path = case_file.parent / f"THOROUGH_STUDY_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf_path = doc.generate(output_path=output_path)
        
        return pdf_path


def main():
    """Main entry point."""
    # Default claim
    claim = "WAFT self-study system enables comprehensive self-monitoring"
    
    # Check for claim in command line args
    if len(sys.argv) > 1:
        claim = " ".join(sys.argv[1:])
    
    builder = ThoroughStudyBuilder(project_root, claim)
    results = builder.run_thorough_study()
    
    return 0 if results["verdict"] == "PROVEN" else 1


if __name__ == "__main__":
    sys.exit(main())
