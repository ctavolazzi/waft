"""
Corporation: Individual corporation entity

Represents a single corporation with financial state, employees (Beings),
departments, and economic transactions.
"""

import json
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

from .financial_state import FinancialState
from .security import (
    write_secure_file,
)


class Department:
    """A department within a corporation."""

    def __init__(
        self, name: str, department_id: str | None = None, created_at: datetime | None = None
    ):
        self.name = name
        self.department_id = department_id or f"dept_{name.lower().replace(' ', '_')}"
        self.created_at = created_at or datetime.utcnow()
        self.employees: list[str] = []  # List of being_ids

    def to_dict(self) -> dict[str, Any]:
        """Convert department to dictionary."""
        return {
            "name": self.name,
            "department_id": self.department_id,
            "created_at": self.created_at.isoformat(),
            "employees": self.employees,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Department":
        """Create Department from dictionary."""
        dept = cls(
            name=data["name"],
            department_id=data.get("department_id"),
            created_at=datetime.fromisoformat(
                data.get("created_at", datetime.utcnow().isoformat())
            ),
        )
        dept.employees = data.get("employees", [])
        return dept


class Employee:
    """An employee (Being) within a corporation."""

    def __init__(
        self,
        being_id: str,
        role: str,
        department: str,
        title: str,
        level: int = 1,
        salary: Decimal | None = None,
        hired_at: datetime | None = None,
        status: str = "active",
    ):
        self.being_id = being_id
        self.role = role
        self.department = department
        self.title = title
        self.level = level
        self.salary = Decimal(str(salary)) if salary else None
        self.hired_at = hired_at or datetime.utcnow()
        self.status = status

    def to_dict(self) -> dict[str, Any]:
        """Convert employee to dictionary."""
        return {
            "being_id": self.being_id,
            "role": self.role,
            "department": self.department,
            "title": self.title,
            "level": self.level,
            "salary": float(self.salary) if self.salary else None,
            "hired_at": self.hired_at.isoformat(),
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Employee":
        """Create Employee from dictionary."""
        return cls(
            being_id=data["being_id"],
            role=data["role"],
            department=data["department"],
            title=data["title"],
            level=data.get("level", 1),
            salary=Decimal(str(data["salary"])) if data.get("salary") else None,
            hired_at=datetime.fromisoformat(data.get("hired_at", datetime.utcnow().isoformat())),
            status=data.get("status", "active"),
        )


class Corporation:
    """
    A corporation entity with financial state, employees, and departments.

    Represents a single corporation that can:
    - Track financial state (cash, assets, liabilities, equity)
    - Manage employees (Beings)
    - Organize into departments
    - Record economic transactions
    - Generate financial reports
    """

    def __init__(
        self,
        corp_id: str,
        name: str,
        founded_date: datetime,
        sector: str = "",
        mission: str = "",
        project_path: Path | None = None,
        initial_capital: Decimal | None = None,
    ):
        """
        Initialize a corporation.

        Args:
            corp_id: Unique corporation identifier
            name: Corporation name
            founded_date: Date corporation was founded
            sector: Industry sector
            mission: Corporate mission statement
            project_path: Project root path for file storage
            initial_capital: Initial capital investment
        """
        self.corp_id = corp_id
        self.name = name
        self.founded_date = founded_date
        self.sector = sector
        self.mission = mission
        self.project_path = Path(project_path) if project_path else Path.cwd()

        # Financial state
        initial_cash = initial_capital or Decimal("0")
        self.financial_state = FinancialState(cash=initial_cash)
        if initial_capital:
            self.financial_state.record_revenue(initial_capital, "Initial capital investment")

        # Organizational structure
        self.departments: dict[str, Department] = {}
        self.employees: dict[str, Employee] = {}  # being_id -> Employee

        # Corporate path
        self.corp_path = (
            self.project_path / "_realms" / "bureaucracy_realm" / "corporations" / self.corp_id
        )
        self.corp_path.mkdir(parents=True, exist_ok=True)

        # Manifest file
        self.manifest_path = self.corp_path / "corporate_manifest.json"
        self._ensure_manifest()

    def _ensure_manifest(self) -> None:
        """Ensure corporate manifest exists."""
        if not self.manifest_path.exists():
            manifest = {
                "corp_id": self.corp_id,
                "name": self.name,
                "founded": self.founded_date.isoformat(),
                "sector": self.sector,
                "mission": self.mission,
                "departments": [],
                "employees": [],
                "financial_state": self.financial_state.to_dict(),
            }
            # CRITICAL: Use secure file write
            write_secure_file(self.manifest_path, json.dumps(manifest, indent=2), encoding="utf-8")
        else:
            # Load existing manifest
            self._load_from_manifest()

    def _load_from_manifest(self) -> None:
        """Load corporation state from manifest."""
        manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))

        # Load departments
        self.departments = {}
        for dept_data in manifest.get("departments", []):
            dept = Department.from_dict(dept_data)
            self.departments[dept.department_id] = dept

        # Load employees
        self.employees = {}
        for emp_data in manifest.get("employees", []):
            emp = Employee.from_dict(emp_data)
            self.employees[emp.being_id] = emp

        # Load financial state
        if "financial_state" in manifest:
            self.financial_state = FinancialState.from_dict(manifest["financial_state"])

    def add_department(self, name: str, department_id: str | None = None) -> Department:
        """
        Add a department to the corporation.

        Args:
            name: Department name
            department_id: Optional department ID (auto-generated if not provided)

        Returns:
            Created Department
        """
        dept = Department(name=name, department_id=department_id)
        self.departments[dept.department_id] = dept
        self._save_manifest()
        return dept

    def hire_employee(
        self,
        being_id: str,
        role: str,
        department: str,
        title: str,
        level: int = 1,
        salary: Decimal | None = None,
    ) -> Employee:
        """
        Hire an employee (Being) to the corporation.

        Args:
            being_id: Being identifier
            role: Role name
            department: Department name
            title: Job title
            level: Seniority level (1-10)
            salary: Annual salary (must be positive if provided)

        Returns:
            Created Employee record

        Raises:
            ValueError: If salary is invalid or negative
        """
        # HIGH: Validate salary if provided
        if salary is not None:
            from .security import validate_financial_amount

            if not validate_financial_amount(salary, min_amount=Decimal("0"), allow_negative=False):
                raise ValueError(f"Invalid salary: {salary} (must be positive)")

        # HIGH: Validate level is in valid range
        if not (1 <= level <= 10):
            raise ValueError(f"Invalid level: {level} (must be between 1 and 10)")

        # Ensure department exists
        dept_id = None
        for dept in self.departments.values():
            if dept.name == department:
                dept_id = dept.department_id
                break

        if dept_id is None:
            # Create department if it doesn't exist
            dept = self.add_department(department)
            dept_id = dept.department_id

        # Create employee
        employee = Employee(
            being_id=being_id,
            role=role,
            department=department,
            title=title,
            level=level,
            salary=salary,
            hired_at=datetime.utcnow(),
        )

        self.employees[being_id] = employee
        self.departments[dept_id].employees.append(being_id)

        self._save_manifest()
        return employee

    def get_employee(self, being_id: str) -> Employee | None:
        """Get employee by being_id."""
        return self.employees.get(being_id)

    def get_department_employees(self, department: str) -> list[Employee]:
        """Get all employees in a department."""
        dept_id = None
        for dept in self.departments.values():
            if dept.name == department:
                dept_id = dept.department_id
                break

        if dept_id is None:
            return []

        dept = self.departments[dept_id]
        return [self.employees[bid] for bid in dept.employees if bid in self.employees]

    def get_monthly_payroll(self) -> Decimal:
        """Calculate total monthly payroll."""
        total = Decimal("0")
        for employee in self.employees.values():
            if employee.salary and employee.status == "active":
                # Convert annual salary to monthly
                monthly = employee.salary / Decimal("12")
                total += monthly
        return total

    def _save_manifest(self) -> None:
        """Save corporation state to manifest."""
        manifest = {
            "corp_id": self.corp_id,
            "name": self.name,
            "founded": self.founded_date.isoformat(),
            "sector": self.sector,
            "mission": self.mission,
            "departments": [dept.to_dict() for dept in self.departments.values()],
            "employees": [emp.to_dict() for emp in self.employees.values()],
            "financial_state": self.financial_state.to_dict(),
        }

        # CRITICAL: Use secure file write
        try:
            write_secure_file(self.manifest_path, json.dumps(manifest, indent=2), encoding="utf-8")
        except OSError as e:
            raise OSError(f"Failed to save corporate manifest to {self.manifest_path}: {e}")

    def to_dict(self) -> dict[str, Any]:
        """Convert corporation to dictionary."""
        return {
            "corp_id": self.corp_id,
            "name": self.name,
            "founded": self.founded_date.isoformat(),
            "sector": self.sector,
            "mission": self.mission,
            "departments": [dept.to_dict() for dept in self.departments.values()],
            "employees": [emp.to_dict() for emp in self.employees.values()],
            "financial_state": self.financial_state.to_dict(),
            "monthly_payroll": float(self.get_monthly_payroll()),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any], project_path: Path | None = None) -> "Corporation":
        """Create Corporation from dictionary."""
        corp = cls(
            corp_id=data["corp_id"],
            name=data["name"],
            founded_date=datetime.fromisoformat(data["founded"]),
            sector=data.get("sector", ""),
            mission=data.get("mission", ""),
            project_path=project_path,
            initial_capital=None,  # Will be loaded from financial_state
        )

        # Load departments
        for dept_data in data.get("departments", []):
            dept = Department.from_dict(dept_data)
            corp.departments[dept.department_id] = dept

        # Load employees
        for emp_data in data.get("employees", []):
            emp = Employee.from_dict(emp_data)
            corp.employees[emp.being_id] = emp

        # Load financial state
        if "financial_state" in data:
            corp.financial_state = FinancialState.from_dict(data["financial_state"])

        return corp
