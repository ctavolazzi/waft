"""
Economic Engine: Transaction system and economic simulation

Handles economic transactions, accounting, and market mechanisms.
"""

from .accounting import AccountingSystem
from .transaction import Transaction, TransactionType

__all__ = [
    "Transaction",
    "TransactionType",
    "AccountingSystem",
]
