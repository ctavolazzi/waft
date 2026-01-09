"""
Tests for InputTransformer - The Gateway (The Airlock)

Tests that the transformer correctly sanitizes and validates raw input data
before it reaches the hardened DecisionMatrix.
"""

import pytest
from waft.core.input_transformer import InputTransformer
from waft.core.decision_matrix import DecisionMatrix


def test_happy_path_perfect_data():
    """Test 1: Happy path with perfect data."""
    data = {
        'alternatives': ['Option A', 'Option B'],
        'criteria': {
            'Cost': 0.5,
            'Quality': 0.5
        },
        'scores': {
            'Option A': {'Cost': 10.0, 'Quality': 5.0},
            'Option B': {'Cost': 5.0, 'Quality': 10.0}
        },
        'methodology': 'WSM'
    }
    
    matrix = InputTransformer.transform_input(data)
    
    assert isinstance(matrix, DecisionMatrix)
    assert len(matrix.alternatives) == 2
    assert len(matrix.criteria) == 2
    assert len(matrix.scores) == 4
    assert matrix.methodology == 'WSM'


def test_dirty_data_type_casting():
    """Test 2: Dirty data (strings "0.5", integers 10) -> Should succeed."""
    data = {
        'alternatives': ['Option A', 'Option B'],
        'criteria': {
            'Cost': '0.5',  # String instead of float
            'Quality': 0.5
        },
        'scores': {
            'Option A': {'Cost': 10, 'Quality': 5},  # Integers instead of floats
            'Option B': {'Cost': '5', 'Quality': '10'}  # String numbers
        }
    }
    
    matrix = InputTransformer.transform_input(data)
    
    assert isinstance(matrix, DecisionMatrix)
    # Verify types were cast correctly
    assert matrix.criteria[0].weight == 0.5
    assert matrix.scores[0].value == 10.0
    assert matrix.scores[1].value == 5.0
    assert matrix.scores[2].value == 5.0
    assert matrix.scores[3].value == 10.0


def test_missing_keys():
    """Test 3: Missing keys -> Should raise ValueError."""
    # Missing 'alternatives'
    data = {
        'criteria': {'Cost': 0.5, 'Quality': 0.5},
        'scores': {'Option A': {'Cost': 10, 'Quality': 5}}
    }
    
    with pytest.raises(ValueError, match="Missing required keys"):
        InputTransformer.transform_input(data)
    
    # Missing 'criteria'
    data = {
        'alternatives': ['Option A'],
        'scores': {'Option A': {'Cost': 10}}
    }
    
    with pytest.raises(ValueError, match="Missing required keys"):
        InputTransformer.transform_input(data)
    
    # Missing 'scores'
    data = {
        'alternatives': ['Option A'],
        'criteria': {'Cost': 1.0}
    }
    
    with pytest.raises(ValueError, match="Missing required keys"):
        InputTransformer.transform_input(data)


def test_invalid_number_strings():
    """Test 4: Invalid number strings ("five") -> Should raise ValueError."""
    data = {
        'alternatives': ['Option A'],
        'criteria': {
            'Cost': 'five',  # Invalid number string
            'Quality': 0.5
        },
        'scores': {
            'Option A': {'Cost': 10, 'Quality': 5}
        }
    }
    
    with pytest.raises(ValueError, match="cannot convert to float"):
        InputTransformer.transform_input(data)
    
    # Test invalid score string
    data = {
        'alternatives': ['Option A'],
        'criteria': {'Cost': 1.0},
        'scores': {
            'Option A': {'Cost': 'not-a-number'}
        }
    }
    
    with pytest.raises(ValueError, match="cannot convert to float"):
        InputTransformer.transform_input(data)


def test_whitespace_sanitization():
    """Test that whitespace is trimmed from names."""
    data = {
        'alternatives': ['  Option A  ', '  Option B  '],
        'criteria': {
            '  Cost  ': 0.5,
            '  Quality  ': 0.5
        },
        'scores': {
            '  Option A  ': {'  Cost  ': 10, '  Quality  ': 5},
            '  Option B  ': {'  Cost  ': 5, '  Quality  ': 10}
        }
    }
    
    matrix = InputTransformer.transform_input(data)
    
    # Verify whitespace was trimmed
    assert matrix.alternatives[0].name == 'Option A'
    assert matrix.alternatives[1].name == 'Option B'
    assert matrix.criteria[0].name == 'Cost'
    assert matrix.criteria[1].name == 'Quality'


def test_alternative_dict_format():
    """Test that alternatives can be provided as dicts with descriptions."""
    data = {
        'alternatives': [
            {'name': 'Option A', 'description': 'First option'},
            'Option B'  # Can mix string and dict
        ],
        'criteria': {'Cost': 1.0},
        'scores': {
            'Option A': {'Cost': 10},
            'Option B': {'Cost': 5}
        }
    }
    
    matrix = InputTransformer.transform_input(data)
    
    assert matrix.alternatives[0].name == 'Option A'
    assert matrix.alternatives[0].description == 'First option'
    assert matrix.alternatives[1].name == 'Option B'
    assert matrix.alternatives[1].description is None


def test_criterion_dict_format():
    """Test that criteria can be provided as dicts with descriptions."""
    data = {
        'alternatives': ['Option A'],
        'criteria': {
            'Cost': {'weight': 0.5, 'description': 'Financial cost'},
            'Quality': 0.5  # Can mix simple and dict format
        },
        'scores': {
            'Option A': {'Cost': 10, 'Quality': 5}
        }
    }
    
    matrix = InputTransformer.transform_input(data)
    
    assert matrix.criteria[0].name == 'Cost'
    assert matrix.criteria[0].weight == 0.5
    assert matrix.criteria[0].description == 'Financial cost'
    assert matrix.criteria[1].name == 'Quality'
    assert matrix.criteria[1].weight == 0.5
    assert matrix.criteria[1].description is None


def test_validation_errors_propagate():
    """Test that validation errors from Iron Core are caught and re-raised with context."""
    data = {
        'alternatives': ['Option A'],
        'criteria': {
            'Cost': -0.5,  # Negative weight (will be caught by Iron Core)
            'Quality': 1.5  # Sums to 1.0 but negative weight invalid
        },
        'scores': {
            'Option A': {'Cost': 10, 'Quality': 5}
        }
    }
    
    # The negative weight will be caught by DecisionMatrixCalculator validation
    # which happens when we try to create the calculator
    from waft.core.decision_matrix import DecisionMatrixCalculator
    
    matrix = InputTransformer.transform_input(data)
    # The error should occur when creating the calculator
    with pytest.raises(ValueError, match="negative weight"):
        DecisionMatrixCalculator(matrix)
