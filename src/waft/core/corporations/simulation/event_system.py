"""
Event System: Economic event generation

Generates economic events (payroll, invoices, expenses) based on time and state.
"""

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any


class EventType(Enum):
    """Types of economic events."""

    PAYROLL = "payroll"  # Process employee salaries
    VENDOR_INVOICE = "vendor_invoice"  # Receive vendor invoice
    CUSTOMER_INVOICE = "customer_invoice"  # Send customer invoice
    EXPENSE = "expense"  # General expense
    INVESTMENT = "investment"  # Capital investment
    MONTHLY_REPORT = "monthly_report"  # Generate monthly report
    QUARTERLY_REPORT = "quarterly_report"  # Generate quarterly report


class EconomicEvent:
    """
    An economic event to be processed.

    Represents something that should happen in the simulation,
    like processing payroll or generating invoices.
    """

    def __init__(
        self,
        event_type: EventType,
        event_date: datetime,
        description: str = "",
        metadata: dict[str, Any] | None = None,
    ):
        """
        Initialize economic event.

        Args:
            event_type: Type of event
            event_date: Date event should occur
            description: Event description
            metadata: Additional event data
        """
        self.event_type = event_type
        self.event_date = event_date
        self.description = description
        self.metadata = metadata or {}
        self.processed = False
        self.processed_at: datetime | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert event to dictionary."""
        return {
            "event_type": self.event_type.value,
            "event_date": self.event_date.isoformat(),
            "description": self.description,
            "metadata": self.metadata,
            "processed": self.processed,
            "processed_at": self.processed_at.isoformat() if self.processed_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EconomicEvent":
        """Create EconomicEvent from dictionary."""
        event = cls(
            event_type=EventType(data["event_type"]),
            event_date=datetime.fromisoformat(data["event_date"]),
            description=data.get("description", ""),
            metadata=data.get("metadata", {}),
        )
        event.processed = data.get("processed", False)
        if data.get("processed_at"):
            event.processed_at = datetime.fromisoformat(data["processed_at"])
        return event


def generate_payroll_events(
    employees: list[dict[str, Any]], event_date: datetime, period: str = "monthly"
) -> list[EconomicEvent]:
    """
    Generate payroll events for employees.

    Args:
        employees: List of employee dictionaries with being_id and salary
        event_date: Date for payroll event
        period: Payment period (monthly, biweekly, etc.)

    Returns:
        List of payroll events
    """
    events = []

    for employee in employees:
        if employee.get("status") != "active":
            continue

        being_id = employee["being_id"]
        salary = employee.get("salary")

        if not salary:
            continue

        # Calculate payment amount based on period
        if period == "monthly":
            amount = Decimal(str(salary)) / Decimal("12")
        elif period == "biweekly":
            amount = Decimal(str(salary)) / Decimal("26")
        else:
            amount = Decimal(str(salary)) / Decimal("12")  # Default to monthly

        event = EconomicEvent(
            event_type=EventType.PAYROLL,
            event_date=event_date,
            description=f"Payroll payment for {being_id}",
            metadata={
                "employee_id": being_id,
                "amount": float(amount),
                "period": period,
                "annual_salary": float(salary),
            },
        )
        events.append(event)

    return events


def generate_monthly_expenses(
    expense_items: list[dict[str, Any]], event_date: datetime
) -> list[EconomicEvent]:
    """
    Generate monthly expense events.

    Args:
        expense_items: List of expense items (rent, utilities, etc.)
        event_date: Date for expense events

    Returns:
        List of expense events
    """
    events = []

    for expense in expense_items:
        event = EconomicEvent(
            event_type=EventType.EXPENSE,
            event_date=event_date,
            description=expense.get("description", "Monthly expense"),
            metadata={
                "amount": expense.get("amount", 0),
                "category": expense.get("category", "general"),
                "vendor": expense.get("vendor"),
            },
        )
        events.append(event)

    return events
