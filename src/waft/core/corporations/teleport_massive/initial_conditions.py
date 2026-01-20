"""
Initial Conditions: Teleport Massive starting configuration

Defines the initial economic and organizational state for Teleport Massive
simulation experiments.
"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Dict, Any, Optional, List


@dataclass
class InitialConditions:
    """Initial conditions for Teleport Massive simulation."""
    
    # Corporation basics
    founded_date: datetime
    initial_capital: Decimal
    sector: str
    mission: str
    
    # Founders
    founders: List[Dict[str, Any]]
    
    # Financial
    monthly_burn_rate: Decimal
    revenue: Decimal  # Initially 0
    
    # Employees (initial hires)
    initial_employees: List[Dict[str, Any]]
    
    # Monthly expenses
    monthly_expenses: List[Dict[str, Any]]
    
    # Research goals
    research_milestones: List[Dict[str, Any]]


def get_initial_conditions() -> InitialConditions:
    """
    Get initial conditions for Teleport Massive (2025 founding).
    
    Returns:
        InitialConditions object
    """
    return InitialConditions(
        founded_date=datetime(2025, 7, 1),
        initial_capital=Decimal("2000000"),  # $2M seed funding
        sector="Quantum Teleportation Technology",
        mission="To study quantum entanglement and scale quantum teleportation from mini to macro, revolutionizing transportation and making distance irrelevant.",
        
        founders=[
            {
                "name": "Dr. Elena Voss",
                "role": "CEO & Co-Founder",
                "salary": 180000,
                "skills": ["quantum_physics", "leadership", "entrepreneurship"]
            },
            {
                "name": "Dr. Marcus Chen",
                "role": "CTO & Co-Founder",
                "salary": 180000,
                "skills": ["experimental_physics", "quantum_systems", "research"]
            }
        ],
        
        monthly_burn_rate=Decimal("150000"),  # ~$150k/month
        revenue=Decimal("0"),  # No revenue initially (research phase)
        
        initial_employees=[
            {
                "name": "Aziah Calderon",
                "role": "Lead Scientist",
                "department": "Research & Development",
                "salary": 95000,
                "hired_date": datetime(2026, 1, 18)
            },
            {
                "name": "Dr. Priya Sharma",
                "role": "Lead Scientist",
                "department": "Research & Development",
                "salary": 95000,
                "hired_date": datetime(2026, 1, 18)
            },
            {
                "name": "Dr. James Park",
                "role": "Lead Scientist",
                "department": "Research & Development",
                "salary": 95000,
                "hired_date": datetime(2026, 1, 18)
            }
        ],
        
        monthly_expenses=[
            {
                "description": "Laboratory rent",
                "amount": 15000,
                "category": "rent",
                "vendor": "Quantum Labs Inc."
            },
            {
                "description": "Quantum research equipment maintenance",
                "amount": 25000,
                "category": "equipment",
                "vendor": "Quantum Systems Corp"
            },
            {
                "description": "Utilities and facilities",
                "amount": 5000,
                "category": "utilities",
                "vendor": "City Utilities"
            },
            {
                "description": "Research supplies and materials",
                "amount": 10000,
                "category": "supplies",
                "vendor": "Quantum Materials Supply"
            }
        ],
        
        research_milestones=[
            {
                "milestone": "Establish quantum entanglement protocols",
                "target_date": datetime(2026, 6, 1),
                "status": "in_progress"
            },
            {
                "milestone": "Develop macro-scale stabilization techniques",
                "target_date": datetime(2026, 12, 1),
                "status": "planned"
            },
            {
                "milestone": "First successful macro-scale teleportation test",
                "target_date": datetime(2027, 6, 1),
                "status": "planned"
            }
        ]
    )
