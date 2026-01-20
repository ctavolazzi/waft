// CORPORATION SIMULATION
// Economic Modeling in WAFT

#import "@preview/showybox:2.0.4": showybox

#set document(title: "Corporation Simulation", author: "WAFT Economics Division")
#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 10pt)

#let primary = rgb("#2f855a")

#align(center)[
  #rect(fill: gradient.linear(primary, primary.darken(30%)), width: 100%, inset: 2em)[
    #text(fill: white, size: 24pt, weight: "bold")[CORPORATION SIMULATION]
    #v(0.3em)
    #text(fill: white.darken(10%), size: 12pt)[WAFT | Economic Modeling System]
  ]
]

#v(1em)

= Overview

WAFT includes a full economic simulation system for modeling corporations. Track finances, employees, departments, and growth over time.

= Corporation Structure

```python
@dataclass
class Corporation:
    corp_id: str              # Unique identifier
    name: str                 # Display name
    sector: str               # Industry sector
    mission: str              # Mission statement
    founded_date: datetime    # Founding date
    capital: Decimal          # Current capital
    employees: dict           # Being ID → Employee record
    departments: list         # Department names
    monthly_expenses: list    # Recurring costs
```

= Creating Corporations

```python
from waft.core import CorporationsSystem
from decimal import Decimal
from datetime import datetime

corps = CorporationsSystem(project_path=Path("."))

corp = corps.create_corporation(
    name="My Startup",
    sector="AI Research",
    mission="Build intelligent systems",
    founded_date=datetime(2026, 1, 1),
    initial_capital=Decimal("500000"),
)
```

#pagebreak()

= Financial Tracking

== Revenue & Expenses

```python
# Add revenue
corp.add_revenue(
    amount=Decimal("50000"),
    source="Contract work",
    date=datetime.now(),
)

# Add expense
corp.add_expense(
    amount=Decimal("15000"),
    category="Equipment",
    description="Quantum analyzer",
    vendor="QuantumTech Inc",
)
```

== Monthly Recurring Expenses

```python
simulator.add_monthly_expense(
    description="Office rent",
    amount=Decimal("10000"),
    category="rent",
    vendor="Building Corp",
)
```

== Balance Sheet

#table(
  columns: (1fr, auto, auto),
  stroke: 0.5pt,
  inset: 8pt,
  [*Item*], [*Debit*], [*Credit*],
  [Initial Capital], [], [\$500,000],
  [Equipment Purchase], [\$15,000], [],
  [Contract Revenue], [], [\$50,000],
  [Monthly Rent], [\$10,000], [],
  [*Balance*], [], [*\$525,000*],
)

= Employee Management

== Hiring

```python
corp.hire_employee(
    being_id=being.being_id,
    role="Engineer",
    department="R&D",
    title="Senior Engineer",
    level=7,
    salary=Decimal("120000"),
)
```

== Department Structure

```python
corp.add_department("Executive")
corp.add_department("Research & Development")
corp.add_department("Operations")
corp.add_department("Finance")
```

= Time Simulation

```python
from waft.core.simulation import CorporationSimulator, TimeUnit

simulator = CorporationSimulator(
    corporation=corp,
    time_unit=TimeUnit.DAILY,
    start_date=datetime(2026, 1, 1),
)

# Advance time
simulator.advance(days=30)

# Check finances
print(f"Capital: ${corp.capital}")
print(f"Burn rate: ${simulator.monthly_burn_rate}")
print(f"Runway: {simulator.runway_months} months")
```

= Reports

```bash
# Generate financial report
waft corp report my_startup --type financial

# Employee roster
waft corp roster my_startup

# Department summary
waft corp departments my_startup
```

#v(1em)

#align(center)[
  #rect(fill: primary, inset: 1em)[
    #text(fill: white)[CORPORATION SIMULATION | Business Evolution]
  ]
]
