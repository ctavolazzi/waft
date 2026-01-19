"""
Experiment Configuration: Save/load initial conditions

Manages experiment configurations for repeatable simulations.
"""

from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
from decimal import Decimal
import json
import uuid

from ..corporation import Corporation
from ..simulation.corporation_simulator import CorporationSimulator, TimeUnit
from ..corporations_system import CorporationsSystem


class ExperimentConfig:
    """
    Configuration for a repeatable economic simulation experiment.
    
    Contains all initial conditions needed to reproduce a simulation.
    """
    
    def __init__(
        self,
        experiment_id: str,
        name: str,
        description: str = "",
        version: str = "1.0.0",
        created_at: Optional[datetime] = None
    ):
        """
        Initialize experiment configuration.
        
        Args:
            experiment_id: Unique experiment identifier
            name: Experiment name
            description: Experiment description
            version: Configuration version
            created_at: Creation timestamp
        """
        self.experiment_id = experiment_id
        self.name = name
        self.description = description
        self.version = version
        self.created_at = created_at or datetime.utcnow()
        
        # Initial conditions
        self.corporation_config: Optional[Dict[str, Any]] = None
        self.employees_config: Optional[list] = None
        self.financial_config: Optional[Dict[str, Any]] = None
        self.simulation_config: Optional[Dict[str, Any]] = None
        self.monthly_expenses: Optional[list] = None
    
    def set_corporation_config(self, corporation: Corporation) -> None:
        """Set corporation configuration from Corporation object."""
        self.corporation_config = {
            "corp_id": corporation.corp_id,
            "name": corporation.name,
            "founded": corporation.founded_date.isoformat(),
            "sector": corporation.sector,
            "mission": corporation.mission,
            "initial_capital": float(corporation.financial_state.cash)
        }
    
    def set_employees_config(self, employees: list) -> None:
        """Set employees configuration."""
        self.employees_config = [
            {
                "being_id": emp.being_id,
                "role": emp.role,
                "department": emp.department,
                "title": emp.title,
                "level": emp.level,
                "salary": float(emp.salary) if emp.salary else None,
                "hired_at": emp.hired_at.isoformat()
            }
            for emp in employees
        ]
    
    def set_financial_config(self, financial_state: Dict[str, Any]) -> None:
        """Set financial configuration."""
        self.financial_config = financial_state
    
    def set_simulation_config(
        self,
        time_unit: TimeUnit,
        start_date: datetime,
        monthly_expenses: Optional[list] = None
    ) -> None:
        """Set simulation configuration."""
        self.simulation_config = {
            "time_unit": time_unit.value,
            "start_date": start_date.isoformat(),
            "monthly_expenses": monthly_expenses or []
        }
        self.monthly_expenses = monthly_expenses
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "experiment_id": self.experiment_id,
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "created_at": self.created_at.isoformat(),
            "initial_conditions": {
                "corporation": self.corporation_config or {},
                "employees": self.employees_config or [],
                "financials": self.financial_config or {},
                "simulation": self.simulation_config or {}
            }
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ExperimentConfig":
        """Create ExperimentConfig from dictionary."""
        config = cls(
            experiment_id=data["experiment_id"],
            name=data["name"],
            description=data.get("description", ""),
            version=data.get("version", "1.0.0"),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.utcnow().isoformat()))
        )
        
        initial_conditions = data.get("initial_conditions", {})
        config.corporation_config = initial_conditions.get("corporation", {})
        config.employees_config = initial_conditions.get("employees", [])
        config.financial_config = initial_conditions.get("financials", {})
        config.simulation_config = initial_conditions.get("simulation", {})
        
        if config.simulation_config:
            config.monthly_expenses = config.simulation_config.get("monthly_expenses", [])
        
        return config
    
    def save(self, output_path: Path) -> None:
        """Save configuration to file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(self.to_dict(), indent=2),
            encoding="utf-8"
        )
    
    @classmethod
    def load(cls, config_path: Path) -> "ExperimentConfig":
        """Load configuration from file."""
        data = json.loads(config_path.read_text(encoding="utf-8"))
        return cls.from_dict(data)


def save_experiment_config(
    corporation: Corporation,
    simulator: CorporationSimulator,
    experiment_name: str,
    description: str = "",
    output_dir: Optional[Path] = None,
    project_path: Optional[Path] = None
) -> Path:
    """
    Save experiment configuration from current corporation and simulator state.
    
    Args:
        corporation: Corporation to save
        simulator: Simulator to save
        experiment_name: Name for the experiment
        description: Experiment description
        output_dir: Directory to save config (defaults to corporation experiments dir)
        project_path: Project root path
        
    Returns:
        Path to saved configuration file
    """
    if output_dir is None:
        if project_path is None:
            project_path = Path.cwd()
        output_dir = (
            Path(project_path) / "_realms" / "bureaucracy_realm" / "corporations"
            / corporation.corp_id / "experiments"
        )
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create experiment config
    experiment_id = f"exp_{uuid.uuid4().hex[:8]}_{datetime.utcnow().strftime('%Y%m%d')}"
    config = ExperimentConfig(
        experiment_id=experiment_id,
        name=experiment_name,
        description=description
    )
    
    # Set configurations
    config.set_corporation_config(corporation)
    config.set_employees_config(list(corporation.employees.values()))
    config.set_financial_config(corporation.financial_state.to_dict())
    config.set_simulation_config(
        time_unit=simulator.time_unit,
        start_date=simulator.time_manager.start_date,
        monthly_expenses=simulator.monthly_expenses
    )
    
    # Save to file
    config_path = output_dir / f"{experiment_id}_config.json"
    config.save(config_path)
    
    return config_path


def load_experiment_config(
    config_path: Path,
    project_path: Optional[Path] = None,
    being_system: Optional[Any] = None
) -> tuple[Corporation, CorporationSimulator]:
    """
    Load experiment configuration and recreate corporation and simulator.
    
    Args:
        config_path: Path to configuration file
        project_path: Project root path
        being_system: BeingSystem instance (for creating employees if needed)
        
    Returns:
        Tuple of (Corporation, CorporationSimulator)
    """
    if project_path is None:
        project_path = Path.cwd()
    
    # Load configuration
    config = ExperimentConfig.load(config_path)
    
    # Recreate corporation
    corps_system = CorporationsSystem(project_path=project_path)
    
    corp_config = config.corporation_config
    corporation = corps_system.create_corporation(
        name=corp_config["name"],
        sector=corp_config.get("sector", ""),
        mission=corp_config.get("mission", ""),
        founded_date=datetime.fromisoformat(corp_config["founded"]),
        initial_capital=Decimal(str(corp_config.get("initial_capital", 0))),
        corp_id=corp_config.get("corp_id")
    )
    
    # Restore financial state
    if config.financial_config:
        from ..financial_state import FinancialState
        corporation.financial_state = FinancialState.from_dict(config.financial_config)
    
    # Restore employees (if being_system provided)
    if being_system and config.employees_config:
        for emp_config in config.employees_config:
            # Note: This assumes beings already exist
            # In a full implementation, you'd create beings if they don't exist
            corporation.hire_employee(
                being_id=emp_config["being_id"],
                role=emp_config["role"],
                department=emp_config["department"],
                title=emp_config["title"],
                level=emp_config.get("level", 1),
                salary=Decimal(str(emp_config["salary"])) if emp_config.get("salary") else None
            )
    
    # Recreate simulator
    sim_config = config.simulation_config
    simulator = CorporationSimulator(
        corporation=corporation,
        time_unit=TimeUnit(sim_config["time_unit"]),
        start_date=datetime.fromisoformat(sim_config["start_date"])
    )
    
    # Restore monthly expenses
    if config.monthly_expenses:
        for expense in config.monthly_expenses:
            simulator.add_monthly_expense(
                description=expense["description"],
                amount=Decimal(str(expense["amount"])),
                category=expense.get("category", "general"),
                vendor=expense.get("vendor")
            )
    
    return corporation, simulator
