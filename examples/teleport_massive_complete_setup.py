"""
Teleport Massive Complete Setup

Creates the corporation, runs simulation, and generates invoices with dollar amounts.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import asyncio
from datetime import datetime

from src.waft.being import BeingSystem
from src.waft.core.corporations.corporations_system import CorporationsSystem
from src.waft.core.corporations.economics.transaction import TransactionType
from src.waft.core.corporations.experiments import save_experiment_config
from src.waft.core.corporations.simulation import CorporationSimulator, TimeUnit
from src.waft.core.corporations.teleport_massive import create_teleport_massive
from src.waft.templates.typst.wrappers.invoice_maker import generate_invoice_from_transaction


async def main():
    """Complete Teleport Massive setup with simulation and invoice generation."""
    project_path = Path.cwd()

    print("=" * 70)
    print("🚀 TELEPORT MASSIVE CORPORATION - COMPLETE SETUP")
    print("=" * 70)
    print()

    # Initialize systems
    print("📊 Initializing systems...")
    being_system = BeingSystem(project_path=project_path)
    corps_system = CorporationsSystem(project_path=project_path)
    print("   ✓ Systems initialized")
    print()

    # Create Teleport Massive
    print("🏢 Creating Teleport Massive Corporation...")
    corporation = create_teleport_massive(
        project_path=project_path, being_system=being_system, create_founders=True
    )

    print(f"   ✓ Corporation: {corporation.name}")
    print(f"   ✓ Founded: {corporation.founded_date.strftime('%B %d, %Y')}")
    print(f"   ✓ Initial Capital: ${corporation.financial_state.cash:,.2f}")
    print(f"   ✓ Employees: {len(corporation.employees)}")
    print(f"   ✓ Departments: {len(corporation.departments)}")
    print()

    # Show employees
    print("👥 Employees:")
    for emp in corporation.employees.values():
        salary_str = f"${emp.salary:,.2f}/year" if emp.salary else "Salary TBD"
        print(f"   • {emp.title} ({emp.department}): {salary_str}")
    print()

    # Create simulator
    print("⚙️  Setting up simulation engine...")
    simulator = CorporationSimulator(
        corporation=corporation, time_unit=TimeUnit.DAILY, start_date=datetime(2025, 7, 1)
    )
    print("   ✓ Simulator ready")
    print()

    # Save initial experiment configuration
    print("💾 Saving experiment configuration...")
    config_path = save_experiment_config(
        corporation=corporation,
        simulator=simulator,
        experiment_name="Teleport Massive 2025 Founding",
        description="Initial simulation from 2025 founding with founders and seed funding",
        project_path=project_path,
    )
    print("   ✓ Configuration saved")
    print()

    # Run simulation for 30 days (1 month)
    print("⏱️  Running simulation (30 days)...")
    print("   Processing economic events...")
    results = await simulator.run_simulation(ticks=30)

    print(f"   ✓ Simulation complete: {len(results)} days processed")
    print()

    # Show results
    print("=" * 70)
    print("📈 SIMULATION RESULTS")
    print("=" * 70)
    final_result = results[-1]
    print(f"   Current Date: {final_result['date']}")
    print(f"   Cash Balance: ${final_result['cash_balance']:,.2f}")
    print(f"   Transactions Processed: {final_result['transactions_processed']}")
    print()

    # Show financial state
    financial = corporation.financial_state
    print("💰 FINANCIAL STATE:")
    print(f"   Cash: ${financial.cash:,.2f}")
    print(f"   Total Assets: ${financial.get_total_assets():,.2f}")
    print(f"   Total Liabilities: ${financial.get_total_liabilities():,.2f}")
    print(f"   Equity: ${financial.equity:,.2f}")
    print(f"   Revenue: ${financial.revenue:,.2f}")
    print(f"   Expenses: ${financial.expenses:,.2f}")
    print(f"   Net Income: ${financial.get_net_income():,.2f}")
    print(f"   Monthly Burn Rate: ${financial.get_burn_rate():,.2f}")

    runway = financial.get_runway_months()
    if runway:
        print(
            f"   Runway: {runway:.1f} months (${financial.cash:,.2f} / ${financial.get_burn_rate():,.2f})"
        )
    else:
        print("   Runway: Generating profit (no runway limit)")
    print()

    # Show accounting summary
    accounting = simulator.accounting
    print("📊 ACCOUNTING SUMMARY:")
    print(f"   Total Transactions: {len(accounting.transactions)}")
    print(f"   Cash Balance: ${accounting.get_cash_balance():,.2f}")
    print(f"   Total Revenue: ${accounting.get_total_revenue():,.2f}")
    print(f"   Total Expenses: ${accounting.get_total_expenses():,.2f}")
    print(f"   Net Income: ${accounting.get_net_income():,.2f}")
    print()

    # Generate invoices for all transactions
    print("=" * 70)
    print("📄 GENERATING INVOICES")
    print("=" * 70)

    invoice_dir = corporation.corp_path / "invoices"
    invoice_dir.mkdir(parents=True, exist_ok=True)

    corporation_address = "123 Quantum Drive\nSan Francisco, CA 94105\nUnited States"

    invoice_count = 0
    for transaction in accounting.transactions:
        try:
            # Determine recipient based on transaction type
            recipient_name = None
            recipient_address = None

            if transaction.transaction_type == TransactionType.SALARY:
                # Get employee name
                emp = corporation.employees.get(transaction.to_party)
                if emp:
                    # Try to load Being to get name
                    try:
                        being = being_system.load_being(transaction.to_party)
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

            # Generate invoice
            invoice_path = generate_invoice_from_transaction(
                transaction=transaction,
                corporation_name=corporation.name,
                corporation_address=corporation_address,
                output_dir=invoice_dir,
                recipient_name=recipient_name,
                recipient_address=recipient_address,
            )

            invoice_count += 1
            print(f"   ✓ Generated: {invoice_path.name}")

        except Exception as e:
            print(f"   ⚠️  Failed to generate invoice for {transaction.transaction_id}: {e}")

    print(f"\n   Total invoices generated: {invoice_count}")
    print()

    # Summary
    print("=" * 70)
    print("✅ SETUP COMPLETE")
    print("=" * 70)
    print()
    print("📁 Files created:")
    print(f"   • Corporation: {corporation.corp_path}")
    print(f"   • Experiment Config: {config_path}")
    print(f"   • Simulation State: {simulator.simulation_path}")
    print(f"   • Invoices: {invoice_dir} ({invoice_count} invoices)")
    print()
    print("💡 Next steps:")
    print("   • Compile invoices to PDF: typst compile <invoice.typ>")
    print("   • Run longer simulation: increase ticks parameter")
    print("   • Add more employees: corporation.hire_employee(...)")
    print("   • Generate reports: use biz-report template")
    print()


if __name__ == "__main__":
    asyncio.run(main())
