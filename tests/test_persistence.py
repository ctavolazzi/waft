"""
Tests for DecisionPersistence - The Vault

Tests that decision matrices can be saved and loaded correctly,
and that loaded data passes through InputTransformer validation.
"""

import pytest
import json
import tempfile
from pathlib import Path
from waft.core.persistence import DecisionPersistence
from waft.core.decision_matrix import (
    DecisionMatrix, Alternative, Criterion, Score, DecisionMatrixCalculator
)


@pytest.fixture
def sample_matrix():
    """Create a sample decision matrix for testing."""
    alts = [
        Alternative("Option A", "First option"),
        Alternative("Option B")
    ]
    crits = [
        Criterion("Cost", 0.6, "Financial cost"),
        Criterion("Quality", 0.4)
    ]
    scores = [
        Score("Option A", "Cost", 8.0, "Good value"),
        Score("Option A", "Quality", 7.0),
        Score("Option B", "Cost", 5.0),
        Score("Option B", "Quality", 9.0, "High quality")
    ]
    return DecisionMatrix(alts, crits, scores, methodology="WSM")


def test_save_and_load_roundtrip(sample_matrix):
    """Test that saving and loading preserves all data."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "test_decision.json"
        
        # Save
        DecisionPersistence.save(sample_matrix, filepath)
        assert filepath.exists()
        
        # Load
        loaded_matrix = DecisionPersistence.load(filepath)
        
        # Verify all data preserved
        assert len(loaded_matrix.alternatives) == 2
        assert loaded_matrix.alternatives[0].name == "Option A"
        assert loaded_matrix.alternatives[0].description == "First option"
        assert loaded_matrix.alternatives[1].name == "Option B"
        assert loaded_matrix.alternatives[1].description is None
        
        assert len(loaded_matrix.criteria) == 2
        assert loaded_matrix.criteria[0].name == "Cost"
        assert loaded_matrix.criteria[0].weight == 0.6
        assert loaded_matrix.criteria[0].description == "Financial cost"
        assert loaded_matrix.criteria[1].name == "Quality"
        assert loaded_matrix.criteria[1].weight == 0.4
        
        assert len(loaded_matrix.scores) == 4
        assert loaded_matrix.methodology == "WSM"


def test_loaded_matrix_is_valid(sample_matrix):
    """Test that loaded matrix passes Iron Core validation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "test_decision.json"
        
        # Save and load
        DecisionPersistence.save(sample_matrix, filepath)
        loaded_matrix = DecisionPersistence.load(filepath)
        
        # Should be able to create calculator (triggers validation)
        calculator = DecisionMatrixCalculator(loaded_matrix)
        results = calculator.calculate_wsm()
        
        # Verify calculations work
        assert "Option A" in results
        assert "Option B" in results
        assert results["Option A"] == (0.6 * 8.0 + 0.4 * 7.0)  # 7.6
        assert results["Option B"] == (0.6 * 5.0 + 0.4 * 9.0)  # 6.6


def test_json_format_is_readable(sample_matrix):
    """Test that saved JSON is properly formatted and readable."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "test_decision.json"
        
        DecisionPersistence.save(sample_matrix, filepath)
        
        # Read JSON directly
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Verify structure
        assert 'alternatives' in data
        assert 'criteria' in data
        assert 'scores' in data
        assert 'methodology' in data
        
        assert len(data['alternatives']) == 2
        assert data['alternatives'][0]['name'] == "Option A"
        assert data['alternatives'][0]['description'] == "First option"
        
        assert len(data['criteria']) == 2
        assert data['criteria'][0]['name'] == "Cost"
        assert data['criteria'][0]['weight'] == 0.6


def test_load_uses_input_transformer_validation():
    """Test that loading uses InputTransformer (security validation)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "malicious.json"
        
        # Create a JSON file in saved format (lists) with "dirty" data
        # The InputTransformer will sanitize names when loading
        malicious_data = {
            'alternatives': [
                {'name': '  Option A  '},  # Whitespace to be trimmed
                {'name': 'Option B'}
            ],
            'criteria': [
                {'name': '  Cost  ', 'weight': '0.6'},  # String weight, whitespace
                {'name': 'Quality', 'weight': 0.4}
            ],
            'scores': [
                {'alternative_name': '  Option A  ', 'criterion_name': '  Cost  ', 'value': '8'},  # String value
                {'alternative_name': '  Option A  ', 'criterion_name': 'Quality', 'value': 7},
                {'alternative_name': 'Option B', 'criterion_name': '  Cost  ', 'value': 5},
                {'alternative_name': 'Option B', 'criterion_name': 'Quality', 'value': 9}
            ],
            'methodology': 'WSM'
        }
        
        with open(filepath, 'w') as f:
            json.dump(malicious_data, f)
        
        # Load should sanitize (whitespace trimmed, types cast)
        matrix = DecisionPersistence.load(filepath)
        
        # Verify sanitization worked
        assert matrix.alternatives[0].name == "Option A"  # Whitespace trimmed
        assert matrix.criteria[0].name == "Cost"  # Whitespace trimmed
        assert matrix.criteria[0].weight == 0.6  # String converted to float
        
        # Verify scores exist and are sanitized
        assert len(matrix.scores) == 4  # 2 alternatives × 2 criteria
        
        # Find the score for Option A on Cost (names are sanitized)
        score_obj = next(
            (s for s in matrix.scores
             if s.alternative_name == "Option A" and s.criterion_name == "Cost"),
            None
        )
        assert score_obj is not None, "Score for Option A on Cost should exist"
        assert score_obj.value == 8.0  # String converted to float
