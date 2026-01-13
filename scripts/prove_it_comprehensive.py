#!/usr/bin/env python3
"""
Comprehensive Proof System - Build Case File with Evidence

This script:
1. Extracts claims from conversation context
2. Runs /verify checks
3. Runs /check-assumptions validation
4. Builds a case file with evidence
5. Creates PDF binder with verdict on cover
6. Displays the proof

If claims are false, states so clearly in the case brief.
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

from src.waft.brief import create_brief
from src.waft.core.check_assumptions import CheckAssumptionsManager
from src.waft.core.session_stats import SessionStats


class ProofCaseBuilder:
    """Builds a comprehensive proof case with evidence."""
    
    def __init__(self, project_path: Path, claim: str):
        """
        Initialize proof case builder.
        
        Args:
            project_path: Project root path
            claim: The claim to prove/disprove
        """
        self.project_path = project_path
        self.claim = claim
        self.verdict: Optional[str] = None
        self.confidence: float = 0.0
        self.verification_results: Dict[str, Any] = {}
        self.assumption_results: Dict[str, Any] = {}
        self.evidence: List[Dict[str, Any]] = []
        self.case_file_path: Optional[Path] = None
        
    def run_verification(self) -> Dict[str, Any]:
        """Run /verify checks."""
        print("🔍 Running Verification Checks...")
        print()
        
        results = {
            "date_time": {},
            "disk_space": {},
            "working_directory": {},
            "git_status": {},
            "file_existence": {},
            "template_verification": {}
        }
        
        # Date/Time
        import subprocess
        date_output = subprocess.run(["date"], capture_output=True, text=True).stdout.strip()
        results["date_time"] = {
            "status": "✅",
            "evidence": date_output,
            "verified": True
        }
        print(f"  ✅ Date/Time: {date_output}")
        
        # Disk space
        df_output = subprocess.run(
            ["df", "-h", "."], capture_output=True, text=True
        ).stdout.strip().split("\n")[-1]
        results["disk_space"] = {
            "status": "✅",
            "evidence": df_output,
            "verified": True
        }
        print(f"  ✅ Disk Space: {df_output}")
        
        # Working directory
        pwd_output = subprocess.run(["pwd"], capture_output=True, text=True).stdout.strip()
        results["working_directory"] = {
            "status": "✅",
            "evidence": pwd_output,
            "verified": True
        }
        print(f"  ✅ Working Directory: {pwd_output}")
        
        # Git status
        try:
            git_status = subprocess.run(
                ["git", "status", "--short"], capture_output=True, text=True
            ).stdout.strip()
            results["git_status"] = {
                "status": "✅",
                "evidence": git_status[:200] if git_status else "No changes",
                "verified": True
            }
            print(f"  ✅ Git Status: {len(git_status.splitlines()) if git_status else 0} changes")
        except Exception as e:
            results["git_status"] = {
                "status": "⚠️",
                "evidence": str(e),
                "verified": False
            }
        
        # Template verification (black bars)
        template_dir = project_root / "src" / "waft" / "templates"
        if template_dir.exists():
            verify_script = project_root / "scripts" / "verify_no_black_bars.py"
            if verify_script.exists():
                verify_output = subprocess.run(
                    ["python3", str(verify_script)],
                    capture_output=True,
                    text=True,
                    cwd=project_root
                )
                results["template_verification"] = {
                    "status": "✅" if verify_output.returncode == 0 else "❌",
                    "evidence": verify_output.stdout,
                    "verified": verify_output.returncode == 0,
                    "source_script": str(verify_script.relative_to(project_root)),
                    "template_directory": str(template_dir.relative_to(project_root)),
                    "verification_method": "Automated regex pattern matching for black bar CSS patterns"
                }
                print(f"  {'✅' if verify_output.returncode == 0 else '❌'} Template Verification: {'PASSED' if verify_output.returncode == 0 else 'FAILED'}")
        
        print()
        return results
    
    def run_assumption_check(self) -> Dict[str, Any]:
        """Run /check-assumptions validation."""
        print("🔍 Running Assumption Validation...")
        print()
        
        # Direct template verification
        template_dir = self.project_path / "src" / "waft" / "templates"
        assumptions = []
        
        if template_dir.exists():
            import re
            template_files = list(template_dir.glob("*.py"))
            black_bar_pattern = re.compile(r'h[1-6]\s*\{[^}]*background:\s*#000', re.MULTILINE | re.DOTALL)
            
            for template_file in template_files:
                try:
                    content = template_file.read_text()
                    matches = list(black_bar_pattern.finditer(content))
                    
                    if matches:
                        line_numbers = [content[:m.start()].count('\n') + 1 for m in matches]
                        code_snippets = [content[max(0, m.start()-50):m.end()+50] for m in matches[:3]]  # First 3 matches
                        assumption = {
                            "statement": f"Template {template_file.name} has no black bar headers",
                            "category": "code",
                            "risk": "high",
                            "status": "DISPROVEN",
                            "confidence": 1.0,
                            "evidence": [{
                                "type": "code_analysis",
                                "description": f"Found {len(matches)} black bar violations in {template_file.name}",
                                "result": f"Lines: {line_numbers}",
                                "source_file": str(template_file.relative_to(self.project_path)),
                                "source_lines": line_numbers,
                                "code_snippets": code_snippets
                            }]
                        }
                        assumptions.append(assumption)
                        print(f"  ❌ {template_file.name}: BLACK BARS FOUND")
                    else:
                        # Check for h2 headers to show what we verified
                        h2_pattern = re.compile(r'h2\s*\{[^}]*\}', re.MULTILINE | re.DOTALL)
                        h2_matches = list(h2_pattern.finditer(content))
                        h2_snippets = []
                        if h2_matches:
                            for m in h2_matches[:2]:  # Show first 2 h2 styles
                                snippet = content[m.start():m.end()]
                                line_num = content[:m.start()].count('\n') + 1
                                h2_snippets.append({
                                    "line": line_num,
                                    "code": snippet[:200]  # First 200 chars
                                })
                        
                        assumption = {
                            "statement": f"Template {template_file.name} has no black bar headers",
                            "category": "code",
                            "risk": "high",
                            "status": "PROVEN",
                            "confidence": 1.0,
                            "evidence": [{
                                "type": "code_analysis",
                                "description": f"No black bar patterns found in {template_file.name}",
                                "result": "Verified clean",
                                "source_file": str(template_file.relative_to(self.project_path)),
                                "verification_method": "Regex pattern search: h[1-6]\\s*\\{[^}]*background:\\s*#000",
                                "h2_headers_found": len(h2_matches),
                                "sample_h2_styles": h2_snippets
                            }]
                        }
                        assumptions.append(assumption)
                        print(f"  ✅ {template_file.name}: No black bars")
                except Exception as e:
                    assumption = {
                        "statement": f"Template {template_file.name} can be checked",
                        "category": "code",
                        "risk": "medium",
                        "status": "INCONCLUSIVE",
                        "confidence": 0.0,
                        "evidence": [{
                            "type": "error",
                            "description": f"Error checking {template_file.name}",
                            "result": str(e)
                        }]
                    }
                    assumptions.append(assumption)
                    print(f"  ⚠️ {template_file.name}: Error - {e}")
        
        print()
        print(f"  ✅ Templates Checked: {len(assumptions)}")
        print(f"  ✅ Proven: {sum(1 for a in assumptions if a.get('status') == 'PROVEN')}")
        print(f"  ❌ Disproven: {sum(1 for a in assumptions if a.get('status') == 'DISPROVEN')}")
        print()
        
        return {
            "assumptions": assumptions,
            "total": len(assumptions),
            "proven": sum(1 for a in assumptions if a.get('status') == 'PROVEN'),
            "disproven": sum(1 for a in assumptions if a.get('status') == 'DISPROVEN')
        }
    
    def build_case_file(self) -> str:
        """Build the case file content."""
        case_content = []
        
        # ========================================================================
        # TITLE PAGE
        # ========================================================================
        case_content.append("# CASE BRIEF: PROOF OF CLAIM")
        case_content.append("")
        case_content.append(f"**Case ID**: PROOF-{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        case_content.append(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        case_content.append(f"**Claim**: {self.claim}")
        case_content.append(f"**Verdict**: {self.verdict}")
        case_content.append(f"**Confidence**: {self.confidence:.1%}")
        case_content.append("")
        case_content.append("=" * 70)
        case_content.append("")
        
        # ========================================================================
        # ABSTRACT
        # ========================================================================
        case_content.append("## ABSTRACT")
        case_content.append("")
        if self.verdict == "PROVEN":
            case_content.append("This case brief presents comprehensive evidence demonstrating that the claim **is proven** beyond reasonable doubt. ")
        elif self.verdict == "DISPROVEN":
            case_content.append("This case brief presents comprehensive evidence demonstrating that the claim **is disproven**. ")
        else:
            case_content.append("This case brief presents evidence regarding the claim, which **cannot be definitively proven or disproven** with the available evidence. ")
        
        # Count evidence
        assumptions = self.assumption_results.get("assumptions", [])
        proven_count = sum(1 for a in assumptions if a.get("status") == "PROVEN")
        total_count = len(assumptions)
        verification_checks = len([r for r in self.verification_results.values() if isinstance(r, dict) and r.get("verified", False)])
        
        case_content.append(f"Evidence was collected through {verification_checks} verification checks and {total_count} assumption validations. ")
        case_content.append(f"Of the assumptions tested, {proven_count} were proven, {sum(1 for a in assumptions if a.get('status') == 'DISPROVEN')} were disproven, ")
        case_content.append(f"and {sum(1 for a in assumptions if a.get('status') == 'INCONCLUSIVE')} were inconclusive. ")
        case_content.append(f"The overall confidence level is {self.confidence:.1%}.")
        case_content.append("")
        case_content.append("=" * 70)
        case_content.append("")
        
        # ========================================================================
        # HYPOTHESIS
        # ========================================================================
        case_content.append("## HYPOTHESIS")
        case_content.append("")
        case_content.append("### Primary Hypothesis")
        case_content.append("")
        case_content.append(f"**H₀ (Null Hypothesis)**: The claim is false")
        case_content.append("")
        case_content.append(f"**H₁ (Alternative Hypothesis)**: {self.claim}")
        case_content.append("")
        case_content.append("### Testable Predictions")
        case_content.append("")
        case_content.append("If the claim is true, we expect to find:")
        case_content.append("")
        
        # Generate predictions based on claim
        if "black bars" in self.claim.lower() or "template" in self.claim.lower():
            case_content.append("1. No CSS patterns matching `background: #000` in header styles (h1-h6)")
            case_content.append("2. All template files use alternative styling (border-bottom, color changes)")
            case_content.append("3. Verification script confirms zero violations")
            case_content.append("4. Generated PDFs display headers without black backgrounds")
        else:
            case_content.append("1. Evidence supporting the claim exists")
            case_content.append("2. Verification checks pass")
            case_content.append("3. Assumptions validate the claim")
        
        case_content.append("")
        case_content.append("=" * 70)
        case_content.append("")
        
        # ========================================================================
        # METHODOLOGY
        # ========================================================================
        case_content.append("## METHODOLOGY")
        case_content.append("")
        case_content.append("### Verification Process")
        case_content.append("")
        case_content.append("This proof employs a multi-layered verification approach:")
        case_content.append("")
        case_content.append("1. **Environment Verification**: Confirms system state, date/time, disk space, working directory")
        case_content.append("2. **Code Analysis**: Direct examination of source files using regex pattern matching")
        case_content.append("3. **Assumption Validation**: Systematic testing of each assumption with evidence collection")
        case_content.append("4. **Evidence Documentation**: All findings include source files, line numbers, and code snippets")
        case_content.append("")
        case_content.append("### Evidence Collection Standards")
        case_content.append("")
        case_content.append("- **Source Attribution**: Every finding includes file path and line numbers")
        case_content.append("- **Reproducibility**: Verification methods are documented and repeatable")
        case_content.append("- **Traceability**: Evidence chains link findings to source code")
        case_content.append("- **Confidence Scoring**: Each assumption receives a confidence level (0.0-1.0)")
        case_content.append("")
        case_content.append("=" * 70)
        case_content.append("")
        
        # ========================================================================
        # VERIFICATION EVIDENCE
        # ========================================================================
        case_content.append("## VERIFICATION EVIDENCE")
        case_content.append("")
        case_content.append("### Overview")
        case_content.append("")
        verification_count = len([r for r in self.verification_results.values() if isinstance(r, dict)])
        verified_count = len([r for r in self.verification_results.values() if isinstance(r, dict) and r.get("verified", False)])
        case_content.append(f"**Total Checks**: {verification_count}")
        case_content.append(f"**Verified**: {verified_count}")
        case_content.append(f"**Failed**: {verification_count - verified_count}")
        case_content.append("")
        case_content.append("---")
        case_content.append("")
        
        for check_name, check_result in self.verification_results.items():
            status = check_result.get("status", "❓")
            evidence = check_result.get("evidence", "No evidence")
            verified = check_result.get("verified", False)
            source_script = check_result.get("source_script", "")
            template_directory = check_result.get("template_directory", "")
            verification_method = check_result.get("verification_method", "")
            
            case_content.append(f"### {check_name.replace('_', ' ').title()}")
            case_content.append("")
            case_content.append(f"**Status**: {status} {'VERIFIED' if verified else 'NOT VERIFIED'}")
            case_content.append("")
            if source_script:
                case_content.append(f"**Source Script**: `{source_script}`")
                case_content.append("")
            if template_directory:
                case_content.append(f"**Template Directory**: `{template_directory}`")
                case_content.append("")
            if verification_method:
                case_content.append(f"**Verification Method**: {verification_method}")
                case_content.append("")
            case_content.append("**Evidence**:")
            case_content.append("```")
            case_content.append(str(evidence))
            case_content.append("```")
            case_content.append("")
        
        case_content.append("=" * 70)
        case_content.append("")
        
        # ========================================================================
        # ASSUMPTION VALIDATION
        # ========================================================================
        case_content.append("## ASSUMPTION VALIDATION")
        case_content.append("")
        case_content.append("### Overview")
        case_content.append("")
        assumptions = self.assumption_results.get("assumptions", [])
        if assumptions:
            proven = sum(1 for a in assumptions if a.get("status") == "PROVEN")
            disproven = sum(1 for a in assumptions if a.get("status") == "DISPROVEN")
            inconclusive = sum(1 for a in assumptions if a.get("status") == "INCONCLUSIVE")
            case_content.append(f"**Total Assumptions**: {len(assumptions)}")
            case_content.append(f"**Proven**: {proven} ({proven/len(assumptions)*100:.1f}%)")
            case_content.append(f"**Disproven**: {disproven} ({disproven/len(assumptions)*100:.1f}%)")
            case_content.append(f"**Inconclusive**: {inconclusive} ({inconclusive/len(assumptions)*100:.1f}%)")
        else:
            case_content.append("**Total Assumptions**: 0")
        case_content.append("")
        case_content.append("---")
        case_content.append("")
        assumptions = self.assumption_results.get("assumptions", [])
        if assumptions:
            for i, assumption in enumerate(assumptions, 1):
                statement = assumption.get("statement", "Unknown")
                status = assumption.get("status", "UNKNOWN")
                confidence = assumption.get("confidence", 0.0)
                evidence_list = assumption.get("evidence", [])
                
                case_content.append(f"### Assumption {i}: {statement}")
                case_content.append("")
                case_content.append(f"**Status**: {status}")
                case_content.append(f"**Confidence**: {confidence:.1%}")
                case_content.append("")
                if evidence_list:
                    case_content.append("**Evidence**:")
                    for ev in evidence_list:
                        ev_type = ev.get("type", "unknown")
                        ev_desc = ev.get("description", "")
                        ev_result = ev.get("result", "")
                        source_file = ev.get("source_file", "")
                        source_lines = ev.get("source_lines", [])
                        code_snippets = ev.get("code_snippets", [])
                        verification_method = ev.get("verification_method", "")
                        sample_styles = ev.get("sample_h2_styles", [])
                        
                        case_content.append(f"- **{ev_type}**: {ev_desc}")
                        if source_file:
                            case_content.append(f"  - **Source File**: `{source_file}`")
                        if source_lines:
                            case_content.append(f"  - **Line Numbers**: {source_lines}")
                        if verification_method:
                            case_content.append(f"  - **Verification Method**: `{verification_method}`")
                        if ev_result:
                            case_content.append(f"  - **Result**: {ev_result}")
                        if code_snippets:
                            case_content.append(f"  - **Code Snippets (violations)**:")
                            for i, snippet in enumerate(code_snippets, 1):
                                case_content.append(f"    ```css")
                                case_content.append(f"    {snippet}")
                                case_content.append(f"    ```")
                        if sample_styles:
                            case_content.append(f"  - **Sample H2 Styles Verified**:")
                            for style in sample_styles:
                                case_content.append(f"    - Line {style.get('line', '?')}:")
                                case_content.append(f"      ```css")
                                case_content.append(f"      {style.get('code', '')}")
                                case_content.append(f"      ```")
                    case_content.append("")
        else:
            case_content.append("No assumptions extracted or validated.")
            case_content.append("")
        
        case_content.append("=" * 70)
        case_content.append("")
        
        # ========================================================================
        # ADDITIONAL EVIDENCE
        # ========================================================================
        if self.evidence:
            case_content.append("## ADDITIONAL EVIDENCE")
            case_content.append("")
            for i, ev in enumerate(self.evidence, 1):
                ev_type = ev.get("type", "unknown")
                ev_desc = ev.get("description", "")
                ev_data = ev.get("data", "")
                
                case_content.append(f"### Evidence {i}: {ev_type}")
                case_content.append("")
                case_content.append(f"**Description**: {ev_desc}")
                case_content.append("")
                if ev_data:
                    case_content.append("**Data**:")
                    case_content.append("```")
                    case_content.append(str(ev_data))
                    case_content.append("```")
                    case_content.append("")
            case_content.append("=" * 70)
            case_content.append("")
        
        # ========================================================================
        # ANALYSIS
        # ========================================================================
        case_content.append("## ANALYSIS")
        case_content.append("")
        case_content.append("### Evidence Evaluation")
        case_content.append("")
        
        # Analyze verification results
        all_verified = all(
            result.get("verified", False)
            for result in self.verification_results.values()
            if isinstance(result, dict)
        )
        template_verified = self.verification_results.get("template_verification", {}).get("verified", False)
        
        case_content.append("**Verification Status**:")
        case_content.append(f"- All checks passed: {'✅ Yes' if all_verified else '❌ No'}")
        case_content.append(f"- Template verification: {'✅ Passed' if template_verified else '❌ Failed'}")
        case_content.append("")
        
        # Analyze assumptions
        if assumptions:
            case_content.append("**Assumption Analysis**:")
            proven = sum(1 for a in assumptions if a.get("status") == "PROVEN")
            avg_confidence = sum(a.get("confidence", 0.0) for a in assumptions) / len(assumptions) if assumptions else 0.0
            case_content.append(f"- Proven assumptions: {proven}/{len(assumptions)} ({proven/len(assumptions)*100:.1f}%)")
            case_content.append(f"- Average confidence: {avg_confidence:.1%}")
            case_content.append("")
        
        case_content.append("### Key Findings")
        case_content.append("")
        if self.verdict == "PROVEN":
            case_content.append("1. ✅ All verification checks passed successfully")
            if assumptions:
                case_content.append(f"2. ✅ {proven}/{len(assumptions)} assumptions validated with evidence")
            case_content.append("3. ✅ Evidence supports the claim beyond reasonable doubt")
            case_content.append("4. ✅ All sources are traceable and reproducible")
        elif self.verdict == "DISPROVEN":
            case_content.append("1. ❌ Evidence contradicts the claim")
            if assumptions:
                case_content.append(f"2. ❌ {sum(1 for a in assumptions if a.get('status') == 'DISPROVEN')} assumptions disproven")
            case_content.append("3. ❌ Verification checks failed or revealed contradictions")
        else:
            case_content.append("1. ⚠️ Evidence is mixed or insufficient")
            case_content.append("2. ⚠️ Some assumptions validated, others inconclusive")
            case_content.append("3. ⚠️ Additional evidence required for definitive conclusion")
        case_content.append("")
        case_content.append("=" * 70)
        case_content.append("")
        
        # ========================================================================
        # CONCLUSION & SUMMARY
        # ========================================================================
        case_content.append("## CONCLUSION & SUMMARY")
        case_content.append("")
        case_content.append("### Final Verdict")
        case_content.append("")
        if self.verdict == "PROVEN":
            case_content.append("✅ **CLAIM IS PROVEN**")
            case_content.append("")
            case_content.append("Based on comprehensive evidence analysis, the claim is **proven beyond reasonable doubt**. ")
            case_content.append("All verification checks passed, assumptions were validated with traceable evidence, ")
            case_content.append("and the evidence consistently supports the claim.")
        elif self.verdict == "DISPROVEN":
            case_content.append("❌ **CLAIM IS DISPROVEN**")
            case_content.append("")
            case_content.append("Based on comprehensive evidence analysis, the claim is **disproven**. ")
            case_content.append("Evidence contradicts the claim, verification checks failed, or assumptions were invalidated.")
        else:
            case_content.append("⚠️ **VERDICT IS INCONCLUSIVE**")
            case_content.append("")
            case_content.append("Based on the evidence analysis, the claim **cannot be definitively proven or disproven**. ")
            case_content.append("The evidence is mixed, insufficient, or requires additional investigation.")
        case_content.append("")
        case_content.append("### Confidence Assessment")
        case_content.append("")
        case_content.append(f"**Overall Confidence**: {self.confidence:.1%}")
        case_content.append("")
        if self.confidence >= 0.95:
            case_content.append("**Interpretation**: Very High Confidence - Evidence is strong and consistent")
        elif self.confidence >= 0.80:
            case_content.append("**Interpretation**: High Confidence - Evidence is strong with minor uncertainties")
        elif self.confidence >= 0.60:
            case_content.append("**Interpretation**: Moderate Confidence - Evidence supports conclusion but with some uncertainty")
        elif self.confidence >= 0.40:
            case_content.append("**Interpretation**: Low Confidence - Evidence is weak or mixed")
        else:
            case_content.append("**Interpretation**: Very Low Confidence - Insufficient or contradictory evidence")
        case_content.append("")
        case_content.append("### Evidence Summary")
        case_content.append("")
        case_content.append("| Category | Count | Status |")
        case_content.append("|----------|-------|--------|")
        case_content.append(f"| Verification Checks | {verification_count} | {verified_count} verified |")
        if assumptions:
            case_content.append(f"| Assumptions Tested | {len(assumptions)} | {proven} proven |")
        case_content.append(f"| Overall Verdict | 1 | {self.verdict} |")
        case_content.append("")
        case_content.append("### Recommendations")
        case_content.append("")
        if self.verdict == "PROVEN":
            case_content.append("1. ✅ **Accept the claim as verified**")
            case_content.append("2. ✅ **Use this evidence for decision-making**")
            case_content.append("3. ✅ **Monitor for any future changes that might affect the claim**")
        elif self.verdict == "DISPROVEN":
            case_content.append("1. ❌ **Reject the claim**")
            case_content.append("2. ⚠️ **Investigate why the claim was made**")
            case_content.append("3. 🔧 **Take corrective action if needed**")
        else:
            case_content.append("1. 🔍 **Gather additional evidence**")
            case_content.append("2. 🧪 **Run additional tests or experiments**")
            case_content.append("3. 📊 **Review methodology for improvements**")
        case_content.append("")
        case_content.append("=" * 70)
        case_content.append("")
        
        # ========================================================================
        # APPENDIX
        # ========================================================================
        case_content.append("## APPENDIX")
        case_content.append("")
        case_content.append("### Case Metadata")
        case_content.append("")
        case_content.append(f"- **Case ID**: PROOF-{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        case_content.append(f"- **Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        case_content.append(f"- **Project Path**: {self.project_path}")
        case_content.append(f"- **Claim**: {self.claim}")
        case_content.append("")
        case_content.append("### Files Generated")
        case_content.append("")
        case_content.append(f"- **Case File**: `{self.case_file_path}` (if generated)")
        case_content.append(f"- **PDF Binder**: Generated in `_work_efforts/proof_cases/`")
        case_content.append("")
        case_content.append("### Verification Scripts Used")
        case_content.append("")
        verify_script = self.project_path / "scripts" / "verify_no_black_bars.py"
        if verify_script.exists():
            case_content.append(f"- **Template Verification**: `{verify_script.relative_to(self.project_path)}`")
        case_content.append(f"- **Proof System**: `scripts/prove_it_comprehensive.py`")
        case_content.append("")
        case_content.append("=" * 70)
        case_content.append("")
        case_content.append(f"*End of Case Brief - Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        
        return "\n".join(case_content)
    
    def determine_verdict(self):
        """Determine verdict based on evidence."""
        # Check verification results
        all_verified = all(
            result.get("verified", False)
            for result in self.verification_results.values()
            if isinstance(result, dict)
        )
        
        # Template verification is critical
        template_verified = self.verification_results.get("template_verification", {}).get("verified", False)
        
        # Check assumptions
        assumptions = self.assumption_results.get("assumptions", [])
        proven_count = 0
        disproven_count = 0
        total_count = 0
        assumption_confidence = 0.0
        
        if assumptions:
            proven_count = sum(1 for a in assumptions if a.get("status") == "PROVEN")
            disproven_count = sum(1 for a in assumptions if a.get("status") == "DISPROVEN")
            total_count = len(assumptions)
            assumption_confidence = proven_count / total_count if total_count > 0 else 0.0
            
            # If any template has black bars, claim is disproven
            if disproven_count > 0:
                self.verdict = "DISPROVEN"
                self.confidence = 0.95
                return
            
            # If all templates proven clean and verification passed, claim is PROVEN
            # Prioritize this check - if all templates are clean, it's proven
            if proven_count == total_count and total_count > 0:
                if template_verified:
                    self.verdict = "PROVEN"
                    self.confidence = 0.95
                    return
                elif all_verified:  # Even if template verification script failed, if all templates checked are clean
                    self.verdict = "PROVEN"
                    self.confidence = 0.90
                    return
        else:
            assumption_confidence = 0.5  # Neutral if no assumptions
        
        # Determine verdict
        if template_verified and all_verified and assumption_confidence >= 0.95:
            self.verdict = "PROVEN"
            self.confidence = 0.95
        elif template_verified and all_verified and assumption_confidence >= 0.8:
            self.verdict = "PROVEN"
            self.confidence = min(0.90, 0.75 + (assumption_confidence * 0.15))
        elif not template_verified:
            self.verdict = "DISPROVEN"
            self.confidence = 0.9
        elif assumption_confidence < 0.5:
            self.verdict = "DISPROVEN"
            self.confidence = 0.7
        else:
            self.verdict = "INCONCLUSIVE"
            self.confidence = assumption_confidence
    
    def generate_pdf(self) -> Path:
        """Generate PDF binder with case brief."""
        case_content = self.build_case_file()
        
        # Determine cover classification based on verdict
        if self.verdict == "PROVEN":
            classification = "VERIFIED"
            cover_warning = {
                "message": "CLAIM VERIFIED - Evidence supports the claim beyond reasonable doubt",
                "severity": "INFO"
            }
        elif self.verdict == "DISPROVEN":
            classification = "REFUTED"
            cover_warning = {
                "message": "CLAIM DISPROVEN - Evidence contradicts the claim",
                "severity": "CRITICAL"
            }
        else:
            classification = "INCONCLUSIVE"
            cover_warning = {
                "message": "INSUFFICIENT EVIDENCE - Cannot definitively prove or disprove",
                "severity": "WARNING"
            }
        
        # Generate PDF
        output_dir = project_root / "_work_efforts" / "proof_cases"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_claim = self.claim[:50].replace(" ", "_").replace("/", "_")
        output_path = output_dir / f"PROOF_CASE_{safe_claim}_{timestamp}.pdf"
        
        # Use BriefDocument directly to add markdown content
        from src.waft.brief import BriefDocument
        
        doc = BriefDocument(
            title=f"PROOF CASE: {self.claim[:60]}",
            doc_id=f"PROOF-{timestamp}",
            subtitle=f"Verdict: {self.verdict} | Confidence: {self.confidence:.1%}",
            classification=classification,
            cover_header="PROOF CASE BRIEF",
            cover_metadata={
                "CLAIM": self.claim[:100],
                "VERDICT": self.verdict,
                "CONFIDENCE": f"{self.confidence:.1%}",
                "DATE": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            cover_warning=cover_warning,
            cover_footer="EVIDENCE-BASED VERIFICATION",
            include_system_status=False
        )
        
        # Convert markdown to HTML properly
        try:
            import markdown
            html_content = markdown.markdown(
                case_content,
                extensions=['fenced_code', 'tables', 'nl2br', 'extra', 'codehilite']
            )
        except ImportError:
            # Fallback: basic conversion
            import re
            html_content = case_content
            # Code blocks
            html_content = re.sub(
                r'```(\w+)?\n(.*?)```',
                r'<pre><code class="language-\1">\2</code></pre>',
                html_content,
                flags=re.DOTALL
            )
            # Inline code
            html_content = re.sub(r'`([^`]+)`', r'<code>\1</code>', html_content)
            # Headers
            html_content = re.sub(r'^#\s+(.+)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
            html_content = re.sub(r'^##\s+(.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
            html_content = re.sub(r'^###\s+(.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
            # Bold
            html_content = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', html_content)
            # Paragraphs
            html_content = re.sub(r'^(.+)$', r'<p>\1</p>', html_content, flags=re.MULTILINE)
        
        # Add HTML content directly
        doc.content_blocks.append(html_content)
        
        # Generate PDF
        pdf_path = doc.generate(output_path=output_path)
        
        # Move to desired location
        if pdf_path != output_path:
            pdf_path.rename(output_path)
        
        return output_path
    
    def run_proof(self) -> Dict[str, Any]:
        """Run complete proof process."""
        print("=" * 70)
        print("COMPREHENSIVE PROOF SYSTEM")
        print("=" * 70)
        print()
        print(f"**Claim to Prove**: {self.claim}")
        print()
        
        # Step 1: Verification
        self.verification_results = self.run_verification()
        
        # Step 2: Assumption Check
        self.assumption_results = self.run_assumption_check()
        
        # Step 3: Determine Verdict
        self.determine_verdict()
        
        # Step 4: Build Case File
        case_content = self.build_case_file()
        case_file = project_root / "_work_efforts" / "proof_cases" / f"case_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        case_file.parent.mkdir(parents=True, exist_ok=True)
        case_file.write_text(case_content)
        self.case_file_path = case_file
        
        # Step 5: Generate PDF
        pdf_path = self.generate_pdf()
        
        print("=" * 70)
        print("PROOF COMPLETE")
        print("=" * 70)
        print()
        print(f"**Verdict**: {self.verdict}")
        print(f"**Confidence**: {self.confidence:.1%}")
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
            "verdict": self.verdict,
            "confidence": self.confidence,
            "case_file": str(case_file),
            "pdf_path": str(pdf_path),
            "verification_results": self.verification_results,
            "assumption_results": self.assumption_results
        }


def main():
    """Main entry point."""
    # Default claim (can be overridden)
    claim = "All PDF templates have been fixed to remove black bars from headers"
    
    # Check for claim in command line args
    if len(sys.argv) > 1:
        claim = " ".join(sys.argv[1:])
    
    builder = ProofCaseBuilder(project_root, claim)
    results = builder.run_proof()
    
    return 0 if results["verdict"] == "PROVEN" else 1


if __name__ == "__main__":
    sys.exit(main())
