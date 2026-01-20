"""
Corporations System: Economic Simulation for Corporate Entities

Manages corporations, their financial state, employees (Beings), and economic transactions.
Integrates with Typst for document generation and supports repeatable economic simulations.
"""

from .corporation import Corporation
from .corporations_system import CorporationsSystem
from .financial_state import FinancialState
from .security import (
    read_secure_json,
    validate_corp_id,
    validate_financial_amount,
    validate_path_in_project,
    write_secure_file,
)

__all__ = [
    "CorporationsSystem",
    "Corporation",
    "FinancialState",
    "validate_corp_id",
    "validate_path_in_project",
    "validate_financial_amount",
    "write_secure_file",
    "read_secure_json",
]
