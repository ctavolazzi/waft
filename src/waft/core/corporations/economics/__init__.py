"""
Economic Engine: Transaction system and economic simulation

Handles economic transactions, accounting, and market mechanisms.
"""

from .transaction import Transaction, TransactionType
from .accounting import AccountingSystem

__all__ = [
    "Transaction",
    "TransactionType",
    "AccountingSystem",
]
