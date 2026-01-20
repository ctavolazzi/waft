#!/usr/bin/env python3
"""
SELF-ANALYSIS DEMO - TheGuide Meta-Cognitive Framework

This demonstrates the self-analysis framework with mock LLM responses
that simulate what a real meta-cognitive analysis would produce.

This shows the ARCHITECTURE and DATA FLOW of self-examination.
"""

import sys
import time
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import importlib.util
guide_path = Path(__file__).parent.parent / "src" / "waft" / "pantheon" / "guide.py"
spec = importlib.util.spec_from_file_location("guide", guide_path)
guide_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guide_module)

TheGuide = guide_module.TheGuide
import tempfile

# ============================================================================
# MOCK LLM WITH REALISTIC SELF-ANALYSIS RESPONSES
# ============================================================================

class SelfAnalysisLLM:
    """Mock LLM that provides realistic self-analysis responses."""

    def __init__(self, analysis_type: str):
        self.analysis_type = analysis_type
        self.call_count = 0

    def complete(self, prompt: str) -> str:
        self.call_count += 1

        # Return different responses based on what's being analyzed
        if "performance issues" in prompt.lower() or "code" in prompt.lower():
            return self._code_analysis_response()
        elif "performance bug" in prompt.lower() or "degradation" in prompt.lower():
            return self._performance_diagnosis_response()
        elif "reasoning" in prompt.lower() or "evaluate" in prompt.lower():
            return self._meta_reasoning_response()
        elif "evaluate the quality" in prompt.lower():
            return self._evaluation_response()
        else:
            return "Analysis in progress..."

    def _code_analysis_response(self) -> str:
        return """CODE ANALYSIS - Performance Issues Identified:

**CRITICAL ISSUE 1: Index File Operations**
The `_save_index()` method writes the entire index file on every session save:
```python
self.index_file.write_text(json.dumps(self.index, indent=2))
```

This causes O(n) performance degradation:
- With 100 sessions: ~1.2ms per save
- With 1000 sessions: ~6.4ms per save
- The index grows linearly, so write time grows linearly

**Root Cause**: The index dict grows with every session, but we rewrite the ENTIRE
file each time instead of appending.

**CRITICAL ISSUE 2: JSON Serialization Cost**
Every session save triggers:
1. Read entire index file
2. Parse JSON
3. Modify dict
4. Serialize entire dict to JSON
5. Write entire file

Cost scales with number of sessions stored.

**Proposed Fixes**:
1. Use append-only log instead of rewriting index
2. Batch index updates
3. Use SQLite for O(1) lookups
4. Add index versioning/compaction
5. Cache index in memory, only write periodically

**Performance Impact**: This explains the 411% degradation observed over 1000 sessions."""

    def _performance_diagnosis_response(self) -> str:
        return """PERFORMANCE BUG DIAGNOSIS:

**Root Cause Identified**: Index File Rewriting

The linear performance degradation (411% over 1000 sessions) is caused by:

1. **Index Growth**: Each session adds an entry to `self.index` dict
2. **Full Rewrite**: `_save_index()` rewrites the ENTIRE index file every time
3. **JSON Serialization**: Cost increases with index size
4. **File I/O**: Disk write time grows with file size

**Why Linear Degradation?**
- Session 1: Write 100 bytes → ~1.2ms
- Session 100: Write 10KB → ~1.7ms
- Session 1000: Write 100KB → ~6.4ms

The relationship is linear: O(n) where n = number of sessions.

**Mathematical Model**:
```
time_per_save = base_time + (k * num_sessions)
```
Where k ≈ 0.0005984 ms/session (from experimental data).

**Verification**:
- Observed slope: 0.000598 ms/session
- Predicted at session 1000: 1.245 + (0.598 * 9) = 6.627ms
- Actual at session 1000: 6.370ms
- Error: 4% (excellent fit)

**Fix Priority**: HIGH - This will cause production issues at scale."""

    def _meta_reasoning_response(self) -> str:
        return """META-COGNITIVE SELF-EVALUATION:

**The Evaluation Paradox**:
I (TheGuide) evaluate Client LLM reasoning, but who evaluates MY evaluations?

**Solution: Multi-Level Trust Framework**

1. **Level 0 - Client LLM**: Generates answers
   - No self-evaluation capability
   - Requires external validation

2. **Level 1 - Guide LLM (Me)**: Evaluates client reasoning
   - Uses FVCU+Faithfulness taxonomy
   - Trained on evaluation principles
   - But needs validation too!

3. **Level 2 - Human Oversight**: Validates guide evaluations
   - Reviews quality scores
   - Checks for consistency
   - Provides ground truth

4. **Level 3 - Statistical Validation**: Empirical evidence
   - Correlation with human judgments
   - Consistency across similar problems
   - Calibration curves

**Avoiding Infinite Regress**:
Instead of requiring infinite evaluators, we bootstrap trust through:
- Cross-validation between multiple guides
- Consistency checks (same problem → same evaluation)
- Comparison with human expert evaluations
- Statistical correlation with ground truth

**Self-Evaluation Mechanism**:
I can evaluate my OWN reasoning by:
1. Generating multiple independent evaluations
2. Checking for consistency
3. Comparing against known good evaluations
4. Using held-out validation sets

**Quality Assurance for Quality Assurance**:
The guide's evaluations are trustworthy when:
- High inter-rater reliability with humans
- Consistent scores for similar inputs
- Proper calibration (predicted quality = actual quality)
- Low variance across multiple runs

This creates a self-correcting system where evaluation quality is validated
through empirical performance rather than circular reasoning."""

    def _evaluation_response(self) -> str:
        """Simulate evaluation scores for the meta-analysis."""
        import random
        base_quality = 0.88 + random.random() * 0.10  # 0.88 to 0.98
        return json.dumps({
            "factuality": round(base_quality + random.uniform(-0.05, 0.05), 3),
            "validity": round(base_quality + random.uniform(-0.05, 0.05), 3),
            "coherence": round(base_quality + random.uniform(-0.03, 0.03), 3),
            "utility": round(base_quality + random.uniform(-0.03, 0.03), 3),
            "faithfulness": round(base_quality + random.uniform(-0.05, 0.05), 3),
            "overall": round(base_quality, 3),
            "should_continue": False
        })

# ============================================================================
# SELF-DIAGNOSTIC EXPERIMENTS WITH MOCK LLM
# ============================================================================

def self_diagnostic_1_code_analysis():
    """TheGuide analyzes its own source code."""

    print("\n" + "="*80)
    print("SELF-DIAGNOSTIC 1: TheGuide Analyzes Its Own Source Code")
    print("="*80)

    source_code = guide_path.read_text()

    print("\nSETUP: Creating TheGuide with self-analysis capability...")

    with tempfile.TemporaryDirectory() as tmpdir:
        client_llm = SelfAnalysisLLM("code_analysis")
        guide_llm = SelfAnalysisLLM("code_analysis")

        guide = TheGuide(
            project_path=Path(tmpdir),
            client_llm=client_llm,
            guide_llm_config={"model": "mock"}
        )
        guide.guide_llm = guide_llm

        problem = f"""Analyze the following Python code and identify potential performance issues.

CODE:
{source_code[:5000]}

ANALYSIS TASK:
1. Identify any code patterns that could cause performance degradation over time
2. Look for potential memory leaks or resource accumulation
3. Check for inefficient data structures or algorithms
4. Suggest specific improvements

Focus especially on the _save_session and indexing operations."""

        print(f"\nINPUT:")
        print(f"  Code length: {len(source_code)} characters")
        print(f"  Analyzing first: 5000 characters")
        print(f"  Focus: _save_session and indexing operations")

        start_time = time.time()

        answer, protocol = guide.solve(
            problem_statement=problem,
            max_iterations=3,
            quality_threshold=0.85
        )

        duration = time.time() - start_time

        print(f"\nMETRICS:")
        print(f"  Execution time: {duration:.2f}s")
        print(f"  Iterations: {protocol.iteration_count}")
        print(f"  Quality score: {protocol.quality_score:.3f}")
        print(f"  Client LLM calls: {client_llm.call_count}")
        print(f"  Guide LLM calls: {guide_llm.call_count}")

        print(f"\nTHEGUIDE'S SELF-ANALYSIS:")
        print("  " + "="*76)
        for line in answer.split('\n'):
            print(f"  {line}")
        print("  " + "="*76)

        # Save analysis
        analysis_file = Path("self_analysis_code.txt")
        analysis_file.write_text(f"""SELF-ANALYSIS: TheGuide Examines Its Own Code
Generated: {datetime.now().isoformat()}
Execution time: {duration:.2f}s
Iterations: {protocol.iteration_count}
Quality: {protocol.quality_score:.3f}

FULL ANALYSIS:
{answer}

PROTOCOL DATA:
Session ID: {protocol.session_id}
Reasoning steps: {len(protocol.reasoning_chain)}
Evaluations: {len(protocol.evaluations)}
""")

        print(f"\n📄 Full analysis saved to: {analysis_file}")

        # Check if it found the bug
        found_index_issue = 'index' in answer.lower()
        found_performance = 'performance' in answer.lower() or 'degradation' in answer.lower()
        found_o_n = 'o(n)' in answer.lower() or 'linear' in answer.lower()

        print(f"\nKEY FINDINGS:")
        print(f"  ✅ Identified index operations: {found_index_issue}")
        print(f"  ✅ Identified performance issue: {found_performance}")
        print(f"  ✅ Identified O(n) complexity: {found_o_n}")

        return {
            'success': True,
            'duration': duration,
            'quality': protocol.quality_score,
            'found_index_issue': found_index_issue,
            'found_performance': found_performance,
            'found_o_n': found_o_n,
            'answer_length': len(answer)
        }

def self_diagnostic_2_performance_introspection():
    """TheGuide diagnoses its own performance bug."""

    print("\n" + "="*80)
    print("SELF-DIAGNOSTIC 2: TheGuide Diagnoses Its Own Performance Bug")
    print("="*80)

    with tempfile.TemporaryDirectory() as tmpdir:
        client_llm = SelfAnalysisLLM("performance_diagnosis")
        guide_llm = SelfAnalysisLLM("performance_diagnosis")

        guide = TheGuide(
            project_path=Path(tmpdir),
            client_llm=client_llm,
            guide_llm_config={"model": "mock"}
        )
        guide.guide_llm = guide_llm

        problem = """PERFORMANCE BUG DIAGNOSIS:

I have discovered a performance degradation bug in my own system (TheGuide).

OBSERVED BEHAVIOR:
- Batch 1 (sessions 1-100): 1.245ms per session (802 sess/s)
- Batch 2 (sessions 101-200): 1.729ms per session (578 sess/s)
- Batch 3 (sessions 201-300): 2.183ms per session (458 sess/s)
- Batch 10 (sessions 901-1000): 6.370ms per session (157 sess/s)

Performance degrades by 411% over 1000 sessions.

SYSTEM ARCHITECTURE:
- File-based storage (JSON files)
- Index file that tracks all sessions
- Each session creates 2 files (session + protocol)
- Index is updated after each session

TASK:
1. Diagnose the root cause of this performance degradation
2. Identify which operation is getting slower
3. Propose specific fixes
4. Explain why the degradation is linear

Think step-by-step about what happens as more sessions accumulate."""

        print("\nINPUT:")
        print("  Performance data: 10 batches of 100 sessions each")
        print("  Degradation: 411% over 1000 sessions")
        print("  Pattern: Linear growth")

        start_time = time.time()

        answer, protocol = guide.solve(
            problem_statement=problem,
            max_iterations=5,
            quality_threshold=0.90
        )

        duration = time.time() - start_time

        print(f"\nMETRICS:")
        print(f"  Execution time: {duration:.2f}s")
        print(f"  Iterations: {protocol.iteration_count}")
        print(f"  Quality score: {protocol.quality_score:.3f}")

        print(f"\nTHEGUIDE'S SELF-DIAGNOSIS:")
        print("  " + "="*76)
        for line in answer.split('\n'):
            print(f"  {line}")
        print("  " + "="*76)

        # Save diagnosis
        diagnosis_file = Path("self_diagnosis_performance.txt")
        diagnosis_file.write_text(f"""SELF-DIAGNOSIS: TheGuide Analyzes Its Own Performance Bug
Generated: {datetime.now().isoformat()}
Execution time: {duration:.2f}s
Iterations: {protocol.iteration_count}
Quality: {protocol.quality_score:.3f}

{answer}
""")

        print(f"\n📄 Full diagnosis saved to: {diagnosis_file}")

        # Check findings
        identified_index = 'index' in answer.lower()
        identified_rewrite = 'rewrite' in answer.lower() or 'entire' in answer.lower()
        identified_linear = 'linear' in answer.lower() or 'o(n)' in answer.lower()
        identified_slope = '0.000598' in answer or '0.0005984' in answer

        print(f"\nKEY FINDINGS:")
        print(f"  ✅ Identified index operations: {identified_index}")
        print(f"  ✅ Identified full rewrite issue: {identified_rewrite}")
        print(f"  ✅ Identified linear complexity: {identified_linear}")
        print(f"  ✅ Calculated slope correctly: {identified_slope}")

        return {
            'success': True,
            'duration': duration,
            'quality': protocol.quality_score,
            'identified_index': identified_index,
            'identified_rewrite': identified_rewrite,
            'identified_linear': identified_linear
        }

def self_diagnostic_3_meta_cognitive_loop():
    """TheGuide reasons about its own reasoning."""

    print("\n" + "="*80)
    print("SELF-DIAGNOSTIC 3: TheGuide Reasons About Its Own Reasoning")
    print("="*80)

    with tempfile.TemporaryDirectory() as tmpdir:
        client_llm = SelfAnalysisLLM("meta_reasoning")
        guide_llm = SelfAnalysisLLM("meta_reasoning")

        guide = TheGuide(
            project_path=Path(tmpdir),
            client_llm=client_llm,
            guide_llm_config={"model": "mock"}
        )
        guide.guide_llm = guide_llm

        problem = """META-COGNITIVE ANALYSIS:

I am TheGuide - a meta-cognitive system that evaluates reasoning using FVCU+Faithfulness criteria.

QUESTION: How do I evaluate my own reasoning?

Consider:
1. I use a Guide LLM to evaluate a Client LLM's reasoning
2. But who evaluates the Guide LLM's evaluations?
3. Is there infinite regress?
4. How can I ensure my own evaluations are accurate?

This is a meta-cognitive paradox. Reason about:
- Self-evaluation mechanisms
- Bootstrapping trust in evaluation
- Avoiding circular reasoning
- Quality assurance for quality assurance

How should a meta-cognitive system evaluate itself?"""

        print("\nINPUT:")
        print("  Topic: Meta-cognitive self-evaluation paradox")
        print("  Question: Who evaluates the evaluator?")

        start_time = time.time()

        answer, protocol = guide.solve(
            problem_statement=problem,
            max_iterations=4,
            quality_threshold=0.88
        )

        duration = time.time() - start_time

        print(f"\nMETRICS:")
        print(f"  Execution time: {duration:.2f}s")
        print(f"  Iterations: {protocol.iteration_count}")
        print(f"  Quality score: {protocol.quality_score:.3f}")

        print(f"\nTHEGUIDE'S META-REASONING:")
        print("  " + "="*76)
        for line in answer.split('\n'):
            print(f"  {line}")
        print("  " + "="*76)

        # Save meta-reasoning
        meta_file = Path("self_meta_reasoning.txt")
        meta_file.write_text(f"""SELF-META-REASONING: TheGuide Reasons About Its Own Reasoning
Generated: {datetime.now().isoformat()}
Execution time: {duration:.2f}s
Iterations: {protocol.iteration_count}
Quality: {protocol.quality_score:.3f}

{answer}
""")

        print(f"\n📄 Meta-reasoning saved to: {meta_file}")

        return {
            'success': True,
            'duration': duration,
            'quality': protocol.quality_score
        }

# ============================================================================
# MAIN
# ============================================================================

def run_self_analysis_demo():
    """Run all self-analysis experiments with mock LLM."""

    print("="*80)
    print("SELF-ANALYSIS SUITE - META-COGNITIVE INTROSPECTION DEMO")
    print("="*80)

    print("\nFRAMEWORK:")
    print("  This demonstrates TheGuide's self-examination architecture")
    print("  using mock LLM responses that simulate realistic meta-cognitive analysis.")
    print("\nEXPERIMENTS:")
    print("  1. TheGuide analyzes its own source code")
    print("  2. TheGuide diagnoses its own performance bug")
    print("  3. TheGuide reasons about its own reasoning process")

    results = {}

    # Experiment 1
    results['code_analysis'] = self_diagnostic_1_code_analysis()

    # Experiment 2
    results['performance_diagnosis'] = self_diagnostic_2_performance_introspection()

    # Experiment 3
    results['meta_reasoning'] = self_diagnostic_3_meta_cognitive_loop()

    # Summary
    print("\n" + "="*80)
    print("SELF-ANALYSIS SUMMARY")
    print("="*80)

    successful = sum(1 for r in results.values() if r.get('success'))
    total = len(results)

    print(f"\n✅ Diagnostics completed: {successful}/{total}")

    for name, result in results.items():
        if result.get('success'):
            print(f"\n{name.upper()}:")
            print(f"  Duration: {result['duration']:.2f}s")
            print(f"  Quality: {result['quality']:.3f}")
            if 'found_index_issue' in result:
                print(f"  Found index issue: {result['found_index_issue']}")
                print(f"  Found performance: {result['found_performance']}")
                print(f"  Found O(n): {result['found_o_n']}")

    # Save results
    results_file = Path("self_analysis_demo_results.json")
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n📊 Results saved to: {results_file}")
    print("\n" + "="*80)
    print("META-COGNITIVE SELF-EXAMINATION COMPLETE")
    print("="*80)

    return results

if __name__ == "__main__":
    results = run_self_analysis_demo()
