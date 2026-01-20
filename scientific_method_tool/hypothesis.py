"""
Hypothesis and Variable System

Defines hypotheses and variables for experimental testing.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class VariableType(Enum):
    """Types of variables in experiments."""

    INDEPENDENT = "independent"  # Variable we control
    DEPENDENT = "dependent"  # Variable we measure
    CONTROL = "control"  # Variable we keep constant
    CONFOUNDING = "confounding"  # Variable that might affect results


@dataclass
class Variable:
    """A variable in an experiment."""

    name: str
    type: VariableType
    value: Any
    description: str
    unit: str | None = None
    range: tuple | None = None  # (min, max) for numeric variables

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "type": self.type.value,
            "value": self.value,
            "description": self.description,
            "unit": self.unit,
            "range": self.range,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Variable":
        """Create from dictionary."""
        return cls(
            name=data["name"],
            type=VariableType(data["type"]),
            value=data["value"],
            description=data["description"],
            unit=data.get("unit"),
            range=tuple(data["range"]) if data.get("range") else None,
        )


@dataclass
class Hypothesis:
    """A testable hypothesis."""

    statement: str
    prediction: str
    variables: list[Variable] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    verified: bool | None = None
    confidence: float = 0.0  # 0.0-1.0

    def add_variable(self, variable: Variable):
        """Add a variable to the hypothesis."""
        self.variables.append(variable)

    def get_variable(self, name: str) -> Variable | None:
        """Get variable by name."""
        for var in self.variables:
            if var.name == name:
                return var
        return None

    def get_independent_variables(self) -> list[Variable]:
        """Get all independent variables."""
        return [v for v in self.variables if v.type == VariableType.INDEPENDENT]

    def get_dependent_variables(self) -> list[Variable]:
        """Get all dependent variables."""
        return [v for v in self.variables if v.type == VariableType.DEPENDENT]

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "statement": self.statement,
            "prediction": self.prediction,
            "variables": [v.to_dict() for v in self.variables],
            "created_at": self.created_at,
            "verified": self.verified,
            "confidence": self.confidence,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Hypothesis":
        """Create from dictionary."""
        return cls(
            statement=data["statement"],
            prediction=data["prediction"],
            variables=[Variable.from_dict(v) for v in data.get("variables", [])],
            created_at=data.get("created_at", datetime.now().isoformat()),
            verified=data.get("verified"),
            confidence=data.get("confidence", 0.0),
        )
