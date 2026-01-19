# Corporations Economic Simulation System

## Overview

A comprehensive economic simulation system for modeling corporations, their financial state, employees (Beings), and economic transactions. The system integrates with WAFT's Being system, generates Typst documentation (invoices, reports), and supports repeatable economic experiments.

## Architecture

### Core Components

1. **Corporations System** (`src/waft/core/corporations/`)
   - `CorporationsSystem`: Main system managing multiple corporations
   - `Corporation`: Individual corporation entity
   - `FinancialState`: Financial tracking (cash, assets, liabilities, equity)
   - `Department`: Organizational departments
   - `Employee`: Employee records (linked to Beings)

2. **Economic Engine** (`src/waft/core/corporations/economics/`)
   - `Transaction`: Economic transactions (invoices, salaries, expenses)
   - `AccountingSystem`: Double-entry accounting
   - `TransactionType`: Types of transactions

3. **Simulation Engine** (`src/waft/core/corporations/simulation/`)
   - `CorporationSimulator`: Main simulation orchestrator
   - `TimeManager`: Time progression (daily/weekly/monthly)
   - `EconomicEvent`: Economic event generation
   - `EventType`: Types of economic events

4. **Typst Integration** (`src/waft/templates/typst/wrappers/`)
   - `invoice_maker.py`: invoice-maker template wrapper
   - Generates Typst invoices for all transactions

5. **Experiment System** (`src/waft/core/corporations/experiments/`)
   - `ExperimentConfig`: Save/load initial configurations
   - `SimulationStateManager`: Checkpoint management
   - `ExperimentManifest`: Experiment metadata tracking

6. **Teleport Massive** (`src/waft/core/corporations/teleport_massive/`)
   - `founding_story.py`: 2025 founding narrative
   - `initial_conditions.py`: Starting conditions
   - Founders and initial setup

## Usage

### Creating a Corporation

```python
from src.waft.core.corporations import CorporationsSystem
from datetime import datetime
from decimal import Decimal

corps_system = CorporationsSystem(project_path=Path.cwd())

corporation = corps_system.create_corporation(
    name="My Corporation",
    sector="Technology",
    mission="Build amazing things",
    founded_date=datetime(2025, 1, 1),
    initial_capital=Decimal("1000000")  # $1M
)
```

### Hiring Employees

```python
corporation.hire_employee(
    being_id="being_123",
    role="Engineer",
    department="Engineering",
    title="Senior Software Engineer",
    level=5,
    salary=Decimal("120000")  # Annual salary
)
```

### Running a Simulation

```python
from src.waft.core.corporations.simulation import CorporationSimulator, TimeUnit

simulator = CorporationSimulator(
    corporation=corporation,
    time_unit=TimeUnit.DAILY,
    start_date=datetime(2025, 1, 1)
)

# Add monthly expenses
simulator.add_monthly_expense(
    description="Office rent",
    amount=Decimal("5000"),
    category="rent"
)

# Run simulation for 30 days
results = await simulator.run_simulation(ticks=30)
```

### Generating Invoices

```python
from src.waft.templates.typst.wrappers.invoice_maker import generate_invoice_from_transaction

# After a transaction is created
invoice_path = generate_invoice_from_transaction(
    transaction=transaction,
    corporation_name=corporation.name,
    corporation_address="123 Main St, City, State",
    output_dir=Path("invoices")
)
```

### Saving/Loading Experiments

```python
from src.waft.core.corporations.experiments import save_experiment_config, load_experiment_config

# Save experiment configuration
config_path = save_experiment_config(
    corporation=corporation,
    simulator=simulator,
    experiment_name="My Experiment",
    description="Initial conditions for my experiment"
)

# Load experiment configuration
corporation, simulator = load_experiment_config(
    config_path=config_path,
    project_path=Path.cwd(),
    being_system=being_system
)
```

### Creating Teleport Massive

```python
from src.waft.core.corporations.teleport_massive import create_teleport_massive
from src.waft.being import BeingSystem

being_system = BeingSystem(project_path=Path.cwd())

corporation = create_teleport_massive(
    project_path=Path.cwd(),
    being_system=being_system,
    create_founders=True
)
```

## Economic Model

### Financial State

Tracks:
- **Cash**: Liquid assets
- **Assets**: Non-cash assets (equipment, property)
- **Liabilities**: Debts and obligations
- **Equity**: Owner's equity (assets - liabilities)
- **Revenue**: Income from operations
- **Expenses**: Operating costs

### Transaction Types

- `SALARY`: Salary payment to employee
- `VENDOR_INVOICE`: Invoice from vendor (expense)
- `CUSTOMER_INVOICE`: Invoice to customer (revenue)
- `INVESTMENT`: Capital investment
- `EXPENSE`: General expense
- `REVENUE`: General revenue
- `ASSET_PURCHASE`: Purchase of asset
- `LOAN`: Loan received or paid

### Economic Cycles

- **Daily**: Process transactions, update balances
- **Weekly**: Generate invoices, process payroll
- **Monthly**: Financial statements, reports
- **Quarterly**: Investor reports, strategic planning

## Teleport Massive (2025)

### Founding Story

Teleport Massive was founded on July 1, 2025 by:
- **Dr. Elena Voss** (CEO): Quantum physicist turned entrepreneur
- **Dr. Marcus Chen** (CTO): Experimental physicist, inventor of Chen Stabilization Protocol

### Initial Conditions

- **Initial Capital**: $2,000,000 (seed funding)
- **Monthly Burn Rate**: ~$150,000
- **Founders**: 2 (CEO, CTO)
- **First Hires**: 3 Lead Scientists (January 2026)
- **Research Focus**: Quantum entanglement, macro-scale teleportation

### Mission

"To study quantum entanglement and scale quantum teleportation from mini to macro, revolutionizing transportation and making distance irrelevant."

## File Structure

```
_realms/bureaucracy_realm/corporations/
├── teleport_massive_20250701/
│   ├── corporate_manifest.json
│   ├── financials/
│   │   └── ledger.json
│   ├── simulation/
│   │   ├── state.json
│   │   └── checkpoints/
│   ├── experiments/
│   │   └── exp_*.json
│   └── founders.json
```

## Integration with Economic Libraries

The system incorporates concepts from:

- **ESL (Economic Simulation Library)**: Agent-based modeling patterns, market mechanisms
- **eno-world-simulation**: Hierarchical structure (employees → departments → corporations)
- **pareto-distribution-simulation**: Economic distribution modeling
- **nash**: Game theory for strategic decisions

These are integrated as patterns and concepts, not direct dependencies, keeping the system WAFT-native.

## Examples

See `examples/teleport_massive_economic_simulation.py` for a complete demo.

## Future Enhancements

- Revenue generation (customer invoices)
- Market mechanisms (pricing, supply/demand)
- Investment rounds (Series A, B, etc.)
- More sophisticated economic modeling
- Integration with external economic data
- Multi-corporation interactions
