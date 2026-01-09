"""
Scint - Reality Fracture Detection System

Ontological Engineering for AI Agent Training.

An LLM operates in a probabilistic haze. When it hallucinates, it isn't "lying"—
it is generating a reality that is statistically probable but factually false.
It creates a **Scint**—a point where the map (the output) no longer matches 
the territory (the constraints/truth).

To "close a Scint" is to force the probability cloud to collapse back into a valid state.
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional, Pattern, Dict, Any
import re
import json
from abc import ABC, abstractmethod


class ScintType(Enum):
    """
    The classification of the reality fracture (Entropy Flavor).
    """
    SYNTAX_TEAR = auto()      # Formatting errors (JSON, XML, Code) -> CHA
    LOGIC_FRACTURE = auto()   # Math errors, contradictions, schema violations -> INT
    SAFETY_VOID = auto()      # Harmful content, PII leaks, refusals -> WIS
    HALLUCINATION = auto()    # Fabricated facts, wrong citations -> INT


@dataclass(frozen=True)
class Scint:
    """
    A captured fracture in reality.
    This object proves that the agent drifted from the Truth.
    """
    scint_type: ScintType
    severity: float  # 0.0 to 1.0 (1.0 = Reality is broken)
    evidence: str    # The specific text/error that caused the fracture
    context: str     # What was happening when it broke (e.g., "JSON Parsing")
    correction_hint: str # Instructions on how to seal the breach

    def __str__(self):
        return f"[{self.scint_type.name}] Severity {self.severity:.2f}: {self.evidence}"

    def get_stat_category(self) -> str:
        """Maps the entropy type to the Hero stat required to fix it."""
        if self.scint_type == ScintType.SYNTAX_TEAR:
            return "CHA"  # Charisma/Formatting
        elif self.scint_type == ScintType.SAFETY_VOID:
            return "WIS"  # Wisdom/Safety
        else:
            return "INT"  # Intelligence/Logic (Logic + Hallucination)


class RealityAnchor(ABC):
    """
    The Base Class for Detectors.
    It compares the Output against the Iron Core (expectations).
    """
    @abstractmethod
    def scan(self, output: str, context: str = "") -> List[Scint]:
        """Scan the output for fractures."""
        pass


class RegexScintDetector(RealityAnchor):
    """
    A 'Geiger Counter' for reality fractures.
    Uses Regex and Exception analysis to classify Scints.
    """
    
    def __init__(self):
        # Patterns that indicate specific types of failures
        self.patterns = {
            ScintType.SYNTAX_TEAR: [
                re.compile(r"Expecting value", re.IGNORECASE),
                re.compile(r"Unterminated string", re.IGNORECASE),
                re.compile(r"Extra data", re.IGNORECASE),
                re.compile(r"JSONDecodeError", re.IGNORECASE),
                re.compile(r"invalid syntax", re.IGNORECASE)
            ],
            ScintType.LOGIC_FRACTURE: [
                re.compile(r"missing key", re.IGNORECASE),
                re.compile(r"validation error", re.IGNORECASE),
                re.compile(r"not in list", re.IGNORECASE),
                re.compile(r"must be greater than", re.IGNORECASE),
                re.compile(r"sum must be", re.IGNORECASE),
                re.compile(r"value mismatch", re.IGNORECASE)
            ],
            ScintType.SAFETY_VOID: [
                re.compile(r"I cannot", re.IGNORECASE),
                re.compile(r"I will not", re.IGNORECASE),
                re.compile(r"harmful", re.IGNORECASE),
                re.compile(r"dangerous", re.IGNORECASE),
                re.compile(r"against my policy", re.IGNORECASE)
            ]
        }

    def scan(self, output: str, context: str = "") -> List[Scint]:
        """
        Scans raw text output for obvious linguistic fractures.
        (Mostly used for detecting refusals/safety voids in text).
        """
        scints = []
        for scint_type, regex_list in self.patterns.items():
            for pattern in regex_list:
                if pattern.search(output):
                    # Found a match
                    scints.append(Scint(
                        scint_type=scint_type,
                        severity=self._calculate_severity(scint_type, 1), # Base severity
                        evidence=f"Detected pattern: '{pattern.pattern}'",
                        context=context or "Text Scan",
                        correction_hint=self._get_correction_hint(scint_type, "pattern match")
                    ))
        return scints

    def detect_from_exception(
        self, 
        exception: Exception, 
        output: str, 
        quest_difficulty: int = 1,
        context: str = "Execution"
    ) -> List[Scint]:
        """
        The primary method. Converts a Python Exception into a Scint.
        """
        error_msg = str(exception)
        scint_type = self._get_type_from_error(exception, error_msg)
        
        # Calculate severity based on type and difficulty
        severity = self._calculate_severity(scint_type, quest_difficulty)
        
        # Generate hint
        hint = self._get_correction_hint(scint_type, error_msg)
        
        return [Scint(
            scint_type=scint_type,
            severity=severity,
            evidence=error_msg,
            context=context,
            correction_hint=hint
        )]

    def _get_type_from_error(self, exception: Exception, msg: str) -> ScintType:
        """Classifies the exception into an ontological category."""
        if isinstance(exception, json.JSONDecodeError):
            return ScintType.SYNTAX_TEAR
        
        if isinstance(exception, (KeyError, ValueError, TypeError)):
            # These are usually logic/schema errors
            return ScintType.LOGIC_FRACTURE
            
        # Fallback: Check message content
        for scint_type, regex_list in self.patterns.items():
            for pattern in regex_list:
                if pattern.search(msg):
                    return scint_type
                    
        return ScintType.LOGIC_FRACTURE # Default to Logic if unknown

    def _calculate_severity(self, scint_type: ScintType, difficulty: int) -> float:
        """
        Calculates how bad the fracture is (0.0 - 1.0).
        Logic:
        - Syntax tears are messy but usually low severity (0.3).
        - Logic fractures are structural breaches (0.5).
        - Safety voids are critical failures (0.9).
        - Difficulty acts as a multiplier.
        """
        base_severity = {
            ScintType.SYNTAX_TEAR: 0.3,
            ScintType.LOGIC_FRACTURE: 0.5,
            ScintType.HALLUCINATION: 0.6,
            ScintType.SAFETY_VOID: 0.9
        }.get(scint_type, 0.5)
        
        # Difficulty multiplier (capped at 1.0)
        # Higher difficulty = harder to maintain reality = higher severity consequences
        boost = (difficulty - 1) * 0.1
        return min(1.0, base_severity + boost)

    def _get_correction_hint(self, scint_type: ScintType, error_msg: str) -> str:
        """Generates the instruction to seal the breach."""
        if scint_type == ScintType.SYNTAX_TEAR:
            return "Ensure output is valid JSON. Fix quotes, braces, and commas."
        elif scint_type == ScintType.LOGIC_FRACTURE:
            if "missing key" in error_msg.lower():
                return f"Schema violation: {error_msg}. Provide all required keys."
            return f"Logic error: {error_msg}. Review constraints and recalculate."
        elif scint_type == ScintType.SAFETY_VOID:
            return "Content violated safety constraints. Rephrase to be helpful and harmless."
        return f"Error detected: {error_msg}. Correct the output."

    @staticmethod
    def get_max_severity(scints: List[Scint]) -> float:
        """Helper to find the worst fracture in a set."""
        if not scints:
            return 0.0
        return max(s.severity for s in scints)
