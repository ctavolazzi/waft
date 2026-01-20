"""
Teleport Massive Economic Simulation Demo

Demonstrates the economic simulation system for Teleport Massive Corporation.
Shows how to create the corporation, run simulations, and generate invoices.
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
from src.waft.core.corporations.experiments import save_experiment_config
from src.waft.core.corporations.simulation import CorporationSimulator, TimeUnit
from src.waft.core.corporations.teleport_massive import create_teleport_massive


async def main():
    """Run Teleport Massive economic simulation demo."""
    project_path = Path.cwd()

    print("🚀 Teleport Massive Economic Simulation Demo\n")

    # Initialize systems
    print("📊 Initializing systems...")
    being_system = BeingSystem(project_path=project_path)
    corps_system = CorporationsSystem(project_path=project_path)

    # Create Teleport Massive
    print("\n🏢 Creating Teleport Massive Corporation...")
    corporation = create_teleport_massive(
        project_path=project_path, being_system=being_system, create_founders=True
    )

    print(f"   ✓ Corporation created: {corporation.name}")
    print(f"   ✓ Founded: {corporation.founded_date.strftime('%Y-%m-%d')}")
    print(f"   ✓ Initial Capital: ${corporation.financial_state.cash:,.2f}")
    print(f"   ✓ Employees: {len(corporation.employees)}")

    # Create simulator
    print("\n⚙️  Setting up simulation engine...")
    simulator = CorporationSimulator(
        corporation=corporation, time_unit=TimeUnit.DAILY, start_date=datetime(2025, 7, 1)
    )

    # Add monthly expenses (already done in create_teleport_massive, but showing here)
    print("   ✓ Monthly expenses configured")

    # Save initial experiment configuration
    print("\n💾 Saving experiment configuration...")
    config_path = save_experiment_config(
        corporation=corporation,
        simulator=simulator,
        experiment_name="Teleport Massive 2025 Founding",
        description="Initial simulation from 2025 founding with founders and seed funding",
        project_path=project_path,
    )
    print(f"   ✓ Configuration saved: {config_path}")

    # Run simulation for 30 days (1 month)
    print("\n⏱️  Running simulation (30 days)...")
    results = await simulator.run_simulation(ticks=30)

    print(f"   ✓ Simulation complete: {len(results)} ticks")

    # Show results
    print("\n📈 Simulation Results:")
    final_result = results[-1]
    print(f"   Current Date: {final_result['date']}")
    print(f"   Cash Balance: ${final_result['cash_balance']:,.2f}")
    print(f"   Transactions Processed: {final_result['transactions_processed']}")

    # Show financial state
    financial = corporation.financial_state
    print("\n💰 Financial State:")
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
        print(f"   Runway: {runway:.1f} months")
    else:
        print("   Runway: Generating profit (no runway limit)")

    # Show accounting summary
    print("\n📊 Accounting Summary:")
    accounting = simulator.accounting
    print(f"   Total Transactions: {len(accounting.transactions)}")
    print(f"   Cash Balance: ${accounting.get_cash_balance():,.2f}")
    print(f"   Total Revenue: ${accounting.get_total_revenue():,.2f}")
    print(f"   Total Expenses: ${accounting.get_total_expenses():,.2f}")
    print(f"   Net Income: ${accounting.get_net_income():,.2f}")

    print("\n✅ Demo complete!")
    print("\n📁 Files created:")
    print(f"   - Corporation: {corporation.corp_path}")
    print(f"   - Experiment Config: {config_path}")
    print(f"   - Simulation State: {simulator.simulation_path}")


if __name__ == "__main__":
    asyncio.run(main())
