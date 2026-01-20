"""
Teleport Massive Full Report Generator

Creates comprehensive report with all financial data, transactions, and invoices.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import asyncio
from datetime import datetime
from decimal import Decimal

from src.waft.being import BeingSystem
from src.waft.core.corporations.corporations_system import CorporationsSystem
from src.waft.core.corporations.economics.transaction import TransactionType
from src.waft.core.corporations.simulation import CorporationSimulator, TimeUnit
from src.waft.core.corporations.teleport_massive import create_teleport_massive
from src.waft.templates.typst.wrappers.invoice_maker import generate_invoice_from_transaction


async def main():
    """Generate complete Teleport Massive report."""
    project_path = Path.cwd()

    print("=" * 80)
    print(" " * 20 + "TELEPORT MASSIVE CORPORATION")
    print(" " * 15 + "COMPLETE ECONOMIC SIMULATION REPORT")
    print("=" * 80)
    print()

    # Initialize systems
    print("📊 Initializing systems...")
    being_system = BeingSystem(project_path=project_path)
    CorporationsSystem(project_path=project_path)
    print("   ✓ Systems ready")
    print()

    # Create or load Teleport Massive
    print("🏢 Teleport Massive Corporation...")
    corporation = create_teleport_massive(
        project_path=project_path, being_system=being_system, create_founders=True
    )

    print(f"   Name: {corporation.name}")
    print(f"   Founded: {corporation.founded_date.strftime('%B %d, %Y')}")
    print(f"   Sector: {corporation.sector}")
    print(
        f"   Mission: {corporation.mission[:80]}..."
        if len(corporation.mission) > 80
        else f"   Mission: {corporation.mission}"
    )
    print()

    # Financial Overview
    financial = corporation.financial_state
    print("=" * 80)
    print("💰 FINANCIAL OVERVIEW")
    print("=" * 80)
    print()
    print(f"   Initial Capital:     ${corporation.financial_state.cash:>15,.2f}")
    print(f"   Current Cash:        ${financial.cash:>15,.2f}")
    print(f"   Total Assets:        ${financial.get_total_assets():>15,.2f}")
    print(f"   Total Liabilities:   ${financial.get_total_liabilities():>15,.2f}")
    print(f"   Equity:              ${financial.equity:>15,.2f}")
    print()
    print(f"   Total Revenue:       ${financial.revenue:>15,.2f}")
    print(f"   Total Expenses:      ${financial.expenses:>15,.2f}")
    print(f"   Net Income:          ${financial.get_net_income():>15,.2f}")
    print()
    print(f"   Monthly Burn Rate:   ${financial.get_burn_rate():>15,.2f}")
    runway = financial.get_runway_months()
    if runway:
        print(f"   Runway:              {runway:>15.1f} months")
        print(
            f"   Runway Value:        ${(financial.cash / financial.get_burn_rate() * financial.get_burn_rate()):>15,.2f}"
        )
    else:
        print(f"   Runway:              {'Profitability':>15}")
    print()

    # Employees
    print("=" * 80)
    print("👥 ORGANIZATIONAL STRUCTURE")
    print("=" * 80)
    print()
    print(f"   Departments: {len(corporation.departments)}")
    for _dept_name, dept in corporation.departments.items():
        print(f"     • {dept.name}: {len(dept.employees)} employees")
    print()
    print(f"   Total Employees: {len(corporation.employees)}")
    print()

    total_payroll = Decimal("0")
    for emp in corporation.employees.values():
        salary_str = f"${emp.salary:,.2f}/year" if emp.salary else "Salary TBD"
        monthly = emp.salary / 12 if emp.salary else Decimal("0")
        total_payroll += monthly
        print(f"     • {emp.title}")
        print(f"       Department: {emp.department}")
        print(f"       Salary: {salary_str} (${monthly:,.2f}/month)")
        print()

    print(f"   Total Monthly Payroll: ${total_payroll:,.2f}")
    print()

    # Run simulation
    print("=" * 80)
    print("⏱️  RUNNING SIMULATION (30 DAYS)")
    print("=" * 80)
    print()

    simulator = CorporationSimulator(
        corporation=corporation, time_unit=TimeUnit.DAILY, start_date=datetime(2025, 7, 1)
    )

    results = await simulator.run_simulation(ticks=30)

    print(f"   ✓ Simulation complete: {len(results)} days")
    print(f"   ✓ Transactions processed: {len(simulator.accounting.transactions)}")
    print()

    # Transactions
    print("=" * 80)
    print("📋 TRANSACTION HISTORY")
    print("=" * 80)
    print()

    accounting = simulator.accounting
    for i, txn in enumerate(accounting.transactions, 1):
        txn_type_str = txn.transaction_type.value.replace("_", " ").title()
        print(f"   {i}. {txn_type_str}")
        print(f"      ID: {txn.transaction_id}")
        print(f"      Date: {txn.timestamp.strftime('%Y-%m-%d')}")
        print(f"      Amount: ${txn.amount:,.2f}")
        print(f"      Description: {txn.description}")
        if txn.from_party:
            print(f"      From: {txn.from_party}")
        if txn.to_party:
            print(f"      To: {txn.to_party}")
        print()

    # Generate all invoices
    print("=" * 80)
    print("📄 INVOICE GENERATION")
    print("=" * 80)
    print()

    invoice_dir = corporation.corp_path / "invoices"
    invoice_dir.mkdir(parents=True, exist_ok=True)

    corporation_address = "123 Quantum Drive\nSan Francisco, CA 94105\nUnited States"

    invoice_count = 0
    for transaction in accounting.transactions:
        try:
            recipient_name = None
            recipient_address = None

            if transaction.transaction_type == TransactionType.SALARY:
                emp = corporation.employees.get(transaction.to_party)
                if emp:
                    try:
                        being = being_system._load_being(transaction.to_party)
                        recipient_name = (
                            being.custom_name if being and being.custom_name else emp.title
                        )
                    except:
                        recipient_name = emp.title
                    recipient_address = ""

            elif transaction.transaction_type == TransactionType.VENDOR_INVOICE:
                recipient_name = corporation.name
                recipient_address = corporation_address

            elif transaction.transaction_type == TransactionType.CUSTOMER_INVOICE:
                recipient_name = transaction.from_party or "Customer"
                recipient_address = ""

            invoice_path = generate_invoice_from_transaction(
                transaction=transaction,
                corporation_name=corporation.name,
                corporation_address=corporation_address,
                output_dir=invoice_dir,
                recipient_name=recipient_name,
                recipient_address=recipient_address,
            )

            invoice_count += 1
            print(f"   ✓ {invoice_path.name}")

        except Exception as e:
            print(f"   ⚠️  {transaction.transaction_id}: {str(e)[:50]}")

    print()
    print(f"   Total invoices: {invoice_count}")
    print()

    # Final Summary
    print("=" * 80)
    print("📊 FINAL SUMMARY")
    print("=" * 80)
    print()

    final_financial = corporation.financial_state
    print(f"   Date: {results[-1]['date']}")
    print(f"   Cash Balance: ${final_financial.cash:,.2f}")
    print(f"   Total Transactions: {len(accounting.transactions)}")
    print(f"   Invoices Generated: {invoice_count}")
    print()

    print("=" * 80)
    print("✅ COMPLETE")
    print("=" * 80)
    print()
    print("📁 All files saved to:")
    print(f"   {corporation.corp_path}")
    print()
    print("💡 To compile invoices to PDF:")
    print(f"   cd {invoice_dir}")
    print("   typst compile invoice_*.typ")
    print()


if __name__ == "__main__":
    asyncio.run(main())
