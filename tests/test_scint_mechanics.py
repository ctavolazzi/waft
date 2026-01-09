import pytest
import json
from src.gym.rpg.scint import ScintType, RegexScintDetector
from src.gym.rpg.stabilizer import StabilizationLoop

class TestScintMechanics:
    
    def setup_method(self):
        self.detector = RegexScintDetector()

    def test_scint_classification_syntax(self):
        """Verify JSON errors are classified as SYNTAX_TEAR (CHA)."""
        # Simulate a JSON error
        try:
            json.loads("{'bad': 'json'}") # Single quotes are invalid JSON
        except json.JSONDecodeError as e:
            scints = self.detector.detect_from_exception(e, "{'bad': 'json'}")
            
            assert len(scints) == 1
            assert scints[0].scint_type == ScintType.SYNTAX_TEAR
            assert scints[0].get_stat_category() == "CHA"
            assert "Expecting property name" in scints[0].evidence

    def test_scint_classification_logic(self):
        """Verify ValueErrors are classified as LOGIC_FRACTURE (INT)."""
        try:
            raise ValueError("Sum must be 1.0, got 1.5")
        except ValueError as e:
            scints = self.detector.detect_from_exception(e, "output")
            
            assert scints[0].scint_type == ScintType.LOGIC_FRACTURE
            assert scints[0].get_stat_category() == "INT"
            assert scints[0].severity >= 0.5  # Logic errors have higher base severity

    def test_scint_classification_safety(self):
        """Verify safety refusals are classified as SAFETY_VOID (WIS)."""
        # Safety voids often come from text scanning, not exceptions
        output = "I cannot fulfill this request because it is dangerous."
        scints = self.detector.scan(output)
        
        assert len(scints) > 0
        assert scints[0].scint_type == ScintType.SAFETY_VOID
        assert scints[0].get_stat_category() == "WIS"
        assert scints[0].severity >= 0.9  # Safety is critical

    def test_severity_calculation(self):
        """Verify severity increases with quest difficulty."""
        try:
            raise ValueError("Test error")
        except ValueError as e:
            # Difficulty 1
            s1 = self.detector.detect_from_exception(e, "", quest_difficulty=1)[0]
            # Difficulty 5
            s5 = self.detector.detect_from_exception(e, "", quest_difficulty=5)[0]
            
            assert s5.severity > s1.severity
            assert s5.severity <= 1.0

    def test_stabilization_prompt_construction(self):
        """Verify the 'Reflexion' prompt contains the error evidence."""
        stabilizer = StabilizationLoop()
        
        # Create a fake scint
        try:
            json.loads("bad")
        except Exception as e:
            scints = self.detector.detect_from_exception(e, "bad")
            
        prompt = stabilizer._build_stabilization_prompt(
            base_context="Original Quest",
            scints=scints,
            bad_output="bad"
        )
        
        assert "⚠️ REALITY FRACTURE DETECTED ⚠️" in prompt
        assert "Expecting value" in prompt or "JSONDecodeError" in prompt  # Error evidence
        assert "Original Quest" in prompt   # Context preserved
        assert "YOUR PREVIOUS FAILED OUTPUT" in prompt
        assert "SYNTAX_TEAR" in prompt  # Scint type should be in evidence block
