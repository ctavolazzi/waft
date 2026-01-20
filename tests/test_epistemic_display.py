"""Tests for epistemic display module."""

from waft.cli.epistemic_display import (
    format_epistemic_state,
    format_epistemic_summary,
    format_gate_result,
    get_moon_phase,
)


def test_get_moon_phase():
    """Test moon phase calculation."""
    assert get_moon_phase(0.1) == "🌑"  # Critical
    assert get_moon_phase(0.3) == "🌒"  # Low
    assert get_moon_phase(0.6) == "🌓"  # Moderate
    assert get_moon_phase(0.85) == "🌔"  # Good
    assert get_moon_phase(0.95) == "🌕"  # Excellent


def test_format_gate_result():
    """Test gate result formatting."""
    proceed = format_gate_result("PROCEED")
    assert "PROCEED" in str(proceed)

    halt = format_gate_result("HALT")
    assert "HALT" in str(halt)


def test_format_epistemic_state():
    """Test epistemic state formatting."""
    state = {
        "vectors": {
            "engagement": 0.8,
            "foundation": {"know": 0.7, "do": 0.6, "context": 0.5},
            "comprehension": {"clarity": 0.8, "coherence": 0.7, "signal": 0.6, "density": 0.5},
            "execution": {"state": 0.7, "change": 0.6, "completion": 0.5, "impact": 0.4},
            "uncertainty": 0.3,
        }
    }

    panel = format_epistemic_state(state)
    assert panel is not None


def test_format_epistemic_summary():
    """Test epistemic summary formatting."""
    state = {
        "vectors": {
            "foundation": {"know": 0.7},
            "uncertainty": 0.3,
        }
    }

    summary = format_epistemic_summary(state)
    assert (
        "🌑" in summary or "🌒" in summary or "🌓" in summary or "🌔" in summary or "🌕" in summary
    )
