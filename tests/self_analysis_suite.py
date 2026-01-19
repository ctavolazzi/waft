#!/usr/bin/env python3
"""
SELF-ANALYSIS SUITE - TheGuide Examines Itself

This is meta-cognitive introspection at its finest:
- TheGuide analyzes its own code
- TheGuide diagnoses its own performance bug
- TheGuide reasons about its own behavior
- TheGuide explores its own failure modes

We're literally having the meta-cognitive system perform meta-cognition on itself.
"""

import sys
import time
import json
import tempfile
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import importlib.util
guide_path = Path(__file__).parent.parent / "src" / "waft" / "pantheon" / "guide.py"
spec = importlib.util.spec_from_file_location("guide", guide_path)
guide_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guide_module)

TheGuide = guide_module.TheGuide

# ============================================================================
# SELF-DIAGNOSTIC EXPERIMENTS
# ============================================================================

def self_diagnostic_1_code_analysis():
    """
    EXPERIMENT: TheGuide analyzes its own source code

    We'll give TheGuide its own source code and ask it to analyze it.
    """

    print("\n" + "="*80)
    print("SELF-DIAGNOSTIC 1: TheGuide Analyzes Its Own Source Code")
    print("="*80)

    # Read TheGuide's source code
    source_code = guide_path.read_text()

    # Create a real LLM-backed Guide (using anthropic if available)
    print("\nSETUP: Creating TheGuide instance with real LLM...")

    try:
        # Try to use real LLM
        from litellm import completion

        class RealLLM:
            def __init__(self, model="anthropic/claude-sonnet-4-5-20250929"):
                self.model = model
                self.call_count = 0

            def complete(self, prompt: str) -> str:
                self.call_count += 1
                try:
                    response = completion(
                        model=self.model,
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=2000
                    )
                    return response.choices[0].message.content
                except Exception as e:
                    return f"LLM Error: {e}"

        with tempfile.TemporaryDirectory() as tmpdir:
            client_llm = RealLLM()
            guide = TheGuide(
                project_path=Path(tmpdir),
                client_llm=client_llm,
                guide_llm_config={"model": "anthropic/claude-sonnet-4-5-20250929"}
            )
            guide.guide_llm = RealLLM()

            problem = f"""Analyze the following Python code and identify potential performance issues.

CODE:
{source_code[:5000]}  # First 5000 chars

ANALYSIS TASK:
1. Identify any code patterns that could cause performance degradation over time
2. Look for potential memory leaks or resource accumulation
3. Check for inefficient data structures or algorithms
4. Suggest specific improvements

Focus especially on the _save_session and indexing operations.
"""

            print("\nPROBLEM: Asking TheGuide to analyze its own code...")
            print(f"Code length: {len(source_code)} characters")
            print(f"Analyzing first: {min(5000, len(source_code))} characters")

            start_time = time.time()

            answer, protocol = guide.solve(
                problem_statement=problem,
                max_iterations=3,
                quality_threshold=0.85
            )

            duration = time.time() - start_time

            print(f"\nRESULTS:")
            print(f"  Execution time: {duration:.2f}s")
            print(f"  Iterations: {protocol.iteration_count}")
            print(f"  Quality score: {protocol.quality_score:.3f}")
            print(f"  LLM calls (client): {client_llm.call_count}")
            print(f"  LLM calls (guide): {guide.guide_llm.call_count}")

            print(f"\nTHEGUIDE'S ANALYSIS:")
            print("  " + "="*76)
            print(answer[:1000])  # First 1000 chars
            if len(answer) > 1000:
                print(f"  ... (truncated, total length: {len(answer)} chars)")
            print("  " + "="*76)

            # Save full analysis
            analysis_file = Path("self_analysis_code.txt")
            analysis_file.write_text(f"""
SELF-ANALYSIS: TheGuide Examines Its Own Code
Generated: {datetime.now().isoformat()}
Execution time: {duration:.2f}s
Iterations: {protocol.iteration_count}
Quality: {protocol.quality_score:.3f}

FULL ANALYSIS:
{answer}

PROTOCOL:
Session ID: {protocol.session_id}
Reasoning chain: {len(protocol.reasoning_chain)} steps
Evaluations: {len(protocol.evaluations)}
""")

            print(f"\n📄 Full analysis saved to: {analysis_file}")

            return {
                'success': True,
                'duration': duration,
                'quality': protocol.quality_score,
                'analysis_length': len(answer),
                'found_issues': 'performance' in answer.lower() or 'degradation' in answer.lower()
            }

    except ImportError:
        print("\n⚠️  litellm not available, using mock LLM for demonstration")
        return {'success': False, 'reason': 'no_real_llm'}
    except Exception as e:
        print(f"\n⚠️  Error: {e}")
        import traceback
        traceback.print_exc()
        return {'success': False, 'reason': str(e)}

def self_diagnostic_2_performance_introspection():
    """
    EXPERIMENT: TheGuide diagnoses its own performance degradation

    We'll describe the performance bug we found and ask TheGuide to diagnose it.
    """

    print("\n" + "="*80)
    print("SELF-DIAGNOSTIC 2: TheGuide Diagnoses Its Own Performance Bug")
    print("="*80)

    try:
        from litellm import completion

        class RealLLM:
            def __init__(self, model="anthropic/claude-sonnet-4-5-20250929"):
                self.model = model

            def complete(self, prompt: str) -> str:
                try:
                    response = completion(
                        model=self.model,
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=2000
                    )
                    return response.choices[0].message.content
                except Exception as e:
                    return f"LLM Error: {e}"

        with tempfile.TemporaryDirectory() as tmpdir:
            guide = TheGuide(
                project_path=Path(tmpdir),
                client_llm=RealLLM(),
                guide_llm_config={"model": "anthropic/claude-sonnet-4-5-20250929"}
            )
            guide.guide_llm = RealLLM()

            problem = """PERFORMANCE BUG DIAGNOSIS:

I have discovered a performance degradation bug in my own system (TheGuide).

OBSERVED BEHAVIOR:
- Batch 1 (sessions 1-100): 1.245ms per session (802 sess/s)
- Batch 2 (sessions 101-200): 1.729ms per session (578 sess/s)
- Batch 3 (sessions 201-300): 2.183ms per session (458 sess/s)
- ...
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

Think step-by-step about what happens as more sessions accumulate.
"""

            print("\nPROBLEM: Asking TheGuide to diagnose its own performance bug...")

            start_time = time.time()

            answer, protocol = guide.solve(
                problem_statement=problem,
                max_iterations=5,
                quality_threshold=0.90
            )

            duration = time.time() - start_time

            print(f"\nRESULTS:")
            print(f"  Execution time: {duration:.2f}s")
            print(f"  Iterations: {protocol.iteration_count}")
            print(f"  Quality score: {protocol.quality_score:.3f}")

            print(f"\nTHEGUIDE'S DIAGNOSIS:")
            print("  " + "="*76)
            print(answer[:1500])
            if len(answer) > 1500:
                print(f"  ... (truncated, total length: {len(answer)} chars)")
            print("  " + "="*76)

            # Save diagnosis
            diagnosis_file = Path("self_diagnosis_performance.txt")
            diagnosis_file.write_text(f"""
SELF-DIAGNOSIS: TheGuide Analyzes Its Own Performance Bug
Generated: {datetime.now().isoformat()}
Execution time: {duration:.2f}s
Iterations: {protocol.iteration_count}
Quality: {protocol.quality_score:.3f}

FULL DIAGNOSIS:
{answer}

REASONING CHAIN:
""")

            # Append reasoning chain
            with open(diagnosis_file, 'a') as f:
                for i, step in enumerate(protocol.reasoning_chain, 1):
                    f.write(f"\n--- Iteration {i} ---\n")
                    f.write(f"Instruction: {step.get('instruction', 'N/A')[:200]}\n")
                    f.write(f"Reasoning: {step.get('reasoning_trace', 'N/A')[:200]}\n")

            print(f"\n📄 Full diagnosis saved to: {diagnosis_file}")

            # Check if it identified key issues
            identified_index = 'index' in answer.lower()
            identified_file = 'file' in answer.lower()
            identified_linear = 'linear' in answer.lower() or 'o(n)' in answer.lower()

            print(f"\nKEY FINDINGS:")
            print(f"  Mentioned index operations: {identified_index}")
            print(f"  Mentioned file operations: {identified_file}")
            print(f"  Identified linear complexity: {identified_linear}")

            return {
                'success': True,
                'duration': duration,
                'quality': protocol.quality_score,
                'identified_index': identified_index,
                'identified_file': identified_file,
                'identified_linear': identified_linear
            }

    except ImportError:
        print("\n⚠️  litellm not available")
        return {'success': False}
    except Exception as e:
        print(f"\n⚠️  Error: {e}")
        import traceback
        traceback.print_exc()
        return {'success': False, 'reason': str(e)}

def self_diagnostic_3_meta_cognitive_loop():
    """
    EXPERIMENT: TheGuide reasons about its own reasoning

    Meta-meta-cognition!
    """

    print("\n" + "="*80)
    print("SELF-DIAGNOSTIC 3: TheGuide Reasons About Its Own Reasoning")
    print("="*80)

    try:
        from litellm import completion

        class RealLLM:
            def __init__(self, model="anthropic/claude-sonnet-4-5-20250929"):
                self.model = model

            def complete(self, prompt: str) -> str:
                try:
                    response = completion(
                        model=self.model,
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=1500
                    )
                    return response.choices[0].message.content
                except Exception as e:
                    return f"LLM Error: {e}"

        with tempfile.TemporaryDirectory() as tmpdir:
            guide = TheGuide(
                project_path=Path(tmpdir),
                client_llm=RealLLM(),
                guide_llm_config={"model": "anthropic/claude-sonnet-4-5-20250929"}
            )
            guide.guide_llm = RealLLM()

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

How should a meta-cognitive system evaluate itself?
"""

            print("\nPROBLEM: Asking TheGuide to reason about its own reasoning process...")

            start_time = time.time()

            answer, protocol = guide.solve(
                problem_statement=problem,
                max_iterations=4,
                quality_threshold=0.88
            )

            duration = time.time() - start_time

            print(f"\nRESULTS:")
            print(f"  Execution time: {duration:.2f}s")
            print(f"  Iterations: {protocol.iteration_count}")
            print(f"  Quality score: {protocol.quality_score:.3f}")

            print(f"\nTHEGUIDE'S META-REASONING:")
            print("  " + "="*76)
            print(answer)
            print("  " + "="*76)

            # Save meta-reasoning
            meta_file = Path("self_meta_reasoning.txt")
            meta_file.write_text(f"""
SELF-META-REASONING: TheGuide Reasons About Its Own Reasoning
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

    except ImportError:
        print("\n⚠️  litellm not available")
        return {'success': False}
    except Exception as e:
        print(f"\n⚠️  Error: {e}")
        return {'success': False, 'reason': str(e)}

# ============================================================================
# MAIN
# ============================================================================

def run_self_analysis():
    """Run all self-analysis experiments."""

    print("="*80)
    print("SELF-ANALYSIS SUITE")
    print("TheGuide Examines Itself - Meta-Cognitive Introspection")
    print("="*80)

    print("\nMETHODOLOGY:")
    print("  Using TheGuide's own meta-cognitive capabilities to:")
    print("  1. Analyze its own source code")
    print("  2. Diagnose its own performance bug")
    print("  3. Reason about its own reasoning process")

    results = {}

    # Self-Diagnostic 1
    result = self_diagnostic_1_code_analysis()
    results['code_analysis'] = result

    # Self-Diagnostic 2
    result = self_diagnostic_2_performance_introspection()
    results['performance_diagnosis'] = result

    # Self-Diagnostic 3
    result = self_diagnostic_3_meta_cognitive_loop()
    results['meta_reasoning'] = result

    # Summary
    print("\n" + "="*80)
    print("SELF-ANALYSIS SUMMARY")
    print("="*80)

    successful = sum(1 for r in results.values() if r.get('success'))
    total = len(results)

    print(f"\nDiagnostics run: {total}")
    print(f"Successful: {successful}")

    for name, result in results.items():
        if result.get('success'):
            print(f"\n{name}: ✅ SUCCESS")
            if 'duration' in result:
                print(f"  Duration: {result['duration']:.2f}s")
            if 'quality' in result:
                print(f"  Quality: {result['quality']:.3f}")
        else:
            reason = result.get('reason', 'unknown')
            print(f"\n{name}: ⚠️  {reason}")

    # Save results
    results_file = Path("self_analysis_results.json")
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n📊 Results saved to: {results_file}")
    print("\n" + "="*80)

    return results

if __name__ == "__main__":
    results = run_self_analysis()
