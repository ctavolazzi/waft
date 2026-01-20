"""
Financial State: Track corporation financial health

Tracks cash, assets, liabilities, equity, revenue, and expenses using
double-entry accounting principles.
"""

from decimal import Decimal
from typing import Dict, Any, Optional
from datetime import datetime
import json

from .security import validate_financial_amount


class FinancialState:
    """
    Financial state tracking for a corporation.
    
    Tracks:
    - Cash: Liquid assets
    - Assets: Non-cash assets (equipment, property, etc.)
    - Liabilities: Debts and obligations
    - Equity: Owner's equity (assets - liabilities)
    - Revenue: Income from operations
    - Expenses: Operating costs
    """
    
    def __init__(
        self,
        cash: Decimal = Decimal("0"),
        assets: Optional[Dict[str, Decimal]] = None,
        liabilities: Optional[Dict[str, Decimal]] = None,
        revenue: Decimal = Decimal("0"),
        expenses: Decimal = Decimal("0"),
        initial_equity: Optional[Decimal] = None
    ):
        """
        Initialize financial state.
        
        Args:
            cash: Starting cash balance
            assets: Dictionary of asset types and values
            liabilities: Dictionary of liability types and values
            revenue: Total revenue accumulated
            expenses: Total expenses accumulated
            initial_equity: Initial equity (if None, calculated as assets - liabilities)
        """
        self.cash = Decimal(str(cash))
        self.assets = assets or {}
        self.liabilities = liabilities or {}
        self.revenue = Decimal(str(revenue))
        self.expenses = Decimal(str(expenses))
        
        # Calculate equity if not provided
        if initial_equity is not None:
            self.equity = Decimal(str(initial_equity))
        else:
            self.equity = self._calculate_equity()
        
        # Transaction history
        self.transactions: list[Dict[str, Any]] = []
        self.last_updated = datetime.utcnow()
    
    def _calculate_equity(self) -> Decimal:
        """Calculate equity as assets - liabilities."""
        total_assets = self.cash + sum(self.assets.values())
        total_liabilities = sum(self.liabilities.values())
        return total_assets - total_liabilities
    
    def update_cash(self, amount: Decimal, description: str = "") -> None:
        """
        Update cash balance.
        
        Args:
            amount: Amount to add (positive) or subtract (negative)
            description: Description of the transaction
            
        Raises:
            ValueError: If amount is invalid or cash would go negative
        """
        # CRITICAL: Validate amount
        if not validate_financial_amount(amount, allow_negative=True):
            raise ValueError(f"Invalid amount: {amount}")
        
        # HIGH: Check if cash would go negative
        new_cash = self.cash + Decimal(str(amount))
        if new_cash < 0:
            raise ValueError(f"Insufficient funds: cash would go negative (current: {self.cash}, change: {amount})")
        
        self.cash = new_cash
        self._record_transaction("cash", amount, description)
        self._update_equity()
        self.last_updated = datetime.utcnow()
    
    def add_asset(self, asset_type: str, value: Decimal, description: str = "") -> None:
        """
        Add an asset.
        
        Args:
            asset_type: Type of asset (e.g., "equipment", "property")
            value: Asset value (must be positive)
            description: Description of the asset
            
        Raises:
            ValueError: If value is invalid or negative
        """
        # CRITICAL: Validate value is positive
        if not validate_financial_amount(value, min_amount=Decimal("0"), allow_negative=False):
            raise ValueError(f"Invalid asset value: {value} (must be positive)")
        
        if asset_type not in self.assets:
            self.assets[asset_type] = Decimal("0")
        self.assets[asset_type] += Decimal(str(value))
        self._record_transaction("asset", value, f"{asset_type}: {description}")
        self._update_equity()
        self.last_updated = datetime.utcnow()
    
    def add_liability(self, liability_type: str, value: Decimal, description: str = "") -> None:
        """
        Add a liability.
        
        Args:
            liability_type: Type of liability (e.g., "loan", "accounts_payable")
            value: Liability value (must be positive)
            description: Description of the liability
            
        Raises:
            ValueError: If value is invalid or negative
        """
        # CRITICAL: Validate value is positive
        if not validate_financial_amount(value, min_amount=Decimal("0"), allow_negative=False):
            raise ValueError(f"Invalid liability value: {value} (must be positive)")
        
        if liability_type not in self.liabilities:
            self.liabilities[liability_type] = Decimal("0")
        self.liabilities[liability_type] += Decimal(str(value))
        self._record_transaction("liability", value, f"{liability_type}: {description}")
        self._update_equity()
        self.last_updated = datetime.utcnow()
    
    def record_revenue(self, amount: Decimal, description: str = "") -> None:
        """
        Record revenue.
        
        Args:
            amount: Revenue amount (must be positive)
            description: Description of revenue source
            
        Raises:
            ValueError: If amount is invalid or negative
        """
        # CRITICAL: Validate amount is positive
        if not validate_financial_amount(amount, min_amount=Decimal("0"), allow_negative=False):
            raise ValueError(f"Invalid revenue amount: {amount} (must be positive)")
        
        self.revenue += Decimal(str(amount))
        self.cash += Decimal(str(amount))  # Revenue increases cash
        self._record_transaction("revenue", amount, description)
        self._update_equity()
        self.last_updated = datetime.utcnow()
    
    def record_expense(self, amount: Decimal, description: str = "") -> None:
        """
        Record an expense.
        
        Args:
            amount: Expense amount (must be positive)
            description: Description of expense
            
        Raises:
            ValueError: If amount is invalid, negative, or cash would go negative
        """
        # CRITICAL: Validate amount is positive
        if not validate_financial_amount(amount, min_amount=Decimal("0"), allow_negative=False):
            raise ValueError(f"Invalid expense amount: {amount} (must be positive)")
        
        # HIGH: Check if cash would go negative
        if self.cash < Decimal(str(amount)):
            raise ValueError(f"Insufficient funds: cannot pay expense of {amount} (cash: {self.cash})")
        
        self.expenses += Decimal(str(amount))
        self.cash -= Decimal(str(amount))  # Expenses decrease cash
        self._record_transaction("expense", amount, description)
        self._update_equity()
        self.last_updated = datetime.utcnow()
    
    def _record_transaction(self, transaction_type: str, amount: Decimal, description: str) -> None:
        """Record a transaction in history."""
        self.transactions.append({
            "type": transaction_type,
            "amount": float(amount),
            "description": description,
            "timestamp": datetime.utcnow().isoformat(),
            "cash_after": float(self.cash),
            "equity_after": float(self.equity)
        })
    
    def _update_equity(self) -> None:
        """Recalculate equity after any change."""
        self.equity = self._calculate_equity()
    
    def get_total_assets(self) -> Decimal:
        """Get total assets (cash + non-cash assets)."""
        return self.cash + sum(self.assets.values())
    
    def get_total_liabilities(self) -> Decimal:
        """Get total liabilities."""
        return sum(self.liabilities.values())
    
    def get_net_income(self) -> Decimal:
        """Get net income (revenue - expenses)."""
        return self.revenue - self.expenses
    
    def get_burn_rate(self, period_days: int = 30) -> Decimal:
        """
        Calculate monthly burn rate based on recent expenses.
        
        Args:
            period_days: Number of days to analyze (default: 30 for monthly)
            
        Returns:
            Estimated monthly burn rate
        """
        # Get expenses from last period_days
        cutoff_date = datetime.utcnow().timestamp() - (period_days * 24 * 60 * 60)
        recent_expenses = [
            t for t in self.transactions
            if t["type"] == "expense" and datetime.fromisoformat(t["timestamp"]).timestamp() > cutoff_date
        ]
        
        if not recent_expenses:
            return Decimal("0")
        
        total_expenses = sum(Decimal(str(t["amount"])) for t in recent_expenses)
        # Project to monthly
        return total_expenses * (Decimal("30") / Decimal(str(period_days)))
    
    def get_runway_months(self) -> Optional[Decimal]:
        """
        Calculate runway in months (how long until cash runs out).
        
        Returns:
            Number of months until cash runs out, or None if burn rate is negative
        """
        burn_rate = self.get_burn_rate()
        if burn_rate <= 0:
            return None  # Not burning cash or generating profit
        
        if self.cash <= 0:
            return Decimal("0")
        
        return self.cash / burn_rate
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert financial state to dictionary."""
        return {
            "cash": float(self.cash),
            "assets": {k: float(v) for k, v in self.assets.items()},
            "liabilities": {k: float(v) for k, v in self.liabilities.items()},
            "equity": float(self.equity),
            "revenue": float(self.revenue),
            "expenses": float(self.expenses),
            "net_income": float(self.get_net_income()),
            "total_assets": float(self.get_total_assets()),
            "total_liabilities": float(self.get_total_liabilities()),
            "burn_rate": float(self.get_burn_rate()),
            "runway_months": float(self.get_runway_months()) if self.get_runway_months() else None,
            "last_updated": self.last_updated.isoformat(),
            "transaction_count": len(self.transactions)
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FinancialState":
        """Create FinancialState from dictionary."""
        state = cls(
            cash=Decimal(str(data.get("cash", 0))),
            assets={k: Decimal(str(v)) for k, v in data.get("assets", {}).items()},
            liabilities={k: Decimal(str(v)) for k, v in data.get("liabilities", {}).items()},
            revenue=Decimal(str(data.get("revenue", 0))),
            expenses=Decimal(str(data.get("expenses", 0)))
        )
        
        # Restore transaction history if available
        if "transactions" in data:
            state.transactions = data["transactions"]
        
        if "last_updated" in data:
            state.last_updated = datetime.fromisoformat(data["last_updated"])
        
        return state
