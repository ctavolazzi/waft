import logging
from typing import List, Optional, Callable, Tuple, Any, Dict
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
import time

from .scint import Scint, RegexScintDetector

logger = logging.getLogger(__name__)

class StabilizationLoop:
    """
    The Stabilization Loop.
    
    When a Scint (Reality Fracture) is detected, this mechanism intervenes.
    It feeds the evidence of the error back into the agent to collapse the
    probability cloud into a consistent state.
    """
    
    def __init__(
        self,
        max_attempts: int = 1,
        timeout: float = 30.0,
        enable_stabilization: bool = True
    ):
        self.max_attempts = max_attempts
        self.timeout = timeout
        self.enable_stabilization = enable_stabilization

    def stabilize(
        self,
        initial_scints: List[Scint],
        original_output: str,
        quest_description: str,
        agent_func: Callable[[str], str],
        validator_func: Callable[[str], Any]
    ) -> Tuple[Optional[str], bool, int, List[Scint]]:
        """
        Attempt to stabilize the reality fractures.
        
        Args:
            initial_scints: The errors detected in the first attempt.
            original_output: The text that caused the errors.
            quest_description: The original prompt context.
            agent_func: Function to call the agent (takes prompt, returns str).
            validator_func: Function to check if output is valid (raises exception if not).
            
        Returns:
            Tuple containing:
            - corrected_output (str or None)
            - success (bool)
            - attempts_made (int)
            - final_scints (List[Scint] - existing errors if failed)
        """
        if not self.enable_stabilization or not initial_scints:
            return None, False, 0, initial_scints

        current_scints = initial_scints
        attempts = 0

        while attempts < self.max_attempts:
            attempts += 1
            logger.info(f"🌀 Stabilization Attempt {attempts}/{self.max_attempts} for {len(current_scints)} Scints")

            # 1. Construct the Stabilization Prompt (Reflexion)
            prompt = self._build_stabilization_prompt(
                quest_description, 
                current_scints, 
                original_output if attempts == 1 else None # Only show original bad output once
            )

            # 2. Call Agent with Timeout
            try:
                # We use a ThreadPool to enforce the timeout on the agent call
                with ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(agent_func, prompt)
                    corrected_output = future.result(timeout=self.timeout)

                # 3. Verify: Did this fix the reality?
                # We try the validator. If it passes, we are good.
                try:
                    validator_func(corrected_output)
                    # If we get here, reality is stabilized.
                    logger.info(f"✨ Scint stabilized on attempt {attempts}")
                    return corrected_output, True, attempts, []
                    
                except Exception as e:
                    # The repair failed. Reality is still broken.
                    # We re-scan to see if the *same* Scints exist or if new ones appeared.
                    # Note: The validator usually raises the exception we need to classify.
                    detector = RegexScintDetector()
                    # We assume a difficulty of 1 for re-tries, or pass it in if needed.
                    new_scints = detector.detect_from_exception(
                        e, corrected_output, context=f"Stabilization Attempt {attempts}"
                    )
                    current_scints = new_scints
                    logger.warning(f"⚠️ Stabilization failed. New fracture count: {len(new_scints)}")

            except FutureTimeoutError:
                logger.error(f"⏰ Stabilization timed out after {self.timeout}s")
                # Timeout is a type of Safety Void (Availability)
                return None, False, attempts, current_scints
            except Exception as e:
                logger.error(f"💥 Critical error during stabilization: {e}")
                return None, False, attempts, current_scints

        # If we exit the loop, we failed to stabilize.
        return None, False, attempts, current_scints

    def _build_stabilization_prompt(
        self, 
        base_context: str, 
        scints: List[Scint],
        bad_output: Optional[str] = None
    ) -> str:
        """
        Constructs the 'Reflexion' prompt.
        It shows the Agent the 'Fracture' it created and asks for a fix.
        """
        evidence_block = "\n".join(
            [f"- [{s.scint_type.name}] {s.evidence}" for s in scints]
        )
        
        hints_block = "\n".join(
            [f"- {s.correction_hint}" for s in scints]
        )
        
        max_sev = RegexScintDetector.get_max_severity(scints)

        prompt = f"""{base_context}

⚠️ REALITY FRACTURE DETECTED ⚠️
The previous attempt created {len(scints)} fracture(s) in reality (Max Severity: {max_sev:.2f}).

ERRORS DIAGNOSED:
{evidence_block}

CORRECTION HINTS:
{hints_block}
"""
        if bad_output:
             prompt += f"\nYOUR PREVIOUS FAILED OUTPUT:\n{bad_output}\n"

        prompt += "\nINSTRUCTION:\nYou must stabilize these fractures.\nRe-generate the response such that it is valid, consistent, and follows the hints above.\nReturn ONLY the corrected JSON."
        
        return prompt
