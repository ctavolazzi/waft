"""
Corporations System: Economic Simulation for Corporate Entities

Manages corporations, their financial state, employees (Beings), and economic transactions.
Integrates with Typst for document generation and supports repeatable economic simulations.
"""

from .corporations_system import CorporationsSystem
from .corporation import Corporation
from .financial_state import FinancialState

__all__ = [
    "CorporationsSystem",
    "Corporation",
    "FinancialState",
]
