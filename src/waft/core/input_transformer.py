"""
Input Transformer - The Gateway (The Airlock)

Sanitizes and validates raw user input (dictionaries/JSON) before it reaches
the strict DecisionMatrix. Acts as a protective layer that handles "dirty"
data and converts it to clean, validated objects.
"""

from typing import Dict, List, Any, Optional
from .decision_matrix import (
    DecisionMatrix, Alternative, Criterion, Score
)


class InputTransformer:
    """
    Transforms raw input data into validated DecisionMatrix objects.
    
    Acts as the "airlock" between user input and the hardened Iron Core,
    sanitizing and validating data before it reaches strict validation.
    """
    
    @staticmethod
    def transform_input(data: Dict[str, Any]) -> DecisionMatrix:
        """
        Transform raw input dictionary into a validated DecisionMatrix.
        
        Args:
            data: Dictionary with keys:
                - 'alternatives': List[str] or List[Dict[str, Any]]
                - 'criteria': Dict[str, float] or Dict[str, Dict[str, Any]]
                - 'scores': Dict[str, Dict[str, float]]
                - 'methodology': str (optional, defaults to "WSM")
        
        Returns:
            Validated DecisionMatrix object
        
        Raises:
            ValueError: If input data is invalid, missing required keys,
                       or contains invalid values (with context)
        """
        try:
            # 1. Schema Check: Ensure required keys exist
            InputTransformer._validate_schema(data)
            
            # 2. Extract and sanitize alternatives
            alternatives = InputTransformer._extract_alternatives(data['alternatives'])
            
            # 3. Extract and sanitize criteria
            criteria = InputTransformer._extract_criteria(data['criteria'])
            
            # 4. Extract and sanitize scores
            scores = InputTransformer._extract_scores(
                data['scores'],
                [alt.name for alt in alternatives],
                [crit.name for crit in criteria]
            )
            
            # 5. Get methodology (optional, defaults to "WSM")
            methodology = data.get('methodology', 'WSM')
            
            # 6. Create DecisionMatrix (this will trigger Iron Core validation)
            matrix = DecisionMatrix(
                alternatives=alternatives,
                criteria=criteria,
                scores=scores,
                methodology=methodology
            )
            
            return matrix
            
        except ValueError as e:
            # Re-raise with context about input data
            raise ValueError(f"Error in input data: {str(e)}") from e
        except KeyError as e:
            raise ValueError(f"Missing required key in input data: {str(e)}") from e
        except (TypeError, AttributeError) as e:
            raise ValueError(f"Invalid data type in input: {str(e)}") from e
    
    @staticmethod
    def _validate_schema(data: Dict[str, Any]) -> None:
        """Validate that required keys exist in input data."""
        required_keys = ['alternatives', 'criteria', 'scores']
        missing_keys = [key for key in required_keys if key not in data]
        
        if missing_keys:
            raise ValueError(f"Missing required keys: {', '.join(missing_keys)}")
    
    @staticmethod
    def _extract_alternatives(alternatives_data: Any) -> List[Alternative]:
        """
        Extract and sanitize alternatives from input data.
        
        Supports:
        - List[str]: ["Option A", "Option B"]
        - List[Dict]: [{"name": "Option A", "description": "..."}]
        """
        if not isinstance(alternatives_data, list):
            raise ValueError(f"alternatives must be a list, got {type(alternatives_data).__name__}")
        
        alternatives = []
        for item in alternatives_data:
            if isinstance(item, str):
                # Simple string: sanitize and create Alternative
                name = InputTransformer._sanitize_name(item)
                alternatives.append(Alternative(name=name))
            elif isinstance(item, dict):
                # Dictionary: extract name and optional description
                if 'name' not in item:
                    raise ValueError("Alternative dict must have 'name' key")
                name = InputTransformer._sanitize_name(item['name'])
                description = item.get('description')
                if description:
                    description = description.strip()
                alternatives.append(Alternative(name=name, description=description))
            else:
                raise ValueError(f"Alternative must be str or dict, got {type(item).__name__}")
        
        return alternatives
    
    @staticmethod
    def _extract_criteria(criteria_data: Any) -> List[Criterion]:
        """
        Extract and sanitize criteria from input data.
        
        Supports:
        - Dict[str, float]: {"Cost": 0.5, "Quality": 0.5}
        - Dict[str, Dict]: {"Cost": {"weight": 0.5, "description": "..."}}
        """
        if not isinstance(criteria_data, dict):
            raise ValueError(f"criteria must be a dict, got {type(criteria_data).__name__}")
        
        criteria = []
        for name, value in criteria_data.items():
            name = InputTransformer._sanitize_name(name)
            
            if isinstance(value, (int, float, str)):
                # Simple weight value (int, float, or numeric string)
                weight = InputTransformer._cast_to_float(value, f"weight for criterion '{name}'")
                criteria.append(Criterion(name=name, weight=weight))
            elif isinstance(value, dict):
                # Dictionary with weight and optional description
                if 'weight' not in value:
                    raise ValueError(f"Criterion '{name}' dict must have 'weight' key")
                weight = InputTransformer._cast_to_float(
                    value['weight'],
                    f"weight for criterion '{name}'"
                )
                description = value.get('description')
                if description:
                    description = description.strip()
                criteria.append(Criterion(name=name, weight=weight, description=description))
            else:
                raise ValueError(
                    f"Criterion '{name}' value must be number, numeric string, or dict, "
                    f"got {type(value).__name__}"
                )
        
        return criteria
    
    @staticmethod
    def _extract_scores(
        scores_data: Any,
        alternative_names: List[str],
        criterion_names: List[str]
    ) -> List[Score]:
        """
        Extract and sanitize scores from input data.
        
        Expected format: Dict[str, Dict[str, Any]]
        {
            "Alternative A": {"Criterion 1": 10, "Criterion 2": 5},
            "Alternative B": {"Criterion 1": 5, "Criterion 2": 10}
        }
        """
        if not isinstance(scores_data, dict):
            raise ValueError(f"scores must be a dict, got {type(scores_data).__name__}")
        
        scores = []
        for alt_name, crit_scores in scores_data.items():
            alt_name = InputTransformer._sanitize_name(alt_name)
            
            # Validate alternative exists
            if alt_name not in alternative_names:
                raise ValueError(f"Alternative '{alt_name}' in scores not found in alternatives list")
            
            if not isinstance(crit_scores, dict):
                raise ValueError(
                    f"Scores for alternative '{alt_name}' must be a dict, "
                    f"got {type(crit_scores).__name__}"
                )
            
            for crit_name, score_value in crit_scores.items():
                crit_name = InputTransformer._sanitize_name(crit_name)
                
                # Validate criterion exists
                if crit_name not in criterion_names:
                    raise ValueError(
                        f"Criterion '{crit_name}' in scores not found in criteria list"
                    )
                
                # Cast score to float
                score_float = InputTransformer._cast_to_float(
                    score_value,
                    f"score for alternative '{alt_name}' on criterion '{crit_name}'"
                )
                
                scores.append(Score(
                    alternative_name=alt_name,
                    criterion_name=crit_name,
                    value=score_float
                ))
        
        return scores
    
    @staticmethod
    def _sanitize_name(name: Any) -> str:
        """
        Sanitize a name by converting to string and trimming whitespace.
        
        Args:
            name: Name to sanitize (can be str, int, etc.)
        
        Returns:
            Sanitized string (trimmed)
        
        Raises:
            ValueError: If name cannot be converted to string
        """
        try:
            name_str = str(name).strip()
            if not name_str:
                raise ValueError("Name cannot be empty after sanitization")
            return name_str
        except Exception as e:
            raise ValueError(f"Invalid name value: {name}") from e
    
    @staticmethod
    def _cast_to_float(value: Any, context: str = "") -> float:
        """
        Safely cast a value to float.
        
        Supports:
        - int -> float
        - float -> float
        - str (numeric) -> float
        
        Args:
            value: Value to cast
            context: Context string for error messages
        
        Returns:
            Float value
        
        Raises:
            ValueError: If value cannot be converted to float
        """
        if isinstance(value, float):
            return value
        elif isinstance(value, int):
            return float(value)
        elif isinstance(value, str):
            # Try to convert string to float
            try:
                return float(value)
            except ValueError:
                raise ValueError(
                    f"Invalid number string for {context}: '{value}' "
                    f"(cannot convert to float)"
                )
        else:
            raise ValueError(
                f"Invalid type for {context}: {type(value).__name__} "
                f"(expected int, float, or numeric string)"
            )
