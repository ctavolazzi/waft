#!/usr/bin/env python3
"""
Test Batch with Karmic Wager

Runs comprehensive test suite with a karmic wager on the hypothesis that
WAFT's self-testing tools work correctly.
"""

import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.waft.evolution.latex_generator import generate_latex
from src.waft.evolution.scientific_pdf_generator import (
    ScientificPDFGenerator,
    generate_scientific_pdf,
)
from src.waft.karmic_wager import KarmicWagerSystem, wager_on_hypothesis


def run_test_batch():
    """Run comprehensive test batch with karmic wager."""
    print("=" * 70)
    print("🎲 WAFT Self-Testing Batch with Karmic Wager")
    print("=" * 70)
    print()

    batch_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"📋 Batch ID: {batch_id}")
    print()

    # Initialize wager system
    wager_system = KarmicWagerSystem(project_path=project_root)

    # Place karmic wager
    print("🎲 Placing Karmic Wager...")
    hypothesis_statement = "WAFT's self-testing tools successfully validate all components and provide actionable quality insights"

    try:
        wager = wager_on_hypothesis(
            wager_system=wager_system,
            hypothesis=hypothesis_statement,
            karma_amount=100.0,
            prediction=True,  # We predict it will be confirmed
            odds=2.0,
        )
        print(f"   ✅ Wager placed: {wager.wager_id}")
        print("   💎 Karma wagered: 100.0")
        print("   📊 Odds: 2.0")
        print()
    except Exception as e:
        print(f"   ⚠️  Wager system error: {e}")
        print("   (Continuing without wager)")
        wager = None
        print()

    # Test results tracking
    test_results = {
        "batch_id": batch_id,
        "timestamp": datetime.now().isoformat(),
        "wager_id": wager.wager_id if wager else None,
        "tests": {},
    }

    # Test 1: Project Verification
    print("1️⃣ Testing Project Verification...")
    try:
        import subprocess

        result = subprocess.run(
            ["waft", "verify"], capture_output=True, text=True, cwd=project_root
        )

        if result.returncode == 0 and "valid" in result.stdout.lower():
            test_results["tests"]["project_verification"] = {
                "status": "PASSED",
                "details": "Project structure valid",
            }
            print("   ✅ PASSED: Project structure valid")
        else:
            test_results["tests"]["project_verification"] = {
                "status": "FAILED",
                "details": result.stdout,
            }
            print("   ❌ FAILED")
    except Exception as e:
        test_results["tests"]["project_verification"] = {"status": "ERROR", "details": str(e)}
        print(f"   ❌ ERROR: {e}")
    print()

    # Test 2: LaTeX Generator
    print("2️⃣ Testing LaTeX Generator...")
    try:
        test_content = """# Batch Test Document

This is a test document for batch verification.

## Features

- LaTeX generation
- Character escaping
- Integration testing
"""
        latex_path = generate_latex(
            content=test_content,
            title="Batch Test Document",
            document_class="article",
            style="clinical_standard",
            compile_pdf=False,
        )

        if latex_path.exists():
            content = latex_path.read_text()
            checks = {
                "documentclass": "\\documentclass" in content,
                "begin_document": "\\begin{document}" in content,
                "end_document": "\\end{document}" in content,
                "title": "Batch Test Document" in content,
            }

            all_passed = all(checks.values())
            test_results["tests"]["latex_generator"] = {
                "status": "PASSED" if all_passed else "FAILED",
                "details": checks,
            }

            if all_passed:
                print("   ✅ PASSED: All LaTeX checks passed")
            else:
                print(f"   ❌ FAILED: {[k for k, v in checks.items() if not v]}")
        else:
            test_results["tests"]["latex_generator"] = {
                "status": "FAILED",
                "details": "File not created",
            }
            print("   ❌ FAILED: File not created")
    except Exception as e:
        test_results["tests"]["latex_generator"] = {"status": "ERROR", "details": str(e)}
        print(f"   ❌ ERROR: {e}")
    print()

    # Test 3: Self-Examination with ScientificPDFGenerator
    print("3️⃣ Testing Self-Examination...")
    try:
        content = """# LaTeX Generator Feature

## Introduction

This document describes the LaTeX generator module developed for WAFT.

## Methodology

The LaTeX generator was developed using WAFT's own tools and frameworks.

## Results

All tests passed successfully.

## Conclusion

The LaTeX generator is functional and ready for use.
"""

        generator = ScientificPDFGenerator.from_content(
            content=content, title="Batch Self-Examination Test", scientific_mode=True
        )

        # Start Study Gym session
        challenge_config = {
            "name": "Batch Self-Examination Test",
            "objective": "Verify self-examination works in batch mode",
            "type": "batch_test",
        }
        generator.study_gym.start_session(challenge_config)

        # Analyze quality
        analysis = generator.analyze_quality()
        quality_score = sum(analysis["scores"].values()) / max(len(analysis["scores"]), 1)

        # Test hypothesis
        result = generator.test_hypothesis(
            statement=hypothesis_statement,
            reasoning="Comprehensive batch testing validates all components",
            test_plan="Run full test suite and verify all tests pass",
            wager_karma=100.0 if wager else None,
        )

        test_results["tests"]["self_examination"] = {
            "status": "PASSED" if result.get("confirmed", False) else "FAILED",
            "quality_score": quality_score,
            "hypothesis_confirmed": result.get("confirmed", False),
            "details": analysis,
        }

        if result.get("confirmed", False):
            print(f"   ✅ PASSED: Quality score {quality_score:.2f}, Hypothesis confirmed")
        else:
            print(f"   ❌ FAILED: Quality score {quality_score:.2f}, Hypothesis not confirmed")
    except Exception as e:
        test_results["tests"]["self_examination"] = {"status": "ERROR", "details": str(e)}
        print(f"   ❌ ERROR: {e}")
        import traceback

        traceback.print_exc()
    print()

    # Test 4: Generate PDF using WAFT tools
    print("4️⃣ Testing PDF Generation...")
    try:
        output_dir = project_root / "_work_efforts" / "one_pagers"
        output_dir.mkdir(parents=True, exist_ok=True)

        pdf_path = output_dir / f"Batch_Test_{batch_id}.pdf"

        pdf_path = generate_scientific_pdf(
            content=content,
            title=f"Batch Test Report {batch_id}",
            output_path=pdf_path,
            style="clinical_standard",
            scientific_mode=True,
            open_pdf=False,
        )

        if pdf_path.exists():
            test_results["tests"]["pdf_generation"] = {
                "status": "PASSED",
                "details": f"PDF generated: {pdf_path}",
            }
            print(f"   ✅ PASSED: PDF generated at {pdf_path}")
        else:
            test_results["tests"]["pdf_generation"] = {
                "status": "FAILED",
                "details": "PDF file not created",
            }
            print("   ❌ FAILED: PDF not created")
    except Exception as e:
        test_results["tests"]["pdf_generation"] = {"status": "ERROR", "details": str(e)}
        print(f"   ❌ ERROR: {e}")
    print()

    # Calculate overall results
    all_tests = test_results["tests"]
    passed = sum(1 for t in all_tests.values() if t.get("status") == "PASSED")
    total = len(all_tests)
    success_rate = (passed / total * 100) if total > 0 else 0

    print("=" * 70)
    print("📊 Batch Test Results Summary")
    print("=" * 70)
    print(f"✅ Passed: {passed}/{total} ({success_rate:.1f}%)")
    print(f"❌ Failed: {sum(1 for t in all_tests.values() if t.get('status') == 'FAILED')}")
    print(f"⚠️  Errors: {sum(1 for t in all_tests.values() if t.get('status') == 'ERROR')}")
    print()

    # Check wager outcome
    if wager:
        hypothesis_confirmed = (
            test_results["tests"].get("self_examination", {}).get("hypothesis_confirmed", False)
        )
        if hypothesis_confirmed:
            print("🎲 Wager Outcome: ✅ WON")
            print("   Hypothesis confirmed - wager successful!")
        else:
            print("🎲 Wager Outcome: ❌ LOST")
            print("   Hypothesis not confirmed - wager lost")
        print()

    # Save results
    results_file = project_root / "_work_efforts" / f"batch_test_results_{batch_id}.json"
    import json

    with open(results_file, "w") as f:
        json.dump(test_results, f, indent=2)
    print(f"💾 Results saved: {results_file}")
    print()

    # Final verdict
    if passed == total:
        print("=" * 70)
        print("✅ ALL TESTS PASSED - BATCH VERIFICATION SUCCESSFUL")
        print("=" * 70)
        return True
    else:
        print("=" * 70)
        print("⚠️  SOME TESTS FAILED - REVIEW REQUIRED")
        print("=" * 70)
        return False


if __name__ == "__main__":
    success = run_test_batch()
    sys.exit(0 if success else 1)
