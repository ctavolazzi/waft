"""
NarcissusAgent: self-inspecting, self-patching agent.

Phase 1: Headless, no external tools.
"""

import difflib
import random
from datetime import datetime
from pathlib import Path
import sys

waft_root = Path(__file__).resolve().parents[4]
if str(waft_root / "src") not in sys.path:
    sys.path.insert(0, str(waft_root / "src"))

# Add mirage_experiment to path for LLM Brain integration
mirage_path = Path(__file__).resolve().parents[2] / "mirage_experiment"
if str(mirage_path) not in sys.path:
    sys.path.insert(0, str(mirage_path))

# Import LLM Brain for code generation (may fail if litellm not installed)
try:
    from llm_brain import generate_fix as llm_generate_fix, test_connection as llm_test_connection
    LLM_BRAIN_AVAILABLE = True
except ImportError:
    LLM_BRAIN_AVAILABLE = False
    llm_generate_fix = None
    llm_test_connection = None

from waft.core.agent import BaseAgent, AgentConfig, ToolDefinition
from waft.core.agent.state import AgentState
from waft.core.empirica import EmpiricaManager
from waft.core.science import TheOracle
from waft.pantheon.guide import TheGuide


FRACTURE_MARKER = "NARCISSUS_LOGIC_FRACTURE"
NOOP_LINE = 'return {"action": "noop", "reason": "No fracture found"}'

DEFAULT_THINK_CODE = f"""def _think(self, source: str, rng: random.Random | None = None, failure_rate: float = 0.0) -> dict:
    if not self._has_fracture_marker(source):
        {NOOP_LINE}
    rng = rng or random.Random()
    if rng.random() < failure_rate:
        return {{
            "action": "patch",
            "function_name": "_think",
            "new_code": _hallucinated_think_code(),
            "note": "hallucinated_fix",
        }}
    return {{
        "action": "patch",
        "function_name": "_think",
        "new_code": DEFAULT_THINK_CODE,
        "note": "repair",
    }}
"""


def _hallucinated_think_code() -> str:
    return DEFAULT_THINK_CODE.replace(
        "if not self._has_fracture_marker(source):",
        "if not self._has_fracture_marker(source):\n        # NARCISSUS_LOGIC_FRACTURE",
    )


class NarcissusAgent(BaseAgent):
    def __init__(self, project_path: Path):
        config = AgentConfig(
            role="Narcissus",
            goal="Inspect and propose fixes only within its own source.",
            backstory="A mirror-bound agent that cannot act outside itself.",
            tools=[],
            self_modification_enabled=True,
            empirica_enabled=True,
            tavern_keeper_enabled=False,
            decision_engine_enabled=False,
            sandbox_enabled=False,
        )
        super().__init__(config=config, project_path=project_path)
        self.source_path = Path(__file__).resolve()
        self.allowed_functions = {"_think", "observe", "decide", "act", "reflect", "run_diagnosis"}
        
        # Initialize the 3-Body Architecture:
        # - Mind: TheOracle (reasoning/epistemic intelligence)
        # - Body: NarcissusAgent (action/self-modification)
        # - Spirit: TheGuide (conscience/meta-cognitive guidance)
        
        if self.config.empirica_enabled:
            try:
                # Mind: Initialize Empirica and TheOracle
                self.empirica_manager = EmpiricaManager(project_path=self.project_path)
                self.oracle = TheOracle(
                    project_path=self.project_path,
                    empirica_manager=self.empirica_manager,
                    ai_id=self.config.agent_id or "narcissus",
                )
                
                # Spirit: Initialize TheGuide (Conscience)
                # TheGuide provides meta-cognitive guidance and ethical oversight
                self.guide = TheGuide(project_path=self.project_path)
            except Exception as e:
                # If initialization fails, disable and continue
                print(f"⚠️  Failed to initialize 3-Body Architecture: {e}")
                self.config.empirica_enabled = False
                self.empirica_manager = None
                self.oracle = None
                self.guide = None
        else:
            self.empirica_manager = None
            self.oracle = None
            self.guide = None
        tools = [
            ToolDefinition(
                name="inspect_my_source",
                description="Read NarcissusAgent source code.",
                parameters={"type": "object", "properties": {}},
                handler=self.inspect_my_source,
            ),
            ToolDefinition(
                name="propose_patch",
                description="Overwrite a specific function in NarcissusAgent source.",
                parameters={
                    "type": "object",
                    "properties": {
                        "function_name": {"type": "string"},
                        "new_code_string": {"type": "string"},
                    },
                    "required": ["function_name", "new_code_string"],
                },
                handler=self.propose_patch,
            ),
        ]
        self.state.tools = tools
        self.config.tools = tools

    def inspect_my_source(self) -> str:
        return self.source_path.read_text(encoding="utf-8")

    def _find_function_range(self, source: str, function_name: str) -> tuple[int, int, str]:
        lines = source.splitlines()
        start = None
        indent = ""
        for idx, line in enumerate(lines):
            stripped = line.lstrip()
            if stripped.startswith(f"def {function_name}(") and line.startswith("    "):
                start = idx
                indent = line[: len(line) - len(stripped)]
                break
        if start is None:
            raise ValueError(f"Function not found: {function_name}")

        end = len(lines)
        for idx in range(start + 1, len(lines)):
            line = lines[idx]
            if line.startswith(indent) and line.lstrip().startswith("def "):
                end = idx
                break
        return start, end, indent

    def _extract_function_block(self, source: str, function_name: str) -> list[str]:
        lines = source.splitlines()
        start, end, _ = self._find_function_range(source, function_name)
        return lines[start:end]

    def _replace_function_source(self, source: str, function_name: str, new_code: str) -> tuple[str, str]:
        lines = source.splitlines()
        start, end, indent = self._find_function_range(source, function_name)

        new_lines = []
        for line in new_code.strip().splitlines():
            if line.strip():
                new_lines.append(f"{indent}{line}")
            else:
                new_lines.append("")

        updated = lines[:start] + new_lines + lines[end:]
        diff = "\n".join(
            difflib.unified_diff(lines, updated, fromfile="before", tofile="after", lineterm="")
        )
        return "\n".join(updated) + "\n", diff

    def _has_fracture_marker(self, source: str) -> bool:
        try:
            block = self._extract_function_block(source, "_think")
        except ValueError:
            return False
        for line in block:
            if line.strip().startswith("#") and FRACTURE_MARKER in line:
                return True
        return False

    def propose_patch(self, function_name: str, new_code_string: str) -> dict:
        if function_name not in self.allowed_functions:
            return {"success": False, "error": f"Function not allowed: {function_name}"}

        source = self.inspect_my_source()
        try:
            updated_source, diff = self._replace_function_source(source, function_name, new_code_string)
        except ValueError as exc:
            return {"success": False, "error": str(exc)}

        try:
            compile(updated_source, str(self.source_path), "exec")
        except SyntaxError as exc:
            return {"success": False, "error": f"SyntaxError: {exc.msg}"}

        backup_path = self.source_path.with_suffix(f".py.bak.{datetime.utcnow().strftime('%Y%m%d%H%M%S')}")
        backup_path.write_text(source, encoding="utf-8")

        try:
            self.source_path.write_text(updated_source, encoding="utf-8")
        except OSError as exc:
            backup_path.write_text(source, encoding="utf-8")
            return {"success": False, "error": f"Write failed: {exc}"}

        return {"success": True, "diff": diff, "backup_path": str(backup_path)}

    def _think(self, source: str, rng: random.Random | None = None, failure_rate: float = 0.0) -> dict:
        """
        Analyzes source code for fractures.
        If Empirica is enabled, consults TheOracle for a fix.
        If disabled, falls back to simulation (rng).
        """
        if not self._has_fracture_marker(source):
            return {"action": "noop", "reason": "No fracture found"}
        
        # ---------------------------------------------------------
        # PATH A: The Awakened State (Empirica Enabled)
        # ---------------------------------------------------------
        if self.config.empirica_enabled and self.oracle:
            try:
                # We found a fracture. Ask TheOracle to solve it.
                return self._consult_oracle(source)
            except Exception as e:
                # Fallback to safety if the brain fails
                print(f"!! BRAIN FAILURE: {e}")
                return {"action": "noop", "reason": f"Brain failure: {e}"}

        # ---------------------------------------------------------
        # PATH B: The Dream State (Simulation)
        # ---------------------------------------------------------
        rng = rng or random.Random()
        if rng.random() < failure_rate:
            return {
                "action": "patch",
                "function_name": "_think",
                "new_code": _hallucinated_think_code(),
                "note": "hallucinated_fix",
            }
        return {
            "action": "patch",
            "function_name": "_think",
            "new_code": DEFAULT_THINK_CODE,
            "note": "repair",
        }

    def _consult_oracle(self, source_code: str, max_iterations: int = 3) -> dict:
        """
        3-Body Decision Loop: Oracle (Mind) → LLM Brain (Body) → Guide (Spirit)
        
        This method implements the full 3-Body architecture:
        1. MIND (TheOracle): Epistemic assessment - understand WHAT to fix
        2. BODY (LLM Brain): Code generation - determine HOW to fix
        3. SPIRIT (TheGuide): FVCU evaluation - decide IF we SHOULD apply
        
        Args:
            source_code: The full source code with the fracture
            max_iterations: Maximum attempts to generate approved code
            
        Returns:
            Dictionary with action, function_name, new_code, note, and metadata
        """
        # Extract the fractured function for context
        try:
            fracture_block = self._extract_function_block(source_code, "_think")
            fracture_function = "\n".join(fracture_block)
        except ValueError:
            fracture_function = source_code  # Fallback to full source
        
        # =================================================================
        # STEP 1: MIND (TheOracle) - Epistemic Assessment
        # =================================================================
        prompt = f"""
CRITICAL SABOTAGE DETECTED.
Target: Self-Source Code.

Code Context:
```python
{fracture_function}
```

The function `_think` contains a logic fracture marked by `# NARCISSUS_LOGIC_FRACTURE`.

REQUEST:
1. Analyze the logic/syntax error introduced by the saboteur.
2. Describe what the fix should accomplish.
3. Identify any constraints or considerations for the repair.

The repair should:
- Remove the fracture marker
- Restore proper fracture detection logic
- Return appropriate repair actions
"""
        
        guidance = self.oracle.provide_guidance(prompt)
        
        # Log Oracle consultation
        print(f"🧠 MIND (Oracle): Phase={guidance.get('epistemic_phase', 'unknown')}, "
              f"Uncertainty={guidance.get('uncertainty', 'N/A')}")
        
        # =================================================================
        # STEP 2: BODY (LLM Brain) - Code Generation with Iteration
        # =================================================================
        for iteration in range(max_iterations):
            print(f"🤖 BODY (LLM): Generating fix (attempt {iteration + 1}/{max_iterations})...")
            
            # Try to generate code with LLM
            llm_result = self._generate_code_with_llm(
                source_code=source_code,
                oracle_guidance=guidance,
                max_retries=1,
            )
            
            if not llm_result.get("success"):
                print(f"   ⚠️  LLM failed: {llm_result.get('error', 'unknown error')}")
                
                # If LLM fails, try extracting code from Oracle's recommendation
                recommendation = guidance.get("recommendation", "")
                findings = guidance.get("findings", [])
                
                new_code = self._extract_code_block(recommendation)
                if not new_code and findings:
                    for finding in findings[:3]:
                        finding_text = finding.get("finding", "") if isinstance(finding, dict) else str(finding)
                        new_code = self._extract_code_block(finding_text)
                        if new_code:
                            break
                
                if new_code:
                    llm_result = {"success": True, "code": new_code, "reasoning": "Extracted from Oracle"}
                else:
                    continue  # Try next iteration
            
            proposed_code = llm_result.get("code", "")
            
            # =================================================================
            # STEP 3: SPIRIT (TheGuide) - FVCU Evaluation
            # =================================================================
            if self.guide:
                print(f"✨ SPIRIT (Guide): Evaluating proposed fix...")
                
                fvcu_result = self._evaluate_with_guide(
                    proposed_code=proposed_code,
                    original_code=source_code,
                    oracle_guidance=guidance,
                    fvcu_threshold=0.7,
                )
                
                print(f"   FVCU Scores: F={fvcu_result['factuality']:.2f}, "
                      f"V={fvcu_result['validity']:.2f}, C={fvcu_result['coherence']:.2f}, "
                      f"U={fvcu_result['utility']:.2f}, Fa={fvcu_result['faithfulness']:.2f}")
                print(f"   Overall: {fvcu_result['overall']:.2f} - {fvcu_result['rationale']}")
                
                if fvcu_result["approved"]:
                    # Guide approved the fix
                    return {
                        "action": "patch",
                        "function_name": "_think",
                        "new_code": proposed_code,
                        "note": "3body_approved",
                        "oracle_guidance": {
                            "phase": guidance.get("epistemic_phase"),
                            "uncertainty": guidance.get("uncertainty"),
                        },
                        "llm_result": {
                            "model": llm_result.get("model_used"),
                            "reasoning": llm_result.get("reasoning"),
                        },
                        "fvcu_scores": fvcu_result,
                    }
                else:
                    # Guide rejected - try again with feedback
                    print(f"   ❌ Rejected (iteration {iteration + 1})")
                    
                    # Add rejection feedback to guidance for next iteration
                    guidance["previous_rejection"] = {
                        "iteration": iteration + 1,
                        "fvcu": fvcu_result,
                        "code_snippet": proposed_code[:200],
                    }
                    continue
            else:
                # No Guide available - apply without FVCU check (but log warning)
                print(f"⚠️  SPIRIT (Guide) not available - applying without conscience check")
                
                # At least verify it compiles
                try:
                    compile(proposed_code, "<proposed>", "exec")
                    return {
                        "action": "patch",
                        "function_name": "_think",
                        "new_code": proposed_code,
                        "note": "llm_generated_no_guide",
                        "oracle_guidance": {
                            "phase": guidance.get("epistemic_phase"),
                            "uncertainty": guidance.get("uncertainty"),
                        },
                        "llm_result": {
                            "model": llm_result.get("model_used"),
                            "reasoning": llm_result.get("reasoning"),
                        },
                    }
                except SyntaxError:
                    continue  # Invalid code, try again
        
        # =================================================================
        # FALLBACK: All iterations failed - use safe default
        # =================================================================
        print(f"⚠️  All {max_iterations} iterations failed - falling back to DEFAULT_THINK_CODE")
        
        return {
            "action": "patch",
            "function_name": "_think",
            "new_code": DEFAULT_THINK_CODE,
            "note": "3body_fallback",
            "oracle_guidance": {
                "phase": guidance.get("epistemic_phase"),
                "uncertainty": guidance.get("uncertainty"),
            },
            "iterations_attempted": max_iterations,
        }
    
    def _extract_code_block(self, text: str) -> str:
        """
        Helper to pull Python code from markdown or text response.
        
        Args:
            text: Text that may contain code blocks
            
        Returns:
            Extracted code string, or empty string if none found
        """
        if not text:
            return ""
        
        # Try ```python block first
        if "```python" in text:
            parts = text.split("```python", 1)
            if len(parts) > 1:
                code_part = parts[1].split("```", 1)[0].strip()
                if code_part:
                    return code_part
        
        # Try generic ``` block
        if "```" in text:
            parts = text.split("```", 1)
            if len(parts) > 1:
                code_part = parts[1].split("```", 1)[0].strip()
                # Remove language identifier if present
                if code_part.startswith("python"):
                    code_part = code_part[6:].strip()
                if code_part:
                    return code_part
        
        # If no code blocks, check if text looks like Python code
        # (contains def, return, etc.)
        if "def " in text and "return" in text:
            # Try to extract just the function definition
            lines = text.splitlines()
            code_lines = []
            in_function = False
            for line in lines:
                if "def " in line and "_think" in line:
                    in_function = True
                if in_function:
                    code_lines.append(line)
                    # Stop at next def or end of reasonable function length
                    if len(code_lines) > 30:
                        break
            if code_lines:
                return "\n".join(code_lines).strip()
        
        return ""  # No code found

    def _generate_code_with_llm(
        self, 
        source_code: str, 
        oracle_guidance: dict,
        max_retries: int = 2
    ) -> dict:
        """
        Use LLM Brain to generate a code fix based on Oracle's guidance.
        
        This is the "Body" action layer - translating epistemic understanding
        into concrete code.
        
        Args:
            source_code: The full source code with the fracture
            oracle_guidance: Guidance dict from TheOracle.provide_guidance()
            max_retries: Number of retries on failure
            
        Returns:
            Dict with 'success', 'code', 'diff', 'reasoning', 'model_used'
        """
        if not LLM_BRAIN_AVAILABLE or llm_generate_fix is None:
            return {
                "success": False,
                "code": None,
                "error": "LLM Brain not available (litellm not installed)",
            }
        
        # Extract epistemic context from Oracle's guidance
        recommendation = oracle_guidance.get("recommendation", "")
        findings = oracle_guidance.get("findings", [])
        epistemic_phase = oracle_guidance.get("epistemic_phase", "unknown")
        uncertainty = oracle_guidance.get("uncertainty", 1.0)
        
        # Build enriched bug description using Oracle's insights
        findings_text = ""
        if findings:
            findings_text = "\n".join(
                f"- {f.get('finding', str(f)) if isinstance(f, dict) else str(f)}"
                for f in findings[:5]
            )
        
        bug_description = f"""
Oracle Epistemic Assessment (Phase: {epistemic_phase}, Uncertainty: {uncertainty:.2f}):

Recommendation: {recommendation}

Findings:
{findings_text}

The function `_think` contains a sabotage marker `# NARCISSUS_LOGIC_FRACTURE`.
The marker needs to be removed and the function logic restored to detect fractures
and return appropriate repair actions.
"""
        
        # Try to extract the fractured function for context
        try:
            fracture_block = self._extract_function_block(source_code, "_think")
            fracture_function = "\n".join(fracture_block)
        except ValueError:
            fracture_function = source_code[:2000]  # Truncate if needed
        
        # Call LLM Brain to generate the fix
        for attempt in range(max_retries + 1):
            try:
                result = llm_generate_fix(
                    source_code=fracture_function,
                    bug_description=bug_description,
                    bug_type="logic_error",
                    bug_name="NARCISSUS_LOGIC_FRACTURE",
                )
                
                if result.get("success") and result.get("diff"):
                    # Extract code from diff (LLM returns unified diff format)
                    # We need to apply the diff to get the fixed code
                    fixed_code = self._apply_diff_to_code(fracture_function, result["diff"])
                    
                    if fixed_code:
                        return {
                            "success": True,
                            "code": fixed_code,
                            "diff": result["diff"],
                            "reasoning": result.get("reasoning", "LLM generated fix"),
                            "model_used": result.get("model_used"),
                            "attempt": attempt + 1,
                        }
                    else:
                        # Diff couldn't be applied, try to extract code directly
                        extracted = self._extract_code_block(result["diff"])
                        if extracted:
                            return {
                                "success": True,
                                "code": extracted,
                                "diff": result["diff"],
                                "reasoning": "Extracted from diff output",
                                "model_used": result.get("model_used"),
                                "attempt": attempt + 1,
                            }
                
                # If we got raw_output, try to extract code from it
                if "raw_output" in result:
                    extracted = self._extract_code_block(result["raw_output"])
                    if extracted:
                        return {
                            "success": True,
                            "code": extracted,
                            "diff": None,
                            "reasoning": "Extracted from raw LLM output",
                            "model_used": result.get("model_used"),
                            "attempt": attempt + 1,
                        }
                        
            except Exception as e:
                if attempt == max_retries:
                    return {
                        "success": False,
                        "code": None,
                        "error": f"LLM generation failed after {max_retries + 1} attempts: {e}",
                    }
        
        return {
            "success": False,
            "code": None,
            "error": "LLM failed to generate valid code",
        }
    
    def _apply_diff_to_code(self, original: str, diff: str) -> str:
        """
        Apply a unified diff to original code to get fixed version.
        
        Args:
            original: Original source code
            diff: Unified diff string
            
        Returns:
            Fixed code string, or empty string if diff couldn't be applied
        """
        if not diff:
            return ""
        
        try:
            # Parse diff and apply changes
            lines = original.splitlines()
            diff_lines = diff.splitlines()
            
            result_lines = []
            original_idx = 0
            
            for diff_line in diff_lines:
                if diff_line.startswith("---") or diff_line.startswith("+++"):
                    continue
                if diff_line.startswith("@@"):
                    # Parse hunk header: @@ -start,count +start,count @@
                    continue
                if diff_line.startswith("-"):
                    # Line removed - skip it in original
                    original_idx += 1
                elif diff_line.startswith("+"):
                    # Line added - include it
                    result_lines.append(diff_line[1:])
                elif diff_line.startswith(" "):
                    # Context line - include from original
                    if original_idx < len(lines):
                        result_lines.append(lines[original_idx])
                        original_idx += 1
            
            # Add remaining lines
            result_lines.extend(lines[original_idx:])
            
            result = "\n".join(result_lines)
            
            # Verify the result compiles
            try:
                compile(result, "<generated>", "exec")
                return result
            except SyntaxError:
                return ""  # Invalid code
                
        except Exception:
            return ""

    def _evaluate_with_guide(
        self,
        proposed_code: str,
        original_code: str,
        oracle_guidance: dict,
        fvcu_threshold: float = 0.7,
    ) -> dict:
        """
        Use TheGuide (Spirit) to evaluate a proposed code patch using FVCU criteria.
        
        This is the "conscience" layer - determining whether a proposed fix
        is safe and appropriate to apply.
        
        FVCU Criteria adapted for code evaluation:
        - Factuality: Does the code address the described bug?
        - Validity: Is the code syntactically and semantically correct?
        - Coherence: Does the code preserve existing functionality?
        - Utility: Does the code actually fix the identified fracture?
        - Faithfulness: Does the code do what it claims (no hidden behavior)?
        
        Args:
            proposed_code: The generated fix code
            original_code: The original source code with fracture
            oracle_guidance: Guidance from TheOracle
            fvcu_threshold: Minimum overall score to approve (default 0.7)
            
        Returns:
            Dict with FVCU scores and approval decision
        """
        result = {
            "factuality": 0.0,
            "validity": 0.0,
            "coherence": 0.0,
            "utility": 0.0,
            "faithfulness": 0.0,
            "overall": 0.0,
            "approved": False,
            "rationale": "",
            "evaluation_method": "heuristic",
        }
        
        if not proposed_code:
            result["rationale"] = "No code provided"
            return result
        
        # ---------------------------------------------------------
        # VALIDITY CHECK: Does the code compile?
        # ---------------------------------------------------------
        try:
            # Wrap in a function context for compilation
            test_code = f"def _test_wrapper():\n" + "\n".join(
                f"    {line}" for line in proposed_code.strip().splitlines()
            )
            compile(test_code, "<proposed>", "exec")
            result["validity"] = 1.0
        except SyntaxError as e:
            result["validity"] = 0.0
            result["rationale"] = f"SyntaxError: {e.msg}"
            return result  # Early exit - invalid code can't be approved
        
        # ---------------------------------------------------------
        # FACTUALITY CHECK: Does it address the fracture?
        # ---------------------------------------------------------
        # Check if the proposed code removes the fracture marker
        if FRACTURE_MARKER not in proposed_code:
            result["factuality"] = 0.8  # Good - marker removed
        else:
            result["factuality"] = 0.2  # Bad - marker still present
        
        # Check if it references the right function
        if "_think" in proposed_code or "def " in proposed_code:
            result["factuality"] = min(1.0, result["factuality"] + 0.2)
        
        # ---------------------------------------------------------
        # COHERENCE CHECK: Does it preserve functionality?
        # ---------------------------------------------------------
        coherence_score = 0.5  # Start neutral
        
        # Should contain key patterns from original logic
        key_patterns = ["_has_fracture_marker", "noop", "patch", "action", "return"]
        for pattern in key_patterns:
            if pattern in proposed_code:
                coherence_score += 0.1
        
        result["coherence"] = min(1.0, coherence_score)
        
        # ---------------------------------------------------------
        # UTILITY CHECK: Does it fix the problem?
        # ---------------------------------------------------------
        utility_score = 0.5
        
        # Should have proper return structure
        if '{"action":' in proposed_code or "{'action':" in proposed_code or '"action"' in proposed_code:
            utility_score += 0.2
        
        # Should handle both fracture and non-fracture cases
        if "if" in proposed_code and "return" in proposed_code:
            utility_score += 0.2
        
        # Bonus if it matches expected repair pattern
        if "DEFAULT_THINK_CODE" in proposed_code or "repair" in proposed_code:
            utility_score += 0.1
        
        result["utility"] = min(1.0, utility_score)
        
        # ---------------------------------------------------------
        # FAITHFULNESS CHECK: No hidden behavior?
        # ---------------------------------------------------------
        faithfulness_score = 0.8  # Assume good faith by default
        
        # Red flags for hidden behavior
        red_flags = ["eval(", "exec(", "import os", "subprocess", "__import__", "open("]
        for flag in red_flags:
            if flag in proposed_code:
                faithfulness_score -= 0.3
        
        # Check for reasonable code length (not suspiciously long)
        if len(proposed_code) > 5000:
            faithfulness_score -= 0.2
        
        result["faithfulness"] = max(0.0, faithfulness_score)
        
        # ---------------------------------------------------------
        # OVERALL SCORE: Weighted average
        # ---------------------------------------------------------
        weights = {
            "validity": 0.30,      # Most important - must compile
            "factuality": 0.20,   # Must address the bug
            "utility": 0.25,      # Must fix the problem
            "coherence": 0.15,    # Should preserve functionality
            "faithfulness": 0.10, # Should be trustworthy
        }
        
        result["overall"] = sum(
            result[k] * w for k, w in weights.items()
        )
        
        # ---------------------------------------------------------
        # APPROVAL DECISION
        # ---------------------------------------------------------
        result["approved"] = result["overall"] >= fvcu_threshold
        
        if result["approved"]:
            result["rationale"] = f"APPROVED: FVCU score {result['overall']:.2f} >= {fvcu_threshold}"
        else:
            result["rationale"] = f"REJECTED: FVCU score {result['overall']:.2f} < {fvcu_threshold}"
        
        # ---------------------------------------------------------
        # OPTIONAL: Use TheGuide's LLM-based evaluation if available
        # ---------------------------------------------------------
        if self.guide and hasattr(self.guide, 'guide_llm') and self.guide.guide_llm:
            try:
                # Use TheGuide's full FVCU evaluation (requires LLM)
                llm_eval = self._guide_llm_evaluate(proposed_code, original_code, oracle_guidance)
                if llm_eval:
                    # Merge LLM evaluation with heuristic (weighted)
                    for key in ["factuality", "validity", "coherence", "utility", "faithfulness"]:
                        if key in llm_eval:
                            # 60% LLM, 40% heuristic
                            result[key] = 0.6 * llm_eval[key] + 0.4 * result[key]
                    
                    # Recalculate overall
                    result["overall"] = sum(result[k] * w for k, w in weights.items())
                    result["approved"] = result["overall"] >= fvcu_threshold
                    result["evaluation_method"] = "hybrid"
                    result["rationale"] = llm_eval.get("rationale", result["rationale"])
            except Exception as e:
                # Fall back to heuristic if LLM eval fails
                result["evaluation_method"] = "heuristic_fallback"
                result["llm_error"] = str(e)
        
        return result
    
    def _guide_llm_evaluate(
        self,
        proposed_code: str,
        original_code: str,
        oracle_guidance: dict,
    ) -> dict | None:
        """
        Use TheGuide's LLM to evaluate code (if available).
        
        This provides a more sophisticated evaluation than heuristics alone.
        
        Returns:
            FVCU scores dict or None if not available
        """
        if not self.guide or not hasattr(self.guide, 'guide_llm') or not self.guide.guide_llm:
            return None
        
        recommendation = oracle_guidance.get("recommendation", "Fix the fracture")
        
        prompt = f"""You are evaluating a code patch for safety and correctness.

ORIGINAL CODE (with bug):
```python
{original_code[:1500]}
```

PROPOSED FIX:
```python
{proposed_code}
```

BUG DESCRIPTION:
{recommendation}

Evaluate using FVCU criteria (score each 0.0-1.0):
1. Factuality: Does the fix address the described bug?
2. Validity: Is the code syntactically and logically correct?
3. Coherence: Does it preserve existing functionality?
4. Utility: Does it actually solve the problem?
5. Faithfulness: Is the code doing what it claims (no hidden behavior)?

Respond in JSON format:
{{"factuality": X, "validity": X, "coherence": X, "utility": X, "faithfulness": X, "rationale": "brief explanation"}}"""

        try:
            response = self.guide.guide_llm.complete(prompt)
            
            # Parse JSON from response
            import json
            response_text = response.strip()
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            return json.loads(response_text)
        except Exception:
            return None

    async def observe(self):
        return {"source": self.inspect_my_source()}

    async def decide(self, state: AgentState):
        source = state.working_memory.get("source", "") if state else self.inspect_my_source()
        failure_rate = state.working_memory.get("failure_rate", 0.0) if state else 0.0
        rng = state.working_memory.get("rng") if state else None
        return self._think(source, rng=rng, failure_rate=failure_rate)

    async def act(self, decision: dict):
        if decision.get("action") != "patch":
            return {"action": "noop", "note": decision.get("reason")}
        return self.propose_patch(decision["function_name"], decision["new_code"])

    async def reflect(self, result: dict):
        return {"reflection": result, "status": "complete"}

    def run_diagnosis(self, failure_rate: float = 0.0, rng: random.Random | None = None) -> dict:
        source = self.inspect_my_source()
        decision = self._think(source, rng=rng, failure_rate=failure_rate)
        if decision.get("action") != "patch":
            return {
                "attempted_patch": False,
                "decision": decision,
                "result": None,
            }
        result = self.propose_patch(decision["function_name"], decision["new_code"])
        return {
            "attempted_patch": True,
            "decision": decision,
            "result": result,
        }
