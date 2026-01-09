"""
Persistence Module - The Vault

Handles saving and loading DecisionMatrix objects to/from JSON files.
Uses InputTransformer for validation when loading to ensure security.
"""

import json
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

from .decision_matrix import DecisionMatrix
from .input_transformer import InputTransformer


class DecisionPersistence:
    """
    Handles persistence of DecisionMatrix objects to JSON files.
    
    Uses InputTransformer for validation when loading to ensure
    loaded data passes through the same security checks as fresh input.
    """
    
    @staticmethod
    def save(matrix: DecisionMatrix, filepath: Path) -> None:
        """
        Save a DecisionMatrix to a JSON file.
        
        Args:
            matrix: The DecisionMatrix to save
            filepath: Path where the JSON file should be written
        
        Raises:
            IOError: If file cannot be written
        """
        # Convert matrix to dictionary
        data = DecisionPersistence._to_dict(matrix)
        
        # Write to JSON file with formatting
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def load(filepath: Path) -> DecisionMatrix:
        """
        Load a DecisionMatrix from a JSON file.
        
        CRITICAL: Uses InputTransformer to validate loaded data.
        This ensures that even saved files pass through the same
        security checks (sanitization, type casting, validation)
        as fresh user input.
        
        Args:
            filepath: Path to the JSON file to load
        
        Returns:
            Validated DecisionMatrix object
        
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file contains invalid data (caught by InputTransformer)
            json.JSONDecodeError: If file is not valid JSON
        """
        # Read JSON file
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Convert from saved format to InputTransformer format
        transformer_data = DecisionPersistence._from_dict_format(data)
        
        # CRITICAL: Use InputTransformer to validate and reconstruct
        # This reuses the "Airlock" validation logic
        matrix = InputTransformer.transform_input(transformer_data)
        
        return matrix
    
    @staticmethod
    def _to_dict(matrix: DecisionMatrix) -> Dict[str, Any]:
        """
        Convert a DecisionMatrix to a serializable dictionary.
        
        Args:
            matrix: The DecisionMatrix to convert
        
        Returns:
            Dictionary representation suitable for JSON serialization
        """
        return {
            'alternatives': [
                {
                    'name': alt.name,
                    'description': alt.description
                }
                for alt in matrix.alternatives
            ],
            'criteria': [
                {
                    'name': crit.name,
                    'weight': crit.weight,
                    'description': crit.description
                }
                for crit in matrix.criteria
            ],
            'scores': [
                {
                    'alternative_name': score.alternative_name,
                    'criterion_name': score.criterion_name,
                    'value': score.value,
                    'reasoning': score.reasoning
                }
                for score in matrix.scores
            ],
            'methodology': matrix.methodology
        }
    
    @staticmethod
    def _from_dict_format(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert saved format to InputTransformer format.
        
        The saved format uses lists for alternatives/criteria/scores,
        but InputTransformer expects a different structure.
        This method converts between formats.
        """
        # Convert alternatives list to InputTransformer format
        # Preserve descriptions if present
        alternatives = []
        for alt in data.get('alternatives', []):
            if isinstance(alt, dict):
                alt_dict = {'name': alt['name']}
                if alt.get('description'):
                    alt_dict['description'] = alt['description']
                alternatives.append(alt_dict)
            else:
                alternatives.append(alt)
        
        # Convert criteria list to dict format
        # Preserve descriptions if present
        criteria = {}
        for crit in data.get('criteria', []):
            if isinstance(crit, dict):
                # If description exists, use dict format; otherwise just weight
                if crit.get('description'):
                    criteria[crit['name']] = {
                        'weight': crit['weight'],
                        'description': crit['description']
                    }
                else:
                    criteria[crit['name']] = crit['weight']
            else:
                # Fallback for old format
                criteria[crit] = data.get('criteria', {}).get(crit, 0.0)
        
        # Convert scores list to nested dict format
        scores = {}
        for score in data.get('scores', []):
            if isinstance(score, dict):
                alt_name = score['alternative_name']
                crit_name = score['criterion_name']
                if alt_name not in scores:
                    scores[alt_name] = {}
                scores[alt_name][crit_name] = score['value']
        
        return {
            'alternatives': alternatives,
            'criteria': criteria,
            'scores': scores,
            'methodology': data.get('methodology', 'WSM')
        }
