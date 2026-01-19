"""
Accounting System: Double-entry accounting for corporations

Tracks all transactions and maintains accounting records.
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from decimal import Decimal
import json

from .transaction import Transaction, TransactionType


class AccountingSystem:
    """
    Double-entry accounting system for a corporation.
    
    Maintains:
    - Transaction ledger
    - Account balances
    - Financial statements
    """
    
    def __init__(self, corp_id: str, project_path: Optional[Path] = None):
        """
        Initialize accounting system.
        
        Args:
            corp_id: Corporation identifier
            project_path: Project root path
        """
        self.corp_id = corp_id
        self.project_path = Path(project_path) if project_path else Path.cwd()
        
        # Transaction ledger
        self.transactions: List[Transaction] = []
        
        # Account balances (account_name -> balance)
        # Positive = debit balance, Negative = credit balance
        self.accounts: Dict[str, Decimal] = {
            "cash": Decimal("0"),
            "revenue": Decimal("0"),
            "expenses": Decimal("0"),
            "equity": Decimal("0"),
        }
        
        # Ledger file path
        self.ledger_path = (
            self.project_path / "_realms" / "bureaucracy_realm" / "corporations" 
            / self.corp_id / "financials" / "ledger.json"
        )
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing ledger if available
        self._load_ledger()
    
    def _load_ledger(self) -> None:
        """Load transaction ledger from disk."""
        if self.ledger_path.exists():
            data = json.loads(self.ledger_path.read_text(encoding="utf-8"))
            
            # Load transactions
            self.transactions = [
                Transaction.from_dict(t) for t in data.get("transactions", [])
            ]
            
            # Recalculate account balances
            self._recalculate_accounts()
    
    def _save_ledger(self) -> None:
        """Save transaction ledger to disk."""
        data = {
            "corp_id": self.corp_id,
            "transactions": [t.to_dict() for t in self.transactions],
            "accounts": {k: float(v) for k, v in self.accounts.items()},
            "last_updated": datetime.utcnow().isoformat()
        }
        
        self.ledger_path.write_text(
            json.dumps(data, indent=2),
            encoding="utf-8"
        )
    
    def record_transaction(self, transaction: Transaction) -> None:
        """
        Record a transaction in the ledger.
        
        Args:
            transaction: Transaction to record
        """
        # Add to ledger
        self.transactions.append(transaction)
        
        # Apply accounting entries
        entries = transaction.get_accounting_entries()
        for account, amount in entries.items():
            if account not in self.accounts:
                self.accounts[account] = Decimal("0")
            self.accounts[account] += Decimal(str(amount))
        
        # Save ledger
        self._save_ledger()
    
    def _recalculate_accounts(self) -> None:
        """Recalculate all account balances from transactions."""
        # Reset accounts
        self.accounts = {
            "cash": Decimal("0"),
            "revenue": Decimal("0"),
            "expenses": Decimal("0"),
            "equity": Decimal("0"),
        }
        
        # Reapply all transactions
        for transaction in self.transactions:
            entries = transaction.get_accounting_entries()
            for account, amount in entries.items():
                if account not in self.accounts:
                    self.accounts[account] = Decimal("0")
                self.accounts[account] += Decimal(str(amount))
    
    def get_account_balance(self, account_name: str) -> Decimal:
        """
        Get balance for an account.
        
        Args:
            account_name: Account name
            
        Returns:
            Account balance (0 if account doesn't exist)
        """
        return self.accounts.get(account_name, Decimal("0"))
    
    def get_cash_balance(self) -> Decimal:
        """Get cash account balance."""
        return self.get_account_balance("cash")
    
    def get_total_revenue(self) -> Decimal:
        """Get total revenue (credit balance, so negative)."""
        return -self.get_account_balance("revenue")
    
    def get_total_expenses(self) -> Decimal:
        """Get total expenses (debit balance, so positive)."""
        return self.get_account_balance("expenses")
    
    def get_net_income(self) -> Decimal:
        """Get net income (revenue - expenses)."""
        return self.get_total_revenue() - self.get_total_expenses()
    
    def get_transactions_by_type(self, transaction_type: TransactionType) -> List[Transaction]:
        """
        Get all transactions of a specific type.
        
        Args:
            transaction_type: Transaction type to filter
            
        Returns:
            List of matching transactions
        """
        return [t for t in self.transactions if t.transaction_type == transaction_type]
    
    def get_transactions_by_date_range(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Transaction]:
        """
        Get transactions within a date range.
        
        Args:
            start_date: Start date (inclusive)
            end_date: End date (inclusive)
            
        Returns:
            List of matching transactions
        """
        filtered = self.transactions
        
        if start_date:
            filtered = [t for t in filtered if t.timestamp >= start_date]
        
        if end_date:
            filtered = [t for t in filtered if t.timestamp <= end_date]
        
        return filtered
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert accounting system to dictionary."""
        return {
            "corp_id": self.corp_id,
            "transaction_count": len(self.transactions),
            "accounts": {k: float(v) for k, v in self.accounts.items()},
            "cash_balance": float(self.get_cash_balance()),
            "total_revenue": float(self.get_total_revenue()),
            "total_expenses": float(self.get_total_expenses()),
            "net_income": float(self.get_net_income())
        }
