"""
Transaction: Economic transaction system

Represents economic transactions (invoices, salaries, expenses, investments)
with double-entry accounting support.
"""

from decimal import Decimal
from typing import Dict, Any, Optional
from datetime import datetime
from enum import Enum
import json

from ..security import validate_financial_amount


class TransactionType(Enum):
    """Types of economic transactions."""
    SALARY = "salary"  # Salary payment to employee
    VENDOR_INVOICE = "vendor_invoice"  # Invoice from vendor (expense)
    CUSTOMER_INVOICE = "customer_invoice"  # Invoice to customer (revenue)
    INVESTMENT = "investment"  # Capital investment
    EXPENSE = "expense"  # General expense
    REVENUE = "revenue"  # General revenue
    ASSET_PURCHASE = "asset_purchase"  # Purchase of asset
    LOAN = "loan"  # Loan received or paid


class Transaction:
    """
    An economic transaction.
    
    Represents a single economic event with:
    - Amount and currency
    - Transaction type
    - Parties involved (from/to)
    - Description and metadata
    - Timestamp
    - Double-entry accounting entries
    """
    
    def __init__(
        self,
        transaction_id: str,
        transaction_type: TransactionType,
        amount: Decimal,
        description: str = "",
        from_party: Optional[str] = None,
        to_party: Optional[str] = None,
        timestamp: Optional[datetime] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a transaction.
        
        Args:
            transaction_id: Unique transaction identifier
            transaction_type: Type of transaction
            amount: Transaction amount (positive)
            description: Transaction description
            from_party: Party paying/sending (for expenses, salaries)
            to_party: Party receiving (for revenue, investments)
            timestamp: Transaction timestamp
            metadata: Additional transaction metadata
            
        Raises:
            ValueError: If amount is invalid or negative
        """
        # CRITICAL: Validate amount is positive
        if not validate_financial_amount(Decimal(str(amount)), min_amount=Decimal("0"), allow_negative=False):
            raise ValueError(f"Invalid transaction amount: {amount} (must be positive)")
        
        self.transaction_id = transaction_id
        self.transaction_type = transaction_type
        self.amount = Decimal(str(amount))
        self.description = description
        self.from_party = from_party
        self.to_party = to_party
        self.timestamp = timestamp or datetime.utcnow()
        self.metadata = metadata or {}
        
        # Invoice reference (if this transaction is related to an invoice)
        self.invoice_id: Optional[str] = None
        self.invoice_path: Optional[str] = None
    
    def is_expense(self) -> bool:
        """Check if transaction is an expense."""
        return self.transaction_type in [
            TransactionType.SALARY,
            TransactionType.VENDOR_INVOICE,
            TransactionType.EXPENSE,
            TransactionType.ASSET_PURCHASE
        ]
    
    def is_revenue(self) -> bool:
        """Check if transaction is revenue."""
        return self.transaction_type in [
            TransactionType.CUSTOMER_INVOICE,
            TransactionType.REVENUE,
            TransactionType.INVESTMENT
        ]
    
    def get_accounting_entries(self) -> Dict[str, Decimal]:
        """
        Get double-entry accounting entries for this transaction.
        
        Returns:
            Dictionary mapping account names to amounts (positive = debit, negative = credit)
        """
        entries = {}
        
        if self.transaction_type == TransactionType.SALARY:
            # Debit: Salary Expense, Credit: Cash
            entries["salary_expense"] = self.amount
            entries["cash"] = -self.amount
        
        elif self.transaction_type == TransactionType.VENDOR_INVOICE:
            # Debit: Expense/Asset, Credit: Accounts Payable or Cash
            account = self.metadata.get("expense_account", "expenses")
            entries[account] = self.amount
            entries["cash"] = -self.amount  # Assuming immediate payment
        
        elif self.transaction_type == TransactionType.CUSTOMER_INVOICE:
            # Debit: Accounts Receivable or Cash, Credit: Revenue
            entries["cash"] = self.amount  # Assuming immediate payment
            entries["revenue"] = -self.amount
        
        elif self.transaction_type == TransactionType.INVESTMENT:
            # Debit: Cash, Credit: Equity
            entries["cash"] = self.amount
            entries["equity"] = -self.amount
        
        elif self.transaction_type == TransactionType.EXPENSE:
            # Debit: Expense, Credit: Cash
            account = self.metadata.get("expense_account", "expenses")
            entries[account] = self.amount
            entries["cash"] = -self.amount
        
        elif self.transaction_type == TransactionType.REVENUE:
            # Debit: Cash, Credit: Revenue
            entries["cash"] = self.amount
            entries["revenue"] = -self.amount
        
        elif self.transaction_type == TransactionType.ASSET_PURCHASE:
            # Debit: Asset, Credit: Cash
            asset_type = self.metadata.get("asset_type", "equipment")
            entries[f"asset_{asset_type}"] = self.amount
            entries["cash"] = -self.amount
        
        elif self.transaction_type == TransactionType.LOAN:
            # Debit: Cash (if receiving), Credit: Liability (if receiving)
            # Reverse if paying
            if self.metadata.get("loan_direction") == "receiving":
                entries["cash"] = self.amount
                entries["liability_loan"] = -self.amount
            else:
                entries["cash"] = -self.amount
                entries["liability_loan"] = self.amount
        
        return entries
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert transaction to dictionary."""
        return {
            "transaction_id": self.transaction_id,
            "transaction_type": self.transaction_type.value,
            "amount": float(self.amount),
            "description": self.description,
            "from_party": self.from_party,
            "to_party": self.to_party,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
            "invoice_id": self.invoice_id,
            "invoice_path": self.invoice_path
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Transaction":
        """Create Transaction from dictionary."""
        transaction = cls(
            transaction_id=data["transaction_id"],
            transaction_type=TransactionType(data["transaction_type"]),
            amount=Decimal(str(data["amount"])),
            description=data.get("description", ""),
            from_party=data.get("from_party"),
            to_party=data.get("to_party"),
            timestamp=datetime.fromisoformat(data.get("timestamp", datetime.utcnow().isoformat())),
            metadata=data.get("metadata", {})
        )
        
        transaction.invoice_id = data.get("invoice_id")
        transaction.invoice_path = data.get("invoice_path")
        
        return transaction


def create_salary_transaction(
    transaction_id: str,
    employee_id: str,
    amount: Decimal,
    period: str = "monthly",
    description: Optional[str] = None
) -> Transaction:
    """
    Create a salary payment transaction.
    
    Args:
        transaction_id: Unique transaction ID
        employee_id: Employee (Being) ID
        amount: Salary amount (must be positive)
        period: Payment period (monthly, biweekly, etc.)
        description: Optional description
        
    Returns:
        Transaction object
        
    Raises:
        ValueError: If amount is invalid or negative
    """
    # CRITICAL: Validate amount (Transaction.__init__ will also validate, but validate here for clearer error)
    if not validate_financial_amount(amount, min_amount=Decimal("0"), allow_negative=False):
        raise ValueError(f"Invalid salary amount: {amount} (must be positive)")
    
    if description is None:
        description = f"Salary payment - {period}"
    
    return Transaction(
        transaction_id=transaction_id,
        transaction_type=TransactionType.SALARY,
        amount=amount,
        description=description,
        from_party="corporation",
        to_party=employee_id,
        metadata={"period": period, "employee_id": employee_id}
    )


def create_vendor_invoice_transaction(
    transaction_id: str,
    vendor_name: str,
    amount: Decimal,
    description: str,
    expense_account: str = "expenses"
) -> Transaction:
    """
    Create a vendor invoice transaction (expense).
    
    Args:
        transaction_id: Unique transaction ID
        vendor_name: Vendor name
        amount: Invoice amount (must be positive)
        description: Invoice description
        expense_account: Expense account name
        
    Returns:
        Transaction object
        
    Raises:
        ValueError: If amount is invalid or negative
    """
    # CRITICAL: Validate amount
    if not validate_financial_amount(amount, min_amount=Decimal("0"), allow_negative=False):
        raise ValueError(f"Invalid invoice amount: {amount} (must be positive)")
    
    return Transaction(
        transaction_id=transaction_id,
        transaction_type=TransactionType.VENDOR_INVOICE,
        amount=amount,
        description=description,
        from_party="corporation",
        to_party=vendor_name,
        metadata={"expense_account": expense_account, "vendor": vendor_name}
    )


def create_customer_invoice_transaction(
    transaction_id: str,
    customer_name: str,
    amount: Decimal,
    description: str
) -> Transaction:
    """
    Create a customer invoice transaction (revenue).
    
    Args:
        transaction_id: Unique transaction ID
        customer_name: Customer name
        amount: Invoice amount (must be positive)
        description: Invoice description
        
    Returns:
        Transaction object
        
    Raises:
        ValueError: If amount is invalid or negative
    """
    # CRITICAL: Validate amount
    if not validate_financial_amount(amount, min_amount=Decimal("0"), allow_negative=False):
        raise ValueError(f"Invalid invoice amount: {amount} (must be positive)")
    
    return Transaction(
        transaction_id=transaction_id,
        transaction_type=TransactionType.CUSTOMER_INVOICE,
        amount=amount,
        description=description,
        from_party=customer_name,
        to_party="corporation",
        metadata={"customer": customer_name}
    )
