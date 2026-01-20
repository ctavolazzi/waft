"""
Corporation Simulator: Main simulation engine

Orchestrates economic simulation with tick-based cycles, event processing,
and transaction generation.
"""

import json
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any

from ..corporation import Corporation
from ..economics.accounting import AccountingSystem
from ..economics.transaction import (
    Transaction,
    create_salary_transaction,
    create_vendor_invoice_transaction,
)
from ..security import (
    read_secure_json,
    set_directory_permissions,
    validate_path_in_project,
    write_secure_file,
)
from .event_system import (
    EconomicEvent,
    EventType,
    generate_monthly_expenses,
    generate_payroll_events,
)
from .time_manager import TimeManager, TimeUnit


class CorporationSimulator:
    """
    Main simulator for a corporation's economic activity.

    Handles:
    - Time progression (daily/weekly/monthly cycles)
    - Economic event processing
    - Transaction generation
    - Financial state updates
    - Invoice generation
    """

    def __init__(
        self,
        corporation: Corporation,
        time_unit: TimeUnit = TimeUnit.DAILY,
        start_date: datetime | None = None,
    ):
        """
        Initialize corporation simulator.

        Args:
            corporation: Corporation to simulate
            time_unit: Time unit for each tick
            start_date: Starting date (defaults to corporation founded date)
        """
        self.corporation = corporation
        self.time_unit = time_unit

        # Time management
        start = start_date or corporation.founded_date
        self.time_manager = TimeManager(start_date=start, time_unit=time_unit)

        # Accounting system
        self.accounting = AccountingSystem(
            corp_id=corporation.corp_id, project_path=corporation.project_path
        )

        # Event queue
        self.event_queue: list[EconomicEvent] = []

        # Monthly expenses configuration
        self.monthly_expenses: list[dict[str, Any]] = []

        # Simulation state
        self.simulation_path = (
            corporation.project_path
            / "_realms"
            / "bureaucracy_realm"
            / "corporations"
            / corporation.corp_id
            / "simulation"
            / "state.json"
        )

        # CRITICAL: Validate path is within project
        if not validate_path_in_project(self.simulation_path, corporation.project_path):
            raise ValueError(
                f"Invalid simulation path: {self.simulation_path} is outside project directory"
            )

        self.simulation_path.parent.mkdir(parents=True, exist_ok=True)
        # CRITICAL: Set secure directory permissions
        set_directory_permissions(self.simulation_path.parent)

    def add_monthly_expense(
        self,
        description: str,
        amount: Decimal,
        category: str = "general",
        vendor: str | None = None,
    ) -> None:
        """
        Add a recurring monthly expense.

        Args:
            description: Expense description
            amount: Monthly amount
            category: Expense category
            vendor: Vendor name (optional)
        """
        self.monthly_expenses.append(
            {
                "description": description,
                "amount": float(amount),
                "category": category,
                "vendor": vendor,
            }
        )

    async def tick(self) -> dict[str, Any]:
        """
        Execute one simulation tick.

        Returns:
            Dictionary with tick results
        """
        # Advance time
        current_date = self.time_manager.tick()

        # Process events for this date
        transactions = []
        events_processed = []

        # Check for monthly payroll (if month end)
        if self.time_manager.is_month_end():
            payroll_events = self._generate_payroll_events(current_date)
            self.event_queue.extend(payroll_events)

            # Generate monthly expenses
            expense_events = generate_monthly_expenses(self.monthly_expenses, current_date)
            self.event_queue.extend(expense_events)

        # Process events due today
        events_to_process = [
            e for e in self.event_queue if not e.processed and e.event_date <= current_date
        ]

        for event in events_to_process:
            transaction = self._process_event(event)
            if transaction:
                transactions.append(transaction)
                self.accounting.record_transaction(transaction)
                # Update corporation financial state
                self._update_financial_state(transaction)

            event.processed = True
            event.processed_at = current_date
            events_processed.append(event)

        # Remove processed events
        self.event_queue = [e for e in self.event_queue if not e.processed]

        # Save simulation state
        self._save_state()

        return {
            "tick": self.time_manager.tick_count,
            "date": current_date.isoformat(),
            "transactions_processed": len(transactions),
            "events_processed": len(events_processed),
            "cash_balance": float(self.accounting.get_cash_balance()),
            "financial_state": self.corporation.financial_state.to_dict(),
        }

    def _generate_payroll_events(self, event_date: datetime) -> list[EconomicEvent]:
        """Generate payroll events for all active employees."""
        employees = [
            {
                "being_id": emp.being_id,
                "salary": float(emp.salary) if emp.salary else None,
                "status": emp.status,
            }
            for emp in self.corporation.employees.values()
        ]

        return generate_payroll_events(employees, event_date, period="monthly")

    def _process_event(self, event: EconomicEvent) -> Transaction | None:
        """Process an economic event and generate transaction."""
        transaction_id = f"txn_{uuid.uuid4().hex[:8]}_{event.event_date.strftime('%Y%m%d')}"

        if event.event_type == EventType.PAYROLL:
            # Process payroll
            employee_id = event.metadata.get("employee_id")
            amount = Decimal(str(event.metadata.get("amount", 0)))

            transaction = create_salary_transaction(
                transaction_id=transaction_id,
                employee_id=employee_id,
                amount=amount,
                period=event.metadata.get("period", "monthly"),
                description=event.description,
            )

            return transaction

        elif event.event_type == EventType.EXPENSE:
            # Process expense
            amount = Decimal(str(event.metadata.get("amount", 0)))
            vendor = event.metadata.get("vendor", "Vendor")
            description = event.description

            transaction = create_vendor_invoice_transaction(
                transaction_id=transaction_id,
                vendor_name=vendor,
                amount=amount,
                description=description,
                expense_account=event.metadata.get("category", "expenses"),
            )

            return transaction

        elif event.event_type == EventType.VENDOR_INVOICE:
            # Process vendor invoice
            amount = Decimal(str(event.metadata.get("amount", 0)))
            vendor = event.metadata.get("vendor", "Vendor")
            description = event.description

            transaction = create_vendor_invoice_transaction(
                transaction_id=transaction_id,
                vendor_name=vendor,
                amount=amount,
                description=description,
            )

            return transaction

        # Other event types not yet implemented
        return None

    def _update_financial_state(self, transaction: Transaction) -> None:
        """Update corporation financial state from transaction."""
        if transaction.is_expense():
            self.corporation.financial_state.record_expense(
                transaction.amount, transaction.description
            )
        elif transaction.is_revenue():
            self.corporation.financial_state.record_revenue(
                transaction.amount, transaction.description
            )

        # Update cash
        if transaction.is_expense():
            self.corporation.financial_state.update_cash(
                -transaction.amount, transaction.description
            )
        elif transaction.is_revenue():
            self.corporation.financial_state.update_cash(
                transaction.amount, transaction.description
            )

        # Save corporation state
        self.corporation._save_manifest()

    def _save_state(self) -> None:
        """Save simulation state to disk."""
        state = {
            "corp_id": self.corporation.corp_id,
            "time_manager": self.time_manager.to_dict(),
            "event_queue": [e.to_dict() for e in self.event_queue],
            "monthly_expenses": self.monthly_expenses,
            "accounting": self.accounting.to_dict(),
            "last_updated": datetime.utcnow().isoformat(),
        }

        # CRITICAL: Use secure file write
        try:
            write_secure_file(self.simulation_path, json.dumps(state, indent=2), encoding="utf-8")
        except OSError as e:
            raise OSError(f"Failed to save simulation state to {self.simulation_path}: {e}")

    def load_state(self) -> None:
        """Load simulation state from disk."""
        if not self.simulation_path.exists():
            return

        try:
            # CRITICAL: Use secure JSON read with size limits
            state = read_secure_json(self.simulation_path)
        except (OSError, ValueError, json.JSONDecodeError):
            # If state is invalid, start fresh
            return

        # Load time manager
        if "time_manager" in state:
            try:
                self.time_manager = TimeManager.from_dict(state["time_manager"])
            except (KeyError, ValueError):
                # If time manager invalid, keep default
                pass

        # Load event queue
        if "event_queue" in state:
            self.event_queue = []
            for e in state["event_queue"]:
                try:
                    event = EconomicEvent.from_dict(e)
                    self.event_queue.append(event)
                except (KeyError, ValueError):
                    # Skip invalid event data
                    continue

        # Load monthly expenses
        if "monthly_expenses" in state:
            self.monthly_expenses = state["monthly_expenses"]

    async def run_simulation(self, ticks: int) -> list[dict[str, Any]]:
        """
        Run simulation for specified number of ticks.

        Args:
            ticks: Number of ticks to run

        Returns:
            List of tick results
        """
        results = []

        for _ in range(ticks):
            result = await self.tick()
            results.append(result)

        return results
