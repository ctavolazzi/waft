"""
Financial Documents: Budget and Balance Sheet Management

Financial document management for the Paperwork God system.
Handles budgets, balance sheets, and financial tracking.
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
from decimal import Decimal
import json


class BudgetItem:
    """A single budget line item."""
    
    def __init__(
        self,
        category: str,
        description: str,
        budgeted_amount: Decimal,
        actual_amount: Decimal = Decimal("0.00"),
        notes: Optional[str] = None
    ):
        """
        Initialize a budget item.
        
        Args:
            category: Budget category (e.g., "Personnel", "Operations", "Infrastructure")
            description: Item description
            budgeted_amount: Budgeted amount
            actual_amount: Actual amount spent/received
            notes: Additional notes
        """
        self.category = category
        self.description = description
        self.budgeted_amount = budgeted_amount
        self.actual_amount = actual_amount
        self.notes = notes
    
    @property
    def variance(self) -> Decimal:
        """Calculate variance (actual - budgeted)."""
        return self.actual_amount - self.budgeted_amount
    
    @property
    def variance_percent(self) -> float:
        """Calculate variance as percentage."""
        if self.budgeted_amount == 0:
            return 0.0
        return float((self.variance / self.budgeted_amount) * 100)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "category": self.category,
            "description": self.description,
            "budgeted_amount": str(self.budgeted_amount),
            "actual_amount": str(self.actual_amount),
            "variance": str(self.variance),
            "variance_percent": self.variance_percent,
            "notes": self.notes
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BudgetItem":
        """Create from dictionary."""
        return cls(
            category=data["category"],
            description=data["description"],
            budgeted_amount=Decimal(data["budgeted_amount"]),
            actual_amount=Decimal(data.get("actual_amount", "0.00")),
            notes=data.get("notes")
        )


class Budget:
    """A budget document."""
    
    def __init__(
        self,
        budget_id: str,
        name: str,
        period_start: str,
        period_end: str,
        items: Optional[List[BudgetItem]] = None,
        created_at: Optional[str] = None,
        last_updated: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a budget.
        
        Args:
            budget_id: Unique budget identifier
            name: Budget name
            period_start: Budget period start (ISO format)
            period_end: Budget period end (ISO format)
            items: List of budget items
            created_at: Creation timestamp
            last_updated: Last update timestamp
            metadata: Additional metadata
        """
        self.budget_id = budget_id
        self.name = name
        self.period_start = period_start
        self.period_end = period_end
        self.items = items or []
        self.created_at = created_at or datetime.now().isoformat()
        self.last_updated = last_updated or datetime.now().isoformat()
        self.metadata = metadata or {}
    
    @property
    def total_budgeted(self) -> Decimal:
        """Calculate total budgeted amount."""
        return sum(item.budgeted_amount for item in self.items)
    
    @property
    def total_actual(self) -> Decimal:
        """Calculate total actual amount."""
        return sum(item.actual_amount for item in self.items)
    
    @property
    def total_variance(self) -> Decimal:
        """Calculate total variance."""
        return self.total_actual - self.total_budgeted
    
    @property
    def total_variance_percent(self) -> float:
        """Calculate total variance as percentage."""
        if self.total_budgeted == 0:
            return 0.0
        return float((self.total_variance / self.total_budgeted) * 100)
    
    def get_category_totals(self) -> Dict[str, Dict[str, Decimal]]:
        """Get totals by category."""
        category_totals = {}
        for item in self.items:
            if item.category not in category_totals:
                category_totals[item.category] = {
                    "budgeted": Decimal("0.00"),
                    "actual": Decimal("0.00")
                }
            category_totals[item.category]["budgeted"] += item.budgeted_amount
            category_totals[item.category]["actual"] += item.actual_amount
        
        return category_totals
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "budget_id": self.budget_id,
            "name": self.name,
            "period_start": self.period_start,
            "period_end": self.period_end,
            "items": [item.to_dict() for item in self.items],
            "totals": {
                "budgeted": str(self.total_budgeted),
                "actual": str(self.total_actual),
                "variance": str(self.total_variance),
                "variance_percent": self.total_variance_percent
            },
            "category_totals": {
                cat: {
                    "budgeted": str(totals["budgeted"]),
                    "actual": str(totals["actual"]),
                    "variance": str(totals["actual"] - totals["budgeted"])
                }
                for cat, totals in self.get_category_totals().items()
            },
            "created_at": self.created_at,
            "last_updated": self.last_updated,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Budget":
        """Create from dictionary."""
        return cls(
            budget_id=data["budget_id"],
            name=data["name"],
            period_start=data["period_start"],
            period_end=data["period_end"],
            items=[BudgetItem.from_dict(item) for item in data.get("items", [])],
            created_at=data.get("created_at"),
            last_updated=data.get("last_updated"),
            metadata=data.get("metadata", {})
        )


class BalanceSheetItem:
    """A balance sheet line item."""
    
    def __init__(
        self,
        account: str,
        description: str,
        amount: Decimal,
        account_type: str,  # "asset", "liability", "equity"
        notes: Optional[str] = None
    ):
        """
        Initialize a balance sheet item.
        
        Args:
            account: Account name
            description: Item description
            amount: Account amount
            account_type: Type of account (asset, liability, equity)
            notes: Additional notes
        """
        self.account = account
        self.description = description
        self.amount = amount
        self.account_type = account_type
        self.notes = notes
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "account": self.account,
            "description": self.description,
            "amount": str(self.amount),
            "account_type": self.account_type,
            "notes": self.notes
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BalanceSheetItem":
        """Create from dictionary."""
        return cls(
            account=data["account"],
            description=data["description"],
            amount=Decimal(data["amount"]),
            account_type=data["account_type"],
            notes=data.get("notes")
        )


class BalanceSheet:
    """A balance sheet document."""
    
    def __init__(
        self,
        balance_sheet_id: str,
        name: str,
        as_of_date: str,
        items: Optional[List[BalanceSheetItem]] = None,
        created_at: Optional[str] = None,
        last_updated: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a balance sheet.
        
        Args:
            balance_sheet_id: Unique balance sheet identifier
            name: Balance sheet name
            as_of_date: Balance sheet date (ISO format)
            items: List of balance sheet items
            created_at: Creation timestamp
            last_updated: Last update timestamp
            metadata: Additional metadata
        """
        self.balance_sheet_id = balance_sheet_id
        self.name = name
        self.as_of_date = as_of_date
        self.items = items or []
        self.created_at = created_at or datetime.now().isoformat()
        self.last_updated = last_updated or datetime.now().isoformat()
        self.metadata = metadata or {}
    
    @property
    def total_assets(self) -> Decimal:
        """Calculate total assets."""
        return sum(
            item.amount for item in self.items
            if item.account_type == "asset"
        )
    
    @property
    def total_liabilities(self) -> Decimal:
        """Calculate total liabilities."""
        return sum(
            item.amount for item in self.items
            if item.account_type == "liability"
        )
    
    @property
    def total_equity(self) -> Decimal:
        """Calculate total equity."""
        return sum(
            item.amount for item in self.items
            if item.account_type == "equity"
        )
    
    @property
    def is_balanced(self) -> bool:
        """Check if balance sheet balances (Assets = Liabilities + Equity)."""
        return abs(self.total_assets - (self.total_liabilities + self.total_equity)) < Decimal("0.01")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "balance_sheet_id": self.balance_sheet_id,
            "name": self.name,
            "as_of_date": self.as_of_date,
            "items": [item.to_dict() for item in self.items],
            "totals": {
                "assets": str(self.total_assets),
                "liabilities": str(self.total_liabilities),
                "equity": str(self.total_equity),
                "liabilities_plus_equity": str(self.total_liabilities + self.total_equity),
                "is_balanced": self.is_balanced
            },
            "created_at": self.created_at,
            "last_updated": self.last_updated,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BalanceSheet":
        """Create from dictionary."""
        return cls(
            balance_sheet_id=data["balance_sheet_id"],
            name=data["name"],
            as_of_date=data["as_of_date"],
            items=[BalanceSheetItem.from_dict(item) for item in data.get("items", [])],
            created_at=data.get("created_at"),
            last_updated=data.get("last_updated"),
            metadata=data.get("metadata", {})
        )


class FinancialDocumentsManager:
    """Manager for financial documents (budgets and balance sheets)."""
    
    def __init__(self, project_path: Optional[Path] = None):
        """
        Initialize financial documents manager.
        
        Args:
            project_path: Path to project root
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)
        
        self.project_path = project_path
        self.pantheon_path = project_path / "_pantheon"
        self.financial_path = self.pantheon_path / "paperwork_god" / "financial"
        
        # Ensure directory structure exists
        self.financial_path.mkdir(parents=True, exist_ok=True)
        (self.financial_path / "budgets").mkdir(parents=True, exist_ok=True)
        (self.financial_path / "balance_sheets").mkdir(parents=True, exist_ok=True)
    
    def save_budget(self, budget: Budget) -> Path:
        """Save budget to file."""
        budget_file = self.financial_path / "budgets" / f"{budget.budget_id}.json"
        budget.last_updated = datetime.now().isoformat()
        budget_file.write_text(
            json.dumps(budget.to_dict(), indent=2),
            encoding="utf-8"
        )
        return budget_file
    
    def load_budget(self, budget_id: str) -> Optional[Budget]:
        """Load budget from file."""
        budget_file = self.financial_path / "budgets" / f"{budget_id}.json"
        if not budget_file.exists():
            return None
        
        data = json.loads(budget_file.read_text(encoding="utf-8"))
        return Budget.from_dict(data)
    
    def list_budgets(self) -> List[Budget]:
        """List all budgets."""
        budgets = []
        budgets_dir = self.financial_path / "budgets"
        if budgets_dir.exists():
            for budget_file in budgets_dir.glob("*.json"):
                data = json.loads(budget_file.read_text(encoding="utf-8"))
                budgets.append(Budget.from_dict(data))
        return budgets
    
    def save_balance_sheet(self, balance_sheet: BalanceSheet) -> Path:
        """Save balance sheet to file."""
        bs_file = self.financial_path / "balance_sheets" / f"{balance_sheet.balance_sheet_id}.json"
        balance_sheet.last_updated = datetime.now().isoformat()
        bs_file.write_text(
            json.dumps(balance_sheet.to_dict(), indent=2),
            encoding="utf-8"
        )
        return bs_file
    
    def load_balance_sheet(self, balance_sheet_id: str) -> Optional[BalanceSheet]:
        """Load balance sheet from file."""
        bs_file = self.financial_path / "balance_sheets" / f"{balance_sheet_id}.json"
        if not bs_file.exists():
            return None
        
        data = json.loads(bs_file.read_text(encoding="utf-8"))
        return BalanceSheet.from_dict(data)
    
    def list_balance_sheets(self) -> List[BalanceSheet]:
        """List all balance sheets."""
        balance_sheets = []
        bs_dir = self.financial_path / "balance_sheets"
        if bs_dir.exists():
            for bs_file in bs_dir.glob("*.json"):
                data = json.loads(bs_file.read_text(encoding="utf-8"))
                balance_sheets.append(BalanceSheet.from_dict(data))
        return balance_sheets
