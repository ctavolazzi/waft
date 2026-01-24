// Appendix A: Full Test Output
// Pages 66-67

#import "../waft_functions.typ": callout, evidence, metric

= Appendix A: Full Test Output

This appendix contains complete test execution outputs referenced in the analysis.

== A.1 Scint Mechanics Test Suite

#evidence("pytest tests/test_scint_mechanics.py -v", [
  ```
  ============================= test session starts ==============================
  platform darwin -- Python 3.12.1, pytest-7.4.3, pluggy-1.3.0
  cachedir: .pytest_cache
  rootdir: /Users/ctavolazzi/Code/active/waft
  plugins: cov-4.1.0, asyncio-0.21.1
  collected 5 items

  tests/test_scint_mechanics.py::test_scint_classification_syntax PASSED   [ 20%]
  tests/test_scint_mechanics.py::test_scint_classification_logic PASSED    [ 40%]
  tests/test_scint_mechanics.py::test_scint_classification_safety PASSED   [ 60%]
  tests/test_scint_mechanics.py::test_severity_calculation PASSED          [ 80%]
  tests/test_scint_mechanics.py::test_stabilization_prompt PASSED          [100%]

  ============================== 5 passed in 0.23s ===============================
  ```
])

== A.2 Individual Test Details

=== A.2.1 test_scint_classification_syntax

```python
def test_scint_classification_syntax():
    """Verify JSON errors are classified as SYNTAX_TEAR."""
    detector = RegexScintDetector()
    
    try:
        json.loads("{invalid json")
    except Exception as exc:
        scints = detector.detect_from_exception(exc, "test_quest_1", difficulty=1)
    
    assert len(scints) == 1
    assert scints[0].scint_type == ScintType.SYNTAX_TEAR
    assert scints[0].get_stat_category() == "CHA"
    assert 0.2 <= scints[0].severity <= 0.4  # Base 0.3 ± tolerance
```

**Result:** ✅ PASS - JSON errors correctly classified as SYNTAX_TEAR with CHA stat

=== A.2.2 test_scint_classification_logic

```python
def test_scint_classification_logic():
    """Verify ValueError is classified as LOGIC_FRACTURE."""
    detector = RegexScintDetector()
    
    try:
        raise ValueError("Invalid computation")
    except Exception as exc:
        scints = detector.detect_from_exception(exc, "test_quest_2", difficulty=2)
    
    assert len(scints) == 1
    assert scints[0].scint_type == ScintType.LOGIC_FRACTURE
    assert scints[0].get_stat_category() == "INT"
    assert 0.5 <= scints[0].severity <= 0.7  # Base 0.5 + difficulty boost
```

**Result:** ✅ PASS - ValueErrors correctly classified as LOGIC_FRACTURE with INT stat

=== A.2.3 test_scint_classification_safety

```python
def test_scint_classification_safety():
    """Verify refusal patterns are classified as SAFETY_VOID."""
    detector = RegexScintDetector()
    
    output = "I cannot help with that request as it may contain harmful content."
    scints = detector.detect_from_string(
        output,
        {"quest_id": "test_quest_3", "difficulty": 2}
    )
    
    assert len(scints) >= 1
    assert scints[0].scint_type == ScintType.SAFETY_VOID
    assert scints[0].severity >= 0.9  # Safety is critical
```

**Result:** ✅ PASS - Refusal patterns correctly classified as SAFETY_VOID with severity ≥ 0.9

=== A.2.4 test_severity_calculation

```python
def test_severity_calculation():
    """Verify severity formula: base + (difficulty - 1) * 0.1."""
    detector = RegexScintDetector()
    
    # Test at difficulty 1 (base only)
    scint_d1 = detector._calculate_severity(ScintType.SYNTAX_TEAR, difficulty=1)
    assert scint_d1 == 0.3  # Base for SYNTAX_TEAR
    
    # Test at difficulty 3 (base + boost)
    scint_d3 = detector._calculate_severity(ScintType.SYNTAX_TEAR, difficulty=3)
    assert scint_d3 == 0.5  # 0.3 + (3-1)*0.1 = 0.5
    
    # Test capping at 1.0
    scint_high = detector._calculate_severity(ScintType.SAFETY_VOID, difficulty=5)
    assert scint_high == 1.0  # 0.9 + 0.4 = 1.3, capped at 1.0
```

**Result:** ✅ PASS - Severity formula verified with exact values

=== A.2.5 test_stabilization_prompt

```python
def test_stabilization_prompt():
    """Verify stabilization prompt includes required components."""
    stabilizer = StabilizationLoop(max_attempts=3)
    scint = Scint(
        scint_type=ScintType.SYNTAX_TEAR,
        severity=0.4,
        evidence="JSONDecodeError: Expecting value",
        context={"quest_id": "test_123"},
        correction_hint="Check JSON syntax"
    )
    
    prompt = stabilizer._build_reflexion_prompt(
        original_input="Parse this JSON",
        scint=scint,
        last_attempt=None,
        attempt_num=0
    )
    
    # Verify prompt contains required elements
    assert "Attempt 1/3" in prompt
    assert "SYNTAX_TEAR" in prompt
    assert "0.40" in prompt  # Severity
    assert "JSONDecodeError" in prompt  # Evidence
    assert "Check JSON syntax" in prompt  # Hint
    assert "fix the error" in prompt.lower()
```

**Result:** ✅ PASS - Stabilization prompts contain all required components

== A.3 Test Discovery Summary

```bash
$ pytest tests/ --collect-only
collected 380 items

tests/test_scint_mechanics.py::test_scint_classification_syntax
tests/test_scint_mechanics.py::test_scint_classification_logic
tests/test_scint_mechanics.py::test_scint_classification_safety
tests/test_scint_mechanics.py::test_severity_calculation
tests/test_scint_mechanics.py::test_stabilization_prompt
# ... 375 more tests not shown
```

**Total Tests Found:** 380  
**Tests Executed:** 5 (critical scint mechanics)  
**Tests Passed:** 5/5 (100%)
